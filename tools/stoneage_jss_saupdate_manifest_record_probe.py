#!/usr/bin/env python3
"""Trace JSS SaUpdate manifest-record consumers from hash-pinned first-party bytes.

The report keeps only normalized instruction/operand roles around the fixed
0x114 record stride, manifest array anchors, and checksum call sites.
"""

from __future__ import annotations

import hashlib

from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_OP_REG, X86_REG_INVALID

from tools.stoneage_jss_launcher_archive_probe import ORIGINAL, get_bounded, replay_url
from tools.stoneage_jss_launcher_deep_probe import KNOWN_SHA256, TIMESTAMP, parse_pe_layout
from tools.stoneage_jss_saupdate_xref_probe import parse_imports
from tools.stoneage_jss_saupdate_function_flow_probe import ascii_strings, disassemble_text
from tools.stoneage_tw10_technical_probe import pe_sections

STRIDE=0x114
ARRAY_TEXT_START=0x407C50
ARRAY_META_START=0x407D50
ARRAY_META_END=0x857D50
CHECKSUM_RVA=0x3F20
WINDOW=34


def clean(value,limit=900):
    s=" ".join(str(value if value is not None else "").split())
    return "".join(c for c in s if c>=" " and c!="\x7f").replace("|","%7C")[:limit]


def operand_shape(ins,op,image_base,strings):
    if op.type==X86_OP_REG:
        return "reg:"+ins.reg_name(op.reg)
    if op.type==X86_OP_IMM:
        v=int(op.imm)&0xffffffff
        if v in strings:
            return "string:"+clean(strings[v],180)
        if image_base<=v<image_base+0x1000000:
            return f"va-rva:0x{v-image_base:x}"
        return f"imm:0x{v:x}"
    if op.type==X86_OP_MEM:
        m=op.mem
        b=ins.reg_name(m.base) if m.base!=X86_REG_INVALID else ""
        i=ins.reg_name(m.index) if m.index!=X86_REG_INVALID else ""
        d=int(m.disp)
        if m.base==X86_REG_INVALID and m.index==X86_REG_INVALID:
            v=d&0xffffffff
            if v in strings:
                return "string-ref:"+clean(strings[v],180)
            if image_base<=v<image_base+0x1000000:
                return f"abs-rva:0x{v-image_base:x}"
            return f"absolute:0x{v:x}"
        return f"mem:{b}:{i}:{d:+#x}:scale={m.scale}"
    return "other"


def abstract(ins,base,strings):
    ops=";".join(f"{n}:{operand_shape(ins,o,base,strings)}" for n,o in enumerate(ins.operands,1))
    return f"rva=0x{ins.address-base:x}|mnemonic={clean(ins.mnemonic)}|ops={clean(ops,1800)}"


def has_imm(ins,value):
    for op in ins.operands:
        if op.type==X86_OP_IMM and (int(op.imm)&0xffffffff)==value:
            return True
    return False


def has_absolute(ins,value):
    for op in ins.operands:
        if op.type==X86_OP_IMM and (int(op.imm)&0xffffffff)==value:
            return True
        if op.type==X86_OP_MEM:
            m=op.mem
            if m.base==X86_REG_INVALID and m.index==X86_REG_INVALID and (int(m.disp)&0xffffffff)==value:
                return True
    return False


def emit_window(label,idx,insns,base,strings):
    lo=max(0,idx-WINDOW); hi=min(len(insns),idx+WINDOW+1)
    anchor=insns[idx].address-base
    print(f"WINDOW|label={label}|anchor_rva=0x{anchor:x}|before={idx-lo}|after={hi-idx-1}")
    for j in range(lo,hi):
        print(f"CONTEXT|label={label}|anchor_rva=0x{anchor:x}|relative={j-idx:+d}|"+abstract(insns[j],base,strings))


def main():
    print("StoneAge JSS SaUpdate manifest-record consumer probe — R1")
    print("SCOPE|record-stride+array-anchors+checksum-call-context|derived-only|no-bytes-no-raw-disassembly")
    status,final,headers,data=get_bounded(replay_url({"timestamp":TIMESTAMP,"original":ORIGINAL}),timeout=20)
    sha=hashlib.sha256(data).hexdigest()
    print(f"FETCH|status={status}|bytes={len(data)}|sha256={sha}|final={clean(final)}")
    if sha!=KNOWN_SHA256:
        print(f"RESOLUTION|HASH_MISMATCH|expected={KNOWN_SHA256}")
        return

    layout=parse_pe_layout(data)
    base=pe_sections(data)["image_base"]
    imports=parse_imports(data,layout,base)
    sec,insns=disassemble_text(data,layout,base)
    strings=ascii_strings(data,layout,base)

    print(f"ARRAY|text_start=0x{ARRAY_TEXT_START:x}|meta_start=0x{ARRAY_META_START:x}|meta_end=0x{ARRAY_META_END:x}|stride=0x{STRIDE:x}")
    for va in (0x405264,):
        dll,name=imports.get(va,("",""))
        print(f"IAT_BINDING|va=0x{va:x}|dll={clean(dll)}|name={clean(name)}")

    seen=set()
    anchors=[]
    for i,ins in enumerate(insns):
        rva=ins.address-base
        labels=[]
        if has_imm(ins,STRIDE):
            labels.append("stride-0x114")
        for va,label in ((ARRAY_TEXT_START,"array-text-start"),(ARRAY_META_START,"array-meta-start"),(ARRAY_META_END,"array-meta-end")):
            if has_absolute(ins,va):
                labels.append(label)
        if ins.mnemonic=="call" and has_imm(ins,base+CHECKSUM_RVA):
            labels.append("checksum-call")
        for label in labels:
            key=(label,rva)
            if key in seen: continue
            seen.add(key); anchors.append((label,i))

    print(f"ANCHORS|count={len(anchors)}")
    for label,idx in anchors:
        emit_window(label,idx,insns,base,strings)

    print(f"RESOLUTION|MANIFEST_RECORD_CONSUMERS_DERIVED|anchors={len(anchors)}|binary-not-committed")


if __name__=="__main__":
    main()
