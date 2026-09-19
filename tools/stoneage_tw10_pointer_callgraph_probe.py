#!/usr/bin/env python3
"""Pointer-chain and bounded callgraph probe for Taiwan StoneAge v1.0 sa_3.exe.

Purpose:
- recover code references hidden behind data-pointer tables for map/login/server strings;
- expand internal call chains from those roots to file/network APIs;
- emit only derived addresses, graph metrics and API names.

The accepted retail payload is transient and never committed.
"""

from __future__ import annotations

import argparse
import collections
from pathlib import Path
import struct
import tempfile

from capstone.x86 import X86_OP_IMM

from tools.stoneage_tw10_technical_probe import find_rows, extract_row
from tools.stoneage_tw10_mapcache_binary_probe import (
    ALL_INTERESTING,
    image_layout,
    locate_strings,
    disassemble_text,
    referenced_absolute_values,
    imported_call,
    likely_function_window,
    direct_call_targets,
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

MAX_POINTER_DEPTH = 3
MAX_POINTER_HITS_PER_LEVEL = 128
MAX_CODE_XREFS = 64
MAX_CALL_DEPTH = 3
MAX_FUNCTIONS = 256


def clean(value, limit=1200):
    text = " ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch >= " " and ch != "\x7f").replace("|", "%7C")[:limit]


def section_for_offset(sections, off):
    for sec in sections:
        if sec["raw"] <= off < sec["raw"] + sec["raw_size"]:
            rva = sec["rva"] + (off - sec["raw"])
            return sec, rva
    return None, None


def pointer_occurrences(data, sections, va):
    needle = struct.pack("<I", va & 0xFFFFFFFF)
    out = []
    for sec in sections:
        # Pointer tables live in data/rdata-like sections; scanning .text would
        # duplicate direct immediate references handled by capstone.
        if sec["name"] == ".text":
            continue
        blob = data[sec["raw"]:sec["raw"] + sec["raw_size"]]
        start = 0
        while True:
            rel = blob.find(needle, start)
            if rel < 0:
                break
            off = sec["raw"] + rel
            rva = sec["rva"] + rel
            out.append(
                {
                    "file_offset": off,
                    "rva": rva,
                    "va": None,  # filled by caller using image base
                    "section": sec["name"],
                    "aligned4": int((off % 4) == 0),
                }
            )
            start = rel + 1
    return out


def pointer_chain(data, base, sections, target_va, max_depth=MAX_POINTER_DEPTH):
    """Return bounded layers of data locations that point to target/pointer VAs."""
    layers = []
    frontier = {target_va}
    seen_locations = set()
    for depth in range(1, max_depth + 1):
        layer = []
        next_frontier = set()
        for va in sorted(frontier):
            for hit in pointer_occurrences(data, sections, va):
                key = hit["file_offset"]
                if key in seen_locations:
                    continue
                seen_locations.add(key)
                hit = dict(hit)
                hit["points_to_va"] = va
                hit["va"] = base + hit["rva"]
                layer.append(hit)
                next_frontier.add(hit["va"])
                if len(layer) >= MAX_POINTER_HITS_PER_LEVEL:
                    break
            if len(layer) >= MAX_POINTER_HITS_PER_LEVEL:
                break
        layers.append(layer)
        if not next_frontier:
            break
        frontier = next_frontier
    return layers


def code_xrefs(instructions, candidate_vas):
    candidate_vas = set(candidate_vas)
    out = []
    for idx, ins in enumerate(instructions):
        values = set(referenced_absolute_values(ins))
        hits = sorted(values & candidate_vas)
        if hits:
            out.append((idx, hits))
    return out


def instruction_index_by_address(instructions):
    return {ins.address: idx for idx, ins in enumerate(instructions)}


def function_record(instructions, idx, imports, text_lo, text_hi):
    start, end, boundary = likely_function_window(instructions, idx)
    import_counts = collections.Counter()
    for ins in instructions[start:end + 1]:
        imp = imported_call(ins, imports)
        if imp:
            import_counts[imp] += 1

    directs = direct_call_targets(instructions, start, end, 0)
    internal = collections.Counter(
        {
            addr: count
            for addr, count in directs.items()
            if text_lo <= addr < text_hi
        }
    )
    return {
        "start_idx": start,
        "end_idx": end,
        "start_va": instructions[start].address,
        "end_va": instructions[end].address,
        "boundary": boundary,
        "instruction_count": end - start + 1,
        "imports": import_counts,
        "internal": internal,
    }


def expand_callgraph(instructions, root_indices, imports, base, text_sec):
    text_lo = base + text_sec["rva"]
    text_hi = text_lo + text_sec["raw_size"]
    by_addr = instruction_index_by_address(instructions)

    queue = collections.deque()
    visited = {}
    for idx in root_indices:
        rec = function_record(instructions, idx, imports, text_lo, text_hi)
        queue.append((rec, 0))

    while queue and len(visited) < MAX_FUNCTIONS:
        rec, depth = queue.popleft()
        key = rec["start_va"]
        if key in visited:
            visited[key]["min_depth"] = min(visited[key]["min_depth"], depth)
            continue
        rec["min_depth"] = depth
        visited[key] = rec
        if depth >= MAX_CALL_DEPTH:
            continue
        for target in rec["internal"]:
            idx = by_addr.get(target)
            if idx is None:
                continue
            child = function_record(instructions, idx, imports, text_lo, text_hi)
            queue.append((child, depth + 1))
    return visited


def summarize_api_calls(graph):
    counts = collections.Counter()
    for rec in graph.values():
        for (dll, name), count in rec["imports"].items():
            if name in ALL_INTERESTING:
                counts[(dll, name)] += count
    return counts


def direct_string_vas(row, layers):
    values = [row["va"]]
    for layer in layers:
        values.extend(hit["va"] for hit in layer)
    return [v for v in values if v is not None]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bin", required=True)
    args = ap.parse_args()

    print("StoneAge Taiwan v1.0 pointer-chain/callgraph probe — R1")
    print("SCOPE|ephemeral-verified-disc|derived-pointer-and-api-graph-only|no-payload-commit")
    print(
        f"LIMIT|max_pointer_depth={MAX_POINTER_DEPTH}|max_code_xrefs={MAX_CODE_XREFS}|"
        f"max_call_depth={MAX_CALL_DEPTH}|max_functions={MAX_FUNCTIONS}"
    )

    img, rows, layout, joliet = find_rows(args.bin)
    td = tempfile.TemporaryDirectory()
    root = Path(td.name)
    try:
        by_path = {r["path"]: r for r in rows if not r["is_dir"]}
        target = "StoneAge/sa_3.exe"
        if target not in by_path:
            raise SystemExit("sa_3.exe missing")
        exe = root / "sa_3.exe"
        extract_row(img, by_path[target], exe)

        data, pe, base, sections, imports = image_layout(exe)
        text_sec, instructions = disassemble_text(data, base, sections)
        print(
            f"FILESYSTEM|layout={layout}|joliet={int(joliet)}|runtime_bytes={exe.stat().st_size}|"
            f"image_base=0x{base:x}|text_rva=0x{text_sec['rva']:x}|text_bytes={text_sec['raw_size']}|"
            f"instructions={len(instructions)}|imports={len(imports)}"
        )

        located = {row["text"].encode("ascii", "replace"): row for row in locate_strings(data, base, sections)}

        global_api_counts = collections.Counter()
        for target_bytes in TARGETS:
            target_text = target_bytes.decode("ascii", "replace")
            row = located.get(target_bytes)
            if row is None or row["va"] is None:
                print(f"TARGET_MISSING|text={clean(target_text)}")
                continue

            layers = pointer_chain(data, base, sections, row["va"])
            chain_vas = direct_string_vas(row, layers)
            refs = code_xrefs(instructions, chain_vas)[:MAX_CODE_XREFS]
            root_indices = [idx for idx, _ in refs]
            graph = expand_callgraph(instructions, root_indices, imports, base, text_sec)
            api_counts = summarize_api_calls(graph)
            global_api_counts.update(api_counts)

            print(
                f"TARGET|text={clean(target_text)}|string_rva=0x{row['rva']:x}|"
                f"pointer_layers={len(layers)}|pointer_nodes={sum(len(x) for x in layers)}|"
                f"candidate_vas={len(chain_vas)}|code_xrefs={len(refs)}|functions={len(graph)}"
            )

            for depth, layer in enumerate(layers, 1):
                for hit in layer[:MAX_POINTER_HITS_PER_LEVEL]:
                    print(
                        f"POINTER|text={clean(target_text)}|depth={depth}|"
                        f"pointer_rva=0x{hit['rva']:x}|points_to_rva=0x{hit['points_to_va']-base:x}|"
                        f"section={clean(hit['section'])}|aligned4={hit['aligned4']}"
                    )

            for ordinal, (idx, values) in enumerate(refs, 1):
                start, end, boundary = likely_function_window(instructions, idx)
                print(
                    f"CODE_XREF|text={clean(target_text)}|n={ordinal}|"
                    f"xref_rva=0x{instructions[idx].address-base:x}|"
                    f"via_rvas={','.join('0x%x' % (v-base) for v in values)}|"
                    f"function_start_rva=0x{instructions[start].address-base:x}|"
                    f"function_end_rva=0x{instructions[end].address-base:x}|boundary={boundary}"
                )

            depth_counts = collections.Counter(rec["min_depth"] for rec in graph.values())
            for depth, count in sorted(depth_counts.items()):
                print(f"GRAPH_DEPTH|text={clean(target_text)}|depth={depth}|functions={count}")

            for (dll, name), count in sorted(api_counts.items(), key=lambda x: (x[0][0].lower(), x[0][1].lower())):
                print(
                    f"GRAPH_API|text={clean(target_text)}|dll={clean(dll)}|"
                    f"api={clean(name)}|calls={count}"
                )

            # Emit graph nodes only as addresses/metrics; no instruction bytes or disassembly.
            for rec in sorted(graph.values(), key=lambda r: (r["min_depth"], r["start_va"]))[:MAX_FUNCTIONS]:
                interesting = [
                    (dll, name, count)
                    for (dll, name), count in rec["imports"].items()
                    if name in ALL_INTERESTING
                ]
                print(
                    f"FUNCTION|text={clean(target_text)}|depth={rec['min_depth']}|"
                    f"start_rva=0x{rec['start_va']-base:x}|end_rva=0x{rec['end_va']-base:x}|"
                    f"boundary={rec['boundary']}|instructions={rec['instruction_count']}|"
                    f"internal_targets={len(rec['internal'])}|interesting_imports={len(interesting)}"
                )
                for dll, name, count in sorted(interesting, key=lambda x:(x[0].lower(),x[1].lower())):
                    print(
                        f"FUNCTION_API|text={clean(target_text)}|start_rva=0x{rec['start_va']-base:x}|"
                        f"dll={clean(dll)}|api={clean(name)}|calls={count}"
                    )

        print(f"COUNT|global_interesting_api_kinds|{len(global_api_counts)}")
        for (dll, name), count in sorted(global_api_counts.items(), key=lambda x:(x[0][0].lower(),x[0][1].lower())):
            print(f"GLOBAL_API|dll={clean(dll)}|api={clean(name)}|calls={count}")
    finally:
        img.close()
        td.cleanup()


if __name__ == "__main__":
    main()
