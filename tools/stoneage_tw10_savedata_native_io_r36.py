"""R36: bounded TEST/JNE routes, opaque barriers and continuation stores.

Graph topology is derived metadata, not an executed path. Never apply a Windows
ABI, evaluate original EAX, or carry ESI through an opaque CALL as a real handle.
"""
import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from capstone import CS_GRP_CALL
from tools.stoneage_tw10_savedata_native_io_r35 import (
    inspect_verified as inspect_r35, RUNTIME_SHA256, SAVEDATA_SHA256,
    PARENT, ANCHOR, OPAQUE, TEST, CLOSE, FLAGS as R35_FLAGS,
)
from tools.stoneage_tw10_savedata_native_io_r35_guard import validate as validate_r35
from tools.stoneage_tw10_savedata_native_io_r33 import bounded_flag_sources
from tools.stoneage_tw10_savedata_native_io_r34 import shape
from tools.stoneage_tw10_savedata_native_io_r28 import candidate_graph, input_surface, ALIASES
from tools.stoneage_tw10_savedata_native_io_r30 import graph_meta
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder, direct_target
from tools.stoneage_tw10_savedata_frontier_r12 import call_identity
from tools.stoneage_tw10_savedata_write_shapes_r17 import operand_shape
from tools.stoneage_tw10_savedata_upstream_r23 import local_push_suffix
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH, SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows, extract_row

SCHEMA = "tw10-r36-original-test-jne-routes-barriers-continuation-stores"
STATUS = "PINNED_ORIGINAL_CONDITIONAL_BRANCH_TOPOLOGY_NATIVE_HANDLE_SAVE_OPEN"
PRIOR_SHA256 = "5052a3d57b89f1d257846df6cef7c513fe544cadeb420e11f0a18468d3908f23"
BRANCH = 0x4ed16
ERROR = 0x4ed1f
CONTINUATION = 0x4ed33
MAX_STORES = 24
FLAGS = tuple(R35_FLAGS) + (
    "actual_getfiletype_result_or_jne_outcome_proven",
    "same_push_register_establishes_same_handle_value",
    "continuation_store_executes_or_contains_api_handle",
    "route_reachability_establishes_runtime_feasibility",
)

def closure(edges, start, reverse=False):
    adjacency = {}
    for a, b in edges:
        if reverse:
            a, b = b, a
        adjacency.setdefault(a, set()).add(b)
    seen, todo = set(), [start]
    while todo:
        at = todo.pop()
        if at not in seen:
            seen.add(at)
            todo.extend(adjacency.get(at, ()))
    return seen

def route(topology, calls, start, goal):
    nodes, edges = set(topology["node_rvas"]), topology["edges"]
    corridor = (closure(edges, start) & closure(edges, goal, True) & nodes
                if start in nodes and goal in nodes else set())
    found = start in corridor and goal in corridor
    if not found:
        corridor = set()
    return {
        "start_rva": start, "goal_rva": goal,
        "structurally_reachable_in_bounded_graph": found,
        "corridor_node_rvas": sorted(corridor),
        "opaque_call_barrier_rvas": sorted(set(calls) & (corridor - {goal})),
        "returning_calls_assumed": True,
        "actual_feasible_path_or_register_preservation_proven": False,
    }

def branch_model(test_shape, branch_mnemonic):
    ops = test_shape["operands"]
    qualified = (test_shape["mnemonic"] == "test" and branch_mnemonic == "jne"
                 and len(ops) == 2 and all(o.get("kind") == "register"
                 and o.get("register") == "eax" and o.get("width_bytes") == 4 for o in ops))
    return {
        "qualified_test_eax_eax_jne_syntax": qualified,
        "symbolic_direct_edge_condition": "u32(EAX_at_TEST) != 0" if qualified else None,
        "symbolic_fallthrough_condition": "u32(EAX_at_TEST) == 0" if qualified else None,
        "original_eax_or_zf_evaluated": False,
        "actual_return_type_success_or_branch_outcome_proven": False,
    }

