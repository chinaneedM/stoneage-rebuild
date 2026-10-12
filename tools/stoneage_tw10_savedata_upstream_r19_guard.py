"""R19 strict original-derived metadata guard; independent from original probe.

Guard validates a bounded source identity and that static syntax has not been
silently turned into heap allocation, pointer ownership or native persistence.
"""
import argparse
import json
from pathlib import Path
from tools.stoneage_tw10_savedata_upstream_r19 import (
    SCHEMA, STATUS, FLAGS, RUNTIME_SHA256, SAVEDATA_SHA256,
    WRITES, SECOND_GLOBAL, EAX_CALL, EBX_CALL, EBX_TARGET, IMUL_CALLS,
)
FORBIDDEN={"raw_bytes","opcode_bytes","binary","original_executable",
           "original_payload","disassembly","asset_payload"}

def validate(data):
    if not isinstance(data,dict) or data.get("schema")!=SCHEMA or data.get("status")!=STATUS:
        raise ValueError("R19 schema and status")
    if (data.get("runtime_sha256")!=RUNTIME_SHA256 or
            data.get("savedata_sha256")!=SAVEDATA_SHA256):
        raise ValueError("R19 original hashes")
    if data.get("r18_original_identity_revalidated") is not True or data.get("conditional_static_only") is not True:
        raise ValueError("R19 chain of custody")
    if any(data.get(k) is not False for k in FLAGS):
        raise ValueError("R19 illegal historical or runtime promotion")
    writes=data.get("second_global_writes")
    if not isinstance(writes,list) or [w.get("site_rva") for w in writes]!=list(WRITES):
        raise ValueError("R19 second global sites")
    for w in writes:
        shape=w.get("write",{})
        if shape.get("expected_global_rva")!=SECOND_GLOBAL:
            raise ValueError("R19 write target")
        if shape.get("destination",{}).get("write_width_bytes")!=4:
            raise ValueError("R19 expected word width")
        for k in ("source_value_proven","actual_executed_write_proven",
                  "initialized_global_proven","same_object_owner_proven"):
            if w.get(k) is not False:raise ValueError("R19 false write promotion")
        local=w.get("local_source",{})
        if (local.get("anchor_is_verified_entry") is not False or
            local.get("value_known") is not False or
            local.get("all_incoming_paths_proven") is not False or
            local.get("call_fallthrough_structural_only") is not True):
            raise ValueError("R19 candidate graph wrongly qualified")
        if not isinstance(local.get("reaching_candidates"),list) or len(local["reaching_candidates"])>24:
            raise ValueError("R19 reaching-source cap")
    h=data.get("heapalloc",{})
    if (h.get("call_identity",{}).get("call_rva")!=EAX_CALL or
        h["call_identity"].get("import_identity")!=
        {"dll":"KERNEL32.dll","name":"HeapAlloc","iat_rva":0x520f8}):
        raise ValueError("R19 exact HeapAlloc IAT identity")
    for k in ("verified_entry_or_path","heapalloc_signature_applied_to_stack",
              "argument_count_and_slots_proven",
              "runtime_heap_handle_flags_size_proven","return_pointer_proven",
              "allocation_success_proven","return_to_second_global_owner_proven"):
        if h.get(k) is not False:raise ValueError("R19 HeapAlloc ABI or effect promoted")
    pushes=h.get("syntactic_pre_call_push_candidates")
    if not isinstance(pushes,list) or len(pushes)>20:
        raise ValueError("R19 push cap")
    for p in pushes:
        if p.get("candidate_only") is not True or p.get("can_be_assigned_to_heapalloc_argument_slot") is not False:
            raise ValueError("R19 candidate push promoted to argument")
    ebx=data.get("ebx_call",{})
    if ebx.get("call_identity",{}).get("call_rva")!=EBX_CALL or ebx["call_identity"].get("direct_target_rva")!=EBX_TARGET:
        raise ValueError("R19 EBX call identity")
    for k in ("original_source_ebx_after_call_known","entry_context_and_arguments_proven",
              "runtime_callee_return_proven","caller_resume_admitted"):
        if ebx.get(k) is not False:raise ValueError("R19 EBX effects promoted")
    summary=ebx.get("callee_summary",{})
    if (summary.get("root_rva")!=EBX_TARGET or
        summary.get("original_helper_accepted") is not False or
        summary.get("native_io_executed") is not False):
        raise ValueError("R19 EBX model summary promoted")
    imul=data.get("imul_caller_contexts")
    if not isinstance(imul,list) or [p.get("call_identity",{}).get("call_rva") for p in imul]!=list(IMUL_CALLS):
        raise ValueError("R19 IMUL callers changed")
    for row in imul:
        if row.get("callee_model_entry_esp_plus8_not_actual_argument") is not True:
            raise ValueError("R19 synthetic stack relation promoted")
        for k in ("verified_effective_entry_esp","caller_argument_ownership_proven",
                  "caller_path_feasible_proven","return_effects_admitted"):
            if row.get(k) is not False:
                raise ValueError("R19 caller frame ownership promoted")
    def reject_keys(item):
        if isinstance(item,dict):
            if set(item)&FORBIDDEN:raise ValueError("R19 forbidden payload bytes")
            for v in item.values():reject_keys(v)
        elif isinstance(item,list):
            for v in item:reject_keys(v)
    reject_keys(data)
    return True

def main():
    p=argparse.ArgumentParser();p.add_argument("--report",required=True,type=Path)
    a=p.parse_args()
    if a.report.stat().st_size>70000:raise ValueError("R19 oversized metadata")
    validate(json.loads(a.report.read_text()))
    print("TW10_R19_STRICT_STATIC_NO_PROMOTION=PASS")
    print("TW10_R19_HEAP_RUNTIME_SAVE_AND_OWNERSHIP=OPEN")
if __name__=="__main__":main()
