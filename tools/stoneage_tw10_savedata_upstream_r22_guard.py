"""R22 semantic no-promotion guard; custody and original artifact equality separate."""
import argparse
import json
from pathlib import Path
from tools.stoneage_tw10_savedata_upstream_r22 import (
    SCHEMA,STATUS,FLAGS,RUNTIME_SHA256,SAVEDATA_SHA256,
    WRITER_CALL,WRITER_SITE,WRITER_ROOT,SECOND_CALL,SECOND_ANCHOR,
    ALIAS_SITE,EBX_TARGET,
)
FORBIDDEN={"raw_bytes","opcode_bytes","instruction_bytes","disassembly",
           "original_binary","original_payload","asset_payload","executable_bytes"}

def source_guard(s):
    if (not isinstance(s,dict) or s.get("anchor_is_verified_entry") is not False
        or s.get("all_incoming_paths_proven") is not False
        or s.get("call_fallthrough_structural_only") is not True
        or s.get("value_known") is not False or s.get("nodes",0)>128
        or len(s.get("reaching_candidates",[]))>24):
        raise ValueError("R22 source/entry promotion")

def validate(d):
    if not isinstance(d,dict) or d.get("schema")!=SCHEMA or d.get("status")!=STATUS:
        raise ValueError("R22 schema/status")
    if d.get("runtime_sha256")!=RUNTIME_SHA256 or d.get("savedata_sha256")!=SAVEDATA_SHA256:
        raise ValueError("R22 hash identity")
    if d.get("r21_original_identity_revalidated") is not True or d.get("static_only") is not True:
        raise ValueError("R22 R21 identity chain")
    if any(d.get(key) is not False for key in FLAGS):
        raise ValueError("R22 forbidden native/runtime promotion")
    c=d.get("writer_opaque_call",{})
    if (c.get("site_rva")!=WRITER_CALL or c.get("writer_rva")!=WRITER_SITE
        or c.get("anchor_rva")!=WRITER_ROOT
        or c.get("call_identity",{}).get("call_rva")!=WRITER_CALL
        or c.get("call_identity",{}).get("kind") not in
           ("direct","memory_indirect","register_indirect","other")):
        raise ValueError("R22 writer CALL identity")
    if (c.get("candidate_nodes",0)>128 or c.get("candidate_edges",0)>350
        or c.get("call_fallthrough_assumes_return_structurally") is not True
        or c.get("call_to_writer_structural_path_exists") is not True):
        raise ValueError("R22 writer CALL graph")
    for key in ("actual_callee_return_or_register_effect_known",
                "writer_value_after_call_known","function_entry_or_path_executed_proven"):
        if c.get(key) is not False: raise ValueError("R22 CALL effect promoted")
    regs=c.get("pre_call_register_sources",{})
    if not isinstance(regs,dict) or set(regs)!={"eax","ecx","edx"}:
        raise ValueError("R22 CALL input registers")
    for val in regs.values():source_guard(val)
    h=d.get("heaprealloc_push_flow",{})
    if (h.get("call_rva")!=SECOND_CALL or h.get("anchor_rva")!=SECOND_ANCHOR
        or h.get("nodes",0)>128 or h.get("edges",0)>350):
        raise ValueError("R22 realloc graph")
    if (h.get("graph_reachability_is_not_stack_argument_proof") is not True
        or h.get("callee_return_eax_effect_unknown") is not True
        or h.get("heaprealloc_stack_signature_applied") is not False
        or h.get("all_incoming_edges_or_real_paths_proven") is not False):
        raise ValueError("R22 HeapReAlloc ABI/return promoted")
    pushes=h.get("push_flow_candidates")
    if not isinstance(pushes,list) or len(pushes)>32:
        raise ValueError("R22 PUSH bound")
    for p in pushes:
        if (p.get("original_stack_position_or_abi_role_proven") is not False
            or p.get("runtime_operand_value_proven") is not False
            or p.get("kind") not in ("register","memory","other")
            or not isinstance(p.get("syntactic_cfg_path_to_call"),bool)):
            raise ValueError("R22 push value/role promotion")
        if p.get("register_source") is not None:source_guard(p["register_source"])
    a=d.get("eax_cycle",{})
    if (a.get("site_rva")!=ALIAS_SITE or a.get("root_rva")!=EBX_TARGET
        or a.get("node_count",0)>128 or a.get("edge_count",0)>350
        or not isinstance(a.get("backward_edges"),list)
        or len(a["backward_edges"])>32 or
        not isinstance(a.get("later_rva_eax_source_candidates"),list)
        or len(a["later_rva_eax_source_candidates"])>24):
        raise ValueError("R22 EAX cycle shape/cap")
    source_guard(a.get("eax_reaching_source",{}))
    if (a.get("reverse_rva_source_does_not_prove_linear_order") is not True
        or a.get("backward_edges_not_executed_paths") is not True
        or a.get("r8_alias_write_unsummarized") is not True):
        raise ValueError("R22 alias-cycle graph promotion")
    for key in ("original_object_owner_known","runtime_cycle_taken_known",
                "return_to_caller_admitted"):
        if a.get(key) is not False:raise ValueError("R22 alias return promoted")
    for edge in a["backward_edges"]:
        if edge.get("to_rva",0)>edge.get("from_rva",0):
            raise ValueError("R22 reverse-edge inconsistency")
    def ban(obj):
        if isinstance(obj,dict):
            if set(obj)&FORBIDDEN:raise ValueError("R22 forbidden proprietary data")
            for v in obj.values():ban(v)
        elif isinstance(obj,list):
            for v in obj:ban(v)
    ban(d)
    return True

def main():
    p=argparse.ArgumentParser();p.add_argument("--report",type=Path,required=True)
    path=p.parse_args().report
    if path.stat().st_size>70000:raise ValueError("R22 oversize")
    validate(json.loads(path.read_text()))
    print("TW10_R22_STRICT_STATIC_SCHEMA=PASS")
    print("TW10_R22_NATIVE_IO=OPEN")
if __name__=="__main__":main()
