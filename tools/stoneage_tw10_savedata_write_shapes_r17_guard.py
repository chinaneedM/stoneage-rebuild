"""Strict independent semantic boundary guard for TW1.0 R17 derived-only reports.

This verifies schema/uncertainty constraints, not historical data authenticity.
Original source/run/artifact custody and exact comparison are separate gates.
"""
import argparse
import json
from pathlib import Path
from tools.stoneage_tw10_savedata_write_shapes_r17 import (
    SCHEMA, STATUS, WRITES, GAP, NESTED, GLOBAL, FLAGS,
    RUNTIME_SHA256, SAVEDATA_SHA256,
)

FORBIDDEN_KEYS = {"raw_bytes", "opcode_bytes", "disassembly", "original_payload",
                  "original_executable", "client_binary", "instruction_bytes"}

def validate(report):
    if not isinstance(report, dict):
        raise ValueError("R17 report must be an object")
    if report.get("schema") != SCHEMA or report.get("status") != STATUS:
        raise ValueError("R17 original schema/status changed")
    if report.get("runtime_sha256") != RUNTIME_SHA256 or report.get("savedata_sha256") != SAVEDATA_SHA256:
        raise ValueError("R17 pinned original hashes changed")
    if report.get("conditional_static_only") is not True or report.get("r16_original_identity_revalidated") is not True:
        raise ValueError("R16 revalidation/static-only identity missing")
    if any(report.get(k) is not False for k in FLAGS):
        raise ValueError("R17 unsupported historical/runtime promotion")
    writes = report.get("writes")
    if not isinstance(writes, list) or [w.get("site_rva") for w in writes] != list(WRITES):
        raise ValueError("R17 original write sites changed")
    for w in writes:
        if any(w.get(k) is not False for k in
               ("actual_value_proven", "executed_write_proven",
                "effective_object_owner_proven")):
            raise ValueError("R17 known/executed write wrongly asserted")
        candidate = w.get("write", {})
        if candidate.get("expected_global_rva") != GLOBAL:
            raise ValueError("R17 candidate target changed")
        rhs = candidate.get("source_operand")
        if rhs is not None and rhs.get("kind") not in (
                "register_input", "immediate_input", "memory_input", "unmodeled_operand"):
            raise ValueError("R17 source kind invalid")
        frontier = w.get("local_source_frontier", {})
        if any(frontier.get(k) is not False for k in (
                "anchor_is_verified_entry", "all_incoming_paths_proven", "value_known")):
            raise ValueError("R17 optional candidate graph promoted to function/value")
        if frontier.get("call_fallthrough_structural_only") is not True:
            raise ValueError("R17 CALL barrier semantics lost")
        if not isinstance(frontier.get("reaching_candidates"), list) or len(frontier["reaching_candidates"]) > 24:
            raise ValueError("R17 reaching source cap")
    gap = report.get("callee_memory_gap", {})
    if gap.get("site_rva") != GAP or gap.get("r8_unsupported_memory_gap_retained") is not True:
        raise ValueError("R17 original callee gap changed")
    if gap.get("effective_address_and_owner_proven") is not False or gap.get("callee_effect_summary_admitted") is not False:
        raise ValueError("R17 callee semantics promoted")
    if not isinstance(gap.get("operand_shapes"), list) or not any(
            op.get("kind") == "memory" for op in gap["operand_shapes"]):
        raise ValueError("R17 memory operand geometry absent")
    nested = report.get("nested_callees")
    if not isinstance(nested, list) or [v.get("root_rva") for v in nested] != list(NESTED):
        raise ValueError("R17 nested targets changed")
    for row in nested:
        if row.get("caller_arguments_known") is not False or row.get("effective_effects_admitted") is not False:
            raise ValueError("R17 nested callee effects promoted")
        effects = row.get("bounded_effects", {})
        if effects.get("root_rva") != row["root_rva"] or effects.get("original_helper_accepted") is not False or effects.get("native_io_executed") is not False:
            raise ValueError("R17 original helper never qualified")
    def check_keys(obj):
        if isinstance(obj, dict):
            if FORBIDDEN_KEYS.intersection(obj):
                raise ValueError("R17 forbidden original-payload field")
            for value in obj.values():
                check_keys(value)
        elif isinstance(obj, list):
            for value in obj:
                check_keys(value)
    check_keys(report)
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    if args.report.stat().st_size > 70000:
        raise ValueError("oversized R17 derived metadata")
    validate(json.loads(args.report.read_text()))
    print("TW10_R17_BOUNDED_STATIC_GUARD=PASS")
    print("TW10_R17_NATIVE_SAVE_AND_OBJECT_OWNERSHIP=OPEN")

if __name__ == "__main__":
    main()
