import unittest
import bs4
from bs4 import BeautifulSoup
from nanorcc.parse import parse_tag, parse_rcc_file



class TestParseTag(unittest.TestCase):
    """test the parse_tag function using example.RCC"""
    def setUp(self):
        with open('test/example.RCC','r') as f:
            soup = BeautifulSoup(f.read(),'html.parser')
        self.header_tag = soup.contents[0]
        self.sample_attributes_tag = soup.contents[2]
        self.lane_attributes_tag = soup.contents[4]
        self.code_summary_tag = soup.contents[6]
        self.comments_tag = soup.contents[8]

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

    def test_comments(self):
        name,result = parse_tag(self.comments_tag)
        self.assertEqual(name,'Messages'.casefold())
        self.assertEqual(result,'')

class TestParseRCCFile(unittest.TestCase):
    def setUp(self):
        self.example = 'example.RCC'
        self.sample_data,self.genes = parse_rcc_file(self.example)
    def test_sample_data(self):
        self.assertIsInstance(self.sample_data,dict)
        self.assertEqual(self.sample_data['hsa-miR-758|0'],12.0)
        self.assertEqual(len(self.sample_data),20)
    def test_genes(self):
        self.assertIsInstance(self.genes,dict)
        self.assertEqual(len(self.genes.items()),4)
        self.assertIn('CodeClass',self.genes.keys())
        self.assertIn('Accession',self.genes.keys())
        self.assertIn('Name',self.genes.keys())

if __name__ == "__main__":
    unittest.main()