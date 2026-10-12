#!/usr/bin/env python3
"""Conservative R5 native TW1.0 savedata callsite-neighborhood audit.

Input: ONLY SHA256-verified original retail sa_3.exe + savedata.dat.
Observed graph connections are possible static paths, never actual execution.
No original PE bytes, operand text, source code or game assets are emitted.
"""
from __future__ import annotations

import argparse
from collections import Counter, deque
import json
from pathlib import Path
import tempfile

from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_GRP_CALL, CS_GRP_JUMP, CS_GRP_RET

from tools.stoneage_tw10_savedata_entrygraph_r4 import (
    explore, CANDIDATE_STARTS, MAX_NODES
)
from tools.stoneage_tw10_savedata_instruction_probe import (
    RUNTIME_SHA256, SAVEDATA_SHA256, EXPECTED_STRING_RVA,
    WORD_RVAS, validate_word, verify_hash, candidate_instructions
)
from tools.stoneage_tw10_mapcache_binary_probe import (
    image_layout, imported_call
)
from tools.stoneage_tw10_savedata_probe import (
    FILE_APIS, RUNTIME_PATH, SAVEDATA_PATH
)
from tools.stoneage_tw10_technical_probe import find_rows, extract_row

MAX_FWD_RVA_SPAN = 2048
MAX_FWD_NODES = 256
MAX_API_EVENTS = 30
MAX_GRAPH_EDGES = 240000
MAX_HOPS = MAX_NODES


def shortest_paths(edges, entry):
    """Shortest potential graph paths, not taken or feasible runtime paths."""
    neighbors = {}
    for source, target in edges:
        neighbors.setdefault(source, []).append(target)
    distances = {entry: 0}
    pending = deque([entry])
    while pending:
        source = pending.popleft()
        for target in neighbors.get(source, ()):
            if target not in distances:
                distances[target] = distances[source] + 1
                pending.append(target)
    return distances


def predecessor_summary(site, decoded, edges):
    """Count only graph edges actually produced by the R4 decoder."""
    inbound = sorted(source for source, target in edges if target == site)
    return {
        "incoming_total": len(inbound),
        "incoming_sequential": sum(source + decoded[source] == site for source in inbound),
        "incoming_branch": sum(source + decoded[source] != site for source in inbound),
    }


def file_api_candidates(raw, base, text_rva, graph, site, imports,
                        max_nodes=MAX_FWD_NODES, span=MAX_FWD_RVA_SPAN):
    """Bounded graph-local API occurrences; NO argument or dataflow claim.

    Branches may be infeasible at runtime. Import-call lexical adjacency
    does not imply that the filename stack value reaches an API argument.
    """
    if not 1 <= max_nodes <= MAX_FWD_NODES or not 1 <= span <= MAX_FWD_RVA_SPAN:
        raise ValueError("file API audit bounds")
    decoded = graph["visited"]
    if site not in decoded:
        return {"visited_local": 0, "limit_hit": False, "api_events": [],
                "api_counts": {}, "createfilea_lexical_present": False}
    edge_map = {}
    for source, target in graph["edges"]:
        if site <= source < site + span and site <= target < site + span:
            edge_map.setdefault(source, []).append(target)
    md = Cs(CS_ARCH_X86, CS_MODE_32)
    md.detail = True
    q = deque([site])
    seen = set()
    events = []
    while q and len(seen) < max_nodes:
        rva = q.popleft()
        if rva in seen or rva not in decoded:
            continue
        if not site <= rva < site + span:
            continue
        offset = rva - text_rva
        if offset < 0 or offset >= len(raw):
            continue
        ins = next(md.disasm(raw[offset:offset+15], base+rva, count=1), None)
        if ins is None or ins.size != decoded[rva]:
            raise ValueError("R4 graph instruction-size drift")
        seen.add(rva)
        match = imported_call(ins, imports)
        if match and match[1] in FILE_APIS:
            if len(events) >= MAX_API_EVENTS:
                raise ValueError("bounded import-event list exceeded")
            events.append({"rva": f"0x{rva:x}", "api": match[1],
                           "dll": match[0]})
        q.extend(target for target in edge_map.get(rva, ()) if target not in seen)
    names = Counter(e["api"] for e in events)
    return {
        "visited_local": len(seen),
        "limit_hit": bool(q),
        "api_events": sorted(events, key=lambda r: (int(r["rva"], 16), r["api"])),
        "api_counts": dict(sorted(names.items())),
        "createfilea_lexical_present": names["CreateFileA"] > 0,
    }


