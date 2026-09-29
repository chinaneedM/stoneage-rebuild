import unittest

from tools.stoneage_materializable_world_geometry_probe import (
    NON_SINGLE_SOURCE,
    OUTSIDE_REPRESENTED_WORLD,
    UNRESOLVED_DESTINATION,
    UNRESOLVED_SOURCE,
    classify_warps,
)
from tools.stoneage_versioned_world_geometry_probe import ClassicWarpGeometry


def _warp(
    source,
    destination,
    *,
    source_rect=(1, 1, 1, 1),
    destination_xy=(2, 2),
):
    return ClassicWarpGeometry(
        source_floor=source,
        placement_id=1,
        source_rect=source_rect,
        destination_floor=destination,
        destination_x=destination_xy[0],
        destination_y=destination_xy[1],
        conditional_time=False,
        destination_is_stable_candidate=False,
    )


class MaterializableWorldGeometryProbeTests(unittest.TestCase):

    def test_unresolved_and_outside_edges_are_quarantined(self):
        audit = classify_warps(
            materializable_dimensions={
                1: (10, 10),
                2: (10, 10),
            },
            unresolved_floor_ids={130},
            represented_floor_ids={1, 2, 130},
            warps=(
                _warp(1, 2),
                _warp(1, 130),
                _warp(130, 1),
                _warp(1, 40),
            ),
        )
        self.assertEqual(len(audit.materializable_warps), 1)
        reasons = [row.reason for row in audit.quarantined_warps]
        self.assertEqual(
            reasons,
            [
                UNRESOLVED_DESTINATION,
                UNRESOLVED_SOURCE,
                OUTSIDE_REPRESENTED_WORLD,
            ],
        )

    def test_non_single_source_is_not_collapsed(self):
        audit = classify_warps(
            materializable_dimensions={1: (10, 10), 2: (10, 10)},
            unresolved_floor_ids=set(),
            represented_floor_ids={1, 2},
            warps=(
                _warp(
                    1,
                    2,
                    source_rect=(1, 1, 2, 1),
                ),
            ),
        )
        self.assertEqual(len(audit.materializable_warps), 0)
        self.assertEqual(audit.quarantined_warps[0].reason, NON_SINGLE_SOURCE)


if __name__ == "__main__":
    unittest.main()
