#!/usr/bin/env python3
"""Probe internal structure of key Taiwan StoneAge v1.0 gameplay callbacks.

Derived metadata only. The accepted retail sa_3.exe is transient.
"""

from __future__ import annotations

import argparse
import collections
from pathlib import Path
import struct
import tempfile

from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_OP_REG

from tools.stoneage_tw10_technical_probe import find_rows, extract_row
from tools.stoneage_tw10_mapcache_binary_probe import (
    image_layout,
    imported_call,
    rva_to_offset,
)
from tools.stoneage_tw10_protocol_handoff_probe import md, section_name_for_va

CALLBACKS = {
    "S": 0x2F670,
    "C": 0x31260,
    "I": 0x325F0,
    "WN": 0x328C0,
}

MAX_BLOCKS = 700
MAX_INSNS = 12000
MAX_BLOCK_INSNS = 400
MAX_BLOCK_BYTES = 0x1800


def clean(value, limit=500):
    text = " ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch >= " " and ch != "\x7f").replace("|", "%7C")[:limit]


def text_bounds(base, sections):
    sec = next(s for s in sections if s["name"] == ".text")
    return base + sec["rva"], base + sec["rva"] + max(sec["raw_size"], sec["vsize"])


def collect_cfg(data, base, sections, imports, start_rva):
    start_va = base + start_rva
    text_lo, text_hi = text_bounds(base, sections)
    queue = [start_va]
    visited_blocks = set()
    instructions = {}
    direct_calls = collections.Counter()
    import_calls = collections.Counter()
    indirect_jumps = []

    while queue and len(visited_blocks) < MAX_BLOCKS and len(instructions) < MAX_INSNS:
        block = queue.pop(0)
        if block in visited_blocks:
            continue
        if not (text_lo <= block < text_hi):
            continue
        visited_blocks.add(block)
        off = rva_to_offset(sections, block - base)
        if off is None:
            continue
        blob = data[off:min(len(data), off + MAX_BLOCK_BYTES)]
        local = []
        for ins in md().disasm(blob, block, count=MAX_BLOCK_INSNS):
            if ins.address in instructions:
                break
            instructions[ins.address] = ins
            local.append(ins)

            imp = imported_call(ins, imports)
            if imp:
                import_calls[imp] += 1

            if ins.mnemonic == "call":
                for op in ins.operands:
                    if op.type == X86_OP_IMM:
                        target = int(op.imm) & 0xFFFFFFFF
                        if text_lo <= target < text_hi:
                            direct_calls[target] += 1

            next_va = ins.address + ins.size
            if ins.mnemonic == "jmp":
                imm_target = next(
                    (int(op.imm) & 0xFFFFFFFF for op in ins.operands if op.type == X86_OP_IMM),
                    None,
                )
                if imm_target is not None and text_lo <= imm_target < text_hi:
                    queue.append(imm_target)
                else:
                    indirect_jumps.append((ins.address, ins))
                break
            if ins.mnemonic.startswith("j") and ins.mnemonic != "jmp":
                target = next(
                    (int(op.imm) & 0xFFFFFFFF for op in ins.operands if op.type == X86_OP_IMM),
                    None,
                )
                if target is not None and text_lo <= target < text_hi:
                    queue.append(target)
                if text_lo <= next_va < text_hi:
                    queue.append(next_va)
                break
            if ins.mnemonic.startswith("ret"):
                break

    return {
        "blocks": visited_blocks,
        "instructions": instructions,
        "direct_calls": direct_calls,
        "import_calls": import_calls,
        "indirect_jumps": indirect_jumps,
    }


def printable_immediate_events(base, cfg):
    out = []
    for addr, ins in cfg["instructions"].items():
        if ins.mnemonic not in {"cmp", "sub", "add", "and", "or", "xor", "test"}:
            continue
        for op in ins.operands:
            if op.type != X86_OP_IMM:
                continue
            value = int(op.imm) & 0xFFFFFFFF
            if 32 <= value <= 126:
                out.append((addr - base, ins.mnemonic, value, chr(value), ins.op_str))
    return sorted(set(out))


