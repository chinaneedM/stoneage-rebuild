#!/usr/bin/env python3
"""Resolve JSS SaUpdate text-resource generations vs final launch control parameters.

This probe is intentionally narrow:
- selector 7 / 9 callers into the generation scanner;
- the two previously unnamed _execl buffers;
- MFC42 ordinal 6199 at the IP/MESSAGE control block.

Only derived addresses, argument sources, strings and relationship summaries are
retained. The hash-pinned executable is fetched transiently and never committed.
"""

from __future__ import annotations

import hashlib

from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_REG_INVALID

from tools.stoneage_jss_launcher_archive_probe import ORIGINAL, get_bounded, replay_url
from tools.stoneage_jss_launcher_deep_probe import KNOWN_SHA256, TIMESTAMP, parse_pe_layout
from tools.stoneage_jss_saupdate_xref_probe import parse_imports
from tools.stoneage_jss_saupdate_http_flow_probe import import_thunks, import_call_sites
from tools.stoneage_jss_saupdate_function_flow_probe import (
    ascii_strings,
    disassemble_text,
    function_summary,
    raw_pointer_hits,
    recover_xref_instruction,
    resolve_call,
)
from tools.stoneage_jss_saupdate_call_args_probe import (
    stack_args,
    nearby_strings,
)
from tools.stoneage_tw10_mapcache_binary_probe import referenced_absolute_values
from tools.stoneage_tw10_technical_probe import pe_sections

MFC42_DEF_SOURCE="isledecomp/MSVC600-8168:VC98/MFC/SRC/PLATFORM/MFC42.DEF"
MFC42_DEF_BLOB_SHA="3fb0685b8c2fe98932d3442d4fa0f9da8d69ccec"
MFC42_ORDINAL_6199="CWnd::SetWindowTextA"

SELECTOR_SITES=(
    (0x176D,7,"soundaddr"),
    (0x17F4,9,"battletxt"),
)

UNKNOWN_BUFFERS=(
    (0x85C2FC,"launch-control-buffer-1"),
    (0x85BEFC,"launch-control-buffer-2"),
)

KNOWN_STATE_BUFFERS=(
    (0x85E2FC,"realbin"),
    (0x85DEFC,"soundbin"),
    (0x85D6FC,"adrnbin"),
    (0x85D2FC,"sprbin"),
    (0x85CEFC,"spradrnbin"),
    (0x85CAFC,"battlebin"),
)

FOCUS_CALLS=(
    (0x1F14,"set-window-text"),
    (0x1F48,"ip-message-followup"),
    (0x3F00,"execl-launch"),
)


def clean(v,limit=1200):
    s=" ".join(str(v if v is not None else "").split())
    return "".join(c for c in s if c>=" " and c!="\x7f").replace("|","%7C")[:limit]


def image_base(data):
    return pe_sections(data)["image_base"]


def operand_relation(ins,target_va):
    """Classify how an exact target address appears, without alias speculation."""
    matches=[]
    for idx,op in enumerate(ins.operands):
        if op.type==X86_OP_IMM and (int(op.imm)&0xffffffff)==target_va:
            matches.append((idx,"address-immediate"))
        elif op.type==X86_OP_MEM:
            m=op.mem
            if m.base==X86_REG_INVALID and m.index==X86_REG_INVALID and (int(m.disp)&0xffffffff)==target_va:
                if ins.mnemonic=="mov" and idx==0:
                    role="absolute-memory-write"
                elif ins.mnemonic=="mov":
                    role="absolute-memory-read"
                else:
                    role="absolute-memory-reference"
                matches.append((idx,role))
    return tuple(matches)


def exact_global_xrefs(data,layout,base,target_va):
    target_rva=target_va-base
    rows=[]
    for ptr_off in raw_pointer_hits(data,layout,base,target_rva):
        ins=recover_xref_instruction(data,layout,base,target_rva,ptr_off)
        if ins is None:
            continue
        rows.append((ins,operand_relation(ins,target_va)))
    dedup={}
    for ins,relations in rows:
        dedup[ins.address]=(ins,relations)
    return tuple(dedup[k] for k in sorted(dedup))


def function_contains(f,rva):
    return f["start_rva"]<=rva<=f["end_rva"]


def target_refs_in_function(instructions,f,targets,base):
    out=[]
    for ins in instructions[f["start_idx"]:f["end_idx"]+1]:
        refs=set(referenced_absolute_values(ins))
        for va,label in targets:
            if va in refs:
                out.append((ins.address-base,va,label))
    return tuple(out)


def mapped_identity(call_rva, imported):
    for site,dll,name,mode in imported:
        if site!=call_rva:
            continue
        if dll.lower()=="mfc42.dll" and name=="ordinal:6199":
            return f"{dll}!{MFC42_ORDINAL_6199}"
        return f"{dll}!{name}"
    return "internal-or-indirect"


