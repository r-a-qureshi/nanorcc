
from nanorcc.parse import *
from nanorcc.preprocess import *
from nanorcc.quality_control import *
import unittest
import pandas as pd
import numpy as np

class TestQC(unittest.TestCase):
    def setUp(self):
        counts,genes = get_rcc_data('test/example_data_RCC/*.RCC')
        self.counts = counts
        self.genes = genes
        self.qc = QualityControl()
    def test_fov(self):
        counts = self.qc.fov_qc(self.counts)
        self.assertFalse(self.counts['FOV QC'].any())
    def test_bad_fov(self):
        counts = self.counts.copy()
        counts.loc[5,'FovCounted'] = 10
        counts = self.qc.fov_qc(counts)
        self.assertEqual(counts['FOV QC'].sum(),1)
        self.assertTrue(counts.loc[5,'FOV QC'])
    def test_binding_density(self):
        counts = self.qc.binding_density_qc(self.counts)
        self.assertFalse(counts['Binding Density QC'].any())
    def test_bad_binding_density(self):
        counts = self.counts.copy()
        counts.loc[5,'BindingDensity'] = 100
        counts.loc[6,'BindingDensity'] = 0.00001
        counts = self.qc.binding_density_qc(counts)
        self.assertEqual(counts['Binding Density QC'].sum(),2)
        self.assertTrue(counts.loc[5,'Binding Density QC'],True)
        self.assertTrue(counts.loc[6,'Binding Density QC'],True)
    def test_pos_control_linearity(self):
        counts = self.qc.pos_control_linearity_qc(self.counts)
        self.assertFalse(counts['Positive Control Linearity QC'].any())
    def test_bad_pos_control_linearity(self):
        counts = self.counts.copy()
        counts.loc[5,'POS_A(128)']=0
        counts.loc[5,'POS_E(0.5)']=10000
        counts = self.qc.pos_control_linearity_qc(counts)
        self.assertTrue(counts.loc[5,'Positive Control Linearity QC'])
    def test_drop_failed_qc(self):
        counts = self.qc.drop_failed_qc(self.counts)
        self.assertEqual(counts.shape[0],12)
    def test_bad_drop_failed_qc(self):
        counts = self.counts.copy()
        counts.loc[5,'FovCounted'] = 10
        counts.loc[10,'BindingDensity'] = 100
        counts = self.qc.drop_failed_qc(counts)
        self.assertEqual(counts.shape[0],10)
        self.assertNotIn(5,counts.index)
        self.assertNotIn(10,counts.index)

if __name__ == "__main__":
    unittest.main()