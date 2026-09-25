import unittest
from tools.stoneage_2000_sina_aid_probe import relevant
class AidProbeTests(unittest.TestCase):
    def test_aid_variant(self):
        r=relevant([{"original":"http://x/download.pl?size=1410&aid=23223&col=map"}])
        self.assertEqual(len(r),1)
    def test_filename_variant(self):
        r=relevant([{"original":"http://x/download.pl?filename=samap_1220.zip"}])
        self.assertEqual(len(r),1)
if __name__=="__main__":unittest.main()
