import unittest
from tools.stoneage_waei_www9_root_20001206_retry import clean,plain,relevant

class T(unittest.TestCase):
    def test_plain(self):
        self.assertEqual(plain("<b>試玩</b>")," 試玩 ")
    def test_relevant(self):
        self.assertTrue(relevant("http://x/download.php?Dcat_ID=2","試玩版"))
    def test_clean_pipe(self):
        self.assertIn("%7C",clean("a|b"))

if __name__=="__main__":unittest.main()
