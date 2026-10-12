"""R17 original TW1.0 bounded write geometry, callee memory and nested-call frontier.

Historical bytes are read only after the pinned R16 hash and identity gates.
Every trace is *static*, and a heuristic CFG anchor is never a function entry.
No original disassembly, opcode bytes or historical asset leaves the runner.
"""
import argparse
import json
import tempfile
from pathlib import Path
from capstone.x86 import X86_OP_REG, X86_OP_MEM, X86_OP_IMM
from tools.stoneage_tw10_savedata_callee_global_r16 import (
    inspect_verified as inspect_r16, GLOBAL, RUNTIME_SHA256, SAVEDATA_SHA256)
from tools.stoneage_tw10_savedata_mutations_r13 import write_candidate
from tools.stoneage_tw10_savedata_reachdefs_r14 import bounded_graph
from tools.stoneage_tw10_savedata_inputs_r11 import reaches, semantic
from tools.stoneage_tw10_savedata_helper_effects_r8 import summarize
from tools.stoneage_tw10_savedata_provenance_r10 import memory_geometry
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH, SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows, extract_row

SCHEMA = "tw10-r17-original-static-write-and-memory-frontier"
STATUS = "CONDITIONAL_ORIGINAL_STATIC_SOURCE_AND_OWNERSHIP_OPEN"
WRITES = (0x49a2c, 0x49d78, 0x49e88)
# Bounded *candidate* anchors, not discovered function entries.
ANCHORS = {0x49a2c: 0x49a00, 0x49d78: 0x49d40, 0x49e88: 0x49e40}
GAP = 0x484c7
NESTED = (0x4e2a8, 0x4e2e1)
FLAGS = (
    "actual_function_entry_proven", "all_incoming_paths_proven",
    "global_actual_value_proven", "global_runtime_initialization_proven",
    "callee_memory_effect_admitted", "callee_return_summary_admitted",
    "nested_call_effects_admitted", "caller_resumption_admitted",
    "filename_api_link_proven", "handle_buffer_size_link_proven",
    "original_save_format_proven", "native_io_executed",
    "original_bytes_published",
)

def operand_shape(ins, op, sections, base):
    result = {"width_bytes": int(op.size), "decoder_read": bool(op.access & 1),
              "decoder_write": bool(op.access & 2)}
    if op.type == X86_OP_REG:
        result.update(kind="register", register=ins.reg_name(op.reg))
    elif op.type == X86_OP_IMM:
        result.update(kind="immediate", constant=int(op.imm))
    elif op.type == X86_OP_MEM:
        result.update(kind="memory", geometry=memory_geometry(ins, op, sections, base))
    else:
        result.update(kind="unmodeled")
    return result

def candidate_sources(dec, site, register, sections, anchor):
    """Optional graph-local syntactic sources; no complete entry or path claim."""
    nodes, edges, frontier, cap = bounded_graph(
        dec, anchor, max_span=192, max_nodes=128)
    item = {"candidate_anchor_rva": anchor, "anchor_is_verified_entry": False,
            "query_site_in_candidate_graph": site in nodes,
            "nodes": len(nodes), "edges": len(edges),
            "frontier": [{"reason": why, "rva": at} for why, at in frontier],
            "node_limit_hit": cap, "all_incoming_paths_proven": False,
            "call_fallthrough_structural_only": True,
            "reaching_candidates": [], "candidates_truncated": False,
            "value_known": False}
    if register is None or site not in nodes:
        return item
    tokens = sorted(reaches(nodes, edges, anchor, register).get(site, ()),
                    key=lambda v: (v[1], v[0]))
    item["candidates_truncated"] = len(tokens) > 24
    item["reaching_candidates"] = [
        {"origin": kind, "rva": at,
         "semantic": semantic(nodes[at], register, sections, dec.base)
         if kind == "definition" else None}
        for kind, at in tokens[:24]]
    return item

