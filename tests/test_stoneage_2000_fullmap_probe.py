import unittest
from tools.stoneage_2000_fullmap_probe import FILENAME,AID,source_hrefs
class FullMap2000Tests(unittest.TestCase):
    def test_target(self):
        self.assertEqual(FILENAME,"samap_1220.zip");self.assertEqual(AID,"23223")
    def test_href(self):
        b=b'<a href="http://games1.sina.com.cn/cgi-bin/games/downgames/download.pl?col=map&aid=23223&filename=samap_1220.zip&size=1410">x</a>'
        r=source_hrefs(b);self.assertEqual(len(r),1);self.assertIn(FILENAME,r[0])
if __name__=="__main__": unittest.main()
