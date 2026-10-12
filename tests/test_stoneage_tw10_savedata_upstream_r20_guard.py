"""R20 synthetic tamper guards; specimen is NOT an original-derived report."""
import unittest
from tools.stoneage_tw10_savedata_upstream_r20 import (
    SCHEMA,STATUS,FLAGS,RUNTIME_SHA256,SAVEDATA_SHA256,
    SECOND_CALL,THIRD_GLOBAL,PUSH_SITE,ALIAS_SITE,EBX_TARGET,EAX_CALL,
)
from tools.stoneage_tw10_savedata_upstream_r20_guard import validate

def specimen():
    return {
      "schema":SCHEMA,"status":STATUS,
      "runtime_sha256":RUNTIME_SHA256,"savedata_sha256":SAVEDATA_SHA256,
      "r19_original_identity_revalidated":True,"static_only":True,
      "second_call":{
        "call_identity":{"call_rva":SECOND_CALL,"kind":"memory_indirect"},
        "fallthrough_structural_only":True,
        "actual_entry_verified":False,"all_incoming_edges_proven":False,
        "runtime_call_target_proven":False,"callee_effect_summary_admitted":False,
        "return_value_in_eax_proven":False,
        "executed_write_at_second_global_proven":False,
        "candidate_nodes":10,"candidate_edges":10,"target_register_sources":[]
      },
      "third_global":{
        "target_virtual_rva":THIRD_GLOBAL,"push_rva":PUSH_SITE,
        "source_operand":{"kind":"memory","width_bytes":4,
          "geometry":{"displacement_region":{"displacement_rva":THIRD_GLOBAL}}},
        "linear_references":{
          "scope":"linear_text_decode_candidates_not_reachable_execution",
          "all_indirect_references_covered":False,
          "globals":[{"global_rva":THIRD_GLOBAL,"runtime_initialization_proven":False,"samples":[]}]
        },
        "actual_heapalloc_argument_position_proven":False,
        "actual_global_value_proven":False,"all_indirect_aliases_covered":False,
        "runtime_heap_size_or_flags_proven":False,
        "push_precedes_heapalloc_iat_site_syntactically":True
      },
      "heapalloc_prefix":{
        "heapalloc_call_rva":EAX_CALL,"prefix_instruction_sites":[],
        "prefix_push_sites":[],
        "all_real_entry_paths_proven":False,"stack_argument_roles_proven":False,
        "original_heapalloc_return_proven":False
      },
      "ebx_alias_gap":{
        "site_rva":ALIAS_SITE,"candidate_root_rva":EBX_TARGET,
        "model_original_gap_present":True,"operand_shapes":[{"kind":"memory"}],
        "candidate_graph_nodes":15,"candidate_graph_edges":18,
        "alias_effective_address_proven":False,"alias_object_owner_proven":False,
        "conditional_branch_outcomes_proven":False,"caller_effects_admitted":False,
        "function_entry_proven":False,"r8_return_summary_qualified":False
      },
      **{k:False for k in FLAGS}
    }

class TestR20Guard(unittest.TestCase):
    def test_static_specimen(self):self.assertTrue(validate(specimen()))
    def test_original_hash_guard(self):
        x=specimen();x["savedata_sha256"]="0"*64
        with self.assertRaises(ValueError):validate(x)
    def test_runtime_promotion(self):
        x=specimen();x["native_file_io_executed"]=True
        with self.assertRaises(ValueError):validate(x)
    def test_call_target_promotion(self):
        x=specimen();x["second_call"]["runtime_call_target_proven"]=True
        with self.assertRaises(ValueError):validate(x)
    def test_call_site_tamper(self):
        x=specimen();x["second_call"]["call_identity"]["call_rva"]+=1
        with self.assertRaises(ValueError):validate(x)
    def test_heap_argument_claim(self):
        x=specimen();x["third_global"]["actual_heapalloc_argument_position_proven"]=True
        with self.assertRaises(ValueError):validate(x)
    def test_global_source_wrong(self):
        x=specimen();x["third_global"]["source_operand"]["geometry"]["displacement_region"]["displacement_rva"]+=4
        with self.assertRaises(ValueError):validate(x)
    def test_linear_scan_promotion(self):
        x=specimen();x["third_global"]["linear_references"]["all_indirect_references_covered"]=True
        with self.assertRaises(ValueError):validate(x)
    def test_heap_return_promotion(self):
        x=specimen();x["heapalloc_prefix"]["original_heapalloc_return_proven"]=True
        with self.assertRaises(ValueError):validate(x)
    def test_alias_ownership_promotion(self):
        x=specimen();x["ebx_alias_gap"]["alias_object_owner_proven"]=True
        with self.assertRaises(ValueError):validate(x)
    def test_ebx_return_effect_promotion(self):
        x=specimen();x["ebx_alias_gap"]["r8_return_summary_qualified"]=True
        with self.assertRaises(ValueError):validate(x)
    def test_raw_original_bytes_banned(self):
        x=specimen();x["raw_bytes"]="forbidden"
        with self.assertRaises(ValueError):validate(x)
    def test_candidate_graph_cap(self):
        x=specimen();x["second_call"]["candidate_nodes"]=129
        with self.assertRaises(ValueError):validate(x)
if __name__=="__main__":unittest.main()
