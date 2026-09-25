import unittest
from tools.stoneage_2001_fullmap_probe import FILENAME, AID, source_hrefs

class FullMap2001Tests(unittest.TestCase):
    def test_target(self):
        self.assertEqual(FILENAME,"Estoneage2.0map_1127.exe")
        self.assertEqual(AID,"43172")
    def test_extract_exact_href(self):
        b=b'<a href="http://games1.sina.com.cn/cgi-bin/games/downgames/download.pl?col=map&aid=43172&filename=Estoneage2.0map_1127.exe&size=1911">x</a>'
        r=source_hrefs(b)
        self.assertEqual(len(r),1)
        self.assertIn("aid=43172",r[0])
        self.assertIn(FILENAME,r[0])

if __name__=="__main__":
    unittest.main()
