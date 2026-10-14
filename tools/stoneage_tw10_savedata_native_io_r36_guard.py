"""R36 strict bounds and internally recomputed routes; original custody separate."""
import argparse
import json
from pathlib import Path
from tools.stoneage_tw10_savedata_native_io_r36 import *
from tools.stoneage_tw10_savedata_native_io_r30_guard import graph_guard
from tools.stoneage_tw10_savedata_native_io_r29_guard import input_guard, shape_guard
from tools.stoneage_tw10_savedata_upstream_r22_guard import FORBIDDEN

def require(ok, why):
    if not ok:
        raise ValueError("R36 " + why)

def validate(d):
    require(isinstance(d, dict) and d.get("schema") == SCHEMA and d.get("status") == STATUS, "schema")
    require(d.get("runtime_sha256") == RUNTIME_SHA256 and d.get("savedata_sha256") == SAVEDATA_SHA256,
            "original identities")
    require(d.get("r35_exact_original_revalidated") is True and d.get("r35_exact_report_sha256") == PRIOR_SHA256
            and d.get("static_only") is True and all(d.get(f) is False for f in FLAGS), "prior/non-promotion")
    graph_guard(d.get("parent_graph", {}))
    t = d.get("bounded_topology", {})
    ns, es = t.get("node_rvas"), t.get("edges")
    require(isinstance(ns, list) and len(ns) == d["parent_graph"]["nodes"]
            and all(type(n) is int and PARENT <= n < PARENT + 768 for n in ns)
            and ns == sorted(set(ns)) and t.get("complete_runtime_cfg_proven") is False, "node topology")
    require(isinstance(es, list) and len(es) == d["parent_graph"]["edges"]
            and all(isinstance(e, list) and len(e) == 2 and all(type(n) is int and n in ns for n in e) for e in es)
            and es == [list(e) for e in sorted(set(tuple(e) for e in es))], "edge topology")
    b = d.get("branch", {})
    require(b == {"site_rva": BRANCH, "mnemonic": "jne", "direct_target_rva": CONTINUATION,
                  "fallthrough_rva": 0x4ed18}, "branch geometry")
    require([BRANCH, CONTINUATION] in es and [BRANCH, 0x4ed18] in es, "branch edge absent")
    sh = d.get("test_shape", {})
    shape_guard({"site_rva": TEST, "class": "unmodeled", "operands": sh.get("operands")}, TEST)
    require(sh.get("site_rva") == TEST and sh.get("mnemonic") == "test"
            and sh.get("actual_inputs_or_predicate_value_proven") is False
            and branch_model(sh, "jne")["qualified_test_eax_eax_jne_syntax"] is True
            and d.get("conditional_predicate") == branch_model(sh, "jne"), "symbolic predicate")
    fs = d.get("branch_flag_sources", {})
    require(isinstance(fs.get("candidates"), list) and len(fs["candidates"]) <= 256
            and all(r.get("site_rva") in ns and r.get("kind") in ("zf_write", "opaque_call") for r in fs["candidates"])
            and type(fs.get("predecessor_nodes_examined")) is int and 0 <= fs["predecessor_nodes_examined"] <= 257
            and type(fs.get("predecessor_cap_hit")) is bool and type(fs.get("branch_disconnected_in_graph")) is bool
            and fs.get("actual_flag_value_known") is False, "flag provenance bounds")
    require(fs["candidates"] == [{"site_rva": TEST, "kind": "zf_write"}]
            and fs["predecessor_cap_hit"] is False and fs["branch_disconnected_in_graph"] is False
            and [e for e in es if e[1] == BRANCH] == [[TEST, BRANCH]], "unique TEST-to-JNE source")
    identities = d.get("opaque_calls")
    require(isinstance(identities, list) and len(identities) <= 256, "call bound")
    calls = []
    for ident in identities:
        at = ident.get("call_rva")
        require(at in ns and ident.get("kind") in ("direct", "memory_indirect", "register_indirect")
                and ident.get("runtime_target_or_effects_proven") is False, "opaque CALL")
        imported, name = ident.get("import_slot_association_proven"), ident.get("import_identity")
        require(type(imported) is bool and ((imported and ident["kind"] == "memory_indirect"
                and isinstance(name, dict) and type(name.get("iat_rva")) is int
                and isinstance(name.get("dll"), str) and isinstance(name.get("name"), str))
                or (not imported and name is None)), "import association")
        calls.append(at)
    require(calls == sorted(set(calls)), "CALL order")
    expected = [route(t, calls, start, goal) for start in (CONTINUATION, 0x4ed18)
                for goal in (CLOSE, ERROR, CONTINUATION)]
    require(d.get("routes") == expected, "route topology/barriers changed")
    keys = input_guard(d.get("input_sources", {}), PARENT)
    require(all(k in keys for k in ((TEST, "eax"), (BRANCH, "eax"), (CONTINUATION, "esi"),
                (CONTINUATION, "eax"), (0x4ed0d, "esi"), (0x4ed18, "esi"))), "missing input surface")
    comparison = d.get("push_spelling_comparison", {})
    pair = []
    for key, site in (("getfiletype_suffix", 0x4ed0d), ("closehandle_suffix", 0x4ed18)):
        s = comparison.get(key, {})
        require(s.get("linear_call_boundary_reached") is True and s.get("conditional_pre_call_esp_only") is True
                and s.get("abi_roles_applied") is False and s.get("actual_stack_values_known") is False
                and isinstance(s.get("pushes"), list) and len(s["pushes"]) == 1, "PUSH suffix")
        p = s["pushes"][0]
        require(p.get("site_rva") == site and p.get("conditional_pre_call_esp_offset") == 0
                and p.get("input", {}).get("kind") == "register"
                and p["input"].get("width_bytes") == 4, "PUSH primitive")
        pair.append(p["input"])
    require(comparison.get("same_single_register_operand_shape") is (pair[0] == pair[1])
            and comparison.get("actual_value_binding_or_callee_preservation_proven") is False, "same spelling not binding")
    stores = d.get("continuation_memory_stores", {})
    count, samples = stores.get("count"), stores.get("samples")
    require(type(count) is int and 0 <= count <= 256 and isinstance(samples, list)
            and len(samples) == min(count, MAX_STORES) and stores.get("samples_truncated") is (count > MAX_STORES)
            and stores.get("complete_alias_writers_or_initialization_proven") is False, "store bounds")
    last = -1
    forward = closure(es, CONTINUATION)
    for r in samples:
        at, ops = r.get("site_rva"), r.get("operands")
        shape_guard({"site_rva": at, "class": "mov", "operands": ops}, at)
        require(type(at) is int and at > last and at in ns and at in forward and r.get("mnemonic") == "mov"
                and len(ops) == 2 and ops[0].get("kind") == "memory" and ops[0].get("decoder_write") is True
                and r.get("actual_store_value_or_handle_owner_proven") is False, "store primitive")
        projections, addresses = store_register_queries(ops)
        regs = sorted({p["query_register"] for p in projections})
        require(r.get("source_registers") == regs and r.get("source_register_projections") == projections
                and r.get("address_registers") == addresses
                and (all((at, reg) in keys for reg in set(regs) | set(addresses))
                or d["input_sources"]["query_limit_hit"]), "store source refs")
        last = at
    def ban(o):
        if isinstance(o, dict):
            require(not set(o) & FORBIDDEN, "original payload")
            for v in o.values():
                ban(v)
        elif isinstance(o, list):
            for v in o:
                ban(v)
    ban(d)
    return True

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--report", type=Path, required=True)
    path = p.parse_args().report
    require(path.stat().st_size <= 100000, "report size")
    validate(json.loads(path.read_text()))
    print("TW10_R36_STRICT_STATIC=PASS; NATIVE_HANDLE_SAVE=OPEN")

if __name__ == "__main__":
    main()
