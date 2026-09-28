import unittest
from collections import Counter
from pathlib import Path

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


def _real_layers():
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
    return spawn, bindings, profiles


class VersionedNpcTemplateProfileTests(unittest.TestCase):

    def test_real_repository_template_profile_closure(self):
        spawn, bindings, profiles = _real_layers()

        self.assertEqual(len(spawn.placements), 3856)
        self.assertEqual(len(bindings.bindings), 3856)
        self.assertEqual(len(bindings.identities), 73)
        self.assertEqual(profiles.profile_variant_count, 79)
        self.assertEqual(len(profiles.profiles_by_identity), 73)
        self.assertEqual(len(profiles.symbolic_profile_variants), 30)
        self.assertEqual(profiles.direct_override_profile_variants, ())

        all_profiles = [
            profile
            for rows in profiles.profiles_by_identity.values()
            for profile in rows
        ]
        self.assertEqual(
            len({profile.variant_fingerprint for profile in all_profiles}),
            73,
        )
        self.assertTrue(all(profile.make_at_nobody == 1 for profile in all_profiles))
        self.assertTrue(all(profile.make_at_no_see == 1 for profile in all_profiles))
        self.assertTrue(all(profile.flying == 0 for profile in all_profiles))
        self.assertEqual(
            Counter(profile.loop_interval for profile in all_profiles),
            Counter({-1: 76, 4000: 3}),
        )
        self.assertEqual(
            Counter(profile.graphic_resolution for profile in all_profiles),
            Counter({
                "DEFAULT_ZERO": 49,
                "NUMERIC": 7,
                "OPAQUE_SYMBOL": 23,
            }),
        )
        self.assertEqual(
            Counter(profile.type_resolution for profile in all_profiles),
            Counter({
                "DEFAULT_SPR_PET001": 32,
                "NUMERIC": 40,
                "OPAQUE_SYMBOL": 7,
            }),
        )

    def test_duplicate_source_definitions_are_runtime_equivalent(self):
        _spawn, bindings, profiles = _real_layers()

        self.assertEqual(len(bindings.duplicate_name_bindings), 3)
        self.assertEqual(len(bindings.runtime_equivalent_bindings), 3856)
        self.assertEqual(
            len(
                bindings.direct_spawn_with_runtime_equivalent_identity_eligible
            ),
            3852,
        )

        for placement_id in (2512, 3539, 3634):
            binding = bindings.by_placement[placement_id]
            identity = bindings.identities[binding.template_key]
            self.assertGreater(identity.variant_count, 1)
            self.assertEqual(identity.variant_fingerprint_count, 1)
            self.assertTrue(identity.runtime_variants_are_byte_equivalent)

            with self.assertRaisesRegex(
                ValueError,
                "duplicate template-name variants",
            ):
                profiles.unique_profile_for_placement(placement_id)

            profile = profiles.runtime_equivalent_profile_for_placement(
                placement_id
            )
            self.assertEqual(profile.template_key, binding.template_key)

    def test_unique_placement_resolves_one_profile(self):
        _spawn, bindings, profiles = _real_layers()
        placement_id = next(
            binding.placement_id
            for binding in bindings.bindings
            if binding.concrete_template_binding_is_unique
        )
        profile = profiles.unique_profile_for_placement(placement_id)
        equivalent = profiles.runtime_equivalent_profile_for_placement(
            placement_id
        )
        self.assertEqual(profile, equivalent)

    def test_profile_report_excludes_text_surfaces(self):
        text = Path(TEMPLATE_PROFILE_REPORT_REF).read_text(encoding="utf-8")
        lowered = text.lower()
        self.assertNotIn("templatename=", lowered)
        self.assertNotIn("npc_name=", lowered)
        self.assertNotIn("dialogue=", lowered)
        self.assertNotIn("callback_name=", lowered)
        self.assertNotIn("argument=", lowered)
        self.assertNotIn("item_payload=", lowered)


if __name__ == "__main__":
    unittest.main()
