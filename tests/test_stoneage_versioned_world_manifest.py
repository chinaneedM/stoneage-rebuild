import unittest
from pathlib import Path

from tools.stoneage_singleplayer_world import LATER_RECOVERED
from tools.stoneage_versioned_world_manifest import (
    COVERAGE_REPORT_REF,
    SEMANTIC_SOURCE_VERSION,
    build_versioned_world_manifest,
    parse_world_content_coverage,
)
from tools.stoneage_world_map_library import (
    LINEAGE_REPORT_REF,
    parse_stable_later_map_manifest,
)


def _reports():
    lineage = Path(LINEAGE_REPORT_REF).read_text(encoding="utf-8")
    coverage = Path(COVERAGE_REPORT_REF).read_text(encoding="utf-8")
    return lineage, coverage


class VersionedWorldManifestTests(unittest.TestCase):

    def test_real_reports_join_without_promoting_later_semantics(self):
        lineage_text, coverage_text = _reports()
        maps = parse_stable_later_map_manifest(lineage_text)
        world = build_versioned_world_manifest(
            maps=maps,
            coverage_text=coverage_text,
        )

        self.assertEqual(world.semantic_source_version, SEMANTIC_SOURCE_VERSION)
        self.assertEqual(len(world.floors), 761)
        self.assertEqual(len(world.topology.maps), 761)
        self.assertEqual(
            world.count(lambda f: f.semantic.server_map_present),
            572,
        )
        self.assertEqual(
            world.count(lambda f: f.semantic.has_npc_semantics),
            553,
        )
        self.assertEqual(
            world.count(lambda f: f.semantic.has_warp_semantics),
            544,
        )
        self.assertEqual(
            world.count(lambda f: f.semantic.has_encounter_semantics),
            361,
        )
        self.assertEqual(
            world.count(
                lambda f: (
                    f.semantic.has_npc_semantics
                    and f.semantic.has_encounter_semantics
                )
            ),
            359,
        )
        self.assertEqual(len(world.semantic_gap_floor_ids), 206)
        self.assertTrue(
            all(
                floor.semantic.evidence_role == LATER_RECOVERED
                for floor in world.floors
            )
        )
        self.assertTrue(
            all(
                not world.topology.maps[floor.floor_id]
                    .provenance.claims_early_membership
                for floor in world.floors
            )
        )

    def test_real_floor_identity_is_cross_checked_to_lineage(self):
        lineage_text, coverage_text = _reports()
        maps = parse_stable_later_map_manifest(lineage_text)
        world = build_versioned_world_manifest(
            maps=maps,
            coverage_text=coverage_text,
        )
        floor = world.by_floor[10001]
        definition = world.topology.maps[10001]

        self.assertEqual(floor.path, "10001.dat")
        self.assertEqual(floor.width, 50)
        self.assertEqual(floor.height, 50)
        self.assertEqual(floor.map_sha256, definition.provenance.payload_sha256)
        self.assertEqual(floor.semantic.npc_create_count, 3)
        self.assertEqual(floor.semantic.warp_functionset_create_count, 2)
        self.assertEqual(floor.semantic.encounter_row_count, 1)

    def test_semantic_gap_means_unknown_not_empty(self):
        lineage_text, coverage_text = _reports()
        maps = parse_stable_later_map_manifest(lineage_text)
        world = build_versioned_world_manifest(
            maps=maps,
            coverage_text=coverage_text,
        )
        gap_id = world.semantic_gap_floor_ids[0]
        floor = world.by_floor[gap_id]

        self.assertTrue(floor.semantic_gap)
        self.assertEqual(floor.semantic.npc_create_count, 0)
        self.assertEqual(floor.semantic.encounter_row_count, 0)
        self.assertEqual(floor.semantic.evidence_role, LATER_RECOVERED)

    def test_truncated_coverage_is_rejected(self):
        _, coverage_text = _reports()
        lines = coverage_text.splitlines()
        first_floor = next(
            index for index, line in enumerate(lines)
            if line.startswith("FLOOR|")
        )
        truncated = "\n".join(lines[:first_floor] + lines[first_floor + 1 :])
        with self.assertRaisesRegex(ValueError, "detail count"):
            parse_world_content_coverage(truncated)

    def test_map_identity_drift_is_rejected(self):
        lineage_text, coverage_text = _reports()
        maps = parse_stable_later_map_manifest(lineage_text)
        drifted = coverage_text.replace(
            "FLOOR|id=10001|path=10001.dat|width=50|height=50|",
            "FLOOR|id=10001|path=10001.dat|width=51|height=50|",
            1,
        )
        with self.assertRaisesRegex(ValueError, "width drift"):
            build_versioned_world_manifest(
                maps=maps,
                coverage_text=drifted,
            )


if __name__ == "__main__":
    unittest.main()
