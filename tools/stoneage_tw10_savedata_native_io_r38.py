"""R38: conditional 32-bit ESP geometry, caller slots and exact shared write.

Never evaluate original register/stack contents. CALLs have unknown ESP effects;
all slot matches are hardware geometry, not ABI/parameter/value/owner proofs.
"""
import argparse
import hashlib
import json
import tempfile
from collections import deque
from pathlib import Path
from capstone import CS_GRP_CALL
from capstone.x86 import X86_OP_MEM
from tools.stoneage_tw10_savedata_native_io_r37 import (
    inspect_verified as inspect_r37, RUNTIME_SHA256, SAVEDATA_SHA256,
    instruction_row, full_width_model, HELPERS, FLAGS as R37_FLAGS,
)
from tools.stoneage_tw10_savedata_native_io_r37_guard import validate as validate_r37
from tools.stoneage_tw10_savedata_native_io_r28 import candidate_graph, input_surface
from tools.stoneage_tw10_savedata_native_io_r30 import graph_meta
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH, SAVEDATA_PATH
from tools.stoneage_tw10_technical_probe import find_rows, extract_row

SCHEMA = "tw10-r38-original-conditional-esp-slots-shared-store-inputs"
STATUS = "PINNED_ORIGINAL_CONDITIONAL_STACK_GEOMETRY_NATIVE_VALUE_BINDING_OPEN"
PRIOR_SHA256 = "a16c858a46d502dec5c99fe43528601f0bc89449c671a717198725c95aa496d0"
ROOT = HELPERS[0][1]
READS = (ROOT, 0x4e83c)
SCALARS = (0x4e81c, 0x4e829)
LEA = 0x4e822
STORE = 0x4e862
MAX_STATES = 8
MAX_BARRIERS = 32
MAX_DELTA = 4096
MAX_UPDATES = 8192
FLAGS = tuple(R37_FLAGS) + (
    "slot_geometry_establishes_actual_argument_value",
    "original_stack_address_attribute_or_contents_proven",
    "shared_store_contains_actual_createfile_handle",
    "callee_esp_abi_cleanup_or_preservation_admitted",
)

def stack_effect(ins, base):
    at = ins.address - base
    mnemonic = ins.mnemonic
    result = {"site_rva": at, "syntax_class": "neutral", "esp_delta": 0,
              "operand_width_bytes": None, "conditional_32bit_stack_address_only": True}
    if ins.group(CS_GRP_CALL):
        result.update(syntax_class="opaque_call", esp_delta=None)
    elif mnemonic in ("push", "pop") and len(ins.operands) == 1:
        op = ins.operands[0]
        from capstone.x86 import X86_OP_REG
        pop_esp = mnemonic == "pop" and op.type == X86_OP_REG and ins.reg_name(op.reg) in ("esp", "sp")
        if op.size in (2, 4) and not pop_esp:
            result.update(syntax_class=mnemonic, esp_delta=(-op.size if mnemonic == "push" else op.size),
                          operand_width_bytes=op.size)
        else:
            result.update(syntax_class="unknown_esp_write", esp_delta=None)
    else:
        writes = {ins.reg_name(r) for r in ins.regs_access()[1]}
        if writes & {"esp", "sp", "spl"} or mnemonic in ("enter", "leave"):
            # Explicitly retain these as unknown until separately qualified.
            result.update(syntax_class="unknown_esp_write", esp_delta=None)
    return result

def merge_state(old, incoming, root):
    known = set(old[0]) | set(incoming[0])
    unknown = set(old[1]) | set(incoming[1])
    capped = old[2] or incoming[2]
    generic = ("barrier_limit", root)
    if generic in unknown or len(unknown) > MAX_BARRIERS:
        return frozenset(), frozenset({generic}), True
    if capped or len(known) > MAX_STATES:
        known = set()
        unknown.add(("state_limit", root))
        capped = True
    return frozenset(known), frozenset(unknown), capped

def advance(state, effect, root):
    known, unknown, capped = state
    at, kind, delta = effect["site_rva"], effect["syntax_class"], effect["esp_delta"]
    if delta is None:
        return frozenset(), frozenset(set(unknown) | {(kind, at)}), capped
    shifted = {n + delta for n in known}
    if any(abs(n) > MAX_DELTA for n in shifted):
        return frozenset(), frozenset(set(unknown) | {("delta_limit", root)}), True
    return frozenset(shifted), unknown, capped

def stack_states(effects, edges, root):
    """Finite monotone may-offset model, no original stack contents or ABI."""
    rows = {e["site_rva"]: e for e in effects}
    if root not in rows:
        raise ValueError("R38 stack root absent")
    adjacency = {}
    for a, b in edges:
        adjacency.setdefault(a, set()).add(b)
    empty = (frozenset(), frozenset(), False)
    states = {root: (frozenset({0}), frozenset(), False)}
    queue, pending = deque([root]), {root}
    updates = 0
    while queue and updates < MAX_UPDATES:
        at = queue.popleft()
        pending.discard(at)
        out = advance(states[at], rows[at], root)
        for target in sorted(adjacency.get(at, ())):
            joined = merge_state(states.get(target, empty), out, root)
            if joined != states.get(target, empty):
                states[target] = joined
                if target not in pending:
                    queue.append(target)
                    pending.add(target)
        updates += 1
    limited = bool(queue)
    return states, updates, limited

