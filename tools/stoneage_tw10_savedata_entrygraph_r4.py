#!/usr/bin/env python3
"""Bounded x86 entrypoint graph for the verified Taiwan 1.0 savedata four words.

This is a deliberately INCOMPLETE static recursive-descent graph. Lack of an
entrypoint path does not prove a target is data or unreachable in the real
executable: indirect transfers, callbacks, non-.text code, relocation and
self-modifying code are outside this graph. No original bytes are emitted.
"""
from __future__ import annotations

import argparse
from collections import Counter, deque
import json
from pathlib import Path
import tempfile

from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_GRP_CALL, CS_GRP_JUMP, CS_GRP_RET
from capstone.x86 import X86_OP_IMM

from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_technical_probe import find_rows, extract_row
from tools.stoneage_tw10_savedata_instruction_probe import (
    WORD_RVAS, EXPECTED_STRING_RVA, RUNTIME_SHA256, SAVEDATA_SHA256,
    verify_hash, validate_word, candidate_instructions
)
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH, SAVEDATA_PATH

MAX_NODES = 120000
MAX_PENDING = 200000
MAX_EDGES = 240000
CANDIDATE_STARTS = tuple(rva - 1 for rva in WORD_RVAS)


def explore(raw: bytes, text_rva: int, image_base: int, entry_rva: int,
            max_nodes: int = MAX_NODES):
    """Explore only direct .text control flow from the PE entry point.

    Each instruction address is visited once. Branch destinations and
    fallthroughs are tracked by exact decoded instruction boundaries, never
    guessed from linear-sweep alignment. 'not seen' is NOT a negative proof.
    """
    if not (0 < max_nodes <= MAX_NODES):
        raise ValueError("invalid graph node bound")
    text_hi = text_rva + len(raw)
    if not (text_rva <= entry_rva < text_hi):
        return {
            "entry_in_text": False, "visited": {}, "edges": set(),
            "statistics": {"entry_outside_text": 1}, "limit_hit": False,
        }
    md = Cs(CS_ARCH_X86, CS_MODE_32)
    md.detail = True
    work = deque([entry_rva])
    decoded = {}
    edges = set()
    count = Counter()
    limit_hit = False
    while work:
        if len(decoded) >= max_nodes or len(work) > MAX_PENDING or len(edges) > MAX_EDGES:
            limit_hit = True
            break
        rva = work.pop()
        if rva in decoded:
            continue
        if not text_rva <= rva < text_hi:
            count["outside_text"] += 1
            continue
        pos = rva - text_rva
        inst = next(md.disasm(raw[pos:pos+15], image_base+rva, count=1), None)
        if inst is None or inst.size == 0 or pos+inst.size > len(raw):
            count["decode_failure"] += 1
            continue
        decoded[rva] = inst.size
        mnemonic = inst.mnemonic
        stop = inst.group(CS_GRP_RET) or mnemonic in (
            "int", "int3", "into", "ud2", "hlt", "iret", "iretd")
        if stop:
            count["terminal_instruction"] += 1
            continue
        succ = []
        if inst.group(CS_GRP_CALL) or inst.group(CS_GRP_JUMP):
            targets = [int(op.imm) - image_base
                       for op in inst.operands if op.type == X86_OP_IMM]
            if not targets:
                count["indirect_transfer"] += 1
            for target in targets:
                if text_rva <= target < text_hi:
                    succ.append(target)
                else:
                    count["branch_target_outside_text"] += 1
            # A call can return; conditional branches have fallthrough.
            if inst.group(CS_GRP_CALL) or (
                    inst.group(CS_GRP_JUMP)
                    and mnemonic not in ("jmp", "ljmp")):
                succ.append(rva + inst.size)
        else:
            succ.append(rva + inst.size)
        for target in dict.fromkeys(succ):
            if not text_rva <= target < text_hi:
                count["fallthrough_outside_text"] += 1
                continue
            edges.add((rva, target))
            if target not in decoded:
                work.append(target)
    count["decoded_nodes"] = len(decoded)
    count["direct_or_fallthrough_edges"] = len(edges)
    count["pending_at_stop"] = len(work)
    return {"entry_in_text": True, "visited": decoded,
            "edges": edges, "statistics": dict(count), "limit_hit": limit_hit}


