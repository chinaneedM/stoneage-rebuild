"""R19: original-only second-global stores and HeapAlloc/callee caller frontier.

This is a static evidence tool. Decode pinned original bytes transiently; no
original executable execution, no operands/opcode bytes in emitted metadata.
No function entry, runtime heap success, argument ABI or object ownership claim.
"""
import argparse
import json
import tempfile
from pathlib import Path
from capstone import CS_GRP_CALL, CS_GRP_JUMP, CS_GRP_RET
from capstone.x86 import X86_OP_REG, X86_OP_IMM, X86_OP_MEM
from tools.stoneage_tw10_savedata_upstream_r18 import (
    inspect_verified as inspect_r18, EAX_CALL, SECOND_GLOBAL,
    EBX_WRITE, IMUL_ROOT, IMUL_SITE, RUNTIME_SHA256, SAVEDATA_SHA256,
)
from tools.stoneage_tw10_savedata_mutations_r13 import write_candidate, operand_value
from tools.stoneage_tw10_savedata_write_shapes_r17 import candidate_sources, operand_shape
from tools.stoneage_tw10_savedata_reachdefs_r14 import bounded_graph, GLOBAL_ANCHOR
from tools.stoneage_tw10_savedata_frontier_r12 import call_identity
from tools.stoneage_tw10_savedata_helper_effects_r8 import summarize
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder, direct_target
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH, SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows, extract_row

SCHEMA="tw10-r19-original-second-global-heapalloc-argument-and-caller-frontier"
STATUS="ORIGINAL_CONDITIONAL_STATIC_ONLY_EFFECTS_AND_OWNERSHIP_OPEN"
WRITES=(0x49a14,0x4a0d5)
# Diagnostic *anchors* selected for code proximity, never verified entries.
ANCHORS={0x49a14:0x49a00,0x4a0d5:0x4a0a0}
EBX_CALL=0x49e6e
EBX_TARGET=0x4a14d
IMUL_CALLS=(0x49444,0x4945d)
HEAP_ANCHOR=0x49a00
FLAGS=(
    "actual_function_entry_proven", "all_incoming_paths_proven",
    "heapalloc_arguments_complete_or_runtime_proven",
    "heapalloc_return_value_or_allocation_proven",
    "global_effective_values_proven", "second_global_initialized_proven",
    "global_owner_proven", "ebx_callee_effects_admitted",
    "imul_caller_frame_owner_proven", "callee_return_effects_admitted",
    "caller_continuation_admitted", "filename_api_link_proven",
    "handle_buffer_length_link_proven", "original_save_format_proven",
    "native_io_executed", "original_binary_published",
)

def second_global_writes(dec, sections, writes=WRITES, anchors=ANCHORS,
                         global_rva=SECOND_GLOBAL):
    if len(set(writes)) != len(writes):
        raise ValueError("duplicate pinned global writes")
    rows=[]
    for site in writes:
        write=write_candidate(dec, site, sections, expected_global=global_rva)
        src=write["source_operand"]
        reg=src["register"] if src and src["kind"]=="register_input" else None
        root=anchors[site]
        entry=candidate_sources(dec,site,reg,sections,root)
        rows.append({
            "site_rva":site, "write":write, "local_source":entry,
            "source_value_proven":False, "actual_executed_write_proven":False,
            "initialized_global_proven":False, "same_object_owner_proven":False,
        })
    return rows

def heapalloc_argument_candidates(dec, sections, imports, call_site=EAX_CALL,
                                  anchor=HEAP_ANCHOR):
    identity=call_identity(dec,call_site,imports,sections)
    if (identity["import_identity"] !=
            {"dll":"KERNEL32.dll","name":"HeapAlloc","iat_rva":0x520f8}):
        raise ValueError("R18 pinned HeapAlloc import identity mismatch")
    nodes,edges,front,cap=bounded_graph(dec,anchor,max_span=192,max_nodes=128)
    if call_site not in nodes:
        raise ValueError("HeapAlloc CALL not in candidate graph")
    candidates=[]
    for at,ins in sorted(nodes.items()):
        if at >= call_site or ins.mnemonic != "push" or len(ins.operands)!=1:
            continue
        src=ins.operands[0]
        candidates.append({
            "site_rva":at,
            "operand":operand_value(ins,src,sections,dec.base),
            "operand_class":src.type,
            "candidate_only":True,
            "can_be_assigned_to_heapalloc_argument_slot":False,
        })
    if len(candidates)>20:
        raise ValueError("candidate push cap")
    return {
        "call_identity":identity,
        "anchor_rva":anchor,
        "nodes":len(nodes),"edges":len(edges),
        "frontier":[{"reason":why,"rva":at} for why,at in front],
        "node_limit_hit":cap,
        "syntactic_pre_call_push_candidates":candidates,
        "verified_entry_or_path":False,
        "heapalloc_signature_applied_to_stack":False,
        "argument_count_and_slots_proven":False,
        "runtime_heap_handle_flags_size_proven":False,
        "return_pointer_proven":False,
        "allocation_success_proven":False,
        "return_to_second_global_owner_proven":False,
    }

