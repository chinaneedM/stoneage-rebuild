"""R70: source-pinned three-return syntax and invented uint32 arithmetic only."""
import argparse
import hashlib
import json
from pathlib import Path
import random

from tools.stoneage_tw10_savedata_r69_guard import validate as validate_r69
from tools.stoneage_tw10_savedata_r68_return_sources import reverse_sources, forward_sources

BASE = Path(__file__).resolve().parents[1] / "research/recovered"
U32 = 0xFFFFFFFF
R69_SHA = "26ff9f92d14a4ef385a279501e456b4bf58156209ad4471aef84109f6e16bfbe"
PINS = {
    "r69": ("STONEAGE-TW10-SAVEDATA-NATIVE-EARLY-R69-ORIGINAL.json", "d5d4924803dc28de8be00f712eecd11cf9003c66"),
    "r67": ("STONEAGE-TW10-SAVEDATA-NATIVE-TAIL-R67-ORIGINAL.json", "04162081d346b8c53424295de9fdc6b8f385b011"),
    "r63": ("STONEAGE-TW10-SAVEDATA-POSTCALL-R63-DERIVED.json", "3b7c9cea63ed4e2a360ddb6934e7dcd44b9833e7"),
}


def need(ok, why):
    if not ok:
        raise ValueError("R70 conditional returns: " + why)


def reg(o, r):
    return o.get("kind") == "register" and o.get("register") == r and o.get("width_bytes") == 4


def frame(o, offset):
    g = o.get("geometry", {})
    return (o.get("kind") == "memory" and o.get("width_bytes") == 4 and
            g.get("base_register") == "ebp" and g.get("index_register") is None and
            g.get("relative_field_offset") == offset and g.get("width_bytes") == 4 and
            g.get("segment_register") is None and g.get("displacement_region") is None)


def qualify(rows, edges):
    def shape(at, mnemonic):
        r = rows.get(at)
        need(r is not None and r["mnemonic"] == mnemonic and
             r["actual_instruction_effect_or_value_known"] is False, "original row " + hex(at))
        return r["operands"]
    zero = shape(0x4C5FE, "xor")
    ones = shape(0x4C759, "or")
    sub = shape(0x4C743, "sub")
    need(len(zero) == 2 and all(reg(o, "eax") for o in zero), "full-width self XOR")
    need(len(ones) == 2 and reg(ones[0], "eax") and ones[1].get("kind") == "immediate"
         and ones[1].get("constant") == U32 and ones[1].get("width_bytes") == 4, "all-ones destination syntax")
    need(len(sub) == 2 and reg(sub[0], "eax") and frame(sub[1], -16), "conditional subtraction geometry")
    need(sorted(a for a, b in edges if b == 0x4C5FE) == [0x4C5FC, 0x4C72B], "both early-return entrances")
    need(shape(0x4C5FC, "jne")[0]["constant"] == 0x44C605 and
         shape(0x4C72B, "je")[0]["constant"] == 0x44C5FE, "exact incoming branch targets")
    edi = shape(0x4C5F1, "xor")
    need(len(edi) == 2 and all(reg(o, "edi") for o in edi), "conditional zero EDI definition")
    cmp = shape(0x4C5F3, "cmp")
    need(len(cmp) == 2 and frame(cmp[0], 16) and reg(cmp[1], "edi"), "early parameter comparison shape")
    need(rows[0x4C5F3]["decoder_written_registers"] == ["eflags"] and
         rows[0x4C5FC]["decoder_read_registers"] == ["eflags"], "early predicate flags")
    for at, off in ((0x4C5F6, -8), (0x4C5F9, -16)):
        op = shape(at, "mov")
        need(len(op) == 2 and frame(op[0], off) and reg(op[1], "edi") and
             "eflags" not in rows[at]["decoder_written_registers"], "flag-neutral counter initialization")
    late = shape(0x4C728, "cmp")
    need(len(late) == 2, "late comparison operand count")
    g = late[0].get("geometry", {})
    need(len(late) == 2 and late[0].get("kind") == "memory" and late[0].get("width_bytes") == 1
         and g.get("base_register") == "eax" and g.get("index_register") is None
         and g.get("relative_field_offset") == 0 and late[1].get("constant") == 26,
         "late byte-comparison syntax")
    need(rows[0x4C728]["decoder_written_registers"] == ["eflags"] and
         rows[0x4C72B]["decoder_read_registers"] == ["eflags"], "late predicate flags")
    load = shape(0x4C725, "mov")
    need(len(load) == 2 and reg(load[0], "eax") and frame(load[1], 12), "late pointer-shaped frame load")
    paths = [
        [0x4C5F1, 0x4C5F3, 0x4C5F6, 0x4C5F9, 0x4C5FC, 0x4C5FE, 0x4C600, 0x4C75C],
        [0x4C725, 0x4C728, 0x4C72B, 0x4C5FE],
        [0x4C6AD, 0x4C6B0, 0x4C6B2, 0x4C743, 0x4C746, 0x4C75C],
        [0x4C759, 0x4C75C],
    ]
    need(all((a, b) in edges for p in paths for a, b in zip(p, p[1:])), "retained structural witnesses")
    return paths


