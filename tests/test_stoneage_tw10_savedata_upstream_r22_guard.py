"""Independent R22 tamper controls: invented report skeleton only."""
import unittest
from tools.stoneage_tw10_savedata_upstream_r22 import (
    SCHEMA,STATUS,FLAGS,RUNTIME_SHA256,SAVEDATA_SHA256,
    WRITER_CALL,WRITER_SITE,WRITER_ROOT,SECOND_CALL,SECOND_ANCHOR,ALIAS_SITE,EBX_TARGET,
)
from tools.stoneage_tw10_savedata_upstream_r22_guard import validate
def source():
    return {"anchor_is_verified_entry":False,"all_incoming_paths_proven":False,
            "call_fallthrough_structural_only":True,"value_known":False,
            "nodes":1,"reaching_candidates":[]}
def specimen():
    return {
        "schema":SCHEMA,"status":STATUS,
        "runtime_sha256":RUNTIME_SHA256,"savedata_sha256":SAVEDATA_SHA256,
        "r21_original_identity_revalidated":True,"static_only":True,
        "writer_opaque_call":{
            "site_rva":WRITER_CALL,"writer_rva":WRITER_SITE,"anchor_rva":WRITER_ROOT,
            "call_identity":{"call_rva":WRITER_CALL,"kind":"direct"},
            "candidate_nodes":4,"candidate_edges":3,
            "call_fallthrough_assumes_return_structurally":True,
            "call_to_writer_structural_path_exists":True,
            "actual_callee_return_or_register_effect_known":False,
            "writer_value_after_call_known":False,
            "function_entry_or_path_executed_proven":False,
            "pre_call_register_sources":{r:source() for r in ("eax","ecx","edx")},
        },
        "heaprealloc_push_flow":{
            "call_rva":SECOND_CALL,"anchor_rva":SECOND_ANCHOR,
            "nodes":5,"edges":4,
            "graph_reachability_is_not_stack_argument_proof":True,
            "callee_return_eax_effect_unknown":True,
            "heaprealloc_stack_signature_applied":False,
            "all_incoming_edges_or_real_paths_proven":False,
            "push_flow_candidates":[{"site_rva":SECOND_ANCHOR,
                "kind":"register","register":"eax","syntactic_cfg_path_to_call":True,
                "register_source":source(),
                "original_stack_position_or_abi_role_proven":False,
                "runtime_operand_value_proven":False}],
        },
        "eax_cycle":{
            "site_rva":ALIAS_SITE,"root_rva":EBX_TARGET,
            "node_count":5,"edge_count":5,
            "backward_edges":[{"from_rva":ALIAS_SITE+10,"to_rva":ALIAS_SITE}],
            "later_rva_eax_source_candidates":[],
            "eax_reaching_source":source(),
            "reverse_rva_source_does_not_prove_linear_order":True,
            "backward_edges_not_executed_paths":True,
            "r8_alias_write_unsummarized":True,
            "original_object_owner_known":False,
            "runtime_cycle_taken_known":False,
            "return_to_caller_admitted":False,
        },
        **{k:False for k in FLAGS},
    }
class R22Guard(unittest.TestCase):
    def bad(self,fn):
        d=specimen();fn(d)
        with self.assertRaises(ValueError):validate(d)
    def test_valid(self):self.assertTrue(validate(specimen()))
    def test_hash(self):self.bad(lambda d:d.update(runtime_sha256="0"*64))
    def test_import_call_site(self):self.bad(lambda d:d["writer_opaque_call"].update(site_rva=0))
    def test_call_return_admission(self):self.bad(lambda d:d["writer_opaque_call"].update(actual_callee_return_or_register_effect_known=True))
    def test_call_graph_fake(self):self.bad(lambda d:d["writer_opaque_call"].update(call_to_writer_structural_path_exists=False))
    def test_call_entry_fake(self):self.bad(lambda d:d["writer_opaque_call"]["pre_call_register_sources"]["eax"].update(anchor_is_verified_entry=True))
    def test_realloc_call_site(self):self.bad(lambda d:d["heaprealloc_push_flow"].update(call_rva=0))
    def test_realloc_abi(self):self.bad(lambda d:d["heaprealloc_push_flow"].update(heaprealloc_stack_signature_applied=True))
    def test_realloc_return(self):self.bad(lambda d:d["heaprealloc_push_flow"].update(callee_return_eax_effect_unknown=False))
    def test_push_role(self):self.bad(lambda d:d["heaprealloc_push_flow"]["push_flow_candidates"][0].update(original_stack_position_or_abi_role_proven=True))
    def test_push_value(self):self.bad(lambda d:d["heaprealloc_push_flow"]["push_flow_candidates"][0].update(runtime_operand_value_proven=True))
    def test_alias_site(self):self.bad(lambda d:d["eax_cycle"].update(site_rva=0))
    def test_alias_backward_edge_inverted(self):self.bad(lambda d:d["eax_cycle"]["backward_edges"][0].update(to_rva=ALIAS_SITE+20))
    def test_alias_ownership(self):self.bad(lambda d:d["eax_cycle"].update(original_object_owner_known=True))
    def test_alias_return(self):self.bad(lambda d:d["eax_cycle"].update(return_to_caller_admitted=True))
    def test_native_save_admission(self):self.bad(lambda d:d.update(native_file_io_executed=True))
    def test_proprietary_bytes(self):self.bad(lambda d:d.update(raw_bytes="forbidden"))
if __name__=="__main__":unittest.main()
