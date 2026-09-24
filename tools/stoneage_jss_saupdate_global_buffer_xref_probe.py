#!/usr/bin/env python3
"""Trace exact global-buffer references in archived JSS SaUpdate.

Purpose: trace selected static strings/global buffers in the archived launcher,
including the two unnamed _execl buffers and the download-folder notice strings.
Derived metadata only; no executable bytes or disassembly text are retained.
"""

from __future__ import annotations

import hashlib
import struct

from tools.stoneage_jss_launcher_archive_probe import ORIGINAL, get_bounded, replay_url
from tools.stoneage_jss_launcher_deep_probe import KNOWN_SHA256, TIMESTAMP, parse_pe_layout
from tools.stoneage_jss_saupdate_xref_probe import parse_imports
from tools.stoneage_jss_saupdate_http_flow_probe import import_thunks
from tools.stoneage_jss_saupdate_function_flow_probe import (
    ascii_strings,
    disassemble_text,
    raw_pointer_hits,
    recover_xref_instruction,
    resolve_call,
    function_summary,
)
from tools.stoneage_tw10_mapcache_binary_probe import referenced_absolute_values
from tools.stoneage_tw10_technical_probe import pe_sections

TARGETS=(
    (0x4070C0,"download-folder-created-message"),
    (0x4070E8,"notice-caption"),
    (0x85E6FC,"sa-executable-buffer"),
    (0x85E2FC,"realbin-state-buffer"),
    (0x85DEFC,"soundbin-state-buffer"),
    (0x85D6FC,"adrnbin-state-buffer"),
    (0x85D2FC,"sprbin-state-buffer"),
    (0x85CEFC,"spradrnbin-state-buffer"),
    (0x85CAFC,"battlebin-state-buffer"),
    (0x85C2FC,"unknown-launch-buffer-1"),
    (0x85BEFC,"unknown-launch-buffer-2"),
)
NEAR=28
NEXT_CALL=18


def clean(v,limit=1000):
    s=" ".join(str(v if v is not None else "").split())
    return "".join(c for c in s if c>=" " and c!="\x7f").replace("|","%7C")[:limit]


def va_to_offset(layout,image_base,va):
    rva=va-image_base
    for sec in layout["sections"]:
        span=max(sec["vsize"],sec["raw_size"])
        if sec["vaddr"]<=rva<sec["vaddr"]+span:
            rel=rva-sec["vaddr"]
            if rel>=sec["raw_size"]:
                return None,sec["name"]
            return sec["raw_ptr"]+rel,sec["name"]
    return None,""


def ascii_at(data,off,limit=256):
    if off is None or off<0 or off>=len(data):
        return ""
    end=data.find(b"\0",off,min(len(data),off+limit))
    if end<0:
        end=min(len(data),off+limit)
    raw=data[off:end]
    if not raw or any(b<0x20 or b>0x7e for b in raw):
        return ""
    return raw.decode("ascii","replace")


def shift_jis_at(data,off,limit=512):
    if off is None or off<0 or off>=len(data):
        return ""
    end=data.find(b"\0",off,min(len(data),off+limit))
    if end<0:
        end=min(len(data),off+limit)
    raw=data[off:end]
    try:
        return raw.decode("shift_jis")
    except UnicodeDecodeError:
        return ""


def xref_role(ins,target_va):
    if not ins.operands:
        return "unknown"
    if ins.mnemonic=="push":
        return "pointer-pass"
    if ins.mnemonic=="lea":
        return "address-load"
    if ins.mnemonic=="mov":
        # We deliberately do not claim read/write without full alias analysis.
        return "move-reference"
    return "reference"


def nearby_strings(instructions,idx,string_map,image_base):
    out=[]; seen=set()
    lo=max(0,idx-NEAR); hi=min(len(instructions),idx+NEAR+1)
    for j in range(lo,hi):
        ins=instructions[j]
        for va in referenced_absolute_values(ins):
            text=string_map.get(va)
            if text is not None and (ins.address-image_base,text) not in seen:
                seen.add((ins.address-image_base,text))
                out.append((ins.address-image_base,text))
    return tuple(out)


def next_call(instructions,idx,image_base,imports,thunks):
    for j in range(idx+1,min(len(instructions),idx+NEXT_CALL+1)):
        ins=instructions[j]
        call=resolve_call(ins,image_base,imports,thunks)
        if call is not None:
            return (ins.address-image_base,*call)
        if ins.mnemonic.startswith("ret"):
            break
    return None


