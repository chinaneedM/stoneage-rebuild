"""R13 original-only bounded memory-store geometry and immediate value-input audit.

Store instructions and single linear decoding windows are static candidates, not
executed paths. Register origins, alias targets, function boundaries, object
ownership, HeapAlloc arguments, FILE*/CRT identities and native save semantics
remain OPEN. Nothing here returns proprietary opcode bytes or disassembly.
"""
import argparse
import json
import tempfile
from pathlib import Path
from capstone import CS_GRP_JUMP
from capstone.x86 import X86_OP_REG, X86_OP_IMM, X86_OP_MEM, X86_REG_INVALID
from tools.stoneage_tw10_savedata_frontier_r12 import (
    inspect_verified as inspect_r12, FLAGS as R12_FLAGS,
    RUNTIME_SHA256, SAVEDATA_SHA256,
)
from tools.stoneage_tw10_savedata_provenance_r10 import memory_geometry
from tools.stoneage_tw10_savedata_helper_frontier_r9 import store_geometry
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH, SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows, extract_row

SCHEMA = "tw10-r13-original-bounded-store-and-global-write-inputs"
STATUS = "PINNED_ORIGINAL_STATIC_MUTATION_CANDIDATES_NO_NAMED_EFFECTS"
HELPER = (0x49dca, 0x49dec)
GLOBAL_WRITES = {0x4943c: 0x17228a0, 0x4944a: 0x1721884,
                 0x49457: 0x17228a0, 0x49463: 0x1721884}
WRITE_MNEMONICS = {"mov", "xchg", "add", "sub", "and", "or", "xor", "inc", "dec"}
FLAGS = R12_FLAGS | {
    "helper_named_effects_admitted", "global_write_paths_proven",
    "store_value_inputs_resolved", "heapalloc_size_or_ownership_proven",
    "frame_mutation_ownership_proven",
}

def operand_value(ins, op, sections, base):
    """Exact operand *shape*, not evaluated value or reaching definition."""
    if op.type == X86_OP_REG:
        return {"kind": "register_input", "register": ins.reg_name(op.reg),
                "immediate": None, "memory_input": None, "width_bytes": op.size}
    if op.type == X86_OP_IMM:
        return {"kind": "immediate_input", "register": None,
                "immediate": int(op.imm), "memory_input": None,
                "width_bytes": op.size}
    if op.type == X86_OP_MEM:
        return {"kind": "memory_input", "register": None, "immediate": None,
                "memory_input": memory_geometry(ins, op, sections, base),
                "width_bytes": op.size}
    return {"kind": "unmodeled_operand", "register": None, "immediate": None,
            "memory_input": None, "width_bytes": op.size}

def write_candidate(dec, site, sections, expected_global=None):
    ins = dec.at(site)
    if ins is None or ins.mnemonic not in WRITE_MNEMONICS:
        raise ValueError("site is not a recognized integer store")
    if not ins.operands or ins.operands[0].type != X86_OP_MEM:
        raise ValueError("site does not write a memory destination")
    dst = ins.operands[0]
    if not (dst.access & 2):
        raise ValueError("memory destination is not decoder-marked writable")
    m = dst.mem
    if m.segment != X86_REG_INVALID:
        raise ValueError("segmented write requires separate model")
    geometry = store_geometry(dec, site, sections)
    if expected_global is not None:
        if (m.base != X86_REG_INVALID or m.index != X86_REG_INVALID
                or ((int(m.disp) & 0xffffffff) - dec.base) != expected_global
                or dst.size != 4):
            raise ValueError("expected exact four-byte absolute global write")
    rhs = (operand_value(ins, ins.operands[1], sections, dec.base)
           if len(ins.operands) > 1 else None)
    # An arithmetic write is a read-modify-write, never an independent assignment.
    previous_required = ins.mnemonic != "mov"
    return {"site_rva": site, "mnemonic_class": ins.mnemonic,
            "destination": geometry, "expected_global_rva": expected_global,
            "source_operand": rhs, "previous_destination_value_required": previous_required,
            "address_inputs": sorted({
                r for r in (geometry["base_register"], geometry["index_register"]) if r
            }),
            "value_input_registers": sorted(set(
                ([rhs["register"]] if rhs and rhs["register"] else [])
                + (["destination_memory"] if previous_required else [])
            )),
            "register_inputs_resolved": False,
            "executed_write_proven": False,
            "effective_object_proven": False,
            "named_caller_effect_admitted": False}

