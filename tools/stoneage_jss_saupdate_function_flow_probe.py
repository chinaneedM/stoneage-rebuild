#!/usr/bin/env python3
"""Function-bounded semantic flow probe for the archived JSS SaUpdate executable.

The probe transiently fetches the already-hash-pinned first-party executable,
locates exact code references to updater strings, recovers the containing
function heuristically, and emits only derived function/string/call summaries.
No disassembly text or executable bytes are retained.
"""

from __future__ import annotations

import collections
import hashlib
import re
import struct

from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from capstone.x86 import X86_OP_IMM

from tools.stoneage_jss_launcher_archive_probe import ORIGINAL, get_bounded, replay_url
from tools.stoneage_jss_launcher_deep_probe import KNOWN_SHA256, TIMESTAMP, parse_pe_layout
from tools.stoneage_jss_saupdate_xref_probe import (
    TARGET_STRINGS,
    find_string_locations,
    parse_imports,
    rva_to_offset,
)
from tools.stoneage_jss_saupdate_http_flow_probe import (
    MFC_NETWORK_ORDINALS,
    import_thunks,
)
from tools.stoneage_tw10_mapcache_binary_probe import (
    imported_call,
    likely_function_window,
    referenced_absolute_values,
)
from tools.stoneage_tw10_technical_probe import pe_sections

ASCII_RE=re.compile(rb"[\x20-\x7e]{2,}")
MAX_STRINGS_PER_FUNCTION=80
MAX_CALLS_PER_FUNCTION=120

# Exact internal E8 targets observed in the recovered SaUpdate binary.
# Labels are analytical roles to be tested, not original source symbols.
SEEDED_FUNCTION_RVAS=(
    ("dialog-init",0x1270),
    ("manifest-control",0x13F0),
    ("resource-generation-scan",0x25D0),
    ("manifest-wrapper",0x2880),
    ("post-download-state",0x3610),
    ("update-state-sequence",0x3C60),
    ("launch-tail",0x3F20),
)

# Probe instructions known from the import-call map; function_summary walks
# backward to the nearest old-MSVC prologue and forward to return.
PARSER_SITE_RVAS=(
    ("fgets-3798",0x3798),
    ("fgets-3903",0x3903),
    ("fgets-3a34",0x3A34),
    ("fgets-3c15",0x3C15),
)

MFC_EXTRA_ORDINALS={
    537:"CString::CString(char const*)",
    690:"CInternetSession::~CInternetSession",
    800:"CString::~CString",
    825:"operator delete",
    1199:"AfxMessageBox",
    1247:"AfxSocketInit",
    1988:"CInternetSession::Close",
    2379:"CWnd::Default",
    2642:"CWnd::EnableWindow",
    3092:"CWnd::GetDlgItem",
}
MFC_NAMES={**MFC_EXTRA_ORDINALS,**MFC_NETWORK_ORDINALS}


def clean(value,limit=1200):
    s=" ".join(str(value if value is not None else "").split())
    return "".join(c for c in s if c>=" " and c!="\x7f").replace("|","%7C")[:limit]


def file_offset_to_rva(layout,off):
    for sec in layout["sections"]:
        if sec["raw_ptr"]<=off<sec["raw_ptr"]+sec["raw_size"]:
            return sec["vaddr"]+(off-sec["raw_ptr"])
    return None


def ascii_strings(data,layout,image_base):
    """Map exact string-start VA -> text for raw PE sections."""
    out={}
    for sec in layout["sections"]:
        if sec["chars"] & 0x20000000:
            continue
        start=sec["raw_ptr"]
        end=min(len(data),start+sec["raw_size"])
        blob=data[start:end]
        for m in ASCII_RE.finditer(blob):
            raw=m.group()
            try:text=raw.decode("ascii")
            except Exception:continue
            if not text or len(text)>700:
                continue
            off=start+m.start()
            rva=file_offset_to_rva(layout,off)
            if rva is not None:
                out[image_base+rva]=text
    return out


def text_section(layout):
    sec=next((s for s in layout["sections"] if s["name"]==".text"),None)
    if sec is None:
        raise ValueError("no .text")
    return sec


def disassemble_text(data,layout,image_base):
    sec=text_section(layout)
    start=sec["raw_ptr"]; end=min(len(data),start+sec["raw_size"])
    md=Cs(CS_ARCH_X86,CS_MODE_32); md.detail=True
    return sec,list(md.disasm(data[start:end],image_base+sec["vaddr"]))


def raw_pointer_hits(data,layout,image_base,target_rva):
    sec=text_section(layout)
    start=sec["raw_ptr"]; end=min(len(data),start+sec["raw_size"])
    blob=data[start:end]
    needle=struct.pack("<I",(image_base+target_rva)&0xffffffff)
    hits=[]
    pos=0
    while True:
        rel=blob.find(needle,pos)
        if rel<0:break
        hits.append(start+rel)
        pos=rel+1
    return tuple(hits)


