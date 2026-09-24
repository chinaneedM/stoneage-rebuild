#!/usr/bin/env python3
"""Abstract call-argument/dataflow probe for the archived JSS SaUpdate program.

Only derived argument-source summaries are retained. The hash-pinned executable
and instruction stream are transient.
"""

from __future__ import annotations

import hashlib
import struct

from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from capstone.x86 import (
    X86_OP_IMM, X86_OP_MEM, X86_OP_REG,
    X86_REG_EBP, X86_REG_ESP, X86_REG_INVALID,
)

from tools.stoneage_jss_launcher_archive_probe import ORIGINAL, get_bounded, replay_url
from tools.stoneage_jss_launcher_deep_probe import KNOWN_SHA256, TIMESTAMP, parse_pe_layout
from tools.stoneage_jss_saupdate_xref_probe import parse_imports, section_blob
from tools.stoneage_jss_saupdate_http_flow_probe import import_thunks, import_call_sites

MAX_BACK=32
MAX_ARGS=16

# Exact code sites already established by prior derived probes.
FOCUS_SITES=(
    (0x1577,"manifest-global-prep-call"),
    (0x157B,"manifest-wrapper-dispatch"),
    (0x2902,"wrapper-to-http-core"),
    (0x2E94,"http-core-to-launch-tail"),
    (0x2F15,"http-core-helper-24a0"),
    (0x3015,"http-core-post-state-a"),
    (0x3076,"http-core-post-state-b"),
    (0x30A6,"http-core-post-state-c"),
    (0x31E3,"http-core-helper-3410"),
    (0x31FF,"http-core-generation-scan"),
    (0x32BD,"http-core-helper-3500"),
    (0x336F,"http-core-final-indirect"),
    (0x299E,"internet-session-ctor"),
    (0x2A28,"get-http-connection"),
    (0x2A44,"open-http-request"),
    (0x2A54,"send-http-request"),
    (0x2A5F,"query-http-status"),
    (0x2D9B,"per-file-http-core-reentry"),
    (0x3798,"parser-a-fgets-1"),
    (0x37D1,"parser-a-token-1"),
    (0x3801,"parser-a-token-2"),
    (0x382B,"parser-a-token-3"),
    (0x3903,"parser-a-fgets-2"),
    (0x3A34,"parser-b-fgets-1"),
    (0x3A76,"parser-b-token-1"),
    (0x3AA9,"parser-b-token-2"),
    (0x3AD8,"parser-b-token-3"),
    (0x3C15,"parser-b-fgets-2"),
    (0x3D54,"sa-name-format-or-helper"),
    (0x3D71,"sa-name-followup"),
    (0x3D78,"unlink-old-sa"),
    (0x3DA0,"generation-scan-before-realbin"),
    (0x3DB4,"state-op-realbin"),
    (0x3DD8,"generation-scan-before-soundbin"),
    (0x3DEC,"state-op-soundbin"),
    (0x3E10,"generation-scan-before-battlebin"),
    (0x3E24,"state-op-battlebin"),
    (0x3E48,"generation-scan-before-sprbin"),
    (0x3E5C,"state-op-sprbin"),
    (0x3E80,"generation-scan-before-spradrnbin"),
    (0x3E94,"state-op-spradrnbin"),
    (0x3EB8,"generation-scan-before-adrnbin"),
    (0x3ECC,"state-op-adrnbin"),
    (0x3F00,"execl-launch"),
)

# Global buffers bound by the immediately preceding format-shaped call sites.
# These are analytical roles derived from argument structure, not original symbols.
GLOBAL_BUFFER_LABELS={
    0x85E6FC:"sa-executable-buffer",
    0x85E2FC:"realbin-state-buffer",
    0x85DEFC:"soundbin-state-buffer",
    0x85CAFC:"battlebin-state-buffer",
    0x85D2FC:"sprbin-state-buffer",
    0x85CEFC:"spradrnbin-state-buffer",
    0x85D6FC:"adrnbin-state-buffer",
}
SELECTOR_BY_LABEL={
    "generation-scan-before-realbin":("realbin",2),
    "generation-scan-before-soundbin":("soundbin",3),
    "generation-scan-before-battlebin":("battlebin",8),
    "generation-scan-before-sprbin":("sprbin",4),
    "generation-scan-before-spradrnbin":("spradrnbin",5),
    "generation-scan-before-adrnbin":("adrnbin",6),
}


def clean(v,limit=900):
    s=" ".join(str(v if v is not None else "").split())
    return "".join(c for c in s if c>=" " and c!="\x7f").replace("|","%7C")[:limit]


