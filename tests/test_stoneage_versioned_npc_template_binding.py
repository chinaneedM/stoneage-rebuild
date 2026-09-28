import unittest
from pathlib import Path

from tools.stoneage_versioned_npc_spawn_catalogue import (
    build_versioned_npc_spawn_catalogue,
)
from tools.stoneage_versioned_npc_template_binding import (
    DUPLICATE_NAME_SAME_FUNCTIONSET,
    TEMPLATE_BINDING_REPORT_REF,
    UNIQUE_NAME,
    parse_versioned_npc_template_bindings,
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


def _real_spawn_catalogue():
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
    return build_versioned_npc_spawn_catalogue(geometry)


class VersionedNpcTemplateBindingTests(unittest.TestCase):

    def test_real_repository_anonymous_template_identity_closure(self):
        spawn_catalogue = _real_spawn_catalogue()
        manifest = parse_versioned_npc_template_bindings(
            spawn_catalogue=spawn_catalogue,
            text=Path(TEMPLATE_BINDING_REPORT_REF).read_text(
                encoding="utf-8"
            ),
        )

        self.assertEqual(len(manifest.bindings), 3856)
        self.assertEqual(len(manifest.identities), 73)
        self.assertEqual(len(manifest.unique_concrete_bindings), 3853)
        self.assertEqual(len(manifest.duplicate_name_bindings), 3)
        self.assertEqual(
            len(manifest.direct_spawn_with_identity_eligible),
            3850,
        )
        self.assertEqual(
            manifest.classic_warp_functionset_inconsistencies,
            (),
        )

        duplicates = {
            binding.placement_id: (
                binding.status,
                binding.variant_count,
                binding.functionset_consensus,
            )
            for binding in manifest.duplicate_name_bindings
        }
        self.assertEqual(
            duplicates,
            {
                2512: (
                    DUPLICATE_NAME_SAME_FUNCTIONSET,
                    4,
                    "Quiz",
                ),
                3539: (
                    DUPLICATE_NAME_SAME_FUNCTIONSET,
                    3,
                    "transmigration",
                ),
                3634: (
                    DUPLICATE_NAME_SAME_FUNCTIONSET,
                    2,
                    "TranserMan",
                ),
            },
        )
        self.assertTrue(
            all(
                binding.functionset_is_consensus
                for binding in manifest.bindings
            )
        )
        self.assertEqual(
            sum(
                binding.classic_warp_geometry
                for binding in manifest.bindings
            ),
            2264,
        )
        self.assertTrue(
            all(
                binding.functionset_consensus == "Warp"
                for binding in manifest.bindings
                if binding.classic_warp_geometry
            )
        )

    def test_report_contains_no_raw_template_name_field(self):
        text = Path(TEMPLATE_BINDING_REPORT_REF).read_text(encoding="utf-8")
        self.assertNotIn("templatename=", text.lower())
        self.assertNotIn("npc_name=", text.lower())
        self.assertNotIn("dialogue=", text.lower())
        self.assertNotIn("argument=", text.lower())

    def test_duplicate_binding_cannot_be_relabelled_unique(self):
        spawn_catalogue = _real_spawn_catalogue()
        text = Path(TEMPLATE_BINDING_REPORT_REF).read_text(encoding="utf-8")
        drifted = text.replace(
            "placement=2512|floor=812|",
            "placement=2512|floor=812|",
            1,
        ).replace(
            "status=DUPLICATE_NAME_SAME_FUNCTIONSET|classic_warp_geometry=0",
            "status=UNIQUE_NAME|classic_warp_geometry=0",
            1,
        )
        with self.assertRaisesRegex(
            ValueError,
            "UNIQUE_NAME binding must have exactly one variant",
        ):
            parse_versioned_npc_template_bindings(
                spawn_catalogue=spawn_catalogue,
                text=drifted,
            )


if __name__ == "__main__":
    unittest.main()
