import unittest

from tools.stoneage_floor130_arbitration import (
    ARCHIVED2003_ALIGNED,
    PRESERVE_VERSION_FORK,
    RECOVERED25_ALIGNED,
    WARP_RUNTIME_CONFLICTING,
    WARP_RUNTIME_CONSISTENT,
    load_floor130_arbitration,
)


class Floor130ArbitrationTests(unittest.TestCase):

    def test_real_reports_preserve_two_sided_version_fork(self):
        arbitration = load_floor130_arbitration()
        self.assertEqual(arbitration.floor_id, 130)
        self.assertEqual(arbitration.resolution, PRESERVE_VERSION_FORK)
        self.assertIsNone(arbitration.selected_path)

        family = arbitration.by_path["family/130"]
        extra = arbitration.by_path["extra/130"]

        self.assertEqual(
            family.temporal_alignment,
            ARCHIVED2003_ALIGNED,
        )
        self.assertEqual(
            family.warp_consistency,
            WARP_RUNTIME_CONSISTENT,
        )
        self.assertEqual(
            extra.temporal_alignment,
            RECOVERED25_ALIGNED,
        )
        self.assertEqual(
            extra.warp_consistency,
            WARP_RUNTIME_CONFLICTING,
        )

        for row in arbitration.candidates:
            self.assertFalse(row.dat_static_exact)
            self.assertFalse(row.historical_static_exact)
            self.assertFalse(row.recovered25_static_exact)

    def test_candidates_remain_byte_divergent(self):
        arbitration = load_floor130_arbitration()
        self.assertEqual(
            len({row.sha256 for row in arbitration.candidates}),
            2,
        )


if __name__ == "__main__":
    unittest.main()
