"""R32 fail-closed guard: never conflate static geometry with live file handles."""
import argparse
import json
from pathlib import Path

from tools.stoneage_tw10_savedata_native_io_r32 import *
from tools.stoneage_tw10_savedata_native_io_r30_guard import graph_guard
from tools.stoneage_tw10_savedata_native_io_r29_guard import input_guard
from tools.stoneage_tw10_savedata_upstream_r22_guard import FORBIDDEN

def check(ok, name):
    if not ok:
        raise ValueError("R32 " + name)

def validate(d):
    check(isinstance(d, dict) and d.get("schema") == SCHEMA and d.get("status") == STATUS, "schema")
    check(d.get("runtime_sha256") == RUNTIME_SHA256
          and d.get("savedata_sha256") == SAVEDATA_SHA256, "pinned original")
    check(d.get("r31_exact_original_revalidated") is True
          and d.get("r31_exact_report_sha256") == PRIOR_SHA256
          and d.get("static_only") is True, "prior provenance")
    check(all(d.get(k) is False for k in FLAGS), "false runtime promotions")
    check(d.get("actual_entry_paths_frames_aliases_or_api_returns_proven") is False, "actual paths")
    graph_guard(d.get("parent_graph", {}))
    call = d.get("intervening_call_identity", {})
    check(call.get("call_rva") == INTERVENING and
          call.get("kind") in ("direct", "register_indirect", "memory_indirect", "other")
          and call.get("runtime_target_or_effects_proven") is False, "call identity")
    if call["kind"] == "direct":
        check(type(call.get("direct_target_rva")) is int, "direct target")
    else:
        check(call.get("direct_target_rva") is None, "indirect call uncertainty")
    branches = d.get("branch_candidates", {})
    n = branches.get("count")
    rows = branches.get("candidates")
    check(type(n) is int and 0 <= n <= 256 and isinstance(rows, list)
          and len(rows) == min(n, MAX_BRANCHES)
          and branches.get("truncated") is (n > MAX_BRANCHES)
          and branches.get("returning_calls_assumed") is True
          and branches.get("all_real_paths_or_indirect_edges_proven") is False, "branch bounds")
    last = POST-1
    for row in rows:
        at = row.get("site_rva")
        check(type(at) is int and last < at < CALL and
              type(row.get("direct_target_rva")) is int
              and type(row.get("fallthrough_rva")) is int
              and row["fallthrough_rva"] > at
              and row.get("mnemonic", "").startswith("j")
              and type(row.get("target_structurally_reaches_helper_call")) is bool
              and type(row.get("fallthrough_structurally_reaches_helper_call")) is bool
              and (row["target_structurally_reaches_helper_call"]
                   or row["fallthrough_structurally_reaches_helper_call"])
              and row.get("branch_condition_or_actual_path_proven") is False,
              "conditional branch not executed")
        last = at
    slot = d.get("conditional_slot", {})
    check(slot.get("conditional_hardware_call_slot_candidate") is True
          and slot.get("single_suffix_push_rva") == PUSH
          and slot.get("callee_entry_stack_read_rva") == HELPER
          and slot.get("caller_pre_call_esp_offset") == 0
          and slot.get("callee_entry_esp_relative_offset") == 4
          and all(slot.get(k) is False for k in (
              "actual_taken_path_or_stack_contents_proven",
              "caller_callee_argument_binding_proven",
              "api_return_handle_link_proven")), "conditional hardware slot, not runtime argument")
    keys = input_guard(d.get("parent_esi_eax_sources", {}), PARENT)
    check(all(x in keys for x in (
        (POST, "esi"), (INTERVENING, "esi"), (INTERVENING, "eax"),
        (PUSH, "eax"), (CALL, "esi"))), "bounded input queries")
    def reject_payload(o):
        if isinstance(o, dict):
            check(not (set(o) & FORBIDDEN), "proprietary payload")
            for value in o.values():
                reject_payload(value)
        elif isinstance(o, list):
            for value in o:
                reject_payload(value)
    reject_payload(d)
    return True

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--report", type=Path, required=True)
    args = p.parse_args()
    check(args.report.stat().st_size <= 75000, "output size")
    validate(json.loads(args.report.read_text()))
    print("TW10_R32_STRICT_STATIC=PASS; NATIVE_SAVE=OPEN")

if __name__ == "__main__":
    main()
