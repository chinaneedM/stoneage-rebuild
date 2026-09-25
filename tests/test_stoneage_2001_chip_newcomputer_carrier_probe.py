import unittest
from tools.stoneage_2001_chip_newcomputer_carrier_probe import IA_QUERIES,DM_QUERIES,targetish_text

class ChipCarrierProbeTests(unittest.TestCase):
    def test_queries_cover_carrier_and_client(self):
        joined="\n".join(q for _,q in IA_QUERIES)+"\n"+"\n".join(DM_QUERIES)
        self.assertIn("CHIP 新电脑",joined)
        self.assertIn("2001",joined)
        self.assertIn("stoneage2.0setup",joined.lower())

    def test_relevance(self):
        self.assertTrue(targetish_text("CHIP 新电脑 2001 11"))
        self.assertTrue(targetish_text("stoneage2.0setup.exe"))
        self.assertFalse(targetish_text("unrelated magazine"))

if __name__=="__main__":
    unittest.main()
