import unittest
from tools.stoneage_waei_www9_exact_postdec6_ids import IDS, FROM, TO, exact_original, cdx_url


class TestExactPostDec6Ids(unittest.TestCase):
    def test_source_derived_range(self):
        self.assertEqual((min(IDS), max(IDS)), (35, 60))
        self.assertEqual(FROM, "20001207")
        self.assertEqual(TO, "20010112")

    def test_exact_dynamic_url(self):
        self.assertEqual(
            exact_original(35),
            "http://www9.waei.net:80/download/downloading.php?ID=35",
        )
        url = cdx_url(35)
        self.assertIn("matchType=exact", url)
        self.assertIn("downloading.php%3FID%3D35", url)


if __name__ == "__main__":
    unittest.main()