def indirect_jump_info(data, base, sections, cfg):
    text_lo, text_hi = text_bounds(base, sections)
    out = []
    ordered = sorted(cfg["instructions"])
    for addr, ins in cfg["indirect_jumps"]:
        mem_ops = [op for op in ins.operands if op.type == X86_OP_MEM]
        table_va = None
        if mem_ops:
            disp = int(mem_ops[0].mem.disp) & 0xFFFFFFFF
            if section_name_for_va(base, sections, disp) in {".text", ".rdata", ".data"}:
                table_va = disp
        context_addrs = [x for x in ordered if x < addr][-12:]
        context = [
            (
                a - base,
                cfg["instructions"][a].mnemonic,
                cfg["instructions"][a].op_str,
            )
            for a in context_addrs
        ]
        entries = []
        if table_va is not None:
            off = rva_to_offset(sections, table_va - base)
            if off is not None:
                invalid_run = 0
                for index in range(128):
                    pos = off + index * 4
                    if pos + 4 > len(data):
                        break
                    target = struct.unpack_from("<I", data, pos)[0]
                    if text_lo <= target < text_hi:
                        entries.append((index, target - base))
                        invalid_run = 0
                    else:
                        invalid_run += 1
                        if entries and invalid_run >= 8:
                            break
        out.append((addr - base, table_va - base if table_va else None, context, entries))
    return out


def s_char_switch(data, base, sections, cfg):
    """Decode the compact S callback dispatch over ASCII C..W.

    The accepted v1 callback normalizes data[0] by subtracting 'C', bounds it
    to 0x14, translates through a byte lookup table, then performs an indexed
    indirect jump through a dword target table. Return only derived mapping
    metadata.
    """
    if not cfg["indirect_jumps"]:
        return None
    jump_addr, jump_ins = cfg["indirect_jumps"][0]
    jump_mem = next((op for op in jump_ins.operands if op.type == X86_OP_MEM), None)
    if jump_mem is None:
        return None
    jump_table_va = int(jump_mem.mem.disp) & 0xFFFFFFFF
    if not section_name_for_va(base, sections, jump_table_va):
        return None

    lookup_va = None
    for addr in sorted(a for a in cfg["instructions"] if a < jump_addr)[-20:]:
        ins = cfg["instructions"][addr]
        if ins.mnemonic not in {"mov", "movzx", "movsx"}:
            continue
        for op in ins.operands:
            if op.type != X86_OP_MEM:
                continue
            disp = int(op.mem.disp) & 0xFFFFFFFF
            # The lookup source is an indexed byte read from image-backed data.
            if disp and section_name_for_va(base, sections, disp):
                lookup_va = disp
    if lookup_va is None:
        return None

    lookup_off = rva_to_offset(sections, lookup_va - base)
    jump_off = rva_to_offset(sections, jump_table_va - base)
    if lookup_off is None or jump_off is None:
        return None

    start_code = ord("C")
    count = ord("W") - start_code + 1
    lookup = list(data[lookup_off:lookup_off + count])
    if len(lookup) != count:
        return None
    max_slot = max(lookup) if lookup else -1
    targets = {}
    for slot in range(max_slot + 1):
        pos = jump_off + slot * 4
        if pos + 4 > len(data):
            break
        target_va = struct.unpack_from("<I", data, pos)[0]
        if section_name_for_va(base, sections, target_va) == ".text":
            targets[slot] = target_va - base

    categories = []
    for offset, slot in enumerate(lookup):
        categories.append(
            {
                "char": chr(start_code + offset),
                "char_code": start_code + offset,
                "slot": slot,
                "target_rva": targets.get(slot),
            }
        )
    return {
        "lookup_rva": lookup_va - base,
        "jump_table_rva": jump_table_va - base,
        "jump_ops": jump_ins.op_str,
        "lookup": lookup,
        "targets": targets,
        "categories": categories,
    }


def direct_call_target(ins):
    if ins.mnemonic != "call":
        return None
    for op in ins.operands:
        if op.type == X86_OP_IMM:
            return int(op.imm) & 0xFFFFFFFF
    return None


