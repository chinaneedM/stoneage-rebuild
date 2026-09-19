#!/usr/bin/env python3
"""Derived-only xref/call-neighborhood probe for Taiwan StoneAge v1.0 sa_3.exe.

Purpose: test whether the early runtime's literal map\\%d.dat references are tied to
local file-cache APIs and/or networking APIs. The accepted retail payload is consumed
only transiently; this tool emits addresses, API names and bounded graph metrics, not
raw code bytes or disassembly listings.
"""

from __future__ import annotations

import argparse
import collections
from pathlib import Path
import struct
import tempfile

import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_REG_INVALID

from tools.stoneage_tw10_technical_probe import find_rows, extract_row

TARGET_PATH = b"map\\%d.dat"
RELATED_STRINGS = (
    b"map\\%d.dat",
    b"ClientLogin",
    b"CharLogin",
    b"waei.bin",
    b"data\\auto.dat",
    b"data\\mail.dat",
    b"data\\chatreg.dat",
    b"data\\album.dat",
)

FILE_APIS = {
    "CreateFileA", "ReadFile", "WriteFile", "SetFilePointer", "SetEndOfFile",
    "CloseHandle", "CreateDirectoryA", "GetFileAttributesA", "DeleteFileA",
}
NET_APIS = {
    "WSAStartup", "WSACleanup", "socket", "connect", "send", "recv", "select",
    "gethostbyname", "inet_addr", "htons", "closesocket", "ioctlsocket", "setsockopt",
}
DYNAMIC_APIS = {"LoadLibraryA", "GetProcAddress"}
ALL_INTERESTING = FILE_APIS | NET_APIS | DYNAMIC_APIS

MAX_BACK = 0x1800
MAX_FORWARD = 0x2800
MAX_XREFS = 32


def clean(v, limit=1000):
    s=" ".join(str(v if v is not None else "").split())
    return "".join(ch for ch in s if ch >= " " and ch != "\x7f").replace("|","%7C")[:limit]


def image_layout(path: Path):
    data=path.read_bytes()
    pe=pefile.PE(data=data, fast_load=False)
    base=pe.OPTIONAL_HEADER.ImageBase
    sections=[]
    for sec in pe.sections:
        name=sec.Name.rstrip(b"\0").decode("ascii","replace")
        sections.append({
            "name":name,
            "rva":sec.VirtualAddress,
            "vsize":sec.Misc_VirtualSize,
            "raw":sec.PointerToRawData,
            "raw_size":sec.SizeOfRawData,
        })
    imports={}
    for entry in getattr(pe,"DIRECTORY_ENTRY_IMPORT",[]):
        dll=entry.dll.decode("ascii","replace") if entry.dll else ""
        for imp in entry.imports:
            name=(imp.name.decode("ascii","replace") if imp.name else f"#{imp.ordinal}")
            imports[int(imp.address)]=(dll,name)
    return data,pe,base,sections,imports


def offset_to_rva(sections, off):
    for sec in sections:
        if sec["raw"] <= off < sec["raw"]+sec["raw_size"]:
            return sec["rva"]+(off-sec["raw"]),sec["name"]
    return None,""


def rva_to_offset(sections, rva):
    for sec in sections:
        span=max(sec["vsize"],sec["raw_size"])
        if sec["rva"] <= rva < sec["rva"]+span:
            delta=rva-sec["rva"]
            if delta >= sec["raw_size"]:
                return None
            return sec["raw"]+delta
    return None


def text_region(data,sections):
    for sec in sections:
        if sec["name"]==".text":
            raw=data[sec["raw"]:sec["raw"]+sec["raw_size"]]
            return sec,raw
    raise ValueError("no .text section")


def locate_strings(data,base,sections):
    rows=[]
    for value in RELATED_STRINGS:
        start=0
        while True:
            off=data.find(value,start)
            if off<0: break
            rva,sec=offset_to_rva(sections,off)
            rows.append({
                "text":value.decode("ascii","replace"),
                "file_offset":off,
                "rva":rva,
                "va":base+rva if rva is not None else None,
                "section":sec,
            })
            start=off+1
    return rows


def disassemble_text(data,base,sections):
    sec,raw=text_region(data,sections)
    md=Cs(CS_ARCH_X86,CS_MODE_32)
    md.detail=True
    ins=list(md.disasm(raw,base+sec["rva"]))
    return sec,ins


def referenced_absolute_values(ins):
    vals=[]
    for op in ins.operands:
        if op.type==X86_OP_IMM:
            vals.append(int(op.imm)&0xffffffff)
        elif op.type==X86_OP_MEM:
            mem=op.mem
            if mem.base==X86_REG_INVALID and mem.index==X86_REG_INVALID:
                vals.append(int(mem.disp)&0xffffffff)
    return vals


def xrefs_to_va(instructions,va):
    return [i for i,ins in enumerate(instructions) if va in referenced_absolute_values(ins)]


def imported_call(ins,imports):
    # direct absolute call/jmp to an import thunk address, or indirect [IAT].
    if ins.mnemonic not in {"call","jmp"}:
        return None
    for val in referenced_absolute_values(ins):
        if val in imports:
            return imports[val]
    return None


