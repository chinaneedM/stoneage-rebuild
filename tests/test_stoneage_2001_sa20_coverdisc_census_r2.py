import unittest
from tools.stoneage_2001_sa20_coverdisc_census_r2 import CARRIERS, title_query

class SA20CarrierCensusR2Tests(unittest.TestCase):
    def test_carriers(self):
        self.assertEqual(len(CARRIERS),13)
    def test_title_query(self):
        self.assertIn('title:"PC任我行"',title_query("PC任我行","pc-renwoxing"))
        self.assertIn("mediatype:software",title_query("PC任我行","pc-renwoxing"))
        self.assertIn("year:2001",title_query("电脑","computer-magazine"))

if __name__=="__main__":
    unittest.main()
