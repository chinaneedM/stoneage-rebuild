"""TW1.0 R22 original static-only opaque CALL, stack candidates and alias cycles.

Never executes original binary and never exports proprietary instruction bytes.
All graph entries, CALL fallthrough, reachability, stack roles and object owners
remain conditional: direct-target syntax != executed callee/returned effect.
"""
import argparse
import json
import tempfile
from collections import deque
from pathlib import Path
from capstone import CS_GRP_CALL, CS_GRP_JUMP
from tools.stoneage_tw10_savedata_upstream_r21 import (
    inspect_verified as inspect_r21, WRITER_SITE, WRITER_ANCHORS,
    SECOND_CALL, SECOND_ANCHOR, ALIAS_SITE, EBX_TARGET,
    HEAPREALLOC_IMPORT, RUNTIME_SHA256, SAVEDATA_SHA256,
)
from tools.stoneage_tw10_savedata_reachdefs_r14 import bounded_graph
from tools.stoneage_tw10_savedata_write_shapes_r17 import candidate_sources
from tools.stoneage_tw10_savedata_frontier_r12 import call_identity
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH, SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows, extract_row
from capstone.x86 import X86_OP_REG, X86_OP_MEM

SCHEMA = "tw10-r22-original-opaque-call-push-feasibility-eax-cycle"
STATUS = "PINNED_ORIGINAL_CONDITIONAL_STATIC_ONLY_NATIVE_IO_OPEN"
WRITER_CALL = 0x499d4
WRITER_ROOT = 0x499d0
FLAGS = (
    "real_function_entries_proven", "runtime_path_feasible_proven",
    "writer_call_executed_proven", "writer_call_return_effect_admitted",
    "third_global_effective_value_proven", "third_global_initialized_proven",
    "heaprealloc_argument_slots_proven", "heaprealloc_return_or_success_proven",
    "heaprealloc_pointer_owner_proven", "alias_cycle_executed_proven",
    "alias_effective_object_proven", "caller_resumption_admitted",
    "native_file_io_executed", "native_save_schema_proven",
    "original_bytes_published",
)

def graph_path(edges, start, target, cap=192):
    """Graph-only path existence, not a symbolic feasible execution trace."""
    pending=deque([start]);seen=set()
    succ={}
    for a,b in edges: succ.setdefault(a,[]).append(b)
    while pending and len(seen)<cap:
        cur=pending.popleft()
        if cur==target:return True
        if cur in seen:continue
        seen.add(cur);pending.extend(x for x in succ.get(cur,()) if x not in seen)
    return False

def writer_call_frontier(dec, sections, imports, root=WRITER_ROOT,
                         site=WRITER_CALL, writer=WRITER_SITE):
    ins=dec.at(site)
    if ins is None or not ins.group(CS_GRP_CALL):
        raise ValueError("R21 writer EAX CALL barrier changed")
    ident=call_identity(dec,site,imports,sections)
    nodes,edges,front,cap=bounded_graph(dec,root,max_span=160,max_nodes=128)
    if site not in nodes or writer not in nodes:
        raise ValueError("R21 original writer call/target outside bounded graph")
    sources={r:candidate_sources(dec,site,r,sections,root)
             for r in ("eax","ecx","edx")}
    return {
        "site_rva":site,"writer_rva":writer,"call_identity":ident,
        "anchor_rva":root,"candidate_nodes":len(nodes),"candidate_edges":len(edges),
        "frontier":[{"reason":kind,"rva":rva} for kind,rva in front],
        "node_limit_hit":cap,
        "call_to_writer_structural_path_exists":graph_path(edges,site,writer),
        "pre_call_register_sources":sources,
        "call_fallthrough_assumes_return_structurally":True,
        "actual_callee_return_or_register_effect_known":False,
        "writer_value_after_call_known":False,
        "function_entry_or_path_executed_proven":False,
    }

