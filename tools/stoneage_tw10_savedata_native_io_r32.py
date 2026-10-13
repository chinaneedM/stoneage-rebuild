"""TW1.0 R32: bounded original CALL/branch and conditional stack-slot candidates.

No original program is executed. Candidate-graph edges assume returning calls;
neither a feasible runtime path nor an API return/handle value is established.
"""
import argparse
import hashlib
import json
import tempfile
from collections import deque
from pathlib import Path

from capstone import CS_GRP_JUMP
from tools.stoneage_tw10_savedata_native_io_r31 import (
    inspect_verified as inspect_r31, PARENT, POST, CALL, HELPER,
    RUNTIME_SHA256, SAVEDATA_SHA256, FLAGS as R31_FLAGS
)
from tools.stoneage_tw10_savedata_native_io_r31_guard import validate as validate_r31
from tools.stoneage_tw10_savedata_native_io_r28 import candidate_graph, input_surface
from tools.stoneage_tw10_savedata_native_io_r30 import graph_meta
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder, direct_target
from tools.stoneage_tw10_savedata_frontier_r12 import call_identity
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH, SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows, extract_row

SCHEMA = "tw10-r32-original-intervening-call-branch-stack-geometry"
STATUS = "PINNED_ORIGINAL_CONDITIONAL_CALL_BRANCH_STACK_API_HANDLE_LINK_OPEN"
PRIOR_SHA256 = "af1e1ee0fb61549e89b6e168e82c5c7b58de170e9a1bb7f9ed2968c095cebdcc"
INTERVENING = 0x4ed1f
PUSH = 0x4ed25
MAX_BRANCHES = 24
FLAGS = tuple(R31_FLAGS) + (
    "intervening_call_effect_or_return_value_known",
    "conditional_branch_taken_or_real_path_proven",
    "caller_callee_actual_stack_or_argument_binding_proven",
    "captured_esi_actual_handle_owner_proven",
)

def reaches(edges, start, goal, cap=256):
    adjacency = {}
    for a, b in edges:
        adjacency.setdefault(a, set()).add(b)
    todo = deque([start])
    seen = set()
    while todo and len(seen) < cap:
        at = todo.popleft()
        if at == goal:
            return True
        if at not in seen:
            seen.add(at)
            todo.extend(sorted(adjacency.get(at, ())))
    return False

def branch_surface(nodes, edges):
    rows = []
    for at, ins in sorted(nodes.items()):
        if not POST <= at < CALL or not ins.group(CS_GRP_JUMP):
            continue
        if ins.mnemonic in ("jmp", "ljmp"):
            continue
        target = direct_target(ins, 0x400000)
        if target is None:
            continue
        fall = at + ins.size
        if not (reaches(edges, target, CALL) or reaches(edges, fall, CALL)):
            continue
        rows.append({
            "site_rva": at,
            "mnemonic": ins.mnemonic,
            "direct_target_rva": target,
            "fallthrough_rva": fall,
            "target_structurally_reaches_helper_call": reaches(edges, target, CALL),
            "fallthrough_structurally_reaches_helper_call": reaches(edges, fall, CALL),
            "branch_condition_or_actual_path_proven": False,
        })
    return {
        "count": len(rows), "candidates": rows[:MAX_BRANCHES],
        "truncated": len(rows) > MAX_BRANCHES,
        "returning_calls_assumed": True,
        "all_real_paths_or_indirect_edges_proven": False,
    }

def bridge_surface(prior):
    c = prior["caller_capture"]
    h = prior["helper_memory"]
    pushes = c["push_candidates"]
    refs = h["stack_reference_candidates"]
    p = next((x for x in pushes if x["site_rva"] == PUSH), None)
    mem = next((x for x in refs
                if x["site_rva"] == HELPER
                and x["operand"].get("geometry", {}).get("base_register") == "esp"
                and x["operand"]["geometry"].get("relative_field_offset") == 4), None)
    candidate = bool(
        len(pushes) == 1 and p
        and p["conditional_pre_call_esp_offset"] == 0
        and p["input"].get("kind") == "register"
        and p["input"].get("register") == "eax"
        and p["input"].get("width_bytes") == 4
        and mem and mem["operand"].get("width_bytes") == 4
    )
    return {
        "single_suffix_push_rva": PUSH if candidate else None,
        "callee_entry_stack_read_rva": HELPER if candidate else None,
        "conditional_hardware_call_slot_candidate": candidate,
        "caller_pre_call_esp_offset": 0 if candidate else None,
        "callee_entry_esp_relative_offset": 4 if candidate else None,
        "actual_taken_path_or_stack_contents_proven": False,
        "caller_callee_argument_binding_proven": False,
        "api_return_handle_link_proven": False,
    }

def derive(dec, sections, imports, prior):
    nodes, edges, front, hit = candidate_graph(dec, PARENT)
    if not {POST, INTERVENING, PUSH, CALL} <= set(nodes):
        raise ValueError("R32 candidate graph missing sites")
    call = call_identity(dec, INTERVENING, imports, sections)
    suffix = prior["caller_capture"]["local_push_suffix"]
    if not suffix["linear_call_boundary_reached"]:
        raise ValueError("R32 no bounded caller suffix")
    inputs = input_surface(dec, sections, nodes, edges, PARENT,
                           {(POST, "esi"), (INTERVENING, "esi"),
                            (INTERVENING, "eax"), (PUSH, "eax"),
                            (CALL, "esi")})
    return {
        "schema": SCHEMA,
        "status": STATUS,
        "runtime_sha256": RUNTIME_SHA256,
        "savedata_sha256": SAVEDATA_SHA256,
        "r31_exact_original_revalidated": True,
        "r31_exact_report_sha256": PRIOR_SHA256,
        "static_only": True,
        "parent_graph": graph_meta(nodes, edges, front, hit),
        "intervening_call_identity": call,
        "branch_candidates": branch_surface(nodes, edges),
        "conditional_slot": bridge_surface(prior),
        "parent_esi_eax_sources": inputs,
        "actual_entry_paths_frames_aliases_or_api_returns_proven": False,
        **{key: False for key in FLAGS},
    }

def inspect_verified(runtime, savedata):
    prior = inspect_r31(runtime, savedata)
    validate_r31(prior)
    digest = hashlib.sha256((json.dumps(prior, sort_keys=True) + "\n").encode()).hexdigest()
    if digest != PRIOR_SHA256:
        raise ValueError("R31 exact original derivative changed")
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "sa_3.exe"
        p.write_bytes(runtime)
        data, pe, base, sections, imports = image_layout(p)
    for section, raw in zip(sections, pe.sections):
        section["characteristics"] = int(raw.Characteristics)
    text = next(section for section in sections if section["name"] == ".text")
    dec = Decoder(data[text["raw"]:text["raw"]+text["raw_size"]],
                  text["rva"], base)
    return derive(dec, sections, imports, prior)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bin", type=Path, required=True)
    args = parser.parse_args()
    image, rows, _, _ = find_rows(args.bin)
    try:
        files = {row["path"]: row for row in rows if not row["is_dir"]}
        with tempfile.TemporaryDirectory() as td:
            exe = Path(td) / "sa_3.exe"
            savedata = Path(td) / "savedata.dat"
            extract_row(image, files[RUNTIME_PATH], exe)
            extract_row(image, files[SAVEDATA_PATH], savedata)
            report = inspect_verified(exe.read_bytes(), savedata.read_bytes())
    finally:
        image.close()
    print(json.dumps(report, sort_keys=True))

if __name__ == "__main__":
    main()
