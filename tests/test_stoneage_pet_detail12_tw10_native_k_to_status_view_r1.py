"""PET-DETAIL12: source-pinned original TW1 native K receiver -> status panel read evidence.

Original proprietary PE32 was re-read and independently decoded in a private
workspace. CI only validates public derived receipts and the preserved evidence
contract; it does not re-disassemble or execute private original binaries.
"""
import hashlib
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PATH="research/pets/PET-DETAIL-EVIDENCE12-TW10-NATIVE-K-TO-STATUS-VIEW-R1.json"
DOC="docs/continuity/STONEAGE-PET-DETAIL12-TW10-NATIVE-K-TO-STATUS-VIEW-20261122.md"

def read(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))

def gitblob(path):
    b=(ROOT/path).read_bytes()
    return hashlib.sha1(b"blob "+str(len(b)).encode("ascii")+b"\0"+b).hexdigest()

class OriginalTW10KPanelEvidenceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=read(PATH)
        cls.k=read(cls.d["linked_prior_receipts"]["native_K_field_map"]["path"])
        cls.album=read(cls.d["linked_prior_receipts"]["original_client_album"]["path"])

    def test_source_custody_and_unchanged_proprietary_boundary(self):
        d=self.d
        for key in ("native_K_field_map","original_client_album"):
            p=d["linked_prior_receipts"][key]
            self.assertEqual(gitblob(p["path"]),p["git_blob"])
        self.assertEqual(gitblob("docs/CURRENT-STATE.md"),
                         d["qualification"]["old_CURRENT_git_blob"])
        self.assertEqual(d["source"]["original_member_sha256"],
                         self.k["original_source"]["exe_sha256"])
        self.assertEqual(d["source"]["original_member_sha256"],
                         self.album["archive"]["files"]["source/sa_3.exe"]["sha256"])
        self.assertEqual(d["source"]["archive_sha256"],
                         self.album["archive"]["sha256"])
        self.assertFalse(d["source"]["original_binary_or_raw_instruction_bytes_published"])
        self.assertFalse(d["qualification"]["original_native_client_executed"])

    def test_same_original_108byte_status_structure_reaches_panel(self):
        evidence=self.d["native_K_to_UI_bridge"]
        m=self.k["k_parser"]
        self.assertEqual(m["stride"],108)
        self.assertEqual(int(evidence["slot_structure_base_va"],16),
                         int(m["slot_struct_base_va"],16))
        fields=evidence["field_reads"]
        self.assertEqual(len(fields),13)
        self.assertEqual(evidence["static_native_UI_read_count"],13)
        self.assertEqual(evidence["native_numeric_text_field_count"],9)
        self.assertEqual(evidence["native_element_visual_field_count"],4)
        src={x["token"]:x for x in m["field_map"]}
        self.assertEqual(len({x["k_data_token"] for x in fields}),13)
        self.assertEqual(len({x["native_instruction_va"] for x in fields}),13)
        for x in fields:
            k=src[x["k_data_token"]]
            self.assertEqual(x["field"],k["name_from_early_lineage"])
            self.assertEqual(x["struct_offset"],k["struct_offset"])
            self.assertEqual(int(x["access_target_va"],16),
                             int(evidence["slot_structure_base_va"],16)+x["struct_offset"])
            v=int(x["native_instruction_va"],16)
            self.assertGreaterEqual(v,int(evidence["original_native_display_window"]["start_va"],16))
            self.assertLess(v,int(evidence["original_native_display_window"]["end_exclusive_va"],16))
            self.assertTrue(x["byte_checked_from_verified_exe"])
        self.assertEqual({x["field"] for x in fields if x["ui_handling"]=="element_visual"},
                         {"earth","water","fire","wind"})

    def test_source_windows_and_old_album_not_new_roster(self):
        d=self.d
        self.assertEqual(d["native_K_to_UI_bridge"]["original_native_display_window"]["bytes"],1293)
        self.assertEqual(len(d["native_K_to_UI_bridge"]["original_native_display_window"]["sha256"]),64)
        self.assertEqual(d["old_client_album_crosscheck"]["full_table_sha256"],
                         self.album["table"]["sha256"])
        self.assertEqual(d["old_client_album_crosscheck"]["record_count"],181)
        self.assertEqual(d["old_client_album_crosscheck"]["valid_nonnegative_table_entries"],
                         len(self.album["records"]))
        self.assertEqual(d["old_client_album_crosscheck"]["missing_minus_one_entries"],
                         len(self.album["table"]["placeholder_graphics"]))
        self.assertEqual(d["old_client_album_crosscheck"]["record_stride"],28)
        names=d["native_K_to_UI_bridge"]["native_status_name_selection"]
        self.assertEqual(names["free_name_source_offset"],87)
        self.assertEqual(names["name_field_source_offset"],70)
        self.assertEqual(names["name_field_token"],20)
        self.assertEqual(names["free_name_field_token"],21)

    def test_no_promotion_to_original_official_birth_stats(self):
        q=self.d["qualification"]
        for key in ("new_early_TW10_official_pet_birth_stat_values_confirmed",
                    "actual_early_official_server_pet_masters_acquired",
                    "actual_early_official_server_K_sender_acquired",
                    "new_official_pet_species_confirmed",
                    "historical_dossiers_fully_restored"):
            self.assertEqual(q[key],0)
        self.assertEqual(q["historical_dossiers_unchanged"],124)
        self.assertFalse(q["native_client_rendering_original_screen_observed"])
        self.assertIsNone(q["overall_completion_percent"])
        self.assertEqual(q["stage_A"],"7_PARTIAL+2_OPEN")
        idx=(ROOT/"docs/pets/INDEX.md").read_text(encoding="utf-8")
        doc=(ROOT/DOC).read_text(encoding="utf-8")
        self.assertIn('STONEAGE-PET-DETAIL12-TW10-NATIVE-K-TO-STATUS-VIEW-20261122.md',idx)
        self.assertIn("PET-DETAIL12",doc)
        self.assertIn("PET-DETAIL12",idx)
        self.assertIn("原官方初生数值仍0项认证",idx)

if __name__=="__main__":
    unittest.main()
