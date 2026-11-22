"""PET-DETAIL16: actual original TW1 native pet battle skill logic source receipt guards."""
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = "research/pets/PET-DETAIL-EVIDENCE16-TW10-NATIVE-BATTLE-SKILL-ID-AND-TARGET-R1.json"
REPORT = "docs/continuity/STONEAGE-PET-DETAIL16-TW10-ORIGINAL-BATTLE-SKILL-ID-TARGET-20261122.md"
SCRIPT = "tools/stoneage_pet_detail16_tw10_battle_skill_audit.py"

def read(p):
    return json.loads((ROOT / p).read_text(encoding="utf-8"))

def git_blob(p):
    b = (ROOT / p).read_bytes()
    return hashlib.sha1(b"blob " + str(len(b)).encode("ascii") + b"\0" + b).hexdigest()

class Detail16NativeBattleSkill(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = read(RECEIPT)
        spec = importlib.util.spec_from_file_location("detail16_verified_source_replay", ROOT / SCRIPT)
        cls.source_audit = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.source_audit)

    def test_original_client_receipts_and_previous_source_boundary(self):
        d = self.d
        self.assertTrue(d["source"]["original_zip_and_member_independently_read_this_work"])
        self.assertEqual(d["source"]["archive_byte_size"], 372626292)
        self.assertEqual(d["source"]["original_executable_byte_size"], 425984)
        self.assertEqual(d["source"]["original_executable_sha256"], self.source_audit.EXE_SHA)
        self.assertEqual(d["source"]["archive_sha256"], self.source_audit.ZIP_SHA)
        for evidence in d["prior_pinned"].values():
            self.assertEqual(git_blob(evidence["path"]), evidence["git_blob"])
        self.assertEqual(git_blob("docs/CURRENT-STATE.md"),
                         d["qualification"]["original_current_state_blob"])

    def test_seven_native_windows_and_32_disassembler_checks_and_14_byte_operands(self):
        d = self.d
        result = d["private_original_source_checks"]
        self.assertEqual(result["source_windows_sha256_verified"], 7)
        self.assertEqual(result["private_disassembler_instruction_anchors_verified"], 32)
        self.assertEqual(result["private_direct_original_bytes_operand_checks_verified"], 14)
        self.assertEqual(len(result["source_windows"]), 7)
        self.assertEqual(len(result["checked_little_endian_operands"]), 14)
        self.assertEqual(len(self.source_audit.WINDOWS), 7)
        self.assertEqual(len(self.source_audit.ASM), 32)
        self.assertEqual(len(self.source_audit.OPERANDS), 14)
        for window in result["source_windows"]:
            label = window["name"]
            start, end, h = self.source_audit.WINDOWS[label]
            self.assertEqual(start, int(window["start_va"], 16))
            self.assertEqual(end, int(window["end_exclusive_va"], 16))
            self.assertEqual(h, window["sha256"])
            self.assertEqual(window["byte_length"], end-start)
        for item in result["checked_little_endian_operands"]:
            k = int(item["at_va"], 16)
            self.assertEqual(self.source_audit.OPERANDS[k],
                             (item["operand_le_offset_bytes"],
                              int(item["operand_value_hex"], 16)))

    def test_original_skill_source_offsets_and_five_pet_lookup(self):
        d = self.d
        battle = d["native_battle_skill_logic"]
        lookup = d["cross_carried_pet_skill_id_lookup"]
        self.assertEqual([battle[f"W_{name}_relative_offset"] for name in
                          ("presence", "skill_id", "field_context", "target_class", "name", "comment")],
                         [0, 2, 4, 6, 8, 33])
        self.assertEqual(battle["W_record_per_pet"], 7)
        self.assertEqual(battle["W_record_bytes"], 106)
        self.assertEqual(battle["W_pet_stride_bytes"], 742)
        self.assertEqual(battle["native_target_integer_dispatch_range_inclusive"], [0, 7])
        self.assertFalse(battle["target_number_to_actual_effects_or_gameplay_targets_confirmed"])
        self.assertTrue(lookup["supports_five_pet_slot_scan_in_original_client"])
        self.assertEqual(lookup["slot_K_stride_bytes"], 108)
        self.assertEqual(lookup["W_per_skill_advance_bytes"], 106)
        self.assertEqual(lookup["W_per_pet_advance_bytes"], 742)
        self.assertEqual(lookup["search_end_exclusive_W_skill_ID_address"], "0x17f8968")
        self.assertEqual(lookup["K_plus_104_state_semantics"], "NOT_RECOVERED")
        self.assertTrue(lookup["search_end_exclusive_equals_first_ID_plus_5_pet_buffers"])
        self.assertEqual(0x17f7aea+5*742, 0x17f8968)

    def test_two_original_numeric_ID_references_not_official_skill_names(self):
        d = self.d
        lookup = d["cross_carried_pet_skill_id_lookup"]
        self.assertEqual([s["original_exe_compiled_ID_decimal"] for s in lookup["candidate_callers"]], [201, 200])
        for x in lookup["candidate_callers"]:
            self.assertIsNone(x["name"])
            self.assertIsNone(x["effect"])
        self.assertFalse(lookup["original_official_species_having_200_or_201_confirmed"])
        self.assertFalse(lookup["original_200_or_201_skill_name_effect_confirmed"])
        self.assertFalse(lookup["original_server_status_SKILL_packet_captured"])
        q = d["qualification"]
        self.assertEqual(q["new_original_native_PC_compiled_numeric_skill_IDs_200_201_detected"], 2)
        for key in ("original_2000_pet_born_skills_confirmed",
                    "new_official_skill_definitions", "new_confirmed_skill_ID_to_name_pairs",
                    "historically_fully_restored_pet_profiles"):
            self.assertEqual(q[key], 0)
        self.assertIsNone(q["overall_percent"])
        self.assertTrue(q["all_124_TW1_pet_profiles_PARTIAL"])

    def test_published_report_and_PET_only_index(self):
        report = (ROOT / REPORT).read_text(encoding="utf-8")
        idx = (ROOT / "docs/pets/INDEX.md").read_text(encoding="utf-8")
        for term in ("PET-DETAIL16", "0x4250D0", "0x4033CD", "200", "201", "PARTIAL"):
            self.assertIn(term, report)
        self.assertIn("PET-DETAIL16", idx)
        self.assertFalse(self.d["source"]["original_executable_executed"])
        self.assertFalse(self.d["source"]["original_software_source_bytes_published"])

if __name__ == "__main__":
    unittest.main()