def linear_window(dec, first, last, max_instructions=64):
    """Consecutive decode boundaries only; NOT a CFG or path feasibility."""
    if last < first or max_instructions < 1 or max_instructions > 64:
        raise ValueError("window bound")
    p = first
    boundaries = []
    jumps = []
    while p <= last:
        if len(boundaries) == max_instructions:
            raise ValueError("window instruction cap")
        ins = dec.at(p)
        if ins is None or ins.size < 1:
            raise ValueError("linear window decode gap")
        boundaries.append(p)
        if ins.group(CS_GRP_JUMP):
            jumps.append(p)
        p += ins.size
    return {"first_rva": first, "last_site_rva": last,
            "instruction_boundaries": boundaries,
            "jump_sites": jumps,
            "same_executed_path_proven": False,
            "function_boundary_proven": False,
            "control_flow_conditions_proven": False}

def inspect_verified(runtime, savedata):
    r12 = inspect_r12(runtime, savedata)
    if (r12["delegate_helper"]["root_rva"] != 0x49d93
            or r12["delegate_helper"]["qualifies_modeled_return_effect_summary"]
            or r12["call_identity"]["import_identity"] != {
                "dll": "KERNEL32.dll", "name": "HeapAlloc", "iat_rva": 0x520f8
            }):
        raise ValueError("R12 original identity changed")
    reference_rows = {x["global_rva"]: x for x in r12["global_references"]["globals"]}
    for site, target in GLOBAL_WRITES.items():
        if not any(x["rva"] == site and x["kind"] == "write_candidate"
                   for x in reference_rows[target]["samples"]):
            raise ValueError("selected write absent from R12 original scan")
    gaps = r12["delegate_helper"]["gap_sites"]
    for site in HELPER:
        if not any(x["rva"] == site and
                   x["reason"] in ("alias_write", "caller_memory_write")
                   for x in gaps):
            raise ValueError("selected helper gap absent from R12")
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "sa_3.exe"
        p.write_bytes(runtime)
        data, pe, base, sections, _ = image_layout(p)
    for s, raw in zip(sections, pe.sections):
        s["characteristics"] = int(raw.Characteristics)
    t = next(s for s in sections if s["name"] == ".text")
    dec = Decoder(data[t["raw"]:t["raw"]+t["raw_size"]], t["rva"], base)
    writes = [write_candidate(dec, x, sections) for x in HELPER]
    writes += [write_candidate(dec, x, sections, GLOBAL_WRITES[x])
               for x in sorted(GLOBAL_WRITES)]
    windows = [linear_window(dec, min(HELPER), max(HELPER)),
               linear_window(dec, min(GLOBAL_WRITES), max(GLOBAL_WRITES))]
    return {"schema": SCHEMA, "status": STATUS,
            "runtime_sha256": RUNTIME_SHA256, "savedata_sha256": SAVEDATA_SHA256,
            "r12_helper_states": r12["delegate_helper"]["visited_states"],
            "r12_import_slot_rva": 0x520f8,
            "store_candidates": writes, "linear_windows": windows,
            "static_candidate_scope": "named-sites-only-no-reachability",
            **{key: False for key in FLAGS}}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--bin", type=Path, required=True)
    args = p.parse_args()
    img, rows, _, _ = find_rows(args.bin)
    try:
        paths = {r["path"]: r for r in rows if not r["is_dir"]}
        with tempfile.TemporaryDirectory() as td:
            exe = Path(td) / "sa_3.exe"
            save = Path(td) / "savedata.dat"
            extract_row(img, paths[RUNTIME_PATH], exe)
            extract_row(img, paths[SAVEDATA_PATH], save)
            report = inspect_verified(exe.read_bytes(), save.read_bytes())
    finally:
        img.close()
    print(json.dumps(report, sort_keys=True))

if __name__ == "__main__":
    main()
