"""O72 bounded derived-data regression; commercial original pixels stay private."""
import json
import unittest
from pathlib import Path

REPORT = Path(__file__).resolve().parents[1] / "research/recovered/STONEAGE-O72-FLOOR1009-ORIGINAL-PIXELS-R1.json"


class OriginalFloor1009PixelEvidenceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.evidence = json.loads(REPORT.read_text(encoding="utf-8"))

    def test_original_resource_conservation(self):
        data = self.evidence["original_floor1009"]
        self.assertEqual((data["dimensions"], data["cells"]), ([40, 60], 2400))
        self.assertEqual(data["distinct_map_aliases_with_nonzero_resource_id"], 85)
        self.assertEqual(data["source_qualified_RD_blocks_read"], 86)
        self.assertEqual(data["independent_legacy_RD_decoders_agreed"], 86)
        self.assertEqual(data["original_RD_total_bytes"], 386898)
        self.assertTrue(data["all_86_records_unique_within_early_shared_index_prefix"])
        self.assertTrue(data["all_86_resource_spans_inside_verified_tw10_real"])
        self.assertEqual(sum(data["placements_by_plane"].values()), data["map_graphic_placements"])
        self.assertEqual(data["map_graphic_placements"], 1034)

    def test_only_bounded_source_qualifications(self):
        sources = self.evidence["qualified_originals"]
        self.assertEqual(sources["tw10_real"]["bytes"], 315842228)
        self.assertTrue(sources["tw10_real"]["full_file_reverified"])
        self.assertFalse(sources["prior_complete_real_prefix_report"]["reran_full_mixed25_real_comparison_this_unit"])
        self.assertTrue(sources["saved_mixed25_adrn"]["full_byte_prefix_against_tw1_reverified"])

    def test_private_assets_and_runtime_gates(self):
        witness = self.evidence["private_research_output"]
        limits = self.evidence["evidence_limits"]
        self.assertEqual(witness["members"], 8)
        self.assertTrue(witness["all_member_CRC_pass"])
        self.assertFalse(witness["commercial_raw_pixels_publicly_published"])
        self.assertFalse(witness["library_uploaded"])
        self.assertTrue(limits["original_floor1009_art_pixels_recovered_in_modern_candidate"])
        for field in (
            "original_client_process_executed", "original_server_executed",
            "native_palette_runtime_selection_confirmed",
            "native_occlusion_and_draw_order_confirmed",
            "native_npc_identity_and_interaction_confirmed",
            "same_commercial_deployment_confirmed",
            "original_client_screenshot_recovered",
        ):
            self.assertIs(limits[field], False, field)
        self.assertIsNone(limits["completion_percent"])
        self.assertEqual(limits["r79"], "PAUSED_NON_BLOCKING")


if __name__ == "__main__":
    unittest.main()