def ebx_callee_frontier(dec,sections,imports,site=EBX_CALL,target=EBX_TARGET):
    call=call_identity(dec,site,imports,sections)
    if call["kind"]!="direct" or call["direct_target_rva"]!=target:
        raise ValueError("R18 EBX CALL target changed")
    # Root already sampled at R16, preserve all unresolved aliases/cycles.
    summary=summarize(dec,target,max_states=80)
    return {
        "call_identity":call,"callee_summary":summary,
        "original_source_ebx_after_call_known":False,
        "entry_context_and_arguments_proven":False,
        "runtime_callee_return_proven":False,
        "caller_resume_admitted":False,
    }

def imul_call_contexts(dec,sections,imports,call_sites=IMUL_CALLS,
                       expected_target=IMUL_ROOT):
    result=[]
    for site in call_sites:
        ident=call_identity(dec,site,imports,sections)
        if ident["kind"]!="direct" or ident["direct_target_rva"]!=expected_target:
            raise ValueError("R16 IMUL callee caller identity changed")
        result.append({
            "call_identity":ident,
            "callee_imul_site_rva":IMUL_SITE,
            "callee_model_entry_esp_plus8_not_actual_argument":True,
            "verified_effective_entry_esp":False,
            "caller_argument_ownership_proven":False,
            "caller_path_feasible_proven":False,
            "return_effects_admitted":False,
        })
    return result

def inspect_static(dec,sections,imports):
    return {
        "second_global_writes":second_global_writes(dec,sections),
        "heapalloc":heapalloc_argument_candidates(dec,sections,imports),
        "ebx_call":ebx_callee_frontier(dec,sections,imports),
        "imul_caller_contexts":imul_call_contexts(dec,sections,imports),
    }

def inspect_verified(runtime,savedata):
    old=inspect_r18(runtime,savedata)
    rows=old["secondary_global"]["global_reference_candidates"]["globals"][0]
    sites=tuple(x["rva"] for x in rows["samples"] if x["kind"]=="write_candidate")
    if (sites!=WRITES or rows["counts"]["write_candidate"]!=2
          or old["eax_call_barrier"]["call_identity"]["import_identity"]
          != {"dll":"KERNEL32.dll","name":"HeapAlloc","iat_rva":0x520f8}
          or old["ebx_graph"]["write_site_rva"]!=EBX_WRITE
          or old["imul_stack"]["modeled_stack_offset_of_memory_operand"]!=8):
        raise ValueError("R18 original static boundary changed")
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/"sa_3.exe";p.write_bytes(runtime)
        data,pe,base,sections,imports=image_layout(p)
    for sec,raw_sec in zip(sections,pe.sections):
        sec["characteristics"]=int(raw_sec.Characteristics)
    t=next(s for s in sections if s["name"]==".text")
    dec=Decoder(data[t["raw"]:t["raw"]+t["raw_size"]],t["rva"],base)
    result=inspect_static(dec,sections,imports)
    return {
        "schema":SCHEMA,"status":STATUS,
        "runtime_sha256":RUNTIME_SHA256,"savedata_sha256":SAVEDATA_SHA256,
        "r18_original_identity_revalidated":True,
        "conditional_static_only":True,
        **result, **{k:False for k in FLAGS}
    }

def main():
    p=argparse.ArgumentParser();p.add_argument("--bin",type=Path,required=True)
    args=p.parse_args()
    image,rows,_,_=find_rows(args.bin)
    try:
        files={r["path"]:r for r in rows if not r["is_dir"]}
        with tempfile.TemporaryDirectory() as td:
            exe=Path(td)/"sa_3.exe";saved=Path(td)/"savedata.dat"
            extract_row(image,files[RUNTIME_PATH],exe)
            extract_row(image,files[SAVEDATA_PATH],saved)
            report=inspect_verified(exe.read_bytes(),saved.read_bytes())
    finally:
        image.close()
    print(json.dumps(report,sort_keys=True))

if __name__=="__main__":
    main()
