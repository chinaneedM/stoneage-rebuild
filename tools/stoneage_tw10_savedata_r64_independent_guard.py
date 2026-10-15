"""R64 independent acceptance guard for original-derived postcall TEST and push data.

The artifact itself is independent of original-source execution: the workflow
validates pinned source Action and artifact ZIP digests separately.
"""
import argparse
import json
from pathlib import Path

SCHEMA="tw10-r64-postwritefile-test-flags-physical-count-pointer-audit"
R63_SHA="91b650db700cf892a7d8c8b2d36a9d49dbeca139be315856d31d59533056c1bd"
R28_BLOB="3671661219120d45bd922e05b6df371523b42432"
PAIRS=((0x4C68C,0x4C692,0x4C694,0x4C67E),
       (0x4C6F1,0x4C6F7,0x4C6F9,0x4C6E8))
FALSE_FLAGS=(
  "original_native_writefile_executed","actual_writefile_bool_return_known",
  "actual_bytes_written_memory_pointer_validated","actual_bytes_written_memory_contents_known",
  "actual_stack_frame_register_callee_preservation_proven",
  "actual_branches_executed_or_conditions_resolved",
  "actual_flush_close_or_disk_persistence_proven",
  "original_savedata_payload_evaluated_or_published"
)

def need(ok,msg):
    if not ok:raise ValueError("R64 independent acceptance guard: "+msg)
def validate(d):
    need(d.get("schema")==SCHEMA and d.get("r63_original_derived_json_sha256")==R63_SHA
         and d.get("r28_git_blob")==R28_BLOB and
         d.get("native_candidate_root_rva")==0x4C5B4,"exact schema and sources")
    need(d.get("call_fallthrough_and_frame_values_assumed_not_proven") is True
         and d.get("separates_bool_like_eax_from_lpnumberofbyteswritten_position") is True,
         "return/stack boundary")
    for f in FALSE_FLAGS:
        need(d.get(f) is False,"must stay OPEN: "+f)
    cs=d.get("postcall_contexts")
    need(isinstance(cs,list) and len(cs)==2,"two exact native call contexts")
    for c,(call,post,branch,pointer_push) in zip(cs,PAIRS):
        need(c.get("native_call_rva")==call and c.get("postcall_test_rva")==post,
             "exact call/test address")
        sig=c.get("test_operand_signatures")
        need(isinstance(sig,list) and len(sig)==2 and
             all(x.get("kind")=="register" and x.get("register")=="eax"
                 and x.get("width_bytes")==4 for x in sig),
             "two TEST EAX operands")
        need("eax" in c.get("test_decoder_read_registers",[]) and
             "eflags" in c.get("test_decoder_written_registers",[]) and
             c.get("postcall_test_has_explicit_eax_operand") is True,
             "EAX/EFLAGS source")
        need(c.get("test_direct_successor_rva")==branch and
             c.get("immediate_successor_mnemonic")=="je" and
             c.get("immediate_successor_is_conditional_jump") is True,
             "immediately adjacent conditional jump")
        successor=c.get("immediate_branch_successors",[])
        need(isinstance(successor,list) and
             successor==sorted(set(successor)) and
             1<=len(successor)<=2,
             "scoped local branch successors")
        need(c.get("both_branch_successors_inside_r63_window") is (len(successor)==2),
             "local-window branch coverage status, not full CFG")
        need(c.get("native_eax_from_opaque_unknown_call") is True and
             c.get("structural_flag_source_candidate") is True and
             c.get("actual_flags_or_branch_values_known") is False and
             c.get("actual_native_api_count_success_or_disk_write_proven") is False,
             "no imported return value / flag resolution")
        stack=c.get("physical_push_candidates")
        need(isinstance(stack,list) and len(stack)==5 and
             [x.get("conditional_pre_call_esp_offset") for x in stack]==[0,4,8,12,16] and
             len({x.get("push_rva") for x in stack})==5,
             "five qualified physical PUSH offsets")
        for s in stack:
            need(s.get("original_pushed_value_known") is False and
                 s.get("original_stack_slot_or_parameter_binding_proven") is False and
                 isinstance(s.get("decoded_operand"),dict),
                 "no historic stack/argument proof")
        p=c.get("win32_x86_stdcall_bytes_written_pointer_position_candidate")
        need(p.get("conditional_pre_call_esp_offset")==12 and
             p.get("original_rva")==pointer_push and
             p.get("operand")==stack[3]["decoded_operand"] and
             p.get("depends_on_unproven_stdcall_frame_and_callee_preservation") is True and
             p.get("actual_pointer_or_written_bytes_proven") is False,
             "bounded physical WriteFile argument-position proposal")
        need(c.get("api_bool_return_eax_is_separate_from_count_pointer_memory") is True,
             "separate BOOL-shaped result from output pointer")
    # One direct branch target is outside the original R63 local window:
    # do not backfill it from assumptions or infer an impossible alternative.
    need(cs[0]["both_branch_successors_inside_r63_window"] is False and
         cs[1]["both_branch_successors_inside_r63_window"] is True,
         "historical local control-window divergence")
    return {"schema":SCHEMA,"guard":"INDEPENDENT_STATIC_ONLY",
            "accepted_original_instruction_shapes_provisional":True,
            "actual_native_write_or_persistence_proven":False,
            "unresolved_first_branch_target_outside_r63_window":True,
            "postcall_sites":[c["postcall_test_rva"] for c in cs]}
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--report",type=Path,required=True)
    a=p.parse_args()
    print(json.dumps(validate(json.loads(a.report.read_text())),sort_keys=True))
if __name__=="__main__":
    main()
