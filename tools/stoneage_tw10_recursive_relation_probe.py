#!/usr/bin/env python3
"""Recursive bounded-code-window probe for Taiwan StoneAge v1.0 runtime relations.

This pass avoids depending on guessed global function boundaries. It starts at concrete
string/near-data xrefs, disassembles bounded windows from direct call targets, and follows
internal calls recursively to imported file/network APIs. Output is derived addresses and
API names only; no executable bytes or disassembly text are committed.
"""

from __future__ import annotations

import argparse
import collections
from pathlib import Path
import tempfile

from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from capstone.x86 import X86_OP_IMM

from tools.stoneage_tw10_technical_probe import find_rows, extract_row
from tools.stoneage_tw10_mapcache_binary_probe import (
    ALL_INTERESTING,
    image_layout,
    locate_strings,
    referenced_absolute_values,
    imported_call,
    rva_to_offset,
)

TARGETS = (
    b"map\\%d.dat",
    b"waei.bin",
    b"ClientLogin",
    b"CharLogin",
    b"data\\auto.dat",
    b"data\\mail.dat",
    b"data\\chatreg.dat",
    b"data\\album.dat",
)

SEARCH_RADII = (0, 0x20, 0x80, 0x200, 0x800, 0x2000)
MAX_ROOT_XREFS = 48
MAX_DEPTH = 5
MAX_NODES = 320
WINDOW_BYTES = 0x1000
MAX_INSNS = 1200

FILE_APIS = {
    "CreateFileA", "ReadFile", "WriteFile", "SetFilePointer", "SetEndOfFile",
    "CloseHandle", "CreateDirectoryA", "DeleteFileA",
}
NET_APIS = {
    "WSAStartup", "WSACleanup", "socket", "connect", "send", "recv", "select",
    "gethostbyname", "inet_addr", "htons", "closesocket", "ioctlsocket",
    "setsockopt", "WSAGetLastError", "__WSAFDIsSet",
}


def clean(value, limit=1000):
    text = " ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch >= " " and ch != "\x7f").replace("|", "%7C")[:limit]


def section_for_rva(sections, rva):
    for sec in sections:
        span = max(sec["vsize"], sec["raw_size"])
        if sec["rva"] <= rva < sec["rva"] + span:
            return sec
    return None


def disasm_window(data, base, sections, start_va):
    rva = start_va - base
    sec = section_for_rva(sections, rva)
    if not sec or sec["name"] != ".text":
        return []
    off = rva_to_offset(sections, rva)
    if off is None:
        return []
    sec_end = sec["raw"] + sec["raw_size"]
    blob = data[off:min(sec_end, off + WINDOW_BYTES)]
    md = Cs(CS_ARCH_X86, CS_MODE_32)
    md.detail = True
    return list(md.disasm(blob, start_va, count=MAX_INSNS))


def all_text_instructions(data, base, sections):
    sec = next((s for s in sections if s["name"] == ".text"), None)
    if not sec:
        raise ValueError("no .text")
    raw = data[sec["raw"]:sec["raw"] + sec["raw_size"]]
    md = Cs(CS_ARCH_X86, CS_MODE_32)
    md.detail = True
    return sec, list(md.disasm(raw, base + sec["rva"]))


def nearest_xrefs(instructions, target_va):
    rows = []
    for idx, ins in enumerate(instructions):
        for value in referenced_absolute_values(ins):
            delta = int(value) - int(target_va)
            rows.append((abs(delta), delta, idx, value))
    rows.sort(key=lambda x:(x[0], x[2]))
    return rows


def roots_for_target(instructions, target_va):
    nearest = nearest_xrefs(instructions, target_va)
    for radius in SEARCH_RADII:
        rows = [row for row in nearest if row[0] <= radius]
        if rows:
            # Deduplicate instruction indices; retain nearest operand delta per instruction.
            by_idx = {}
            for distance, delta, idx, value in rows:
                if idx not in by_idx or distance < by_idx[idx][0]:
                    by_idx[idx] = (distance, delta, value)
            chosen = [(idx,)+by_idx[idx] for idx in sorted(by_idx)]
            return radius, chosen[:MAX_ROOT_XREFS]
    return None, []


def direct_internal_targets(insns, text_lo, text_hi):
    out = collections.Counter()
    for ins in insns:
        if ins.mnemonic != "call":
            continue
        for op in ins.operands:
            if op.type == X86_OP_IMM:
                target = int(op.imm) & 0xFFFFFFFF
                if text_lo <= target < text_hi:
                    out[target] += 1
    return out


def analyze_window(data, base, sections, imports, start_va, text_lo, text_hi):
    insns = disasm_window(data, base, sections, start_va)
    api_counts = collections.Counter()
    for ins in insns:
        imp = imported_call(ins, imports)
        if imp:
            api_counts[imp] += 1
    internal = direct_internal_targets(insns, text_lo, text_hi)
    return {
        "start_va": start_va,
        "instructions": len(insns),
        "api_counts": api_counts,
        "internal": internal,
    }


