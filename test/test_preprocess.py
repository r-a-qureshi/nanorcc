from nanorcc.parse import *
from nanorcc.preprocess import *
import unittest
import pandas as pd
import numpy as np

class TestCodeClassGeneSelector(unittest.TestCase):
    """Test CodeClassGeneSelector"""
    def setUp(self):
        counts,genes = get_rcc_data('test/example_data_RCC/*.RCC')
        self.ccgs = CodeClassGeneSelector(genes)
    def test_gene_selector(self):
        hk = ['RPLP0|0','RPL19|0','ACTB|0','GAPDH|0','B2M|0']
        hk.sort()
        self.assertListEqual(
            self.ccgs.get('Housekeeping'),
            hk,
        )
        self.assertEqual(len(self.ccgs.get('Endogenous1')),654)

class TestNormalize(unittest.TestCase):
    """Test CodeClassGeneSelector"""
    def setUp(self):
        counts,genes = get_rcc_data('test/example_data_RCC/*.RCC')
        self.counts = counts
        self.genes = genes
        self.ccgs = CodeClassGeneSelector(genes)
        self.norm = Normalize(counts,genes)
    def test_background_subtract(self):
        bg = self.counts[self.ccgs.get('Negative')].mean(axis=1)
        self.assertEqual(len(bg),12)
        self.norm.background_subtract(genes=self.ccgs.get('Negative'))
        test_gene = self.ccgs.get('Endogenous1')[10]
        self.assertAlmostEqual(
            self.counts.loc[3,test_gene]-bg.loc[3],
            self.norm.norm_data.loc[3,test_gene],
            delta=0.1
        )
        np.testing.assert_allclose(
            self.norm.norm_data.values,
            (self.counts[self.genes['Name']]
                .subtract(bg,axis='index')
                .drop(self.ccgs.get('Negative'),axis=1)
                .values
            ),
            rtol=.01,
        )
    def test_scale_by_genes(self):
        avg_per_sample = np.mean(self.counts[self.ccgs.get('Positive')],axis=1)
        overall_avg = np.mean(avg_per_sample)
        scale_factor = avg_per_sample/overall_avg
        np.testing.assert_allclose(
            scale_factor,
            self.norm._scale_factor(genes=self.ccgs.get('Positive')).values,
            rtol=.01,
        )
        self.norm.scale_by_genes(self.ccgs.get('Positive'))
        np.testing.assert_allclose(
            (self.counts[self.genes['Name']]
                .multiply(scale_factor,axis='index')
                .drop(self.ccgs.get('Positive'),axis=1)
                .values
            ),
            self.norm.norm_data.values,
            rtol=.01,
        ) 
    def test_quantile(self):
        self.norm.quantile()
        shape = self.norm.norm_data.shape
        np.testing.assert_allclose(
            self.norm.norm_data.mean(axis=1).values,
            np.repeat(self.norm.norm_data.iloc[0].mean(),shape[0]),
            rtol=.01,
        )
        np.testing.assert_allclose(
            self.norm.norm_data.std(axis=1).values,
            np.repeat(self.norm.norm_data.iloc[0].std(),shape[0]),
            rtol=.01,
        )
    #TODO: write tests for FunctionGeneSelector