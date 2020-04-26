import pandas as pd
import numpy as np

class PreProcess(object):
    def __init__(self, df, ddir, target_col, shift_day):
        self.df=df
        self.ddir=ddir
        self.target_col=target_col
        self.df_dis=None
        self.cols=['Date Time']
        self.X=None
        self.y=None
        self._get_target(target_col)
        self._shift_features(shift_day)
        
    def _get_target(self, col):
        self.X= self.df.filter(items=list(set(self.df.columns)-set([col])))
        self.y= self.df.filter(items=[col])
    
    def _shift_features(self, shift_d):
        cols=[col for col in self.df.columns if col!='Date Time']
        for col in cols:
            for i in range(1,shift_d+1):
                self.df[f"{col}shift-{i}"]=self.df[col].shift(i)
                #self.df[f"shift-{i}-wd"]=self.df["wd (deg)"].shift(i)
                self.cols.append(f"{col}shift-{i}")
                #self.cols.append(f"shift-{i}-wd")
            
            
    def _convert_todate(self, lss, year):
        date=str(year)+'-'+lss[2:4]+'-'+lss[0:2]+' '+lss[4:6]+':'+lss[6:]
        if date[:10]==str(year)+"-02-29" and year%4!=0:
            date='2017-12-31 00:00'
        return date
    
    def _txt_tocsv(self,ddir, year):
        dates=[]
        vals=[]
        with open(ddir, 'r') as file:
            for line in file:
                dates.append(self._convert_todate(line[1:9], year))
                vals.append(line[12:-2].split(','))
        dfs=pd.DataFrame(vals)
        dfs.insert(loc=0, column='Date', value=dates)
        dfs.sort_values(by="Date", inplace=True)
        dfs = dfs.reset_index(drop=True)
        

        dfs.columns=['Date Time', 'p (mbar)', 'T (degC)', 'Tpot (K)', 'Tdew (degC)',
          'rh (%)', 'VPmax (mbar)', 'VPact (mbar)', 'VPdef (mbar)', 'sh (g/kg)',
          'H2OC (mmol/mol)', 'rho (g/m**3)', 'wv (m/s)', 'max. wv (m/s)',
          'wd (deg)']
        dfs["Date Time"]=pd.to_datetime(dfs["Date Time"])
        self.df_dis=dfs
    
    def _create_feature(self,target_col,df1,df_tr, df_test, day_number,day_pred, day_start):
        inds=df1.index[df1['Date Time']==df_tr.iloc[0,0]][0]
        day_end=day_number
        end_of=inds+(day_end*144)
        days_s=144*day_start

        ind_s=df1.iloc[day_start].index
        a=df1[inds:end_of][target_col]
        print(inds)
        b=df1[end_of:end_of+(144*day_pred)][target_col]
        print(b.shape)
        a.index=range(df_tr.index.start, df_tr.index.stop, df_tr.index.step)
        b.index=range(df_test.index.start, df_test.index.stop, df_test.index.step)

        df_tr["avg"]=a.astype('float')
        df_test["avg"]=b.astype('float')
        self.cols.append('avg')
        return df_tr, df_test
    
    def _check_drop(self, df):
        df.fillna(0, inplace=True)
        if 'Date Time' in self.cols:
            self.cols.remove('Date Time')
        df.drop(['Date Time'], inplace=True, axis=1)
        return df
    
    def split_data(self, day_number,day_pred, day_start):
        ind_start=144*day_start
        day_end=day_start+day_number
        day_before=day_end*144
        

        df_train=self.df.iloc[ind_start:day_before]
        self._txt_tocsv(self.ddir, df_train.loc[ind_start, 'Date Time'].year)
        df_test=self.df.iloc[day_before:day_before+(144*day_pred)]
        df_train, df_test=self._create_feature(self.target_col,self.df_dis,df_train, df_test, day_number,day_pred, day_start)
        y_tr=self.y.iloc[ind_start:day_before,0]
        y_test=self.y.iloc[day_before:day_before+(144*day_pred),0]
        
        df_train=self._check_drop(df_train)
        df_test=self._check_drop(df_test)
        
        return df_train[self.cols], y_tr, df_test[self.cols], y_test
    