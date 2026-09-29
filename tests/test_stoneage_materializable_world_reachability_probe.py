import unittest
from pathlib import Path

from tools.stoneage_materializable_world_reachability_probe import (
    MaterializableWarpEdge,
    compute_materializable_reachability,
    parse_materializable_geometry,
)


class MaterializableWorldReachabilityProbeTests(unittest.TestCase):

    def test_bfs_reports_orphan_after_unresolved_intermediate_is_removed(self):
        audit = compute_materializable_reachability(
            stable_floor_ids={1},
            resolved_supplemental_ids={2, 3},
            unresolved_supplemental_ids={130},
            edges=(
                MaterializableWarpEdge(1, 2),
                MaterializableWarpEdge(2, 1),
            ),
        )
        self.assertEqual(audit.reached_floor_ids, frozenset({1, 2}))
        self.assertEqual(audit.orphan_resolved_supplemental_ids, (3,))
        self.assertEqual(audit.resolved_rows[0].floor_id, 2)
        self.assertEqual(audit.resolved_rows[0].depth, 1)

    def test_materializable_edge_cannot_target_unresolved_floor(self):
        with self.assertRaisesRegex(ValueError, "outside materializable world"):
            compute_materializable_reachability(
                stable_floor_ids={1},
                resolved_supplemental_ids={2},
                unresolved_supplemental_ids={130},
                edges=(MaterializableWarpEdge(1, 130),),
            )

    def test_real_geometry_report_has_declared_edge_details(self):
        text = Path(
            "research/recovered/"
            "STONEAGE-25-MATERIALIZABLE-WORLD-WARP-GEOMETRY-R1.txt"
        ).read_text(encoding="utf-8")
        edges, counts = parse_materializable_geometry(text)
        self.assertEqual(len(edges), counts["materializable_classic_warps"])
        self.assertEqual(counts["materializable_floor_ids"], 826)
        self.assertTrue(edges)


if __name__ == "__main__":
    unittest.main()
