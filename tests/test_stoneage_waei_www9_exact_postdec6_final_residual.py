import unittest
from tools.stoneage_waei_www9_exact_postdec6_final_residual import (
    IDS, VARIANTS, original, cdx_url,
)

class TestFinalResidual(unittest.TestCase):
    def test_only_remaining_ids(self):
        self.assertEqual(IDS,(59,60))
        self.assertEqual(VARIANTS,("port80","noport"))
    def test_both_url_forms(self):
        self.assertIn(":80/download/downloading.php?ID=59",original(59,"port80"))
        self.assertNotIn(":80/download",original(59,"noport"))
        self.assertIn("matchType=exact",cdx_url(60,"noport"))

if __name__=="__main__":
    unittest.main()
