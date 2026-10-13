"""R35: identify pinned TW1.0 opaque CALL 0x4ed0e and conditional input geometry.

Never execute original bytes. No x86 register value, stack ABI, handle ownership,
Windows API result, branch outcome, or native-save persistence is inferred.
"""
import argparse
import hashlib
import json
import tempfile
from pathlib import Path

from tools.stoneage_tw10_savedata_native_io_r34 import (
    inspect_verified as inspect_r34, RUNTIME_SHA256, SAVEDATA_SHA256,
    PARENT, ANCHOR, TEST, CALL as CLOSE, FLAGS as R34_FLAGS,
)
from tools.stoneage_tw10_savedata_native_io_r34_guard import validate as validate_r34
from tools.stoneage_tw10_savedata_native_io_r28 import candidate_graph, input_surface, ALIASES
from tools.stoneage_tw10_savedata_native_io_r30 import graph_meta
from tools.stoneage_tw10_savedata_upstream_r23 import local_push_suffix
from tools.stoneage_tw10_savedata_frontier_r12 import call_identity
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH, SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows, extract_row

SCHEMA = "tw10-r35-original-opaque-call-input-geometry"
STATUS = "PINNED_ORIGINAL_CONDITIONAL_CALL_IDENTITY_NATIVE_SAVE_OPEN"
PRIOR_SHA256 = "e95548eb5e9b60b1f5214ed751c1f3df9b83f27a4d20ebe35a49427cf9b32c34"
OPAQUE = 0x4ed0e
MAX_PUSHES = 24
FLAGS = tuple(R34_FLAGS) + (
    "opaque_call_runtime_invoked_or_return_known",
    "call_input_value_or_abi_binding_proven",
    "postcall_esi_eax_callee_preservation_proven",
    "filename_handle_buffer_length128_or_persistence_proven",
)

def source_queries(pushes):
    keys = {(OPAQUE, "eax"), (OPAQUE, "esi"), (OPAQUE, "edi"),
            (TEST, "eax"), (CLOSE, "esi")}
    results = []
    for p in pushes:
        op = p["input"]
        if op.get("kind") == "register":
            regs = [op.get("register")]
        else:
            geom = op.get("geometry") or {}
            regs = [geom.get("base_register"), geom.get("index_register")]
        regs = sorted({r for r in regs if r in ALIASES})
        results.append({**p,
                        "source_queries": [{"site_rva": p["site_rva"], "register": r}
                                           for r in regs],
                        "actual_argument_role_or_value_proven": False})
        keys.update((p["site_rva"], r) for r in regs)
    return sorted(keys), results

def derive(dec, sections, imports, previous):
    if previous.get("schema") != "tw10-r34-original-cmp-test-closehandle-input-provenance":
        raise ValueError("R35 R34 original prerequisite schema")
    nodes, edges, frontier, cap = candidate_graph(dec, PARENT)
    if not {OPAQUE, TEST, CLOSE} <= set(nodes):
        raise ValueError("R35 pinned original call/test/close sites outside graph")
    ins = dec.at(OPAQUE)
    if ins is None or ins.mnemonic != "call":
        raise ValueError("R35 exact opaque CALL instruction changed")
    identity = call_identity(dec, OPAQUE, imports, sections)
    if identity["kind"] not in ("direct", "memory_indirect", "register_indirect"):
        raise ValueError("R35 undecodable CALL target form")
    suffix = local_push_suffix(dec, sections, ANCHOR, OPAQUE)
    if not suffix["linear_call_boundary_reached"]:
        raise ValueError("R35 original anchor-to-CALL linear decode changed")
    if len(suffix["pushes"]) > MAX_PUSHES:
        raise ValueError("R35 push cap exceeded")
    queries, push_candidates = source_queries(suffix["pushes"])
    pre_post = input_surface(dec, sections, nodes, edges, PARENT, queries)
    return {
        "schema": SCHEMA, "status": STATUS,
        "runtime_sha256": RUNTIME_SHA256, "savedata_sha256": SAVEDATA_SHA256,
        "r34_exact_original_revalidated": True,
        "r34_exact_report_sha256": PRIOR_SHA256,
        "static_only": True,
        "parent_graph": graph_meta(nodes, edges, frontier, cap),
        "opaque_call_identity": identity,
        "opaque_call_pre_call_suffix": suffix,
        "opaque_call_push_candidates": push_candidates,
        "register_sources_before_and_after_call": pre_post,
        "call_is_opaque_register_and_effect_barrier": True,
        "returning_call_graph_is_structural_only": True,
        "actual_stack_paths_alias_and_return_proven": False,
        **{flag: False for flag in FLAGS},
    }

def inspect_verified(runtime, savedata):
    previous = inspect_r34(runtime, savedata)
    validate_r34(previous)
    digest = hashlib.sha256((json.dumps(previous, sort_keys=True) + "\n").encode()).hexdigest()
    if digest != PRIOR_SHA256:
        raise ValueError("R34 exact original derivative changed")
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "sa_3.exe"
        path.write_bytes(runtime)
        data, pe, base, sections, imports = image_layout(path)
    for section, raw in zip(sections, pe.sections):
        section["characteristics"] = int(raw.Characteristics)
    code = next(s for s in sections if s["name"] == ".text")
    dec = Decoder(data[code["raw"]:code["raw"] + code["raw_size"]], code["rva"], base)
    return derive(dec, sections, imports, previous)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bin", required=True, type=Path)
    args = parser.parse_args()
    image, rows, _, _ = find_rows(args.bin)
    try:
        mapping = {r["path"]: r for r in rows if not r["is_dir"]}
        with tempfile.TemporaryDirectory() as td:
            exe, save = Path(td) / "sa_3.exe", Path(td) / "savedata.dat"
            extract_row(image, mapping[RUNTIME_PATH], exe)
            extract_row(image, mapping[SAVEDATA_PATH], save)
            result = inspect_verified(exe.read_bytes(), save.read_bytes())
    finally:
        image.close()
    print(json.dumps(result, sort_keys=True))

if __name__ == "__main__":
    main()
