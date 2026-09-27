#!/usr/bin/env python3
"""Resolve indirect/table references for Taiwan v1.0 data/savedata.dat.

R1 proved the exact string exists in sa_3.exe .data but has zero direct .text
xrefs. R2 therefore searches:
1) stored 32-bit pointers to the string VA anywhere in the image;
2) .text xrefs to those pointer slots;
3) direct absolute .text references to a bounded .data neighborhood around the
   string, ranked by distance;
4) bounded call graphs from the nearest referenced globals, reporting only
   derived RVAs/API names/constants.

No executable/disc/savedata bytes or disassembly text are committed.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import struct
from pathlib import Path
import tempfile

from capstone import Cs, CS_ARCH_X86, CS_MODE_32

from tools.stoneage_tw10_technical_probe import find_rows, extract_row
from tools.stoneage_tw10_mapcache_binary_probe import (
    image_layout,
    likely_function_window,
    referenced_absolute_values,
    imported_call,
)
from tools.stoneage_tw10_savedata_probe import (
    RUNTIME_PATH,
    SAVEDATA_PATH,
    NEEDLE,
    FILE_APIS,
    SIZE_CONSTANTS,
    writable_ranges,
    graph_from_root,
    offset_to_rva,
    text_instructions,
)

NEIGHBOR_RADIUS=0x800
MAX_NEIGHBOR_REFS=80
MAX_PTR_SLOTS=64

def clean(v,n=1400):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def section_for_va(sections,base,va):
    rva=va-base
    for sec in sections:
        span=max(sec["vsize"],sec["raw_size"])
        if sec["rva"]<=rva<sec["rva"]+span:
            return sec["name"],rva-sec["rva"]
    return "",-1

def all_occurrences(data,needle):
    out=[]; start=0
    while True:
        pos=data.find(needle,start)
        if pos<0: break
        out.append(pos); start=pos+1
    return tuple(out)

def pointer_slots(data,base,sections,target_va):
    needle=struct.pack("<I",target_va)
    rows=[]
    for off in all_occurrences(data,needle):
        rva,sec=offset_to_rva(sections,off)
        if rva is not None:
            rows.append((off,rva,base+rva,sec))
    return tuple(rows)

def xref_indices(insns,va):
    return tuple(i for i,ins in enumerate(insns) if va in referenced_absolute_values(ins))

def neighborhood_refs(insns,target_va,radius):
    rows=[]
    lo=target_va-radius; hi=target_va+radius
    for i,ins in enumerate(insns):
        for value in referenced_absolute_values(ins):
            if lo<=value<=hi:
                rows.append((abs(value-target_va),value,i))
    # one row per (value, instruction)
    uniq={}
    for dist,value,i in rows:
        uniq[(value,i)]=(dist,value,i)
    return tuple(sorted(uniq.values(),key=lambda x:(x[0],x[1],x[2])))

def emit_root(label,idx,insns,imports,base,text_sec,writable):
    a,b,conf,nodes=graph_from_root(insns,idx,imports,base,text_sec,writable)
    print(
        f"ROOT|label={clean(label)}|xref_rva=0x{insns[idx].address-base:x}|"
        f"function_start_rva=0x{insns[a].address-base:x}|"
        f"function_end_rva=0x{insns[b].address-base:x}|boundary={conf}|nodes={len(nodes)}"
    )
    api=collections.Counter(); sizes=collections.Counter()
    for node in nodes:
        for k,v in node["api"].items(): api[k]+=v
        for k,v in node["sizes"].items(): sizes[k]+=v
    for (dll,name),count in sorted(api.items()):
        print(f"ROOT_API|label={clean(label)}|dll={clean(dll)}|api={clean(name)}|calls={count}")
    for value,count in sorted(sizes.items()):
        print(f"ROOT_SIZE|label={clean(label)}|value={value}|count={count}")
    return api,sizes

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--bin",required=True)
    args=ap.parse_args()

    print("StoneAge Taiwan v1.0 savedata pointer/table probe — R2")
    print("PARENT|STONEAGE-TW10-SAVEDATA-R1.txt|direct string xrefs=0")
    print("SCOPE|accepted-clean-disc|pointer-slot+neighbor-global xrefs|derived metadata only|no payload")

    img,rows,layout,joliet=find_rows(args.bin)
    td=tempfile.TemporaryDirectory()
    root=Path(td.name)
    try:
        by={r["path"]:r for r in rows if not r["is_dir"]}
        runtime=root/"sa_3.exe"; saved=root/"savedata.dat"
        extract_row(img,by[RUNTIME_PATH],runtime)
        extract_row(img,by[SAVEDATA_PATH],saved)

        data,pe,base,sections,imports=image_layout(runtime)
        text_sec,insns=text_instructions(data,base,sections)
        writable=writable_ranges(pe,base)
        pos=data.find(NEEDLE)
        if pos<0:
            raise SystemExit("savedata string missing")
        rva,sec=offset_to_rva(sections,pos)
        target_va=base+rva
        print(
            f"TARGET|string_rva=0x{rva:x}|section={clean(sec)}|"
            f"savedata_size={saved.stat().st_size}|savedata_sha256={hashlib.sha256(saved.read_bytes()).hexdigest()}"
        )

        slots=pointer_slots(data,base,sections,target_va)
        print(f"COUNT|pointer_slots={len(slots)}")
        aggregate_api=collections.Counter()
        root_keys=set()
        for n,(off,srva,sva,ssec) in enumerate(slots[:MAX_PTR_SLOTS],1):
            refs=xref_indices(insns,sva)
            print(
                f"POINTER_SLOT|n={n}|slot_rva=0x{srva:x}|section={clean(ssec)}|"
                f"target_string_rva=0x{rva:x}|text_xrefs={len(refs)}"
            )
            for rn,idx in enumerate(refs[:24],1):
                key=("slot",insns[idx].address)
                if key in root_keys: continue
                root_keys.add(key)
                api,_=emit_root(f"slot{n}_ref{rn}",idx,insns,imports,base,text_sec,writable)
                aggregate_api.update(api)

        neighbors=neighborhood_refs(insns,target_va,NEIGHBOR_RADIUS)
        print(
            f"NEIGHBORHOOD|radius=0x{NEIGHBOR_RADIUS:x}|raw_refs={len(neighbors)}|"
            f"unique_values={len(set(v for _,v,_ in neighbors))}"
        )
        emitted=0
        for dist,value,idx in neighbors:
            secname,secoff=section_for_va(sections,base,value)
            # The target is in .data; prioritize references into the same section.
            if secname!=sec:
                continue
            print(
                f"NEIGHBOR_REF|distance={dist}|direction={'before' if value<target_va else 'after' if value>target_va else 'exact'}|"
                f"target_section_offset=0x{secoff:x}|xref_rva=0x{insns[idx].address-base:x}"
            )
            key=("neighbor",insns[idx].address)
            if key not in root_keys:
                root_keys.add(key)
                api,_=emit_root(
                    f"neighbor_{'m' if value<target_va else 'p'}{dist:x}",
                    idx,insns,imports,base,text_sec,writable
                )
                aggregate_api.update(api)
            emitted+=1
            if emitted>=MAX_NEIGHBOR_REFS:
                break

        print(f"COUNT|neighbor_refs_emitted={emitted}")
        print(f"COUNT|root_functions={len(root_keys)}")
        for (dll,name),count in sorted(aggregate_api.items()):
            print(f"AGG_FILE_API|dll={clean(dll)}|api={clean(name)}|calls={count}")

        has_io=any(name in {"ReadFile","WriteFile","CreateFileA"} for _,name in aggregate_api)
        if slots and any(xref_indices(insns,sva) for _,_,sva,_ in slots):
            print(
                "RESOLUTION|SAVEDATA_POINTER_SLOT_XREF_RECOVERED|"
                f"file_io_in_reachable_graph={int(has_io)}"
            )
        elif emitted:
            print(
                "RESOLUTION|SAVEDATA_NEIGHBOR_GLOBAL_REFERENCE_SURFACE_RECOVERED|"
                f"file_io_in_reachable_graph={int(has_io)}"
            )
        else:
            print("RESOLUTION|SAVEDATA_INDIRECTION_STILL_UNRESOLVED|next use data-table base/registration callsite discovery")
        print(
            "EVIDENCE_BOUNDARY|Neighbor-global proximity is a discovery aid only. "
            "No nearby global is assigned savedata semantics without a code path linking it to file I/O."
        )
    finally:
        img.close(); td.cleanup()

if __name__=="__main__":
    main()
