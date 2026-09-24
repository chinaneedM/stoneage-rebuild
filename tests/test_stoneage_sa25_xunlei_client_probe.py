import unittest
from tools.stoneage_sa25_xunlei_client_probe import TARGET, cdx_url

class T(unittest.TestCase):
    def test_target(self):
        self.assertEqual(TARGET,"http://kuai.xunlei.com/d/DX1fAAJeiQBWT-tR9ee")
    def test_cdx(self):
        self.assertIn("matchType=exact",cdx_url(TARGET,"exact"))
        self.assertIn("matchType=prefix",cdx_url(TARGET,"prefix"))

if __name__=="__main__":
    unittest.main()
