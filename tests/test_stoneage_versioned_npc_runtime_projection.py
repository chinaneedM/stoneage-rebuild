import unittest
from pathlib import Path

from tools.stoneage_singleplayer_domain import (
    NpcTemplateId,
    RuntimeObjectId,
    SinglePlayerHistoricalDomain,
)
from tools.stoneage_versioned_npc_runtime_projection import (
    ANONYMOUS_TEMPLATE_NAMESPACE,
    build_versioned_generic_npc_spawn_projection,
)
from tools.stoneage_versioned_npc_spawn_catalogue import (
    build_versioned_npc_spawn_catalogue,
)
from tools.stoneage_versioned_npc_template_binding import (
    TEMPLATE_BINDING_REPORT_REF,
    parse_versioned_npc_template_bindings,
)
from tools.stoneage_versioned_npc_template_profile import (
    TEMPLATE_PROFILE_REPORT_REF,
    parse_versioned_npc_template_profiles,
)
from tools.stoneage_versioned_world_geometry import (
    WORLD_GEOMETRY_REPORT_REF,
    parse_versioned_world_geometry,
)
from tools.stoneage_versioned_world_manifest import (
    COVERAGE_REPORT_REF,
    build_versioned_world_manifest,
)
from tools.stoneage_world_map_library import (
    LINEAGE_REPORT_REF,
    parse_stable_later_map_manifest,
)


def _real_projection():
    maps = parse_stable_later_map_manifest(
        Path(LINEAGE_REPORT_REF).read_text(encoding="utf-8")
    )
    world = build_versioned_world_manifest(
        maps=maps,
        coverage_text=Path(COVERAGE_REPORT_REF).read_text(encoding="utf-8"),
    )
    geometry = parse_versioned_world_geometry(
        world=world,
        text=Path(WORLD_GEOMETRY_REPORT_REF).read_text(encoding="utf-8"),
    )
    spawn = build_versioned_npc_spawn_catalogue(geometry)
    bindings = parse_versioned_npc_template_bindings(
        spawn_catalogue=spawn,
        text=Path(TEMPLATE_BINDING_REPORT_REF).read_text(encoding="utf-8"),
    )
    profiles = parse_versioned_npc_template_profiles(
        bindings=bindings,
        text=Path(TEMPLATE_PROFILE_REPORT_REF).read_text(encoding="utf-8"),
    )
    return build_versioned_generic_npc_spawn_projection(
        spawn_catalogue=spawn,
        bindings=bindings,
        profiles=profiles,
    )


class VersionedNpcRuntimeProjectionTests(unittest.TestCase):

    def test_real_generic_spawn_projection_closure(self):
        projection = _real_projection()

        self.assertEqual(len(projection.intents), 3856)
        self.assertEqual(len(projection.spawn_integrity_eligible), 3852)
        self.assertEqual(len(projection.intrinsic_graphic_resolved), 2976)
        self.assertEqual(
            len(projection.spawn_safe_intrinsic_graphic_resolved),
            2974,
        )
        self.assertEqual(len(projection.opaque_graphic_intents), 880)
        self.assertEqual(len(projection.opaque_type_intents), 89)
        self.assertTrue(
            all(
                intent.deterministic_birth_position is not None
                for intent in projection.intents
            )
        )
        self.assertTrue(
            all(intent.population_cap == 1 for intent in projection.intents)
        )

    def test_intrinsic_graphic_intent_can_feed_existing_domain_boundary(self):
        projection = _real_projection()
        intent = next(
            row
            for row in projection.spawn_safe_intrinsic_graphic_resolved
            if row.intrinsic_graphic_id is not None
        )
        state = intent.materialize_npc_runtime_state(
            runtime_object_id=90001,
            display_name="runtime-presentation-input",
            object_type=1,
            default_level=0,
            default_name_color=0,
        )

        self.assertEqual(
            state.template_ref.namespace,
            ANONYMOUS_TEMPLATE_NAMESPACE,
        )
        self.assertEqual(state.template_ref.template_id, intent.template_key)
        self.assertEqual(state.create_index, intent.placement_id)
        self.assertEqual(state.base_graphic_id, intent.intrinsic_graphic_id)
        self.assertEqual(state.direction, intent.raw_direction)

        domain = SinglePlayerHistoricalDomain()
        npc = domain.place_npc(state)
        self.assertEqual(npc.runtime_object_id, RuntimeObjectId(90001))
        self.assertEqual(npc.template_id, NpcTemplateId(intent.template_key))
        self.assertEqual(
            npc.position,
            intent.deterministic_birth_position,
        )
        self.assertEqual(
            npc.world_view["name"],
            "runtime-presentation-input",
        )

    def test_opaque_graphic_requires_explicit_resolution(self):
        projection = _real_projection()
        intent = next(
            row
            for row in projection.opaque_graphic_intents
            if row.spawn_integrity_eligible
        )
        with self.assertRaisesRegex(ValueError, "opaque graphic token"):
            intent.materialize_npc_runtime_state(
                runtime_object_id=90002,
                display_name="runtime-presentation-input",
                object_type=1,
                default_level=0,
                default_name_color=0,
            )

        state = intent.materialize_npc_runtime_state(
            runtime_object_id=90002,
            display_name="runtime-presentation-input",
            object_type=1,
            default_level=0,
            default_name_color=0,
            resolved_graphic_id=1234,
        )
        self.assertEqual(state.base_graphic_id, 1234)

    def test_quarantined_spawn_cannot_materialize(self):
        projection = _real_projection()
        intent = next(
            row for row in projection.intents
            if not row.spawn_integrity_eligible
        )
        with self.assertRaisesRegex(ValueError, "quarantined"):
            intent.materialize_npc_runtime_state(
                runtime_object_id=90003,
                display_name="runtime-presentation-input",
                object_type=1,
                default_level=0,
                default_name_color=0,
                resolved_graphic_id=1234,
            )

    def test_duplicate_source_definitions_do_not_block_runtime_equivalent_intent(self):
        projection = _real_projection()
        for placement_id in (2512, 3539, 3634):
            intent = projection.by_placement[placement_id]
            self.assertIsNotNone(intent.profile)
            self.assertEqual(intent.profile.template_key, intent.template_key)

        self.assertTrue(projection.by_placement[2512].spawn_integrity_eligible)
        self.assertTrue(projection.by_placement[3539].spawn_integrity_eligible)
        self.assertFalse(projection.by_placement[3634].spawn_integrity_eligible)


if __name__ == "__main__":
    unittest.main()
