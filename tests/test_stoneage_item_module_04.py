"""Public source-derived ITEM04 check; proprietary pixels remain outside Git."""
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
ITEM02=ROOT/"research/recovered/STONEAGE-ITEM02-ORIGINAL-NUMERIC-EQUIPMENT-AND-TW1-RD-BOUNDARY-R1.json"
ITEM04=ROOT/"research/recovered/STONEAGE-ITEM04-TW10-FOUR-TERMINAL-RLE-SOURCE-CANVAS-PREFIX-R1.json"

class Item04SourceCanvasPrefixTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads(ITEM04.read_text(encoding="utf-8"))
        cls.p=json.loads(ITEM02.read_text(encoding="utf-8"))

    def test_original_parent_sha_and_full_dataset_conservation(self):
        r=self.r;p=self.p
        self.assertEqual(r["source_sha256"]["TW1_ADRN"],p["source_sha256"]["TW1_ADRN"])
        self.assertEqual(r["source_sha256"]["TW1_REAL"],p["source_sha256"]["TW1_REAL"])
        self.assertEqual(r["source_sha256"]["TW1_P3H_zip"],p["source_sha256"]["TW1_P3H"])
        self.assertEqual(r["source_sha256"]["mixed25_itemset_a"],p["source_sha256"]["itemset_a"])
        self.assertEqual(r["source_sha256"]["mixed25_itemset_b"],p["source_sha256"]["itemset_b"])
        self.assertEqual((r["source_item_aliases_reviewed"],r["TW1_ADRN_record_found"],r["TW1_no_ADRN_record"],r["TW1_strict_RD_decoded_retained"],r["TW1_strict_RD_failures_retained"]),(1667,836,831,832,4))
        self.assertEqual(r["TW1_ADRN_record_found"],r["TW1_strict_RD_decoded_retained"]+r["TW1_strict_RD_failures_retained"])

    def test_exact_four_known_original_rds_are_not_reclassified(self):
        previous={record[0]:record for record in self.p["original_tw1_rd_strict_failed_records"]}
        self.assertEqual(set(previous),{24077,24137,24138,24140})
        rows=self.r["rows"]
        self.assertEqual([r["alias"] for r in rows],[24077,24137,24138,24140])
        for row in rows:
            prior=previous[row["alias"]]
            with self.subTest(alias=row["alias"]):
                self.assertEqual([row["alias"],row["ordinal"],row["bytes"],row["width"],row["height"],row["packet_offset"],row["packets"],row["record_sha"],row["rd_sha"]],prior)
                self.assertEqual(row["source_original_RD_strict_status"],"DECODING_FAILED")

    def test_terminal_zero_run_is_exactly_one_out_of_canvas(self):
        for x in self.r["rows"]:
            with self.subTest(alias=x["alias"]):
                area=x["width"]*x["height"]
                self.assertEqual(x["original_RLE_decoded_length"],area+1)
                self.assertEqual(x["source_canvas_prefix_length"],area)
                self.assertEqual(x["last_opcode"],"0xC2")
                self.assertEqual(x["last_opcode_count"],2)
                self.assertEqual(x["last_opcode_output_before"],area-1)
                self.assertEqual(x["last_opcode_output_after"],area+1)
                self.assertEqual(x["last_two_decoded_indices"],[0,0])
                self.assertEqual(x["source_canvas_last_pixel_index"],0)
                self.assertTrue(x["full_original_RLE_stream_read"])
                self.assertTrue(x["independent_source_canvas_limited_decoder_matches"])

    def test_unique_source_prefix_sha_and_later_id_reference_coverage(self):
        r=self.r
        self.assertEqual(len({x["pixels_sha"] for x in r["rows"]}),4)
        self.assertEqual(sum(len(x["item_ids"]) for x in r["rows"]),7)
        self.assertEqual(sum(2*len(x["item_ids"]) for x in r["rows"]),14)
        self.assertEqual(len({i for x in r["rows"] for i in x["item_ids"]}),7)
        for x in r["rows"]:
            self.assertTrue(x["two_later_mixed25_itemsets_both_reference_ids"])
            self.assertFalse(x["original_client_render_and_item_deployment_verified"])
            for k in ("record_sha","rd_sha","pixels_sha","gray_sha","color_sha"):
                self.assertRegex(x[k],r"^[0-9a-f]{64}$")

    def test_private_deliverable_identity_without_original_art(self):
        v=self.r["private_delivery"]
        self.assertEqual((v["bytes"],v["ZIP_members"]),(39918,11))
        self.assertTrue(v["CRC_all_members_verified"])
        self.assertTrue(v["private_Library_upload_and_re_read_byte_identity_verified"])
        self.assertRegex(v["sha256"],r"^[0-9a-f]{64}$")
        self.assertEqual((v["original_index_prefix_PNG_count"],v["modern_color_flip_candidate_PNG_count"]),(4,4))
        bounds=self.r["negative_boundaries"]
        for flag in ("original_client_started","native_RD_overflow_handling_verified","exact_native_palette_and_vertical_flip_selector_verified",
                     "official_TW1_itemset_or_same_deployment_verified","mixed25_community_name_to_TW1_illustration_as_historical_fact",
                     "original_art_or_commercial_names_published_in_repo"):
            self.assertIs(bounds[flag],False)
        self.assertEqual(bounds["strict_RD_complete_decode_new_successes"],0)
        self.assertEqual(self.r["WORLD37_R2"]["claim_original_tail_executed"],False)

    def test_global_strict_decoder_still_rejects_one_extra_terminal_zero(self):
        from tools.stoneage_rd_codec import RDDecodeError,decode_legacy_rle
        # Synthetic negative control, NOT copied original RD bytes.
        synthetic=bytes([0x03,0x11,0x22,0x33,0xC2])
        self.assertEqual(decode_legacy_rle(synthetic),bytes([0x11,0x22,0x33,0,0]))
        with self.assertRaises(RDDecodeError):
            decode_legacy_rle(synthetic,expected_len=4)

if __name__=="__main__":
    unittest.main()
