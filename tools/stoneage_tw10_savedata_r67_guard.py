"""Independent R67 metadata gate: graph incidence is not native behavior."""
import argparse
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / "research/recovered"
TAIL = (313137, 313147, 313153, 313155, 313158, 313160, 313167,
        313177, 313180, 313181, 313182, 313183, 313184)
NEGATIVE = ("original_program_executed", "original_savedata_payload_read_or_published",
            "actual_native_api_return_or_count_known", "actual_paths_or_conditions_proven",
            "actual_abi_frame_register_memory_preservation_proven", "actual_flush_close_or_persistence_proven",
            "original_savedata_schema_or_server_authority_proven", "stage_b_started")
PINS = {
    "r44": ("STONEAGE-TW10-SAVEDATA-NATIVE-IO-R44-ORIGINAL.json", "39c1c0f673747fb560cc285d627490e5cd38047a"),
    "r45": ("STONEAGE-TW10-SAVEDATA-NATIVE-IO-R45-ORIGINAL.json", "1e7fb71cec336c1b4fc531d4f4a6933c9f66d415"),
    "r63": ("STONEAGE-TW10-SAVEDATA-POSTCALL-R63-DERIVED.json", "3b7c9cea63ed4e2a360ddb6934e7dcd44b9833e7"),
    "r66": ("STONEAGE-TW10-SAVEDATA-R66-EXPANDED-TAIL-PREFLIGHT.json", "4544b2a428bca8571286530f3ea94e1991c6ad85"),
}


def need(ok, why):
    if not ok:
        raise ValueError("R67 independent static guard: " + why)


def validate(d, directory=BASE):
    originals = {}
    for k, (name, pin) in PINS.items():
        raw = (directory / name).read_bytes()
        need(hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == pin, "prior blob " + k)
        originals[k] = json.loads(raw)
    need(d.get("schema") == "tw10-r67-original-static-native-tail-operand-neighborhood", "schema")
    need(d.get("source_git_blobs") == {k: v[1] for k, v in PINS.items()}, "source custody pins")
    need(d.get("runtime_sha256") == originals["r63"]["runtime_sha256"] and d.get("image_base") == 4194304,
         "runtime and VA/RVA identity")
    need(d.get("r63_exact_original_rederived_sha256") ==
         "91b650db700cf892a7d8c8b2d36a9d49dbeca139be315856d31d59533056c1bd", "rederived prior identity")
    for k in NEGATIVE:
        need(d.get(k) is False, "promotion " + k)
    need(d.get("candidate_root_rva") == 312756 and d.get("bounded_graph_frontier") == []
         and d.get("bounded_graph_node_cap_hit") is False
         and d.get("complete_only_within_bounded_returning_call_graph") is True, "bounded root scope")
    nodes = d.get("bounded_graph_node_rvas", [])
    prior45 = next(x for x in originals["r45"]["native_api_contexts"] if x["site_rva"] == 312972)
    need(nodes == prior45["bounded_node_rvas"] and len(nodes) == 139, "exact prior full node inventory")
    edges = d.get("bounded_graph_edges", [])
    need(len(edges) == 156 and edges == [list(e) for e in sorted({tuple(e) for e in edges})]
         and all(len(e) == 2 and all(type(a) is int and a in nodes for a in e) for e in edges), "bounded graph edges")
    need(d.get("originally_missing_operand_sites_rva") == list(TAIL[:-2]) and
         d.get("requalified_epilogue_sites_rva") == list(TAIL[-2:]), "new versus requalified sites")
    selected = set(TAIL)
    for a, b in edges:
        if a in TAIL or b in TAIL:
            selected.update((a, b))
    need(d.get("selected_node_rvas") == sorted(selected) and len(selected) <= 48, "exact one-hop scope")
    rows = d.get("decoded_instruction_rows", [])
    need([r.get("site_rva") for r in rows] == sorted(selected), "exact decoded row inventory")
    for r in rows:
        need(isinstance(r.get("mnemonic"), str) and bool(r["mnemonic"]) and isinstance(r.get("operands"), list)
             and r.get("actual_instruction_effect_or_value_known") is False, "static row")
        need(all(isinstance(r.get(k), list) for k in ("decoder_read_registers", "decoder_written_registers", "input_query_registers")),
             "decoder register inventories")
    def no_raw(x):
        if isinstance(x, dict):
            need(not set(x) & {"bytes", "raw_binary", "source_code", "original_payload", "original_savedata_bytes"}, "raw source disclosure")
            for v in x.values():
                no_raw(v)
        elif isinstance(x, list):
            for v in x:
                no_raw(v)
    no_raw(d)
    by = {r["site_rva"]: r for r in rows}
    native44 = next(x for x in originals["r44"]["native_contexts"] if x["native_root_candidate_rva"] == 312756)
    prior_epilogue = [r for r in native44["literal_esp_adjustment_or_unknown_shapes"] if r["site_rva"] in TAIL[-2:]]
    need(len(prior_epilogue) == 2 and all(by[r["site_rva"]] == r for r in prior_epilogue), "retained LEAVE/RET unchanged")
    for s in originals["r63"]["sites"]:
        for r in s["decoded_instruction_rows"]:
            if r["site_rva"] in by:
                need(r == by[r["site_rva"]], "old overlapping operand row unchanged")
    internal = [e for e in edges if e[0] in selected and e[1] in selected]
    need(d.get("selected_internal_edges") == internal, "exact local incidence")
    for at in TAIL:
        need(d.get("tail_predecessors", {}).get(str(at)) == sorted(a for a, b in edges if b == at), "all bounded predecessors")
        need(d.get("tail_successors", {}).get(str(at)) == sorted(b for a, b in edges if a == at), "all bounded successors")
    return {"status": "STRUCTURAL_DERIVED_METADATA_ONLY", "decoded_rows": len(rows), "native_persistence": "OPEN"}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--report", type=Path, required=True)
    a = p.parse_args()
    print(json.dumps(validate(json.loads(a.report.read_bytes())), sort_keys=True))


if __name__ == "__main__":
    main()
