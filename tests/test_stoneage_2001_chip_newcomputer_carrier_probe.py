import unittest
from tools.stoneage_2001_chip_newcomputer_carrier_probe import (
    IA_QUERIES,DM_QUERIES,ia_candidate,dm_candidate
)

class ChipCarrierProbeTests(unittest.TestCase):
    def test_queries_cover_carrier_and_client(self):
        joined="\n".join(q for _,q in IA_QUERIES)+"\n"+"\n".join(DM_QUERIES)
        self.assertIn("CHIP 新电脑",joined)
        self.assertIn("2001",joined)
        self.assertIn("stoneage2.0setup",joined.lower())

    def test_ia_requires_chinese_carrier_and_period_or_exact_client(self):
        self.assertTrue(ia_candidate({"title":"CHIP 新电脑 2001-11","year":2001,"date":"2001-11-01"}))
        self.assertTrue(ia_candidate({"title":"stoneage2.0setup.exe"}))
        self.assertFalse(ia_candidate({"title":"CHIP CD 11/2001 (Polish)","year":2001,"date":"2001-11-01"}))
        self.assertFalse(ia_candidate({"title":"CHIP 新电脑 2005-08","year":2005,"date":"2005-08-01"}))

    def test_dm_rejects_2005_chinese_false_positive(self):
        self.assertFalse(dm_candidate({"itemName":"Chip 2005 August (CD-ROM)","filename":"新电脑0508.iso"}))
        self.assertTrue(dm_candidate({"itemName":"CHIP 新电脑 2001-11","filename":"disc.iso"}))
        self.assertTrue(dm_candidate({"itemName":"carrier","filename":"stoneage2.0setup.exe"}))

if __name__=="__main__":
    unittest.main()
