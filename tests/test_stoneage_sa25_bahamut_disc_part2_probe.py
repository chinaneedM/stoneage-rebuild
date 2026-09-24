import unittest
from tools.stoneage_sa25_bahamut_disc_part2_probe import TARGETS, cdx_url, attrs

class T(unittest.TestCase):
    def test_target(self):
        self.assertTrue(any("snA=81429" in x for x in TARGETS))
    def test_cdx(self):
        self.assertIn("matchType=exact",cdx_url(TARGETS[0]))
    def test_attrs(self):
        x=attrs('<img src="https://truth.bahamut.com.tw/s01/x.jpg"><a href="/C.php?bsn=1571">x</a>')
        self.assertEqual(len(x),1)\n        self.assertIn("truth.bahamut.com.tw",x[0])

if __name__=="__main__":
    unittest.main()
