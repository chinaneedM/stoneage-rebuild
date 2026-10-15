"""R66: retained count-consumer syntax and precisely bounded native-tail gaps.

Counts below describe metadata, not historical bytes transferred. Arithmetic
and field offsets are conditional instruction shapes, not save-file schema.
"""
import argparse
import hashlib
import json
from pathlib import Path

from tools.stoneage_tw10_savedata_r62_source_coverage import analyze_sources, load_directory
from tools.stoneage_tw10_savedata_r65_cross_window import BASE, SOURCES, frame, reg, inspect_raw

TARGETS = (0x4C696, 0x4C699, 0x4C69C, 0x4C69E, 0x4C6AB, 0x4C6AD,
           0x4C6B0, 0x4C6B2, 0x4C6DF, 0x4C6FB, 0x4C6FE, 0x4C701,
           0x4C70C, 0x4C731, 0x4C73B, 0x4C741, 0x4C743, 0x4C746,
           0x4C748, 0x4C74F, 0x4C759, 0x4C75C, 0x4C75D, 0x4C75E, 0x4C75F, 0x4C760)


def need(ok, why):
    if not ok:
        raise ValueError("R66 retained count ledger: " + why)


def blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def collect(d, targets=TARGETS):
    """Same-object mnemonic/operand census, never an exhaustive text search."""
    hits = {str(at): [] for at in targets}

    def visit(x, path, depth):
        need(depth < 45, "bounded nesting")
        if isinstance(x, dict):
            at = x.get("site_rva")
            if type(at) is int and at in targets:
                full = isinstance(x.get("mnemonic"), str) and bool(x["mnemonic"]) and isinstance(x.get("operands"), list)
                hits[str(at)].append({"path": path, "decoded_mnemonic_and_operands": full,
                                      "mnemonic": x["mnemonic"] if full else None})
            for k, v in x.items():
                if isinstance(v, (list, dict)):
                    visit(v, path + "." + k, depth + 1)
        elif isinstance(x, list):
            for i, v in enumerate(x):
                if isinstance(v, (list, dict)):
                    visit(v, path + "[" + str(i) + "]", depth + 1)

    visit(d, "$", 0)
    return hits


def consumer_contract(r63):
    rows = {r["site_rva"]: r for s in r63["sites"] for r in s["decoded_instruction_rows"]}
    edges = {tuple(e) for s in r63["sites"] for e in s["bounded_local_edges"]}

    def operands(at, mnemonic):
        row = rows.get(at)
        need(row is not None and row["mnemonic"] == mnemonic, "exact decoded row " + hex(at))
        need(row["actual_instruction_effect_or_value_known"] is False, "static-only row")
        return row["operands"]

    def pair(at, mnemonic, left, right):
        op = operands(at, mnemonic)
        need(len(op) == 2 and left(op[0]) and right(op[1]), "operand geometry " + hex(at))

    def path(ats):
        need(all((a, b) in edges for a, b in zip(ats, ats[1:])), "retained consumer path")
        return ats

    eax = lambda o: reg(o, "eax")
    edi = lambda o: reg(o, "edi")
    slot = lambda offset: lambda o: frame(o, offset)
    pair(0x4C696, "mov", eax, slot(-12))
    pair(0x4C699, "add", slot(-8), eax)
    pair(0x4C69C, "cmp", eax, edi)
    first = path([0x4C696, 0x4C699, 0x4C69C, 0x4C69E])
    j = operands(0x4C69E, "jl")
    need(len(j) == 1 and j[0].get("constant") == 0x44C6AB, "signed comparison target")
    pair(0x4C6FB, "mov", eax, slot(-12))
    pair(0x4C6FE, "mov", slot(8), edi)
    pair(0x4C701, "mov", slot(-8), eax)
    second = path([0x4C6FB, 0x4C6FE, 0x4C701, 0x4C704])
    pair(0x4C6DF, "mov", slot(8), eax)
    pair(0x4C70C, "mov", slot(8), eax)
    first_error = path([0x4C6D9, 0x4C6DF, 0x4C6E2])
    second_error = path([0x4C706, 0x4C70C, 0x4C70F])
    pair(0x4C6AB, "xor", edi, edi)
    pair(0x4C6AD, "mov", eax, slot(-8))
    pair(0x4C6B0, "cmp", eax, edi)
    join = path([0x4C6AD, 0x4C6B0, 0x4C6B2])
    j = operands(0x4C6B2, "jne")
    need(len(j) == 1 and j[0].get("constant") == 0x44C743, "common conditional target")
    return {
        "first_count_read_accumulate_compare_path": first,
        "first_count_read_symbol": "frame_after_first_native[-12]",
        "first_accumulator_update_shape": "frame[-8] <- frame[-8] + EAX (32-bit ADD syntax)",
        "first_compare_shape": "signed JL after CMP EAX,EDI; actual operands and feasibility unknown",
        "first_signed_target_rva": 0x4C6AB,
        "second_count_read_assign_path": second,
        "second_assignment_shapes": ["frame[+8] <- EDI", "frame[-8] <- EAX"],
        "opaque_call_result_store_paths": [first_error, second_error],
        "opaque_result_store_shape": "frame[+8] <- EAX after opaque slot call; not a validated OS error code",
        "common_accumulator_read_compare_path": join,
        "common_read_shape": "EAX <- frame[-8]; CMP EAX,EDI; JNE 0x4c743",
        "zero_edi_shape_rva": 0x4C6AB,
        "second_rejoin_bypasses_zero_edi_instruction": True,
        "edi_zero_on_all_rejoins_proven": False,
        "frame_offsets_are_savedata_fields": False,
        "actual_output_count_or_return_value_known": False,
    }


