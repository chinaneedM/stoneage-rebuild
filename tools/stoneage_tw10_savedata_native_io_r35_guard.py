"""Reject R35 runtime/ABI/persistence promotion from original static evidence."""
import argparse
import json
from pathlib import Path

from tools.stoneage_tw10_savedata_native_io_r35 import *
from tools.stoneage_tw10_savedata_native_io_r30_guard import graph_guard
from tools.stoneage_tw10_savedata_native_io_r29_guard import input_guard
from tools.stoneage_tw10_savedata_upstream_r22_guard import FORBIDDEN

def require(test, context):
    if not test:
        raise ValueError("R35 " + context)

def validate(d):
    require(isinstance(d, dict) and d.get("schema") == SCHEMA and d.get("status") == STATUS,
            "schema/status")
    require(d.get("runtime_sha256") == RUNTIME_SHA256
            and d.get("savedata_sha256") == SAVEDATA_SHA256, "original identities")
    require(d.get("r34_exact_original_revalidated") is True
            and d.get("r34_exact_report_sha256") == PRIOR_SHA256
            and d.get("static_only") is True, "prior canonical")
    require(d.get("actual_stack_paths_alias_and_return_proven") is False
            and d.get("call_is_opaque_register_and_effect_barrier") is True
            and d.get("returning_call_graph_is_structural_only") is True
            and all(d.get(k) is False for k in FLAGS), "semantic non-promotion")
    graph_guard(d.get("parent_graph", {}))
    ident = d.get("opaque_call_identity", {})
    require(ident.get("call_rva") == OPAQUE
            and ident.get("kind") in ("direct", "memory_indirect", "register_indirect")
            and ident.get("runtime_target_or_effects_proven") is False, "CALL identity")
    kind = ident["kind"]
    if kind == "direct":
        require(type(ident.get("direct_target_rva")) is int
                and ident.get("import_identity") is None
                and ident.get("import_slot_association_proven") is False,
                "direct call not import")
    elif kind == "register_indirect":
        require(isinstance(ident.get("register_target"), str)
                and ident.get("import_identity") is None
                and ident.get("import_slot_association_proven") is False,
                "register-indirect identity")
    else:
        require(isinstance(ident.get("memory_target"), dict), "memory geometry")
        imported = ident.get("import_slot_association_proven")
        named = ident.get("import_identity")
        require(type(imported) is bool, "IAT association flag")
        if imported:
            require(isinstance(named, dict)
                    and isinstance(named.get("dll"), str) and bool(named["dll"])
                    and isinstance(named.get("name"), str) and bool(named["name"])
                    and type(named.get("iat_rva")) is int, "IAT metadata")
        else:
            require(named is None, "unproven IAT identity")
    suffix = d.get("opaque_call_pre_call_suffix", {})
    require(suffix.get("linear_call_boundary_reached") is True
            and suffix.get("conditional_pre_call_esp_only") is True
            and suffix.get("abi_roles_applied") is False
            and suffix.get("actual_stack_values_known") is False
            and suffix.get("stop_reason") in ("control_transfer", "candidate_anchor",
                  "stack_or_memory_barrier", "push_cap"), "conditional stack suffix")
    pushes = suffix.get("pushes")
    ps = d.get("opaque_call_push_candidates")
    require(isinstance(pushes, list) and isinstance(ps, list)
            and len(pushes) == len(ps) and len(ps) <= MAX_PUSHES,
            "bounded PUSH shapes")
    keys = input_guard(d.get("register_sources_before_and_after_call", {}), PARENT)
    require(all(k in keys for k in ((OPAQUE, "eax"), (OPAQUE, "esi"),
                                    (OPAQUE, "edi"), (TEST, "eax"),
                                    (CLOSE, "esi"))), "input surfaces")
    last = OPAQUE
    for idx, (p, old) in enumerate(zip(ps, pushes)):
        at = p.get("site_rva")
        require(type(at) is int and ANCHOR <= at < last
                and p.get("conditional_pre_call_esp_offset") == 4 * idx
                and p.get("input", {}).get("width_bytes") == 4
                and all(p.get(k) == v for k, v in old.items())
                and p.get("actual_argument_role_or_value_proven") is False,
                "PUSH geometry not ABI")
        op = p["input"]
        if op.get("kind") == "register":
            regs = [op.get("register")]
        else:
            geo = op.get("geometry") or {}
            regs = [geo.get("base_register"), geo.get("index_register")]
        refs = [{"site_rva": at, "register": r} for r in
                sorted({r for r in regs if r in ALIASES})]
        require(p.get("source_queries") == refs
                and (all((at, r) in keys for r in (x["register"] for x in refs))
                     or d["register_sources_before_and_after_call"]["query_limit_hit"]),
                "PUSH provenance")
        last = at
    def inspect(obj):
        if isinstance(obj, dict):
            require(not (set(obj) & FORBIDDEN), "forbidden original payload")
            for value in obj.values():
                inspect(value)
        elif isinstance(obj, list):
            for value in obj:
                inspect(value)
    inspect(d)
    return True

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--report", required=True, type=Path)
    args = p.parse_args()
    require(args.report.stat().st_size <= 75000, "bounded report")
    validate(json.loads(args.report.read_text()))
    print("TW10_R35_STRICT_STATIC=PASS; NATIVE_SAVE=OPEN")

if __name__ == "__main__":
    main()
