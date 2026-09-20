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

from capstone.x86 import X86_OP_IMM, X86_OP_MEM

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
            if section_name_for_va(base, sections, disp) in {".rdata", ".data"}:
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
            for jump_rva, table_rva, context, entries in indirect_jump_info(
                data, base, sections, cfg
            ):
                print(
                    f"INDIRECT_JUMP|name={label}|instruction_rva=0x{jump_rva:x}|"
                    f"table_rva={'' if table_rva is None else hex(table_rva)}|entries={len(entries)}"
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

        for target, counts in sorted(
            shared_direct_targets(cfgs).items(),
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
