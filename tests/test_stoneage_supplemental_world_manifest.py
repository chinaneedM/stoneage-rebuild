import unittest
from pathlib import Path

from tools.stoneage_singleplayer_world import (
    LATER_RECOVERED,
    RESOURCE_RELATION_UNKNOWN,
)
from tools.stoneage_supplemental_world_manifest import (
    SUPPLEMENTAL_AUDIT_REPORT_REF,
    DUPLICATE_DIVERGENT,
    parse_supplemental_world_audit,
)
from tools.stoneage_versioned_world_manifest import (
    COVERAGE_REPORT_REF,
    build_versioned_world_manifest,
)
from tools.stoneage_world_map_library import (
    LINEAGE_REPORT_REF,
    parse_stable_later_map_manifest,
)


def _stable_world():
    maps = parse_stable_later_map_manifest(
        Path(LINEAGE_REPORT_REF).read_text(encoding="utf-8")
    )
    return build_versioned_world_manifest(
        maps=maps,
        coverage_text=Path(COVERAGE_REPORT_REF).read_text(encoding="utf-8"),
    )


def _audit_text():
    return Path(SUPPLEMENTAL_AUDIT_REPORT_REF).read_text(encoding="utf-8")


class SupplementalWorldManifestTests(unittest.TestCase):

    def test_real_extension_preserves_stable_world_and_exposes_conflict(self):
        stable = _stable_world()
        stable_ids_before = frozenset(stable.by_floor)
        extension = parse_supplemental_world_audit(
            stable_world=stable,
            text=_audit_text(),
        )

        self.assertEqual(len(stable.by_floor), 761)
        self.assertEqual(frozenset(stable.by_floor), stable_ids_before)
        self.assertEqual(len(extension.resolved_floors), 65)
        self.assertEqual(len(extension.unresolved_floors), 1)
        self.assertEqual(len(extension.reachable_floor_ids), 827)
        self.assertEqual(len(extension.materializable_floor_ids), 826)
        self.assertEqual(len(extension.materializable_map_definitions), 826)

        unresolved = extension.unresolved_by_floor[130]
        self.assertEqual(
            unresolved.server_copy_status,
            DUPLICATE_DIVERGENT,
        )
        self.assertEqual(unresolved.server_dimensions, ((60, 60), (60, 60)))
        self.assertEqual(len(set(unresolved.server_sha256s)), 2)
        self.assertNotIn(130, extension.materializable_map_definitions)

    def test_resolved_supplemental_map_never_claims_early_membership(self):
        extension = parse_supplemental_world_audit(
            stable_world=_stable_world(),
            text=_audit_text(),
        )
        floor = extension.resolved_by_floor[100]
        definition = floor.to_map_definition()

        self.assertEqual(definition.floor_id, 100)
        self.assertEqual((definition.width, definition.height), (800, 800))
        self.assertEqual(
            definition.provenance.content_role,
            LATER_RECOVERED,
        )
        self.assertEqual(
            definition.provenance.resource_role,
            RESOURCE_RELATION_UNKNOWN,
        )
        self.assertFalse(definition.provenance.claims_early_membership)
        self.assertEqual(
            definition.provenance.payload_sha256,
            "20ae120c511d0219070dc9970aaf3dd4d783adb18bafd13ca90266e60e6c4496",
        )
        self.assertEqual(floor.semantic.coverage.npc_create_count, 103)
        self.assertEqual(floor.semantic.coverage.encounter_row_count, 45)

    def test_materializable_map_topology_excludes_only_unresolved_supplemental(self):
        extension = parse_supplemental_world_audit(
            stable_world=_stable_world(),
            text=_audit_text(),
        )
        topology = extension.materializable_map_topology()
        self.assertEqual(len(topology.maps), 826)
        self.assertNotIn(130, topology.maps)
        self.assertIn(100, topology.maps)
        self.assertTrue(topology.require_structured_provenance)

    def test_promoted_supplemental_evidence_is_rejected(self):
        promoted = _audit_text().replace(
            "EVIDENCE_ROLE|LATER_RECOVERED",
            "EVIDENCE_ROLE|EARLY_MEMBERSHIP_PROVEN",
            1,
        )
        with self.assertRaisesRegex(ValueError, "promoted"):
            parse_supplemental_world_audit(
                stable_world=_stable_world(),
                text=promoted,
            )

    def test_divergent_floor_cannot_be_silently_marked_materializable(self):
        drifted = _audit_text().replace(
            "floor=130|depth=1|reachability_status=CHANGED|"
            "incoming_reachable_warps=2|outgoing_runtime_warps=2|"
            "server_copy_count=2|server_copy_status=DUPLICATE_DIVERGENT|",
            "floor=130|depth=1|reachability_status=CHANGED|"
            "incoming_reachable_warps=2|outgoing_runtime_warps=2|"
            "server_copy_count=2|server_copy_status=DUPLICATE_DIVERGENT|",
            1,
        ).replace(
            "server_sha256s=b62fca539743b5ac91f38b344e34e4655a287d4e71582d8e3547c83fc0ee8fa2,"
            "8f6e5e1983830694f090decbb32417ea1b6ba3ac0f61953495a910d513e2fe7d|"
            "static_materializable=0|",
            "server_sha256s=b62fca539743b5ac91f38b344e34e4655a287d4e71582d8e3547c83fc0ee8fa2,"
            "8f6e5e1983830694f090decbb32417ea1b6ba3ac0f61953495a910d513e2fe7d|"
            "static_materializable=1|",
            1,
        )
        with self.assertRaisesRegex(ValueError, "silently materialized"):
            parse_supplemental_world_audit(
                stable_world=_stable_world(),
                text=drifted,
            )


if __name__ == "__main__":
    unittest.main()
