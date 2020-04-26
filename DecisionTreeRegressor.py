from Node import Node
import pandas as pd
import numpy as np
class DecisionTreeRegressor(object):
    def fit(self, X, y, min_leaf = 10, max_depth=6):
        X.index=range(0, X.shape[0],1)
        y.index=range(0, X.shape[0],1)
        self.endi=X.index.stop
        #y_test.index=range(4320, 4320+X_test.shape[0],1)
        self.dtree = Node(X, y, np.array(np.arange(len(y))), min_leaf, max_depth=max_depth, depth=0)
        return self
    def predict(self, X):
        X.index=range(self.endi, self.endi+X.shape[0],1)
        return self.dtree.predict(X.values)