def callsite_stack_signature(base, cfg, target_va):
    """Collect derived caller-cleanup and nearby immediate push patterns."""
    ordered = sorted(cfg["instructions"])
    position = {addr: i for i, addr in enumerate(ordered)}
    rows = []
    for addr in ordered:
        ins = cfg["instructions"][addr]
        if direct_call_target(ins) != target_va:
            continue
        idx = position[addr]
        pushes = []
        # Only accept a short contiguous linear window before the call.
        previous = []
        cursor = idx - 1
        last_start = addr
        while cursor >= 0 and len(previous) < 12:
            paddr = ordered[cursor]
            pins = cfg["instructions"][paddr]
            if paddr + pins.size != last_start:
                break
            if pins.mnemonic.startswith("j") or pins.mnemonic == "call":
                break
            previous.append(pins)
            last_start = paddr
            cursor -= 1
        previous.reverse()
        for pins in previous:
            if pins.mnemonic != "push":
                continue
            imm = next(
                (int(op.imm) & 0xFFFFFFFF for op in pins.operands if op.type == X86_OP_IMM),
                None,
            )
            if imm is not None:
                pushes.append(imm)

        cleanup = None
        next_addr = addr + ins.size
        nxt = cfg["instructions"].get(next_addr)
        if nxt is not None and nxt.mnemonic == "add" and len(nxt.operands) >= 2:
            dst, src = nxt.operands[0], nxt.operands[1]
            if (
                dst.type == X86_OP_REG
                and nxt.reg_name(dst.reg).lower() == "esp"
                and src.type == X86_OP_IMM
            ):
                cleanup = int(src.imm) & 0xFFFFFFFF
        rows.append((addr - base, cleanup, tuple(pushes)))
    return rows


def helper_body_fingerprint(data, base, sections, imports, target_rva):
    cfg = collect_cfg(data, base, sections, imports, target_rva)
    rets = []
    for addr, ins in sorted(cfg["instructions"].items()):
        if ins.mnemonic.startswith("ret"):
            rets.append((addr - base, ins.op_str))
    return cfg, rets


def scaled_index_arithmetic(base, cfg):
    """Return compact derived index-multiplier evidence without raw disassembly."""
    rows = []
    for addr, ins in sorted(cfg["instructions"].items()):
        if ins.mnemonic == "lea" and len(ins.operands) >= 2:
            dst, src = ins.operands[0], ins.operands[1]
            if dst.type == X86_OP_REG and src.type == X86_OP_MEM:
                mem = src.mem
                if mem.scale in (2, 4, 8) and mem.index:
                    rows.append(
                        (
                            addr - base,
                            "lea",
                            ins.reg_name(dst.reg),
                            ins.reg_name(mem.base) if mem.base else "",
                            ins.reg_name(mem.index),
                            mem.scale,
                            int(mem.disp),
                        )
                    )
        elif ins.mnemonic == "imul" and len(ins.operands) >= 3:
            dst, src, imm = ins.operands[0], ins.operands[1], ins.operands[2]
            if dst.type == X86_OP_REG and src.type == X86_OP_REG and imm.type == X86_OP_IMM:
                value = int(imm.imm)
                if -128 <= value <= 128:
                    rows.append(
                        (
                            addr - base,
                            "imul",
                            ins.reg_name(dst.reg),
                            ins.reg_name(src.reg),
                            "",
                            value,
                            0,
                        )
                    )
    return rows


def call_prelude(base, cfg, target_va, limit=16):
    ordered = sorted(cfg["instructions"])
    pos = {addr: idx for idx, addr in enumerate(ordered)}
    rows = []
    for addr in ordered:
        ins = cfg["instructions"][addr]
        if direct_call_target(ins) != target_va:
            continue
        idx = pos[addr]
        seq = []
        cursor = idx - 1
        last_start = addr
        while cursor >= 0 and len(seq) < limit:
            paddr = ordered[cursor]
            pins = cfg["instructions"][paddr]
            if paddr + pins.size != last_start:
                break
            if pins.mnemonic.startswith("j") or pins.mnemonic == "call":
                break
            seq.append((paddr - base, pins.mnemonic, pins.op_str))
            last_start = paddr
            cursor -= 1
        seq.reverse()
        rows.append((addr - base, seq))
    return rows


