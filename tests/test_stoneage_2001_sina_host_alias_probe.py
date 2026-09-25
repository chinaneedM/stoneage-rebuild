import unittest
from tools.stoneage_2001_sina_host_alias_probe import TARGET_AID,TARGET_FILENAME,relevant,extract_route_values

class Sina2001HostAliasTests(unittest.TestCase):
    def test_identity(self):
        self.assertEqual(TARGET_AID,"43172")
        self.assertEqual(TARGET_FILENAME,"Estoneage2.0map_1127.exe")

    def test_relevant(self):
        self.assertTrue(relevant({"original":"http://x/download.pl?aid=43172&filename=x"}))
        self.assertTrue(relevant({"original":"http://x/download.pl?filename=Estoneage2.0map_1127.exe"}))
        self.assertFalse(relevant({"original":"http://x/download.pl?aid=1&filename=other.exe"}))

    def test_extract_route(self):
        b=b'<a href="http://202.0.0.1/down/Estoneage2.0map_1127.exe">x</a>'
        self.assertIn("http://202.0.0.1/down/Estoneage2.0map_1127.exe",extract_route_values(b,"http://x/"))

if __name__=="__main__":
    unittest.main()
