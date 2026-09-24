#!/usr/bin/env python3
"""Derive the JSS SaUpdate newest.txt grammar from hash-pinned first-party bytes.

The executable is fetched transiently and verified against the repository-pinned
SHA-256. The report retains only normalized instruction roles, operand classes,
field xrefs and control-flow/call metadata. It retains no executable bytes and
no raw disassembly text.
"""

from __future__ import annotations

import hashlib

from capstone.x86 import (
    X86_OP_IMM, X86_OP_MEM, X86_OP_REG,
    X86_REG_EBP, X86_REG_ESP, X86_REG_INVALID,
)

from tools.stoneage_jss_launcher_archive_probe import ORIGINAL, get_bounded, replay_url
from tools.stoneage_jss_launcher_deep_probe import KNOWN_SHA256, TIMESTAMP, parse_pe_layout
from tools.stoneage_jss_saupdate_xref_probe import parse_imports
from tools.stoneage_jss_saupdate_http_flow_probe import import_thunks
from tools.stoneage_jss_saupdate_function_flow_probe import (
    ascii_strings, disassemble_text, resolve_call,
)
from tools.stoneage_tw10_technical_probe import pe_sections


MANIFEST_RANGE=(0x19D0,0x1F71)
HELPER_RANGES=(
    ("manifest-line-helper",0x1F80,0x1FDF),
    ("manifest-load-helper",0x2060,0x209B),
)
FIELDS=(
    "EXE","SPRBIN","SPRADRNBIN","REALBIN","ADRNBIN","SOUNDBIN",
    "SOUNDADDRTXT","BATTLEBIN","BATTLETXT","IP","IP:1","MESSAGE",
)
CONTEXT_BEFORE=5
CONTEXT_AFTER=7


def clean(value,limit=900):
    s=" ".join(str(value if value is not None else "").split())
    return "".join(c for c in s if c>=" " and c!="\\x7f").replace("|","%7C")[:limit]


def operand_shape(ins,op,image_base,strings):
    if op.type==X86_OP_REG:
        return "reg:"+ins.reg_name(op.reg)
    if op.type==X86_OP_IMM:
        value=int(op.imm)&0xffffffff
        if value in strings:
            return "string:"+clean(strings[value],180)
        if image_base<=value<image_base+0x1000000:
            return f"va-rva:0x{value-image_base:x}"
        if value<=0xffff:
            return f"imm:0x{value:x}"
        return f"imm32:0x{value:x}"
    if op.type==X86_OP_MEM:
        mem=op.mem
        base=ins.reg_name(mem.base) if mem.base!=X86_REG_INVALID else ""
        index=ins.reg_name(mem.index) if mem.index!=X86_REG_INVALID else ""
        disp=int(mem.disp)
        if mem.base==X86_REG_EBP and mem.index==X86_REG_INVALID:
            return f"frame:{disp:+#x}"
        if mem.base==X86_REG_ESP and mem.index==X86_REG_INVALID:
            return f"stack:{disp:+#x}"
        if mem.base==X86_REG_INVALID and mem.index==X86_REG_INVALID:
            value=disp&0xffffffff
            if value in strings:
                return "string-ref:"+clean(strings[value],180)
            if image_base<=value<image_base+0x1000000:
                return f"abs-rva:0x{value-image_base:x}"
            return f"absolute:0x{value:x}"
        return f"mem:{base}:{index}:{disp:+#x}:scale={mem.scale}"
    return "other"


def abstract_instruction(ins,image_base,strings):
    ops=";".join(
        f"{n}:{operand_shape(ins,op,image_base,strings)}"
        for n,op in enumerate(ins.operands,1)
    )
    return f"rva=0x{ins.address-image_base:x}|mnemonic={clean(ins.mnemonic)}|ops={clean(ops,1800)}"


def field_vas(strings):
    wanted=set(FIELDS)
    out={}
    for va,text in strings.items():
        if text in wanted and text not in out:
            out[text]=va
    return out


def semantic_shape(by_rva,rva,base,strings):
    ins=by_rva.get(rva)
    return abstract_instruction(ins,base,strings) if ins is not None else ""


