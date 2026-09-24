#!/usr/bin/env python3
"""Trace the JSS SaUpdate manifest host/path literal dataflow around RVA 0x13f0.

Derived metadata only: operand shapes, absolute-memory references, enclosing
function boundaries and direct caller RVAs. No executable bytes or disassembly
text are retained.
"""

from __future__ import annotations

import hashlib
import struct
from collections import defaultdict

from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_OP_REG, X86_REG_INVALID, X86_REG_EDI

from tools.stoneage_jss_launcher_archive_probe import ORIGINAL,get_bounded,replay_url
from tools.stoneage_jss_launcher_deep_probe import KNOWN_SHA256,TIMESTAMP,parse_pe_layout
from tools.stoneage_jss_saupdate_xref_probe import (
    find_string_locations,parse_imports,
)
from tools.stoneage_jss_saupdate_http_flow_probe import import_thunks
from tools.stoneage_jss_saupdate_function_flow_probe import (
    ascii_strings,disassemble_text,function_summary,resolve_call,
    raw_pointer_hits,recover_xref_instruction,
)
from tools.stoneage_tw10_mapcache_binary_probe import referenced_absolute_values
from tools.stoneage_tw10_technical_probe import pe_sections

TARGETS=(
    (b"update.gamersdream.ne.jp","manifest-host"),
    (b"/~stoneage/newest.txt","manifest-path"),
)
WINDOW=28


def clean(v,limit=1000):
    s=" ".join(str(v if v is not None else "").split())
    return "".join(c for c in s if c>=" " and c!="\x7f").replace("|","%7C")[:limit]


def operand_shape(ins,op,image_base,strings):
    if op.type==X86_OP_REG:
        return "reg:"+ins.reg_name(op.reg)
    if op.type==X86_OP_IMM:
        value=int(op.imm)&0xffffffff
        text=strings.get(value)
        if text is not None:
            return "string:"+clean(text)
        return f"imm:0x{value:x}"
    if op.type==X86_OP_MEM:
        mem=op.mem
        base=ins.reg_name(mem.base) if mem.base!=X86_REG_INVALID else ""
        index=ins.reg_name(mem.index) if mem.index!=X86_REG_INVALID else ""
        disp=int(mem.disp)
        if mem.base==X86_REG_INVALID and mem.index==X86_REG_INVALID:
            return f"absolute:0x{disp&0xffffffff:x}"
        return f"mem:{base}:{index}:{disp:+#x}:scale={mem.scale}"
    return "other"


def edi_flow(insns,start_idx,image_base,strings,limit=48):
    rows=[]
    for j in range(start_idx+1,min(len(insns),start_idx+1+limit)):
        ins=insns[j]
        uses=[]
        for op_index,op in enumerate(ins.operands,1):
            hit=False
            if op.type==X86_OP_REG and op.reg==X86_REG_EDI:
                hit=True
            elif op.type==X86_OP_MEM and (
                op.mem.base==X86_REG_EDI or op.mem.index==X86_REG_EDI
            ):
                hit=True
            if hit:
                uses.append((op_index,operand_shape(ins,op,image_base,strings)))
        if uses:
            all_shapes=tuple(
                (n,operand_shape(ins,op,image_base,strings))
                for n,op in enumerate(ins.operands,1)
            )
            rows.append((
                ins.address-image_base,
                ins.mnemonic,
                tuple(uses),
                all_shapes,
            ))
        # Stop when EDI is overwritten by a new non-EDI source.
        if (
            ins.mnemonic in {"mov","lea"}
            and ins.operands
            and ins.operands[0].type==X86_OP_REG
            and ins.operands[0].reg==X86_REG_EDI
        ):
            src_edi=(
                len(ins.operands)>1
                and ins.operands[1].type==X86_OP_REG
                and ins.operands[1].reg==X86_REG_EDI
            )
            if not src_edi:
                break
        if ins.mnemonic.startswith("ret"):
            break
    return tuple(rows)


def direct_callers(insns,image_base,target_va):
    out=[]
    for ins in insns:
        if ins.mnemonic!="call" or not ins.operands:
            continue
        op=ins.operands[0]
        if op.type==X86_OP_IMM and (int(op.imm)&0xffffffff)==target_va:
            out.append(ins.address-image_base)
    return tuple(out)


