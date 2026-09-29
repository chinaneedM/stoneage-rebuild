import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.stoneage_ambiguous_warp_create_order_probe import (
    CROSS_FILE_UNORDERED,
    SAME_FILE_ORDERED,
    CreateWarpProvenance,
    analyze,
    parse_ambiguous_geometry,
)


def _geometry():
    return "\n".join(
        [
            "COUNT|materializable_classic_warps|4",
            (
                "MATERIALIZABLE_WARP|source=810,28,27|placement=10|"
                "destination=809,18,13|conditional_time=0"
            ),
            (
                "MATERIALIZABLE_WARP|source=810,28,27|placement=20|"
                "destination=829,18,13|conditional_time=0"
            ),
            (
                "MATERIALIZABLE_WARP|source=1,2,3|placement=30|"
                "destination=4,5,6|conditional_time=0"
            ),
            (
                "MATERIALIZABLE_WARP|source=1,2,3|placement=31|"
                "destination=7,8,9|conditional_time=0"
            ),
            "RESOLUTION|MATERIALIZABLE_RECOVERED_WORLD_WARP_GEOMETRY_CLOSED",
        ]
    )


class AmbiguousWarpCreateOrderProbeTests(unittest.TestCase):

    def test_geometry_parser_selects_only_multi_signature_sources(self):
        rows = parse_ambiguous_geometry(_geometry())
        self.assertEqual(set(rows), {(810, 28, 27), (1, 2, 3)})
        self.assertEqual(len(rows[(810, 28, 27)]), 2)

    def test_same_file_is_ordered_but_cross_file_remains_unselected(self):
        provenance = {
            10: CreateWarpProvenance(
                10, (810, 28, 27), (809, 18, 13),
                "quiz/a.create", 4, 1, 0
            ),
            20: CreateWarpProvenance(
                20, (810, 28, 27), (829, 18, 13),
                "quiz/a.create", 9, 1, 0
            ),
            30: CreateWarpProvenance(
                30, (1, 2, 3), (4, 5, 6),
                "a.create", 1, 1, 0
            ),
            31: CreateWarpProvenance(
                31, (1, 2, 3), (7, 8, 9),
                "b.create", 1, 1, 0
            ),
        }
        with patch(
            "tools.stoneage_ambiguous_warp_create_order_probe."
            "collect_create_warp_provenance",
            return_value=provenance,
        ):
            audit = analyze(
                geometry_text=_geometry(),
                npc_dir=Path("."),
                represented_floor_ids={1, 4, 7, 809, 810, 829},
            )
        by_source = {row.source: row for row in audit.rows}
        same = by_source[(810, 28, 27)]
        cross = by_source[(1, 2, 3)]
        self.assertEqual(same.classification, SAME_FILE_ORDERED)
        self.assertEqual(same.first_placement_id, 10)
        self.assertEqual(cross.classification, CROSS_FILE_UNORDERED)
        self.assertIsNone(cross.first_placement_id)


if __name__ == "__main__":
    unittest.main()
