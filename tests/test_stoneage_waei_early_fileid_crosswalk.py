import unittest
from tools.stoneage_waei_early_fileid_crosswalk import cdx,IDS

class T(unittest.TestCase):
    def test_ids(self): self.assertEqual((min(IDS),max(IDS)),(30,40))
    def test_url(self):
        orig,url=cdx(35,True)
        self.assertIn("fileid=35",orig)
        self.assertIn("matchType=exact",url)

if __name__=="__main__":unittest.main()
