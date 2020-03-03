import pandas as pd
import numpy as np
from collections import UserDict

class CodeClassGeneSelector(UserDict):
    """Class for easy access to genes by their code class"""
    def __init__(self,df):
        if 'CodeClass' not in df.columns:
            raise ValueError(
                'df must be a gene DataFrame returned by '\
                'parse.get_rcc_data'
            )
        else:
            self.df = df
        self.gene_dict = (
            df.groupby('CodeClass')
            .apply(lambda x: x.to_dict('list'))
            .to_dict()
        )
        super().__init__(
            df.groupby('CodeClass')
            .apply(lambda x: x.drop('CodeClass',axis=1).to_dict('list'))
            .to_dict()
        )
    def get(self,code_class,field='Name'):
        return(self.gene_dict[code_class][field])

def _check_func(func):
    """Check the function to make sure it is valid"""
    if func == 'mean':
        func = np.mean
    elif func == 'median':
        func = np.median
    elif func == 'std':
        func = np.std
    elif not callable(func):
        raise TypeError(
            'func must be "mean" or "median" or a callable '\
                'function (e.g. scipy.stats.mstats.gmean)'
        )
    else:
        func = func
    return(func)
    
class FunctionGeneSelector():
    """Choose genes for normalization based on the data. For example you can 
    use the 100 genes with least standard deviation for normalization."""
    def __init__(self,func='std',n=100,select_least=True):
        self.func = _check_func(func)
        self.n = n
        self.select_least = select_least
    def get(df):
        if self.select_least:
            genes = df.apply(self.func).nsmallest(n).index
        else:
            genes = df.apply(self.func).nlargest(n).index
        return(genes)

class Normalize():
    def __init__(self,raw_data):
        self.raw_data = raw_data
        self.norm_data = raw_data.copy()
    def _check_func(self,func):
        """Check the function to make sure it is valid"""
        if func == 'mean':
            func = np.mean
        elif func == 'median':
            func = np.median
        elif not callable(func):
            raise TypeError(
                'func must be "mean" or "median" or a callable '\
                    'function (e.g. scipy.stats.mstats.gmean)'
            )
        else:
            func = func
        return(func)
    def _check_genes(self,genes):
        if isinstance(genes,FunctionGeneSelector):
            genes = genes.get(self.norm_data)
        else:
            pass
        return(genes)
    def background_subtract(self,genes,func='mean',drop_genes=True):
        """Subtract background using negative controls."""
        func = self._check_func(func)
        genes = self._check_genes(genes)
        bg = self.norm_data[genes].apply(func,axis=1)
        if drop_genes:
            self.norm_data = self.norm_data.drop(genes,axis=1)
        self.norm_data = self.norm_data.subtract(bg,axis='index')
    def _scale_factor(self,genes,func='mean'):
        func = self._check_func(func)
        genes = self._check_genes(genes)
        scale_factor = func(self.norm_data[genes],axis=1)\
            /func(func(self.norm_data[genes],axis=1))
        return(scale_factor)
    def scale_by_genes(self,genes,func='mean',drop_genes=True):
        """Normalize against a set of genes usually positive controls or
        housekeeping genes."""
        sf = self._scale_factor(self.norm_data)
        genes = self._check_genes(genes)
        if drop_genes:
            self.norm_data = self.norm_data.drop(genes,axis=1)
        self.norm_data = self.norm_data.multiply(sf,axis='index')
    def quantile(self):
        """Performs Quantile normalization on a data frame where samples are rows
        and genes are columns."""
        m_rank = self.norm_data.rank(axis=1)
        m_sorted = self.norm_data.apply(
            lambda x: np.sort(x.values),axis=1,result_type='expand'
        )
        m_sorted.columns = self.norm_data.columns
        mean_vals = m_sorted.mean(axis=0)
        qnm = m_rank.apply(lambda x: np.interp(
            x,np.arange(1,m_rank.shape[1]+1),mean_vals),axis=1,
            result_type='expand'
        )
        qnm.columns = self.norm_data.columns
        self.norm_data = qnm