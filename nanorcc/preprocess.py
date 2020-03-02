import pandas as pd
import numpy as np

class GeneSelector(object):
    # TODO: make code_classes properties of this class and add mathematical
    # gene selection methods
    def __init__(self,genes,code_class=None,regex=None):
        self.genes = genes
        self.code_class = code_class
        self.regex = regex
    def get_cols(self):
        if self.code_class is None:
            gs = self.genes
        else:
            gs = self.genes.loc[self.genes['CodeClass']==self.code_class]
        if self.regex is None:
            pass
        else:
            gs = gs.loc[self.genes['Name'].str.contains(self.regex)]
        return(gs['Name'].tolist())


class Normalizer(object):
    def __init__(self,cols=r'',func='mean',drop_cols=True):
        self.cols = cols
        self.drop_cols = drop_cols
        if func == 'mean':
            self.func = np.mean
        elif func == 'median':
            self.func = np.median
        elif not callable(func):
            raise TypeError(
                'func must be "mean" or "median" or a callable '\
                    'function (e.g. scipy.stats.mstats.gmean)'
            )
        else:
            self.func = func
    def get_cols(self,df):
        if type(self.cols) == str:
            self.cols = df.filter(regex=self.cols).columns
        return(self.cols)

class BackgroundSubtract(Normalizer):
    def __init__(self,cols=r'^NEG\_[A-Z]\(\d+\)$',func='mean',drop_cols=True):
        super().__init__(cols,func,drop_cols)
    def eval(self,df):
        cols = self.get_cols(df)
        bg = df[cols].apply(self.func,axis=1)
        if self.drop_cols:
            df = df.drop(self.cols,axis=1)
        df = df.subtract(bg,axis='index')
        return(df)

class NormalizeUsingControls(Normalizer):
    def __init__(self,cols=r'^POS\_[A-Z]\(\d+\)$',func='mean',drop_cols=True):
        super().__init__(cols,func,drop_cols)
    def norm_factor(self,df):
        cols = self.get_cols(df)
        return(
            self.func(df[cols],axis=1)/self.func(self.func(df[cols],axis=1))
        )
    def eval(self,df):
        nf = self.norm_factor(df)
        if self.drop_cols:
            df = df.drop(self.cols,axis=1)
        df = df.multiply(nf,axis='index')
        return(df)