def state_summary(states, site, update_limit=False):
    state = states.get(site, (frozenset(), frozenset(), False))
    known, barriers, capped = state
    return {"site_rva": site, "site_reached_in_stack_model": site in states,
            "known_conditional_esp_deltas": sorted(known),
            "unknown_barrier_candidates": [{"kind": k, "site_rva": a} for k, a in sorted(barriers)],
            "state_limit_hit": capped, "update_limit_hit": update_limit,
            "unique_conditional_esp_delta": (next(iter(known)) if len(known) == 1 and not barriers
                                              and not capped and not update_limit else None),
            "actual_original_esp_or_stack_contents_known": False}

def slot_bridge(row, summary, pushes):
    refs = [op for op in row["operands"] if op.get("kind") == "memory"
            and op.get("geometry", {}).get("base_register") == "esp"
            and op["geometry"].get("index_register") is None
            and op["geometry"].get("segment_register") is None]
    delta = summary["unique_conditional_esp_delta"]
    displacement = refs[0]["geometry"]["relative_field_offset"] if len(refs) == 1 else None
    qualified = delta is not None and type(displacement) is int and len(refs) == 1 and refs[0]["decoder_read"]
    entry_offset = delta + displacement if qualified else None
    caller_offset = entry_offset - 4 if qualified else None  # Conditional near CALL return-address slot.
    match = next((p for p in pushes if p["conditional_pre_call_esp_offset"] == caller_offset), None)
    return {"callee_read_site_rva": row["site_rva"], "conditional_32bit_stack_address_required": True,
            "conditional_32bit_near_call_return_address_required": True,
            "unique_local_esp_geometry_qualified": bool(qualified),
            "callee_entry_esp_relative_offset": entry_offset,
            "caller_pre_call_esp_relative_offset": caller_offset,
            "matching_suffix_push_rva": match["site_rva"] if match else None,
            "matching_push_operand_shape": match["input"] if match else None,
            "conditional_hardware_slot_candidate": bool(match),
            "actual_argument_value_abi_owner_or_stack_alias_binding_proven": False}

def derive(dec, sections, imports, prior):
    if prior.get("schema") != "tw10-r37-original-continuation-helpers-partial-register-geometry":
        raise ValueError("R38 prerequisite schema")
    old = prior["helper_candidates"][0]
    if old["caller_call_identity"]["direct_target_rva"] != ROOT or old["callee_context"]["root_candidate_rva"] != ROOT:
        raise ValueError("R38 prior helper identity")
    nodes, edges, front, hit = candidate_graph(dec, ROOT)
    effects = [stack_effect(ins, dec.base) for _, ins in sorted(nodes.items())]
    states, updates, limit = stack_states(effects, edges, ROOT)
    reads = [instruction_row(dec, sections, nodes, at) for at in READS]
    scalars = [instruction_row(dec, sections, nodes, at) for at in SCALARS]
    for row in scalars:
        row["conditional_full_width_model"] = full_width_model(row)
    address, store = instruction_row(dec, sections, nodes, LEA), instruction_row(dec, sections, nodes, STORE)
    if store["mnemonic"] != "mov" or len(store["operands"]) != 2:
        raise ValueError("R38 original shared MOV shape changed")
    queries = {(row["site_rva"], reg) for row in reads + scalars + [address, store]
               for reg in row["input_query_registers"]}
    summaries = [state_summary(states, at, limit) for at in (*READS, STORE)]
    return {"schema": SCHEMA, "status": STATUS,
            "runtime_sha256": RUNTIME_SHA256, "savedata_sha256": SAVEDATA_SHA256,
            "r37_exact_original_revalidated": True, "r37_exact_report_sha256": PRIOR_SHA256,
            "static_only": True, "root_candidate_rva": ROOT,
            "caller_identity": old["caller_call_identity"], "prior_push_candidates": old["push_candidates"],
            "graph": graph_meta(nodes, edges, front, hit),
            "stack_effect_candidates": effects, "bounded_edges": [list(e) for e in sorted(edges)],
            "opaque_call_candidates": old["callee_context"]["call_candidates"],
            "stack_model": {"known_offset_limit": MAX_STATES, "barrier_limit": MAX_BARRIERS,
                            "absolute_delta_limit": MAX_DELTA, "update_limit": MAX_UPDATES,
                            "updates": updates, "update_limit_hit": limit,
                            "requires_32bit_stack_address_attribute": True,
                            "actual_stack_address_attribute_or_return_effects_proven": False},
            "stack_state_queries": summaries,
            "callee_stack_read_shapes": reads,
            "conditional_slot_bridges": [slot_bridge(row, summary, old["push_candidates"])
                                         for row, summary in zip(reads, summaries)],
            "scalar_shapes": scalars, "shared_address_shape": address, "shared_store_shape": store,
            "register_input_sources": input_surface(dec, sections, nodes, edges, ROOT, queries),
            "explicit_memory_write_barrier_sites": sorted(at for at, ins in nodes.items()
                if any(op.type == X86_OP_MEM and op.access & 2 for op in ins.operands)),
            "memory_alias_contents_or_actual_caller_callee_binding_proven": False,
            **{flag: False for flag in FLAGS}}

def inspect_verified(runtime, savedata):
    prior = inspect_r37(runtime, savedata)
    validate_r37(prior)
    digest = hashlib.sha256((json.dumps(prior, sort_keys=True) + "\n").encode()).hexdigest()
    if digest != PRIOR_SHA256:
        raise ValueError("R38 R37 exact original derivative changed")
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
