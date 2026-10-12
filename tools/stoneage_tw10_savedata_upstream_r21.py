"""TW1.0 R21: third-global writer, HeapReAlloc candidate inputs and alias gap.

STATIC ONLY. Historic executable data is hash-verified and held temporarily.
This emits bounded operand shapes and graph-local candidates, never original
bytes, runtime observations, ABI conclusions or actual object ownership.
"""
import argparse
import json
import tempfile
from pathlib import Path
from capstone.x86 import X86_OP_MEM, X86_OP_REG, X86_REG_INVALID
from tools.stoneage_tw10_savedata_upstream_r20 import (
    inspect_verified as inspect_r20, SECOND_CALL, SECOND_ANCHOR,
    THIRD_GLOBAL, ALIAS_SITE, EBX_TARGET, RUNTIME_SHA256, SAVEDATA_SHA256,
)
from tools.stoneage_tw10_savedata_mutations_r13 import write_candidate
from tools.stoneage_tw10_savedata_write_shapes_r17 import operand_shape, candidate_sources
from tools.stoneage_tw10_savedata_reachdefs_r14 import bounded_graph
from tools.stoneage_tw10_savedata_frontier_r12 import call_identity
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH, SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows, extract_row

SCHEMA = "tw10-r21-original-writer-heaprealloc-alias-source-frontier"
STATUS = "PINNED_ORIGINAL_CONDITIONAL_STATIC_ONLY_NO_RUNTIME_ADMISSION"
WRITER_SITE = 0x499dc
WRITER_ANCHORS = (0x499b0, 0x499c0, 0x499d0, WRITER_SITE)
HEAPREALLOC_IMPORT = {"dll":"KERNEL32.dll","name":"HeapReAlloc","iat_rva":0x520dc}
FLAGS = (
    "actual_branch_feasibility_proven", "real_function_entries_proven",
    "third_global_effective_write_proven", "third_global_value_proven",
    "third_global_initialization_proven", "heaprealloc_abi_slots_proven",
    "heaprealloc_success_or_return_proven", "heap_pointer_ownership_proven",
    "alias_effective_address_proven", "alias_owner_proven",
    "callee_return_effects_admitted", "caller_resumption_admitted",
    "native_file_io_executed", "native_save_format_proven",
    "original_bytes_published",
)

def third_global_writer(dec, sections, site=WRITER_SITE, target=THIRD_GLOBAL,
                        anchors=WRITER_ANCHORS):
    write=write_candidate(dec,site,sections,expected_global=target)
    src=write["source_operand"]
    reg=src["register"] if src and src["kind"]=="register_input" else None
    # Try bounded *candidate* anchors, never claim a function boundary.
    candidates=[candidate_sources(dec,site,reg,sections,a) for a in anchors]
    selected=next((c for c in candidates if c["query_site_in_candidate_graph"]),
                  candidates[-1])
    return {
        "site_rva":site, "target_rva":target, "write":write,
        "local_source":selected,
        "anchors_examined":[{"rva":a,"site_reached":c["query_site_in_candidate_graph"]}
                            for a,c in zip(anchors,candidates)],
        "writer_reachable_from_real_entry_proven":False,
        "source_register_value_proven":False,
        "direct_store_executed_proven":False,
        "all_indirect_aliases_covered":False,
    }

def heaprealloc_candidate_inputs(dec, sections, imports, root=SECOND_ANCHOR,
                                 callsite=SECOND_CALL):
    ident=call_identity(dec,callsite,imports,sections)
    nodes,edges,front,cap=bounded_graph(dec,root,max_span=192,max_nodes=128)
    if callsite not in nodes:raise ValueError("HeapReAlloc site absent from bounded candidate graph")
    pushes=[]
    for at,ins in sorted(nodes.items()):
        if at<callsite and ins.mnemonic=="push" and len(ins.operands)==1:
            pushes.append({"site_rva":at,
                           "input_shape":operand_shape(ins,ins.operands[0],sections,dec.base),
                           "conditional_candidate_only":True,
                           "heaprealloc_abi_position_proven":False})
    if len(pushes)>32:raise ValueError("HeapReAlloc push candidates exceed bound")
    # The register definitions are explicitly cut at the opaque CALL.
    before=[{"register":r,"candidate_source":candidate_sources(dec,callsite,r,sections,root)}
            for r in ("eax","ecx","edx")]
    return {
        "call_identity":ident,"candidate_anchor_rva":root,
        "candidate_nodes":len(nodes),"candidate_edges":len(edges),
        "node_limit_hit":cap,
        "frontier":[{"reason":reason,"rva":site} for reason,site in front],
        "pre_call_push_candidates":pushes, "register_candidates_before_call":before,
        "call_is_opaque_register_barrier":True,
        "post_call_eax_value_unknown":True,
        "stack_argument_slots_admitted":False,
        "heap_handle_flags_size_proven":False,
        "success_or_return_pointer_proven":False,
        "same_pointer_as_global_store_proven":False,
        "real_entry_and_paths_proven":False,
    }

