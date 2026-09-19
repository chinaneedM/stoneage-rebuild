#!/usr/bin/env python3
"""Exact raw-string-xref forward-call probe for Taiwan StoneAge v1.0 sa_3.exe.

Uses the byte-exact string xref technique that previously found real references missed by
linear whole-.text disassembly. For every exact pointer occurrence in .text, recover the
containing x86 instruction, follow only forward code from that concrete point to a return,
then recursively follow direct call targets. This avoids broad proximity graphs.

Output is derived metadata only: RVAs, mnemonics, graph shape, and imported API names.
No executable/disc bytes or instruction operands are committed.
"""

from __future__ import annotations

import argparse
import collections
from pathlib import Path
import struct
import tempfile

from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from capstone.x86 import X86_OP_IMM

from tools.stoneage_tw10_technical_probe import find_rows, extract_row
from tools.stoneage_tw10_mapcache_binary_probe import (
    ALL_INTERESTING,
    image_layout,
    imported_call,
    referenced_absolute_values,
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

MAX_ROOTS_PER_TARGET = 16
MAX_DEPTH = 5
MAX_NODES = 120
MAX_NODE_BYTES = 0x1800
MAX_NODE_INSNS = 1000

FILE_APIS = {
    "CloseHandle", "CreateDirectoryA", "CreateFileA", "DeleteFileA",
    "ReadFile", "SetEndOfFile", "SetFilePointer", "WriteFile",
}
NET_APIS = {
    "WSAStartup", "WSACleanup", "socket", "connect", "send", "recv", "select",
    "gethostbyname", "inet_addr", "htons", "closesocket", "ioctlsocket",
    "setsockopt", "WSAGetLastError", "__WSAFDIsSet",
}


def clean(value, limit=900):
    text = " ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch >= " " and ch != "\x7f").replace("|", "%7C")[:limit]


def file_offset_to_rva(sections, off):
    for sec in sections:
        if sec["raw"] <= off < sec["raw"] + sec["raw_size"]:
            return sec["rva"] + (off - sec["raw"]), sec
    return None, None


def text_section(sections):
    sec = next((s for s in sections if s["name"] == ".text"), None)
    if sec is None:
        raise ValueError("no .text")
    return sec


def locate_target(data, base, sections, needle):
    pos = data.find(needle)
    if pos < 0:
        return None
    rva, sec = file_offset_to_rva(sections, pos)
    if rva is None:
        return None
    return {"file_offset": pos, "rva": rva, "va": base + rva, "section": sec["name"]}


def raw_text_pointer_hits(data, base, sections, target_va):
    sec = text_section(sections)
    blob = data[sec["raw"]:sec["raw"] + sec["raw_size"]]
    ptr = struct.pack("<I", target_va & 0xFFFFFFFF)
    hits = []
    start = 0
    while True:
        rel = blob.find(ptr, start)
        if rel < 0:
            break
        hits.append(
            {
                "ptr_file_offset": sec["raw"] + rel,
                "ptr_rva": sec["rva"] + rel,
                "ptr_va": base + sec["rva"] + rel,
            }
        )
        start = rel + 1
    return hits


def capstone():
    md = Cs(CS_ARCH_X86, CS_MODE_32)
    md.detail = True
    return md


def recover_xref_instruction(data, base, sections, hit, target_va):
    """Find an instruction whose encoded bytes contain the raw pointer and whose operand resolves to target."""
    ptr_off = hit["ptr_file_offset"]
    md = capstone()
    candidates = []
    for back in range(0, 16):
        start = ptr_off - back
        if start < 0:
            continue
        rva, sec = file_offset_to_rva(sections, start)
        if rva is None or sec["name"] != ".text":
            continue
        blob = data[start:min(len(data), start + 24)]
        insns = list(md.disasm(blob, base + rva, count=1))
        if not insns:
            continue
        ins = insns[0]
        ins_start = start
        ins_end = start + ins.size
        if not (ins_start <= ptr_off and ptr_off + 4 <= ins_end):
            continue
        refs = set(referenced_absolute_values(ins))
        if target_va not in refs:
            continue
        candidates.append((back, ins))
    if not candidates:
        return None
    # Prefer the candidate with the smallest back-distance, then shorter instruction.
    _, ins = sorted(candidates, key=lambda x: (x[0], x[1].size))[0]
    return ins


def section_for_va(base, sections, va):
    rva = va - base
    for sec in sections:
        span = max(sec["vsize"], sec["raw_size"])
        if sec["rva"] <= rva < sec["rva"] + span:
            return sec
    return None


def decode_forward_node(data, base, sections, imports, start_va):
    sec = section_for_va(base, sections, start_va)
    if sec is None or sec["name"] != ".text":
        return None
    off = rva_to_offset(sections, start_va - base)
    if off is None:
        return None
    sec_end = sec["raw"] + sec["raw_size"]
    blob = data[off:min(sec_end, off + MAX_NODE_BYTES)]
    md = capstone()
    insns = []
    api_counts = collections.Counter()
    internal = collections.Counter()
    end_reason = "limit"

    text = text_section(sections)
    text_lo = base + text["rva"]
    text_hi = text_lo + text["raw_size"]

    for ins in md.disasm(blob, start_va, count=MAX_NODE_INSNS):
        insns.append(ins)
        imp = imported_call(ins, imports)
        if imp:
            api_counts[imp] += 1
        if ins.mnemonic == "call":
            for op in ins.operands:
                if op.type == X86_OP_IMM:
                    target = int(op.imm) & 0xFFFFFFFF
                    if text_lo <= target < text_hi:
                        internal[target] += 1
        if ins.mnemonic.startswith("ret"):
            end_reason = "ret"
            break
        if ins.mnemonic in {"jmp"}:
            # Direct tail calls are graph edges; stop the linear node here to avoid
            # wandering into unrelated fall-through bytes.
            direct = False
            for op in ins.operands:
                if op.type == X86_OP_IMM:
                    target = int(op.imm) & 0xFFFFFFFF
                    if text_lo <= target < text_hi:
                        internal[target] += 1
                        direct = True
            if direct:
                end_reason = "tail-jmp"
                break

    return {
        "start_va": start_va,
        "end_va": insns[-1].address if insns else start_va,
        "instructions": len(insns),
        "api_counts": api_counts,
        "internal": internal,
        "end_reason": end_reason,
    }


def expand_from_exact_root(data, base, sections, imports, root_va):
    queue = collections.deque([(root_va, 0)])
    nodes = {}
    while queue and len(nodes) < MAX_NODES:
        va, depth = queue.popleft()
        if va in nodes:
            nodes[va]["depth"] = min(nodes[va]["depth"], depth)
            continue
        node = decode_forward_node(data, base, sections, imports, va)
        if node is None:
            continue
        node["depth"] = depth
        nodes[va] = node
        if depth >= MAX_DEPTH:
            continue
        for target in node["internal"]:
            if target not in nodes:
                queue.append((target, depth + 1))
    return nodes


def api_class(name):
    if name in FILE_APIS:
        return "file"
    if name in NET_APIS:
        return "net"
    return "other"


def aggregate(nodes):
    counts = collections.Counter()
    depth_hits = collections.defaultdict(set)
    for node in nodes.values():
        for (dll, name), count in node["api_counts"].items():
            if name in ALL_INTERESTING:
                counts[(dll, name)] += count
                depth_hits[(dll, name)].add(node["depth"])
    return counts, depth_hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bin", required=True)
    args = ap.parse_args()

    print("StoneAge Taiwan v1.0 exact-xref forward-call probe — R1")
    print("SCOPE|ephemeral-verified-disc|exact-raw-string-xref-callgraph|derived-metadata-only")
    print(
        f"LIMIT|max_roots={MAX_ROOTS_PER_TARGET}|max_depth={MAX_DEPTH}|max_nodes={MAX_NODES}|"
        f"max_node_bytes={MAX_NODE_BYTES}|max_node_insns={MAX_NODE_INSNS}"
    )

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
        text = text_section(sections)

        print(
            f"RUNTIME|bytes={exe.stat().st_size}|image_base=0x{base:x}|"
            f"text_rva=0x{text['rva']:x}|text_bytes={text['raw_size']}|imports={len(imports)}|"
            f"layout={layout}|joliet={int(joliet)}"
        )

        for needle in TARGETS:
            label = needle.decode("ascii", "replace")
            target = locate_target(data, base, sections, needle)
            if target is None:
                print(f"TARGET_MISSING|text={clean(label)}")
                continue
            hits = raw_text_pointer_hits(data, base, sections, target["va"])[:MAX_ROOTS_PER_TARGET]
            recovered = []
            for hit in hits:
                ins = recover_xref_instruction(data, base, sections, hit, target["va"])
                if ins is not None:
                    recovered.append((hit, ins))

            print(
                f"TARGET|text={clean(label)}|string_rva=0x{target['rva']:x}|"
                f"raw_text_xrefs={len(hits)}|decoded_xrefs={len(recovered)}"
            )

            combined_nodes = {}
            shared_root_targets = collections.Counter()
            for n, (hit, ins) in enumerate(recovered, 1):
                print(
                    f"XREF|text={clean(label)}|n={n}|pointer_rva=0x{hit['ptr_rva']:x}|"
                    f"instruction_rva=0x{ins.address-base:x}|mnemonic={clean(ins.mnemonic)}|"
                    f"instruction_size={ins.size}"
                )
                graph = expand_from_exact_root(data, base, sections, imports, ins.address)
                root_node = graph.get(ins.address)
                if root_node is not None:
                    for target_va, calls in sorted(root_node["internal"].items()):
                        shared_root_targets[target_va] += 1
                        print(
                            f"XREF_CALL|text={clean(label)}|n={n}|"
                            f"target_rva=0x{target_va-base:x}|calls={calls}"
                        )
                    for (dll, name), calls in sorted(
                        root_node["api_counts"].items(),
                        key=lambda x: (x[0][0].lower(), x[0][1].lower()),
                    ):
                        print(
                            f"XREF_DIRECT_API|text={clean(label)}|n={n}|"
                            f"dll={clean(dll)}|api={clean(name)}|calls={calls}"
                        )
                for va, node in graph.items():
                    prev = combined_nodes.get(va)
                    if prev is None or node["depth"] < prev["depth"]:
                        combined_nodes[va] = node
                counts, depths = aggregate(graph)
                print(
                    f"XREF_GRAPH|text={clean(label)}|n={n}|nodes={len(graph)}|"
                    f"max_depth={max((x['depth'] for x in graph.values()), default=0)}|"
                    f"interesting_api_kinds={len(counts)}"
                )
                for (dll, name), count in sorted(counts.items(), key=lambda x:(x[0][0].lower(),x[0][1].lower())):
                    print(
                        f"XREF_API|text={clean(label)}|n={n}|class={api_class(name)}|"
                        f"dll={clean(dll)}|api={clean(name)}|calls={count}|"
                        f"depths={','.join(str(d) for d in sorted(depths[(dll,name)]))}"
                    )

            counts, depths = aggregate(combined_nodes)
            for target_va, root_count in sorted(
                shared_root_targets.items(),
                key=lambda x: (-x[1], x[0]),
            ):
                print(
                    f"SHARED_ROOT_CALL|text={clean(label)}|target_rva=0x{target_va-base:x}|"
                    f"root_xrefs={root_count}"
                )
            print(
                f"TARGET_GRAPH|text={clean(label)}|nodes={len(combined_nodes)}|"
                f"interesting_api_kinds={len(counts)}"
            )
            for (dll, name), count in sorted(counts.items(), key=lambda x:(x[0][0].lower(),x[0][1].lower())):
                print(
                    f"TARGET_API|text={clean(label)}|class={api_class(name)}|"
                    f"dll={clean(dll)}|api={clean(name)}|calls={count}|"
                    f"depths={','.join(str(d) for d in sorted(depths[(dll,name)]))}"
                )
    finally:
        img.close()
        td.cleanup()


if __name__ == "__main__":
    main()
