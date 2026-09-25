import unittest
from tools.stoneage_2001_sa20_coverdisc_census import CARRIERS, walk_rows

class SA20CarrierCensusTests(unittest.TestCase):
    def test_carrier_count(self):
        self.assertEqual(len(CARRIERS),13)
        self.assertIn(("jinghe-ruby","晶合秘藏 红宝石"),CARRIERS)

    def test_walk_rows_dedup(self):
        row={"itemid":"1","itemName":"disc","fileid":"disc/stoneage.exe","b3sum":"a"}
        rows=walk_rows({"a":[row,row]})
        self.assertEqual(len(rows),1)

if __name__=="__main__":
    unittest.main()
