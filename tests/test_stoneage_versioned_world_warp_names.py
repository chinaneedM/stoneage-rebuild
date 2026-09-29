import unittest
from pathlib import Path

from tools.stoneage_versioned_world_geometry import (
    WORLD_GEOMETRY_REPORT_REF,
    parse_versioned_world_geometry,
)
from tools.stoneage_versioned_world_manifest import (
    COVERAGE_REPORT_REF,
    build_versioned_world_manifest,
)
from tools.stoneage_versioned_world_names import (
    MAP_NAMES_REPORT_REF,
    bind_versioned_world_names,
)
from tools.stoneage_versioned_world_warp_names import (
    OUTSIDE_STABLE_WORLD,
    RESOLVED,
    UNRESOLVED,
    build_versioned_warp_name_diagnostics,
)
from tools.stoneage_world_map_library import (
    LINEAGE_REPORT_REF,
    parse_stable_later_map_manifest,
)


def _diagnostics():
    maps = parse_stable_later_map_manifest(
        Path(LINEAGE_REPORT_REF).read_text(encoding="utf-8")
    )
    world = build_versioned_world_manifest(
        maps=maps,
        coverage_text=Path(COVERAGE_REPORT_REF).read_text(encoding="utf-8"),
    )
    names = bind_versioned_world_names(
        world=world,
        names_text=Path(MAP_NAMES_REPORT_REF).read_text(encoding="utf-8"),
    )
    geometry = parse_versioned_world_geometry(
        world=world,
        text=Path(WORLD_GEOMETRY_REPORT_REF).read_text(encoding="utf-8"),
    )
    return build_versioned_warp_name_diagnostics(
        geometry=geometry,
        names=names,
    )


class VersionedWorldWarpNamesTests(unittest.TestCase):

    def test_real_warp_graph_gets_provenance_safe_name_diagnostics(self):
        diagnostics = _diagnostics()
        counts = diagnostics.counts

        self.assertEqual(counts["total"], 2264)
        self.assertEqual(counts["source:RESOLVED"], 2261)
        self.assertEqual(counts["source:UNRESOLVED"], 3)
        self.assertEqual(counts["destination:RESOLVED"], 1908)
        self.assertEqual(counts["destination:UNRESOLVED"], 1)
        self.assertEqual(
            counts["destination:OUTSIDE_STABLE_WORLD"],
            355,
        )
        self.assertEqual(counts["pair:RESOLVED->RESOLVED"], 1907)
        self.assertEqual(
            counts["pair:RESOLVED->OUTSIDE_STABLE_WORLD"],
            353,
        )
        self.assertEqual(
            counts["pair:UNRESOLVED->OUTSIDE_STABLE_WORLD"],
            2,
        )
        self.assertEqual(counts["pair:UNRESOLVED->RESOLVED"], 1)
        self.assertEqual(counts["pair:RESOLVED->UNRESOLVED"], 1)
        self.assertEqual(len(diagnostics.distinct_floor_pairs), 985)

    def test_known_warp_pair_exposes_recovered_text_without_cleaning(self):
        diagnostics = _diagnostics()
        row = next(
            row for row in diagnostics.rows
            if (
                row.warp.source_floor == 3021
                and row.warp.destination_floor == 3022
            )
        )

        self.assertEqual(row.source_name_state, RESOLVED)
        self.assertEqual(row.destination_name_state, RESOLVED)
        self.assertEqual(
            row.source_recovered_text,
            "百人聯手道場|0",
        )
        self.assertEqual(
            row.destination_recovered_text,
            "加加的道場醫務室|0",
        )

    def test_conflicting_floor_never_gets_selected_text(self):
        diagnostics = _diagnostics()
        touching = [
            row for row in diagnostics.rows
            if (
                row.warp.source_floor == 31001
                or row.warp.destination_floor == 31001
            )
        ]
        self.assertTrue(touching)

        for row in touching:
            if row.warp.source_floor == 31001:
                self.assertEqual(row.source_name_state, UNRESOLVED)
                self.assertIsNone(row.source_recovered_text)
            if row.warp.destination_floor == 31001:
                self.assertEqual(
                    row.destination_name_state,
                    UNRESOLVED,
                )
                self.assertIsNone(row.destination_recovered_text)


if __name__ == "__main__":
    unittest.main()
