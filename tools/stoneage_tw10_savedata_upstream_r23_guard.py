"""Strict R23 derivative limits; original run/artifact custody checked separately."""
import argparse
import json
from pathlib import Path
from tools.stoneage_tw10_savedata_upstream_r23 import (
    SCHEMA, STATUS, FLAGS, CALLS, GLOBALS, RUNTIME_SHA256, SAVEDATA_SHA256)
from tools.stoneage_tw10_savedata_upstream_r22_guard import source_guard, FORBIDDEN

def require(ok, why):
    if not ok:
        raise ValueError("R23 " + why)

def validate(d):
    require(isinstance(d, dict) and d.get("schema") == SCHEMA and d.get("status") == STATUS, "schema")
    require(d.get("runtime_sha256") == RUNTIME_SHA256 and d.get("savedata_sha256") == SAVEDATA_SHA256, "hash")
    require(d.get("static_only") is True and d.get("r22_original_identity_revalidated") is True, "prior gate")
    require(all(d.get(k) is False for k in FLAGS), "runtime promotion")
    rows = d.get("heap_links")
    require(isinstance(rows, list) and len(rows) == 3, "three original links")
    for row, (name, anchor, call, store, target, slot) in zip(rows, CALLS):
        require((row.get("name"), row.get("anchor_rva"), row.get("call_rva"),
                 row.get("store_rva"), row.get("target_global_rva")) ==
                (name, anchor, call, store, target), "link identity/order")
        i = row.get("call_identity", {})
        require(i.get("call_rva") == call and i.get("kind") == "memory_indirect"
                and i.get("import_identity") == {"dll": "KERNEL32.dll", "name": name, "iat_rva": slot}
                and i.get("import_slot_association_proven") is True
                and i.get("runtime_target_or_effects_proven") is False, "import/effect")
        g = i.get("memory_target", {})
        require(g.get("width_bytes") == 4 and all(g.get(k) is None for k in
                ("base_register", "index_register", "segment_register"))
                and g.get("displacement_region", {}).get("displacement_rva") == slot, "import geometry")
        w = row.get("write", {})
        require(w.get("site_rva") == store and w.get("expected_global_rva") == target
                and w.get("mnemonic_class") == "mov"
                and w.get("source_operand", {}).get("register") == "eax"
                and w.get("source_operand", {}).get("width_bytes") == 4, "store syntax")
        dst = w.get("destination", {})
        require(dst.get("write_width_bytes") == 4
                and dst.get("displacement_region", {}).get("displacement_rva") == target
                and all(w.get(k) is False for k in ("register_inputs_resolved", "executed_write_proven",
                    "effective_object_proven", "named_caller_effect_admitted", "previous_destination_value_required")), "store effect")
        require(type(row.get("nodes")) is int and 1 <= row["nodes"] <= 128
                and type(row.get("edges")) is int and 0 <= row["edges"] <= 350
                and type(row.get("structural_call_to_store")) is bool, "graph bounds")
        require(row.get("call_is_opaque_value_barrier") is True
                and row.get("same_address_not_same_runtime_heap") is True
                and row.get("runtime_return_or_write_known") is False
                and row.get("heap_owner_or_success_known") is False, "heap promotion")
        source_guard(row.get("store_eax_sources", {}))
        s = row.get("local_push_suffix", {})
        require(s.get("conditional_pre_call_esp_only") is True
                and s.get("abi_roles_applied") is False and s.get("actual_stack_values_known") is False
                and type(s.get("linear_call_boundary_reached")) is bool
                and s.get("stop_reason") in ("candidate_anchor", "control_transfer", "stack_or_memory_barrier",
                    "push_cap", "decode_or_boundary_gap", "bound"), "suffix uncertainty")
        pushes = s.get("pushes")
        require(isinstance(pushes, list) and len(pushes) <= 24
                and (s["linear_call_boundary_reached"] or not pushes), "suffix bounds")
        previous = call
        for n, p in enumerate(pushes):
            require(type(p.get("site_rva")) is int and anchor <= p["site_rva"] < previous
                    and p.get("conditional_pre_call_esp_offset") == 4 * n
                    and p.get("input", {}).get("width_bytes") == 4, "suffix order/width")
            previous = p["site_rva"]
        refs = row.get("global_push_candidates")
        require(isinstance(refs, list) and len(refs) <= 32, "global candidate bound")
        for p in refs:
            geom = p.get("operand", {}).get("geometry", {})
            require(p.get("global_rva") in GLOBALS and anchor <= p.get("site_rva", -1) < call
                    and type(p.get("graph_path_to_call")) is bool
                    and p.get("operand", {}).get("kind") == "memory"
                    and geom.get("width_bytes") == 4
                    and geom.get("displacement_region", {}).get("displacement_rva") == p["global_rva"]
                    and all(geom.get(k) is None for k in ("base_register", "index_register", "segment_register")), "global operand")
    def ban(obj):
        if isinstance(obj, dict):
            require(not set(obj) & FORBIDDEN, "proprietary payload")
            for value in obj.values():
                ban(value)
        elif isinstance(obj, list):
            for value in obj:
                ban(value)
    ban(d)
    return True

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--report", type=Path, required=True)
    path = p.parse_args().report
    require(path.stat().st_size <= 70000, "report bound")
    validate(json.loads(path.read_text()))
    print("TW10_R23_STRICT_STATIC=PASS; HEAP_OWNERSHIP_NATIVE_IO=OPEN")

if __name__ == "__main__":
    main()