def recover_xref_instruction(data,layout,image_base,target_rva,ptr_file_off):
    target_va=image_base+target_rva
    md=Cs(CS_ARCH_X86,CS_MODE_32); md.detail=True
    for back in range(0,16):
        off=ptr_file_off-back
        if off<0:continue
        rva=file_offset_to_rva(layout,off)
        if rva is None:continue
        blob=data[off:min(len(data),off+24)]
        insns=list(md.disasm(blob,image_base+rva,count=1))
        if not insns:continue
        ins=insns[0]
        if not (off<=ptr_file_off and ptr_file_off+4<=off+ins.size):
            continue
        if target_va not in set(referenced_absolute_values(ins)):
            continue
        return ins
    return None


def mapped_import(dll,name):
    if dll.lower()=="mfc42.dll" and name.startswith("ordinal:"):
        try:n=int(name.split(":",1)[1])
        except Exception:return name
        return MFC_NAMES.get(n,name)
    return name


def resolve_call(ins,image_base,imports,thunks):
    imp=imported_call(ins,imports)
    if imp:
        return ("import",imp[0],mapped_import(*imp))
    if ins.mnemonic!="call":
        return None
    for op in ins.operands:
        if op.type!=X86_OP_IMM:
            continue
        target=int(op.imm)&0xffffffff
        rva=target-image_base
        if rva in thunks:
            dll,name=thunks[rva]
            return ("import",dll,mapped_import(dll,name))
        return ("internal","",f"0x{rva:x}")
    return ("indirect","","")


def target_xrefs(data,layout,image_base):
    rows=[]
    for token in TARGET_STRINGS:
        label=token.decode("ascii","replace")
        for _,rva in find_string_locations(data,layout,token):
            for ptr_off in raw_pointer_hits(data,layout,image_base,rva):
                ins=recover_xref_instruction(data,layout,image_base,rva,ptr_off)
                if ins is not None:
                    rows.append((label,rva,ins.address))
    return tuple(sorted(set(rows),key=lambda x:(x[2],x[0])))


def function_summary(instructions,idx,image_base,imports,thunks,string_map):
    start,end,boundary=likely_function_window(instructions,idx)
    strings=[]
    calls=[]
    seen_strings=set()
    for ins in instructions[start:end+1]:
        for va in referenced_absolute_values(ins):
            text=string_map.get(va)
            if text is not None and (va,text) not in seen_strings:
                seen_strings.add((va,text))
                strings.append((ins.address-image_base,va-image_base,text))
        call=resolve_call(ins,image_base,imports,thunks)
        if call is not None:
            calls.append((ins.address-image_base,*call))
    return {
        "start_idx":start,"end_idx":end,
        "start_rva":instructions[start].address-image_base,
        "end_rva":instructions[end].address-image_base,
        "boundary":boundary,
        "instructions":end-start+1,
        "strings":tuple(strings[:MAX_STRINGS_PER_FUNCTION]),
        "calls":tuple(calls[:MAX_CALLS_PER_FUNCTION]),
        "string_total":len(strings),
        "call_total":len(calls),
    }


