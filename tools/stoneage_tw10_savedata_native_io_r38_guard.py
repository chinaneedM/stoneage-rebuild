"""Replay R38 bounded offset geometry; no original runtime/value admission."""
import argparse
import json
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r38 import *
from tools.stoneage_tw10_savedata_native_io_r37_guard import row_guard, direct_guard
from tools.stoneage_tw10_savedata_native_io_r30_guard import graph_guard
from tools.stoneage_tw10_savedata_native_io_r29_guard import input_guard
from tools.stoneage_tw10_savedata_upstream_r22_guard import FORBIDDEN

def require(ok, why):
    if not ok:
        raise ValueError("R38 " + why)

def validate(d):
    require(isinstance(d, dict) and d.get("schema") == SCHEMA and d.get("status") == STATUS, "schema/status")
    require(d.get("runtime_sha256") == RUNTIME_SHA256 and d.get("savedata_sha256") == SAVEDATA_SHA256
            and d.get("r37_exact_original_revalidated") is True and d.get("r37_exact_report_sha256") == PRIOR_SHA256
            and d.get("static_only") is True and d.get("root_candidate_rva") == ROOT
            and all(d.get(k) is False for k in FLAGS)
            and d.get("memory_alias_contents_or_actual_caller_callee_binding_proven") is False, "prior/non-promotion")
    direct_guard(d.get("caller_identity", {}), HELPERS[0][0], ROOT)
    graph_guard(d.get("graph", {}))
    effects, edges = d.get("stack_effect_candidates"), d.get("bounded_edges")
    require(isinstance(effects, list) and len(effects) == d["graph"]["nodes"], "effect count")
    ats = []
    for effect in effects:
        at, kind, delta = effect.get("site_rva"), effect.get("syntax_class"), effect.get("esp_delta")
        width = effect.get("operand_width_bytes")
        require(type(at) is int and ROOT <= at < ROOT + 768
                and effect.get("conditional_32bit_stack_address_only") is True
                and kind in ("neutral", "push", "pop", "opaque_call", "unknown_esp_write"), "stack effect scope")
        if kind in ("push", "pop"):
            require(type(width) is int and width in (2, 4)
                    and type(delta) is int and delta == (-width if kind == "push" else width), "stack width/delta")
        else:
            require(width is None and (type(delta) is int and delta == 0 if kind == "neutral" else delta is None), "unknown/neutral delta")
        ats.append(at)
    require(ats == sorted(set(ats)) and ROOT in ats, "effect order")
    require(isinstance(edges, list) and len(edges) == d["graph"]["edges"]
            and all(isinstance(e, list) and len(e) == 2 and all(type(x) is int and x in ats for x in e) for e in edges)
            and edges == [list(e) for e in sorted(set(tuple(e) for e in edges))], "edge topology")
    calls = d.get("opaque_call_candidates")
    require(isinstance(calls, list) and len(calls) <= 24
            and [c.get("call_rva") for c in calls] == [e["site_rva"] for e in effects if e["syntax_class"] == "opaque_call"]
            and all(c.get("runtime_target_or_effects_proven") is False for c in calls), "CALL barrier agreement")
    states, updates, limited = stack_states(effects, edges, ROOT)
    require(d.get("stack_model") == {"known_offset_limit": MAX_STATES, "barrier_limit": MAX_BARRIERS,
            "absolute_delta_limit": MAX_DELTA, "update_limit": MAX_UPDATES,
            "updates": updates, "update_limit_hit": limited,
            "requires_32bit_stack_address_attribute": True,
            "actual_stack_address_attribute_or_return_effects_proven": False}, "offset replay limits/assumptions")
    summaries = [state_summary(states, at, limited) for at in (*READS, STORE)]
    require(d.get("stack_state_queries") == summaries, "stack state replay mismatch")
    keys = input_guard(d.get("register_input_sources", {}), ROOT)
    capped = d["register_input_sources"]["query_limit_hit"]
    reads, scalars = d.get("callee_stack_read_shapes"), d.get("scalar_shapes")
    require(isinstance(reads, list) and len(reads) == 2 and isinstance(scalars, list) and len(scalars) == 2, "shape counts")
    for row, at in zip(reads, READS):
        row_guard(row, at, keys, capped)
        require(at in ats, "read not in stack graph")
    for row, at in zip(scalars, SCALARS):
        row_guard(row, at, keys, capped)
        require(row.get("conditional_full_width_model") == full_width_model(row), "scalar model")
    address, store = d.get("shared_address_shape", {}), d.get("shared_store_shape", {})
    row_guard(address, LEA, keys, capped)
    row_guard(store, STORE, keys, capped)
    require(store.get("mnemonic") == "mov" and len(store["operands"]) == 2
            and store["operands"][0].get("kind") == "memory"
            and store["operands"][0].get("decoder_write") is True, "store shape")
    pushes = d.get("prior_push_candidates")
    require(isinstance(pushes, list) and len(pushes) <= 24, "caller push bounds")
    last = HELPERS[0][0]
    for idx, p in enumerate(pushes):
        at = p.get("site_rva")
        require(type(at) is int and 0x4ed33 <= at < last
                and p.get("conditional_pre_call_esp_offset") == idx * 4
                and p.get("input", {}).get("width_bytes") == 4
                and p.get("actual_argument_role_value_or_binding_proven") is False, "caller push geometry not value")
        last = at
    require(d.get("conditional_slot_bridges") == [slot_bridge(row, summary, pushes)
            for row, summary in zip(reads, summaries)], "slot bridge replay/value tamper")
    memory = d.get("explicit_memory_write_barrier_sites")
    require(isinstance(memory, list) and len(memory) <= 256 and memory == sorted(set(memory))
            and all(type(at) is int and at in ats for at in memory), "memory/alias barrier list")
    def ban(obj):
        if isinstance(obj, dict):
            require(not (set(obj) & FORBIDDEN), "original payload")
            for val in obj.values():
                ban(val)
        elif isinstance(obj, list):
            for val in obj:
                ban(val)
    ban(d)
    return True

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--report", type=Path, required=True)
    path = p.parse_args().report
    require(path.stat().st_size <= 100000, "report size")
    validate(json.loads(path.read_text()))
    print("TW10_R38_STRICT_STATIC=PASS; NATIVE_VALUE_HANDLE_SAVE=OPEN")

if __name__ == "__main__":
    main()
