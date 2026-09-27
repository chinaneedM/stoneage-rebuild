import unittest
from tools.stoneage_waei_legacy_download_id_crosswalk import cdx,IDS
class T(unittest.TestCase):
    def test_ids(self): self.assertEqual((min(IDS),max(IDS)),(30,40))
    def test_path(self):
        orig,url=cdx(35,True)
        self.assertIn("downloading.php?ID=35",orig)
        self.assertIn("matchType=exact",url)
if __name__=="__main__":unittest.main()
