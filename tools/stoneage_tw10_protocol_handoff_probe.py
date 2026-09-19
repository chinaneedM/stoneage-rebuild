#!/usr/bin/env python3
"""Trace the indirect network handoff from Taiwan v1.0 lssproto_Send.

The helper RVAs were established by exact protocol-message call count/order:
  0x1b480 CreateHeader
  0x1b060 strcatsafe
  0x1b0f0 mkstr_string
  0x1b0b0 mkstr_int
  0x1b3f0 Send

This probe disassembles only the identified Send helper, records indirect calls and
absolute globals, then searches .text for exact references/assignments to those globals.
Derived metadata only; no payload bytes or instruction operands are committed.
"""

from __future__ import annotations

import argparse
import collections
from pathlib import Path
import struct
import tempfile

from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_OP_REG

from tools.stoneage_tw10_technical_probe import find_rows, extract_row
from tools.stoneage_tw10_mapcache_binary_probe import (
    image_layout,
    imported_call,
    referenced_absolute_values,
    rva_to_offset,
    disassemble_text,
)
from tools.stoneage_tw10_exact_xref_probe import (
    recover_xref_instruction,
    raw_text_pointer_hits,
)

SEND_RVA = 0x1B3F0
INIT_RVA = 0x1AC10
DEFAULT_WRITE_RVA = 0x1B3D0
MAX_BYTES = 0x800
MAX_INSNS = 400
MAX_GLOBAL_XREFS = 64
ASSIGN_CONTEXT_BEFORE = 16
ASSIGN_CONTEXT_AFTER = 4
BACKTRACE_DEPTH = 10
BACKTRACE_MAX_PATHS = 24


def clean(v, limit=800):
    s = " ".join(str(v if v is not None else "").split())
    return "".join(ch for ch in s if ch >= " " and ch != "\x7f").replace("|", "%7C")[:limit]


def md():
    obj = Cs(CS_ARCH_X86, CS_MODE_32)
    obj.detail = True
    return obj


def image_range(base, sections):
    hi = base
    for sec in sections:
        hi = max(hi, base + sec["rva"] + max(sec["vsize"], sec["raw_size"]))
    return base, hi


def abs_mem_address(ins, op):
    if op.type != X86_OP_MEM:
        return None
    mem = op.mem
    if mem.base == 0 and mem.index == 0:
        return int(mem.disp) & 0xFFFFFFFF
    return None


def decode_helper(data, base, sections, imports, start_rva):
    off = rva_to_offset(sections, start_rva)
    if off is None:
        raise ValueError("helper RVA unmapped")
    blob = data[off:min(len(data), off + MAX_BYTES)]
    instructions = []
    for ins in md().disasm(blob, base + start_rva, count=MAX_INSNS):
        instructions.append(ins)
        if ins.mnemonic.startswith("ret"):
            break
    events = []
    globals_seen = collections.Counter()
    for ins in instructions:
        imp = imported_call(ins, imports)
        if imp:
            events.append(("import", ins.address, imp[0], imp[1], None))
        if ins.mnemonic == "call":
            if any(op.type == X86_OP_IMM for op in ins.operands):
                for op in ins.operands:
                    if op.type == X86_OP_IMM:
                        events.append(("direct", ins.address, "", "", int(op.imm) & 0xFFFFFFFF))
            else:
                for op in ins.operands:
                    if op.type == X86_OP_MEM:
                        addr = abs_mem_address(ins, op)
                        if addr is not None:
                            globals_seen[addr] += 1
                            events.append(("indirect_mem", ins.address, "", "", addr))
                        else:
                            events.append(("indirect_mem_indexed", ins.address, "", "", None))
                    elif op.type == X86_OP_REG:
                        events.append(("indirect_reg", ins.address, "", "", op.reg))
        for op in ins.operands:
            addr = abs_mem_address(ins, op)
            if addr is not None:
                globals_seen[addr] += 1
    return instructions, events, globals_seen


