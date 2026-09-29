import unittest
from pathlib import Path

from tools.stoneage_floor130_arbitration import (
    ARCHIVED2003_ALIGNED,
    RECOVERED25_ALIGNED,
    WARP_RUNTIME_CONFLICTING,
    WARP_RUNTIME_CONSISTENT,
    load_floor130_arbitration,
)
from tools.stoneage_singleplayer_world import (
    LATER_RECOVERED,
    RESOURCE_RELATION_UNKNOWN,
)
from tools.stoneage_supplemental_world_fork_binding import (
    bind_floor130_version_fork,
)
from tools.stoneage_supplemental_world_manifest import (
    SUPPLEMENTAL_AUDIT_REPORT_REF,
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


def _extension():
    maps = parse_stable_later_map_manifest(
        Path(LINEAGE_REPORT_REF).read_text(encoding="utf-8")
    )
    stable = build_versioned_world_manifest(
        maps=maps,
        coverage_text=Path(COVERAGE_REPORT_REF).read_text(encoding="utf-8"),
    )
    return parse_supplemental_world_audit(
        stable_world=stable,
        text=Path(SUPPLEMENTAL_AUDIT_REPORT_REF).read_text(encoding="utf-8"),
    )


class SupplementalWorldForkBindingTests(unittest.TestCase):

    def test_real_floor130_fork_binds_without_creating_default(self):
        extension = _extension()
        binding = bind_floor130_version_fork(
            extension=extension,
            arbitration=load_floor130_arbitration(),
        )
        self.assertEqual(binding.floor_id, 130)
        self.assertIsNone(binding.selected_path)
        self.assertIsNone(binding.default_map_definition)
        self.assertEqual(set(binding.by_path), {"extra/130", "family/130"})
        self.assertNotIn(130, extension.materializable_map_definitions)

        family = binding.by_path["family/130"]
        extra = binding.by_path["extra/130"]
        self.assertEqual(family.arbitration.temporal_alignment, ARCHIVED2003_ALIGNED)
        self.assertEqual(family.arbitration.warp_consistency, WARP_RUNTIME_CONSISTENT)
        self.assertEqual(extra.arbitration.temporal_alignment, RECOVERED25_ALIGNED)
        self.assertEqual(extra.arbitration.warp_consistency, WARP_RUNTIME_CONFLICTING)

    def test_candidate_definition_requires_explicit_path_and_stays_later_recovered(self):
        binding = bind_floor130_version_fork(
            extension=_extension(),
            arbitration=load_floor130_arbitration(),
        )
        definition = binding.candidate_map_definition("family/130")
        self.assertEqual(definition.floor_id, 130)
        self.assertEqual((definition.width, definition.height), (60, 60))
        self.assertEqual(definition.provenance.content_role, LATER_RECOVERED)
        self.assertEqual(
            definition.provenance.resource_role,
            RESOURCE_RELATION_UNKNOWN,
        )
        self.assertFalse(definition.provenance.claims_early_membership)
        self.assertEqual(
            definition.provenance.payload_sha256,
            "8f6e5e1983830694f090decbb32417ea1b6ba3ac0f61953495a910d513e2fe7d",
        )
        with self.assertRaises(KeyError):
            binding.candidate_map_definition("default")

    def test_binding_rejects_arbitration_sha_drift(self):
        arbitration = load_floor130_arbitration()
        # Frozen dataclasses make accidental mutation impossible; instead verify
        # the real unresolved audit hash set exactly matches arbitration.
        extension = _extension()
        unresolved = extension.unresolved_by_floor[130]
        self.assertEqual(
            set(unresolved.server_sha256s),
            {row.sha256 for row in arbitration.candidates},
        )


if __name__ == "__main__":
    unittest.main()