def main():
    print("StoneAge JSS SaUpdate function-flow probe — R1")
    print("SCOPE|exact-string-xrefs+heuristic-function-boundaries+call-and-string-sequence|derived-only|no-disassembly-retained")

    status,final,headers,data=get_bounded(
        replay_url({"timestamp":TIMESTAMP,"original":ORIGINAL}),timeout=20
    )
    sha=hashlib.sha256(data).hexdigest()
    print(f"FETCH|status={status}|bytes={len(data)}|sha256={sha}|final={clean(final)}")
    if sha!=KNOWN_SHA256:
        print(f"RESOLUTION|HASH_MISMATCH|expected={KNOWN_SHA256}")
        return

    layout=parse_pe_layout(data)
    pe=pe_sections(data)
    image_base=pe["image_base"]
    imports=parse_imports(data,layout,image_base)
    thunks=import_thunks(data,layout,imports)
    sec,instructions=disassemble_text(data,layout,image_base)
    by_addr={ins.address:i for i,ins in enumerate(instructions)}
    strings=ascii_strings(data,layout,image_base)
    xrefs=target_xrefs(data,layout,image_base)

    print(
        f"PE|image_base=0x{image_base:x}|text_rva=0x{sec['vaddr']:x}|"
        f"text_bytes={sec['raw_size']}|instructions={len(instructions)}|"
        f"imports={len(imports)}|thunks={len(thunks)}|ascii_strings={len(strings)}"
    )
    print(f"COUNT|decoded_target_xrefs|{len(xrefs)}")

    functions={}
    anchors=collections.defaultdict(list)
    for label,string_rva,addr in xrefs:
        idx=by_addr.get(addr)
        if idx is None:
            continue
        summary=function_summary(instructions,idx,image_base,imports,thunks,strings)
        key=summary["start_rva"]
        functions.setdefault(key,summary)
        anchors[key].append((label,string_rva,addr-image_base))

    print(f"COUNT|anchor_functions|{len(functions)}")
    for start_rva in sorted(functions):
        f=functions[start_rva]
        a=anchors[start_rva]
        print(
            f"FUNCTION|start_rva=0x{f['start_rva']:x}|end_rva=0x{f['end_rva']:x}|"
            f"boundary={f['boundary']}|instructions={f['instructions']}|"
            f"anchors={len(a)}|strings={f['string_total']}|calls={f['call_total']}"
        )
        for label,string_rva,xref_rva in sorted(a,key=lambda x:x[2]):
            print(
                f"ANCHOR|function_rva=0x{start_rva:x}|xref_rva=0x{xref_rva:x}|"
                f"string_rva=0x{string_rva:x}|text={clean(label)}"
            )
        for order,(ins_rva,string_rva,text_value) in enumerate(f["strings"],1):
            print(
                f"STRING_REF|function_rva=0x{start_rva:x}|order={order}|"
                f"ins_rva=0x{ins_rva:x}|string_rva=0x{string_rva:x}|text={clean(text_value)}"
            )
        for order,(call_rva,kind,dll,name) in enumerate(f["calls"],1):
            print(
                f"CALL|function_rva=0x{start_rva:x}|order={order}|call_rva=0x{call_rva:x}|"
                f"kind={kind}|dll={clean(dll)}|target={clean(name)}"
            )

    # Inspect selected exact local call targets independently of string anchoring.
    for role,rva in SEEDED_FUNCTION_RVAS:
        idx=by_addr.get(image_base+rva)
        if idx is None:
            print(f"SEEDED_FUNCTION|role={role}|rva=0x{rva:x}|decoded=0")
            continue
        f=function_summary(instructions,idx,image_base,imports,thunks,strings)
        print(
            f"SEEDED_FUNCTION|role={role}|rva=0x{rva:x}|decoded=1|"
            f"start_rva=0x{f['start_rva']:x}|end_rva=0x{f['end_rva']:x}|"
            f"boundary={f['boundary']}|instructions={f['instructions']}|"
            f"strings={f['string_total']}|calls={f['call_total']}"
        )
        for order,(ins_rva,string_rva,text_value) in enumerate(f["strings"],1):
            print(
                f"SEEDED_STRING|role={role}|order={order}|ins_rva=0x{ins_rva:x}|"
                f"string_rva=0x{string_rva:x}|text={clean(text_value)}"
            )
        for order,(call_rva,kind,dll,name) in enumerate(f["calls"],1):
            print(
                f"SEEDED_CALL|role={role}|order={order}|call_rva=0x{call_rva:x}|"
                f"kind={kind}|dll={clean(dll)}|target={clean(name)}"
            )

    # Recover containing functions for parser-like stdio call sites.
    parser_functions={}
    for role,rva in PARSER_SITE_RVAS:
        idx=by_addr.get(image_base+rva)
        if idx is None:
            print(f"PARSER_SITE|role={role}|rva=0x{rva:x}|decoded=0")
            continue
        f=function_summary(instructions,idx,image_base,imports,thunks,strings)
        parser_functions.setdefault(f["start_rva"],f)
        print(
            f"PARSER_SITE|role={role}|rva=0x{rva:x}|decoded=1|"
            f"function_start_rva=0x{f['start_rva']:x}|function_end_rva=0x{f['end_rva']:x}|"
            f"boundary={f['boundary']}|strings={f['string_total']}|calls={f['call_total']}"
        )
    for start_rva in sorted(parser_functions):
        f=parser_functions[start_rva]
        print(
            f"PARSER_FUNCTION|start_rva=0x{f['start_rva']:x}|end_rva=0x{f['end_rva']:x}|"
            f"boundary={f['boundary']}|instructions={f['instructions']}|"
            f"strings={f['string_total']}|calls={f['call_total']}"
        )
        for order,(ins_rva,string_rva,text_value) in enumerate(f["strings"],1):
            print(
                f"PARSER_STRING|function_rva=0x{start_rva:x}|order={order}|"
                f"ins_rva=0x{ins_rva:x}|string_rva=0x{string_rva:x}|text={clean(text_value)}"
            )
        for order,(call_rva,kind,dll,name) in enumerate(f["calls"],1):
            print(
                f"PARSER_CALL|function_rva=0x{start_rva:x}|order={order}|call_rva=0x{call_rva:x}|"
                f"kind={kind}|dll={clean(dll)}|target={clean(name)}"
            )

    # Summarize which anchor functions share concrete import calls.
    api_functions=collections.defaultdict(set)
    for start_rva,f in functions.items():
        for _,kind,dll,name in f["calls"]:
            if kind=="import":
                api_functions[(dll,name)].add(start_rva)
    for (dll,name),starts in sorted(api_functions.items(),key=lambda x:(x[0][0].lower(),x[0][1].lower())):
        print(
            f"API_FUNCTIONS|dll={clean(dll)}|target={clean(name)}|"
            f"functions={','.join(f'0x{x:x}' for x in sorted(starts))}"
        )

    print(
        "RESOLUTION|FUNCTION_FLOW_DERIVED|"
        f"target_xrefs={len(xrefs)}|functions={len(functions)}|binary-not-committed"
    )


if __name__=="__main__":
    main()