def derive_field5_semantics(insns,base,strings):
    rows=[]
    for ins in insns:
        rva=ins.address-base
        if not (MANIFEST_RANGE[0] <= rva <= MANIFEST_RANGE[1]):
            continue
        for op in ins.operands:
            if op.type!=X86_OP_MEM or op.mem.base!=X86_REG_ESP or op.mem.index!=X86_REG_INVALID:
                continue
            disp=int(op.mem.disp)
            # The fifth-field buffer is stable-stack +0x141c. After pushes,
            # an alias would appear at a larger displacement, so retain a
            # generous 0x1400..0x15ff window across the parser.
            if 0x1400 <= disp <= 0x15ff:
                rows.append((rva,disp,abstract_instruction(ins,base,strings)))
    exact=[row for row in rows if row[0]==0x1aad and row[1]==0x141c]
    post=[row for row in rows if row[0]>0x1ac6]
    print(
        f"FIELD5_STACK_WINDOW|refs={len(rows)}|extract_dest_refs={len(exact)}|"
        f"post_extract_refs={len(post)}"
    )
    for rva,disp,shape in rows:
        print(
            f"FIELD5_STACK_REF|rva=0x{rva:x}|disp=0x{disp:x}|"
            f"phase={'post' if rva>0x1ac6 else 'extract'}|insn={clean(shape,1800)}"
        )
    if len(rows)==1 and len(exact)==1 and not post:
        print(
            "FIELD5_SEMANTIC|parser_behavior=extracted-but-not-consumed|"
            "persistent-record-member=none-recovered|historical-producer-meaning=unknown"
        )
    else:
        print("FIELD5_SEMANTIC|parser_behavior=REQUIRES_REVIEW")


def derive_control_semantics(insns,base,strings,imports,thunks):
    by_rva={ins.address-base:ins for ins in insns}
    checks=(
        (0x1a46,"imm:0x1"),
        (0x1a48,"imm:0x3a"),
        (0x1d74,"string:IP"),
        (0x1daa,"stack:+0x10"),
        (0x1db2,"stack:+0x41c"),
        (0x1dc6,"va-rva:0x45c2fc"),
        (0x1de5,"imm:0x1"),
        (0x1dea,"stack:+0x41c"),
        (0x1e00,"va-rva:0x45befc"),
        (0x1e11,"stack:+0x10"),
        (0x1e1a,"string:IP:1"),
        (0x1e77,"string:MESSAGE"),
        (0x1ead,"stack:+0x81c"),
        (0x1ec6,"va-rva:0x457c74"),
    )
    ok=True
    for rva,needle in checks:
        observed=semantic_shape(by_rva,rva,base,strings)
        hit=needle in observed
        ok &= hit
        print(
            f"CONTROL_CHECK|rva=0x{rva:x}|match={int(hit)}|"
            f"expect={clean(needle)}|observed={clean(observed,1800)}"
        )
    call=by_rva.get(0x1f14)
    resolved=resolve_call(call,base,imports,thunks) if call is not None else None
    call_ok=resolved==("import","MFC42.DLL","CWnd::SetWindowTextA")
    print(
        f"CONTROL_CHECK|rva=0x1f14|match={int(call_ok)}|expect=MFC42.DLL!CWnd::SetWindowTextA|"
        f"observed={clean(resolved)}"
    )
    ok &= call_ok
    if ok:
        print(
            "IP_CONTROL|key=IP|source=full-manifest-line|first_buffer=0x85c2fc|"
            "second_buffer=0x85befc|counter=0-based|copies=first-two-lines|"
            "launch_args=execl-8-and-9"
        )
        print(
            "MESSAGE_CONTROL|key=MESSAGE|source=colon-field-2|"
            "presentation=CWnd::SetWindowTextA|launch_control_buffer=0"
        )
        print(
            "IP1_REACHABILITY|literal_compare=present|normal_colon-field1=IP-for-IP:1-prefix|"
            "direct-record-key-reachability=not-demonstrated"
        )
    else:
        print("CONTROL_SEMANTICS|resolution=PATTERN_MISMATCH")


