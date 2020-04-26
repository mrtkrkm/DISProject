from DecisionTreeRegressor import DecisionTreeRegressor
import numpy as np
class RandomForestRegressor(object):
    def __init__(self, X, y, min_leaf, max_depth=None, tree_number=5, max_feature=None, max_sample=None,random_seed=0, bootstrap=True):
        self.X=X
        self.target=y
        self.min_leaf=min_leaf
        self.max_depth=max_depth
        self.tree_number=tree_number
        self.max_feature=max_feature
        self.max_sample=max_sample
        if self.max_sample==None:
            self.max_sample=self.X.shape[0]
        self.dtrees=[]
        self.random_seed=random_seed
        self.bootstrap=bootstrap
        X.index=range(0, X.shape[0],1)
        y.index=range(0, X.shape[0],1)
        self.endi=X.index.stop
    def fit(self):
        for i,dtree in enumerate(range(self.tree_number)):
            np.random.seed(self.random_seed+i)
            new_inds=np.random.choice(np.arange(self.X.shape[0]), self.max_sample, replace=self.bootstrap)
            new_features=np.sort(np.random.choice(np.arange(self.X.shape[1]), self.max_feature, replace=False))
            newx=self.X.iloc[new_inds, :]
            newx.index=range(0, newx.shape[0],1)
            newy=self.target[new_inds]
            newy.index=range(0, len(newy),1)
            self.dtrees.append(DecisionTreeRegressor().fit(newx, newy, min_leaf=self.min_leaf,max_depth=self.max_depth).dtree)
        return self
    def predict(self,data):
        alls=np.zeros((len(self.dtrees), data.shape[0]))
        for i,dtree in enumerate(self.dtrees):
            alls[i,:]=dtree.predict(data.values)
        return np.mean(alls, axis=0)      