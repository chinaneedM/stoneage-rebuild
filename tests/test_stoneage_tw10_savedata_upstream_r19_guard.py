"""R19 independent synthetic guards. These are not original evidence."""
import unittest
from tools.stoneage_tw10_savedata_upstream_r19 import (
    SCHEMA,STATUS,FLAGS,RUNTIME_SHA256,SAVEDATA_SHA256,
    WRITES,SECOND_GLOBAL,EAX_CALL,EBX_CALL,EBX_TARGET,IMUL_CALLS
)
from tools.stoneage_tw10_savedata_upstream_r19_guard import validate

def base():
    return {
        "schema":SCHEMA,"status":STATUS,
        "runtime_sha256":RUNTIME_SHA256,"savedata_sha256":SAVEDATA_SHA256,
        "r18_original_identity_revalidated":True,"conditional_static_only":True,
        "second_global_writes":[{
            "site_rva":site,
            "write":{"expected_global_rva":SECOND_GLOBAL,
                     "destination":{"write_width_bytes":4}},
            "source_value_proven":False,"actual_executed_write_proven":False,
            "initialized_global_proven":False,"same_object_owner_proven":False,
            "local_source":{"anchor_is_verified_entry":False,"value_known":False,
                            "all_incoming_paths_proven":False,
                            "call_fallthrough_structural_only":True,
                            "reaching_candidates":[]},
        } for site in WRITES],
        "heapalloc":{
            "call_identity":{"call_rva":EAX_CALL,
                             "import_identity":{"dll":"KERNEL32.dll","name":"HeapAlloc","iat_rva":0x520f8}},
            "verified_entry_or_path":False,
            "heapalloc_signature_applied_to_stack":False,
            "argument_count_and_slots_proven":False,
            "runtime_heap_handle_flags_size_proven":False,
            "return_pointer_proven":False,"allocation_success_proven":False,
            "return_to_second_global_owner_proven":False,
            "syntactic_pre_call_push_candidates":[{"candidate_only":True,"can_be_assigned_to_heapalloc_argument_slot":False}],
        },
        "ebx_call":{
            "call_identity":{"call_rva":EBX_CALL,"direct_target_rva":EBX_TARGET},
            "callee_summary":{"root_rva":EBX_TARGET,"original_helper_accepted":False,"native_io_executed":False},
            "original_source_ebx_after_call_known":False,
            "entry_context_and_arguments_proven":False,
            "runtime_callee_return_proven":False,"caller_resume_admitted":False,
        },
        "imul_caller_contexts":[{
            "call_identity":{"call_rva":site},
            "callee_model_entry_esp_plus8_not_actual_argument":True,
            "verified_effective_entry_esp":False,
            "caller_argument_ownership_proven":False,
            "caller_path_feasible_proven":False,"return_effects_admitted":False,
        } for site in IMUL_CALLS],
        **{f:False for f in FLAGS}
    }

class TestR19Guard(unittest.TestCase):
    def test_valid(self):self.assertTrue(validate(base()))
    def test_runtime_promotion(self):
        x=base();x["native_io_executed"]=True
        with self.assertRaises(ValueError):validate(x)
    def test_original_identification(self):
        x=base();x["r18_original_identity_revalidated"]=False
        with self.assertRaises(ValueError):validate(x)
    def test_store_width(self):
        x=base();x["second_global_writes"][0]["write"]["destination"]["write_width_bytes"]=1
        with self.assertRaises(ValueError):validate(x)
    def test_store_value_claim(self):
        x=base();x["second_global_writes"][0]["source_value_proven"]=True
        with self.assertRaises(ValueError):validate(x)
    def test_heap_slot_claim(self):
        x=base();x["heapalloc"]["argument_count_and_slots_proven"]=True
        with self.assertRaises(ValueError):validate(x)
    def test_heap_runtime_allocation(self):
        x=base();x["heapalloc"]["allocation_success_proven"]=True
        with self.assertRaises(ValueError):validate(x)
    def test_heap_import_tamper(self):
        x=base();x["heapalloc"]["call_identity"]["import_identity"]["name"]="ReadFile"
        with self.assertRaises(ValueError):validate(x)
    def test_indirect_callee_effect_claim(self):
        x=base();x["ebx_call"]["caller_resume_admitted"]=True
        with self.assertRaises(ValueError):validate(x)
    def test_unproven_stack_ownership(self):
        x=base();x["imul_caller_contexts"][0]["caller_argument_ownership_proven"]=True
        with self.assertRaises(ValueError):validate(x)
    def test_push_assigned_abi(self):
        x=base();x["heapalloc"]["syntactic_pre_call_push_candidates"][0]["can_be_assigned_to_heapalloc_argument_slot"]=True
        with self.assertRaises(ValueError):validate(x)
    def test_original_payload(self):
        x=base();x["original_payload"]="x"
        with self.assertRaises(ValueError):validate(x)
if __name__=="__main__":unittest.main()
