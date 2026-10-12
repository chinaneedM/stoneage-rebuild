"""TW1.0 R20 pinned original CALL, third-global and EBX alias source frontiers.

Nonexecuting static inspection ONLY. Never exports disassembly or original bytes.
References, branch graphs and stack prefixes are conditional candidates; no
effective values, runtime allocation, calling convention or native save proven.
"""
import argparse
import json
import tempfile
from pathlib import Path
from capstone import CS_GRP_CALL, CS_GRP_JUMP, CS_GRP_RET
from capstone.x86 import X86_OP_MEM, X86_OP_REG
from tools.stoneage_tw10_savedata_upstream_r19 import (
    inspect_verified as inspect_r19, RUNTIME_SHA256, SAVEDATA_SHA256,
    WRITES, EAX_CALL, EBX_TARGET,
)
from tools.stoneage_tw10_savedata_upstream_r18 import SECOND_GLOBAL
from tools.stoneage_tw10_savedata_frontier_r12 import (
    call_identity, linear_references,
)
from tools.stoneage_tw10_savedata_write_shapes_r17 import operand_shape, candidate_sources
from tools.stoneage_tw10_savedata_reachdefs_r14 import bounded_graph
from tools.stoneage_tw10_savedata_helper_effects_r8 import summarize
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH, SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows, extract_row

SCHEMA="tw10-r20-original-indirect-call-third-global-alias-frontier"
STATUS="PINNED_ORIGINAL_CONDITIONAL_STATIC_GAPS_RETAINED"
SECOND_CALL=0x4a0c4
SECOND_ANCHOR=0x4a0a0
THIRD_GLOBAL=0x172187c
PUSH_SITE=0x49a06
ALIAS_SITE=0x4a17d
HEAP_ANCHOR=0x49a00
FLAGS=(
    "original_function_entries_proven", "actual_path_feasibility_proven",
    "second_callee_runtime_target_proven", "call_effect_summary_admitted",
    "third_global_actual_value_proven", "third_global_initialization_proven",
    "heapalloc_abi_arguments_proven", "heapalloc_runtime_allocation_proven",
    "allocation_pointer_ownership_proven", "alias_effective_address_proven",
    "alias_memory_effect_proven", "ebx_caller_resumption_admitted",
    "native_file_io_executed", "original_save_format_proven",
    "filename_handle_buffer_128_link_proven", "original_payload_published",
)

def indirect_call_frontier(dec, sections, imports, site=SECOND_CALL,
                           root=SECOND_ANCHOR):
    call=call_identity(dec,site,imports,sections)
    nodes,edges,front,cap=bounded_graph(dec,root,max_span=192,max_nodes=128)
    if site not in nodes:raise ValueError("R19 second global CALL site not reached")
    regs=[]
    if call["kind"]=="register_indirect" and call["register_target"]:
        regs.append(call["register_target"])
    if call["kind"]=="memory_indirect" and call["memory_target"]:
        for k in ("base_register","index_register"):
            v=call["memory_target"][k]
            if v:regs.append(v)
    # The reaching-register definitions are locally conditional, not ABI.
    tracked=[]
    for reg in sorted(set(regs)):
        if reg in ("eax","ebx","ecx","edx","esi","edi","ebp"):
            tracked.append({"register":reg,
                "local_sources":candidate_sources(dec,site,reg,sections,root)})
    return {
        "call_identity":call,
        "anchor_rva":root,"candidate_nodes":len(nodes),
        "candidate_edges":len(edges),
        "frontier":[{"reason":reason,"rva":rva} for reason,rva in front],
        "node_limit_hit":cap, "target_register_sources":tracked,
        "actual_entry_verified":False,"all_incoming_edges_proven":False,
        "fallthrough_structural_only":True,"runtime_call_target_proven":False,
        "callee_effect_summary_admitted":False,
        "return_value_in_eax_proven":False,
        "executed_write_at_second_global_proven":False,
    }

def third_global_frontier(dec, sections, push_site=PUSH_SITE,
                          target=THIRD_GLOBAL):
    ins=dec.at(push_site)
    if (ins is None or ins.mnemonic!="push" or
        len(ins.operands)!=1 or ins.operands[0].type!=X86_OP_MEM):
        raise ValueError("R19 pre-HeapAlloc PUSH identity mismatch")
    m=ins.operands[0]
    if (m.mem.base or m.mem.index or m.mem.segment or m.size!=4 or
        ((int(m.mem.disp)&0xffffffff)-dec.base)&0xffffffff!=target):
        raise ValueError("R19 third global PUSH target changed")
    refs=linear_references(dec,targets=(target,))
    return {
        "push_rva":push_site, "source_operand":operand_shape(ins,m,sections,dec.base),
        "linear_references":refs,
        "target_virtual_rva":target,
        "push_precedes_heapalloc_iat_site_syntactically":push_site<EAX_CALL,
        "actual_heapalloc_argument_position_proven":False,
        "actual_global_value_proven":False,
        "all_indirect_aliases_covered":False,
        "runtime_heap_size_or_flags_proven":False,
    }

