"""Public *receipt* checks. Private commercial SPR/RD is never included in CI."""
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "research/recovered/STONEAGE-INTEGRATION117-ORIGINAL-TW10-UNCLASSIFIED-TEN-SPR-ACTUAL-PIXELS-R1.json"

class TestSourceBoundedOriginalSpr(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(P.read_text(encoding="utf-8"))
        cls.groups = cls.r["groups"]
        cls.obs = cls.r["actual_original_bytes_observation"]

    def test_01_retail_parent_source_provenance(self):
        src = self.r["original_retail_source"]
        self.assertEqual(src["carrier"], "TW_WAEI_JSS1_0_RETAIL_NOT_JSS1999")
        self.assertEqual(src["private_zip_bytes"], 372626292)
        self.assertEqual(src["private_zip_sha256"], "3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24")
        self.assertEqual(src["zip_member_CRC_passed"], 379)
        for name, n in {"spradrn_1.bin":5568,"spr_1.bin":2889630,"adrn_1.bin":10079680,"real_1.bin":315842228,"Palet_0.sap":708,"Palet_1.sap":708}.items():
            meta = src["original_member_full_sha256"][name]
            self.assertEqual(meta["bytes"], n)
            self.assertEqual(len(bytes.fromhex(meta["sha256"])),32)

    def test_02_exact_groups_and_unique_indices(self):
        self.assertEqual([g["graphic"] for g in self.groups],list(range(100462,100472)))
        self.assertEqual([g["original_SPR_index"] for g in self.groups],list(range(425,435)))
        self.assertEqual(len(set(g["original_SPR_index"] for g in self.groups)),10)
        for g in self.groups:
            for attr in ("original_SPRADRN_record_sha256","source_original_SPR_segment_sha256","source_original_bitmap_ids_sorted_sha256"):
                self.assertEqual(len(bytes.fromhex(g[attr])),32)
            self.assertGreater(g["source_spr_group_bytes"],0)

    def test_03_actual_sequence_reference_and_per_group_bitmap_count(self):
        for g in self.groups:
            self.assertEqual(g["source_anim_sequence_count"],g["action_direction_pairs"])
            self.assertEqual(g["direction_codes"],list(range(8)))
            self.assertEqual(g["source_RD_strict_count"]+g["source_RD_terminal_zero_only_count"],g["distinct_original_bitmap_keys"])
        self.assertEqual(sum(g["source_anim_sequence_count"] for g in self.groups),752)
        self.assertEqual(sum(g["source_frame_positions"] for g in self.groups),4856)
        self.assertEqual(self.obs["source_sequences"],752)
        self.assertEqual(self.obs["valid_frame_positions"],4856)
        self.assertEqual(self.obs["source_sentinel_count"],0)
        for g in self.groups[:4]:
            self.assertEqual(g["source_anim_sequence_count"],104)
            self.assertEqual(g["action_codes"],list(range(13)))
            self.assertEqual(g["distinct_original_bitmap_keys"],344)
        self.assertEqual([g["source_frame_positions"] for g in self.groups[:4]],[640,568,648,648])
        for g in self.groups[4:]:
            self.assertEqual(g["source_anim_sequence_count"],56)
            self.assertEqual(g["action_codes"],[0,1,2,3,4,9,10])
            self.assertEqual(g["source_frame_positions"],392)
            self.assertEqual(g["distinct_original_bitmap_keys"],1)

    def test_04_preserve_overlap_and_no_false_novelty_claim(self):
        self.assertEqual(self.obs["cross_group_distinct_real_RD_read"],1238)
        self.assertEqual(self.obs["prior_INTEGRATION116_source_bitmap_overlap"],48)
        self.assertEqual(self.obs["outside_INTEGRATION116_source_bitmap_keys"],1190)
        self.assertEqual(self.obs["prior_INTEGRATION116_source_bitmap_overlap"]+self.obs["outside_INTEGRATION116_source_bitmap_keys"],1238)
        self.assertTrue(self.obs["not_claimed_new_vs_all_earlier_research"])
        self.assertLess(1238,sum(g["distinct_original_bitmap_keys"] for g in self.groups))

    def test_05_strict_vs_only_one_terminal_zero_exception(self):
        self.assertEqual(self.obs["independent_RLE_two_implementations_agree"],1238)
        self.assertEqual((self.obs["strict_canvas_RLE"],self.obs["bounded_only_terminal_zero_anomaly"]),(1237,1))
        self.assertEqual(self.obs["source_bounded_RD_bitmap_id"],94427)
        self.assertEqual(self.obs["source_bounded_RD_w_h"],[68,79])
        self.assertEqual((self.obs["source_bounded_RD_declared_canvas_length"],self.obs["source_bounded_RD_decoded_length"]),(5372,5373))
        self.assertEqual(self.obs["source_bounded_RD_SHA256"],"c08dc0b72da3d1aab6e6123ed0919823d6f68604605086e05878d0381248a600")
        self.assertEqual(self.obs["decoded_original_index_pixels_total"],5179744)
        self.assertEqual([g["source_RD_terminal_zero_only_count"] for g in self.groups],[1]+[0]*9)
        for key in ("all_original_RD_SHA256_by_sorted_bitmap_ID_aggregate","all_original_pixels_SHA256_by_sorted_bitmap_ID_aggregate"):
            self.assertEqual(len(bytes.fromhex(self.obs[key])),32)

    def test_06_private_library_custody_no_public_asset_promotion(self):
        p = self.r["private_observation"]
        self.assertEqual(p["private_package_bytes"],169128)
        self.assertEqual(p["private_package_sha256"],"753573d4f0b28f6bcbf59a2ae376cf7dda69116cbed53a795ce57f536428f8c5")
        self.assertEqual(p["ZIP_members_CRC_verified"],12)
        self.assertEqual(p["grayscale_original_index_png_previews"],10)
        self.assertTrue(p["private_library_roundtrip_same_SHA256"])
        self.assertTrue(p["private_archive_not_public_Git"])
        limit = self.r["no_cross_carrier_identity_promotion"]
        self.assertEqual(set(limit),{"commercial_source_binaries_published","native_game_executed","native_original_palette_verified","native_sprite_action_names_or_timing_verified","official_character_pet_NPC_type_verified","same_historical_server_deployment_verified"})
        self.assertTrue(all(v is False for v in limit.values()))

    def test_07_historical_continuity_unchanged(self):
        self.assertEqual(self.r["source_full_CURRENT_unmodified_blob"],"c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertEqual(self.r["source_repository_HEAD_at_check"],"206a2b37171d735560a7c0b4bd801d4953f8b137")
        self.assertEqual(self.r["project_state"],{"StageA":"7 PARTIAL + 2 OPEN","StageBWiki":"GATED","R79":"PAUSED_NON_BLOCKING","overall_percent":None})

if __name__ == "__main__":
    unittest.main()
