"""PET126D public receipt checks; never pretend to re-execute the private original EXE."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REC = ROOT / "research/recovered/STONEAGE-PET126D-TW10-CLIENT-CAPTURE-FIVE-SLOT-STATIC-R1.json"
PRIOR = ROOT / "research/recovered/STONEAGE-PET126C-TW10-ORIGINAL-SOURCE-REACCESS-R1.json"
MATRIX = ROOT / "research/recovered/STONEAGE-PET-MODULE-20-FIELD-COVERAGE-AND-SOURCE-STOP-MATRIX-R1.json"

class OriginalTw10ClientCaptureStaticGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(REC.read_text(encoding="utf-8"))
        cls.p = json.loads(PRIOR.read_text(encoding="utf-8"))
        cls.m = json.loads(MATRIX.read_text(encoding="utf-8"))

    def test_private_byte_provenance_is_exact_not_new_species(self):
        r, p = self.r, self.p
        self.assertEqual(r["source"]["archive_sha256"],p["original_source"]["archive_sha256"])
        self.assertEqual(r["source"]["archive_bytes"],p["original_source"]["archive_bytes"])
        self.assertEqual(r["source"]["pe_member_sha256"],p["source_file_pins"]["source/sa_3.exe"]["sha256"])
        self.assertEqual(r["source"]["pe_member_bytes"],p["source_file_pins"]["source/sa_3.exe"]["bytes"])
        self.assertTrue(r["source"]["zip_crc_all_pass"])
        self.assertEqual(r["source"]["archive_members_rechecked_this_session"],379)
        self.assertFalse(r["source"]["native_program_executed_in_this_unit"])
        self.assertFalse(r["source"]["proprietary_original_published"])
        self.assertEqual(r["new_official_pet_species_proven"],0)

    def test_exact_local_five_slot_counter_bounded_by_evidence(self):
        r = self.r
        s = r["slot_counter"]
        start=int(s["array_start_va"],16)
        end=int(s["array_end_exclusive_va"],16)
        self.assertEqual(end-start,540)
        self.assertEqual((end-start)//s["element_stride_bytes"],5)
        self.assertEqual((end-start)%s["element_stride_bytes"],0)
        self.assertEqual(s["slot_count"],5)
        self.assertEqual(s["flag_width_bits"],16)
        self.assertEqual(s["count_if_flag_equals"],1)
        self.assertFalse(s["slot_species_identity_proven"])
        self.assertEqual(r["capture_gate"]["counter_call_target_va"],s["function_va"])
        self.assertEqual(r["capture_gate"]["compare_count_against"],5)
        self.assertEqual(r["second_counter_comparison"]["counter_target_va"],s["function_va"])
        self.assertEqual(r["second_counter_comparison"]["compare_count_against"],5)
        self.assertEqual(r["capture_gate"]["label_vas"],["0x455F00","0x455F08"])
        self.assertTrue(r["capture_gate"]["client_ui_branch_static_proven"])
        self.assertFalse(r["capture_gate"]["original_server_capture_accepted_proven"])
        self.assertFalse(r["capture_gate"]["total_owned_pet_capacity_proven"])
        self.assertEqual(len(r["source_code_windows"]),3)
        for w in r["source_code_windows"]:
            self.assertGreater(w["file_end_exclusive"],w["file_start"])
            self.assertEqual(int(w["virtual_address"],16),0x400000+w["file_start"])
            self.assertEqual(len(w["sha256"]),64)
            int(w["sha256"],16)

    def test_qualified_literal_client_ui_not_full_native_skill_or_capture(self):
        self.assertEqual(self.r["evidence_grade"],
                         "ORIGINAL_CLIENT_STATIC_LOCAL_CAPTURE_UI_CAPACITY_GATE")
        roles={x["role"] for x in self.r["other_pet_ui_literal_xrefs"]}
        self.assertEqual(roles,{"no_active_battle_pet","switch_pet","use_skill",
                                "no_pet","pet_mail_notice"})
        for s in self.r["other_pet_ui_literal_xrefs"]:
            self.assertEqual(s["file_offset"],int(s["label_va"],16)-0x400000)
        self.assertIn("SERVER_ENFORCED_CAPTURE_LIMIT_FIVE",
                      self.r["assertions_not_supported"])
        self.assertIn("ORIGINAL_PET_SKILL_EFFECT",
                      self.r["assertions_not_supported"])
        self.assertIn("IN_GAME_PET_RELEASE_CONFIRMED",
                      self.r["assertions_not_supported"])
        self.assertEqual(len(self.r["seven_dimensions"]),7)
        self.assertTrue(all(not d["closed"] for d in self.r["seven_dimensions"]))
        self.assertFalse(self.r["source_bounded_closed"])
        self.assertFalse(self.r["historically_complete"])
        self.assertFalse(self.r["native_runtime_verified"])
        self.assertFalse(self.m["source_bounded_closed"])

    def test_pc_only_year_locked_and_original_current_blob_byte_identical(self):
        self.assertEqual(self.r["scope"],"ORIGINAL_OFFICIAL_CLASSIC_2D_PC_ONLY")
        self.assertEqual(self.r["active_module"],"PET")
        self.assertEqual((self.r["working_year"],self.r["working_year_status"]),
                         (2026,"NOT_YEAR_AUDITED"))
        self.assertEqual(self.r["stage_A"],"7_PARTIAL_2_OPEN")
        self.assertEqual(self.r["stage_B_wiki"],"GATED")
        self.assertEqual(self.r["r79"],"PAUSED_NON_BLOCKING")
        self.assertIsNone(self.r["overall_percent"])
        p=ROOT / "docs/CURRENT-STATE.md"
        data=p.read_bytes()
        self.assertEqual(len(data),2709173)
        actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\\x00"+data).hexdigest()
        self.assertEqual(actual,self.r["historical_current_blob"])
        self.assertEqual(actual,"c89e0e33537990aa2132b47c40fef49a985a935c")

if __name__=="__main__":
    unittest.main()