def section_name_for_va(base, sections, va):
    rva = va - base
    for sec in sections:
        if sec["rva"] <= rva < sec["rva"] + max(sec["vsize"], sec["raw_size"]):
            return sec["name"]
    return ""


def assignment_details(ins, global_va, base, sections):
    """Classify writes to [global_va] and expose immediate text target if present."""
    if not ins.operands:
        return None
    dst = ins.operands[0]
    dst_addr = abs_mem_address(ins, dst)
    if dst_addr != global_va:
        return None
    src_kind = ""
    src_value = None
    if len(ins.operands) >= 2:
        src = ins.operands[1]
        if src.type == X86_OP_IMM:
            src_kind = "imm"
            src_value = int(src.imm) & 0xFFFFFFFF
        elif src.type == X86_OP_REG:
            src_kind = "reg"
            src_value = int(src.reg)
        elif src.type == X86_OP_MEM:
            src_kind = "mem"
            src_value = abs_mem_address(ins, src)
    return {
        "mnemonic": ins.mnemonic,
        "src_kind": src_kind,
        "src_value": src_value,
        "src_section": section_name_for_va(base, sections, src_value) if src_kind == "imm" else "",
    }


def operand_summary(ins, base, sections):
    parts = []
    for op in ins.operands:
        if op.type == X86_OP_REG:
            parts.append(f"reg:{ins.reg_name(op.reg)}")
        elif op.type == X86_OP_IMM:
            value = int(op.imm) & 0xFFFFFFFF
            sec = section_name_for_va(base, sections, value)
            if sec:
                parts.append(f"imm:0x{value-base:x}:{sec}")
            else:
                parts.append(f"imm:0x{value:x}")
        elif op.type == X86_OP_MEM:
            addr = abs_mem_address(ins, op)
            if addr is not None:
                sec = section_name_for_va(base, sections, addr)
                if sec:
                    parts.append(f"memabs:0x{addr-base:x}:{sec}")
                else:
                    parts.append(f"memabs:0x{addr:x}")
            else:
                mem = op.mem
                b = ins.reg_name(mem.base) if mem.base else ""
                x = ins.reg_name(mem.index) if mem.index else ""
                parts.append(f"mem:{b}:{x}:{int(mem.scale)}:{int(mem.disp)}")
        else:
            parts.append(f"op:{op.type}")
    return ",".join(parts)


def assignment_context(instructions, target_va, base, sections):
    index = next((i for i, ins in enumerate(instructions) if ins.address == target_va), None)
    if index is None:
        return []
    lo = max(0, index - ASSIGN_CONTEXT_BEFORE)
    hi = min(len(instructions), index + ASSIGN_CONTEXT_AFTER + 1)
    return instructions[lo:hi]


def predecessor_candidates(data, base, sections, target_va):
    target_off = rva_to_offset(sections, target_va - base)
    if target_off is None:
        return []
    out = []
    decoder = md()
    for back in range(1, 16):
        start = target_off - back
        if start < 0:
            continue
        start_rva = None
        for sec in sections:
            if sec["raw"] <= start < sec["raw"] + sec["raw_size"]:
                start_rva = sec["rva"] + (start - sec["raw"])
                if sec["name"] != ".text":
                    start_rva = None
                break
        if start_rva is None:
            continue
        one = list(decoder.disasm(data[start:target_off], base + start_rva, count=1))
        if not one:
            continue
        ins = one[0]
        if ins.address + ins.size == target_va:
            out.append(ins)
    uniq = {}
    for ins in out:
        uniq[(ins.address, ins.size, ins.mnemonic, ins.op_str)] = ins
    return sorted(uniq.values(), key=lambda x: x.address)


