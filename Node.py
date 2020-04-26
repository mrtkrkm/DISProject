import pandas as pd
import numpy as np
class Node:
    def __init__(self, attrs, target, idxs, min_leaf=10, max_depth=8,depth=0):
        self.attrs = attrs
        self.target = target
        self.idxs = idxs 
        self.min_leaf = min_leaf
        self.val = np.mean(target[idxs])
        self.score = np.inf
        self.max_depth=max_depth
        self.depth=depth
        self.find_varsplit()
        

    def find_varsplit(self):
        if self.depth==self.max_depth: 
            return
        else:
            self.depth +=1
            for col in range(self.attrs.shape[1]): 
                self.find_best_attr(col)
            if self.is_leaf: return
            attr = self.split_col
            below = np.nonzero(attr <= self.split)[0]
            above = np.nonzero(attr > self.split)[0]
            self.below = Node(self.attrs, self.target, self.idxs[below], self.min_leaf,max_depth=self.max_depth,depth=self.depth)
            self.above = Node(self.attrs, self.target, self.idxs[above], self.min_leaf,max_depth=self.max_depth,depth=self.depth)
        
    def find_best_attr(self, col_idx):
      
        attrs = self.attrs.values[self.idxs, col_idx]
        mean=attrs.mean()
        below=attrs<= mean
        above=attrs>  mean
        
        if above.sum() < self.min_leaf or below.sum() < self.min_leaf: return
        curr_score = self.calculate_var(below, above)
        if curr_score < self.score: 
            self.col_idx = col_idx
            self.score = curr_score
            self.split = mean
                
    def calculate_mse(self,ix):
        target=self.target[self.idxs]
        ys=target[ix]
        mean=ys.mean()
        mse=sum(np.power(ys-mean,2)/len(ix))
        return mse
    
    def calculate_var(self,below,above):
        total=len(below)+len(above)
        propL=len(below)/total
        propR=len(above)/total
        
        var=(propL*self.calculate_mse(below)+propR*self.calculate_mse(above))
        return var
                
    @property
    def split_col(self): return self.attrs.values[self.idxs,self.col_idx]
                
    @property
    def is_leaf(self): return self.score == np.inf                

    def predict(self, samples):
        return np.array([self.predict_row(sample) for sample in samples])

    def predict_row(self, sample):
        if self.is_leaf: return self.val
        node = self.below if sample[self.col_idx] <= self.split else self.above
        return node.predict_row(sample)