def reference(kind, eax, adjustment):
    """Independently written architectural formula; no original values."""
    if kind == "zero":
        return 0
    if kind == "all_ones":
        return 2**32 - 1
    if kind == "subtraction":
        return (eax - adjustment) % (2**32)
    raise ValueError("R70 reference: unknown kind")


def execute_shape(row, eax, adjustment):
    need(type(eax) is int and type(adjustment) is int and 0 <= eax <= U32 and 0 <= adjustment <= U32,
         "invented uint32 input domain")
    op = row["operands"]
    need(len(op) == 2 and reg(op[0], "eax"), "modeled full register destination")
    if row["mnemonic"] == "xor" and reg(op[1], "eax"):
        return eax ^ eax
    if row["mnemonic"] == "or" and op[1].get("constant") == U32:
        return eax | U32
    if row["mnemonic"] == "sub" and frame(op[1], -16):
        return (eax - adjustment) & U32
    raise ValueError("R70 invented shape model: unsupported operand geometry")


def analyze(raws):
    need(set(raws) == set(PINS), "exact source inventory")
    sources = {}
    for key, (_, pin) in PINS.items():
        raw = raws[key]
        need(hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == pin, "immutable original-derived " + key)
        sources[key] = json.loads(raw)
    need(hashlib.sha256(raws["r69"]).hexdigest() == R69_SHA, "R69 exact raw SHA256")
    validate_r69(sources["r69"])
    rows = {}
    for report in [sources["r67"], *sources["r63"]["sites"], sources["r69"]]:
        for r in report["decoded_instruction_rows"]:
            need(r["site_rva"] not in rows or rows[r["site_rva"]] == r, "overlapping source row equality")
            rows[r["site_rva"]] = r
    nodes = set(sources["r69"]["bounded_graph_node_rvas"])
    edges = {tuple(e) for e in sources["r69"]["bounded_graph_edges"]}
    paths = qualify(rows, edges)
    fwd = forward_sources(nodes, edges, rows, 0x4C5B4, 0x4C760)
    rev = reverse_sources(nodes, edges, rows, 0x4C5B4, 0x4C760)
    expected = {("full_eax_definition", at) for at in (0x4C5FE, 0x4C743, 0x4C759)}
    need(fwd == rev == expected, "three exact direct return definitions; no undecoded barrier at return")
    edge = [0, 1, 26, 127, 128, 255, 0x7FFFFFFF, 0x80000000, U32]
    pairs = [(a, b) for a in edge for b in edge]
    rng = random.Random(0x70)
    pairs.extend((rng.randrange(2**32), rng.randrange(2**32)) for _ in range(256))
    profiles = (("zero", 0x4C5FE), ("subtraction", 0x4C743), ("all_ones", 0x4C759))
    for kind, at in profiles:
        need(all(execute_shape(rows[at], a, b) == reference(kind, a, b) for a, b in pairs), "invented arithmetic model " + kind)
    return {
        "schema": "tw10-r70-three-conditional-native-return-shapes",
        "source_git_blobs": {k: v[1] for k, v in PINS.items()}, "r69_raw_sha256": R69_SHA,
        "bounded_graph_nodes": len(nodes), "bounded_graph_edges": len(edges),
        "available_decoded_rows": len(set(rows) & nodes),
        "forward_reverse_direct_return_sources": [{"origin": k, "site_rva": at} for k, at in sorted(fwd)],
        "direct_return_source_unknown_barriers_remaining": [],
        "complete_full_function_operands_or_inputs_proven": False,
        "structural_paths_returning_call_assumption_only": paths,
        "conditional_early_zero_shape": "CMP frame[+16],EDI after XOR EDI,EDI; intervening frame[-8]/[-16] stores preserve flags; JNE fallthrough -> XOR EAX,EAX",
        "conditional_late_zero_shape": "MOV EAX,frame[+12]; CMP byte[EAX],26; JE -> XOR EAX,EAX; pointer/value/path validity unproven",
        "conditional_subtraction_shape": "32-bit (EAX - frame[-16]) modulo 2^32; EAX input and frame/memory validity unknown",
        "all_ones_shape_is_not_validated_native_error_semantics": True,
        "invented_pairs_per_return_shape": len(pairs), "invented_arithmetic_comparisons": len(pairs)*3,
        "no_original_values_used_in_numerical_model": True,
        "actual_original_path_predicates_or_return_values_proven": False,
        "actual_native_bool_count_or_success_proven": False,
        "actual_abi_frame_register_memory_alias_proven": False,
        "actual_flush_close_or_disk_persistence_proven": False,
        "original_savedata_schema_or_server_authority_proven": False,
        "original_program_or_payload_executed": False, "stage_b_started": False,
        "next": "R71 qualify frame[-16] adjustment update and native memory-count/return-unit relationships from retained evidence first; preserve opaque calls, path and frame/alias barriers.",
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--verify", type=Path)
    a = p.parse_args()
    report = analyze({k: (BASE / name).read_bytes() for k, (name, _) in PINS.items()})
    if a.verify:
        need(report == json.loads(a.verify.read_bytes()), "exact derived contract replay")
        print("TW10_R70_THREE_CONDITIONAL_RETURN_SHAPES=PASS; ORIGINAL_NATIVE_PERSISTENCE=OPEN")
    else:
        print(json.dumps(report, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
