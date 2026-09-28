import tempfile
import unittest
from pathlib import Path

from tools.stoneage_versioned_npc_behavior_coverage import (
    CLOSED_ORDINARY_CORE,
    DEFERRED_VERSIONED_PACKAGE,
    NO_DISPATCH_PROFILE,
    UNCLASSIFIED,
    analyze,
    classify_functionset,
)


BINDING_REPORT = (
    "research/recovered/STONEAGE-25-STABLE-NPC-TEMPLATE-BINDINGS-R1.txt"
)
PROFILE_REPORT = (
    "research/recovered/STONEAGE-25-STABLE-NPC-TEMPLATE-PROFILES-R1.txt"
)


class VersionedNpcBehaviorCoverageTests(unittest.TestCase):

    def test_real_stable_world_behavior_coverage(self):
        coverage = analyze(
            binding_report=Path(BINDING_REPORT),
            profile_report=Path(PROFILE_REPORT),
        )
        self.assertEqual(coverage.total_placements, 3856)
        self.assertEqual(
            coverage.category_counts,
            {
                CLOSED_ORDINARY_CORE: 3710,
                NO_DISPATCH_PROFILE: 84,
                DEFERRED_VERSIONED_PACKAGE: 62,
            },
        )
        self.assertEqual(coverage.ordinary_or_no_dispatch_count, 3794)
        self.assertEqual(coverage.unknown_functionsets, ())

        by_name = {row.functionset: row for row in coverage.rows}
        self.assertEqual(by_name["Warp"].placement_count, 2264)
        self.assertEqual(by_name["Warp"].category, CLOSED_ORDINARY_CORE)
        self.assertEqual(
            by_name["Warp"].closure_ref,
            "STONEAGE-WARP-MAP-TRANSITION-CORE-R1",
        )
        self.assertEqual(by_name["<none>"].placement_count, 84)
        self.assertEqual(by_name["<none>"].category, NO_DISPATCH_PROFILE)
        self.assertEqual(by_name["Familyman"].category, DEFERRED_VERSIONED_PACKAGE)
        self.assertEqual(by_name["TranserMan"].category, DEFERRED_VERSIONED_PACKAGE)

    def test_registry_keeps_unknown_functionset_visible(self):
        category, ref = classify_functionset("NeverSeenClass")
        self.assertEqual(category, UNCLASSIFIED)
        self.assertIsNone(ref)

    def test_none_functionset_with_direct_override_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            binding = root / "binding.txt"
            profile = root / "profile.txt"
            key = "a" * 64
            binding.write_text(
                "PLACEMENT_TEMPLATE|placement=0|floor=100|"
                f"template_key={key}|variants=1|"
                "functionset_consensus=<none>|functionset_variants=1|"
                "status=UNIQUE_NAME|classic_warp_geometry=0\n",
                encoding="utf-8",
            )
            profile.write_text(
                "TEMPLATE_PROFILE|"
                f"template_key={key}|variant={'b'*64}|functionset=<none>|"
                "make_at_nobody=1|make_at_no_see=1|"
                "graphic_resolution=DEFAULT_ZERO|graphic_value=|"
                "graphic_token_key=|type_resolution=DEFAULT_SPR_PET001|"
                "type_value=|type_token_key=|hp=0,0|mp=0,0|"
                "strength=0,0|toughness=0,0|flying=0|"
                "loop_interval=-1|direct_overrides=1\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                ValueError,
                "direct callback override",
            ):
                analyze(
                    binding_report=binding,
                    profile_report=profile,
                )


if __name__ == "__main__":
    unittest.main()
