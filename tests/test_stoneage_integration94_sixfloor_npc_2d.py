import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def load(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))
def chain(values):
    return hashlib.sha256("".join(values).encode("ascii")).hexdigest()

class Integration94SourceQualifiedNPC2D(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=load("research/recovered/STONEAGE-INTEGRATION94-SIX-FLOOR-18-NPC-TW1-ORIGINAL-2D-R1.json")
        cls.c=load("research/recovered/STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json")
        cls.p=load("research/recovered/STONEAGE-PET-MODULE-07-TW10-BATCH-PUBLIC-R1.json")
        cls.m=load("research/recovered/STONEAGE-MAP-SCENE-MODULE-04-955-ORIGINAL-DAT-4166-RD-PIXEL-INDEX-R1.json")
        cls.original=[r for r in cls.c["create_rows"] if r[0]=="genout/shop_m.create"]

    def test_01_precise_raw_CREATE_full_file_provenance(self):
        d=self.d["later_mixed25_actual_raw_original_CREATE"]
        m=next(x for x in self.c["source_files"] if x[0]==d["member_original_path"])
        self.assertEqual([m[1],m[2],m[3]],[d["source_size_bytes"],d["original_full_file_SHA256"],d["source_crc32"]])
        self.assertEqual((len(self.original),d["source_CREATE_blocks_total_actual_raw_byte_window_SHA_verified"]),(119,119))
        self.assertEqual(chain([r[4] for r in self.original]),d["original_all_119_SHA256_text_sequence_digest"])
        self.assertEqual(dict(Counter(r[11] for r in self.original)),d["literal_type_counts"])
        self.assertTrue(d["source_CREATE_file_raw_equal_from_both_archives"])
        self.assertEqual([x["CRC_members_success"] for x in d["two_existing_private_custody_archives"]],[131,136])

    def test_02_source_exact_18_CREATES_not_all_shopkeepers(self):
        rs=self.d["selected_original_later_npcgen_mugon_eighteen_exact_raw_bytes_source_rows"]
        self.assertEqual(len(rs),18)
        self.assertEqual([r["source_CREATE_ordinal"] for r in rs],[4,5,28,29,43,44,45,55,56,57,58,59,60,72,73,84,85,86])
        for x in rs:
            r=next(v for v in self.original if v[1]==x["source_CREATE_ordinal"])
            self.assertEqual([r[2],r[3],r[4],r[5],r[6],r[7],r[11]],
              [*x["source_exact_byte_window"],x["source_original_window_SHA256"],x["source_floor"],x["numeric_graphic"],x["borncorner_original"],x["source_type_literal"]])
            self.assertEqual(r[11],"npcgen_mugon")
        self.assertEqual(dict(Counter(r["source_floor"] for r in rs)),{1003:2,1103:2,1203:3,1303:6,1403:2,2003:3})

    def test_03_six_real_DAT_source_sha_prior_MAP04_no_new_bytes(self):
        d=self.d["six_original_DAT_floor_catalog_crosscheck_MAP04_not_raw_DAT_reread"]
        maps={x[0]:x for x in self.m["per_floor_source_rows"]}
        self.assertEqual(len(d),6)
        for x in d:
            a=maps[x["source_DAT_name"]]
            self.assertEqual(x["source_DAT_name"],f'{x["later_source_floor"]}.dat')
            self.assertEqual([a[1],a[2],a[3],a[4],a[6],a[7],a[11]],
              [x["prior_DAT_original_bytes"],x["prior_DAT_full_source_SHA256"],*x["prior_DAT_dimensions"],*x["prior_DAT_first_two_planes_numeric_occurrences"],x["prior_DAT_unmatched_source_RD_occurrences"]])
            self.assertEqual(x["prior_DAT_dimensions"],[30,30])
            self.assertFalse(x["actual_original_DAT_raw_bytes_reread_in_this_unit"])

    def test_04_separate_actual_TW1_15_SPR_group_sha(self):
        gs=self.d["separate_retail_TW1_original_15_SPR_source_groups"]
        base={r[0]:r for r in self.p["source_groups"]}
        self.assertEqual(len(gs),15)
        self.assertEqual([g["numeric_graphic"] for g in gs],sorted(set(x["numeric_graphic"] for x in self.d["selected_original_later_npcgen_mugon_eighteen_exact_raw_bytes_source_rows"])))
        for g in gs:
            r=base[g["numeric_graphic"]]
            self.assertEqual([r[1],r[2],r[3],r[4],r[5],r[6]],
               [g["source_group_index"],g["original_TW1_full_SPR_group_SHA256"],g["full_SPR_original_animation_count"],g["selected_source_frame_positions"],g["selected_three_source_action_direction0_sequence_headers"],g["distinct_source_RD_bitmaps"]])
            self.assertEqual(r[3],56)
            self.assertEqual([s[:2] for s in r[5]],[[0,0],[2,0],[1,0]])

    def test_05_45_source_sequences_323_original_frame_positions(self):
        gs=self.d["separate_retail_TW1_original_15_SPR_source_groups"]
        self.assertEqual(sum(len(g["selected_three_source_action_direction0_sequence_headers"]) for g in gs),45)
        self.assertEqual(sum(g["selected_source_frame_positions"] for g in gs),323)
        self.assertEqual(sum(g["distinct_source_RD_bitmaps"] for g in gs),245)

    def test_06_all_245_source_original_RD_index_and_sha_receipts(self):
        rows=self.d["original_RD_Palet1_candidate_bitmap_receipts"]
        src={x[0]:x for x in self.p["source_actual_pixel_receipts"]}
        expect=sorted(x for g in self.d["separate_retail_TW1_original_15_SPR_source_groups"] for x in g["selected_original_bitmap_numbers_sorted"])
        self.assertEqual(len(rows),245)
        self.assertEqual([x["bitmap_id"] for x in rows],expect)
        for x in rows:
            r=src[x["bitmap_id"]]
            self.assertEqual([x["prior_original_RD_block_SHA256"],x["prior_selected_Palet1_PNG_SHA256"],x["source_RD_width"],x["source_RD_height"]],
                             [r[2],r[8],r[5],r[6]])
        d=self.d["private_actual_source"]
        self.assertEqual(chain(x["prior_original_RD_block_SHA256"] for x in rows),d["selected_245_source_RD_original_bytes_SHA256_text_chain"])
        self.assertEqual(chain(x["prior_selected_Palet1_PNG_SHA256"] for x in rows),d["prior_canonical_Palet1_PNG_245_source_SHA256_text_chain"])

    def test_07_52_private_gallery_PNG_SHA_disagreement_kept(self):
        rows=self.d["original_RD_Palet1_candidate_bitmap_receipts"]
        wrong=[x for x in rows if not x["private_original_PET07_gallery_PNG_SHA_matches_prior_Palet1"]]
        self.assertEqual((len(rows)-len(wrong),len(wrong)),(193,52))
        self.assertEqual(self.d["private_actual_source"]["original_PNG_same_prior_Palet1_byte_SHA"],193)
        self.assertEqual(self.d["private_actual_source"]["original_PNG_different_prior_Palet1_byte_SHA"],52)
        self.assertEqual(self.d["private_actual_source"]["difference_52_concentrated_in_numeric_graphic"],[100250,100251,100252])
        self.assertEqual(len(self.d["private_actual_source"]["private_PET07_gallery_PNGs_selected_245_actual_byte_SHA256_text_chain"]),64)
        self.assertNotEqual(self.d["private_actual_source"]["private_PET07_gallery_PNGs_selected_245_actual_byte_SHA256_text_chain"],
                            self.d["private_actual_source"]["prior_canonical_Palet1_PNG_245_source_SHA256_text_chain"])

    def test_08_private_original_source_zip_Library_and_248_CRC(self):
        d=self.d["private_visual_observer"]
        self.assertEqual((d["zip_size"],d["original_zip_members_CRC_verified"]),(1575502,248))
        self.assertEqual(d["zip_SHA256"],"1ae2d376a8ca35cad5c19db24bdf71a94d13508dbe3a8894a8d7d62df735989e")
        self.assertTrue(d["private_Library_upload_succeeded"])
        self.assertTrue(d["private_independent_Library_retrieval_full_byte_SHA256_matched"])
        self.assertTrue(d["private_independent_Library_retrieval_all_248_CRC_success"])
        self.assertFalse(d["original_copyrighted_graphics_and_CREATE_public_git"])

    def test_09_18_real_source_2D_viewer_cards_and_54_clicks(self):
        d=self.d["private_visual_observer"]
        self.assertEqual((d["actual_chromium_page_set_content_source_cards"],d["actual_initial_images_loaded"],d["actual_browser_source_frame_action_clicks"]),(18,18,54))
        self.assertEqual(d["six_browser_source_floor_cards"],[2,2,3,6,2,3])
        self.assertEqual((d["actual_javascript_errors"],d["actual_external_network_requests"],d["actual_console_errors"]),(0,0,0))
        self.assertFalse(d["original_file_navigation_succeeded_claim"])
        self.assertFalse(d["original_native_client_executed"])

    def test_10_no_early_same_deployment_or_new_engine_claim(self):
        d=self.d
        self.assertEqual(d["counts"]["new_original_RD_decodes"],0)
        self.assertEqual(d["stage"]["A"],"7_PARTIAL_2_OPEN")
        self.assertEqual((d["stage"]["B"],d["stage"]["wiki"]),("GATED","GATED"))
        self.assertIsNone(d["stage"]["overall_percent"])
        self.assertFalse(d["private_visual_observer"]["original_native_client_executed"])

if __name__=="__main__":
    unittest.main()
