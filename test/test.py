import unittest
from bs4 import BeautifulSoup
from nanorcc.parse import parse_tag, parse_rcc_file, get_rcc_data
from collections import OrderedDict
import pandas as pd



class TestParseTag(unittest.TestCase):
    """test the parse_tag function using example.RCC"""
    def setUp(self):
        with open('test/example.RCC','r') as f:
            soup = BeautifulSoup(f.read(),'html.parser')
        self.header_tag = soup.contents[0]
        self.sample_attributes_tag = soup.contents[2]
        self.lane_attributes_tag = soup.contents[4]
        self.code_summary_tag = soup.contents[6]
        self.messages_tag = soup.contents[8]

    def test_header(self):
        name,result = parse_tag(self.header_tag)
        self.assertDictEqual(
            result,
            {'FileVersion':'1.6','SoftwareVersion':'2.1.1.0005'}
        )
        self.assertEqual(name,'Header'.casefold())

    def test_sample_attributes(self):
        name,result = parse_tag(self.sample_attributes_tag)
        self.assertDictEqual(
            result,
            {
                'SampleID':'01',
                'Owner':'mk',
                'Comments':'50ng',
                'Date':'20100714',
                'GeneRLF':'NS_H_miR',
                'SystemAPF':'n6_vDV1',
            }
        )
        self.assertEqual(name,'Sample_Attributes'.casefold())

    def test_lane_attributes(self):
        name,result = parse_tag(self.lane_attributes_tag)
        self.assertDictEqual(
            result,
            {
                'LaneID':'1',
                'FovCount':'600',
                'FovCounted':'600',
                'ScannerID':'DA01',
                'StagePosition':'1',
                'BindingDensity':'0.22',
                'CartridgeID':'miRNAlinearity',
            }
        )
        self.assertEqual(name,'Lane_Attributes'.casefold())

    def test_code_summary(self):
        name,result = parse_tag(self.code_summary_tag)
        self.assertCountEqual(
            result,
            [
                {
                   'CodeClass':'Positive',
                   'Name':'POS_A(128)',
                   'Accession':'nmiR00813.1',
                   'Count':'8667',
                },
                {
                   'CodeClass':'Negative',
                   'Name':'NEG_C(0)',
                   'Accession':'nmiR00828.1',
                   'Count':'11',
                },
                {
                   'CodeClass':'Housekeeping',
                   'Name':'RPLP0|0',
                   'Accession':'NM_001002.3',
                   'Count':'137',
                },
                {
                   'CodeClass':'Endogenous1',
                   'Name':'hsa-miR-758|0',
                   'Accession':'nmiR00633.1',
                   'Count':'12',
                },
            ]
        )
        self.assertEqual(name,'Code_Summary'.casefold())

    def test_messages(self):
        name,result = parse_tag(self.messages_tag)
        self.assertEqual(name,'Messages'.casefold())
        self.assertEqual(result,'')

class TestParseRCCFile(unittest.TestCase):
    """test parse_rcc_file function"""
    def setUp(self):
        self.example = 'test/example.RCC'
        self.sample_data,self.genes = parse_rcc_file(self.example)
    def test_sample_data(self):
        self.assertIsInstance(self.sample_data,OrderedDict)
        self.assertEqual(self.sample_data['hsa-miR-758|0'],12.0)
        self.assertEqual(self.sample_data['NEG_C(0)'],11.0)
        self.assertEqual(len(self.sample_data),20)
    def test_genes(self):
        self.assertIsInstance(self.genes,list)
        [self.assertIsInstance(i,OrderedDict) for i in self.genes]
        self.assertEqual(len(self.genes),4)
        self.assertIn('CodeClass',self.genes[0].keys())
        self.assertIn('Accession',self.genes[0].keys())
        self.assertIn('Name',self.genes[0].keys())
    def test_full_file(self):
        data,genes = parse_rcc_file('test/full_file_test.RCC')
        self.assertEqual(len(genes),753)
        self.assertEqual(len(data),769)

class TestGetRccData(unittest.TestCase):
    """test get_rcc_data function"""
    def setUp(self):
        self.file_path = r'test\example_data_RCC\*RCC'
        self.data,self.genes = get_rcc_data(self.file_path)
    def test_input_type_raise(self):
        self.assertRaises(TypeError,get_rcc_data,12)
    def test_warning(self):
        self.assertWarns(UserWarning,get_rcc_data,self.file_path)
    def test_is_dataframe(self):
        self.assertIsInstance(self.data,pd.core.frame.DataFrame)
        self.assertIsInstance(self.genes,pd.core.frame.DataFrame)
    def test_output_size(self):
        self.assertTupleEqual(self.data.shape,(12,769))
        self.assertTupleEqual(self.genes.shape,(753,3))

if __name__ == "__main__":
    unittest.main()