def analyze(directory):
    sources = load_directory(directory)
    # Requalify the complete prior 32-report scope and its independent controls.
    coverage = analyze_sources(sources)
    originals = {k: (directory / v[0]).read_bytes() for k, v in SOURCES.items()}
    r65 = inspect_raw(originals)
    sources.update({SOURCES[k][0]: originals[k] for k in ("r63", "r64")})
    need(len(sources) == 34, "exact R27-R58 plus permanent R63/R64 corpus")
    summary = []
    full = {str(at): [] for at in TARGETS}
    for name, raw in sorted(sources.items()):
        hits = collect(json.loads(raw))
        summary.append({"file": name, "git_blob": blob(raw), "bytes": len(raw),
                        "site_bearing_objects": {at: hs for at, hs in hits.items() if hs}})
        for at, entries in hits.items():
            full[at].extend({"file": name, **h} for h in entries if h["decoded_mnemonic_and_operands"])
    r44 = json.loads(sources["STONEAGE-TW10-SAVEDATA-NATIVE-IO-R44-ORIGINAL.json"])
    context = next(c for c in r44["native_contexts"] if c["native_root_candidate_rva"] == 0x4C5B4)
    tail = [x for x in context["inherited_stack_effect_candidates"] if 0x4C731 <= x["site_rva"] <= 0x4C760]
    need(len(tail) == 13, "retained thirteen tail stack-effect sites")
    epilogue = [x for x in context["literal_esp_adjustment_or_unknown_shapes"] if x["site_rva"] >= 0x4C731]
    need([(x["site_rva"], x["mnemonic"]) for x in epilogue] == [(0x4C75F, "leave"), (0x4C760, "ret")],
         "retained epilogue operand rows")
    return {
        "schema": "tw10-r66-retained-native-count-consumers-and-tail-operand-gap",
        "registered_scope": "R27-R58 plus R63/R64; same-site dictionary mnemonic+operand representation only",
        "report_count": len(summary), "reports": summary,
        "r62_prior_scope_report_count": coverage["report_count"],
        "r65_source_git_blobs": r65["source_git_blobs"],
        "consumer_contract": consumer_contract(json.loads(originals["r63"])),
        "decoded_rows_at_target_sites": full,
        "tail_stack_effect_rows_not_decoded_instructions": tail,
        "retained_epilogue_decoded_rows": epilogue,
        "missing_tail_decoded_sites": [x["site_rva"] for x in tail if not full[str(x["site_rva"]) ]],
        "missing_same_object_decoded_sites": [at for at in TARGETS if not full[str(at)]],
        "absence_is_bounded_to_registered_representation": True,
        "actual_native_bool_count_frame_alias_or_persistence_proven": False,
        "original_program_or_save_payload_executed": False,
        "stage_a_family_status": "PARTIAL_OPEN", "stage_b_started": False,
        "next": "R67: only after fresh custody, obtain nonexecuting original-static operands at the 11 missing R44 tail sites 0x4c731..0x4c75e, with required direct CFG edges; requalify retained LEAVE 0x4c75f / RET 0x4c760 instead of treating them as absent. Reconcile count/error return syntax, preserving call/frame/alias and execution barriers.",
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--directory", type=Path, default=BASE)
    p.add_argument("--verify", type=Path)
    a = p.parse_args()
    result = analyze(a.directory)
    if a.verify:
        need(result == json.loads(a.verify.read_bytes()), "exact permanent source census and contract replay")
        print("TW10_R66_RETAINED_COUNT_CONSUMERS_AND_TAIL_GAP=PASS; ORIGINAL_NATIVE_PERSISTENCE=OPEN")
    else:
        print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