def derive(dec, sections, imports, prior):
    if prior.get("schema") != "tw10-r35-original-opaque-call-input-geometry":
        raise ValueError("R36 prior schema")
    nodes, edges, front, hit = candidate_graph(dec, PARENT)
    if not {TEST, BRANCH, CLOSE, ERROR, CONTINUATION} <= set(nodes):
        raise ValueError("R36 original branch/API continuation absent")
    branch = nodes[BRANCH]
    target, fall = direct_target(branch, dec.base), BRANCH + branch.size
    if branch.mnemonic != "jne" or target != CONTINUATION or fall != 0x4ed18:
        raise ValueError("R36 pinned JNE geometry changed")
    test_shape = shape(dec, sections, TEST, "test", ("eax", "eax"))
    sources, examined, cap, disconnected = bounded_flag_sources(nodes, edges, BRANCH)
    if sources != [(TEST, "zf_write")] or cap or disconnected:
        raise ValueError("R36 original unique TEST-to-JNE ZF source changed")
    topology = {"node_rvas": sorted(nodes), "edges": [list(e) for e in sorted(edges)],
                "complete_runtime_cfg_proven": False}
    calls = sorted(at for at, ins in nodes.items() if ins.group(CS_GRP_CALL))
    routes = [route(topology, calls, start, goal) for start in (target, fall)
              for goal in (CLOSE, ERROR, CONTINUATION)]
    suffix = local_push_suffix(dec, sections, ANCHOR, CLOSE)
    prior_suffix = prior["opaque_call_pre_call_suffix"]
    queries = {(TEST, "eax"), (BRANCH, "eax"), (CONTINUATION, "esi"),
               (CONTINUATION, "eax"), (0x4ed0d, "esi"), (0x4ed18, "esi")}
    forward = closure(edges, CONTINUATION) & set(nodes)
    stores = []
    for at in sorted(forward):
        ins = nodes[at]
        if ins.mnemonic != "mov" or len(ins.operands) != 2:
            continue
        ops = [operand_shape(ins, op, sections, dec.base) for op in ins.operands]
        if ops[0].get("kind") != "memory" or not ops[0].get("decoder_write"):
            continue
        regs = ([ops[1]["register"]] if ops[1].get("kind") == "register" else [])
        regs = sorted(set(regs) & set(ALIASES))
        if len(stores) < MAX_STORES:
            queries.update((at, r) for r in regs)
        stores.append({"site_rva": at, "mnemonic": "mov", "operands": ops,
                       "source_registers": regs, "actual_store_value_or_handle_owner_proven": False})
    return {
        "schema": SCHEMA, "status": STATUS,
        "runtime_sha256": RUNTIME_SHA256, "savedata_sha256": SAVEDATA_SHA256,
        "r35_exact_original_revalidated": True, "r35_exact_report_sha256": PRIOR_SHA256,
        "static_only": True, "parent_graph": graph_meta(nodes, edges, front, hit),
        "bounded_topology": topology,
        "branch": {"site_rva": BRANCH, "mnemonic": branch.mnemonic,
                   "direct_target_rva": target, "fallthrough_rva": fall},
        "test_shape": test_shape,
        "branch_flag_sources": {"candidates": [{"site_rva": at, "kind": kind} for at, kind in sources],
                                "predecessor_nodes_examined": examined, "predecessor_cap_hit": cap,
                                "branch_disconnected_in_graph": disconnected,
                                "actual_flag_value_known": False},
        "conditional_predicate": branch_model(test_shape, branch.mnemonic),
        "opaque_calls": [call_identity(dec, at, imports, sections) for at in calls],
        "routes": routes,
        "push_spelling_comparison": {
            "getfiletype_suffix": prior_suffix, "closehandle_suffix": suffix,
            "same_single_register_operand_shape": (
                len(prior_suffix["pushes"]) == len(suffix["pushes"]) == 1
                and prior_suffix["pushes"][0]["input"] == suffix["pushes"][0]["input"]),
            "actual_value_binding_or_callee_preservation_proven": False},
        "continuation_memory_stores": {"count": len(stores), "samples": stores[:MAX_STORES],
                                      "samples_truncated": len(stores) > MAX_STORES,
                                      "complete_alias_writers_or_initialization_proven": False},
        "input_sources": input_surface(dec, sections, nodes, edges, PARENT, queries),
        **{flag: False for flag in FLAGS},
    }

def inspect_verified(runtime, savedata):
    prior = inspect_r35(runtime, savedata)
    validate_r35(prior)
    digest = hashlib.sha256((json.dumps(prior, sort_keys=True) + "\n").encode()).hexdigest()
    if digest != PRIOR_SHA256:
        raise ValueError("R36 R35 exact original derivative changed")
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "sa_3.exe"
        p.write_bytes(runtime)
        data, pe, base, sections, imports = image_layout(p)
    for sec, raw in zip(sections, pe.sections):
        sec["characteristics"] = int(raw.Characteristics)
    code = next(s for s in sections if s["name"] == ".text")
    dec = Decoder(data[code["raw"]:code["raw"] + code["raw_size"]], code["rva"], base)
    return derive(dec, sections, imports, prior)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--bin", required=True, type=Path)
    image, rows, _, _ = find_rows(p.parse_args().bin)
    try:
        files = {r["path"]: r for r in rows if not r["is_dir"]}
        with tempfile.TemporaryDirectory() as td:
            exe, save = Path(td) / "sa_3.exe", Path(td) / "savedata.dat"
            extract_row(image, files[RUNTIME_PATH], exe)
            extract_row(image, files[SAVEDATA_PATH], save)
            result = inspect_verified(exe.read_bytes(), save.read_bytes())
    finally:
        image.close()
    print(json.dumps(result, sort_keys=True))

if __name__ == "__main__":
    main()