def summarize_sites(graph, text_rva, raw, image_base, target_va):
    visited = graph["visited"]
    edges = graph["edges"]
    sites = []
    for word_rva, cand_start in zip(WORD_RVAS, CANDIDATE_STARTS):
        possible = candidate_instructions(raw, image_base, text_rva,
                                          word_rva, target_va)
        if len(possible) != 1 or possible[0]["start"] != cand_start or (
                possible[0]["mnemonic"] != "push"):
            raise ValueError("original four-word R3 candidate identity changed")
        overlaps = sorted(start for start, size in visited.items()
                          if start < word_rva + 4 and start + size > word_rva)
        incoming = sum(int(dst == cand_start) for _, dst in edges)
        sites.append({
            "word_rva": f"0x{word_rva:x}",
            "push_candidate_start_rva": f"0x{cand_start:x}",
            "entrypoint_graph_candidate_seen": cand_start in visited,
            "entrypoint_graph_word_overlap_count": len(overlaps),
            "entrypoint_graph_incoming_edges": incoming,
            "independently_proven_executed_code": False,
            "data_ownership_proven": False,
        })
    return sites


def inspect_runtime(runtime: bytes, savedata: bytes):
    verify_hash(runtime, RUNTIME_SHA256, "sa_3.exe")
    verify_hash(savedata, SAVEDATA_SHA256, "savedata.dat")
    with tempfile.TemporaryDirectory() as directory:
        exe = Path(directory) / "sa_3.exe"
        exe.write_bytes(runtime)
        data, pe, image_base, sections, _imports = image_layout(exe)
    text = next((s for s in sections if s["name"] == ".text"), None)
    if text is None or text["raw_size"] <= 0:
        raise ValueError("original executable .text missing")
    raw = data[text["raw"]:text["raw"]+text["raw_size"]]
    if len(raw) != text["raw_size"]:
        raise ValueError("raw .text is truncated")
    target_va = image_base + EXPECTED_STRING_RVA
    for word in WORD_RVAS:
        validate_word(data, sections, word, target_va)
    entry_rva = int(pe.OPTIONAL_HEADER.AddressOfEntryPoint)
    graph = explore(raw, text["rva"], image_base, entry_rva)
    sites = summarize_sites(graph, text["rva"], raw, image_base, target_va)
    return {
        "schema": "tw10-savedata-four-word-entrygraph-r4",
        "scope": "verified-original-bytes-bounded-entrypoint-direct-graph",
        "runtime_sha256": RUNTIME_SHA256,
        "savedata_sha256": SAVEDATA_SHA256,
        "entry_rva": f"0x{entry_rva:x}",
        "text_rva": f"0x{text['rva']:x}",
        "text_raw_size": text["raw_size"],
        "entry_in_text": graph["entry_in_text"],
        "graph_limit_hit": graph["limit_hit"],
        "graph_statistics": graph["statistics"],
        "sites": sites,
        "original_runtime_reachability_admitted": False,
        "savedata_io_semantics_admitted": False,
        "fixed_128_byte_schema_admitted": False,
        "original_bytes_published": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bin", type=Path, required=True)
    args = parser.parse_args()
    img, rows, _, _ = find_rows(args.bin)
    try:
        paths = {row["path"]: row for row in rows if not row["is_dir"]}
        if RUNTIME_PATH not in paths or SAVEDATA_PATH not in paths:
            raise ValueError("original executable or savedata missing")
        with tempfile.TemporaryDirectory() as directory:
            exe = Path(directory) / "sa_3.exe"
            saved = Path(directory) / "savedata.dat"
            extract_row(img, paths[RUNTIME_PATH], exe)
            extract_row(img, paths[SAVEDATA_PATH], saved)
            result = inspect_runtime(exe.read_bytes(), saved.read_bytes())
    finally:
        img.close()
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
