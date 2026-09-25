import unittest
from tools.stoneage_shiqi_blog_image_archive_probe import PATHS,HOST,cdx_url,avail_url

class ShiqiBlogImageArchiveProbeTests(unittest.TestCase):
    def test_five_exact_jpg_tokens(self):
        self.assertEqual(len(PATHS),5)
        self.assertTrue(all(p.endswith(".jpg") for p in PATHS))
        self.assertTrue(all("20201218" in p for p in PATHS))

    def test_archive_queries_keep_exact_host(self):
        u="http://"+HOST+PATHS[0]
        self.assertIn("matchType=exact",cdx_url(u))
        self.assertIn("timestamp=20201218",avail_url(u))

if __name__=="__main__":
    unittest.main()
