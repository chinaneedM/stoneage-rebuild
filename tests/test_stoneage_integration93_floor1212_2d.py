import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

class Integration93Original2D(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=load("research/recovered/STONEAGE-INTEGRATION93-FLOOR1212-ORIGINAL-2D-R1.json")
        cls.c=load("research/recovered/STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json")
        cls.p=load("research/recovered/STONEAGE-PET-MODULE-07-TW10-BATCH-PUBLIC-R1.json")

    def test_01_source_file_custody(self):
        s=self.d["community_source"]
        row=next(x for x in self.c["source_files"] if x[0]==s["source_path"])
        self.assertEqual(row,[s["source_path"],s["source_bytes"],s["sha256"],s["crc32"],"create"])
        self.assertFalse(s["fresh_raw_CREATE_byte_read"])

    def test_02_original_four_CREATE_spans_and_coordinates(self):
        rs=self.d["four_original_create_numeric_rows_and_independent_TW1_original_SPR_groups"]
        self.assertEqual([x["ordinal"] for x in rs],[14,15,16,17])
        self.assertEqual([x["graphic_numeric"] for x in rs],[100326,100265,100259,100294])
        self.assertEqual([x["original_borncorner"][:2] for x in rs],[[12,19],[14,19],[16,20],[18,19]])
        for x in rs:
            r=next(z for z in self.c["create_rows"] if z[0]=="genout/nevent_03.create" and z[1]==x["ordinal"])
            self.assertEqual([r[2],r[3],r[4],r[5],r[6],r[7],r[11],r[13]],
              [x["original_byte_offset"],x["original_span_bytes"],x["original_byte_span_SHA256"],x["floor"],x["graphic_numeric"],x["original_borncorner"],x["original_npcgen_type"],x["original_source_template"]])
            self.assertEqual((r[5],r[11]),(1212,"npcgen_man"))

    def test_03_original_TW1_SPR_group_sha_and_12_sequences(self):
        source={x[0]:x for x in self.p["source_groups"]}
        rs=self.d["four_original_create_numeric_rows_and_independent_TW1_original_SPR_groups"]
        for x in rs:
            self.assertEqual(x["TW1_source_full_SPR_group"],source[x["graphic_numeric"]])
            self.assertEqual(source[x["graphic_numeric"]][3],56)
            self.assertEqual([a[:2] for a in source[x["graphic_numeric"]][5]],[[0,0],[2,0],[1,0]])
        self.assertEqual(sum(len(x["TW1_source_full_SPR_group"][5]) for x in rs),12)

    def test_04_ordered_frame_positions_and_70_distinct_bitmaps(self):
        rs=self.d["four_original_create_numeric_rows_and_independent_TW1_original_SPR_groups"]
        self.assertEqual([x["TW1_source_full_SPR_group"][4] for x in rs],[20,22,19,35])
        self.assertEqual([x["TW1_source_full_SPR_group"][6] for x in rs],[16,22,17,15])
        self.assertEqual(sum(x["TW1_source_full_SPR_group"][4] for x in rs),96)
        ids=[i for x in rs for i in x["selected_source_bitmap_ids"]]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertEqual(len(ids),70)

    def test_05_all_70_original_RD_PNG_sha_lineages(self):
        source={x[0]:x for x in self.p["source_actual_pixel_receipts"]}
        rows=self.d["selected_original_TW1_source_RD_and_PNG_source_sha_rows"]
        ids=[i for x in self.d["four_original_create_numeric_rows_and_independent_TW1_original_SPR_groups"] for i in x["selected_source_bitmap_ids"]]
        self.assertEqual([x[0] for x in rows],sorted(ids))
        for x in rows:self.assertEqual(x,source[x[0]])

    def test_06_private_actual_viewer_does_not_prove_native_runtime(self):
        a=self.d["private_custody"]
        self.assertEqual((a["ZIP_bytes"],a["ZIP_members_and_CRC_pass"]),(474219,72))
        self.assertEqual(a["ZIP_sha256"],"ffcee80fc069ec364af35422bdb54b1c951091c7129637f373f356e81686ca50")
        self.assertEqual((a["chromium_real_four_cards_loaded"],a["chromium_four_cards_three_buttons_each"]),(4,12))
        self.assertEqual((a["chromium_JS_errors"],a["chromium_external_requests"]),(0,0))
        self.assertFalse(a["raw_file_URL_navigation_succeeded"])
        self.assertFalse(a["uploaded_to_public_Git"])

    def test_07_cross_source_identity_and_stage_guards(self):
        self.assertEqual(self.d["status"],"CROSS_BUILD_SOURCE_BOUND_NOT_ORIGINAL_GAMEPLAY")
        self.assertEqual(self.d["taiwan_v1_sprite_source"]["new_original_RD_decodes"],0)
        self.assertEqual(self.d["counts"]["source_frame_occurrences"],96)
        self.assertEqual(self.d["counts"]["unique_private_original_pngs_sha_checked"],70)
        self.assertIsNone(self.d["status_gates"]["overall_percent"])
        self.assertEqual(self.d["status_gates"]["Stage_B"],"GATED")

if __name__=="__main__":unittest.main()
