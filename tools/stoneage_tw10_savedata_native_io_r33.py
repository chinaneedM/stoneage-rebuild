"""R33: original TW1.0 secondary CALL identity and bounded branch ZF sources.

Static PE only. Calls are opaque state/flag barriers. A graph-local possible
source never proves taken paths, actual return values, or original native save.
"""
import argparse
import hashlib
import json
import tempfile
from collections import deque
from pathlib import Path

from capstone import CS_GRP_CALL
from capstone import x86
from capstone.x86 import X86_OP_REG, X86_OP_MEM
from tools.stoneage_tw10_savedata_native_io_r32 import (
    inspect_verified as inspect_r32, derive as derive_r32,
    RUNTIME_SHA256, SAVEDATA_SHA256, PARENT, POST, CALL,
)
from tools.stoneage_tw10_savedata_native_io_r32_guard import validate as validate_r32
from tools.stoneage_tw10_savedata_native_io_r28 import candidate_graph, input_surface
from tools.stoneage_tw10_savedata_native_io_r30 import graph_meta
from tools.stoneage_tw10_savedata_frontier_r12 import call_identity
from tools.stoneage_tw10_savedata_write_shapes_r17 import operand_shape
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH, SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows, extract_row

SCHEMA = "tw10-r33-original-second-call-branch-zf-provenance"
STATUS = "PINNED_ORIGINAL_CONDITIONAL_ZF_CALL_PROVENANCE_NATIVE_SAVE_OPEN"
PRIOR_SHA256 = "24849b161be51b4fbf50fa7fe2c2bb48b6e79a6a83fb012f33ddd961f6336c9c"
SECONDARY = 0x4ed19
BRANCHES = (0x4ed0b, 0x4ed16)
MAX_SOURCE_SAMPLES = 24
MAX_PRED_NODES = 256
# Capstone's x86 instruction-details use independent action-bit flags for ZF.
ZF_WRITE_BITS = sum(getattr(x86, "X86_EFLAGS_" + action + "_ZF", 0)
                    for action in ("MODIFY", "SET", "RESET", "UNDEFINED"))
FLAGS = (
    "actual_branch_predicates_or_taken_paths_proven",
    "actual_error_code_or_file_api_result_proven",
    "actual_successful_handle_or_native_persistence_proven",
    "actual_stack_argument_alias_owner_or_callee_return_proven",
    "complete_original_eflags_paths_or_indirect_edges_proven",
    "original_runtime_executed",
    "original_proprietary_bytes_published",
)

def bounded_flag_sources(nodes, edges, branch):
    """Collect all candidate ZF definitions and opaque calls backwards.

    This is a may-reach model, not path feasibility. A CALL is conservatively
    an unknown-effects barrier, including where later ABI might preserve ZF.
    """
    incoming = {}
    for a, b in edges:
        incoming.setdefault(b, []).append(a)
    todo = deque([branch])
    seen = {branch}
    sources = []
    while todo and len(seen) <= MAX_PRED_NODES:
        at = todo.popleft()
        for prev in sorted(incoming.get(at, ())):
            if prev in seen:
                continue
            seen.add(prev)
            ins = nodes[prev]
            if ins.group(CS_GRP_CALL):
                sources.append((prev, "opaque_call"))
            elif int(getattr(ins, "eflags", 0)) & ZF_WRITE_BITS:
                sources.append((prev, "zf_write"))
            else:
                todo.append(prev)
    cap_hit = bool(todo) or len(seen) > MAX_PRED_NODES
    return sorted(set(sources)), len(seen), cap_hit, not bool(incoming.get(branch))

def operand_inputs(ins):
    """Small bounded register read surface for candidate ZF writers."""
    reads, _ = ins.regs_access()
    names = {ins.reg_name(r) for r in reads}
    return sorted(names & {"eax", "ebx", "ecx", "edx", "esi", "edi", "ebp"})

