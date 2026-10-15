"""R65: join retained static windows; never evaluate original code or save data.

Edges reconstructed from a decoded VA operand are explicitly distinguished from
edges actually retained inside an R63 window. Local predecessor completeness
does not establish completeness in the original 139-node graph.
"""
import argparse
import hashlib
import json
from pathlib import Path

from tools.stoneage_tw10_savedata_r64_flag_count import inspect_raw as replay_r64

BASE = Path(__file__).resolve().parents[1] / "research/recovered"
SOURCES = {
    "r28": ("STONEAGE-TW10-SAVEDATA-NATIVE-IO-R28-ORIGINAL.json", "3671661219120d45bd922e05b6df371523b42432"),
    "r41": ("STONEAGE-TW10-SAVEDATA-NATIVE-IO-R41-ORIGINAL.json", "7250a7c5b45a054d5ee8c3e92f14cd32612f3ac8"),
    "r63": ("STONEAGE-TW10-SAVEDATA-POSTCALL-R63-DERIVED.json", "3b7c9cea63ed4e2a360ddb6934e7dcd44b9833e7"),
    "r64": ("STONEAGE-TW10-SAVEDATA-FLAGS-R64-DERIVED.json", "57cc0ea45bba16d994bb9fda47af257b6ddbb9df"),
}
FALSE_FLAGS = (
    "original_program_or_native_api_executed",
    "actual_flags_or_branch_feasibility_proven",
    "complete_original_cfg_predecessors_proven",
    "actual_frame_abi_or_register_preservation_proven",
    "actual_count_pointer_address_or_memory_contents_proven",
    "actual_native_bool_or_transferred_count_proven",
    "actual_flush_close_or_persistence_proven",
    "original_savedata_payload_or_schema_evaluated",
    "original_server_authority_proven",
    "stage_b_started",
)


def need(ok, why):
    if not ok:
        raise ValueError("R65 static join: " + why)


def git_blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def reg(op, name):
    return op.get("kind") == "register" and op.get("register") == name and op.get("width_bytes") == 4


def frame(op, offset):
    g = op.get("geometry", {})
    return (op.get("kind") == "memory" and op.get("width_bytes") == 4
            and g.get("base_register") == "ebp" and g.get("index_register") is None
            and g.get("segment_register") is None and g.get("index_scale") == 1
            and g.get("relative_field_offset") == offset and g.get("width_bytes") == 4
            and g.get("displacement_region") is None)


