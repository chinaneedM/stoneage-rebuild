"""R23: bounded original heap-call/global-store and local PUSH geometry.

No historical program is executed. A straight decoded suffix is a conditional
instruction sequence, not a verified entry, feasible path or Windows ABI proof.
Opaque CALLs still kill register values; equal global addresses do not establish
equal runtime contents, successful allocations or common heap ownership.
"""
import argparse
import json
import tempfile
from pathlib import Path
from capstone import CS_GRP_CALL, CS_GRP_JUMP, CS_GRP_RET
from capstone.x86 import X86_OP_REG, X86_OP_MEM
from tools.stoneage_tw10_savedata_upstream_r22 import (
    inspect_verified as inspect_r22, graph_path, RUNTIME_SHA256, SAVEDATA_SHA256)
from tools.stoneage_tw10_savedata_upstream_r22_guard import validate as validate_r22
from tools.stoneage_tw10_savedata_write_shapes_r17 import operand_shape, candidate_sources
from tools.stoneage_tw10_savedata_mutations_r13 import write_candidate
from tools.stoneage_tw10_savedata_reachdefs_r14 import bounded_graph
from tools.stoneage_tw10_savedata_frontier_r12 import call_identity
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH, SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows, extract_row

SCHEMA = "tw10-r23-original-heap-global-links-local-push-geometry"
STATUS = "PINNED_ORIGINAL_CONDITIONAL_STATIC_ONLY_HEAP_AND_NATIVE_IO_OPEN"
CALLS = (("HeapCreate", 0x499d0, 0x499d4, 0x499dc, 0x172187c, 0x520e8),
         ("HeapAlloc", 0x49a00, 0x49a0c, 0x49a14, 0x1721878, 0x520f8),
         ("HeapReAlloc", 0x4a0a0, 0x4a0c4, 0x4a0d5, 0x1721878, 0x520dc))
GLOBALS = (0x1721878, 0x172187c)
FLAGS = ("actual_entries_proven", "all_incoming_paths_proven",
         "runtime_path_feasible_proven", "call_return_value_admitted",
         "effective_global_values_proven", "stack_abi_slots_proven",
         "same_heap_owner_proven", "allocation_success_proven",
         "caller_resumption_admitted", "native_io_executed",
         "native_save_schema_proven", "original_bytes_published")

def local_push_suffix(dec, sections, anchor, call):
    """Decode an anchor-to-call straight sequence, then bound its final suffix.

    Only full-width PUSH and instructions not changing ESP/SP, transferring
    control, or writing memory can occur in the modeled suffix. Stores are
    barriers because stack aliases are unqualified. Offsets refer to ESP just
    BEFORE the CALL, never the callee's entry ESP or an argument signature.
    """
    cur = anchor
    sequence = []
    stop = None
    while cur < call and len(sequence) < 64 and cur - anchor < 192:
        ins = dec.at(cur)
        if ins is None or cur + ins.size > call:
            stop = "decode_or_boundary_gap"
            break
        sequence.append(ins)
        cur += ins.size
    if cur != call:
        return {"linear_call_boundary_reached": False, "stop_reason": stop or "bound",
                "pushes": [], "conditional_pre_call_esp_only": True,
                "abi_roles_applied": False, "actual_stack_values_known": False}
    pushes = []
    stop = "candidate_anchor"
    for ins in reversed(sequence):
        writes = {ins.reg_name(r) for r in ins.regs_access()[1]}
        if ins.group(CS_GRP_CALL) or ins.group(CS_GRP_JUMP) or ins.group(CS_GRP_RET):
            stop = "control_transfer"
            break
        if ins.mnemonic == "push" and len(ins.operands) == 1 and ins.operands[0].size == 4:
            op = ins.operands[0]
            pushes.append({"site_rva": ins.address - dec.base,
                           "conditional_pre_call_esp_offset": 4 * len(pushes),
                           "input": operand_shape(ins, op, sections, dec.base)})
            if len(pushes) == 24:
                stop = "push_cap"
                break
        elif (writes & {"esp", "sp", "spl"}
              or ins.mnemonic in ("enter", "leave", "pusha", "pushal", "pushf", "pushfd")
              or any(o.type == X86_OP_MEM and o.access & 2 for o in ins.operands)):
            stop = "stack_or_memory_barrier"
            break
    return {"linear_call_boundary_reached": True, "stop_reason": stop,
            "pushes": pushes, "conditional_pre_call_esp_only": True,
            "abi_roles_applied": False, "actual_stack_values_known": False}

