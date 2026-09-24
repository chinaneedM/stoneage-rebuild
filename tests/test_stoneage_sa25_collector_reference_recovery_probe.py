import unittest
from tools.stoneage_sa25_collector_reference_recovery_probe import OFFICIAL_HTTP,cdx_url
from tools.stoneage_sa25_physical_image_fingerprint_probe import OFFICIAL_MAINLAND_REFERENCE

class T(unittest.TestCase):
    def test_reference(self):
        self.assertTrue(OFFICIAL_MAINLAND_REFERENCE.endswith("/5fe128952732d.jpg"))
        self.assertTrue(OFFICIAL_HTTP.startswith("http://"))
    def test_cdx_prefix(self):
        u=cdx_url("http://example.com/a","prefix")
        self.assertIn("matchType=prefix",u)
        self.assertIn("output=json",u)

if __name__=="__main__":
    unittest.main()
