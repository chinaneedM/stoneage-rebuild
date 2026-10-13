"""Fail-closed R33 original static ZF and secondary CALL constraints."""
import argparse
import json
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r33 import *
from tools.stoneage_tw10_savedata_native_io_r30_guard import graph_guard
from tools.stoneage_tw10_savedata_native_io_r29_guard import input_guard
from tools.stoneage_tw10_savedata_upstream_r22_guard import FORBIDDEN

def check(condition, reason):
    if not condition:
        raise ValueError("R33 " + reason)

def validate(d):
    check(isinstance(d, dict) and d.get("schema") == SCHEMA and d.get("status") == STATUS, "schema")
    check(d.get("runtime_sha256") == RUNTIME_SHA256 and d.get("savedata_sha256") == SAVEDATA_SHA256,
          "pinned source hashes")
    check(d.get("r32_exact_original_revalidated") is True
          and d.get("r32_exact_report_sha256") == PRIOR_SHA256 and d.get("static_only") is True,
          "original exact R32 provenance")
    check(all(d.get(k) is False for k in FLAGS), "runtime/owner promotions")
    check(d.get("all_flag_source_paths_or_effects_proven") is False and ZF_WRITE_BITS != 0,
          "ZF and effects scope")
    graph_guard(d.get("parent_graph", {}))
    call = d.get("secondary_call_identity", {})
    check(call.get("call_rva") == SECONDARY
          and call.get("kind") in ("direct", "register_indirect", "memory_indirect", "other")
          and call.get("runtime_target_or_effects_proven") is False, "secondary CALL")
    if call["kind"] == "direct":
        check(type(call.get("direct_target_rva")) is int, "direct call target")
    else:
        check(call.get("direct_target_rva") is None, "indirect CALL target")
    rows = d.get("branch_flag_contexts")
    check(isinstance(rows, list) and len(rows) == len(BRANCHES), "branch coverage")
    keys = input_guard(d.get("flag_operand_input_surface", {}), PARENT)
    for at, row in zip(BRANCHES, rows):
        count = row.get("source_count")
        samples = row.get("source_candidates")
        check(row.get("branch_site_rva") == at
              and row.get("branch_mnemonic") in ("je", "jne")
              and type(row.get("direct_target_rva")) is int
              and type(row.get("fallthrough_rva")) is int
              and row.get("flag_source_model") == "bounded_backward_ZF_may_def_CALL_opaque"
              and row.get("actual_predicate_value_or_feasible_path_proven") is False,
              "branch identity")
        check(type(count) is int and 0 <= count <= 256
              and isinstance(samples, list) and len(samples) == min(count, MAX_SOURCE_SAMPLES)
              and row.get("candidates_truncated") is (count > MAX_SOURCE_SAMPLES)
              and type(row.get("predecessor_nodes_examined")) is int
              and 1 <= row["predecessor_nodes_examined"] <= MAX_PRED_NODES+1
              and type(row.get("predecessor_cap_hit")) is bool
              and type(row.get("branch_disconnected_in_graph")) is bool,
              "bounded branch source count")
        prev = PARENT-1
        for s in samples:
            at_source = s.get("site_rva")
            check(type(at_source) is int and PARENT <= at_source < PARENT+768
                  and at_source > prev and s.get("kind") in ("opaque_call", "zf_write")
                  and s.get("candidate_actual_flag_value_known") is False
                  and s.get("branch_predicate_or_taken_path_proven") is False,
                  "flag candidate site")
            ops = s.get("operands"); regs = s.get("input_registers")
            check(isinstance(ops, list) and len(ops) <= 3
                  and isinstance(regs, list) and len(regs) <= 7
                  and regs == sorted(set(regs)), "ZF operand bounds")
            if s["kind"] == "opaque_call":
                check(s.get("mnemonic") is None and not ops and not regs, "opaque callee effects")
            else:
                check(isinstance(s.get("mnemonic"), str) and bool(s["mnemonic"])
                      and all(o.get("kind") in ("register", "immediate", "memory", "unmodeled")
                              and type(o.get("width_bytes")) is int
                              and 1 <= o["width_bytes"] <= 16 for o in ops),
                      "ZF static operand shapes")
                check(all((at_source, reg) in keys for reg in regs)
                      or d["flag_operand_input_surface"]["query_limit_hit"],
                      "ZF input query links")
            prev = at_source
    def no_payload(o):
        if isinstance(o, dict):
            check(not (set(o) & FORBIDDEN), "proprietary payload")
            for v in o.values(): no_payload(v)
        elif isinstance(o, list):
            for v in o: no_payload(v)
    no_payload(d)
    return True

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--report", type=Path, required=True)
    args = p.parse_args()
    check(args.report.stat().st_size <= 80000, "report cap")
    validate(json.loads(args.report.read_text()))
    print("TW10_R33_STRICT_STATIC=PASS; NATIVE_SAVE=OPEN")

if __name__ == "__main__":
    main()