def likely_function_window(instructions,idx):
    # Heuristic only: old MSVC x86 commonly starts with push ebp / mov ebp,esp.
    # Fall back to a bounded byte-distance window and mark the boundary confidence.
    here=instructions[idx].address
    start_idx=idx
    confidence="bounded"
    for j in range(idx,max(-1,idx-800),-1):
        if here-instructions[j].address>MAX_BACK:
            break
        if j+1<len(instructions):
            a=instructions[j]
            b=instructions[j+1]
            if a.mnemonic=="push" and a.op_str=="ebp" and b.mnemonic=="mov" and b.op_str.replace(" ","")=="ebp,esp":
                start_idx=j
                confidence="prologue"
                break
    end_idx=idx
    for j in range(idx,min(len(instructions),idx+1200)):
        if instructions[j].address-here>MAX_FORWARD:
            break
        end_idx=j
        if j>idx and instructions[j].mnemonic.startswith("ret"):
            break
    return start_idx,end_idx,confidence


def direct_call_targets(instructions,a,b,base):
    out=collections.Counter()
    for ins in instructions[a:b+1]:
        if ins.mnemonic!="call":
            continue
        for op in ins.operands:
            if op.type==X86_OP_IMM:
                target=int(op.imm)&0xffffffff
                out[target]+=1
    return out


def emit_xref_neighborhoods(data,base,sections,imports):
    strings=locate_strings(data,base,sections)
    text_sec,instructions=disassemble_text(data,base,sections)
    print(f"PE|image_base=0x{base:x}|text_rva=0x{text_sec['rva']:x}|text_bytes={text_sec['raw_size']}|imports={len(imports)}")
    for (dll,name) in sorted(set(imports.values()),key=lambda x:(x[0].lower(),x[1].lower())):
        if name in ALL_INTERESTING:
            print(f"INTERESTING_IMPORT|dll={clean(dll)}|name={clean(name)}")

    for row in strings:
        if row["va"] is None:
            continue
        refs=xrefs_to_va(instructions,row["va"])
        print(
            f"STRING|text={clean(row['text'])}|file_offset=0x{row['file_offset']:x}|"
            f"rva=0x{row['rva']:x}|va=0x{row['va']:x}|section={clean(row['section'])}|xrefs={len(refs)}"
        )
        for ordinal,idx in enumerate(refs[:MAX_XREFS],1):
            start,end,confidence=likely_function_window(instructions,idx)
            calls=collections.Counter()
            for ins in instructions[start:end+1]:
                imp=imported_call(ins,imports)
                if imp:
                    calls[imp]+=1
            interesting=[
                (dll,name,count) for (dll,name),count in calls.items()
                if name in ALL_INTERESTING
            ]
            directs=direct_call_targets(instructions,start,end,base)
            # Keep only internal .text direct calls as graph fingerprints.
            text_lo=base+text_sec["rva"]
            text_hi=text_lo+text_sec["raw_size"]
            internal=[(addr,count) for addr,count in directs.items() if text_lo<=addr<text_hi]
            internal.sort()
            x=instructions[idx]
            print(
                f"XREF|text={clean(row['text'])}|n={ordinal}|xref_rva=0x{x.address-base:x}|"
                f"function_start_rva=0x{instructions[start].address-base:x}|"
                f"function_end_rva=0x{instructions[end].address-base:x}|boundary={confidence}|"
                f"instruction_count={end-start+1}|import_calls={sum(calls.values())}|"
                f"interesting_calls={len(interesting)}|internal_call_targets={len(internal)}"
            )
            for dll,name,count in sorted(interesting,key=lambda x:(x[0].lower(),x[1].lower())):
                print(
                    f"XREF_API|text={clean(row['text'])}|xref_rva=0x{x.address-base:x}|"
                    f"dll={clean(dll)}|api={clean(name)}|calls={count}"
                )
            for addr,count in internal[:80]:
                print(
                    f"XREF_CALL|text={clean(row['text'])}|xref_rva=0x{x.address-base:x}|"
                    f"target_rva=0x{addr-base:x}|calls={count}"
                )


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--bin",required=True)
    args=ap.parse_args()

    print("StoneAge Taiwan v1.0 map-cache binary relation probe — R1")
    print("SCOPE|ephemeral-verified-disc|derived-xref-callgraph-only|no-disassembly-or-payload-commit")

    img,rows,layout,joliet=find_rows(args.bin)
    td=tempfile.TemporaryDirectory()
    root=Path(td.name)
    try:
        by={r["path"]:r for r in rows if not r["is_dir"]}
        target="StoneAge/sa_3.exe"
        if target not in by:
            raise SystemExit("sa_3.exe missing")
        out=root/"sa_3.exe"
        extract_row(img,by[target],out)
        print(f"FILESYSTEM|layout={layout}|joliet={int(joliet)}|runtime_bytes={out.stat().st_size}")
        data,pe,base,sections,imports=image_layout(out)
        emit_xref_neighborhoods(data,base,sections,imports)
    finally:
        img.close(); td.cleanup()


if __name__=="__main__":
    main()
