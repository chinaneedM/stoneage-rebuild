"""R20 independent anti-promotion guard for derived static original metadata.

This tests semantics and accepted evidence boundaries, NOT original authenticity:
immutable successful source run, ZIP digest and JSON equality are separate.
"""
import argparse,json
from pathlib import Path
from tools.stoneage_tw10_savedata_upstream_r20 import (
    SCHEMA,STATUS,FLAGS,RUNTIME_SHA256,SAVEDATA_SHA256,
    SECOND_CALL,THIRD_GLOBAL,PUSH_SITE,ALIAS_SITE,EBX_TARGET,EAX_CALL,
)
FORBIDDEN={"original_binary","opcode_bytes","raw_bytes","instruction_bytes",
           "disassembly","original_payload","asset_payload","executable_bytes"}

def validate(d):
    if not isinstance(d,dict) or d.get("schema")!=SCHEMA or d.get("status")!=STATUS:
        raise ValueError("R20 schema/status")
    if d.get("runtime_sha256")!=RUNTIME_SHA256 or d.get("savedata_sha256")!=SAVEDATA_SHA256:
        raise ValueError("R20 original hashes")
    if d.get("r19_original_identity_revalidated") is not True or d.get("static_only") is not True:
        raise ValueError("R20 original chain of custody")
    if any(d.get(x) is not False for x in FLAGS):
        raise ValueError("R20 false historical/native admission")
    call=d.get("second_call",{})
    ident=call.get("call_identity",{})
    if ident.get("call_rva")!=SECOND_CALL or ident.get("kind") not in (
        "direct","register_indirect","memory_indirect","other"):
        raise ValueError("R20 original second CALL")
    if call.get("fallthrough_structural_only") is not True:
        raise ValueError("R20 CALL fallthrough must be structural")
    for k in ("actual_entry_verified","all_incoming_edges_proven",
              "runtime_call_target_proven","callee_effect_summary_admitted",
              "return_value_in_eax_proven","executed_write_at_second_global_proven"):
        if call.get(k) is not False:raise ValueError("R20 CALL runtime promoted")
    if call.get("candidate_nodes",0)>128 or call.get("candidate_edges",0)>350:
        raise ValueError("R20 bounded graph exceeded")
    ts=call.get("target_register_sources")
    if not isinstance(ts,list) or len(ts)>3:
        raise ValueError("R20 register candidate cap")
    for row in ts:
        if row.get("local_sources",{}).get("anchor_is_verified_entry") is not False:
            raise ValueError("R20 source candidate promoted to actual entry")
    global_=d.get("third_global",{})
    if global_.get("target_virtual_rva")!=THIRD_GLOBAL or global_.get("push_rva")!=PUSH_SITE:
        raise ValueError("R20 third global identity")
    shape=global_.get("source_operand",{})
    geometry=shape.get("geometry",{})
    if (shape.get("kind")!="memory" or shape.get("width_bytes")!=4 or
        geometry.get("displacement_region",{}).get("displacement_rva")!=THIRD_GLOBAL):
        raise ValueError("R20 pinned push operand geometry")
    refs=global_.get("linear_references",{})
    rows=refs.get("globals")
    if (refs.get("scope")!="linear_text_decode_candidates_not_reachable_execution"
        or refs.get("all_indirect_references_covered") is not False
        or not isinstance(rows,list) or len(rows)!=1 or
        rows[0].get("global_rva")!=THIRD_GLOBAL
        or rows[0].get("runtime_initialization_proven") is not False):
        raise ValueError("R20 scan cannot prove runtime")
    if len(rows[0].get("samples",[]))>32:raise ValueError("R20 reference sample cap")
    for k in ("actual_heapalloc_argument_position_proven",
              "actual_global_value_proven","all_indirect_aliases_covered",
              "runtime_heap_size_or_flags_proven"):
        if global_.get(k) is not False:raise ValueError("R20 value/alias promoted")
    if global_.get("push_precedes_heapalloc_iat_site_syntactically") is not True:
        raise ValueError("R20 HeapAlloc ordering")
    prefix=d.get("heapalloc_prefix",{})
    if prefix.get("heapalloc_call_rva")!=EAX_CALL:
        raise ValueError("R20 HeapAlloc prefix identity")
    if not isinstance(prefix.get("prefix_instruction_sites"),list) or len(prefix["prefix_instruction_sites"])>16:
        raise ValueError("R20 prefix cap")
    if not isinstance(prefix.get("prefix_push_sites"),list) or len(prefix["prefix_push_sites"])>16:
        raise ValueError("R20 push prefix cap")
    for k in ("all_real_entry_paths_proven","stack_argument_roles_proven",
              "original_heapalloc_return_proven"):
        if prefix.get(k) is not False:raise ValueError("R20 HeapAlloc prefix promoted")
    alias=d.get("ebx_alias_gap",{})
    if alias.get("site_rva")!=ALIAS_SITE or alias.get("candidate_root_rva")!=EBX_TARGET:
        raise ValueError("R20 alias site identity")
    if alias.get("model_original_gap_present") is not True:
        raise ValueError("R20 R19 alias gap lost")
    if (not isinstance(alias.get("operand_shapes"),list) or
        not any(row.get("kind")=="memory" for row in alias["operand_shapes"])):
        raise ValueError("R20 alias memory operand missing")
    if alias.get("candidate_graph_nodes",0)>128 or alias.get("candidate_graph_edges",0)>350:
        raise ValueError("R20 EBX graph cap")
    for k in ("alias_effective_address_proven","alias_object_owner_proven",
              "conditional_branch_outcomes_proven","caller_effects_admitted",
              "function_entry_proven"):
        if alias.get(k) is not False:raise ValueError("R20 alias ownership promoted")
    if alias.get("r8_return_summary_qualified") is not False:
        raise ValueError("R20 R8 alias gap cannot qualify return")
    def ban(obj):
        if isinstance(obj,dict):
            if set(obj)&FORBIDDEN:raise ValueError("R20 forbidden original bytes")
            for value in obj.values():ban(value)
        elif isinstance(obj,list):
            for value in obj:ban(value)
    ban(d)
    return True

def main():
    p=argparse.ArgumentParser();p.add_argument("--report",type=Path,required=True)
    a=p.parse_args()
    if a.report.stat().st_size>70000:raise ValueError("R20 oversized report")
    validate(json.loads(a.report.read_text()))
    print("TW10_R20_STATIC_SCHEMA_NO_PROMOTION=PASS")
    print("TW10_R20_NATIVE_IO_AND_OBJECT_OWNERSHIP=OPEN")

if __name__=="__main__":main()
