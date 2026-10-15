"""Adversarial R64 independent derived contract acceptance. Synthetic fixtures only."""
import copy
import unittest
from tools.stoneage_tw10_savedata_r64_independent_guard import validate,SCHEMA,R63_SHA,R28_BLOB

class Guard(unittest.TestCase):
    def fixture(self):
        # Runtime test data, not any original source: build minimal explicit shape.
        contexts=[]
        for call,post,branch,push in (
            (0x4c68c,0x4c692,0x4c694,0x4c67e),
            (0x4c6f1,0x4c6f7,0x4c6f9,0x4c6e8),
        ):
            stack=[{"push_rva":call-20+i*2,"conditional_pre_call_esp_offset":i*4,
                    "decoded_operand":{"kind":"register","register":"eax","width_bytes":4},
                    "original_pushed_value_known":False,
                    "original_stack_slot_or_parameter_binding_proven":False}
                   for i in range(5)]
            stack[3]["push_rva"]=push
            contexts.append({
              "native_call_rva":call,"postcall_test_rva":post,
              "test_operand_signatures":[{"kind":"register","register":"eax","width_bytes":4} for _ in range(2)],
              "test_decoder_read_registers":["eax"],
              "test_decoder_written_registers":["eflags"],
              "test_direct_successor_rva":branch,
              "immediate_successor_mnemonic":"je",
              "immediate_successor_is_conditional_jump":True,
              "immediate_branch_successors":[branch+2] if post==0x4c692 else [branch+2,branch+10],
              "both_branch_successors_inside_r63_window":post!=0x4c692,
              "postcall_test_has_explicit_eax_operand":True,
              "native_eax_from_opaque_unknown_call":True,
              "structural_flag_source_candidate":True,
              "actual_flags_or_branch_values_known":False,
              "physical_push_candidates":stack,
              "win32_x86_stdcall_bytes_written_pointer_position_candidate":{
                  "conditional_pre_call_esp_offset":12,"original_rva":push,
                  "operand":stack[3]["decoded_operand"],
                  "depends_on_unproven_stdcall_frame_and_callee_preservation":True,
                  "actual_pointer_or_written_bytes_proven":False},
              "api_bool_return_eax_is_separate_from_count_pointer_memory":True,
              "actual_native_api_count_success_or_disk_write_proven":False,
            })
        return {"schema":SCHEMA,
                "r63_original_derived_json_sha256":R63_SHA,
                "r28_git_blob":R28_BLOB,
                "native_candidate_root_rva":0x4c5b4,
                "call_fallthrough_and_frame_values_assumed_not_proven":True,
                "separates_bool_like_eax_from_lpnumberofbyteswritten_position":True,
                "postcall_contexts":contexts,
                **{k:False for k in (
                  "original_native_writefile_executed","actual_writefile_bool_return_known",
                  "actual_bytes_written_memory_pointer_validated",
                  "actual_bytes_written_memory_contents_known",
                  "actual_stack_frame_register_callee_preservation_proven",
                  "actual_branches_executed_or_conditions_resolved",
                  "actual_flush_close_or_disk_persistence_proven",
                  "original_savedata_payload_evaluated_or_published"
                )}}
    def reject(self,fn):
        d=self.fixture();fn(d)
        with self.assertRaises(ValueError):validate(d)
    def test_synthetic_positive_is_static_only(self):
        d=validate(self.fixture())
        self.assertTrue(d["unresolved_first_branch_target_outside_r63_window"])
        self.assertFalse(d["actual_native_write_or_persistence_proven"])
    def test_swapped_test_register(self):
        self.reject(lambda d:d["postcall_contexts"][0]["test_operand_signatures"][0].__setitem__("register","ebx"))
    def test_fake_bool(self):
        self.reject(lambda d:d.__setitem__("actual_writefile_bool_return_known",True))
    def test_fake_count(self):
        self.reject(lambda d:d.__setitem__("actual_bytes_written_memory_contents_known",True))
    def test_fake_stack(self):
        self.reject(lambda d:d["postcall_contexts"][0]["physical_push_candidates"][3].__setitem__("original_stack_slot_or_parameter_binding_proven",True))
    def test_branch_import_fake(self):
        self.reject(lambda d:d["postcall_contexts"][1].__setitem__("immediate_successor_mnemonic","jne"))
    def test_first_branch_target_forged(self):
        self.reject(lambda d:d["postcall_contexts"][0].__setitem__("both_branch_successors_inside_r63_window",True))
    def test_second_branch_target_dropped(self):
        self.reject(lambda d:d["postcall_contexts"][1]["immediate_branch_successors"].pop())
    def test_wrong_count_pointer_rva(self):
        self.reject(lambda d:d["postcall_contexts"][0]["win32_x86_stdcall_bytes_written_pointer_position_candidate"].__setitem__("original_rva",0))
    def test_fake_persistence(self):
        self.reject(lambda d:d.__setitem__("actual_flush_close_or_disk_persistence_proven",True))
    def test_wrong_r63_source(self):
        self.reject(lambda d:d.__setitem__("r63_original_derived_json_sha256","0"*64))

if __name__=="__main__":
    unittest.main()
