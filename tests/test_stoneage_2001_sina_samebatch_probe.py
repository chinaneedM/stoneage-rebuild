import unittest
from tools.stoneage_2001_sina_samebatch_probe import download_links, targetish, TARGET_AID, TARGET_FILENAME

class SameBatchProbeTests(unittest.TestCase):
    def test_extract_map_download(self):
        b=b'<a href="http://games1.sina.com.cn/cgi-bin/games/downgames/download.pl?col=map&aid=43172&filename=Estoneage2.0map_1127.exe&size=1911">x</a>'
        rows=download_links(b,"https://games.sina.com.cn/downgames/map/11271899.shtml")
        self.assertEqual(len(rows),1)
        _,p=rows[0]
        self.assertEqual(p["aid"],TARGET_AID)
        self.assertEqual(p["filename"],TARGET_FILENAME)

    def test_ignore_non_map(self):
        b=b'<a href="http://games1.sina.com.cn/cgi-bin/games/downgames/download.pl?col=demo&aid=1&filename=x.exe">x</a>'
        self.assertEqual(download_links(b,"https://games.sina.com.cn/"),())

    def test_targetish(self):
        self.assertTrue(targetish({"aid":TARGET_AID}))
        self.assertTrue(targetish({"filename":TARGET_FILENAME.lower()}))
        self.assertFalse(targetish({"aid":"1","filename":"other.zip"}))

if __name__=="__main__":
    unittest.main()
