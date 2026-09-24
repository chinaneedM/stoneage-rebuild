import unittest
from tools.stoneage_sa25_collector_archive_probe import cdx_url, clean

class T(unittest.TestCase):
    def test_cdx_url(self):
        u=cdx_url("https://example.com/a.jpg")
        self.assertIn("matchType=exact",u)
        self.assertIn("output=json",u)
        self.assertIn("a.jpg",u)
    def test_clean(self):
        self.assertEqual(clean("a|b"),"a%7Cb")

if __name__=="__main__":
    unittest.main()
