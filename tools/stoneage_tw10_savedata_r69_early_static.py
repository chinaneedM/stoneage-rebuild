"""R69: original-static early return and both direct entering predicates only."""
import argparse
import hashlib
import json
from pathlib import Path
import tempfile

BASE = Path(__file__).resolve().parents[1] / "research/recovered"
RUNTIME_SHA = "cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a"
R67_SHA = "8bb5923de9a630a953de6c62cf9c10463aed9a4066db9a0aa97c7aaff338ab50"
ROOT = 0x4C5B4
TARGET = 0x4C5FE
PINS = {
    "r67": ("STONEAGE-TW10-SAVEDATA-NATIVE-TAIL-R67-ORIGINAL.json", "04162081d346b8c53424295de9fdc6b8f385b011"),
    "r63": ("STONEAGE-TW10-SAVEDATA-POSTCALL-R63-DERIVED.json", "3b7c9cea63ed4e2a360ddb6934e7dcd44b9833e7"),
    "preflight": ("STONEAGE-TW10-SAVEDATA-R69-PREFLIGHT.json", "f46c50e58885276c85773321f0f35c9f0d635412"),
}
FALSE = ("original_program_executed", "original_savedata_payload_read_or_published",
         "actual_native_return_count_or_success_proven", "actual_path_predicates_or_values_proven",
         "actual_abi_frame_register_memory_preservation_proven", "actual_flush_close_or_persistence_proven",
         "original_schema_or_server_authority_proven", "stage_b_started")


def need(ok, why):
    if not ok:
        raise ValueError("R69 early static: " + why)


def priors():
    out = {}
    for key, (name, pin) in PINS.items():
        raw = (BASE / name).read_bytes()
        need(hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == pin, "pinned prior " + key)
        out[key] = json.loads(raw)
    need(out["preflight"]["report_count"] == 133 and out["preflight"]["decoded_hits"] == []
         and out["preflight"]["target_rva"] == TARGET, "fresh retained-source gap")
    return out


def selection(nodes, edges, row):
    """Bound the needed prefix and late predicate, with exact one-hop closure."""
    nodes, edges = set(nodes), set(edges)
    focus = {at for at in nodes if ROOT <= at <= 0x4C600 or 0x4C71C <= at <= 0x4C72B}
    need(len(focus) == 32 and TARGET in focus, "fixed incoming-predicate focus")
    selected = set(focus)
    for a, b in edges:
        need(a in nodes and b in nodes, "graph endpoints")
        if a in focus or b in focus:
            selected.update((a, b))
    need(len(selected) <= 48, "narrow operand cap")
    rows = [row(at) for at in sorted(selected)]
    need([r.get("site_rva") for r in rows] == sorted(selected), "exact row inventory")
    for r in rows:
        need(isinstance(r.get("mnemonic"), str) and bool(r["mnemonic"]) and isinstance(r.get("operands"), list)
             and r.get("actual_instruction_effect_or_value_known") is False, "static row only")
        need(not set(r) & {"bytes", "raw_binary", "source_code", "original_payload"}, "no raw original disclosure")
    return {
        "focus_node_rvas": sorted(focus), "selected_node_rvas": sorted(selected),
        "decoded_instruction_rows": rows,
        "selected_internal_edges": [list(e) for e in sorted(edges) if e[0] in selected and e[1] in selected],
        "target_direct_predecessors": sorted(a for a, b in edges if b == TARGET),
        "focus_predecessors": {str(at): sorted(a for a, b in edges if b == at) for at in sorted(focus)},
        "focus_successors": {str(at): sorted(b for a, b in edges if a == at) for at in sorted(focus)},
    }


def inspect_verified(runtime):
    need(hashlib.sha256(runtime).hexdigest() == RUNTIME_SHA, "original runtime SHA256")
    old = priors()
    from tools.stoneage_tw10_savedata_r67_tail_static import inspect_verified as original_r67
    from tools.stoneage_tw10_savedata_native_io_r28 import candidate_graph
    from tools.stoneage_tw10_savedata_native_io_r37 import instruction_row
    from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
    from tools.stoneage_tw10_mapcache_binary_probe import image_layout
    r67 = original_r67(runtime)
    raw67 = (json.dumps(r67, sort_keys=True) + "\n").encode()
    need(hashlib.sha256(raw67).hexdigest() == R67_SHA and r67 == old["r67"], "exact original R67 rederivation")
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "sa_3.exe"
        p.write_bytes(runtime)
        data, pe, base, sections, _ = image_layout(p)
    for meta, sec in zip(sections, pe.sections):
        meta["characteristics"] = int(sec.Characteristics)
    t = next(s for s in sections if s["name"] == ".text")
    dec = Decoder(data[t["raw"]:t["raw"]+t["raw_size"]], t["rva"], base)
    nodes, edges, frontier, cap = candidate_graph(dec, ROOT)
    need(base == 0x400000 and sorted(nodes) == r67["bounded_graph_node_rvas"] and
         [list(e) for e in sorted(edges)] == r67["bounded_graph_edges"] and not frontier and not cap,
         "unchanged original bounded graph")
    result = selection(nodes, edges, lambda at: instruction_row(dec, sections, nodes, at))
    by = {r["site_rva"]: r for r in result["decoded_instruction_rows"]}
    for previous in [r67["decoded_instruction_rows"], *[s["decoded_instruction_rows"] for s in old["r63"]["sites"]]]:
        for r in previous:
            if r["site_rva"] in by:
                need(by[r["site_rva"]] == r, "old overlapping operand row")
    return {
        "schema": "tw10-r69-original-static-early-return-prefix-and-late-predicate",
        "runtime_sha256": RUNTIME_SHA, "image_base": base,
        "source_git_blobs": {k: v[1] for k, v in PINS.items()},
        "r67_exact_original_rederived_sha256": R67_SHA,
        "root_rva": ROOT, "previously_undecoded_target_rva": TARGET,
        "bounded_graph_node_rvas": sorted(nodes), "bounded_graph_edges": [list(e) for e in sorted(edges)],
        "bounded_graph_frontier": [], "bounded_graph_node_cap_hit": False,
        "selection_rule": "root prefix through 0x4c600 plus late 0x4c71c..0x4c72b predicate and exact one-hop incidence",
        **result, **{k: False for k in FALSE},
        "next": "Independently authenticate and reconcile the third return-source syntax and both entry predicates; do not admit native IO or persistence.",
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--bin", type=Path, required=True)
    a = p.parse_args()
    from tools.stoneage_tw10_savedata_probe import RUNTIME_PATH
    from tools.stoneage_tw10_technical_probe import find_rows, extract_row
    image, rows, _, _ = find_rows(a.bin)
    try:
        files = {r["path"]: r for r in rows if not r["is_dir"]}
        with tempfile.TemporaryDirectory() as td:
            exe = Path(td) / "sa_3.exe"
            extract_row(image, files[RUNTIME_PATH], exe)
            result = inspect_verified(exe.read_bytes())
    finally:
        image.close()
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