def eax_alias_frontier(dec, sections, site=ALIAS_SITE, root=EBX_TARGET):
    ins=dec.at(site)
    if ins is None or ins.mnemonic!="mov" or len(ins.operands)!=2:
        raise ValueError("R20 alias site changed")
    dst,src=ins.operands
    if (dst.type!=X86_OP_MEM or src.type!=X86_OP_REG or
        dst.size!=4 or src.size!=4 or
        ins.reg_name(dst.mem.base)!="eax" or
        dst.mem.index!=X86_REG_INVALID or
        dst.mem.disp!=8 or
        ins.reg_name(src.reg)!="eax"):
        raise ValueError("R20 exact [EAX+8] <- EAX alias identity changed")
    source=candidate_sources(dec,site,"eax",sections,root)
    return {
        "site_rva":site,"candidate_root_rva":root,
        "destination":operand_shape(ins,dst,sections,dec.base),
        "source":operand_shape(ins,src,sections,dec.base),
        "same_syntactic_register_for_address_and_value":True,
        "eax_local_source":source,
        "real_object_base_or_alias_proven":False,
        "effective_write_proven":False,
        "callee_return_or_caller_effect_admitted":False,
        "cycle_or_branch_feasibility_proven":False,
    }

def inspect_static(dec,sections,imports):
    return {
        "third_writer":third_global_writer(dec,sections),
        "heaprealloc_inputs":heaprealloc_candidate_inputs(dec,sections,imports),
        "eax_alias":eax_alias_frontier(dec,sections),
    }

def inspect_verified(runtime,savedata):
    old=inspect_r20(runtime,savedata)
    refs=old["third_global"]["linear_references"]["globals"][0]
    writes=[x["rva"] for x in refs["samples"] if x["kind"]=="write_candidate"]
    if (writes!=[WRITER_SITE] or refs["counts"]["write_candidate"]!=1
        or old["second_call"]["call_identity"]["import_identity"]!=HEAPREALLOC_IMPORT
        or old["ebx_alias_gap"]["site_rva"]!=ALIAS_SITE
        or old["ebx_alias_gap"]["r8_return_summary_qualified"] is not False):
        raise ValueError("R20 pinned source/call/alias identity changed")
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/"sa_3.exe";p.write_bytes(runtime)
        data,pe,base,sections,imports=image_layout(p)
    for s,raw in zip(sections,pe.sections):
        s["characteristics"]=int(raw.Characteristics)
    t=next(s for s in sections if s["name"]==".text")
    dec=Decoder(data[t["raw"]:t["raw"]+t["raw_size"]],t["rva"],base)
    report=inspect_static(dec,sections,imports)
    if report["heaprealloc_inputs"]["call_identity"]["import_identity"]!=HEAPREALLOC_IMPORT:
        raise ValueError("R21 HeapReAlloc IAT identity changed")
    return {
        "schema":SCHEMA,"status":STATUS,
        "runtime_sha256":RUNTIME_SHA256,"savedata_sha256":SAVEDATA_SHA256,
        "r20_original_identity_revalidated":True,"static_only":True,
        **report, **{name:False for name in FLAGS},
    }

def main():
    p=argparse.ArgumentParser();p.add_argument("--bin",type=Path,required=True)
    args=p.parse_args()
    image,rows,_,_=find_rows(args.bin)
    try:
        paths={r["path"]:r for r in rows if not r["is_dir"]}
        with tempfile.TemporaryDirectory() as td:
            exe,saved=Path(td)/"sa_3.exe",Path(td)/"savedata.dat"
            extract_row(image,paths[RUNTIME_PATH],exe)
            extract_row(image,paths[SAVEDATA_PATH],saved)
            report=inspect_verified(exe.read_bytes(),saved.read_bytes())
    finally:image.close()
    print(json.dumps(report,sort_keys=True))

if __name__=="__main__":main()
