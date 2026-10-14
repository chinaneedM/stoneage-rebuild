"""R37: CALL-supported continuation helpers and partial-register syntax.

Nonexecuting original inspection. Callers/callees are independent bounded
contexts; no actual stack parameter, callee result, handle or save is admitted.
"""
import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from capstone import CS_GRP_CALL
from tools.stoneage_tw10_savedata_native_io_r36 import (
    inspect_verified as inspect_r36, RUNTIME_SHA256, SAVEDATA_SHA256,
    PARENT, CONTINUATION, FLAGS as R36_FLAGS,
)
from tools.stoneage_tw10_savedata_native_io_r36_guard import validate as validate_r36
from tools.stoneage_tw10_savedata_native_io_r28 import candidate_graph, input_surface, ALIASES
from tools.stoneage_tw10_savedata_native_io_r30 import graph_meta
from tools.stoneage_tw10_savedata_write_shapes_r17 import operand_shape
from tools.stoneage_tw10_savedata_upstream_r23 import local_push_suffix
from tools.stoneage_tw10_savedata_frontier_r12 import call_identity
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH, SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows, extract_row

SCHEMA = "tw10-r37-original-continuation-helpers-partial-register-geometry"
STATUS = "PINNED_ORIGINAL_CONDITIONAL_HELPER_OPERANDS_NATIVE_HANDLE_SAVE_OPEN"
PRIOR_SHA256 = "872dbbf431891c19c27ddb0f6f5e87c466e89231e87e1a615a808aac0288a91c"
HELPERS = ((0x4ed49, 0x4e80a), (0x4ed87, 0x4c761))
PARTIAL_SITES = (0x4ed57, 0x4ed59, 0x4ed69)
STORE_SITES = (0x4ed5f, 0x4ed72, 0x4ed92)
MAX_MEMORY_REFS = 48
MAX_HELPER_CALLS = 24
SHARED = 0x1721760
FLAGS = tuple(R36_FLAGS) + (
    "caller_value_to_helper_parameter_binding_proven",
    "partial_syntax_establishes_original_whole_register_value",
    "shared_displacement_establishes_handle_table_or_owner",
    "helper_return_memory_or_native_save_effects_proven",
)

def family(reg):
    return next((key for key, names in ALIASES.items() if reg in names), None)

def operand_registers(op):
    if op.get("kind") == "register":
        names = [op.get("register")]
    else:
        geo = op.get("geometry") or {}
        names = [geo.get("base_register"), geo.get("index_register")]
    return sorted({family(r) for r in names} - {None})

def partial_model(row):
    """Architectural slice geometry only, never original-state arithmetic."""
    ops = row["operands"]
    dst = ops[0] if ops else {}
    reg = dst.get("register") if dst.get("kind") == "register" else None
    shift = 8 if reg in ("ah", "bh", "ch", "dh") else 0
    width = dst.get("width_bytes", 0)
    expected = (1 if reg in ("al", "ah", "bl", "bh", "cl", "ch", "dl", "dh")
                else 2 if reg in ("ax", "bx", "cx", "dx", "si", "di", "bp") else None)
    supported = (row["mnemonic"] in ("mov", "or", "and", "xor", "add", "sub", "inc", "dec")
                 and dst.get("decoder_write") is True and family(reg) is not None
                 and width == expected and expected is not None)
    mask = ((1 << (8 * width)) - 1) << shift if supported else None
    return {"qualified_partial_write_syntax": supported,
            "parent_register": family(reg) if supported else None,
            "written_operand_register": reg if supported else None,
            "slice_width_bits": 8 * width if supported else None,
            "slice_lsb_bit": shift if supported else None,
            "preserved_parent_bits_mask": 0xffffffff ^ mask if supported else None,
            "slice_operation": row["mnemonic"] if supported else None,
            "architecture_geometry_only": True,
            "evaluated_original_value_or_result": None,
            "actual_whole_register_or_memory_value_known": False}

def instruction_row(dec, sections, nodes, site):
    if site not in nodes:
        raise ValueError("R37 original operand site outside bounded graph")
    ins = nodes[site]
    ops = [operand_shape(ins, op, sections, dec.base) for op in ins.operands]
    reads, writes = ins.regs_access()
    names = sorted({ins.reg_name(r) for r in reads})
    queries = {family(r) for r in names} - {None}
    for op in ops:
        queries.update(operand_registers(op))
    return {"site_rva": site, "mnemonic": ins.mnemonic, "operands": ops,
            "decoder_read_registers": names,
            "decoder_written_registers": sorted({ins.reg_name(r) for r in writes}),
            "input_query_registers": sorted(queries),
            "actual_instruction_effect_or_value_known": False}

