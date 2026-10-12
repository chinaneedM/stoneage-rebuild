"""R21 derived-report semantic guard; run/artifact custody is a separate gate."""
import argparse
import json
from pathlib import Path
from tools.stoneage_tw10_savedata_upstream_r21 import (
    SCHEMA, STATUS, FLAGS, RUNTIME_SHA256, SAVEDATA_SHA256,
    WRITER_SITE, THIRD_GLOBAL, SECOND_CALL, HEAPREALLOC_IMPORT,
    ALIAS_SITE, EBX_TARGET,
)

FORBIDDEN = {"raw_bytes","opcode_bytes","instruction_bytes","disassembly",
             "original_binary","original_payload","asset_payload","executable_bytes"}

def validate(d):
    if not isinstance(d,dict) or d.get("schema")!=SCHEMA or d.get("status")!=STATUS:
        raise ValueError("R21 schema mismatch")
    if d.get("runtime_sha256")!=RUNTIME_SHA256 or d.get("savedata_sha256")!=SAVEDATA_SHA256:
        raise ValueError("R21 original hashes mismatch")
    if d.get("r20_original_identity_revalidated") is not True or d.get("static_only") is not True:
        raise ValueError("R21 evidence chain broken")
    if any(d.get(k) is not False for k in FLAGS):
        raise ValueError("R21 unsupported native/runtime promotion")
    w=d.get("third_writer",{})
    if w.get("site_rva")!=WRITER_SITE or w.get("target_rva")!=THIRD_GLOBAL:
        raise ValueError("R21 writer identity")
    shape=w.get("write",{})
    if (shape.get("site_rva")!=WRITER_SITE or shape.get("expected_global_rva")!=THIRD_GLOBAL
        or shape.get("register_inputs_resolved") is not False
        or shape.get("executed_write_proven") is not False
        or shape.get("effective_object_proven") is not False
        or shape.get("named_caller_effect_admitted") is not False):
        raise ValueError("R21 writer effect prematurely admitted")
    source=w.get("local_source",{})
    if (source.get("anchor_is_verified_entry") is not False
        or source.get("all_incoming_paths_proven") is not False
        or source.get("value_known") is not False
        or source.get("call_fallthrough_structural_only") is not True
        or source.get("nodes",0)>128
        or len(source.get("reaching_candidates",[]))>24):
        raise ValueError("R21 writer candidate promoted")
    if not isinstance(w.get("anchors_examined"),list) or len(w["anchors_examined"])>4:
        raise ValueError("R21 writer anchor cap")
    for key in ("writer_reachable_from_real_entry_proven","source_register_value_proven",
                "direct_store_executed_proven","all_indirect_aliases_covered"):
        if w.get(key) is not False:raise ValueError("R21 executed writer promoted")
    h=d.get("heaprealloc_inputs",{})
    call=h.get("call_identity",{})
    if (call.get("call_rva")!=SECOND_CALL or
        call.get("import_identity")!=HEAPREALLOC_IMPORT or
        call.get("kind")!="memory_indirect"):
        raise ValueError("R21 imported call identity")
    if (h.get("call_is_opaque_register_barrier") is not True or
        h.get("post_call_eax_value_unknown") is not True or
        h.get("candidate_nodes",0)>128 or h.get("candidate_edges",0)>350):
        raise ValueError("R21 CALL barrier/cap")
    pushes=h.get("pre_call_push_candidates",[])
    if not isinstance(pushes,list) or len(pushes)>32:
        raise ValueError("R21 pre-CALL PUSH cap")
    if any(p.get("conditional_candidate_only") is not True or
           p.get("heaprealloc_abi_position_proven") is not False for p in pushes):
        raise ValueError("R21 PUSH argument promoted")
    regs=h.get("register_candidates_before_call",[])
    if not isinstance(regs,list) or [r.get("register") for r in regs]!=["eax","ecx","edx"]:
        raise ValueError("R21 pre-CALL register query identity")
    if any(r.get("candidate_source",{}).get("value_known") is not False for r in regs):
        raise ValueError("R21 pre-CALL register value claimed")
    for k in ("stack_argument_slots_admitted","heap_handle_flags_size_proven",
              "success_or_return_pointer_proven","same_pointer_as_global_store_proven",
              "real_entry_and_paths_proven"):
        if h.get(k) is not False:raise ValueError("R21 CALL effects admitted")
    a=d.get("eax_alias",{})
    if a.get("site_rva")!=ALIAS_SITE or a.get("candidate_root_rva")!=EBX_TARGET:
        raise ValueError("R21 alias identity")
    dst,src=a.get("destination",{}),a.get("source",{})
    geom=dst.get("geometry",{})
    if (dst.get("kind")!="memory" or dst.get("width_bytes")!=4
        or geom.get("base_register")!="eax" or geom.get("relative_field_offset")!=8
        or src.get("kind")!="register" or src.get("register")!="eax"
        or a.get("same_syntactic_register_for_address_and_value") is not True):
        raise ValueError("R21 exact alias geometry")
    if a.get("eax_local_source",{}).get("value_known") is not False:
        raise ValueError("R21 EAX alias value")
    for k in ("real_object_base_or_alias_proven","effective_write_proven",
              "callee_return_or_caller_effect_admitted","cycle_or_branch_feasibility_proven"):
        if a.get(k) is not False:raise ValueError("R21 alias caller effects admitted")
    def ban(obj):
        if isinstance(obj,dict):
            if set(obj)&FORBIDDEN:raise ValueError("R21 proprietary content leaked")
            for v in obj.values():ban(v)
        elif isinstance(obj,list):
            for v in obj:ban(v)
    ban(d)
    return True

def main():
    p=argparse.ArgumentParser();p.add_argument("--report",type=Path,required=True)
    path=p.parse_args().report
    if path.stat().st_size>70000:raise ValueError("R21 report too large")
    validate(json.loads(path.read_text()))
    print("TW10_R21_STATIC_NO_PROMOTION=PASS")
    print("TW10_R21_NATIVE_SAVE=OPEN")
if __name__=="__main__":main()
