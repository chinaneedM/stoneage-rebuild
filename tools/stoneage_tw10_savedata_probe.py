#!/usr/bin/env python3
"""Reverse-engineer Taiwan v1.0 data/savedata.dat from accepted clean bytes.

Derived-output-only probe:
- extracts sa_3.exe and data/savedata.dat transiently from the accepted disc;
- hashes and summarizes the 128-byte default local-state file without printing bytes;
- locates exact runtime string xrefs for data\\savedata.dat;
- follows bounded direct-call graph from each xref function;
- reports imported file APIs and size-related immediate constants;
- reports references into writable PE sections as candidate state buffers.

No executable, disc, savedata bytes, or disassembly text are committed.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import math
from pathlib import Path
import tempfile

from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_REG_INVALID

from tools.stoneage_tw10_technical_probe import find_rows, extract_row
from tools.stoneage_tw10_mapcache_binary_probe import (
    image_layout,
    imported_call,
    likely_function_window,
    referenced_absolute_values,
)

RUNTIME_PATH="StoneAge/sa_3.exe"
SAVEDATA_PATH="StoneAge/data/savedata.dat"
NEEDLE=b"data\\savedata.dat"
MAX_DEPTH=4
MAX_NODES=96
MAX_FUNCTION_BYTES=0x3000
SIZE_CONSTANTS={1,2,4,8,16,32,36,64,80,96,128,256,512,1024}
FILE_APIS={
    "CreateFileA","ReadFile","WriteFile","CloseHandle","SetFilePointer",
    "SetEndOfFile","FlushFileBuffers","DeleteFileA","CreateDirectoryA",
}

def clean(v,n=1200):
    return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def entropy(data: bytes) -> float:
    if not data:
        return 0.0
    counts=collections.Counter(data)
    total=len(data)
    return -sum((n/total)*math.log2(n/total) for n in counts.values())

def zero_runs(data: bytes):
    out=[]; start=None
    for i,b in enumerate(data):
        if b==0 and start is None:
            start=i
        elif b!=0 and start is not None:
            out.append((start,i-start)); start=None
    if start is not None:
        out.append((start,len(data)-start))
    return tuple(out)

def offset_to_rva(sections,off):
    for sec in sections:
        if sec["raw"]<=off<sec["raw"]+sec["raw_size"]:
            return sec["rva"]+(off-sec["raw"]),sec["name"]
    return None,""

def text_instructions(data,base,sections):
    sec=next(s for s in sections if s["name"]==".text")
    blob=data[sec["raw"]:sec["raw"]+sec["raw_size"]]
    md=Cs(CS_ARCH_X86,CS_MODE_32); md.detail=True
    return sec,list(md.disasm(blob,base+sec["rva"]))

def xrefs(instructions,va):
    return [i for i,ins in enumerate(instructions) if va in referenced_absolute_values(ins)]

def direct_targets(insns,a,b,text_lo,text_hi):
    out=collections.Counter()
    for ins in insns[a:b+1]:
        if ins.mnemonic!="call":
            continue
        for op in ins.operands:
            if op.type==X86_OP_IMM:
                target=int(op.imm)&0xffffffff
                if text_lo<=target<text_hi:
                    out[target]+=1
    return out

def nearest_index(insns,address):
    lo=0; hi=len(insns)
    while lo<hi:
        mid=(lo+hi)//2
        if insns[mid].address<address: lo=mid+1
        else: hi=mid
    if lo<len(insns) and insns[lo].address==address:
        return lo
    return None

def node_window(insns,idx):
    a,b,confidence=likely_function_window(insns,idx)
    # Keep recursion bounded even if heuristic function recovery runs long.
    start=insns[a].address
    while b>a and insns[b].address-start>MAX_FUNCTION_BYTES:
        b-=1
    return a,b,confidence

def writable_ranges(pe,base):
    out=[]
    IMAGE_SCN_MEM_WRITE=0x80000000
    for sec in pe.sections:
        if sec.Characteristics & IMAGE_SCN_MEM_WRITE:
            name=sec.Name.rstrip(b"\0").decode("ascii","replace")
            lo=base+sec.VirtualAddress
            hi=lo+max(sec.Misc_VirtualSize,sec.SizeOfRawData)
            out.append((lo,hi,name))
    return tuple(out)

def writable_ref(value,ranges):
    for lo,hi,name in ranges:
        if lo<=value<hi:
            return value-lo,name
    return None

def summarize_savedata(data):
    zr=zero_runs(data)
    nonzero=[i for i,b in enumerate(data) if b]
    longest=max((length for _,length in zr),default=0)
    print(
        f"SAVEDATA|size={len(data)}|sha256={hashlib.sha256(data).hexdigest()}|"
        f"md5={hashlib.md5(data).hexdigest()}|zero_bytes={data.count(0)}|"
        f"nonzero_bytes={len(nonzero)}|unique_byte_values={len(set(data))}|"
        f"entropy_bits_per_byte={entropy(data):.6f}|zero_runs={len(zr)}|longest_zero_run={longest}"
    )
    if nonzero:
        print(
            f"SAVEDATA_SPAN|first_nonzero={min(nonzero)}|last_nonzero={max(nonzero)}|"
            f"nonzero_span={max(nonzero)-min(nonzero)+1}"
        )
    else:
        print("SAVEDATA_SPAN|first_nonzero=-1|last_nonzero=-1|nonzero_span=0")
    # Emit only run geometry, never byte values.
    for start,length in sorted(zr,key=lambda x:(-x[1],x[0]))[:12]:
        print(f"ZERO_RUN|start={start}|length={length}")

def graph_from_root(insns,root_idx,imports,base,text_sec,writable):
    text_lo=base+text_sec["rva"]; text_hi=text_lo+text_sec["raw_size"]
    root_a,root_b,root_conf=node_window(insns,root_idx)
    root_start=insns[root_a].address
    queue=[(root_start,root_idx,0)]
    seen=set(); nodes=[]

    while queue and len(nodes)<MAX_NODES:
        start_va,hint_idx,depth=queue.pop(0)
        if start_va in seen or depth>MAX_DEPTH:
            continue
        idx=nearest_index(insns,start_va)
        if idx is None:
            idx=hint_idx
        a,b,conf=node_window(insns,idx)
        canonical=insns[a].address
        if canonical in seen:
            continue
        seen.add(canonical)

        api=collections.Counter()
        sizes=collections.Counter()
        globals_=collections.Counter()
        for ins in insns[a:b+1]:
            imp=imported_call(ins,imports)
            if imp and imp[1] in FILE_APIS:
                api[imp]+=1
            for op in ins.operands:
                if op.type==X86_OP_IMM:
                    val=int(op.imm)&0xffffffff
                    if val in SIZE_CONSTANTS:
                        sizes[val]+=1
                elif op.type==X86_OP_MEM:
                    mem=op.mem
                    if mem.base==X86_REG_INVALID and mem.index==X86_REG_INVALID:
                        val=int(mem.disp)&0xffffffff
                        wr=writable_ref(val,writable)
                        if wr:
                            globals_[(wr[1],wr[0])]+=1

        targets=direct_targets(insns,a,b,text_lo,text_hi)
        nodes.append({
            "start":canonical,"end":insns[b].address,"depth":depth,
            "confidence":conf,"api":api,"sizes":sizes,"globals":globals_,
            "targets":targets,
        })
        if depth<MAX_DEPTH:
            for target in targets:
                ti=nearest_index(insns,target)
                if ti is not None:
                    queue.append((target,ti,depth+1))
    return root_a,root_b,root_conf,nodes

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--bin",required=True)
    args=ap.parse_args()

    print("StoneAge Taiwan v1.0 savedata.dat runtime probe — R1")
    print("SCOPE|accepted-clean-disc|transient-bytes|derived-xref-callgraph-layout-only|no-payload-commit")

    img,rows,layout,joliet=find_rows(args.bin)
    td=tempfile.TemporaryDirectory()
    root=Path(td.name)
    try:
        by={r["path"]:r for r in rows if not r["is_dir"]}
        missing=[p for p in (RUNTIME_PATH,SAVEDATA_PATH) if p not in by]
        print(f"FILESYSTEM|layout={layout}|joliet={int(joliet)}|missing={len(missing)}")
        for p in missing:
            print(f"MISSING|path={clean(p)}")
        if missing:
            return

        runtime=root/"sa_3.exe"; saved=root/"savedata.dat"
        extract_row(img,by[RUNTIME_PATH],runtime)
        extract_row(img,by[SAVEDATA_PATH],saved)

        sdata=saved.read_bytes()
        summarize_savedata(sdata)

        data,pe,base,sections,imports=image_layout(runtime)
        text_sec,insns=text_instructions(data,base,sections)
        writable=writable_ranges(pe,base)
        print(
            f"RUNTIME|size={len(data)}|sha256={hashlib.sha256(data).hexdigest()}|"
            f"image_base=0x{base:x}|text_rva=0x{text_sec['rva']:x}|text_bytes={text_sec['raw_size']}|"
            f"writable_sections={len(writable)}"
        )

        locs=[]; start=0
        while True:
            off=data.find(NEEDLE,start)
            if off<0: break
            rva,sec=offset_to_rva(sections,off)
            if rva is not None:
                locs.append((off,rva,base+rva,sec))
            start=off+1
        print(f"STRING_COUNT|needle=data\\savedata.dat|occurrences={len(locs)}")

        total_xrefs=0; aggregate_api=collections.Counter(); aggregate_sizes=collections.Counter()
        aggregate_globals=collections.Counter()
        for ordinal,(off,rva,va,secname) in enumerate(locs,1):
            refs=xrefs(insns,va)
            print(
                f"STRING|n={ordinal}|file_offset=0x{off:x}|rva=0x{rva:x}|"
                f"section={clean(secname)}|xrefs={len(refs)}"
            )
            total_xrefs+=len(refs)
            for rn,idx in enumerate(refs,1):
                a,b,conf,nodes=graph_from_root(insns,idx,imports,base,text_sec,writable)
                x=insns[idx]
                print(
                    f"XREF|string_n={ordinal}|ref_n={rn}|xref_rva=0x{x.address-base:x}|"
                    f"root_start_rva=0x{insns[a].address-base:x}|root_end_rva=0x{insns[b].address-base:x}|"
                    f"boundary={conf}|graph_nodes={len(nodes)}"
                )
                for node in nodes:
                    print(
                        f"NODE|root_ref_n={rn}|depth={node['depth']}|"
                        f"start_rva=0x{node['start']-base:x}|end_rva=0x{node['end']-base:x}|"
                        f"boundary={node['confidence']}|direct_targets={len(node['targets'])}"
                    )
                    for (dll,name),count in sorted(node["api"].items()):
                        aggregate_api[(dll,name)]+=count
                        print(
                            f"FILE_API|root_ref_n={rn}|depth={node['depth']}|"
                            f"node_rva=0x{node['start']-base:x}|dll={clean(dll)}|api={clean(name)}|calls={count}"
                        )
                    for value,count in sorted(node["sizes"].items()):
                        aggregate_sizes[value]+=count
                        print(
                            f"SIZE_IMMEDIATE|root_ref_n={rn}|depth={node['depth']}|"
                            f"node_rva=0x{node['start']-base:x}|value={value}|count={count}"
                        )
                    for (section,offset),count in sorted(node["globals"].items()):
                        aggregate_globals[(section,offset)]+=count
                        print(
                            f"WRITABLE_REF|root_ref_n={rn}|depth={node['depth']}|"
                            f"node_rva=0x{node['start']-base:x}|section={clean(section)}|"
                            f"section_offset=0x{offset:x}|refs={count}"
                        )

        print(f"COUNT|string_occurrences={len(locs)}")
        print(f"COUNT|string_xrefs={total_xrefs}")
        print(f"COUNT|file_api_kinds={len(aggregate_api)}")
        print(f"COUNT|writable_ref_sites={len(aggregate_globals)}")
        print(f"SIZE128_CALLGRAPH_OCCURRENCES|{aggregate_sizes.get(128,0)}")
        for (dll,name),count in sorted(aggregate_api.items()):
            print(f"AGG_FILE_API|dll={clean(dll)}|api={clean(name)}|calls={count}")

        has_read=any(name=="ReadFile" for _,name in aggregate_api)
        has_write=any(name=="WriteFile" for _,name in aggregate_api)
        if total_xrefs and (has_read or has_write):
            print(
                "RESOLUTION|SAVEDATA_RUNTIME_FILE_CHAIN_RECOVERED|"
                f"read={int(has_read)}|write={int(has_write)}|size128_static_hits={aggregate_sizes.get(128,0)}"
            )
        elif total_xrefs:
            print("RESOLUTION|SAVEDATA_STRING_XREF_RECOVERED_FILE_IO_INDIRECT|follow internal wrappers/dynamic APIs next")
        else:
            print("RESOLUTION|SAVEDATA_STRING_PRESENT_NO_TEXT_XREF|use pointer/table indirection analysis next")
        print(
            "EVIDENCE_BOUNDARY|Default savedata bytes are hashed/summarized only. "
            "Static writable references are candidate state storage, not field semantics until access patterns are recovered."
        )
    finally:
        img.close()
        td.cleanup()

if __name__=="__main__":
    main()