def memory_surface(dec, sections, imports, root):
    nodes, edges, front, hit = candidate_graph(dec, root)
    refs, calls, queries = [], [], set()
    for at, ins in sorted(nodes.items()):
        if ins.group(CS_GRP_CALL):
            calls.append(call_identity(dec, at, imports, sections))
        for n, op in enumerate(ins.operands):
            shaped = operand_shape(ins, op, sections, dec.base)
            if shaped["kind"] != "memory":
                continue
            geo = shaped["geometry"]
            regs = set(operand_registers(shaped))
            # Include source family for stores and register destination context
            # for loads. Reaching definitions remain pre-instruction candidates.
            for item in ins.operands:
                regs.update(operand_registers(operand_shape(ins, item, sections, dec.base)))
            if len(refs) < MAX_MEMORY_REFS:
                queries.update((at, r) for r in regs)
            refs.append({"site_rva": at, "operand_index": n, "mnemonic": ins.mnemonic,
                         "operand": shaped, "input_query_registers": sorted(regs),
                         "stack_or_frame_spelling_candidate": geo.get("base_register") in ("esp", "ebp"),
                         "shared_displacement_reference_candidate":
                             (geo.get("displacement_region") or {}).get("displacement_rva") == SHARED,
                         "actual_effective_address_value_owner_or_parameter_proven": False})
    return {"root_candidate_rva": root, "graph": graph_meta(nodes, edges, front, hit),
            "memory_reference_count": len(refs), "memory_references": refs[:MAX_MEMORY_REFS],
            "memory_references_truncated": len(refs) > MAX_MEMORY_REFS,
            "call_count": len(calls), "call_candidates": calls[:MAX_HELPER_CALLS],
            "calls_truncated": len(calls) > MAX_HELPER_CALLS,
            "input_sources": input_surface(dec, sections, nodes, edges, root, queries),
            "actual_function_entry_call_effect_or_complete_aliases_proven": False}

def boundary_candidates(dec):
    pos, decoded, gaps, starts = dec.lo, 0, 0, set()
    roots = {root for _, root in HELPERS}
    while pos < dec.hi:
        ins = dec.at(pos)
        if ins is None:
            gaps += 1
            pos += 1
            continue
        if pos in roots:
            starts.add(pos)
        decoded += 1
        pos += ins.size
    return {"scope": "full_raw_text_linear_decode_candidate_boundaries",
            "text_start_rva": dec.lo, "text_bytes": dec.hi - dec.lo,
            "decoded_instructions": decoded, "decode_gap_bytes": gaps,
            "roots": [{"root_rva": root, "linear_boundary_candidate": root in starts,
                       "true_function_entry_or_executed_alignment_proven": False}
                      for _, root in HELPERS],
            "complete_runtime_alignment_or_cfg_proven": False}

def derive(dec, sections, imports, prior):
    if prior.get("schema") != "tw10-r36-original-test-jne-routes-barriers-continuation-stores":
        raise ValueError("R37 prerequisite schema")
    nodes, edges, front, hit = candidate_graph(dec, PARENT)
    partial = [instruction_row(dec, sections, nodes, at) for at in PARTIAL_SITES]
    for row in partial:
        row["conditional_partial_model"] = partial_model(row)
    stores = [instruction_row(dec, sections, nodes, at) for at in STORE_SITES]
    queries = {(r["site_rva"], reg) for r in partial + stores for reg in r["input_query_registers"]}
    helpers = []
    old_calls = {r["call_rva"]: r for r in prior["opaque_calls"]}
    for call, root in HELPERS:
        ident = call_identity(dec, call, imports, sections)
        if ident != old_calls.get(call) or ident["kind"] != "direct" or ident["direct_target_rva"] != root:
            raise ValueError("R37 original direct CALL support changed")
        suffix = local_push_suffix(dec, sections, CONTINUATION, call)
        pushes = []
        for p in suffix["pushes"]:
            regs = operand_registers(p["input"])
            queries.update((p["site_rva"], reg) for reg in regs)
            pushes.append({**p, "input_query_registers": regs,
                           "actual_argument_role_value_or_binding_proven": False})
        queries.update((call, reg) for reg in ("eax", "esi", "ecx", "edi", "ebp"))
        helpers.append({"caller_call_identity": ident, "supported_by_exact_r36_original_call": True,
                        "pre_call_suffix": suffix, "push_candidates": pushes,
                        "callee_context": memory_surface(dec, sections, imports, root),
                        "actual_caller_callee_stack_or_value_binding_proven": False})
    return {"schema": SCHEMA, "status": STATUS,
            "runtime_sha256": RUNTIME_SHA256, "savedata_sha256": SAVEDATA_SHA256,
            "r36_exact_original_revalidated": True, "r36_exact_report_sha256": PRIOR_SHA256,
            "static_only": True, "parent_graph": graph_meta(nodes, edges, front, hit),
            "helper_boundary_candidates": boundary_candidates(dec),
            "partial_definition_shapes": partial, "continuation_store_shapes": stores,
            "helper_candidates": helpers,
            "caller_input_sources": input_surface(dec, sections, nodes, edges, PARENT, queries),
            **{flag: False for flag in FLAGS}}

def inspect_verified(runtime, savedata):
    prior = inspect_r36(runtime, savedata)
    validate_r36(prior)
    digest = hashlib.sha256((json.dumps(prior, sort_keys=True) + "\n").encode()).hexdigest()
    if digest != PRIOR_SHA256:
        raise ValueError("R37 R36 exact original derivative changed")
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