def backward_paths(data, base, sections, target_va):
    frontier = [(target_va, [])]
    complete = []
    for _ in range(BACKTRACE_DEPTH):
        nxt = []
        for cursor, rev_path in frontier:
            preds = predecessor_candidates(data, base, sections, cursor)
            if not preds:
                complete.append(list(reversed(rev_path)))
                continue
            for pred in preds:
                nxt.append((pred.address, rev_path + [pred]))
                if len(nxt) >= BACKTRACE_MAX_PATHS:
                    break
            if len(nxt) >= BACKTRACE_MAX_PATHS:
                break
        if not nxt:
            break
        frontier = nxt[:BACKTRACE_MAX_PATHS]
    complete.extend(list(reversed(path)) for _, path in frontier)
    return complete[:BACKTRACE_MAX_PATHS]


def direct_rel32_call_sites(data, base, sections, target_va):
    sec = next((s for s in sections if s["name"] == ".text"), None)
    if sec is None:
        return []
    blob = data[sec["raw"]:sec["raw"] + sec["raw_size"]]
    out = []
    for rel in range(0, max(0, len(blob) - 5)):
        if blob[rel] != 0xE8:
            continue
        disp = struct.unpack_from("<i", blob, rel + 1)[0]
        site_va = base + sec["rva"] + rel
        if (site_va + 5 + disp) & 0xFFFFFFFF == target_va:
            out.append(site_va)
    return out


def immediate_text_push(ins, base, sections):
    if ins.mnemonic != "push" or len(ins.operands) != 1:
        return None
    op = ins.operands[0]
    if op.type != X86_OP_IMM:
        return None
    value = int(op.imm) & 0xFFFFFFFF
    return value if section_name_for_va(base, sections, value) == ".text" else None


def callback_cfg_probe(data, base, sections, imports, callback_va):
    queue = [callback_va]
    visited_blocks = set()
    visited_ins = set()
    api = collections.Counter()
    direct = collections.Counter()
    globals_seen = collections.Counter()
    block_count = 0
    while queue and block_count < 48 and len(visited_ins) < 600:
        start = queue.pop(0)
        if start in visited_blocks:
            continue
        visited_blocks.add(start)
        block_count += 1
        off = rva_to_offset(sections, start - base)
        if off is None:
            continue
        blob = data[off:min(len(data), off + 0x600)]
        for ins in md().disasm(blob, start, count=160):
            if ins.address in visited_ins:
                break
            visited_ins.add(ins.address)
            imp = imported_call(ins, imports)
            if imp:
                api[imp] += 1
            for value in referenced_absolute_values(ins):
                if section_name_for_va(base, sections, value) == ".data":
                    globals_seen[value] += 1
            if ins.mnemonic == "call":
                for op in ins.operands:
                    if op.type == X86_OP_IMM:
                        target = int(op.imm) & 0xFFFFFFFF
                        if section_name_for_va(base, sections, target) == ".text":
                            direct[target] += 1
            next_va = ins.address + ins.size
            if ins.mnemonic == "jmp":
                target = next((int(op.imm) & 0xFFFFFFFF for op in ins.operands if op.type == X86_OP_IMM), None)
                if target is not None and section_name_for_va(base, sections, target) == ".text":
                    queue.append(target)
                break
            if ins.mnemonic.startswith("j") and ins.mnemonic != "jmp":
                target = next((int(op.imm) & 0xFFFFFFFF for op in ins.operands if op.type == X86_OP_IMM), None)
                if target is not None and section_name_for_va(base, sections, target) == ".text":
                    queue.append(target)
                if section_name_for_va(base, sections, next_va) == ".text":
                    queue.append(next_va)
                break
            if ins.mnemonic.startswith("ret"):
                break
    return {
        "blocks": block_count,
        "instructions": len(visited_ins),
        "api": api,
        "direct": direct,
        "globals": globals_seen,
    }


def exact_iat_opcode_sites(data, base, sections, iat_va):
    sec = next((s for s in sections if s["name"] == ".text"), None)
    if sec is None:
        return []
    blob = data[sec["raw"]:sec["raw"] + sec["raw_size"]]
    ptr = struct.pack("<I", iat_va & 0xFFFFFFFF)
    patterns = (("call", b"\xff\x15" + ptr), ("jmp", b"\xff\x25" + ptr))
    out = []
    for kind, pattern in patterns:
        start = 0
        while True:
            rel = blob.find(pattern, start)
            if rel < 0:
                break
            out.append((kind, base + sec["rva"] + rel))
            start = rel + 1
    return sorted(out, key=lambda x:(x[1],x[0]))