def main():
    print("StoneAge JSS SaUpdate global-buffer xref probe — R1")
    print("SCOPE|exact-global-pointer-xrefs+nearby-strings+next-call|derived-only|no-disassembly-retained")

    status,final,headers,data=get_bounded(
        replay_url({"timestamp":TIMESTAMP,"original":ORIGINAL}),timeout=20
    )
    sha=hashlib.sha256(data).hexdigest()
    print(f"FETCH|status={status}|bytes={len(data)}|sha256={sha}|final={clean(final)}")
    if sha!=KNOWN_SHA256:
        print(f"RESOLUTION|HASH_MISMATCH|expected={KNOWN_SHA256}")
        return

    layout=parse_pe_layout(data)
    pe=pe_sections(data); image_base=pe["image_base"]
    imports=parse_imports(data,layout,image_base)
    thunks=import_thunks(data,layout,imports)
    sec,instructions=disassemble_text(data,layout,image_base)
    by_addr={ins.address:i for i,ins in enumerate(instructions)}
    strings=ascii_strings(data,layout,image_base)

    total=0
    unknown_function_indexes=[]
    for target_va,label in TARGETS:
        target_rva=target_va-image_base
        rows=[]
        for ptr_off in raw_pointer_hits(data,layout,image_base,target_rva):
            ins=recover_xref_instruction(data,layout,image_base,target_rva,ptr_off)
            if ins is None:
                continue
            idx=by_addr.get(ins.address)
            if idx is None:
                continue
            rows.append((ins,idx))
            if label.startswith("unknown-launch-buffer-"):
                unknown_function_indexes.append((label,idx))
        rows=sorted({(ins.address,idx):(ins,idx) for ins,idx in rows}.values(),key=lambda x:x[0].address)
        total+=len(rows)
        print(f"BUFFER|label={label}|va=0x{target_va:x}|xrefs={len(rows)}")
        if label in {"download-folder-created-message","notice-caption"}:
            off,section=va_to_offset(layout,image_base,target_va)
            text_value=shift_jis_at(data,off)
            print(
                f"STATIC_TEXT|label={label}|section={clean(section)}|"
                f"encoding=shift_jis|text={clean(text_value)}"
            )
        for ins,idx in rows:
            near=nearby_strings(instructions,idx,strings,image_base)
            call=next_call(instructions,idx,image_base,imports,thunks)
            print(
                f"XREF|label={label}|rva=0x{ins.address-image_base:x}|"
                f"mnemonic={clean(ins.mnemonic)}|role={xref_role(ins,target_va)}|"
                f"nearby_strings={len(near)}|next_call={int(call is not None)}"
            )
            for order,(rva,text) in enumerate(near,1):
                print(
                    f"NEAR_STRING|label={label}|xref_rva=0x{ins.address-image_base:x}|"
                    f"order={order}|ins_rva=0x{rva:x}|text={clean(text)}"
                )
            if call is not None:
                call_rva,kind,dll,name=call
                print(
                    f"NEXT_CALL|label={label}|xref_rva=0x{ins.address-image_base:x}|"
                    f"call_rva=0x{call_rva:x}|kind={kind}|dll={clean(dll)}|target={clean(name)}"
                )

    # Function-level context for the two unknown launch buffers.
    emitted=set()
    for label,idx in unknown_function_indexes:
        f=function_summary(instructions,idx,image_base,imports,thunks,strings)
        key=(f["start_rva"],f["end_rva"])
        if key in emitted:
            continue
        emitted.add(key)
        print(
            f"UNKNOWN_FUNCTION|start_rva=0x{f['start_rva']:x}|end_rva=0x{f['end_rva']:x}|"
            f"boundary={f['boundary']}|instructions={f['instructions']}|"
            f"strings={f['string_total']}|calls={f['call_total']}"
        )
        for order,(ins_rva,string_rva,text_value) in enumerate(f["strings"],1):
            print(
                f"UNKNOWN_STRING|function_rva=0x{f['start_rva']:x}|order={order}|"
                f"ins_rva=0x{ins_rva:x}|text={clean(text_value)}"
            )
        for order,(call_rva,kind,dll,name) in enumerate(f["calls"],1):
            print(
                f"UNKNOWN_CALL|function_rva=0x{f['start_rva']:x}|order={order}|"
                f"call_rva=0x{call_rva:x}|kind={kind}|dll={clean(dll)}|target={clean(name)}"
            )

    print(
        f"RESOLUTION|GLOBAL_BUFFER_XREFS_DERIVED|targets={len(TARGETS)}|xrefs={total}|"
        f"unknown_functions={len(emitted)}|binary-not-committed"
    )


if __name__=="__main__":
    main()
