"""R21 independent guard tamper controls using invented metadata, not original."""
import copy
import unittest
from tools.stoneage_tw10_savedata_upstream_r21 import (
    SCHEMA,STATUS,FLAGS,RUNTIME_SHA256,SAVEDATA_SHA256,
    WRITER_SITE,THIRD_GLOBAL,SECOND_CALL,HEAPREALLOC_IMPORT,ALIAS_SITE,EBX_TARGET,
)
from tools.stoneage_tw10_savedata_upstream_r21_guard import validate

def specimen():
    src={"anchor_is_verified_entry":False,"all_incoming_paths_proven":False,
         "call_fallthrough_structural_only":True,"value_known":False,
         "nodes":1,"reaching_candidates":[]}
    return {
        "schema":SCHEMA,"status":STATUS,
        "runtime_sha256":RUNTIME_SHA256,"savedata_sha256":SAVEDATA_SHA256,
        "r20_original_identity_revalidated":True,"static_only":True,
        "third_writer":{
            "site_rva":WRITER_SITE,"target_rva":THIRD_GLOBAL,
            "write":{
                "site_rva":WRITER_SITE,"expected_global_rva":THIRD_GLOBAL,
                "register_inputs_resolved":False,"executed_write_proven":False,
                "effective_object_proven":False,"named_caller_effect_admitted":False,
            },
            "local_source":src,"anchors_examined":[],
            "writer_reachable_from_real_entry_proven":False,
            "source_register_value_proven":False,
            "direct_store_executed_proven":False,
            "all_indirect_aliases_covered":False,
        },
        "heaprealloc_inputs":{
            "call_identity":{"call_rva":SECOND_CALL,"kind":"memory_indirect",
                             "import_identity":dict(HEAPREALLOC_IMPORT)},
            "call_is_opaque_register_barrier":True,
            "post_call_eax_value_unknown":True,
            "candidate_nodes":1,"candidate_edges":0,"pre_call_push_candidates":[],
            "register_candidates_before_call":[{"register":r,"candidate_source":{"value_known":False}}
                                                for r in ("eax","ecx","edx")],
            "stack_argument_slots_admitted":False,
            "heap_handle_flags_size_proven":False,
            "success_or_return_pointer_proven":False,
            "same_pointer_as_global_store_proven":False,
            "real_entry_and_paths_proven":False,
        },
        "eax_alias":{
            "site_rva":ALIAS_SITE,"candidate_root_rva":EBX_TARGET,
            "destination":{"kind":"memory","width_bytes":4,
                           "geometry":{"base_register":"eax","relative_field_offset":8}},
            "source":{"kind":"register","register":"eax"},
            "same_syntactic_register_for_address_and_value":True,
            "eax_local_source":{"value_known":False},
            "real_object_base_or_alias_proven":False,
            "effective_write_proven":False,
            "callee_return_or_caller_effect_admitted":False,
            "cycle_or_branch_feasibility_proven":False,
        },
        **{k:False for k in FLAGS},
    }

class R21GuardTests(unittest.TestCase):
    def test_synthetic_specimen_valid(self): self.assertTrue(validate(specimen()))
    def check_bad(self,mutate):
        d=specimen();mutate(d)
        with self.assertRaises(ValueError):validate(d)
    def test_wrong_original_hash(self):
        self.check_bad(lambda d:d.update(runtime_sha256="0"*64))
    def test_wrong_call_site(self):
        self.check_bad(lambda d:d["heaprealloc_inputs"]["call_identity"].update(call_rva=1))
    def test_wrong_import(self):
        self.check_bad(lambda d:d["heaprealloc_inputs"]["call_identity"]["import_identity"].update(name="CreateFileA"))
    def test_pre_call_becomes_argument(self):
        self.check_bad(lambda d:d["heaprealloc_inputs"].update(stack_argument_slots_admitted=True))
    def test_heap_result_known(self):
        self.check_bad(lambda d:d["heaprealloc_inputs"].update(post_call_eax_value_unknown=False))
    def test_writer_runtime_value(self):
        self.check_bad(lambda d:d["third_writer"].update(source_register_value_proven=True))
    def test_writer_entry_promoted(self):
        self.check_bad(lambda d:d["third_writer"]["local_source"].update(anchor_is_verified_entry=True))
    def test_writer_wrong_global(self):
        self.check_bad(lambda d:d["third_writer"].update(target_rva=THIRD_GLOBAL+4))
    def test_alias_wrong_offset(self):
        self.check_bad(lambda d:d["eax_alias"]["destination"]["geometry"].update(relative_field_offset=4))
    def test_alias_owned(self):
        self.check_bad(lambda d:d["eax_alias"].update(real_object_base_or_alias_proven=True))
    def test_caller_resumption(self):
        self.check_bad(lambda d:d.update(caller_resumption_admitted=True))
    def test_proprietary_bytes_rejected(self):
        self.check_bad(lambda d:d.update(raw_bytes="not acceptable"))
    def test_push_abi_inference(self):
        def mutation(d):
            d["heaprealloc_inputs"]["pre_call_push_candidates"]=[
                {"conditional_candidate_only":True,"heaprealloc_abi_position_proven":True}]
        self.check_bad(mutation)
    def test_wrong_register_query(self):
        self.check_bad(lambda d:d["heaprealloc_inputs"].update(register_candidates_before_call=[]))

if __name__=="__main__":unittest.main()
