"""Independent numerical acceptance of the R65 permanent-metadata join.

This verifier intentionally does not import the R65 derivation. The complete
semantic replay is a separate CI gate. Digest custody is not runtime proof.
"""
import argparse
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / "research/recovered"
PINS = {
    "r28": ("STONEAGE-TW10-SAVEDATA-NATIVE-IO-R28-ORIGINAL.json", "3671661219120d45bd922e05b6df371523b42432"),
    "r41": ("STONEAGE-TW10-SAVEDATA-NATIVE-IO-R41-ORIGINAL.json", "7250a7c5b45a054d5ee8c3e92f14cd32612f3ac8"),
    "r63": ("STONEAGE-TW10-SAVEDATA-POSTCALL-R63-DERIVED.json", "3b7c9cea63ed4e2a360ddb6934e7dcd44b9833e7"),
    "r64": ("STONEAGE-TW10-SAVEDATA-FLAGS-R64-DERIVED.json", "57cc0ea45bba16d994bb9fda47af257b6ddbb9df"),
}
NEGATIVE = (
    "original_program_or_native_api_executed", "actual_flags_or_branch_feasibility_proven",
    "complete_original_cfg_predecessors_proven", "actual_frame_abi_or_register_preservation_proven",
    "actual_count_pointer_address_or_memory_contents_proven", "actual_native_bool_or_transferred_count_proven",
    "actual_flush_close_or_persistence_proven", "original_savedata_payload_or_schema_evaluated",
    "original_server_authority_proven", "stage_b_started", "original_full_cfg_or_runtime_coverage_claimed",
    "original_media_reacquisition_required_for_this_scope",
)


def require(ok, why):
    if not ok:
        raise ValueError("R65 independent acceptance: " + why)


def validate(d, raws):
    require(set(raws) == set(PINS), "source inventory")
    for key, (_, sha) in PINS.items():
        raw = raws[key]
        actual = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        require(actual == sha, "original-derived immutable source " + key)
    r41, r63 = json.loads(raws["r41"]), json.loads(raws["r63"])
    require(r41["image_base"] == d.get("image_base") == 4194304, "image-base custody")
    require(d.get("runtime_sha256") == r41["runtime_sha256"] == r63["runtime_sha256"], "runtime custody")
    require(d.get("schema") == "tw10-r65-retained-cross-window-je-flags-count-pointer-static", "schema")
    require(d.get("source_git_blobs") == {k: v[1] for k, v in PINS.items()}, "reported source pins")
    for key in NEGATIVE:
        require(d.get(key) is False, "runtime or coverage promotion " + key)
    rows = {r["site_rva"]: r for s in r63["sites"] for r in s["decoded_instruction_rows"]}
    edges = {tuple(e) for s in r63["sites"] for e in s["bounded_local_edges"]}
    require(d.get("union_instruction_rows") == len(rows) == 60 and
            d.get("union_retained_edges") == len(edges) == 55, "bounded union inventory")
    branches = d.get("branches", [])
    require(len(branches) == 2, "two branch contexts")
    for b, values in zip(branches, (
        (312972, 312978, 312980, 312982, 313049, False, [0], [1]),
        (313073, 313079, 313081, 313083, 313094, True, [1], [1]),
    )):
        call, test, je, fall, target, retained, bw, tw = values
        require([b.get(k) for k in ("call_rva", "test_rva", "je_rva", "fallthrough_rva",
                                    "normalized_taken_target_rva")] == [call, test, je, fall, target], "branch coordinates")
        # Separate VA normalization and exact decoded operand from graph edges.
        require(b.get("decoded_taken_target_va") == rows[je]["operands"][0]["constant"] == target + 4194304,
                "VA normalization")
        require(rows[test]["mnemonic"] == "test" and rows[je]["mnemonic"] == "je"
                and [o["register"] for o in rows[test]["operands"]] == ["eax", "eax"], "source TEST/JE")
        require(b.get("retained_local_predecessors") == sorted(a for a, z in edges if z == je) == [test]
                and b.get("test_is_sole_flag_source_on_retained_direct_edge") is True, "local flag provenance")
        require(b.get("taken_edge_retained_in_one_r63_window") is retained
                and ((je, target) in edges) is retained
                and b.get("taken_edge_reconstructed_from_operand") is True, "observed versus reconstructed edge")
        require(b.get("branch_window_indices") == bw and b.get("target_window_indices") == tw, "window scope")
        require(rows[target]["mnemonic"] == "call" and b.get("taken_target_indirect_slot_rva") ==
                rows[target]["operands"][0]["geometry"]["displacement_region"]["displacement_rva"] == 336012,
                "target opaque import slot")
        require(b.get("actual_branch_taken") is None, "no executed branch")
    expected = [(313058, 313003), (313092, 313005), (313103, 313005)]
    joins = d.get("operand_derived_rejoins", [])
    require(len(joins) == len(expected), "rejoin inventory")
    for j, (a, b) in zip(joins, expected):
        require(j == {"source_rva": a, "target_rva": b, "edge_retained_in_one_window": False,
                      "operand_derived_edge_only": True}, "rejoin source classification")
        require(rows[a]["mnemonic"] == "jmp" and rows[a]["operands"][0]["constant"] - 4194304 == b,
                "independent rejoin arithmetic")
    pointers = d.get("conditional_count_pointer_prefixes", [])
    require(len(pointers) == 2, "pointer candidates")
    for p, expected in zip(pointers, (
        (312953, 312958, "eax", 312972, 312982, [312953, 312956, 312958]),
        (313060, 313064, "ecx", 313073, 313083, [313060, 313063, 313064]),
    )):
        lea, push, reg, call, load, path = expected
        require([p.get(k) for k in ("lea_rva", "push_rva", "source_register", "native_call_rva", "postcall_load_rva")]
                == [lea, push, reg, call, load], "pointer coordinates")
        require(p.get("conditional_pre_call_esp_offset") == 12 and p.get("lea_to_push_retained_path") == path,
                "conditional pointer slot and prefix")
        require(all(tuple(e) in edges for e in zip(path, path[1:])), "original retained prefix edges")
        for at, op_index in ((lea, 1), (load, 1)):
            g = rows[at]["operands"][op_index]["geometry"]
            require(g["base_register"] == "ebp" and g["relative_field_offset"] == -12, "same offset geometry")
        require(p.get("same_displacement_spelling") is True and p.get("same_runtime_memory_address_proven") is False
                and p.get("memory_output_count_or_pointer_contents_known") is False, "no temporal alias promotion")
        require(len(p.get("barriers", [])) == 4, "explicit ABI/memory barriers")
    return {"guard": "PASS_STATIC_METADATA_ONLY", "native_persistence": "OPEN"}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--report", type=Path, required=True)
    p.add_argument("--source-dir", type=Path, default=BASE)
    a = p.parse_args()
    print(json.dumps(validate(json.loads(a.report.read_bytes()),
                             {k: (a.source_dir / v[0]).read_bytes() for k, v in PINS.items()}), sort_keys=True))


if __name__ == "__main__":
    main()