def absolute_refs_near(insns,idx,image_base,strings):
    rows=[]
    seen=set()
    for j in range(max(0,idx-WINDOW),min(len(insns),idx+WINDOW+1)):
        ins=insns[j]
        for op_index,op in enumerate(ins.operands):
            if op.type!=X86_OP_MEM:
                continue
            mem=op.mem
            if mem.base!=X86_REG_INVALID or mem.index!=X86_REG_INVALID:
                continue
            va=int(mem.disp)&0xffffffff
            if not (image_base<=va<image_base+0x600000):
                continue
            key=(ins.address,op_index,va)
            if key in seen:
                continue
            seen.add(key)
            all_shapes=tuple(
                (n,operand_shape(ins,x,image_base,strings))
                for n,x in enumerate(ins.operands,1)
            )
            rows.append((
                ins.address-image_base,ins.mnemonic,op_index,va,
                strings.get(va,""),all_shapes,
            ))
    return tuple(rows)


def main():
    print("StoneAge JSS SaUpdate manifest-root dataflow probe — R1")
    print("SCOPE|first-party-host-path-xrefs+operand-shapes+absolute-datarefs+direct-callers|derived-only")

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
    base=pe["image_base"]
    imports=parse_imports(data,layout,base)
    thunks=import_thunks(data,layout,imports)
    sec,insns=disassemble_text(data,layout,base)
    by_addr={ins.address:i for i,ins in enumerate(insns)}
    strings=ascii_strings(data,layout,base)

    roots=set()
    total_refs=0
    for token,label in TARGETS:
        locs=find_string_locations(data,layout,token)
        print(f"TARGET|label={label}|text={clean(token.decode('ascii'))}|locations={len(locs)}")
        for file_off,rva in locs:
            ptr_offsets=raw_pointer_hits(data,layout,base,rva)
            decoded=[]
            for ptr_off in ptr_offsets:
                ins=recover_xref_instruction(data,layout,base,rva,ptr_off)
                if ins is not None:
                    decoded.append(ins)
            decoded=sorted(
                {ins.address:ins for ins in decoded}.values(),
                key=lambda ins:ins.address,
            )
            print(
                f"STRING_LOCATION|label={label}|file_off={file_off}|rva=0x{rva:x}|"
                f"raw_pointer_hits={len(ptr_offsets)}|decoded_xrefs={len(decoded)}"
            )
            for ins in decoded:
                total_refs+=1
                ref_rva=ins.address-base
                idx=by_addr.get(ins.address)
                if idx is None:
                    continue
                f=function_summary(insns,idx,base,imports,thunks,strings)
                roots.add(f["start_rva"])
                print(
                    f"XREF|label={label}|rva=0x{ref_rva:x}|mnemonic={clean(ins.mnemonic)}|"
                    f"function_start_rva=0x{f['start_rva']:x}|function_end_rva=0x{f['end_rva']:x}|"
                    f"operand_count={len(ins.operands)}"
                )
                for n,op in enumerate(ins.operands,1):
                    print(
                        f"OPERAND|label={label}|xref_rva=0x{ref_rva:x}|index={n}|"
                        f"shape={clean(operand_shape(ins,op,base,strings))}"
                    )
                flow=edi_flow(insns,idx,base,strings)
                print(
                    f"EDI_FLOW|label={label}|xref_rva=0x{ref_rva:x}|events={len(flow)}"
                )
                for order,(flow_rva,mnemonic,uses,all_shapes) in enumerate(flow,1):
                    print(
                        f"EDI_USE|label={label}|xref_rva=0x{ref_rva:x}|order={order}|"
                        f"rva=0x{flow_rva:x}|mnemonic={clean(mnemonic)}|"
                        f"edi_operands={';'.join(f'{n}:{shape}' for n,shape in uses)}|"
                        f"all_operands={';'.join(f'{n}:{shape}' for n,shape in all_shapes)}"
                    )
                for rrva,mnemonic,op_index,va,text_value,all_shapes in absolute_refs_near(
                    insns,idx,base,strings
                ):
                    print(
                        f"NEAR_ABSOLUTE|label={label}|xref_rva=0x{ref_rva:x}|"
                        f"ins_rva=0x{rrva:x}|mnemonic={clean(mnemonic)}|operand_index={op_index}|"
                        f"va=0x{va:x}|text={clean(text_value)}|"
                        f"all_operands={';'.join(f'{n}:{shape}' for n,shape in all_shapes)}"
                    )

    for root_rva in sorted(roots):
        callers=direct_callers(insns,base,base+root_rva)
        print(
            f"ROOT_FUNCTION|rva=0x{root_rva:x}|direct_callers={len(callers)}|"
            f"caller_rvas={','.join(f'0x{x:x}' for x in callers)}"
        )

    print(
        f"RESOLUTION|MANIFEST_ROOT_DATAFLOW_DERIVED|targets={len(TARGETS)}|"
        f"xrefs={total_refs}|root_functions={len(roots)}|binary-not-committed"
    )


if __name__=="__main__":
    main()
