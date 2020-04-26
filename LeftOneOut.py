import pandas as pd 
import numpy as np 
from Preprocess import PreProcess
from models.DecisionTreeRegressor import DecisionTreeRegressor
from scoreFunc import Scores
from tqdm import notebook

class LeftOneOut(object):
    def __init__(self, train_data, train_res, test_data, test_res):
        self.X_train=train_data
        self.y_train=train_res
        self.X_test=test_data
        self.y_test=test_res
    
    def fit(self):
        res={}
        regressor =DecisionTreeRegressor()
        regressor=regressor.fit(self.X_train, self.y_train, min_leaf=10,max_depth=8)
        pred_dectest = regressor.predict(self.X_test)
        daily_scoreDt=Scores.mean_squared_errors(pred_dectest, self.y_test)
        res['All_together']=daily_scoreDt
        for col in notebook.tqdm(self.X_train.columns):
            cols=[cols for cols in self.X_train.columns if cols!=col]
            regressor =DecisionTreeRegressor()
            regressor=regressor.fit(self.X_train[cols], self.y_train, min_leaf=10,max_depth=8)
            pred_dectest = regressor.predict(self.X_test[cols])
            daily_scoreDt=Scores.mean_squared_errors(pred_dectest, self.y_test)
            res[f'Without{col}']=daily_scoreDt
        return res