def expand(data, base, sections, imports, roots, text_sec):
    text_lo = base + text_sec["rva"]
    text_hi = text_lo + text_sec["raw_size"]
    queue = collections.deque((va, 0) for va in roots)
    nodes = {}
    while queue and len(nodes) < MAX_NODES:
        va, depth = queue.popleft()
        if va in nodes:
            nodes[va]["depth"] = min(nodes[va]["depth"], depth)
            continue
        node = analyze_window(data, base, sections, imports, va, text_lo, text_hi)
        node["depth"] = depth
        nodes[va] = node
        if depth >= MAX_DEPTH:
            continue
        for target in node["internal"]:
            if target not in nodes:
                queue.append((target, depth + 1))
    return nodes


def aggregate_interesting(nodes):
    counts = collections.Counter()
    for node in nodes.values():
        for (dll, name), count in node["api_counts"].items():
            if name in ALL_INTERESTING:
                counts[(dll, name)] += count
    return counts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bin", required=True)
    args = ap.parse_args()

    print("StoneAge Taiwan v1.0 recursive runtime relation probe — R1")
    print("SCOPE|ephemeral-verified-disc|derived-code-window-callgraph-only|no-payload-commit")
    print(
        f"LIMIT|max_depth={MAX_DEPTH}|max_nodes={MAX_NODES}|window_bytes={WINDOW_BYTES}|"
        f"max_root_xrefs={MAX_ROOT_XREFS}"
    )

    img, rows, layout, joliet = find_rows(args.bin)
    td = tempfile.TemporaryDirectory()
    root = Path(td.name)
    try:
        by_path = {r["path"]:r for r in rows if not r["is_dir"]}
        src = by_path.get("StoneAge/sa_3.exe")
        if not src:
            raise SystemExit("sa_3.exe missing")
        exe = root / "sa_3.exe"
        extract_row(img, src, exe)

        data, pe, base, sections, imports = image_layout(exe)
        text_sec, instructions = all_text_instructions(data, base, sections)
        located = {row["text"].encode("ascii","replace"):row for row in locate_strings(data, base, sections)}

        print(
            f"FILESYSTEM|layout={layout}|joliet={int(joliet)}|runtime_bytes={exe.stat().st_size}|"
            f"image_base=0x{base:x}|text_rva=0x{text_sec['rva']:x}|"
            f"text_bytes={text_sec['raw_size']}|linear_instructions={len(instructions)}|imports={len(imports)}"
        )

        for target in TARGETS:
            label = target.decode("ascii","replace")
            row = located.get(target)
            if row is None or row["va"] is None:
                print(f"TARGET_MISSING|text={clean(label)}")
                continue

            radius, xrefs = roots_for_target(instructions, row["va"])
            root_vas = [instructions[idx].address for idx, *_ in xrefs]
            nodes = expand(data, base, sections, imports, root_vas, text_sec)
            interesting = aggregate_interesting(nodes)

            print(
                f"TARGET|text={clean(label)}|string_rva=0x{row['rva']:x}|"
                f"search_radius={'none' if radius is None else hex(radius)}|"
                f"root_xrefs={len(xrefs)}|graph_nodes={len(nodes)}"
            )
            for n,(idx,distance,delta,value) in enumerate(xrefs,1):
                print(
                    f"ROOT_XREF|text={clean(label)}|n={n}|xref_rva=0x{instructions[idx].address-base:x}|"
                    f"operand_rva=0x{value-base:x}|delta={delta}|distance={distance}"
                )

            for (dll,name),count in sorted(interesting.items(),key=lambda x:(x[0][0].lower(),x[0][1].lower())):
                cls = "file" if name in FILE_APIS else ("net" if name in NET_APIS else "other")
                print(
                    f"GRAPH_API|text={clean(label)}|class={cls}|dll={clean(dll)}|"
                    f"api={clean(name)}|calls={count}"
                )

            depths = collections.Counter(node["depth"] for node in nodes.values())
            for depth,count in sorted(depths.items()):
                print(f"GRAPH_DEPTH|text={clean(label)}|depth={depth}|nodes={count}")

            # Per-node output remains compact and purely structural.
            for va,node in sorted(nodes.items(),key=lambda kv:(kv[1]["depth"],kv[0])):
                interesting_node=[
                    (dll,name,count)
                    for (dll,name),count in node["api_counts"].items()
                    if name in ALL_INTERESTING
                ]
                if interesting_node or node["depth"] <= 1:
                    print(
                        f"NODE|text={clean(label)}|depth={node['depth']}|start_rva=0x{va-base:x}|"
                        f"instructions={node['instructions']}|internal_targets={len(node['internal'])}|"
                        f"interesting_imports={len(interesting_node)}"
                    )
                    for dll,name,count in sorted(interesting_node,key=lambda x:(x[0].lower(),x[1].lower())):
                        cls="file" if name in FILE_APIS else ("net" if name in NET_APIS else "other")
                        print(
                            f"NODE_API|text={clean(label)}|start_rva=0x{va-base:x}|class={cls}|"
                            f"dll={clean(dll)}|api={clean(name)}|calls={count}"
                        )
    finally:
        img.close()
        td.cleanup()


if __name__ == "__main__":
    main()
