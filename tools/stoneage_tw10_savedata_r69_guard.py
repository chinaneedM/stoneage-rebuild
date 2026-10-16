"""Independent numeric/incidence guard for R69 original-derived metadata."""
import argparse
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / "research/recovered"
PINS = {
    "r67": ("STONEAGE-TW10-SAVEDATA-NATIVE-TAIL-R67-ORIGINAL.json", "04162081d346b8c53424295de9fdc6b8f385b011"),
    "r63": ("STONEAGE-TW10-SAVEDATA-POSTCALL-R63-DERIVED.json", "3b7c9cea63ed4e2a360ddb6934e7dcd44b9833e7"),
    "preflight": ("STONEAGE-TW10-SAVEDATA-R69-PREFLIGHT.json", "f46c50e58885276c85773321f0f35c9f0d635412"),
}
NEGATIVE = ("original_program_executed", "original_savedata_payload_read_or_published",
            "actual_native_return_count_or_success_proven", "actual_path_predicates_or_values_proven",
            "actual_abi_frame_register_memory_preservation_proven", "actual_flush_close_or_persistence_proven",
            "original_schema_or_server_authority_proven", "stage_b_started")


def need(ok, why):
    if not ok:
        raise ValueError("R69 independent static guard: " + why)


def validate(d):
    old = {}
    for k, (name, pin) in PINS.items():
        raw = (BASE / name).read_bytes()
        need(hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == pin, "source prior " + k)
        old[k] = json.loads(raw)
    need(d.get("schema") == "tw10-r69-original-static-early-return-prefix-and-late-predicate", "schema")
    need(d.get("runtime_sha256") == old["r67"]["runtime_sha256"] and d.get("image_base") == 4194304,
         "runtime/base identity")
    need(d.get("source_git_blobs") == {k: v[1] for k, v in PINS.items()}, "prior custody pins")
    need(d.get("r67_exact_original_rederived_sha256") ==
         "8bb5923de9a630a953de6c62cf9c10463aed9a4066db9a0aa97c7aaff338ab50", "exact original rederivation")
    need(d.get("root_rva") == 312756 and d.get("previously_undecoded_target_rva") == 312830,
         "fixed original target")
    for k in NEGATIVE:
        need(d.get(k) is False, "nonpromotion " + k)
    nodes, edges = d.get("bounded_graph_node_rvas"), d.get("bounded_graph_edges")
    need(nodes == old["r67"]["bounded_graph_node_rvas"] and edges == old["r67"]["bounded_graph_edges"],
         "exact earlier graph topology")
    need(d.get("bounded_graph_frontier") == [] and d.get("bounded_graph_node_cap_hit") is False,
         "bounded graph scope")
    focus = sorted(n for n in nodes if 312756 <= n <= 312832 or 313116 <= n <= 313131)
    need(len(focus) == 32 and d.get("focus_node_rvas") == focus, "exact predicate/prefix selection")
    selected = set(focus)
    for a, b in edges:
        if a in focus or b in focus:
            selected.update((a, b))
    need(len(selected) <= 48 and d.get("selected_node_rvas") == sorted(selected), "exact one-hop closure")
    rows = d.get("decoded_instruction_rows", [])
    need([r.get("site_rva") for r in rows] == sorted(selected), "complete operand row inventory")
    for r in rows:
        need(isinstance(r.get("mnemonic"), str) and r["mnemonic"] and isinstance(r.get("operands"), list)
             and r.get("actual_instruction_effect_or_value_known") is False, "unexecuted decoded row")
        need(all(isinstance(r.get(k), list) for k in ("decoder_read_registers", "decoder_written_registers", "input_query_registers")), "register inventories")
    by = {r["site_rva"]: r for r in rows}
    for previous in [old["r67"]["decoded_instruction_rows"], *[s["decoded_instruction_rows"] for s in old["r63"]["sites"]]]:
        for r in previous:
            if r["site_rva"] in by:
                need(r == by[r["site_rva"]], "requalified overlapping instruction")
    need(d.get("selected_internal_edges") == [e for e in edges if e[0] in selected and e[1] in selected], "local edge replay")
    need(d.get("target_direct_predecessors") == [312828, 313131], "both target predecessors retained")
    for at in focus:
        need(d.get("focus_predecessors", {}).get(str(at)) == sorted(a for a, b in edges if b == at), "prefix predecessors")
        need(d.get("focus_successors", {}).get(str(at)) == sorted(b for a, b in edges if a == at), "prefix successors")
    def no_raw(x):
        if isinstance(x, dict):
            need(not set(x) & {"bytes", "raw_binary", "original_payload", "source_code", "original_savedata_bytes"}, "raw source disclosure")
            for v in x.values():
                no_raw(v)
        elif isinstance(x, list):
            for v in x:
                no_raw(v)
    no_raw(d)
    return {"status": "STRUCTURAL_DERIVED_METADATA_ONLY", "decoded_rows": len(rows), "native_persistence": "OPEN"}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--report", type=Path, required=True)
    a = p.parse_args()
    print(json.dumps(validate(json.loads(a.report.read_bytes())), sort_keys=True))


if __name__ == "__main__":
    main()