def c_main_parse_profile(base, cfg):
    """Accepted-v1 legacy character/object record parse window.

    The main character branch begins with integer token 1 at 0x31307 and the
    next parser branch starts at 0x3167a. Emit only helper call positions and
    fixed immediate token indices from this bounded path.
    """
    roles = {
        0x46C70: "string_token",
        0x46DA0: "decimal_token",
        0x46DF0: "base62_convert",
        0x46FF0: "unescape",
        0x49566: "decimal_convert",
    }
    rows = []
    for addr, ins in sorted(cfg["instructions"].items()):
        rva = addr - base
        if not (0x31307 <= rva < 0x3167A):
            continue
        target = direct_call_target(ins)
        if target is None:
            continue
        trva = target - base
        role = roles.get(trva)
        if role is None:
            continue
        pushes = callsite_stack_signature(base, cfg, target)
        fixed = next((p for call_rva, _cleanup, p in pushes if call_rva == rva), ())
        rows.append((rva, trva, role, fixed))
    return rows


def bounded_instruction_window(base, cfg, start_rva, end_rva):
    rows = []
    for addr, ins in sorted(cfg["instructions"].items()):
        rva = addr - base
        if start_rva <= rva < end_rva:
            rows.append((rva, ins.mnemonic, ins.op_str))
    return rows


