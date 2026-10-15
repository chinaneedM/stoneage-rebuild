"""R67: narrowly derive native-tail operand/CFG metadata, never execute originals."""
import argparse
import hashlib
import json
from pathlib import Path
import tempfile

ROOT = 0x4C5B4
TAIL = (0x4C731, 0x4C73B, 0x4C741, 0x4C743, 0x4C746, 0x4C748, 0x4C74F,
        0x4C759, 0x4C75C, 0x4C75D, 0x4C75E, 0x4C75F, 0x4C760)
MISSING = TAIL[:-2]
RUNTIME_SHA = "cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a"
R63_SHA = "91b650db700cf892a7d8c8b2d36a9d49dbeca139be315856d31d59533056c1bd"
SCHEMA = "tw10-r67-original-static-native-tail-operand-neighborhood"
BASE = Path(__file__).resolve().parents[1] / "research/recovered"
PINS = {
    "r44": ("STONEAGE-TW10-SAVEDATA-NATIVE-IO-R44-ORIGINAL.json", "39c1c0f673747fb560cc285d627490e5cd38047a"),
    "r45": ("STONEAGE-TW10-SAVEDATA-NATIVE-IO-R45-ORIGINAL.json", "1e7fb71cec336c1b4fc531d4f4a6933c9f66d415"),
    "r63": ("STONEAGE-TW10-SAVEDATA-POSTCALL-R63-DERIVED.json", "3b7c9cea63ed4e2a360ddb6934e7dcd44b9833e7"),
    "r66": ("STONEAGE-TW10-SAVEDATA-R66-EXPANDED-TAIL-PREFLIGHT.json", "4544b2a428bca8571286530f3ea94e1991c6ad85"),
}
FALSE = ("original_program_executed", "original_savedata_payload_read_or_published",
         "actual_native_api_return_or_count_known", "actual_paths_or_conditions_proven",
         "actual_abi_frame_register_memory_preservation_proven", "actual_flush_close_or_persistence_proven",
         "original_savedata_schema_or_server_authority_proven", "stage_b_started")


def need(ok, why):
    if not ok:
        raise ValueError("R67 static tail: " + why)


def blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def priors(directory=BASE):
    out = {}
    for key, (name, sha) in PINS.items():
        raw = (directory / name).read_bytes()
        need(blob(raw) == sha, "immutable prior " + key)
        out[key] = json.loads(raw)
    need(out["r66"]["target_tail_sites_rva"] == list(MISSING) and
         out["r66"]["registered_source_count"] == 127 and
         out["r66"]["decoded_same_object_hits"] == [], "retained missing-row justification")
    return out


def neighborhood(nodes, edges, row):
    """Complete one-hop neighborhood of thirteen fixed tail sites, not a trace."""
    nodes = set(nodes)
    edges = set(edges)
    need(set(TAIL) <= nodes, "all fixed tail sites in original bounded graph")
    need(all(a in nodes and b in nodes for a, b in edges), "graph endpoints")
    selected = set(TAIL)
    for a, b in edges:
        if a in TAIL or b in TAIL:
            selected.update((a, b))
    need(len(selected) <= 48, "narrow one-hop operand row cap")
    rows = [row(at) for at in sorted(selected)]
    need([r["site_rva"] for r in rows] == sorted(selected), "complete ordered decoded neighborhood")
    for r in rows:
        need(isinstance(r.get("mnemonic"), str) and r["mnemonic"] and isinstance(r.get("operands"), list)
             and r.get("actual_instruction_effect_or_value_known") is False, "static row shape")
        need(not set(r) & {"bytes", "raw_binary", "source_code", "original_payload"}, "no raw original bytes")
    return {
        "selected_node_rvas": sorted(selected), "decoded_instruction_rows": rows,
        "selected_internal_edges": [list(e) for e in sorted(edges) if e[0] in selected and e[1] in selected],
        "tail_predecessors": {str(at): sorted(a for a, b in edges if b == at) for at in TAIL},
        "tail_successors": {str(at): sorted(b for a, b in edges if a == at) for at in TAIL},
        "complete_only_within_bounded_returning_call_graph": True,
    }


def inspect_verified(runtime, directory=BASE):
    need(hashlib.sha256(runtime).hexdigest() == RUNTIME_SHA, "original runtime SHA256")
    prior = priors(directory)
    # Static decoder imports are intentionally lazy: pure metadata tests never
    # need an original executable, Capstone or a platform-specific runtime.
    from tools.stoneage_tw10_savedata_r63_postcall_static import inspect_verified as prior_r63
    from tools.stoneage_tw10_savedata_native_io_r28 import candidate_graph
    from tools.stoneage_tw10_savedata_native_io_r37 import instruction_row
    from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
    from tools.stoneage_tw10_mapcache_binary_probe import image_layout
    r63 = prior_r63(runtime)
    raw63 = (json.dumps(r63, sort_keys=True) + "\n").encode()
    need(hashlib.sha256(raw63).hexdigest() == R63_SHA and r63 == prior["r63"], "exact original R63 rederivation")
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "sa_3.exe"
        p.write_bytes(runtime)
        data, pe, base, sections, _ = image_layout(p)
    for meta, sec in zip(sections, pe.sections):
        meta["characteristics"] = int(sec.Characteristics)
    text = next(s for s in sections if s["name"] == ".text")
    dec = Decoder(data[text["raw"]:text["raw"]+text["raw_size"]], text["rva"], base)
    nodes, edges, frontier, cap = candidate_graph(dec, ROOT)
    native45 = next(x for x in prior["r45"]["native_api_contexts"] if x["site_rva"] == 0x4C68C)
    native44 = next(x for x in prior["r44"]["native_contexts"] if x["native_root_candidate_rva"] == ROOT)
    need(base == 0x400000 and len(nodes) == 139 and len(edges) == 156 and not frontier and not cap,
         "exact original R28 root graph bounds")
    need(sorted(nodes) == native45["bounded_node_rvas"] ==
         [r["site_rva"] for r in native44["inherited_stack_effect_candidates"]], "R44/R45 original node identity")
    result = neighborhood(nodes, edges, lambda at: instruction_row(dec, sections, nodes, at))
    by = {r["site_rva"]: r for r in result["decoded_instruction_rows"]}
    known = [r for r in native44["literal_esp_adjustment_or_unknown_shapes"] if r["site_rva"] in TAIL[-2:]]
    need([by[r["site_rva"]] for r in known] == known and len(known) == 2, "existing LEAVE/RET exact requalification")
    for site in prior["r63"]["sites"]:
        for r in site["decoded_instruction_rows"]:
            if r["site_rva"] in by:
                need(by[r["site_rva"]] == r, "overlapping R63 operand equality")
    return {
        "schema": SCHEMA, "runtime_sha256": RUNTIME_SHA, "image_base": base,
        "source_git_blobs": {k: v[1] for k, v in PINS.items()},
        "r63_exact_original_rederived_sha256": R63_SHA,
        "candidate_root_rva": ROOT, "bounded_graph_node_rvas": sorted(nodes),
        "bounded_graph_edges": [list(e) for e in sorted(edges)],
        "bounded_graph_frontier": [], "bounded_graph_node_cap_hit": False,
        "originally_missing_operand_sites_rva": list(MISSING), "requalified_epilogue_sites_rva": list(TAIL[-2:]),
        "selection_rule": "thirteen fixed tail nodes plus exactly their direct predecessors/successors in accepted bounded graph",
        **result, **{k: False for k in FALSE},
        "next": "Independently authenticate source artifact and interpret tail return/count/error syntax without admitting native execution or persistence.",
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--bin", required=True, type=Path)
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
