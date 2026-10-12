"""R14 bounded conditional register reaching-definitions for pinned TW1.0.

Starting instruction anchors are NOT independently established function entry
points. Call fallthrough is a structural assumption, never a callee summary.
External edges, decode gaps, missing sites and the graph bound are explicit.
No branch feasibility, stack ownership or native persistence is claimed.
"""
import argparse
import json
import tempfile
from collections import deque
from pathlib import Path
from capstone import CS_GRP_JUMP, CS_GRP_CALL, CS_GRP_RET
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder, direct_target
from tools.stoneage_tw10_savedata_inputs_r11 import reaches, semantic
from tools.stoneage_tw10_savedata_mutations_r13 import (
    inspect_verified as inspect_r13, HELPER, GLOBAL_WRITES, RUNTIME_SHA256,
    SAVEDATA_SHA256,
)
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH, SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows, extract_row

SCHEMA = "tw10-r14-bounded-conditional-reaching-definitions"
STATUS = "ORIGINAL_STATIC_BOUNDED_INPUTS_FUNCTION_OWNERSHIP_RUNTIME_OPEN"
MAX_NODES = 192
MAX_SPAN = 384
HELPER_ANCHOR = 0x49d93
GLOBAL_ANCHOR = 0x4943c
SITES = ((0x49dec, "ebx"), (0x4943c, "eax"), (0x4944a, "eax"),
         (0x49457, "esi"), (0x49463, "eax"))
FLAGS = (
    "actual_function_entry_proven",
    "frame_or_stack_ownership_proven",
    "global_initialization_proven",
    "branch_feasibility_proven",
    "complete_register_values_proven",
    "caller_effects_admitted",
    "global_effects_admitted",
    "heapalloc_size_or_ownership_proven",
    "filename_api_link_proven",
    "handle_buffer_size_link_proven",
    "native_io_executed",
    "fixed_128_byte_schema_proven",
    "original_bytes_published",
)

def bounded_graph(dec, root, max_span=MAX_SPAN, max_nodes=MAX_NODES):
    if not (1 <= max_span <= MAX_SPAN and 1 <= max_nodes <= MAX_NODES):
        raise ValueError("bounded region must be within R14 caps")
    q = deque([root])
    nodes, edges, boundary = {}, set(), set()
    while q and len(nodes) < max_nodes:
        rva = q.popleft()
        if rva in nodes:
            continue
        if not root <= rva < root + max_span:
            boundary.add(("out_of_window", rva))
            continue
        ins = dec.at(rva)
        if ins is None:
            boundary.add(("decode_gap", rva))
            continue
        nodes[rva] = ins
        if ins.group(CS_GRP_RET) or ins.mnemonic in (
            "int", "int3", "into", "ud2", "hlt", "iret", "iretd",
            "sysenter", "sysexit", "syscall", "sysret",
        ):
            continue
        if ins.group(CS_GRP_JUMP):
            target = direct_target(ins, dec.base)
            if target is None:
                boundary.add(("indirect_jump", rva))
                continue
            succ = [target]
            if ins.mnemonic not in ("jmp", "ljmp"):
                succ.append(rva + ins.size)
        else:
            # Every CALL is an opaque register barrier at its continuation.
            # This edge assumes a returning callee solely for exploration.
            succ = [rva + ins.size]
        for dst in sorted(set(succ)):
            edges.add((rva, dst))
            if dst not in nodes:
                q.append(dst)
    cap = any(root <= rva < root + max_span and rva not in nodes for rva in q)
    if cap:
        boundary.add(("node_cap", max_nodes))
    internal = {(a, b) for a, b in edges if a in nodes and b in nodes}
    return nodes, internal, sorted(boundary), bool(cap)

def probe_region(dec, root, queries, sections):
    nodes, edges, frontier, cap = bounded_graph(dec, root)
    maps = {reg: reaches(nodes, edges, root, reg) for _, reg in queries}
    answers = []
    for site, reg in queries:
        if site not in nodes:
            answers.append({"site_rva": site, "register": reg,
                            "reachable_in_bounded_graph": False,
                            "reaching_sources": [], "register_value_known": False})
            continue
        sources = []
        for origin, at in sorted(maps[reg].get(site, ()), key=lambda x: (x[1], x[0])):
            sources.append({"origin": origin, "rva": at,
                            "semantic": semantic(nodes[at], reg, sections, dec.base)
                            if origin == "definition" else None})
        answers.append({"site_rva": site, "register": reg,
                        "reachable_in_bounded_graph": True,
                        "reaching_sources": sources, "register_value_known": False})
    return {"anchor_rva": root, "anchor_is_verified_function_entry": False,
            "node_count": len(nodes), "edge_count": len(edges),
            "branch_sites": sorted(rva for rva, ins in nodes.items()
                                   if ins.group(CS_GRP_JUMP)),
            "call_barrier_sites": sorted(rva for rva, ins in nodes.items()
                                        if ins.group(CS_GRP_CALL)),
            "frontier": [{"reason": why, "rva": at} for why, at in frontier],
            "node_limit_hit": cap,
            "call_fallthrough_is_structural_only": True,
            "all_incoming_edges_proven": False,
            "inputs": answers}

def inspect_verified(runtime, savedata):
    prior = inspect_r13(runtime, savedata)
    if prior["schema"] != "tw10-r13-original-bounded-store-and-global-write-inputs":
        raise ValueError("R13 anchored identity changed")
    old = prior["store_candidates"]
    if [(x["site_rva"], x["source_operand"]["register"] if x["source_operand"] else None)
        for x in old if x["site_rva"] in dict(SITES)] != [
        (site, reg) for site, reg in SITES
    ]:
        raise ValueError("R13 selected source-register identity changed")
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "sa_3.exe"
        path.write_bytes(runtime)
        data, pe, base, sections, _ = image_layout(path)
    for sec, raw in zip(sections, pe.sections):
        sec["characteristics"] = int(raw.Characteristics)
    t = next(s for s in sections if s["name"] == ".text")
    dec = Decoder(data[t["raw"]:t["raw"]+t["raw_size"]], t["rva"], base)
    helper = probe_region(dec, HELPER_ANCHOR, SITES[:1], sections)
    globals_ = probe_region(dec, GLOBAL_ANCHOR, SITES[1:], sections)
    return {"schema": SCHEMA, "status": STATUS,
            "runtime_sha256": RUNTIME_SHA256,
            "savedata_sha256": SAVEDATA_SHA256,
            "prior_r13_status": prior["status"],
            "regions": [helper, globals_],
            "static_scope": "two-instruction-anchors-bounded-cfg-not-complete-functions",
            **{name: False for name in FLAGS}}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bin", type=Path, required=True)
    args = parser.parse_args()
    img, rows, _, _ = find_rows(args.bin)
    try:
        paths = {row["path"]: row for row in rows if not row["is_dir"]}
        with tempfile.TemporaryDirectory() as td:
            exe, save = Path(td)/"sa_3.exe", Path(td)/"savedata.dat"
            extract_row(img, paths[RUNTIME_PATH], exe)
            extract_row(img, paths[SAVEDATA_PATH], save)
            result = inspect_verified(exe.read_bytes(), save.read_bytes())
    finally:
        img.close()
    print(json.dumps(result, sort_keys=True))

if __name__ == "__main__":
    main()
