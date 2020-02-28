import unittest
import bs4
from bs4 import BeautifulSoup
from unittest.mock import MagicMock
from nanorcc.parse import parse_tag



class TestParseTag(unittest.TestCase):
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
        self.assertEqual(name,'Header')

    def test_sample_attributes(self):
        name,result = parse_tag(self.sample_attributes_tag)
        self.assertDictEqual(
            result,
            {
                'ID':'01',
                'Owner':'mk',
                'Comments':'50ng',
                'Date':'20100714',
                'GeneRLF':'NS_H_miR',
                'SystemAPF':'n6_vDV1',
            }
        )
        self.assertEqual(name,'Sample_Attributes')

    def test_lane_attributes(self):
        name,result = parse_tag(self.sample_attributes_tag)
        self.assertDictEqual(
            result,
            {
                'ID':'01',
                'Owner':'mk',
                'Comments':'50ng',
                'Date':'20100714',
                'GeneRLF':'NS_H_miR',
                'SystemAPF':'n6_vDV1',
            }
        )
        self.assertEqual(name,'Sample_Attributes')
    def test_lane_attributes():
        name,result = parse_tag(self.lane_attributes_tag)
        self.assertDictEqual(
            result,
            {
                'ID':'1',
                'FovCount':'600',
                'FovCounted':'600',
                'ScannerID':'DA01',
                'StagePosition':'1',
                'BindingDensity':'0.22',
                'CartridgeID':'miRNAlinearity',
            }
        )
        self.assertEqual(name,'Lane_Attributes')
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
        self.assertEqual(name,'Code_Summary')
    def test_comments(self):
        name,result = parse_tag(self.comments_tag)
        self.assertEqual(name,'Comments')
        self.assertEqual(result,'')

if __name__ == "__main__":
    unittest.main()