def heap_link(dec, sections, imports, name, anchor, call, store, target, slot):
    identity = call_identity(dec, call, imports, sections)
    expected = {"dll": "KERNEL32.dll", "name": name, "iat_rva": slot}
    if identity["kind"] != "memory_indirect" or identity["import_identity"] != expected:
        raise ValueError("R23 pinned heap import changed")
    nodes, edges, frontier, cap = bounded_graph(dec, anchor, max_span=192, max_nodes=128)
    if call not in nodes or store not in nodes:
        raise ValueError("R23 call/store outside candidate graph")
    write = write_candidate(dec, store, sections, expected_global=target)
    if write["source_operand"].get("register") != "eax":
        raise ValueError("R23 global writer source changed")
    refs = []
    for at, ins in sorted(nodes.items()):
        if at >= call or ins.mnemonic != "push" or len(ins.operands) != 1:
            continue
        op = ins.operands[0]
        if op.type != X86_OP_MEM:
            continue
        shape = operand_shape(ins, op, sections, dec.base)
        geom = shape["geometry"]
        region = geom.get("displacement_region")
        if (not geom["base_register"] and not geom["index_register"]
            and not geom["segment_register"] and region
            and region["displacement_rva"] in GLOBALS):
            refs.append({"site_rva": at, "global_rva": region["displacement_rva"],
                         "operand": shape, "graph_path_to_call": graph_path(edges, at, call)})
    return {"name": name, "anchor_rva": anchor, "call_rva": call,
            "store_rva": store, "target_global_rva": target,
            "call_identity": identity, "write": write,
            "nodes": len(nodes), "edges": len(edges), "node_cap": cap,
            "frontier": [{"reason": why, "rva": at} for why, at in frontier],
            "structural_call_to_store": graph_path(edges, call, store),
            "store_eax_sources": candidate_sources(dec, store, "eax", sections, anchor),
            "global_push_candidates": refs,
            "local_push_suffix": local_push_suffix(dec, sections, anchor, call),
            "call_is_opaque_value_barrier": True,
            "same_address_not_same_runtime_heap": True,
            "runtime_return_or_write_known": False,
            "heap_owner_or_success_known": False}

def inspect_verified(runtime, savedata):
    validate_r22(inspect_r22(runtime, savedata))
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "sa_3.exe"
        p.write_bytes(runtime)
        data, pe, base, sections, imports = image_layout(p)
    for sec, raw in zip(sections, pe.sections):
        sec["characteristics"] = int(raw.Characteristics)
    t = next(s for s in sections if s["name"] == ".text")
    dec = Decoder(data[t["raw"]:t["raw"] + t["raw_size"]], t["rva"], base)
    return {"schema": SCHEMA, "status": STATUS,
            "runtime_sha256": RUNTIME_SHA256, "savedata_sha256": SAVEDATA_SHA256,
            "r22_original_identity_revalidated": True, "static_only": True,
            "heap_links": [heap_link(dec, sections, imports, *row) for row in CALLS],
            **{key: False for key in FLAGS}}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--bin", type=Path, required=True)
    image, rows, _, _ = find_rows(p.parse_args().bin)
    try:
        files = {row["path"]: row for row in rows if not row["is_dir"]}
        with tempfile.TemporaryDirectory() as td:
            exe, saved = Path(td) / "sa_3.exe", Path(td) / "savedata.dat"
            extract_row(image, files[RUNTIME_PATH], exe)
            extract_row(image, files[SAVEDATA_PATH], saved)
            report = inspect_verified(exe.read_bytes(), saved.read_bytes())
    finally:
        image.close()
    print(json.dumps(report, sort_keys=True))

if __name__ == "__main__":
    main()
