import unittest

from tools.stoneage_shadowed_branch_fresh_start_coordinate_gap_probe import (
    _frontier_reason,
    _reverse_floor_distances,
)
from tools.stoneage_shadowed_branch_fresh_start_coordinate_probe import WarpEdge


class FreshStartCoordinateGapProbeTests(unittest.TestCase):

    def test_reverse_floor_distances(self):
        rows=_reverse_floor_distances(
            [
                WarpEdge(1,0,0,2,0,0),
                WarpEdge(2,0,0,3,0,0),
                WarpEdge(4,0,0,2,0,0),
            ],
            3,
        )
        self.assertEqual(rows[3],0)
        self.assertEqual(rows[2],1)
        self.assertEqual(rows[1],2)
        self.assertEqual(rows[4],2)

    def test_frontier_reason_prefers_static_source_disconnect(self):
        self.assertEqual(
            _frontier_reason(
                min_remaining=2,
                source_disconnected=3,
                destination_invalid=0,
                usable=0,
                start_valid=True,
            ),
            "CLASSIC_WARP_SOURCE_COMPONENT_DISCONNECTED",
        )

    def test_frontier_reason_identifies_award_component_mismatch(self):
        self.assertEqual(
            _frontier_reason(
                min_remaining=0,
                source_disconnected=0,
                destination_invalid=0,
                usable=0,
                start_valid=True,
            ),
            "AWARD_LOCAL_COMPONENT_MISMATCH",
        )


if __name__=="__main__":
    unittest.main()