def image_base(data):
    pe=struct.unpack_from("<I",data,0x3c)[0]
    return struct.unpack_from("<I",data,pe+24+28)[0]


def file_offset_to_rva(layout,off):
    for sec in layout["sections"]:
        if sec["raw_ptr"]<=off<sec["raw_ptr"]+sec["raw_size"]:
            return sec["vaddr"]+(off-sec["raw_ptr"])
    return None


def ascii_strings(data,layout,base,min_len=2):
    out={}
    for sec in layout["sections"]:
        if sec["chars"] & 0x20000000:
            continue
        start=sec["raw_ptr"]; end=min(len(data),start+sec["raw_size"])
        blob=data[start:end]
        p=0
        while p<len(blob):
            if 0x20<=blob[p]<=0x7e:
                q=p
                while q<len(blob) and 0x20<=blob[q]<=0x7e:
                    q+=1
                if q-p>=min_len:
                    rva=file_offset_to_rva(layout,start+p)
                    if rva is not None:
                        try:s=blob[p:q].decode("ascii")
                        except Exception:s=""
                        if s and len(s)<=700:
                            out[base+rva]=s
                p=q
            else:
                p+=1
    return out


def disassemble(data,layout,base):
    sec=next(s for s in layout["sections"] if s["name"]==".text")
    md=Cs(CS_ARCH_X86,CS_MODE_32); md.detail=True
    return list(md.disasm(section_blob(data,sec),base+sec["vaddr"]))


def reg_name(ins,reg):
    try:return ins.reg_name(reg)
    except Exception:return f"reg:{reg}"


def mem_desc(ins,mem):
    b=reg_name(ins,mem.base) if mem.base!=X86_REG_INVALID else ""
    i=reg_name(ins,mem.index) if mem.index!=X86_REG_INVALID else ""
    d=int(mem.disp)
    if mem.base==X86_REG_EBP and mem.index==X86_REG_INVALID:
        return f"local:{d:+#x}"
    if mem.base==X86_REG_ESP and mem.index==X86_REG_INVALID:
        return f"stack:{d:+#x}"
    if mem.base==X86_REG_INVALID and mem.index==X86_REG_INVALID:
        return f"absolute:0x{d&0xffffffff:x}"
    return f"mem:{b}:{i}:{d:+#x}"


def imm_desc(value,strings):
    v=int(value)&0xffffffff
    if v==0:return "null"
    if v in strings:return "string:"+clean(strings[v],500)
    if v in GLOBAL_BUFFER_LABELS:
        return f"global:{GLOBAL_BUFFER_LABELS[v]}@0x{v:x}"
    return f"imm:0x{v:x}"


def trace_reg(insns,idx,reg,strings,depth=0):
    if depth>3:return "register:"+reg_name(insns[idx],reg)
    for j in range(idx-1,max(-1,idx-18),-1):
        ins=insns[j]
        if not ins.operands:continue
        dst=ins.operands[0]
        if dst.type!=X86_OP_REG or dst.reg!=reg:continue
        if ins.mnemonic=="lea" and len(ins.operands)>1 and ins.operands[1].type==X86_OP_MEM:
            return mem_desc(ins,ins.operands[1].mem)
        if ins.mnemonic=="mov" and len(ins.operands)>1:
            src=ins.operands[1]
            if src.type==X86_OP_IMM:return imm_desc(src.imm,strings)
            if src.type==X86_OP_REG:return trace_reg(insns,j,src.reg,strings,depth+1)
            if src.type==X86_OP_MEM:return mem_desc(ins,src.mem)
        return "register:"+reg_name(ins,reg)
    return "register:"+reg_name(insns[idx],reg)


def push_desc(insns,idx,strings):
    ins=insns[idx]
    if ins.mnemonic!="push" or not ins.operands:return None
    op=ins.operands[0]
    if op.type==X86_OP_IMM:return imm_desc(op.imm,strings)
    if op.type==X86_OP_REG:return trace_reg(insns,idx,op.reg,strings)
    if op.type==X86_OP_MEM:return mem_desc(ins,op.mem)
    return "unknown"


def stack_args(insns,idx,strings,max_args=MAX_ARGS):
    """Nearest push to call is stack argument 1 for cdecl/stdcall-shaped calls."""
    found=[]
    for j in range(idx-1,max(-1,idx-MAX_BACK),-1):
        ins=insns[j]
        if ins.mnemonic=="push":
            found.append((ins.address,push_desc(insns,j,strings)))
            if len(found)>=max_args:break
            continue
        if ins.mnemonic=="call" and found:
            break
        if ins.mnemonic.startswith("ret") or ins.mnemonic=="jmp":
            break
    return tuple(found)


