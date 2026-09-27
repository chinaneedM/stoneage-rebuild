import unittest
from tools.stoneage_waei_www9_fast_cdx_probe import cdx_url,did
class FastWww9CdxTests(unittest.TestCase):
    def test_no_collapse(self):
        u=cdx_url("http://www9.waei.net/download.php?Dcat_ID=2","exact")
        self.assertNotIn("collapse",u)
        self.assertIn("matchType=exact",u)
    def test_id(self):
        self.assertEqual(did("http://www9.waei.net/download/downloading.php?ID=35"),"35")
        self.assertEqual(did("http://x"),"")
if __name__=="__main__":unittest.main()