def shared_direct_targets(cfgs):
    memberships = collections.defaultdict(dict)
    for label, cfg in cfgs.items():
        for target, count in cfg["direct_calls"].items():
            memberships[target][label] = count
    return {
        target: counts
        for target, counts in memberships.items()
        if len(counts) >= 2
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bin", required=True)
    args = ap.parse_args()

    print("StoneAge Taiwan v1.0 gameplay callback structure probe — R1")
    print("SCOPE|accepted-retail-disc|derived-binary-metadata-only|no-payload")

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
        data, _pe, base, sections, imports = image_layout(exe)
        print(f"RUNTIME|image_base=0x{base:x}|layout={layout}|joliet={int(joliet)}")

        cfgs = {}
        s_branch_cfgs = {}
        for label, rva in CALLBACKS.items():
            cfg = collect_cfg(data, base, sections, imports, rva)
            cfgs[label] = cfg
            print(
                f"CALLBACK|name={label}|rva=0x{rva:x}|blocks={len(cfg['blocks'])}|"
                f"instructions={len(cfg['instructions'])}|direct_targets={len(cfg['direct_calls'])}|"
                f"import_targets={len(cfg['import_calls'])}|indirect_jumps={len(cfg['indirect_jumps'])}"
            )
            for target, count in sorted(
                cfg["direct_calls"].items(), key=lambda x: (-x[1], x[0])
            ):
                print(
                    f"DIRECT|name={label}|target_rva=0x{target-base:x}|calls={count}"
                )
            for (dll, api), count in sorted(
                cfg["import_calls"].items(), key=lambda x: (-x[1], x[0][0].lower(), x[0][1].lower())
            ):
                print(
                    f"IMPORT|name={label}|dll={clean(dll)}|api={clean(api)}|calls={count}"
                )
            for rva_event, mnemonic, value, char, ops in printable_immediate_events(base, cfg):
                print(
                    f"ASCII_IMM|name={label}|instruction_rva=0x{rva_event:x}|"
                    f"mnemonic={mnemonic}|value={value}|char={clean(char)}|ops={clean(ops)}"
                )
            if label == "I":
                for rva_event, kind, dst, base_reg, index_reg, scale, disp in scaled_index_arithmetic(base, cfg):
                    print(
                        f"INDEX_ARITH|name=I|instruction_rva=0x{rva_event:x}|kind={kind}|"
                        f"dst={dst}|base={base_reg}|index={index_reg}|scale={scale}|disp={disp}"
                    )
            for jump_rva, table_rva, context, entries in indirect_jump_info(
                data, base, sections, cfg
            ):
                jump_ins = next(
                    ins for addr, ins in cfg["indirect_jumps"]
                    if addr - base == jump_rva
                )
                print(
                    f"INDIRECT_JUMP|name={label}|instruction_rva=0x{jump_rva:x}|"
                    f"table_rva={'' if table_rva is None else hex(table_rva)}|entries={len(entries)}|"
                    f"ops={clean(jump_ins.op_str)}"
                )
                for order, (ctx_rva, mnemonic, ops) in enumerate(context, 1):
                    print(
                        f"JUMP_CONTEXT|name={label}|jump_rva=0x{jump_rva:x}|order={order}|"
                        f"instruction_rva=0x{ctx_rva:x}|mnemonic={mnemonic}|ops={clean(ops)}"
                    )
                for index, target_rva in entries:
                    print(
                        f"JUMP_TABLE|name={label}|jump_rva=0x{jump_rva:x}|index={index}|"
                        f"target_rva=0x{target_rva:x}"
                    )

            if label == "S":
                switch = s_char_switch(data, base, sections, cfg)
                if switch is not None:
                    print(
                        f"S_SWITCH|start=C|end=W|lookup_rva=0x{switch['lookup_rva']:x}|"
                        f"jump_table_rva=0x{switch['jump_table_rva']:x}|"
                        f"jump_ops={clean(switch['jump_ops'])}|"
                        f"lookup_slots={','.join(map(str, switch['lookup']))}|"
                        f"unique_slots={len(set(switch['lookup']))}|"
                        f"resolved_slots={len(switch['targets'])}"
                    )
                    seen_targets = {}
                    for item in switch["categories"]:
                        target = item["target_rva"]
                        print(
                            f"S_CATEGORY|char={item['char']}|code={item['char_code']}|"
                            f"slot={item['slot']}|target_rva={'' if target is None else hex(target)}"
                        )
                        if target is not None:
                            seen_targets.setdefault(target, []).append(item["char"])
                    for target_rva, chars in sorted(seen_targets.items()):
                        branch = collect_cfg(data, base, sections, imports, target_rva)
                        s_branch_cfgs[f"S:{','.join(chars)}"] = branch
                        print(
                            f"S_BRANCH|chars={','.join(chars)}|target_rva=0x{target_rva:x}|"
                            f"blocks={len(branch['blocks'])}|instructions={len(branch['instructions'])}|"
                            f"direct_targets={len(branch['direct_calls'])}"
                        )
                        for target, count in sorted(
                            branch["direct_calls"].items(),
                            key=lambda x: (-x[1], x[0]),
                        ):
                            print(
                                f"S_BRANCH_DIRECT|chars={','.join(chars)}|branch_rva=0x{target_rva:x}|"
                                f"target_rva=0x{target-base:x}|calls={count}"
                            )
                        if chars in (["I"], ["W"]):
                            for rva_event, kind, dst, base_reg, index_reg, scale, disp in scaled_index_arithmetic(base, branch):
                                print(
                                    f"INDEX_ARITH|name=S:{chars[0]}|instruction_rva=0x{rva_event:x}|"
                                    f"kind={kind}|dst={dst}|base={base_reg}|index={index_reg}|"
                                    f"scale={scale}|disp={disp}"
                                )

        # Dynamic token-helper preludes: enough to reconstruct j*N+k index arithmetic
        # without committing proprietary payload bytes.
        for label, cfg in (
            ("I", cfgs["I"]),
            ("S:I", s_branch_cfgs.get("I")),
            ("S:W", s_branch_cfgs.get("W")),
        ):
            if cfg is None:
                continue
            for helper_rva in (0x46C70, 0x46DA0):
                for call_rva, seq in call_prelude(
                    base, cfg, base + helper_rva, limit=18
                ):
                    print(
                        f"TOKEN_PRELUDE|name={label}|helper_rva=0x{helper_rva:x}|"
                        f"callsite_rva=0x{call_rva:x}|instructions={len(seq)}"
                    )
                    for order, (irva, mnemonic, ops) in enumerate(seq, 1):
                        print(
                            f"TOKEN_PRELUDE_INSN|name={label}|helper_rva=0x{helper_rva:x}|"
                            f"callsite_rva=0x{call_rva:x}|order={order}|"
                            f"instruction_rva=0x{irva:x}|mnemonic={mnemonic}|ops={clean(ops)}"
                        )

        # Compact arithmetic/control windows used to resolve dynamic token strides.
        for label, cfg, start_rva, end_rva in (
            ("I", cfgs["I"], 0x32650, 0x326B0),
            ("S:I", s_branch_cfgs.get("I"), 0x30922, 0x309B0),
            ("S:W", s_branch_cfgs.get("W"), 0x30B4F, 0x30BC0),
        ):
            if cfg is None:
                continue
            for irva, mnemonic, ops in bounded_instruction_window(
                base, cfg, start_rva, end_rva
            ):
                print(
                    f"PARSE_WINDOW|name={label}|instruction_rva=0x{irva:x}|"
                    f"mnemonic={mnemonic}|ops={clean(ops)}"
                )

        wn_cfg = cfgs["WN"]
        for call_rva, seq in call_prelude(base, wn_cfg, base + 0x12930):
            print(
                f"WN_FORWARD|callsite_rva=0x{call_rva:x}|target_rva=0x12930|"
                f"prelude_instructions={len(seq)}"
            )
            for order, (irva, mnemonic, ops) in enumerate(seq, 1):
                print(
                    f"WN_FORWARD_PRELUDE|order={order}|instruction_rva=0x{irva:x}|"
                    f"mnemonic={mnemonic}|ops={clean(ops)}"
                )

        for rva, target_rva, role, pushes in c_main_parse_profile(base, cfgs["C"]):
            print(
                f"C_MAIN_PARSE|callsite_rva=0x{rva:x}|target_rva=0x{target_rva:x}|"
                f"role={role}|immediate_pushes={','.join(hex(v) for v in pushes)}"
            )

        shared = shared_direct_targets(cfgs)
        analysis_cfgs = dict(cfgs)
        analysis_cfgs.update(s_branch_cfgs)
        for helper_rva in (0x46C70, 0x46DA0, 0x46E70, 0x46FF0):
            helper_va = base + helper_rva
            helper_cfg, helper_rets = helper_body_fingerprint(
                data, base, sections, imports, helper_rva
            )
            print(
                f"HELPER|rva=0x{helper_rva:x}|blocks={len(helper_cfg['blocks'])}|"
                f"instructions={len(helper_cfg['instructions'])}|"
                f"direct_targets={len(helper_cfg['direct_calls'])}|"
                f"import_targets={len(helper_cfg['import_calls'])}|"
                f"ret_sites={len(helper_rets)}"
            )
            for target, count in sorted(helper_cfg["direct_calls"].items()):
                print(
                    f"HELPER_DIRECT|rva=0x{helper_rva:x}|target_rva=0x{target-base:x}|"
                    f"calls={count}"
                )
            for (dll, api), count in sorted(helper_cfg["import_calls"].items()):
                print(
                    f"HELPER_IMPORT|rva=0x{helper_rva:x}|dll={clean(dll)}|"
                    f"api={clean(api)}|calls={count}"
                )
            for ret_rva, ops in helper_rets:
                print(
                    f"HELPER_RET|rva=0x{helper_rva:x}|instruction_rva=0x{ret_rva:x}|"
                    f"ops={clean(ops)}"
                )
            for label, cfg in analysis_cfgs.items():
                sigs = callsite_stack_signature(base, cfg, helper_va)
                if not sigs:
                    continue
                cleanup_counts = collections.Counter(
                    cleanup for _, cleanup, _ in sigs
                )
                print(
                    f"HELPER_CALLS|callback={label}|helper_rva=0x{helper_rva:x}|"
                    f"calls={len(sigs)}|cleanup_bytes="
                    + ",".join(
                        f"{'none' if key is None else key}:{count}"
                        for key, count in sorted(
                            cleanup_counts.items(),
                            key=lambda x: (-1 if x[0] is None else x[0]),
                        )
                    )
                )
                for call_rva, cleanup, pushes in sigs:
                    print(
                        f"HELPER_CALLSITE|callback={label}|helper_rva=0x{helper_rva:x}|"
                        f"callsite_rva=0x{call_rva:x}|"
                        f"cleanup_bytes={'' if cleanup is None else cleanup}|"
                        f"immediate_pushes={','.join(hex(v) for v in pushes)}"
                    )

        for target, counts in sorted(
            shared.items(),
            key=lambda x: (-sum(x[1].values()), x[0]),
        ):
            detail = ",".join(f"{name}:{counts[name]}" for name in sorted(counts))
            print(
                f"SHARED_DIRECT|target_rva=0x{target-base:x}|callbacks={len(counts)}|"
                f"calls={detail}|total={sum(counts.values())}"
            )
    finally:
        img.close()
        td.cleanup()


if __name__ == "__main__":
    main()
