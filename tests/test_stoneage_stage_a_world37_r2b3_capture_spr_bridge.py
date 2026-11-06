"""Public replay of a source-bounded WORLD37 capture-condition to SPR-index bridge.

CI contains only rights-safe original-source-derived hashes and numbers; original
RAR, enemybase text and SPR payload are never committed or executed here.
"""
import copy
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "research/recovered"
BRIDGE = BASE / "STONEAGE-STAGE-A-WORLD37-R2B3-CAPTURE-ORIGINAL-SPR-BRIDGE-R1.json"
CAPTURE = BASE / "STONEAGE-STAGE-A-WORLD37-R2B-COMPILED-CAPTURE-REQUIRED-ITEMS-R1.json"
PETS = BASE / "STONEAGE-PET-MODULE-10-ORIGINAL-MIXED25-SERVER-TABLES-R1.json"

class CaptureSpriteBridge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.b = json.loads(BRIDGE.read_text(encoding="utf-8"))
        cls.c = json.loads(CAPTURE.read_text(encoding="utf-8"))
        cls.p = json.loads(PETS.read_text(encoding="utf-8"))

    def test_source_member_sha_crc_identity(self):
        s = self.b["original_source_integrity"]
        self.assertTrue(s["archive_full_sha256_reverified_in_this_session"])
        self.assertEqual(s["private_original_archive_sha256"],
                         self.p["preserved_original_rar"]["sha256"])
        self.assertEqual(s["private_original_archive_sha256"],self.c["archive_expected_sha256"])
        for name, got in s["original_archive_members_extracted_in_this_session"].items():
            orig=self.p["verified_original_archive_members"][name]
            self.assertEqual((got["bytes"],got["sha256"],got["crc32"]),
                             (orig["bytes"],orig["sha256"],orig["archive_record_crc32"]))
        self.assertFalse(s["original_program_executable_complete_SHA_CRC_qualified_this_session"])
        self.assertFalse(s["source_original_spr_5_animation_payload_member_found_in_this_archive"])

    def test_all_original_capture_keys_join_and_every_source_row(self):
        b=self.b
        rows=b["rows"]
        captures=self.c["original_condition_table"]["rows"]
        self.assertEqual(len(rows),len(captures))
        source_main=self.p["source_rows"]["enemybase.txt"]
        source_alt=self.p["source_rows"]["enemybase2.txt"]
        source_spr=self.p["source_rows"]["spradrn_5.bin"]
        old_names={x["char_int_key_53_value"]:x for x in self.c["enemybase_field6_numeric_join_candidates"]}
        self.assertEqual([v["source_char_int_key53"] for v in rows],
                         [v["char_int_key_53_value"] for v in captures])
        for derived, compiled in zip(rows,captures):
            key=compiled["char_int_key_53_value"]
            original=old_names[key]
            self.assertEqual(derived["source_capture_record_index"],compiled["source_record_index"])
            self.assertEqual(derived["source_required_item_ids"],compiled["required_item_id_candidates"])
            m=[x for x in source_main if x[1]==key]
            self.assertEqual(len(m),1)
            m=m[0]
            self.assertEqual((derived["configured_enemybase_column37_graphic_number"],
                              derived["configured_enemybase_column38_PETFLG"],
                              derived["configured_enemybase_normalized_fields_sha256"]), (m[2],m[3],m[17]))
            original_line=original["configured_enemybase_field6_same_numeric_candidate"]
            self.assertEqual((derived["configured_enemybase_physical_line"],
                              derived["configured_enemybase_original_line_sha256"],
                              derived["configured_enemybase_name_original_cp950"]),
                             (original_line["line"],original_line["original_row_sha256"],original_line["name_cp950"]))
            alt=[x for x in source_alt if x[1]==key]
            self.assertLessEqual(len(alt),1)
            if alt:
                self.assertIsNotNone(derived["alternate_enemybase2"])
                self.assertEqual((derived["alternate_enemybase2"]["column37_graphic_number"],
                                  derived["alternate_enemybase2"]["column38_PETFLG"],
                                  derived["alternate_enemybase2"]["normalized_fields_sha256"]),
                                 (alt[0][2],alt[0][3],alt[0][17]))
                self.assertEqual(derived["alternate_enemybase2"]["original_line_sha256"],
                                 original["alternate_enemybase2_field6_same_numeric_candidate"]["original_row_sha256"])
            else:
                self.assertIsNone(derived["alternate_enemybase2"])
            matches=[x for x in source_spr if x[1]==m[2]]
            self.assertLessEqual(len(matches),1)
            record=derived["preserved_original_spradrn_5_match"]
            if matches:
                self.assertIsNotNone(record)
                z=matches[0]
                self.assertEqual((record["physical_index"],record["source_graphic_number"],
                                  record["original_source_offset"],record["original_anim_count_field"],
                                  record["reserved_field"]),tuple(z))
                self.assertFalse(record["original_animation_payload_recovered_in_this_archive"])
            else:
                self.assertIsNone(record)
            self.assertFalse(derived["source_capture_runtime_entity_identity_verified"])

    def test_conservation_and_important_flag_zero(self):
        r=self.b
        x=r["conservation"]
        self.assertEqual((x["source_capture_rows"],x["source_item_references"],
                          x["source_distinct_item_ids"]), (11,13,12))
        self.assertEqual((x["distinct_configured_graphic_numbers"],x["PETFLG_1_rows"],
                          x["PETFLG_0_rows"]), (11,10,1))
        self.assertEqual((x["one_to_one_source_spr_index_graphics"],
                          x["graph_numbers_absent_within_this_single_spradrn_index"]), (5,6))
        self.assertEqual((x["original_spradrn_total_positions"],
                          x["original_spradrn_unique_graphic_ids"]), (847,841))
        self.assertEqual(x["alternate_enemybase2_same_numeric_graphic_and_PETFLG_rows"],7)
        self.assertEqual(x["original_sprite_images_or_animation_frames_recovered_now"],0)
        self.assertEqual({v["source_char_int_key53"]:v["configured_enemybase_column38_PETFLG"] for v in r["rows"] if v["configured_enemybase_column38_PETFLG"]==0},{8:0})
        self.assertEqual(sorted(v["source_char_int_key53"] for v in r["rows"] if v["preserved_original_spradrn_5_match"]),[8,524,777,796,812])

    def test_no_runtime_or_official_promotion(self):
        self.assertTrue(self.b["scope"].startswith("STAGE_A_MIXED25_COMMUNITY"))
        for name,val in self.b["negative_boundaries"].items():
            if isinstance(val,bool):
                self.assertFalse(val,name)
        self.assertIsNone(self.b["negative_boundaries"]["overall_completion_percent"])
        self.assertEqual(self.b["negative_boundaries"]["stageA"],"7_PARTIAL_2_OPEN")
        self.assertIn("CRC/SHA-verified",self.b["next"])

if __name__=="__main__":
    unittest.main()