def exact_import_calls(data, base, sections, imports, dll_name, api_names):
    names = {str(x).lower() for x in api_names}
    out = []
    for iat_va, (dll, name) in imports.items():
        if dll.lower() != dll_name.lower() or name.lower() not in names:
            continue
        for hit in raw_text_pointer_hits(data, base, sections, iat_va):
            ins = recover_xref_instruction(data, base, sections, hit, iat_va)
            if ins is not None and ins.mnemonic == "call":
                out.append((iat_va, ins))
    uniq = {}
    for iat_va, ins in out:
        uniq[(iat_va, ins.address)] = (iat_va, ins)
    return [uniq[k] for k in sorted(uniq)]


def callback_probe(data, base, sections, imports, callback_va):
    rva = callback_va - base
    off = rva_to_offset(sections, rva)
    if off is None:
        return None
    blob = data[off:min(len(data), off + 0x1000)]
    api = collections.Counter()
    indirect = 0
    direct = collections.Counter()
    count = 0
    for ins in md().disasm(blob, callback_va, count=600):
        count += 1
        imp = imported_call(ins, imports)
        if imp:
            api[imp] += 1
        if ins.mnemonic == "call":
            seen_direct = False
            for op in ins.operands:
                if op.type == X86_OP_IMM:
                    direct[int(op.imm) & 0xFFFFFFFF] += 1
                    seen_direct = True
            if not seen_direct:
                indirect += 1
        if ins.mnemonic.startswith("ret"):
            break
    return {"instructions": count, "api": api, "direct": direct, "indirect": indirect}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bin", required=True)
    args = ap.parse_args()

    print("StoneAge Taiwan v1.0 protocol network-handoff probe — R1")
    print("SCOPE|ephemeral-verified-disc|identified-lssproto-send-indirect-handoff|derived-only")

    img, rows, layout, joliet = find_rows(args.bin)
    td = tempfile.TemporaryDirectory()
    root = Path(td.name)
    try:
        by_path = {r["path"]: r for r in rows if not r["is_dir"]}
        row = by_path.get("StoneAge/sa_3.exe")
        if row is None:
            raise SystemExit("sa_3.exe missing")
        exe = root / "sa_3.exe"
        extract_row(img, row, exe)
        data, pe, base, sections, imports = image_layout(exe)
        lo, hi = image_range(base, sections)
        text_sec, text_instructions = disassemble_text(data, base, sections)

        instructions, events, globals_seen = decode_helper(
            data, base, sections, imports, SEND_RVA
        )
        print(
            f"SEND_HELPER|rva=0x{SEND_RVA:x}|instructions={len(instructions)}|"
            f"globals={len(globals_seen)}|events={len(events)}"
        )
        for order, event in enumerate(events, 1):
            kind, addr, dll, name, value = event
            extra = ""
            if kind == "indirect_mem" and value is not None:
                extra = f"|global_rva=0x{value-base:x}|global_section={clean(section_name_for_va(base,sections,value))}"
            elif kind == "direct" and value is not None:
                extra = f"|target_rva=0x{value-base:x}"
            elif kind == "import":
                extra = f"|dll={clean(dll)}|api={clean(name)}"
            elif kind == "indirect_reg" and value is not None:
                extra = f"|reg_id={value}"
            print(
                f"SEND_EVENT|order={order}|kind={kind}|callsite_rva=0x{addr-base:x}{extra}"
            )

        init_va = base + INIT_RVA
        init_calls = direct_rel32_call_sites(data, base, sections, init_va)
        print(
            f"INIT_HELPER|rva=0x{INIT_RVA:x}|default_write_rva=0x{DEFAULT_WRITE_RVA:x}|"
            f"direct_callers={len(init_calls)}"
        )
        init_callback_candidates = set()
        for n, call_va in enumerate(init_calls, 1):
            print(f"INIT_CALL|n={n}|callsite_rva=0x{call_va-base:x}")
            paths = backward_paths(data, base, sections, call_va)
            for path_no, path in enumerate(paths, 1):
                pushed = []
                for prev in path:
                    candidate = immediate_text_push(prev, base, sections)
                    if candidate is not None:
                        pushed.append(candidate)
                if pushed:
                    nearest = pushed[-1]
                    init_callback_candidates.add(nearest)
                    print(
                        f"INIT_CALLBACK_CANDIDATE|callsite_rva=0x{call_va-base:x}|path={path_no}|"
                        f"callback_rva=0x{nearest-base:x}"
                    )
        for cb_va in sorted(init_callback_candidates):
            probed = callback_probe(data, base, sections, imports, cb_va)
            if probed is None:
                continue
            print(
                f"INIT_CALLBACK|callback_rva=0x{cb_va-base:x}|instructions={probed['instructions']}|"
                f"indirect_calls={probed['indirect']}|import_api_kinds={len(probed['api'])}|"
                f"direct_targets={len(probed['direct'])}"
            )
            for (dll, name), count in sorted(
                probed["api"].items(), key=lambda x:(x[0][0].lower(),x[0][1].lower())
            ):
                print(
                    f"INIT_CALLBACK_API|callback_rva=0x{cb_va-base:x}|dll={clean(dll)}|"
                    f"api={clean(name)}|calls={count}"
                )
            for target, count in sorted(probed["direct"].items()):
                sec_name = section_name_for_va(base, sections, target)
                if sec_name == ".text":
                    print(
                        f"INIT_CALLBACK_DIRECT|callback_rva=0x{cb_va-base:x}|"
                        f"target_rva=0x{target-base:x}|calls={count}"
                    )

        for cb_va in sorted(init_callback_candidates):
            cfg = callback_cfg_probe(data, base, sections, imports, cb_va)
            print(
                f"INIT_CALLBACK_CFG|callback_rva=0x{cb_va-base:x}|blocks={cfg['blocks']}|"
                f"instructions={cfg['instructions']}|globals={len(cfg['globals'])}|"
                f"import_api_kinds={len(cfg['api'])}|direct_targets={len(cfg['direct'])}"
            )
            for global_va, count in sorted(cfg["globals"].items()):
                print(
                    f"INIT_CALLBACK_GLOBAL|callback_rva=0x{cb_va-base:x}|"
                    f"global_rva=0x{global_va-base:x}|refs={count}"
                )
            for (dll, name), count in sorted(cfg["api"].items(), key=lambda x:(x[0][0].lower(),x[0][1].lower())):
                print(
                    f"INIT_CALLBACK_CFG_API|callback_rva=0x{cb_va-base:x}|dll={clean(dll)}|"
                    f"api={clean(name)}|calls={count}"
                )
            for target, count in sorted(cfg["direct"].items()):
                print(
                    f"INIT_CALLBACK_CFG_DIRECT|callback_rva=0x{cb_va-base:x}|"
                    f"target_rva=0x{target-base:x}|calls={count}"
                )

        wsock_imports = sorted(
            (iat_va, name) for iat_va, (dll, name) in imports.items()
            if dll.lower() == "wsock32.dll"
        )
        print(f"WSOCK_IMPORTS|count={len(wsock_imports)}")
        for iat_va, name in wsock_imports:
            print(f"WSOCK_IMPORT|iat_rva=0x{iat_va-base:x}|name={clean(name)}")
        send_iats = [
            iat_va for iat_va, (dll, name) in imports.items()
            if dll.lower() == "wsock32.dll" and name.lower() in {"send", "#19"}
        ]
        thunk_call_sites = []
        opcode_direct_sites = []
        for iat_va in send_iats:
            exact_sites = exact_iat_opcode_sites(data, base, sections, iat_va)
            print(
                f"WSOCK_SEND_IAT_OPCODE|iat_rva=0x{iat_va-base:x}|"
                f"exact_sites={len(exact_sites)}"
            )
            for kind, site_va in exact_sites:
                print(
                    f"WSOCK_SEND_IAT_SITE|iat_rva=0x{iat_va-base:x}|kind={kind}|"
                    f"instruction_rva=0x{site_va-base:x}"
                )
                if kind == "jmp":
                    callers = direct_rel32_call_sites(data, base, sections, site_va)
                    print(
                        f"WSOCK_SEND_THUNK|thunk_rva=0x{site_va-base:x}|"
                        f"direct_callers={len(callers)}"
                    )
                    thunk_call_sites.extend((iat_va, site_va, x) for x in callers)
                else:
                    opcode_direct_sites.append((iat_va, site_va, None))
            hits = raw_text_pointer_hits(data, base, sections, iat_va)
            print(f"WSOCK_SEND_IAT|iat_rva=0x{iat_va-base:x}|raw_text_xrefs={len(hits)}")
            for n, hit in enumerate(hits, 1):
                ins = recover_xref_instruction(data, base, sections, hit, iat_va)
                if ins is None:
                    print(
                        f"WSOCK_SEND_IAT_REF|iat_rva=0x{iat_va-base:x}|n={n}|"
                        f"pointer_rva=0x{hit['ptr_rva']:x}|decoded=0"
                    )
                    continue
                print(
                    f"WSOCK_SEND_IAT_REF|iat_rva=0x{iat_va-base:x}|n={n}|decoded=1|"
                    f"instruction_rva=0x{ins.address-base:x}|mnemonic={clean(ins.mnemonic)}|"
                    f"ops={clean(operand_summary(ins,base,sections))}"
                )
                if ins.mnemonic == "jmp":
                    callers = direct_rel32_call_sites(data, base, sections, ins.address)
                    print(
                        f"WSOCK_SEND_THUNK|thunk_rva=0x{ins.address-base:x}|"
                        f"direct_callers={len(callers)}"
                    )
                    thunk_call_sites.extend((iat_va, ins.address, x) for x in callers)
        send_import_calls = exact_import_calls(
            data, base, sections, imports, "WSOCK32.dll", {"send", "#19"}
        )
        combined_send_calls = [(iat_va, ins.address, None) for iat_va, ins in send_import_calls]
        combined_send_calls.extend(opcode_direct_sites)
        combined_send_calls.extend(thunk_call_sites)
        uniq_send = {}
        for iat_va, thunk_va, call_va in combined_send_calls:
            site = thunk_va if call_va is None else call_va
            uniq_send[(iat_va, site)] = (iat_va, site, call_va is not None, thunk_va)
        print(f"WSOCK_SEND|exact_calls={len(uniq_send)}")
        for n, (iat_va, send_site, via_thunk, thunk_va) in enumerate(
            [uniq_send[k] for k in sorted(uniq_send)], 1
        ):
            print(
                f"WSOCK_SEND_CALL|n={n}|callsite_rva=0x{send_site-base:x}|"
                f"iat_rva=0x{iat_va-base:x}|via_thunk={int(via_thunk)}|"
                f"thunk_rva=0x{thunk_va-base:x}"
            )
            paths = backward_paths(data, base, sections, send_site)
            ranked = sorted(
                enumerate(paths, 1),
                key=lambda item: (
                    -sum(1 for ins in item[1] if ins.mnemonic == "push"),
                    -len(item[1]),
                    item[0],
                ),
            )[:6]
            for path_no, path in ranked:
                for order, prev in enumerate(path, 1):
                    print(
                        f"WSOCK_SEND_PREV|callsite_rva=0x{send_site-base:x}|path={path_no}|"
                        f"order={order}|instruction_rva=0x{prev.address-base:x}|"
                        f"mnemonic={clean(prev.mnemonic)}|ops={clean(operand_summary(prev,base,sections))}"
                    )

        for global_va, refs_in_send in sorted(globals_seen.items()):
            if not (lo <= global_va < hi):
                continue
            hits = raw_text_pointer_hits(data, base, sections, global_va)[:MAX_GLOBAL_XREFS]
            print(
                f"GLOBAL|rva=0x{global_va-base:x}|section={clean(section_name_for_va(base,sections,global_va))}|"
                f"send_refs={refs_in_send}|text_raw_xrefs={len(hits)}"
            )
            callback_candidates = set()
            for n, hit in enumerate(hits, 1):
                ins = recover_xref_instruction(data, base, sections, hit, global_va)
                if ins is None:
                    print(
                        f"GLOBAL_XREF_UNDECODED|global_rva=0x{global_va-base:x}|n={n}|"
                        f"pointer_rva=0x{hit['ptr_rva']:x}"
                    )
                    continue
                details = assignment_details(ins, global_va, base, sections)
                print(
                    f"GLOBAL_XREF|global_rva=0x{global_va-base:x}|n={n}|"
                    f"instruction_rva=0x{ins.address-base:x}|mnemonic={clean(ins.mnemonic)}|"
                    f"assignment={int(details is not None)}"
                    + (
                        f"|src_kind={clean(details['src_kind'])}|"
                        f"src_value={'' if details['src_value'] is None else hex(details['src_value'])}|"
                        f"src_section={clean(details['src_section'])}"
                        if details is not None else ""
                    )
                )
                if details is not None and details["src_kind"] == "reg":
                    ctx = assignment_context(text_instructions, ins.address, base, sections)
                    print(
                        f"ASSIGN_CONTEXT|global_rva=0x{global_va-base:x}|"
                        f"assignment_rva=0x{ins.address-base:x}|src_reg={clean(ins.reg_name(details['src_value']))}|"
                        f"instructions={len(ctx)}"
                    )
                    for order, ctx_ins in enumerate(ctx, 1):
                        print(
                            f"ASSIGN_CTX|global_rva=0x{global_va-base:x}|assignment_rva=0x{ins.address-base:x}|"
                            f"order={order}|instruction_rva=0x{ctx_ins.address-base:x}|"
                            f"mnemonic={clean(ctx_ins.mnemonic)}|ops={clean(operand_summary(ctx_ins,base,sections))}"
                        )
                    paths = backward_paths(data, base, sections, ins.address)
                    print(
                        f"ASSIGN_BACKTRACE|global_rva=0x{global_va-base:x}|"
                        f"assignment_rva=0x{ins.address-base:x}|paths={len(paths)}|depth={BACKTRACE_DEPTH}"
                    )
                    for path_no, path in enumerate(paths, 1):
                        for order, prev in enumerate(path, 1):
                            print(
                                f"ASSIGN_PREV|global_rva=0x{global_va-base:x}|assignment_rva=0x{ins.address-base:x}|"
                                f"path={path_no}|order={order}|instruction_rva=0x{prev.address-base:x}|"
                                f"mnemonic={clean(prev.mnemonic)}|ops={clean(operand_summary(prev,base,sections))}"
                            )
                if (
                    details is not None
                    and details["src_kind"] == "imm"
                    and details["src_section"] == ".text"
                ):
                    callback_candidates.add(details["src_value"])

            for cb_va in sorted(callback_candidates):
                probed = callback_probe(data, base, sections, imports, cb_va)
                if probed is None:
                    continue
                print(
                    f"CALLBACK|global_rva=0x{global_va-base:x}|callback_rva=0x{cb_va-base:x}|"
                    f"instructions={probed['instructions']}|indirect_calls={probed['indirect']}|"
                    f"import_api_kinds={len(probed['api'])}|direct_targets={len(probed['direct'])}"
                )
                for (dll, name), count in sorted(
                    probed["api"].items(), key=lambda x:(x[0][0].lower(),x[0][1].lower())
                ):
                    print(
                        f"CALLBACK_API|callback_rva=0x{cb_va-base:x}|dll={clean(dll)}|"
                        f"api={clean(name)}|calls={count}"
                    )
    finally:
        img.close()
        td.cleanup()


if __name__ == "__main__":
    main()