def main():
    print("StoneAge JSS SaUpdate launch-parameter semantics probe — R1")
    print("SCOPE|selector7+selector9+launch-control-buffers+SetWindowTextA|derived-only|binary-not-committed")
    print(f"MFC42_DEF|source={MFC42_DEF_SOURCE}|blob_sha={MFC42_DEF_BLOB_SHA}|ordinal_6199={MFC42_ORDINAL_6199}")

    status,final,headers,data=get_bounded(
        replay_url({"timestamp":TIMESTAMP,"original":ORIGINAL}),timeout=20
    )
    sha=hashlib.sha256(data).hexdigest()
    print(f"FETCH|status={status}|bytes={len(data)}|sha256={sha}|final={clean(final)}")
    if sha!=KNOWN_SHA256:
        print(f"RESOLUTION|HASH_MISMATCH|expected={KNOWN_SHA256}")
        return

    layout=parse_pe_layout(data)
    base=image_base(data)
    iat=parse_imports(data,layout,base)
    thunks=import_thunks(data,layout,iat)
    imported=import_call_sites(data,layout,iat,thunks)
    sec,instructions=disassemble_text(data,layout,base)
    by_rva={ins.address-base:i for i,ins in enumerate(instructions)}
    strings=ascii_strings(data,layout,base)

    print(f"PE|image_base=0x{base:x}|instructions={len(instructions)}|strings={len(strings)}|imports={len(iat)}")

    selector_functions=[]
    all_targets=UNKNOWN_BUFFERS+KNOWN_STATE_BUFFERS
    for call_rva,selector,label in SELECTOR_SITES:
        idx=by_rva.get(call_rva)
        if idx is None:
            print(f"SELECTOR_SITE|label={label}|rva=0x{call_rva:x}|decoded=0")
            continue
        args=stack_args(instructions,idx,strings)
        f=function_summary(instructions,idx,base,iat,thunks,strings)
        selector_functions.append((label,selector,f))
        refs=target_refs_in_function(instructions,f,all_targets,base)
        print(
            f"SELECTOR_SITE|label={label}|selector={selector}|rva=0x{call_rva:x}|decoded=1|"
            f"function_start=0x{f['start_rva']:x}|function_end=0x{f['end_rva']:x}|"
            f"strings={f['string_total']}|calls={f['call_total']}|state_buffer_refs={len(refs)}"
        )
        for n,(addr,src) in enumerate(args,1):
            print(f"SELECTOR_ARG|label={label}|index={n}|push_rva=0x{addr-base:x}|source={clean(src)}")
        for order,(ins_rva,string_rva,text_value) in enumerate(f["strings"],1):
            if any(k in text_value.lower() for k in ("soundaddr","battletxt","ip:","message","data\\")):
                print(
                    f"SELECTOR_STRING|label={label}|order={order}|ins_rva=0x{ins_rva:x}|"
                    f"text={clean(text_value)}"
                )
        for ins_rva,va,target_label in refs:
            print(
                f"SELECTOR_BUFFER_REF|label={label}|ins_rva=0x{ins_rva:x}|"
                f"target={target_label}|va=0x{va:x}"
            )

    unknown_xref_total=0
    for target_va,label in UNKNOWN_BUFFERS:
        rows=exact_global_xrefs(data,layout,base,target_va)
        unknown_xref_total+=len(rows)
        print(f"CONTROL_BUFFER|label={label}|va=0x{target_va:x}|xrefs={len(rows)}")
        for ins,relations in rows:
            idx=by_rva.get(ins.address-base)
            near=nearby_strings(instructions,idx,strings,base,back=40) if idx is not None else ()
            relation=",".join(f"{op}:{role}" for op,role in relations) or "unclassified"
            call=resolve_call(ins,base,iat,thunks)
            print(
                f"CONTROL_XREF|label={label}|rva=0x{ins.address-base:x}|"
                f"mnemonic={clean(ins.mnemonic)}|relation={clean(relation)}|"
                f"resolved_call={clean(call if call is not None else '')}|nearby_strings={len(near)}"
            )
            for order,(nrva,text_value) in enumerate(near,1):
                if any(k in text_value.lower() for k in ("ip:","message","updated","bin:%d")):
                    print(
                        f"CONTROL_NEAR_STRING|label={label}|xref_rva=0x{ins.address-base:x}|"
                        f"order={order}|ins_rva=0x{nrva:x}|text={clean(text_value)}"
                    )

    for call_rva,label in FOCUS_CALLS:
        idx=by_rva.get(call_rva)
        if idx is None:
            print(f"FOCUS_CALL|label={label}|rva=0x{call_rva:x}|decoded=0")
            continue
        args=stack_args(instructions,idx,strings)
        near=nearby_strings(instructions,idx,strings,base,back=48)
        print(
            f"FOCUS_CALL|label={label}|rva=0x{call_rva:x}|decoded=1|"
            f"identity={clean(mapped_identity(call_rva,imported))}|stack_args={len(args)}|nearby_strings={len(near)}"
        )
        for n,(addr,src) in enumerate(args,1):
            print(f"FOCUS_ARG|label={label}|index={n}|push_rva=0x{addr-base:x}|source={clean(src)}")
        for order,(nrva,text_value) in enumerate(near,1):
            if any(k in text_value.lower() for k in ("ip:","message","updated","bin:%d")):
                print(
                    f"FOCUS_STRING|label={label}|order={order}|ins_rva=0x{nrva:x}|text={clean(text_value)}"
                )

    selector_unknown_overlap=0
    for label,selector,f in selector_functions:
        refs=target_refs_in_function(instructions,f,UNKNOWN_BUFFERS,base)
        selector_unknown_overlap+=len(refs)
        print(
            f"SEPARATION_CHECK|selector={selector}|label={label}|"
            f"unknown_launch_buffer_refs={len(refs)}"
        )

    print(
        "RESOLUTION|LAUNCH_PARAMETER_RELATIONSHIPS_DERIVED|"
        f"selector_functions={len(selector_functions)}|unknown_buffer_xrefs={unknown_xref_total}|"
        f"selector_unknown_overlap={selector_unknown_overlap}|binary-not-committed"
    )


if __name__=="__main__":
    main()