def heapalloc_prefix(dec,root=HEAP_ANCHOR,call=EAX_CALL,max_steps=16):
    if type(max_steps) is not int or not 1<=max_steps<=16:
        raise ValueError("heap prefix bound")
    # Consecutive instruction boundary check with early control-transfer stop.
    cur=root;sites=[];stop=None;candidate_pushes=[]
    for _ in range(max_steps):
        ins=dec.at(cur)
        if ins is None:stop="decode_or_outside_text";break
        if cur==call:
            if not ins.group(CS_GRP_CALL):raise ValueError("original HeapAlloc CALL changed")
            stop="at_opaque_heapalloc_call";break
        if ins.group(CS_GRP_CALL) or ins.group(CS_GRP_JUMP) or ins.group(CS_GRP_RET):
            stop="earlier_control_transfer_barrier";break
        if ins.mnemonic=="push":
            candidate_pushes.append(cur)
        sites.append(cur);cur+=ins.size
    else:stop="prefix_bound"
    return {
        "candidate_anchor_rva":root,"heapalloc_call_rva":call,
        "prefix_instruction_sites":sites,"prefix_push_sites":candidate_pushes,
        "stop_reason":stop,
        "all_real_entry_paths_proven":False,
        "stack_argument_roles_proven":False,
        "original_heapalloc_return_proven":False,
    }

def alias_gap_frontier(dec,sections,site=ALIAS_SITE,root=EBX_TARGET):
    ins=dec.at(site)
    if ins is None or not any(op.type==X86_OP_MEM for op in ins.operands):
        raise ValueError("R19 EBX alias gap no longer memory-bearing")
    model=summarize(dec,root,max_states=80)
    if not any(g["rva"]==site and g["reason"]=="alias_write" for g in model["gap_sites"]):
        raise ValueError("R19 bounded alias/write gap changed")
    nodes,edges,front,cap=bounded_graph(dec,root,max_span=160,max_nodes=128)
    return {
        "site_rva":site,"candidate_root_rva":root,
        "mnemonic_class":ins.mnemonic,
        "operand_shapes":[operand_shape(ins,o,sections,dec.base) for o in ins.operands],
        "model_original_gap_present":True,
        "candidate_graph_reaches_site":site in nodes,
        "candidate_graph_nodes":len(nodes),
        "candidate_graph_edges":len(edges),
        "candidate_frontier":[{"reason":why,"rva":at} for why,at in front],
        "candidate_graph_cap_hit":cap,
        "r8_cycle_retained":model["control_flow_cycle"],
        "r8_gaps":model["gaps"],
        "r8_return_summary_qualified":model["qualifies_modeled_return_effect_summary"],
        "alias_effective_address_proven":False,"alias_object_owner_proven":False,
        "conditional_branch_outcomes_proven":False,
        "caller_effects_admitted":False,
        "function_entry_proven":False,
    }

def inspect_static(dec,sections,imports):
    return {
        "second_call":indirect_call_frontier(dec,sections,imports),
        "third_global":third_global_frontier(dec,sections),
        "heapalloc_prefix":heapalloc_prefix(dec),
        "ebx_alias_gap":alias_gap_frontier(dec,sections),
    }

def inspect_verified(runtime,savedata):
    old=inspect_r19(runtime,savedata)
    writes=old["second_global_writes"]
    if (tuple(w["site_rva"] for w in writes)!=WRITES
        or writes[1]["local_source"]["reaching_candidates"][0]["rva"]!=SECOND_CALL
        or old["heapalloc"]["call_identity"]["import_identity"]!=
        {"dll":"KERNEL32.dll","name":"HeapAlloc","iat_rva":0x520f8}
        or old["ebx_call"]["callee_summary"]["gap_sites"][0]["rva"]!=ALIAS_SITE
        or old["heapalloc"]["syntactic_pre_call_push_candidates"][0]["site_rva"]!=PUSH_SITE
        or old["heapalloc"]["syntactic_pre_call_push_candidates"][0]["operand"]["memory_input"]["displacement_region"]["displacement_rva"]!=THIRD_GLOBAL):
        raise ValueError("R19 pinned original evidence changed")
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/"sa_3.exe";p.write_bytes(runtime)
        data,pe,base,sections,imports=image_layout(p)
    for sec,raw in zip(sections,pe.sections):
        sec["characteristics"]=int(raw.Characteristics)
    t=next(sec for sec in sections if sec["name"]==".text")
    dec=Decoder(data[t["raw"]:t["raw"]+t["raw_size"]],t["rva"],base)
    derived=inspect_static(dec,sections,imports)
    return {
        "schema":SCHEMA,"status":STATUS,
        "runtime_sha256":RUNTIME_SHA256,"savedata_sha256":SAVEDATA_SHA256,
        "r19_original_identity_revalidated":True,
        "static_only":True, **derived, **{k:False for k in FLAGS},
    }

def main():
    p=argparse.ArgumentParser();p.add_argument("--bin",type=Path,required=True)
    args=p.parse_args();image,rows,_,_=find_rows(args.bin)
    try:
        files={r["path"]:r for r in rows if not r["is_dir"]}
        with tempfile.TemporaryDirectory() as td:
            exe,saved=Path(td)/"sa_3.exe",Path(td)/"savedata.dat"
            extract_row(image,files[RUNTIME_PATH],exe)
            extract_row(image,files[SAVEDATA_PATH],saved)
            report=inspect_verified(exe.read_bytes(),saved.read_bytes())
    finally:image.close()
    print(json.dumps(report,sort_keys=True))
if __name__=="__main__":main()
