"""Independent bounded-schema guard: R18 report carries no runtime admissions.

Checks expected original identities and conservative uncertainty fields.
The independent workflow also pins a successful immutable original Actions
run, artifact digest and exact JSON equality before evidence acceptance.
"""
import argparse
import json
from pathlib import Path
from tools.stoneage_tw10_savedata_upstream_r18 import (
    SCHEMA, STATUS, FLAGS, RUNTIME_SHA256, SAVEDATA_SHA256,
    EAX_CALL, EAX_WRITE, ECX_LOAD, SECOND_GLOBAL,
    EBX_WRITE, IMUL_SITE, HELPER_ANCHOR,
)

NO_ORIGINAL = {"original_binary", "raw_bytes", "opcode_bytes",
               "instruction_bytes", "disassembly", "embedded_executable",
               "asset_payload", "original_payload"}

def validate(data):
    if not isinstance(data, dict):
        raise ValueError("R18 report not object")
    if data.get("schema") != SCHEMA or data.get("status") != STATUS:
        raise ValueError("R18 pinned schema/status mismatch")
    if data.get("runtime_sha256") != RUNTIME_SHA256 or data.get("savedata_sha256") != SAVEDATA_SHA256:
        raise ValueError("R18 original hashes mismatch")
    if data.get("r17_original_identity_revalidated") is not True or data.get("original_static_only") is not True:
        raise ValueError("R18 original identity/static boundary missing")
    if any(data.get(k) is not False for k in FLAGS):
        raise ValueError("R18 runtime/effects falsehood")
    call = data.get("eax_call_barrier", {})
    if call.get("call_site_rva") != EAX_CALL or call.get("write_site_rva") != EAX_WRITE:
        raise ValueError("R18 EAX CALL site changed")
    identity = call.get("call_identity", {})
    if identity.get("call_rva") != EAX_CALL or identity.get("kind") not in ("direct", "register_indirect", "memory_indirect", "other"):
        raise ValueError("R18 CALL identity invalid")
    if any(call.get(k) is not False for k in (
            "candidate_anchor_verified_entry", "eax_after_call_known",
            "callee_summary_admitted", "original_return_value_proven")):
        raise ValueError("R18 CALL effect promoted")
    if call.get("call_fallthrough_structural_only") is not True:
        raise ValueError("R18 opaque CALL/fallthrough guard missing")
    if call.get("candidate_graph_nodes", 0) > 128 or call.get("candidate_graph_edges", 0) > 256:
        raise ValueError("R18 CALL graph cap")
    effect = call.get("direct_callee_model")
    if effect is not None and (effect.get("original_helper_accepted") is not False
                             or effect.get("native_io_executed") is not False):
        raise ValueError("R18 conditional callee model promoted")
    global_ = data.get("secondary_global", {})
    if (global_.get("read_site_rva") != ECX_LOAD
            or global_.get("original_global_identity_proven") is not True):
        raise ValueError("R18 distinct global read identity mismatch")
    if any(global_.get(k) is not False for k in (
        "global_value_known", "alias_reference_coverage_complete",
        "runtime_initialized", "same_object_as_primary_global_proven"
    )):
        raise ValueError("R18 global runtime alias promoted")
    scans = global_.get("global_reference_candidates", {})
    if scans.get("scope") != "linear_text_decode_candidates_not_reachable_execution" or scans.get("all_indirect_references_covered") is not False:
        raise ValueError("R18 global linear scan scope promoted")
    rows = scans.get("globals")
    if not isinstance(rows, list) or len(rows) != 1 or rows[0].get("global_rva") != SECOND_GLOBAL:
        raise ValueError("R18 other .data identity changed")
    if rows[0].get("runtime_initialization_proven") is not False:
        raise ValueError("R18 .data initialization promoted")
    if len(rows[0].get("samples", [])) > 32:
        raise ValueError("R18 original scan sample cap")
    graph = data.get("ebx_graph", {})
    if graph.get("write_site_rva") != EBX_WRITE or graph.get("anchor_rva") != HELPER_ANCHOR:
        raise ValueError("R18 EBX graph anchors changed")
    if graph.get("nodes",0) > 192 or graph.get("edges",0) > 600:
        raise ValueError("R18 graph bounds")
    if any(graph.get(k) is not False for k in (
        "actual_function_entry_proven","all_incoming_edges_proven",
        "value_known","feasible_path_proven"
    )):
        raise ValueError("R18 EBX graph evidence promoted")
    if graph.get("call_fallthrough_structural_only") is not True:
        raise ValueError("R18 EBX structural-only fallthrough removed")
    if not isinstance(graph.get("source_candidates"), list) or len(graph["source_candidates"]) > 32:
        raise ValueError("R18 EBX source cap")
    stack = data.get("imul_stack", {})
    if stack.get("imul_site_rva") != IMUL_SITE:
        raise ValueError("R18 IMUL site changed")
    if stack.get("stack_offset_model_is_conditional_only") is not True:
        raise ValueError("R18 stack modeled not original")
    if any(stack.get(k) is not False for k in (
        "real_esp_or_caller_frame_proven", "effective_memory_value_proven",
        "register_multiplier_value_proven","callee_effect_summary_admitted"
    )):
        raise ValueError("R18 IMUL original ownership claimed")
    pos = stack.get("modeled_stack_offset_of_memory_operand")
    if pos is not None and (type(pos) is not int or abs(pos)>1024
                            or stack.get("stopped_at_original_memory_gap") is not True):
        raise ValueError("R18 invalid symbolic stack offset")
    def scan_keys(obj):
        if isinstance(obj, dict):
            if set(obj).intersection(NO_ORIGINAL):
                raise ValueError("R18 forbidden historical byte field")
            for value in obj.values():
                scan_keys(value)
        elif isinstance(obj, list):
            for value in obj:
                scan_keys(value)
    scan_keys(data)
    return True

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--report", type=Path, required=True)
    args = p.parse_args()
    if args.report.stat().st_size > 70000:
        raise ValueError("R18 derived report oversized")
    validate(json.loads(args.report.read_text()))
    print("TW10_R18_STATIC_SCHEMA_AND_NO_PROMOTION=PASS")
    print("TW10_R18_NATIVE_IO_AND_OBJECT_OWNERSHIP=OPEN")

if __name__ == "__main__":
    main()
