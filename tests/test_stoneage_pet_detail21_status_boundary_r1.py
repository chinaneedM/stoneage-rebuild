"""PET-DETAIL21 strictly source-bound original TW1 PS vs independent pet/item status audit."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RECEIPT="research/pets/PET-DETAIL-EVIDENCE21-PS-STATUS-K-W-I-SOURCE-BOUNDARY-R1.json"
def read(path): return json.loads((ROOT/path).read_text(encoding="utf-8"))
def git_blob(path):
    b=(ROOT/path).read_bytes()
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()

class Pet21SourceBoundary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=read(RECEIPT)
        cls.p=read("research/pets/PET-DETAIL-EVIDENCE20-TW10-ORIGINAL-PS-REQUEST-SEND-REPLY-R1.json")
        cls.k=read("research/recovered/STONEAGE-PET126E-TW10-K-STATUS-CAPTURE-STATIC-R1.json")
        cls.s=read("research/clients/STONEAGE-TW10-GAMEPLAY-SCHEMA-R1.json")

    def test_pinned_prior_source_bytes_not_modified(self):
        for path,sha in self.r["pinned_source_blobs"].items():
            self.assertEqual(git_blob(path),sha,path)

    def test_original_ps_anchors_do_not_invent_packet(self):
        r=self.r["prior_verified_original_PS"]
        p=self.p
        self.assertEqual(r["request_command"],p["packet_code_path"]["original_protocol_command_ascii"])
        self.assertEqual(r["outgoing_material_representation"],"%d|")
        self.assertEqual((r["selected_item_indices"]["min"],r["selected_item_indices"]["max"]),(5,19))
        self.assertEqual(r["response_handler_va"],p["reply_code_path"]["response_handler_entry"])
        self.assertEqual(r["pending_flag_reset_va"],p["reply_code_path"]["client_pending_cleared_on_PS_response_va"])
        self.assertEqual(r["zero_value_failure_message"],"失敗！")
        self.assertEqual(r["response_parsed_field_count"],4)
        self.assertFalse(r["nonzero_means_success_proven"])
        self.assertIsNone(r["actual_PS_packet"])

    def test_four_independent_client_status_channels_are_exact(self):
        expected={
           "status_pet_full":("S","K","0x2fe94",21),
           "pet_skill_view_slot":("S","W","0x30b4f",5),
           "inventory_full_slot":("S","I","0x30922",9),
           "inventory_incremental_record":("I",None,"0x325f0",10)
        }
        cs=self.r["independently_documented_client_status_update_channels"]
        self.assertEqual(set(x["record"] for x in cs),set(expected))
        for x in cs:
            source=self.s["records"][x["record"]]
            self.assertEqual((x["protocol"],x["category"],x["callback_rva"],x["field_count"]),expected[x["record"]])
            self.assertEqual(x["field_names"],[f["name"] for f in source["fields"]])
            self.assertFalse(x["is_verified_as_caused_by_PS"])
        self.assertIn("max_skill_slots",cs[0]["field_names"])
        self.assertIn("skill_id",cs[1]["field_names"])

    def test_tw1_original_k_record_and_causal_boundary(self):
        k=self.r["original_K_local_slot_evidence"]
        self.assertEqual(k["callback_va"],self.k["k_parser"]["callback_va"])
        self.assertEqual(k["in_memory_pet_slots_count"],self.k["capture_join"]["count_total_slots"])
        self.assertEqual(k["per_slot_record_stride_bytes"],self.k["k_parser"]["stride"])
        self.assertFalse(k["server_live_pet_grant_proven"])
        self.assertTrue(all(v is None for name,v in self.r["cross_message_causality"].items() if name!="conclusion"))
        self.assertEqual(self.r["limits"]["TW10_source_named_pet_dossiers_partial"],124)
        self.assertEqual(self.r["limits"]["TW10_complete_official_historical_pet_dossiers"],0)
        self.assertIsNone(self.r["limits"]["overall_completion_percent"])
        self.assertFalse(self.r["original_source_reopened_this_work"])
        self.assertFalse(self.r["original_client_executed_this_work"])
        self.assertFalse(self.r["original_server_packet_observed_this_work"])
        self.assertIn("PET-DETAIL21",(ROOT/"docs/pets/INDEX.md").read_text(encoding="utf-8"))
        self.assertIn("PET-DETAIL21",(ROOT/"README.md").read_text(encoding="utf-8"))

if __name__=="__main__": unittest.main()