def main():
    print("StoneAge JSS SaUpdate manifest grammar probe — R1")
    print("SCOPE|newest-field-xrefs+normalized-context+helper-instruction-roles+call-graph|derived-only|no-bytes-no-raw-disassembly")

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
    strings=ascii_strings(data,layout,base)
    by_addr={ins.address:i for i,ins in enumerate(insns)}
    fvas=field_vas(strings)

    for target_rva in (0x5264,):
        binding=imports.get(base+target_rva)
        if binding is None:
            print(f"IAT_BINDING|rva=0x{target_rva:x}|found=0|dll=|name=")
        else:
            dll,name=binding
            print(
                f"IAT_BINDING|rva=0x{target_rva:x}|found=1|"
                f"dll={clean(dll)}|name={clean(name)}"
            )

    print(
        f"PE|image_base=0x{base:x}|instructions={len(insns)}|"
        f"ascii_strings={len(strings)}|fields_found={len(fvas)}"
    )
    for field in FIELDS:
        va=fvas.get(field)
        print(
            f"FIELD|name={field}|found={int(va is not None)}|"
            + (f"rva=0x{va-base:x}" if va is not None else "rva=")
        )

    mstart,mend=MANIFEST_RANGE
    manifest_idxs=[
        i for i,ins in enumerate(insns)
        if mstart<=ins.address-base<=mend
    ]
    print(
        f"MANIFEST_FUNCTION|start_rva=0x{mstart:x}|end_rva=0x{mend:x}|"
        f"instructions={len(manifest_idxs)}"
    )
    for i in manifest_idxs:
        print("MANIFEST_INSN|"+abstract_instruction(insns[i],base,strings))

    total_xrefs=0
    for field in FIELDS:
        va=fvas.get(field)
        if va is None:
            continue
        refs=[]
        for i in manifest_idxs:
            ins=insns[i]
            hit=False
            for op in ins.operands:
                if op.type==X86_OP_IMM and (int(op.imm)&0xffffffff)==va:
                    hit=True
                elif op.type==X86_OP_MEM:
                    mem=op.mem
                    if (
                        mem.base==X86_REG_INVALID and mem.index==X86_REG_INVALID
                        and (int(mem.disp)&0xffffffff)==va
                    ):
                        hit=True
            if hit:
                refs.append(i)
        print(f"FIELD_XREF_COUNT|name={field}|count={len(refs)}")
        total_xrefs+=len(refs)
        for ref_i in refs:
            ref=insns[ref_i]
            print(
                f"FIELD_XREF|name={field}|"
                + abstract_instruction(ref,base,strings)
            )
            lo=max(manifest_idxs[0],ref_i-CONTEXT_BEFORE)
            hi=min(manifest_idxs[-1],ref_i+CONTEXT_AFTER)
            for j in range(lo,hi+1):
                ins=insns[j]
                rel=j-ref_i
                print(
                    f"FIELD_CONTEXT|name={field}|xref_rva=0x{ref.address-base:x}|"
                    f"relative={rel:+d}|"
                    + abstract_instruction(ins,base,strings)
                )

    for role,start,end in HELPER_RANGES:
        rows=[ins for ins in insns if start<=ins.address-base<=end]
        print(
            f"HELPER|role={role}|start_rva=0x{start:x}|end_rva=0x{end:x}|"
            f"instructions={len(rows)}"
        )
        for ins in rows:
            print(f"HELPER_INSN|role={role}|"+abstract_instruction(ins,base,strings))

        target=base+start
        callers=[]
        for i,ins in enumerate(insns):
            if ins.mnemonic!="call":
                continue
            for op in ins.operands:
                if op.type==X86_OP_IMM and (int(op.imm)&0xffffffff)==target:
                    callers.append(i)
                    break
        print(f"HELPER_CALLERS|role={role}|count={len(callers)}")
        for i in callers:
            call=insns[i]
            print(f"HELPER_CALLER|role={role}|"+abstract_instruction(call,base,strings))
            lo=max(0,i-6)
            for j in range(lo,i+1):
                print(
                    f"CALL_CONTEXT|role={role}|call_rva=0x{call.address-base:x}|"
                    f"relative={j-i:+d}|"
                    + abstract_instruction(insns[j],base,strings)
                )

    calls=0
    for i in manifest_idxs:
        ins=insns[i]
        resolved=resolve_call(ins,base,imports,thunks)
        if resolved is None:
            continue
        calls+=1
        kind,dll,target=resolved
        print(
            f"MANIFEST_CALL|rva=0x{ins.address-base:x}|kind={kind}|"
            f"dll={clean(dll)}|target={clean(target)}"
        )

    derive_field5_semantics(insns,base,strings)
    derive_control_semantics(insns,base,strings,imports,thunks)

    print(
        f"RESOLUTION|MANIFEST_GRAMMAR_DERIVED|fields={len(FIELDS)}|"
        f"field_xrefs={total_xrefs}|manifest_calls={calls}|helpers={len(HELPER_RANGES)}|"
        "binary-not-committed"
    )


if __name__=="__main__":
    main()
