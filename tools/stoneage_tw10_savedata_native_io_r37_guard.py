"""Strict R37 shape/query/slice bounds; independent original custody required."""
import argparse
import json
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r37 import *
from tools.stoneage_tw10_savedata_native_io_r30_guard import graph_guard
from tools.stoneage_tw10_savedata_native_io_r29_guard import shape_guard, input_guard
from tools.stoneage_tw10_savedata_upstream_r22_guard import FORBIDDEN

def require(ok, why):
    if not ok:
        raise ValueError("R37 " + why)

def row_guard(row, site, keys, capped=False):
    ops = row.get("operands")
    shape_guard({"site_rva": site, "class": "unmodeled", "operands": ops}, site)
    require(row.get("site_rva") == site and isinstance(row.get("mnemonic"), str)
            and row.get("actual_instruction_effect_or_value_known") is False, "instruction shape/value")
    reads, writes = row.get("decoder_read_registers"), row.get("decoder_written_registers")
    require(isinstance(reads, list) and isinstance(writes, list)
            and len(reads) <= 32 and len(writes) <= 32
            and all(isinstance(r, str) for r in reads + writes)
            and reads == sorted(set(reads)) and writes == sorted(set(writes)), "decoder register metadata")
    expected = {family(r) for r in reads} - {None}
    for op in ops:
        expected.update(operand_registers(op))
    require(row.get("input_query_registers") == sorted(expected)
            and (all((site, r) in keys for r in expected) or capped), "instruction query refs")

def direct_guard(ident, call, root):
    require(ident.get("call_rva") == call and ident.get("kind") == "direct"
            and ident.get("direct_target_rva") == root and ident.get("import_identity") is None
            and ident.get("import_slot_association_proven") is False
            and ident.get("runtime_target_or_effects_proven") is False, "direct caller identity")