def analyze_candidate_surfaces(raw, text_rva, base, graph, imports, entry_rva):
    dist = shortest_paths(graph["edges"], entry_rva)
    result = []
    for word, site in zip(WORD_RVAS, CANDIDATE_STARTS):
        plausible = candidate_instructions(raw, base, text_rva, word,
                                           base + EXPECTED_STRING_RVA)
        if (len(plausible) != 1 or plausible[0]["start"] != site
                or plausible[0]["mnemonic"] != "push"):
            raise ValueError("verified R3 candidate decode unexpectedly changed")
        if site not in graph["visited"]:
            raise ValueError("original R4 graph expectation changed")
        preds = predecessor_summary(site, graph["visited"], graph["edges"])
        nearby = file_api_candidates(raw, base, text_rva, graph, site, imports)
        result.append({
            "word_rva": f"0x{word:x}",
            "push_candidate_start_rva": f"0x{site:x}",
            "entrypoint_graph_min_hops": dist.get(site),
            "predecessors": preds,
            "local_graph": nearby,
            "actual_path_feasibility_proven": False,
            "filename_argument_to_file_api_proven": False,
            "native_read_write_size_proven": False,
        })
    return result


def inspect_verified(runtime: bytes, savedata: bytes):
    verify_hash(runtime, RUNTIME_SHA256, "sa_3.exe")
    verify_hash(savedata, SAVEDATA_SHA256, "savedata.dat")
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "sa_3.exe"
        path.write_bytes(runtime)
        data, pe, base, sections, imports = image_layout(path)
    text = next((s for s in sections if s["name"] == ".text"), None)
    if not text or text["raw_size"] <= 0:
        raise ValueError("original raw-backed .text missing")
    raw = data[text["raw"]:text["raw"] + text["raw_size"]]
    if len(raw) != text["raw_size"]:
        raise ValueError("original raw-backed .text truncated")
    for word in WORD_RVAS:
        validate_word(data, sections, word, base + EXPECTED_STRING_RVA)
    entry = int(pe.OPTIONAL_HEADER.AddressOfEntryPoint)
    graph = explore(raw, text["rva"], base, entry)
    if graph["limit_hit"] or not graph["entry_in_text"]:
        raise ValueError("original R4 entry graph truncated/outside section")
    if (len(graph["visited"]) != 31665 or len(graph["edges"]) != 35092):
        raise ValueError("accepted original R4 graph totals drift")
    return {
        "schema": "stoneage-tw10-savedata-r5-static-api-neighborhood",
        "status": "PINNED_ORIGINAL_STATIC_SURFACE_NOT_NATIVE_IO",
        "original_runtime_sha256": RUNTIME_SHA256,
        "original_savedata_sha256": SAVEDATA_SHA256,
        "entry_rva": f"0x{entry:x}",
        "r4_graph_nodes": len(graph["visited"]),
        "r4_graph_edges": len(graph["edges"]),
        "r4_graph_limit_hit": graph["limit_hit"],
        "sites": analyze_candidate_surfaces(raw, text["rva"], base, graph, imports, entry),
        "filename_argument_to_CreateFileA_proven": False,
        "ReadFile_WriteFile_buffer_size_proven": False,
        "native_save_io_executed": False,
        "original_bytes_published": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bin", type=Path, required=True)
    args = parser.parse_args()
    img, rows, _, _ = find_rows(args.bin)
    try:
        paths = {r["path"]: r for r in rows if not r["is_dir"]}
        if RUNTIME_PATH not in paths or SAVEDATA_PATH not in paths:
            raise ValueError("accepted original paths missing")
        with tempfile.TemporaryDirectory() as td:
            exe = Path(td) / "sa_3.exe"
            savedata = Path(td) / "savedata.dat"
            extract_row(img, paths[RUNTIME_PATH], exe)
            extract_row(img, paths[SAVEDATA_PATH], savedata)
            result = inspect_verified(exe.read_bytes(), savedata.read_bytes())
    finally:
        img.close()
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
