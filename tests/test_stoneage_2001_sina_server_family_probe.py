import unittest
from tools.stoneage_2001_sina_server_family_probe import directory_of,is_target,TARGETS

class Sina2001ServerFamilyTests(unittest.TestCase):
    def test_directory(self):
        self.assertEqual(directory_of("http://202.0.0.1/map_1004/a.zip"),"/map_1004/")

    def test_target_detection(self):
        self.assertTrue(is_target("http://x/a/Estoneage2.0map_1127.exe"))
        self.assertTrue(is_target("http://x/a/stoneage2.0setup.exe"))
        self.assertFalse(is_target("http://x/a/other.zip"))
        self.assertEqual(len(TARGETS),2)

if __name__=="__main__":
    unittest.main()