def nearby_strings(insns,idx,strings,base,back=28):
    out=[]; seen=set()
    for j in range(max(0,idx-back),idx):
        ins=insns[j]
        for op in ins.operands:
            vals=[]
            if op.type==X86_OP_IMM:
                vals.append(int(op.imm)&0xffffffff)
            elif op.type==X86_OP_MEM:
                m=op.mem
                if m.base==X86_REG_INVALID and m.index==X86_REG_INVALID:
                    vals.append(int(m.disp)&0xffffffff)
            for va in vals:
                s=strings.get(va)
                if s is not None and (ins.address-base,s) not in seen:
                    seen.add((ins.address-base,s))
                    out.append((ins.address-base,s))
    return tuple(out)


def call_identity(rva,imports):
    for site,dll,name,mode in imports:
        if site==rva:return f"{dll}!{name}"
    return "internal-or-indirect"


def main():
    print("StoneAge JSS SaUpdate call-argument probe — R1")
    print("SCOPE|focused-callsite-argument-sources|heuristic-dataflow|derived-only|no-disassembly-retained")
    status,final,headers,data=get_bounded(
        replay_url({"timestamp":TIMESTAMP,"original":ORIGINAL}),timeout=20
    )
    sha=hashlib.sha256(data).hexdigest()
    print(f"FETCH|status={status}|bytes={len(data)}|sha256={sha}|final={clean(final)}")
    if sha!=KNOWN_SHA256:
        print(f"RESOLUTION|HASH_MISMATCH|expected={KNOWN_SHA256}")
        return

    layout=parse_pe_layout(data); base=image_base(data)
    iat=parse_imports(data,layout,base); thunks=import_thunks(data,layout,iat)
    imported=import_call_sites(data,layout,iat,thunks)
    insns=disassemble(data,layout,base)
    by_rva={ins.address-base:i for i,ins in enumerate(insns)}
    strings=ascii_strings(data,layout,base)

    print(f"PE|image_base=0x{base:x}|instructions={len(insns)}|strings={len(strings)}")
    decoded=0
    for rva,label in FOCUS_SITES:
        idx=by_rva.get(rva)
        if idx is None:
            print(f"CALLSITE|rva=0x{rva:x}|label={label}|decoded=0")
            continue
        decoded+=1
        args=stack_args(insns,idx,strings)
        near=nearby_strings(insns,idx,strings,base)
        print(
            f"CALLSITE|rva=0x{rva:x}|label={label}|decoded=1|"
            f"identity={clean(call_identity(rva,imported))}|stack_args={len(args)}|nearby_strings={len(near)}"
        )
        for n,(addr,src) in enumerate(args,1):
            print(f"STACK_ARG|call_rva=0x{rva:x}|index={n}|push_rva=0x{addr-base:x}|source={clean(src)}")
        for n,(ins_rva,s) in enumerate(near,1):
            print(f"NEAR_STRING|call_rva=0x{rva:x}|order={n}|ins_rva=0x{ins_rva:x}|text={clean(s)}")

        if label in SELECTOR_BY_LABEL and args:
            key,expected=SELECTOR_BY_LABEL[label]
            observed=args[0][1]
            print(
                f"GENERATION_SELECTOR|call_rva=0x{rva:x}|key={key}|"
                f"expected={expected}|observed={clean(observed)}|match={int(observed==f'imm:0x{expected:x}')}"
            )

        # Recognize the repeated destination + '*bin:%d' + integer formatting shape.
        if label.startswith("state-op-") and len(args)>=3:
            print(
                f"STATE_FORMAT_BINDING|call_rva=0x{rva:x}|key={label[9:]}|"
                f"destination={clean(args[0][1])}|format={clean(args[1][1])}|value={clean(args[2][1])}"
            )

        if label=="execl-launch":
            vector=";".join(f"{n}:{src}" for n,(_,src) in enumerate(args,1))
            print(f"LAUNCH_VECTOR|call_rva=0x{rva:x}|args={clean(vector,4000)}")

    print(
        f"RESOLUTION|CALL_ARGUMENT_SOURCES_DERIVED|decoded_sites={decoded}|"
        f"focus_sites={len(FOCUS_SITES)}|heuristic=1|binary-not-committed"
    )


if __name__=="__main__":
    main()