def derive(r28, r41, r63, r64):
    """Structural analysis only; use inspect_raw for historical custody."""
    need(r41.get("image_base") == 0x400000 and r41.get("static_only") is True
         and r41.get("native_io_executed") is False, "R41 VA/RVA base and static scope")
    need(r41.get("runtime_sha256") == r63.get("runtime_sha256") == r28.get("runtime_sha256"),
         "cross-report runtime identity")
    for name in FALSE_FLAGS:
        need(name not in r63 or r63[name] is False, "no injected promotion " + name)
    # Replaying R64 requalifies the R63 structure and original R28 PUSH metadata.
    from tools.stoneage_tw10_savedata_r64_flag_count import trace
    need(trace(r63, r28) == r64, "R64 exact semantic replay")
    base = r41["image_base"]
    rows = {}
    windows = {}
    retained = set()
    for n, site in enumerate(r63["sites"]):
        for row in site["decoded_instruction_rows"]:
            at = row["site_rva"]
            need(at not in rows or rows[at] == row, "overlapping row disagreement")
            rows[at] = row
            windows.setdefault(at, []).append(n)
        retained.update(tuple(e) for e in site["bounded_local_edges"])

    def instruction(at, mnemonic):
        row = rows.get(at)
        need(row is not None and row["mnemonic"] == mnemonic, "row " + hex(at))
        return row

    def target(at, mnemonic):
        row = instruction(at, mnemonic)
        ops = row["operands"]
        need(len(ops) == 1 and ops[0].get("kind") == "immediate"
             and type(ops[0].get("constant")) is int, "direct branch VA operand")
        return ops[0]["constant"] - base

    branches = []
    for call, test, branch, fall, taken in (
        (0x4C68C, 0x4C692, 0x4C694, 0x4C696, 0x4C6D9),
        (0x4C6F1, 0x4C6F7, 0x4C6F9, 0x4C6FB, 0x4C706),
    ):
        t = instruction(test, "test")
        b = instruction(branch, "je")
        need(len(t["operands"]) == 2 and all(reg(o, "eax") for o in t["operands"]), "TEST EAX,EAX")
        need(t["decoder_written_registers"] == ["eflags"] and b["decoder_read_registers"] == ["eflags"]
             and b["decoder_written_registers"] == [], "TEST flag definition and JE use")
        predecessors = sorted(a for a, z in retained if z == branch)
        need(predecessors == [test] and (call, test) in retained and (branch, fall) in retained,
             "retained local TEST/JE predecessors and fallthrough")
        need(target(branch, "je") == taken and taken in rows, "taken target retained in union")
        dest = instruction(taken, "call")
        ops = dest["operands"]
        need(len(ops) == 1 and ops[0].get("kind") == "memory", "taken target indirect call")
        geometry = ops[0]["geometry"]
        need(geometry.get("displacement_region", {}).get("displacement_rva") == 0x5208C
             and geometry.get("base_register") is None and geometry.get("index_register") is None,
             "opaque call static slot")
        branches.append({
            "call_rva": call, "test_rva": test, "je_rva": branch,
            "decoded_taken_target_va": b["operands"][0]["constant"],
            "normalized_taken_target_rva": taken, "fallthrough_rva": fall,
            "retained_local_predecessors": predecessors,
            "test_is_sole_flag_source_on_retained_direct_edge": True,
            "taken_edge_retained_in_one_r63_window": (branch, taken) in retained,
            "taken_edge_reconstructed_from_operand": True,
            "branch_window_indices": windows[branch], "target_window_indices": windows[taken],
            "taken_target_indirect_slot_rva": 0x5208C,
            "condition": "ZF=1 if TEST EAX,EAX evaluates zero; incoming native EAX remains opaque",
            "actual_branch_taken": None,
        })

    joins = []
    for at, expected in ((0x4C6E2, 0x4C6AB), (0x4C704, 0x4C6AD), (0x4C70F, 0x4C6AD)):
        need(target(at, "jmp") == expected and expected in rows, "cross-window rejoin")
        joins.append({"source_rva": at, "target_rva": expected,
                      "edge_retained_in_one_window": (at, expected) in retained,
                      "operand_derived_edge_only": True})

    pointers = []
    for lea, push, register, call, load in (
        (0x4C679, 0x4C67E, "eax", 0x4C68C, 0x4C696),
        (0x4C6E4, 0x4C6E8, "ecx", 0x4C6F1, 0x4C6FB),
    ):
        l = instruction(lea, "lea")["operands"]
        p = instruction(push, "push")["operands"]
        read = instruction(load, "mov")["operands"]
        need(len(l) == 2 and reg(l[0], register) and frame(l[1], -12), "count candidate LEA frame geometry")
        need(len(p) == 1 and reg(p[0], register), "count candidate PUSH register")
        need(len(read) == 2 and reg(read[0], "eax") and frame(read[1], -12), "postcall count-shaped read")
        # Enumerate the straight local chain; never carry any register/memory
        # identity across the opaque native call.
        cursor = lea
        witness = [lea]
        while cursor != push:
            successors = sorted(b for a, b in retained if a == cursor)
            need(len(successors) == 1, "unique LEA-to-PUSH local continuation")
            cursor = successors[0]
            need(cursor <= push and cursor not in witness, "bounded acyclic pointer prefix")
            if cursor != push:
                row = rows[cursor]
                need(row["mnemonic"] != "call" and register not in row["decoder_written_registers"],
                     "pointer candidate overwritten or crossed call")
            witness.append(cursor)
        pointers.append({
            "lea_rva": lea, "push_rva": push, "source_register": register,
            "conditional_pre_call_esp_offset": 12, "lea_to_push_retained_path": witness,
            "symbolic_address_spelling": "EBP_before_native_call - 12",
            "native_call_rva": call, "postcall_load_rva": load,
            "postcall_load_spelling": "EAX <- [EBP_after_native_call - 12]",
            "same_displacement_spelling": True,
            "same_runtime_memory_address_proven": False,
            "memory_output_count_or_pointer_contents_known": False,
            "barriers": ["unproven stdcall argument binding", "opaque native return and memory effects",
                         "EBP/frame preservation and valid writable allocation unproven",
                         "same offset does not establish temporal address or memory identity"],
        })
    return {
        "schema": "tw10-r65-retained-cross-window-je-flags-count-pointer-static",
        "runtime_sha256": r63["runtime_sha256"], "image_base": base,
        "source_git_blobs": {k: v[1] for k, v in SOURCES.items()},
        "source_mode": "permanent derived metadata only; no original acquisition",
        "union_instruction_rows": len(rows), "union_retained_edges": len(retained),
        "branches": branches, "operand_derived_rejoins": joins,
        "conditional_count_pointer_prefixes": pointers,
        "original_media_reacquisition_required_for_this_scope": False,
        "original_full_cfg_or_runtime_coverage_claimed": False,
        **{k: False for k in FALSE_FLAGS},
        "next": "R66: audit retained native-context return/count consumers and predicates; separate conditional frame-local memory flow from actual IO and persistence; only reacquire missing exact rows.",
    }


def inspect_raw(raws):
    need(set(raws) == set(SOURCES), "exact source inventory")
    for key, (_, blob) in SOURCES.items():
        need(git_blob(raws[key]) == blob, "immutable Git blob " + key)
    r64 = replay_r64(raws["r63"], raws["r28"])
    need(r64 == json.loads(raws["r64"]), "archived R64 replay")
    return derive(*(json.loads(raws[k]) for k in ("r28", "r41", "r63", "r64")))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source-dir", type=Path, default=BASE)
    p.add_argument("--verify", type=Path)
    a = p.parse_args()
    result = inspect_raw({k: (a.source_dir / v[0]).read_bytes() for k, v in SOURCES.items()})
    if a.verify:
        need(result == json.loads(a.verify.read_bytes()), "exact archived R65 replay")
        print("TW10_R65_RETAINED_STATIC_JOIN=PASS; ACTUAL_NATIVE_PERSISTENCE=OPEN")
    else:
        print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
