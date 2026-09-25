import unittest
from tools.stoneage_xinhaonanhai_archive_probe import relevant_url
class ContributorProbeTests(unittest.TestCase):
    def test_target_relevant(self):
        self.assertTrue(relevant_url("http://www.xinhaonanhai.com/down/Estoneage2.0map_1127.exe"))
    def test_2000_map_target(self):
        self.assertTrue(relevant_url("http://www.xinhaonanhai.com/down/samap_1220.zip"))
    def test_stoneage_zip_relevant(self):
        self.assertTrue(relevant_url("http://www.xinhaonanhai.com/stoneage/map.zip"))
    def test_unrelated_false(self):
        self.assertFalse(relevant_url("http://www.xinhaonanhai.com/images/logo.gif"))
if __name__=="__main__":
    unittest.main()