def realloc_push_flow(dec, sections, root=SECOND_ANCHOR, site=SECOND_CALL):
    nodes,edges,front,cap=bounded_graph(dec,root,max_span=192,max_nodes=128)
    if site not in nodes:raise ValueError("R21 realloc CALL not in candidate graph")
    pushes=[]
    for rva,ins in sorted(nodes.items()):
        if rva>=site or ins.mnemonic!="push" or len(ins.operands)!=1:continue
        op=ins.operands[0]
        source=dec.at(rva)
        if op.type==X86_OP_REG:
            kind="register";reg=ins.reg_name(op.reg)
        elif op.type==X86_OP_MEM:
            kind="memory";reg=None
        else:
            kind="other";reg=None
        pushes.append({
            "site_rva":rva,"kind":kind,"register":reg,
            "syntactic_cfg_path_to_call":graph_path(edges,rva,site),
            "register_source":candidate_sources(dec,rva,reg,sections,root)
                              if reg is not None else None,
            "original_stack_position_or_abi_role_proven":False,
            "runtime_operand_value_proven":False,
        })
    if len(pushes)>32:raise ValueError("R22 push candidate bound")
    return {
        "call_rva":site,"anchor_rva":root,
        "nodes":len(nodes),"edges":len(edges),"node_cap":cap,
        "graph_frontier":[{"reason":kind,"rva":at} for kind,at in front],
        "push_flow_candidates":pushes,
        "graph_reachability_is_not_stack_argument_proof":True,
        "callee_return_eax_effect_unknown":True,
        "heaprealloc_stack_signature_applied":False,
        "all_incoming_edges_or_real_paths_proven":False,
    }

def alias_cycle_frontier(dec, sections, root=EBX_TARGET, site=ALIAS_SITE):
    nodes,edges,front,cap=bounded_graph(dec,root,max_span=192,max_nodes=128)
    if site not in nodes:raise ValueError("R21 alias target outside graph")
    edges_back=sorted((a,b) for a,b in edges if b<=a)
    if len(edges_back)>32:raise ValueError("R22 backward edge cap")
    eax=candidate_sources(dec,site,"eax",sections,root)
    later=[r for r in eax["reaching_candidates"] if r["rva"]>site]
    return {
        "site_rva":site,"root_rva":root,"node_count":len(nodes),
        "edge_count":len(edges),"node_cap":cap,
        "frontier":[{"reason":reason,"rva":at} for reason,at in front],
        "backward_edges":[{"from_rva":a,"to_rva":b} for a,b in edges_back],
        "later_rva_eax_source_candidates":later,
        "eax_reaching_source":eax,
        "reverse_rva_source_does_not_prove_linear_order":True,
        "backward_edges_not_executed_paths":True,
        "r8_alias_write_unsummarized":True,
        "original_object_owner_known":False,
        "runtime_cycle_taken_known":False,
        "return_to_caller_admitted":False,
    }

def inspect_static(dec,sections,imports):
    return {
        "writer_opaque_call":writer_call_frontier(dec,sections,imports),
        "heaprealloc_push_flow":realloc_push_flow(dec,sections),
        "eax_cycle":alias_cycle_frontier(dec,sections),
    }

def inspect_verified(runtime,savedata):
    prior=inspect_r21(runtime,savedata)
    if (prior["third_writer"]["site_rva"]!=WRITER_SITE
        or prior["third_writer"]["local_source"]["reaching_candidates"][0]
           !={"origin":"unknown_call","rva":WRITER_CALL,"semantic":None}
        or prior["heaprealloc_inputs"]["call_identity"]["import_identity"]
           !=HEAPREALLOC_IMPORT
        or prior["eax_alias"]["site_rva"]!=ALIAS_SITE
        or prior["eax_alias"]["effective_write_proven"] is not False):
        raise ValueError("R21 original conditional identity changed")
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/"sa_3.exe";p.write_bytes(runtime)
        data,pe,base,sections,imports=image_layout(p)
    for sec,raw in zip(sections,pe.sections):
        sec["characteristics"]=int(raw.Characteristics)
    t=next(sec for sec in sections if sec["name"]==".text")
    dec=Decoder(data[t["raw"]:t["raw"]+t["raw_size"]],t["rva"],base)
    d=inspect_static(dec,sections,imports)
    if d["heaprealloc_push_flow"]["call_rva"]!=SECOND_CALL:
        raise ValueError("R22 realloc identity")
    return {
        "schema":SCHEMA,"status":STATUS,
        "runtime_sha256":RUNTIME_SHA256,"savedata_sha256":SAVEDATA_SHA256,
        "r21_original_identity_revalidated":True,"static_only":True,
        **d, **{x:False for x in FLAGS},
    }

def main():
    p=argparse.ArgumentParser();p.add_argument("--bin",type=Path,required=True)
    args=p.parse_args()
    image,rows,_,_=find_rows(args.bin)
    try:
        files={row["path"]:row for row in rows if not row["is_dir"]}
        with tempfile.TemporaryDirectory() as td:
            exe,saved=Path(td)/"sa_3.exe",Path(td)/"savedata.dat"
            extract_row(image,files[RUNTIME_PATH],exe)
            extract_row(image,files[SAVEDATA_PATH],saved)
            report=inspect_verified(exe.read_bytes(),saved.read_bytes())
    finally:image.close()
    print(json.dumps(report,sort_keys=True))

if __name__=="__main__":main()
