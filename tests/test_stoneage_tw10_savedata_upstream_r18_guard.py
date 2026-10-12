"""R18 bounded static schema independent tamper controls (synthetic only)."""
import unittest
from tools.stoneage_tw10_savedata_upstream_r18 import (
    SCHEMA,STATUS,FLAGS,RUNTIME_SHA256,SAVEDATA_SHA256,
    EAX_CALL,EAX_WRITE,ECX_LOAD,SECOND_GLOBAL,EBX_WRITE,
    IMUL_SITE,HELPER_ANCHOR,
)
from tools.stoneage_tw10_savedata_upstream_r18_guard import validate

def specimen():
    return {
        "schema":SCHEMA, "status":STATUS,
        "runtime_sha256":RUNTIME_SHA256,"savedata_sha256":SAVEDATA_SHA256,
        "r17_original_identity_revalidated":True,"original_static_only":True,
        "eax_call_barrier":{
            "call_site_rva":EAX_CALL,"write_site_rva":EAX_WRITE,
            "call_identity":{"call_rva":EAX_CALL,"kind":"direct","direct_target_rva":0x1000},
            "direct_callee_model":{"original_helper_accepted":False,"native_io_executed":False},
            "candidate_graph_nodes":10,"candidate_graph_edges":10,
            "candidate_anchor_verified_entry":False,"eax_after_call_known":False,
            "callee_summary_admitted":False,"original_return_value_proven":False,
            "call_fallthrough_structural_only":True,
        },
        "secondary_global":{
            "read_site_rva":ECX_LOAD,"original_global_identity_proven":True,
            "global_value_known":False,"alias_reference_coverage_complete":False,
            "runtime_initialized":False,"same_object_as_primary_global_proven":False,
            "global_reference_candidates":{
                "scope":"linear_text_decode_candidates_not_reachable_execution",
                "all_indirect_references_covered":False,
                "globals":[{
                    "global_rva":SECOND_GLOBAL,"samples":[],"runtime_initialization_proven":False
                }],
            },
        },
        "ebx_graph":{
            "write_site_rva":EBX_WRITE,"anchor_rva":HELPER_ANCHOR,
            "nodes":20,"edges":22,
            "actual_function_entry_proven":False,"all_incoming_edges_proven":False,
            "value_known":False,"feasible_path_proven":False,
            "call_fallthrough_structural_only":True,"source_candidates":[],
        },
        "imul_stack":{
            "imul_site_rva":IMUL_SITE,"stack_offset_model_is_conditional_only":True,
            "stopped_at_original_memory_gap":True,
            "modeled_stack_offset_of_memory_operand":20,
            "real_esp_or_caller_frame_proven":False,
            "effective_memory_value_proven":False,
            "register_multiplier_value_proven":False,
            "callee_effect_summary_admitted":False,
        },
        **{k:False for k in FLAGS},
    }

class TestR18Guard(unittest.TestCase):
    def test_specimen_static_only(self):
        self.assertTrue(validate(specimen()))
    def test_native_promotion_blocked(self):
        x=specimen();x["native_save_io_executed"]=True
        with self.assertRaises(ValueError):validate(x)
    def test_call_return_value_promotion_blocked(self):
        x=specimen();x["eax_call_barrier"]["original_return_value_proven"]=True
        with self.assertRaises(ValueError):validate(x)
    def test_callee_model_promotion_blocked(self):
        x=specimen();x["eax_call_barrier"]["direct_callee_model"]["original_helper_accepted"]=True
        with self.assertRaises(ValueError):validate(x)
    def test_wrong_global_address_blocked(self):
        x=specimen();x["secondary_global"]["global_reference_candidates"]["globals"][0]["global_rva"]+=4
        with self.assertRaises(ValueError):validate(x)
    def test_global_runtime_alias_claim_blocked(self):
        x=specimen();x["secondary_global"]["same_object_as_primary_global_proven"]=True
        with self.assertRaises(ValueError):validate(x)
    def test_path_proof_blocked(self):
        x=specimen();x["ebx_graph"]["feasible_path_proven"]=True
        with self.assertRaises(ValueError):validate(x)
    def test_stack_caller_ownership_blocked(self):
        x=specimen();x["imul_stack"]["real_esp_or_caller_frame_proven"]=True
        with self.assertRaises(ValueError):validate(x)
    def test_raw_payload_field_blocked(self):
        x=specimen();x["secondary_global"]["original_binary"]="fake"
        with self.assertRaises(ValueError):validate(x)
    def test_misidentified_call_blocked(self):
        x=specimen();x["eax_call_barrier"]["call_site_rva"]+=1
        with self.assertRaises(ValueError):validate(x)
    def test_oversized_source_set_blocked(self):
        x=specimen();x["ebx_graph"]["source_candidates"]=[{}]*33
        with self.assertRaises(ValueError):validate(x)
    def test_static_original_identity_gate(self):
        x=specimen();x["r17_original_identity_revalidated"]=False
        with self.assertRaises(ValueError):validate(x)

if __name__=="__main__":
    unittest.main()
