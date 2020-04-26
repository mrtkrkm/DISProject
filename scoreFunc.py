import numpy as np
import pandas as pd

class Scores(object):
    def mean_squared_errors(y_predict,y_true):
        return sum(np.power(y_predict-y_true,2)/len(y_true))

    def rmse(y_predict, y_true):
        return np.sqrt(self.mean_squared_errors(y_predict, y_true))

    def create_csv(df,predict):
        ids=df.Id
        pred=predict
        df_sub=pd.DataFrame({"Id":ids, "SalePrice":predict})
        df_sub.to_csv("submission.csv", index=False)
        print(df_sub.shape)