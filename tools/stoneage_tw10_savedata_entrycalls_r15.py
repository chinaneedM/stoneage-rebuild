"""TW1.0 R15 original-only bounded upstream definitions, frame and call identities.

No ABI assumptions: every CALL invalidates candidate register values. Anchors
are not proven entries; frame writes cannot be assigned caller ownership.
Never execute the original PE; report no opcode/disassembly or original bytes.
"""
import argparse
import json
import tempfile
from pathlib import Path
from capstone import CS_GRP_CALL
from tools.stoneage_tw10_savedata_reachdefs_r14 import (
    inspect_verified as inspect_r14, bounded_graph, HELPER_ANCHOR, GLOBAL_ANCHOR,
    RUNTIME_SHA256, SAVEDATA_SHA256,
)
from tools.stoneage_tw10_savedata_inputs_r11 import reaches, semantic
from tools.stoneage_tw10_savedata_frontier_r12 import call_identity
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH,SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows,extract_row

SCHEMA="tw10-r15-original-upstream-frame-and-opaque-call-frontier"
STATUS="PINNED_ORIGINAL_STATIC_PROVENANCE_NO_NAMED_EFFECTS"
QUERIES=((0x49de8,"eax"), (0x49dca,"ebp"), (0x49dec,"ebp"),
         (0x49dec,"esp"))
CALL_SITES=(0x49444,0x4945d,0x4946f,0x49e5f,0x49e6e)
FLAGS=("actual_function_entry_proven","frame_setup_ownership_proven",
       "register_values_fully_known","global_initialization_proven",
       "opaque_call_effects_resolved","branch_feasibility_proven",
       "caller_effects_admitted","native_io_executed",
       "fixed_128_byte_schema_proven","filename_api_link_proven",
       "handle_buffer_size_link_proven","original_bytes_published")
# R11 deliberately omits ESP. Add it explicitly without treating CALL as an
# ABI-preservation event; implicit PUSH/POP/RET writes remain just definitions.
def register_origins(nodes,edges,root,register):
    if register!="esp":
        return reaches(nodes,edges,root,register)
    from collections import deque
    incoming={root:{("entry",root)}};succ={}
    for a,b in edges:succ.setdefault(a,[]).append(b)
    q=deque([root]);pending={root}
    while q:
        site=q.popleft();pending.discard(site);ins=nodes[site]
        writes=ins.regs_access()[1]
        defines=any(ins.reg_name(x) in ("esp","sp","spl") for x in writes)
        if ins.group(CS_GRP_CALL):out={("unknown_call",site)}
        elif defines:out={("definition",site)}
        else:out=incoming[site]
        for dst in succ.get(site,()):
            prior=incoming.setdefault(dst,set());n=len(prior);prior.update(out)
            if len(prior)!=n and dst not in pending:
                q.append(dst);pending.add(dst)
    return incoming

def query_origins(dec,nodes,edges,sections,queries,root):
    results=[]
    maps={reg:register_origins(nodes,edges,root,reg) for _,reg in queries}
    for site,reg in queries:
        if site not in nodes:
            raise ValueError("R15 selected original site missing from R14 graph")
        origin=[]
        for kind,at in sorted(maps[reg].get(site,()),key=lambda x:(x[1],x[0])):
            # Even 'definition' can be merely register copy/stack adjustment.
            sem=semantic(nodes[at],reg,sections,dec.base) if kind=="definition" and reg!="esp" else None
            origin.append({"kind":kind,"rva":at,"semantic":sem})
        results.append({"query_site_rva":site,"register":reg,
                        "origins":origin,"fully_known_value":False,
                        "verified_entry_to_query_path":False})
    return results

def call_surfaces(dec,sites,imports,sections,nodes):
    result=[]
    for site in sites:
        if site not in nodes:
            raise ValueError("R15 CALL not in bounded R14 source graph")
        ins=nodes[site]
        if not ins.group(CS_GRP_CALL):
            raise ValueError("R15 expected exact CALL")
        ident=call_identity(dec,site,imports,sections)
        result.append({**ident,"callee_effect_summary_admitted":False,
                       "calling_convention_proven":False,
                       "returned_value_proven":False,
                       "runtime_transfer_proven":False})
    return result

def frame_sites(nodes):
    # Registers are observed syntactically; neither a stack prologue nor a
    # caller/local ownership proof is implied. Bounded count avoids raw bytes.
    return [{"rva":rva,"writes_ebp":any(ins.reg_name(x) in ("ebp","bp") for x in ins.regs_access()[1]),
             "writes_esp":any(ins.reg_name(x) in ("esp","sp","spl") for x in ins.regs_access()[1])}
            for rva,ins in sorted(nodes.items())
            if any(ins.reg_name(x) in ("ebp","bp","esp","sp","spl")
                   for x in ins.regs_access()[1])]

def inspect_verified(runtime,savedata):
    prior=inspect_r14(runtime,savedata)
    helper,globals_=prior["regions"]
    if (helper["node_count"],helper["edge_count"],globals_["node_count"],
        globals_["edge_count"])!=(139,158,48,53):
        raise ValueError("R14 original bounded graph changed")
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/"sa_3.exe";p.write_bytes(runtime)
        data,pe,base,sections,imports=image_layout(p)
    for s,raw in zip(sections,pe.sections):
        s["characteristics"]=int(raw.Characteristics)
    text=next(s for s in sections if s["name"]==".text")
    dec=Decoder(data[text["raw"]:text["raw"]+text["raw_size"]],text["rva"],base)
    hn,he,hf,hcap=bounded_graph(dec,HELPER_ANCHOR)
    gn,ge,gf,gcap=bounded_graph(dec,GLOBAL_ANCHOR)
    if hcap or gcap or sorted(hn)!=sorted(helper["branch_sites"]+helper["call_barrier_sites"]) and len(hn)!=139:
        raise ValueError("unexpected R14 graph")
    if [v for v in CALL_SITES if v in hn or v in gn]!=list(CALL_SITES):
        raise ValueError("R15 explicit CALL sites no longer match")
    inquiries=query_origins(dec,hn,he,sections,QUERIES,HELPER_ANCHOR)
    call_nodes={**gn,**hn}
    calls=call_surfaces(dec,CALL_SITES,imports,sections,call_nodes)
    return {"schema":SCHEMA,"status":STATUS,
            "runtime_sha256":RUNTIME_SHA256,"savedata_sha256":SAVEDATA_SHA256,
            "r14_helper_nodes":len(hn),"r14_global_nodes":len(gn),
            "upstream_inputs":inquiries,"call_surfaces":calls,
            "helper_frame_write_candidates":frame_sites(hn),
            "global_frame_write_candidates":frame_sites(gn),
            "helper_outside_edges":len(hf),"global_outside_edges":len(gf),
            "bounded_graph_entry_not_proven":True,
            "call_fallthrough_structural_only":True,
            "exact_local_register_definitions_not_effective_values":True,
            **{flag:False for flag in FLAGS}}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--bin",type=Path,required=True)
    args=p.parse_args()
    image,rows,_,_=find_rows(args.bin)
    try:
        paths={item["path"]:item for item in rows if not item["is_dir"]}
        with tempfile.TemporaryDirectory() as d:
            exe,save=Path(d)/"sa_3.exe",Path(d)/"savedata.dat"
            extract_row(image,paths[RUNTIME_PATH],exe)
            extract_row(image,paths[SAVEDATA_PATH],save)
            obj=inspect_verified(exe.read_bytes(),save.read_bytes())
    finally:
        image.close()
    print(json.dumps(obj,sort_keys=True))

if __name__=="__main__":
    main()
