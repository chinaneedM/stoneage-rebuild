#!/usr/bin/env python3
"""Trace the five dword members of each JSS SaUpdate manifest resource record.

Each resource record is 0x114 bytes: a 0x100-byte text/name area followed by
five dwords. This probe emits only normalized references to those members and
small normalized contexts from hash-pinned first-party bytes.
"""

from __future__ import annotations

import hashlib

from capstone.x86 import X86_OP_MEM, X86_REG_EBP, X86_REG_ESP, X86_REG_INVALID

from tools.stoneage_jss_launcher_archive_probe import ORIGINAL, get_bounded, replay_url
from tools.stoneage_jss_launcher_deep_probe import KNOWN_SHA256, TIMESTAMP, parse_pe_layout
from tools.stoneage_jss_saupdate_function_flow_probe import ascii_strings, disassemble_text
from tools.stoneage_jss_saupdate_manifest_record_probe import abstract
from tools.stoneage_tw10_technical_probe import pe_sections

MEMBERS=(
    ("selector",0x100),
    ("field4-checksum",0x104),
    ("field3",0x108),
    ("filename-generation",0x10C),
    ("runtime-flag",0x110),
    ("filename-from-meta",-0x100),
)
RVA_MIN=0x1900
RVA_MAX=0x3600
CONTEXT=10


def clean(value,limit=900):
    s=" ".join(str(value if value is not None else "").split())
    return "".join(c for c in s if c>=" " and c!="\x7f").replace("|","%7C")[:limit]


def matching_member(ins):
    out=[]
    for op in ins.operands:
        if op.type!=X86_OP_MEM:
            continue
        m=op.mem
        if m.base in (X86_REG_INVALID,X86_REG_EBP,X86_REG_ESP):
            continue
        disp=int(m.disp)
        for role,wanted in MEMBERS:
            if disp==wanted:
                out.append((role,disp,ins.reg_name(m.base),ins.reg_name(m.index) if m.index!=X86_REG_INVALID else "",m.scale))
    return out


def main():
    print("StoneAge JSS SaUpdate manifest record-layout probe — R1")
    print("SCOPE|record-member-xrefs+normalized-context|derived-only|no-bytes-no-raw-disassembly")
    status,final,headers,data=get_bounded(
        replay_url({"timestamp":TIMESTAMP,"original":ORIGINAL}),timeout=20
    )
    sha=hashlib.sha256(data).hexdigest()
    print(f"FETCH|status={status}|bytes={len(data)}|sha256={sha}|final={clean(final)}")
    if sha!=KNOWN_SHA256:
        print(f"RESOLUTION|HASH_MISMATCH|expected={KNOWN_SHA256}")
        return

    layout=parse_pe_layout(data)
    base=pe_sections(data)["image_base"]
    sec,insns=disassemble_text(data,layout,base)
    strings=ascii_strings(data,layout,base)

    counts={role:0 for role,_ in MEMBERS}
    for i,ins in enumerate(insns):
        rva=ins.address-base
        if not (RVA_MIN<=rva<=RVA_MAX):
            continue
        matches=matching_member(ins)
        for role,disp,breg,ireg,scale in matches:
            counts[role]+=1
            print(
                f"MEMBER_XREF|role={role}|disp={disp:+#x}|rva=0x{rva:x}|"
                f"base={clean(breg)}|index={clean(ireg)}|scale={scale}|"
                +abstract(ins,base,strings)
            )
            lo=max(0,i-CONTEXT); hi=min(len(insns),i+CONTEXT+1)
            for j in range(lo,hi):
                jrva=insns[j].address-base
                if not (RVA_MIN<=jrva<=RVA_MAX):
                    continue
                print(
                    f"MEMBER_CONTEXT|role={role}|xref_rva=0x{rva:x}|relative={j-i:+d}|"
                    +abstract(insns[j],base,strings)
                )

    for role,_ in MEMBERS:
        print(f"MEMBER_COUNT|role={role}|count={counts[role]}")
    print(
        "RESOLUTION|MANIFEST_RECORD_LAYOUT_DERIVED|"
        + "|".join(f"{role}={counts[role]}" for role,_ in MEMBERS)
        + "|binary-not-committed"
    )


if __name__=="__main__":
    main()