def branch_context(dec, sections, nodes, edges, old):
    site = old["site_rva"]
    if site not in BRANCHES or site not in nodes:
        raise ValueError("R33 branch identity not present")
    ins = nodes[site]
    if ins.mnemonic != old["mnemonic"]:
        raise ValueError("R33 original conditional mnemonic changed")
    sources, inspected, hit, disconnected = bounded_flag_sources(nodes, edges, site)
    samples = []
    queries = set()
    for rva, kind in sources[:MAX_SOURCE_SAMPLES]:
        src = nodes[rva]
        row = {"site_rva": rva, "kind": kind,
               "mnemonic": src.mnemonic if kind == "zf_write" else None,
               "candidate_actual_flag_value_known": False,
               "branch_predicate_or_taken_path_proven": False}
        if kind == "zf_write":
            row["operands"] = [operand_shape(src, op, sections, dec.base)
                               for op in src.operands[:3]]
            row["input_registers"] = operand_inputs(src)
            queries.update((rva, reg) for reg in row["input_registers"])
        else:
            row["operands"] = []
            row["input_registers"] = []
        samples.append(row)
    return {
        "branch_site_rva": site,
        "branch_mnemonic": old["mnemonic"],
        "direct_target_rva": old["direct_target_rva"],
        "fallthrough_rva": old["fallthrough_rva"],
        "source_count": len(sources),
        "source_candidates": samples,
        "candidates_truncated": len(sources) > MAX_SOURCE_SAMPLES,
        "predecessor_nodes_examined": inspected,
        "predecessor_cap_hit": hit,
        "branch_disconnected_in_graph": disconnected,
        "flag_source_model": "bounded_backward_ZF_may_def_CALL_opaque",
        "actual_predicate_value_or_feasible_path_proven": False,
        "operand_queries": queries,
    }

def derive(dec, sections, imports, prior):
    if prior["schema"] != "tw10-r32-original-intervening-call-branch-stack-geometry":
        raise ValueError("R33 prerequisite schema")
    nodes, edges, front, hit = candidate_graph(dec, PARENT)
    if not {SECONDARY, *BRANCHES} <= set(nodes):
        raise ValueError("R33 exact sites absent")
    sec = call_identity(dec, SECONDARY, imports, sections)
    branches = prior["branch_candidates"]
    if branches["truncated"] or branches["count"] != 2:
        raise ValueError("R33 exact R32 branches truncated or changed")
    old = {x["site_rva"]: x for x in branches["candidates"]}
    if set(old) != set(BRANCHES):
        raise ValueError("R33 expected original branch sites changed")
    contexts = [branch_context(dec, sections, nodes, edges, old[at]) for at in BRANCHES]
    queries = set()
    for row in contexts:
        queries.update(row.pop("operand_queries"))
    if len(queries) > 32:
        raise ValueError("R33 bounded flag source inputs exceeded")
    inputs = input_surface(dec, sections, nodes, edges, PARENT, queries)
    return {
        "schema": SCHEMA, "status": STATUS,
        "runtime_sha256": RUNTIME_SHA256,
        "savedata_sha256": SAVEDATA_SHA256,
        "r32_exact_original_revalidated": True,
        "r32_exact_report_sha256": PRIOR_SHA256,
        "static_only": True,
        "parent_graph": graph_meta(nodes, edges, front, hit),
        "secondary_call_identity": sec,
        "branch_flag_contexts": contexts,
        "flag_operand_input_surface": inputs,
        "all_flag_source_paths_or_effects_proven": False,
        **{key: False for key in FLAGS},
    }

def inspect_verified(runtime, savedata):
    prior = inspect_r32(runtime, savedata)
    validate_r32(prior)
    digest = hashlib.sha256((json.dumps(prior, sort_keys=True) + "\n").encode()).hexdigest()
    if digest != PRIOR_SHA256:
        raise ValueError("R32 exact original derivative changed")
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "sa_3.exe"
        path.write_bytes(runtime)
        data, pe, base, sections, imports = image_layout(path)
    for sec, raw in zip(sections, pe.sections):
        sec["characteristics"] = int(raw.Characteristics)
    text = next(s for s in sections if s["name"] == ".text")
    dec = Decoder(data[text["raw"]:text["raw"] + text["raw_size"]], text["rva"], base)
    return derive(dec, sections, imports, prior)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bin", type=Path, required=True)
    args = parser.parse_args()
    image, rows, _, _ = find_rows(args.bin)
    try:
        files = {r["path"]: r for r in rows if not r["is_dir"]}
        with tempfile.TemporaryDirectory() as td:
            exe, save = Path(td) / "sa_3.exe", Path(td) / "savedata.dat"
            extract_row(image, files[RUNTIME_PATH], exe)
            extract_row(image, files[SAVEDATA_PATH], save)
            report = inspect_verified(exe.read_bytes(), save.read_bytes())
    finally:
        image.close()
    print(json.dumps(report, sort_keys=True))

if __name__ == "__main__":
    main()
