import unittest

from tools.stoneage_sa25_disc_region_match_probe import (
    STANDALONE,
    bbox_coverage,
    polygon_area,
    sane_quad,
)


class DiscRegionMatchProbeTests(unittest.TestCase):
    def test_bbox_coverage(self):
        self.assertAlmostEqual(bbox_coverage([(0, 0), (50, 50)], 100, 100), 0.25)
        self.assertEqual(bbox_coverage([], 100, 100), 0.0)

    def test_polygon_area(self):
        self.assertAlmostEqual(polygon_area([(0, 0), (10, 0), (10, 10), (0, 10)]), 100.0)

    def test_sane_quad(self):
        ok, ratio = sane_quad([(10, 10), (90, 10), (90, 90), (10, 90)], 100, 100)
        self.assertTrue(ok)
        self.assertAlmostEqual(ratio, 0.64)
        ok, _ = sane_quad([(0, 0), (0, 0), (0, 0), (0, 0)], 100, 100)
        self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()
