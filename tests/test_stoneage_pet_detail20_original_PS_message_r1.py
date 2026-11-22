"""PET-DETAIL20 original TW1 PS message source-only regression and negative claims."""
import hashlib
import importlib.util
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RECEIPT="research/pets/PET-DETAIL-EVIDENCE20-TW10-ORIGINAL-PS-REQUEST-SEND-REPLY-R1.json"
TOOL="tools/stoneage_pet_detail20_tw10_original_PS_request_response_audit.py"

def load(path): return json.loads((ROOT/path).read_text(encoding="utf-8"))
def blob_sha(path):
    data=(ROOT/path).read_bytes()
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()

class SourceBoundPET20(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=load(RECEIPT)
        spec=importlib.util.spec_from_file_location("private_tw10_audit20",ROOT/TOOL)
        cls.audit=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.audit)

    def test_original_identity_and_earlier_blobs_unchanged(self):
        src=self.r["source"]
        self.assertEqual(src["archive_sha256"],self.audit.ZIP_SHA)
        self.assertEqual(src["exe_sha256"],self.audit.EXE_SHA)
        self.assertEqual(src["archive_bytes"],self.audit.ZIP_BYTES)
        self.assertEqual(src["exe_bytes"],self.audit.EXE_BYTES)
        self.assertTrue(src["original_source_zip_and_exe_reopened_this_work"])
        self.assertFalse(src["original_game_runtime_executed"])
        self.assertFalse(src["original_game_source_bytes_publicly_distributed"])
        for pinned in self.r["prior_source_guard"].values():
            self.assertEqual(blob_sha(pinned["path"]),pinned["blob"])
        self.assertEqual(blob_sha("docs/CURRENT-STATE.md"),self.r["limit_guards"]["preserved_docs_current_state_git_blob"])

    def test_all_nine_native_code_sha_windows_and_49_objdump_anchors(self):
        self.assertEqual(len(self.r["source_windows"]),9)
        self.assertEqual(len(self.audit.WINDOWS),9)
        for w in self.r["source_windows"]:
            self.assertEqual(self.audit.WINDOWS[w["name"]],(int(w["begin"],16),int(w["end_exclusive"],16),w["sha256"]))
            self.assertEqual(w["size"],int(w["end_exclusive"],16)-int(w["begin"],16))
        self.assertEqual(len(self.audit.OPCODES),27)
        self.assertEqual(len(self.audit.ASM),49)
        self.assertEqual(len(self.audit.LITERALS),3)
        checks=self.r["direct_original_validation"]
        self.assertEqual((checks["source_window_sha256_checks"],checks["original_raw_opcode_checks"],checks["independent_objdump_instruction_anchors"],checks["embedded_literal_checks"]),(9,27,49,3))

    def test_PS_wire_literal_and_socket_queue_not_live_capture(self):
        r=self.r["packet_code_path"]
        self.assertEqual(r["original_protocol_command_ascii"],"PS")
        self.assertEqual(self.audit.LITERALS["protocol_tag_PS"],(0x459834,b"PS\x00"))
        self.assertEqual(self.audit.LITERALS["material_slot_formatter"],(0x45c3a4,b"%d|\x00"))
        self.assertEqual(r["first_candidate_slot_index"],5)
        self.assertEqual(r["last_candidate_slot_index"],19)
        self.assertEqual(r["state_stride_bytes"],32)
        self.assertTrue(r["output_slot_index_list_not_item_IDs"])
        self.assertEqual(r["outbound_request_serializer_va"],"0x419090")
        self.assertEqual(r["outbound_queue_address"],"0x17f1e34")
        self.assertEqual(r["Winsock_send_call_va"],"0x42eb33")
        self.assertEqual(r["Winsock_send_import_jump_va"],"0x448466")
        self.assertEqual(self.r["direct_original_validation"]["import_ordinal"],19)
        self.assertTrue(r["call_queued_static_source_proven"])
        self.assertFalse(r["real_online_packet_sent_or_captured"])
        self.assertIsNone(r["exact_runtime_encrypted_wire_bytes"])

    def test_original_reply_only_failure_display_for_zero(self):
        r=self.r["reply_code_path"]
        self.assertEqual(r["same_PS_literal_ref_va"],"0x41a50c")
        self.assertEqual(r["response_handler_entry"],"0x433030")
        self.assertEqual(r["parsed_response_fields_count"],4)
        self.assertEqual(r["client_pending_set_after_request_va"],"0x42461a")
        self.assertEqual(r["client_pending_cleared_on_PS_response_va"],"0x43303c")
        self.assertEqual(r["failure_CP950_original_literal"],"失敗！")
        self.assertEqual(self.audit.LITERALS["client_zero_response_message"],(0x45c9c4,"失敗！".encode("cp950")+b"\x00"))
        self.assertFalse(r["nonzero_result_equates_to_proven_success"])
        self.assertFalse(r["live_original_PS_response_packet_captured"])

    def test_strict_official_boundary_and_continuity(self):
        g=self.r["limit_guards"]
        for key in ("original_TW1_official_server_PetSkill_master","original_actual_W_packet",
                    "original_actual_PS_packet","original_pet_innate_skill_loadout",
                    "original_material_consumption_rules","original_recipe_formula_and_success_probability"):
            self.assertIsNone(g[key])
        self.assertEqual(g["original_TW10_pet_dossiers_PARTIAL"],124)
        self.assertEqual(g["original_TW10_pet_dossiers_historically_complete"],0)
        self.assertEqual(g["original_TW10_verified_new_species"],0)
        self.assertIsNone(g["overall_percent"])
        self.assertIn("PET-DETAIL20",(ROOT/"docs/pets/INDEX.md").read_text(encoding="utf-8"))
        self.assertIn("PET-DETAIL21",self.r["next"])

if __name__=="__main__": unittest.main()
