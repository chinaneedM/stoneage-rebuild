"""BATTLE181: only public source-derived provenance and negative boundaries; private originals not present in CI."""
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
CURRENT=ROOT/"research/recovered/STONEAGE-O16-TW10-BATTLE-NATIVE-PALETTE-INTERLEAVE-R1.json"
ITEM04=ROOT/"research/recovered/STONEAGE-ITEM04-TW10-FOUR-TERMINAL-RLE-SOURCE-CANVAS-PREFIX-R1.json"
B181=ROOT/"research/recovered/STONEAGE-STAGE-A-BATTLE181-TW10-SAB6729-SOURCE-CANVAS-R1.json"

class Battle181SourceBoundaryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old=json.loads(CURRENT.read_text(encoding="utf-8"))
        cls.item=json.loads(ITEM04.read_text(encoding="utf-8"))
        cls.new=json.loads(B181.read_text(encoding="utf-8"))
    def test_exact_original_tw10_source_lineage(self):
        n=self.new;o=self.old["original_source"];h=n["source_sha256"];i=self.item["source_sha256"]
        for key,expected in (
            ("P3H_full_archive",o["archive_sha256"]),("original_ADRN",o["adrn_sha256"]),
            ("original_REAL",o["real_sha256"]),("original_battle_1_bin",o["battle_1_bin_sha256"]),
            ("original_Palet_1",i["TW1_Palet_1"]),("original_RD6729",i["TW1_REAL"] and self.old["source_bitmap_coverage"]["source_rd_codec_open_sha256"])):
            self.assertEqual(h[key],expected)
        self.assertEqual(h["P3H_full_archive"],i["TW1_private_P3H_zip"])
        self.assertEqual(h["original_ADRN"],i["TW1_ADRN"])
        self.assertEqual(h["original_REAL"],i["TW1_REAL"])
        self.assertEqual(n["source_size_bytes"]["P3H"],o["archive_bytes"])
    def test_original_SAB181_exact_documented_sha(self):
        n=self.new["source_BATTLE181"];prev=self.old["battle_sab_records"]
        r=next(x for x in prev if x["id"]==181)
        self.assertEqual((r["bytes"],r["packed_offset"]),(804,145524))
        self.assertEqual(self.new["source_sha256"]["original_battle181_SAB"],r["sha256"])
        self.assertEqual((n["SAB_id"],n["grid_rows"],n["grid_columns"],n["grid_u16_BE_cells"]),(181,20,20,400))
        self.assertTrue(n["standalone_SAB181_equals_same_archive_battle_1_slice"])
    def test_RD6729_exact_original_item04_prefix_not_strict(self):
        row=next(x for x in self.item["rows"] if x["ordinal"]==6729)
        x=self.new["original_RD6729"];n=self.new["source_BATTLE181"];h=self.new["source_sha256"]
        self.assertEqual((row["width"],row["height"],row["original_RLE_decoded_length"],row["source_canvas_prefix_length"]),(40,30,1201,1200))
        self.assertEqual((row["alias"],row["rd_sha"],row["pixels_sha"]),(24140,h["original_RD6729"],h["original_RD6729_bounded_canvas_indices"]))
        self.assertEqual((x["source_dimensions"],x["canvas_declared_pixels"],x["original_RLE_stream_decoded_pixel_count"]),([40,30],1200,1201))
        self.assertEqual((x["terminal_opcode"],x["terminal_zero_overrun_pixels"]),("0xC2",1))
        self.assertEqual((n["source_only_problem_bitmapno"],n["problem_occurrences"],n["original_grid_6729_coordinate_zero_based"]),(6729,1,{"x":0,"y":13}))
    def test_strict_boundary_and_source_bounded_canvas_do_not_conflate(self):
        n=self.new["source_BATTLE181"];b=self.old["source_bitmap_coverage"];d=self.new["continuity"]
        self.assertEqual((n["unique_original_adrn_bitmap_IDs"],n["strict_original_RD_decoded_unique"],n["bounded_source_canvas_prefix_unique"]),(65,64,1))
        self.assertTrue(n["all_400_cells_resolved_to_original_source_canvas_indices"])
        self.assertTrue(n["all_65_exact_original_RD_and_ADRN_SHA_verified"])
        self.assertEqual((b["source_rd_decoded"],b["source_rd_codec_open_count"],b["full_scene_source_RD_coverage"]),(2295,1,217))
        self.assertTrue(d["historical_O16_217_of_218_strict_full_RD_maps_preserved"])
        self.assertFalse(d["strict_native_218_of_218_claim"])
    def test_persisted_private_deliverable_identity_only(self):
        x=self.new["private_delivery"]
        self.assertEqual((x["file_bytes"],x["zip_members"]),(805734,4))
        self.assertTrue(x["all_ZIP_CRC_verified"] and x["library_saved_and_re_read_full_sha_verified"])
        for field in ("sha256","candidate_isometric_PNG_sha256","annotated_source_location_PNG_sha256","source_tile_detail_PNG_sha256","private_source_and_full_400_cell_grid_JSON_sha256"):
            self.assertRegex(x[field],r"^[0-9a-f]{64}$")
        self.assertTrue(x["file_name"].startswith("StoneAge-BATTLE181-private-"))
    def test_historical_native_and_copyright_negative_boundaries(self):
        k=self.new["negative_boundaries"]
        for field in ("whole_original_SAB_400_grid_and_original_RD_payload_in_Git","original_client_3d_or_battle_runtime_executed",
                      "original_native_terminal_RLE_extra_pixel_handling_proven","original_native_battle181_selected_as_map_in_real_fight",
                      "exact_original_native_palette_or_layer_order_verified","later_mixed25_item_id_to_official_TW10_bitmap_identity_promoted",
                      "WORLD37_R2_original_GMSV_available"):
            self.assertIs(k[field],False)
        self.assertIs(k["source_bounded_canvas_pixels_are_not_a_strict_native_decode"],True)
        self.assertEqual((k["Stage_A"],k["Stage_B_wiki"],k["R79"],k["overall_percent"]),("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING",None))

if __name__=="__main__":
    unittest.main()