def inspect_static(dec, sections, writes=WRITES, gap=GAP, nested=NESTED,
                   anchors=ANCHORS, global_rva=GLOBAL):
    if len(set(writes)) != len(writes):
        raise ValueError("duplicate original write identity")
    result = []
    for site in writes:
        write = write_candidate(dec, site, sections, global_rva)
        # Treat decoder width/source as a candidate, not a value or runtime store.
        source = write["source_operand"]
        reg = source.get("register") if source and source["kind"] == "register_input" else None
        result.append({
            "site_rva": site, "write": write,
            "local_source_frontier": candidate_sources(
                dec, site, reg, sections, anchors[site]),
            "actual_value_proven": False, "executed_write_proven": False,
            "effective_object_owner_proven": False,
        })
    ins = dec.at(gap)
    if ins is None or not any(o.type == X86_OP_MEM for o in ins.operands):
        raise ValueError("R16 unresolved memory site no longer decodes as memory")
    blocked = {"site_rva": gap, "mnemonic_class": ins.mnemonic,
               "operand_shapes": [operand_shape(ins, o, sections, dec.base)
                                  for o in ins.operands],
               "register_writes": sorted(set(ins.reg_name(r)
                                             for r in ins.regs_access()[1])),
               "r8_unsupported_memory_gap_retained": True,
               "effective_address_and_owner_proven": False,
               "callee_effect_summary_admitted": False}
    callees = [{
        "root_rva": root, "bounded_effects": summarize(dec, root, max_states=96),
        "caller_arguments_known": False, "effective_effects_admitted": False,
    } for root in nested]
    return {"writes": result, "callee_memory_gap": blocked,
            "nested_callees": callees}

def inspect_verified(runtime, savedata):
    previous = inspect_r16(runtime, savedata)
    samples = previous["third_global_references"]["globals"][0]["samples"]
    actual = tuple(x["rva"] for x in samples if x["kind"] == "write_candidate")
    if actual != WRITES or previous["r15_upstream_global_rva"] != GLOBAL:
        raise ValueError("R16 pinned original global candidate identities changed")
    if [(x["root_rva"], x["summary"]["gap_sites"]) for x in
        previous["callee_frontiers"][:2]][0][1][0]["rva"] != GAP:
        raise ValueError("R16 callee original memory gap changed")
    nested_sites = previous["callee_frontiers"][1]["summary"]["gap_sites"]
    if tuple(x["direct_target_rva"] for x in nested_sites) != NESTED:
        raise ValueError("R16 nested callee identities changed")
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "sa_3.exe"
        p.write_bytes(runtime)
        data, pe, base, sections, _ = image_layout(p)
    for sec, raw_sec in zip(sections, pe.sections):
        sec["characteristics"] = int(raw_sec.Characteristics)
    t = next(s for s in sections if s["name"] == ".text")
    dec = Decoder(data[t["raw"]:t["raw"] + t["raw_size"]], t["rva"], base)
    report = inspect_static(dec, sections)
    return {"schema": SCHEMA, "status": STATUS,
            "runtime_sha256": RUNTIME_SHA256, "savedata_sha256": SAVEDATA_SHA256,
            "r16_original_identity_revalidated": True,
            "conditional_static_only": True,
            **report, **{k: False for k in FLAGS}}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--bin", type=Path, required=True)
    args = p.parse_args()
    image, rows, _, _ = find_rows(args.bin)
    try:
        paths = {row["path"]: row for row in rows if not row["is_dir"]}
        with tempfile.TemporaryDirectory() as td:
            exe, save = Path(td) / "sa_3.exe", Path(td) / "savedata.dat"
            extract_row(image, paths[RUNTIME_PATH], exe)
            extract_row(image, paths[SAVEDATA_PATH], save)
            report = inspect_verified(exe.read_bytes(), save.read_bytes())
    finally:
        image.close()
    print(json.dumps(report, sort_keys=True))

if __name__ == "__main__":
    main()