def validate(d):
    require(isinstance(d, dict) and d.get("schema") == SCHEMA and d.get("status") == STATUS, "schema/status")
    require(d.get("runtime_sha256") == RUNTIME_SHA256 and d.get("savedata_sha256") == SAVEDATA_SHA256
            and d.get("r36_exact_original_revalidated") is True
            and d.get("r36_exact_report_sha256") == PRIOR_SHA256 and d.get("static_only") is True
            and all(d.get(k) is False for k in FLAGS), "prior/original/non-promotion")
    graph_guard(d.get("parent_graph", {}))
    keys = input_guard(d.get("caller_input_sources", {}), PARENT)
    capped = d["caller_input_sources"]["query_limit_hit"]
    parts, stores = d.get("partial_definition_shapes"), d.get("continuation_store_shapes")
    require(isinstance(parts, list) and len(parts) == 3 and isinstance(stores, list) and len(stores) == 3, "shape counts")
    for row, site in zip(parts, PARTIAL_SITES):
        row_guard(row, site, keys, capped)
        require(row.get("conditional_partial_model") == partial_model(row), "partial-register model")
    for row, site in zip(stores, STORE_SITES):
        row_guard(row, site, keys, capped)
        require(row.get("mnemonic") == "mov" and len(row["operands"]) == 2
                and row["operands"][0].get("kind") == "memory"
                and row["operands"][0].get("decoder_write") is True, "store identity")
    boundary = d.get("helper_boundary_candidates", {})
    lo, size = boundary.get("text_start_rva"), boundary.get("text_bytes")
    require(boundary.get("scope") == "full_raw_text_linear_decode_candidate_boundaries"
            and type(lo) is int and lo >= 0 and type(size) is int and 0 < size <= 1000000
            and type(boundary.get("decoded_instructions")) is int and 0 < boundary["decoded_instructions"] <= size
            and type(boundary.get("decode_gap_bytes")) is int and 0 <= boundary["decode_gap_bytes"] <= size
            and boundary.get("complete_runtime_alignment_or_cfg_proven") is False
            and isinstance(boundary.get("roots"), list) and len(boundary["roots"]) == 2, "boundary scope")
    for b, (_, root) in zip(boundary["roots"], HELPERS):
        require(b.get("root_rva") == root and lo <= root < lo + size
                and type(b.get("linear_boundary_candidate")) is bool
                and b.get("true_function_entry_or_executed_alignment_proven") is False, "boundary candidate")
    helpers = d.get("helper_candidates")
    require(isinstance(helpers, list) and len(helpers) == 2, "helper count")
    for h, (call, root) in zip(helpers, HELPERS):
        direct_guard(h.get("caller_call_identity", {}), call, root)
        require(h.get("supported_by_exact_r36_original_call") is True
                and h.get("actual_caller_callee_stack_or_value_binding_proven") is False, "caller-callee binding")
        suffix = h.get("pre_call_suffix", {})
        require(type(suffix.get("linear_call_boundary_reached")) is bool
                and suffix.get("conditional_pre_call_esp_only") is True
                and suffix.get("abi_roles_applied") is False and suffix.get("actual_stack_values_known") is False
                and suffix.get("stop_reason") in ("candidate_anchor", "control_transfer", "stack_or_memory_barrier",
                                                "push_cap", "decode_or_boundary_gap", "bound"), "suffix scope")
        ps, old = h.get("push_candidates"), suffix.get("pushes")
        require(isinstance(ps, list) and isinstance(old, list) and len(ps) == len(old) <= 24
                and (suffix["linear_call_boundary_reached"] or not ps), "push count")
        last = call
        for idx, (p, orig) in enumerate(zip(ps, old)):
            at = p.get("site_rva")
            require(type(at) is int and CONTINUATION <= at < last
                    and p.get("conditional_pre_call_esp_offset") == idx * 4
                    and p.get("input", {}).get("width_bytes") == 4
                    and all(p.get(k) == v for k, v in orig.items())
                    and p.get("actual_argument_role_value_or_binding_proven") is False, "PUSH geometry")
            regs = operand_registers(p["input"])
            require(p.get("input_query_registers") == regs
                    and (all((at, r) in keys for r in regs) or capped), "PUSH provenance")
            last = at
        require(all((call, r) in keys for r in ("eax", "esi", "ecx", "edi", "ebp")) or capped, "CALL inputs")
        c = h.get("callee_context", {})
        require(c.get("root_candidate_rva") == root
                and c.get("actual_function_entry_call_effect_or_complete_aliases_proven") is False, "callee scope")
        graph_guard(c.get("graph", {}))
        hk = input_guard(c.get("input_sources", {}), root)
        count, refs = c.get("memory_reference_count"), c.get("memory_references")
        require(type(count) is int and 0 <= count <= 8 * 256 and isinstance(refs, list)
                and len(refs) == min(count, MAX_MEMORY_REFS)
                and c.get("memory_references_truncated") is (count > MAX_MEMORY_REFS), "memory reference bounds")
        ref_keys = []
        for row in refs:
            at, n, op = row.get("site_rva"), row.get("operand_index"), row.get("operand", {})
            shape_guard({"site_rva": at, "class": "unmodeled", "operands": [op]}, at)
            geo = op.get("geometry", {})
            require(type(at) is int and root <= at < root + 768 and type(n) is int and 0 <= n < 8
                    and isinstance(row.get("mnemonic"), str) and op.get("kind") == "memory"
                    and row.get("stack_or_frame_spelling_candidate") is (geo.get("base_register") in ("esp", "ebp"))
                    and row.get("shared_displacement_reference_candidate") is
                        ((geo.get("displacement_region") or {}).get("displacement_rva") == SHARED)
                    and row.get("actual_effective_address_value_owner_or_parameter_proven") is False, "memory geometry/ownership")
            regs = row.get("input_query_registers")
            require(isinstance(regs, list) and all(r in ALIASES for r in regs) and regs == sorted(set(regs))
                    and set(operand_registers(op)) <= set(regs)
                    and (all((at, r) in hk for r in regs) or c["input_sources"]["query_limit_hit"]), "memory source query refs")
            ref_keys.append((at, n))
        require(ref_keys == sorted(set(ref_keys)), "memory reference order")
        count, calls = c.get("call_count"), c.get("call_candidates")
        require(type(count) is int and 0 <= count <= 256 and isinstance(calls, list)
                and len(calls) == min(count, MAX_HELPER_CALLS)
                and c.get("calls_truncated") is (count > MAX_HELPER_CALLS), "callee call bounds")
        ats = []
        for ident in calls:
            at = ident.get("call_rva")
            require(type(at) is int and root <= at < root + 768
                    and ident.get("kind") in ("direct", "memory_indirect", "register_indirect")
                    and ident.get("runtime_target_or_effects_proven") is False, "callee CALL effect")
            ats.append(at)
        require(ats == sorted(set(ats)), "callee CALL order")
    def ban(obj):
        if isinstance(obj, dict):
            require(not (set(obj) & FORBIDDEN), "original payload")
            for v in obj.values():
                ban(v)
        elif isinstance(obj, list):
            for v in obj:
                ban(v)
    ban(d)
    return True

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--report", required=True, type=Path)
    path = p.parse_args().report
    require(path.stat().st_size <= 250000, "report size")
    validate(json.loads(path.read_text()))
    print("TW10_R37_STRICT_STATIC=PASS; NATIVE_HANDLE_SAVE=OPEN")

if __name__ == "__main__":
    main()
