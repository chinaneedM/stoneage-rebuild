"""Replay the preserved CN50 client's SPR-to-album rules and portrait lookup."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import struct
import subprocess
import tempfile

from tools.stoneage_cn50_spr_metadata import export_cn50_spr
from tools.stoneage_pet126k_cn50_original_exe_probe import EXPECTED
from tools.stoneage_pet126l_cn50_table_graphic_probe import (
    RESOURCE_DIR, ROWS, STRIDE, TABLE_OFFSET, digest, read_gz_rows, source_rows,
)
from tools.stoneage_pet126m_cn50_pe_album_xrefs import parse_objdump, pe32_text_identity
from tools.stoneage_pet_detail36_cn50_album_portrait_join import ALBUM, METADATA
from tools.stoneage_pet_high_first_cn50_catalog import COLUMNS, ROOT, build, git_blob

TARGET = ROOT / "research/pets/PET-HIGH-FIRST-CN50-NATIVE-SPR-ALBUM-R1.json"
GRAPHIC_BASE = 100250
SELECTOR_RANGES = (
    (0x4D7, 0x379), (0x4A2, 0x376), (0x494, 0x36D), (0x489, 0x364),
    (0x3A2, 0x2E9), (0x3A1, 0x284), (0x39F, 0x283), (0x384, 0x26D),
    (0xB4, 0x185),
)
HELD_PET_EXCLUSIONS = frozenset((
    0x18863, 0x18850, 0x18BA0, 0x18BA1, 0x186AF, 0x186B2, 0x18B9F, 0x18831, 0x18C26,
))
PORTRAIT_PREDECESSORS = dict(zip(range(28085, 28089), range(126066, 126070), strict=True))
SPR_TABLES = ("SPR-GROUP-R1.tsv.gz", "SPR-ANIMATION-R1.tsv.gz", "SPR-FRAME-R1.tsv.gz")
WINDOWS = (
    ("action_object_to_album", 0x430DEC, 0x430EA0, "7ca14ac8aa44f2eebf8647ac356628fdcc056fff87927e7ea992ea2e8594f8a5"),
    ("held_pet_to_album", 0x4345C0, 0x434705, "5ceb86ffa14f9eef365a766a950c7ddb37f95c5a6c04468bb6fe60b206aa843f"),
    ("album_rows_initialized", 0x430749, 0x43076B, "c72e0f80acf7fa1e2d49a75feb41ac9235b28df85fc3323dd3c32d71d0fd8d72"),
    ("held_pet_stores_album_name_and_portrait", 0x4346EB, 0x43477A,
     "20d2c1e5e8288a3f09e6eb7953b64d43a5497d1a3e80e4f8cb5012294449f216"),
    ("action_object_to_album_call", 0x430EEB, 0x430EF6,
     "0280200a0d2ab5281b06214d280243cc09b88c577c2c63d773e5e24631ed3e72"),
    ("held_pet_sprite_preview_call", 0x4340C8, 0x434129,
     "d947c16ee7ba6ebdb290eaa38e5b267a6997ea68beaabed2d721249349c5b249"),
    ("preview_copies_graphic_and_calls_sprite_lookup", 0x4303B2, 0x430423,
     "28bc015fafc6de931f846b7e27d18c845af81b5c33ec8317eefde22fd487834f"),
    ("sprite_group_action_lookup", 0x44E844, 0x44E88F,
     "e83f52fada6656f4fbe367d8398998b878578723917617d7a02fd1c706986817"),
    ("spradrn_index_loader", 0x411804, 0x41185C,
     "06b4d2c7c5db77107219f01c5e5441b2cb7ff0aa51c3a5e7d1233ccefbd4a028"),
    ("adrn_loader_overwrites_alias_in_file_order", 0x4114E8, 0x41157B,
     "8ff61e9a9a20a5bb28be1c16a96008c443f9369437f56ece7bdc197c85288f8e"),
    ("physical_bitmap_lookup_by_alias", 0x4116CD, 0x4116F3,
     "542eb03ef0ac63ba0f2d9beeff57c7e812965247d56ffb3c98738b03afba2240"),
    ("album_portrait_argument", 0x439F07, 0x439F39,
     "d49e6fe79bae9cb34268f3e7411cb9122ce1e0a804a5a3e2ddb2fcb9fa8afb75"),
    ("portrait_draw_queue_uses_resolved_bitmap", 0x453B91, 0x453C04,
     "3248f7f4631539318a5950e4ee6821ab31971acb4cd5a45b8ac16e7a09e5f1db"),
)


def album_ordinal(graphic, *, held_pet=False):
    """Inverse-searchable source rule, conditional on the original path being reached."""
    if held_pet and graphic in HELD_PET_EXCLUSIONS:
        return None
    offset = graphic - GRAPHIC_BASE
    if offset == 0x39F:
        return 0x125
    for threshold, deduction in SELECTOR_RANGES:
        if offset > threshold:
            offset -= deduction
            break
    return offset if 0 <= offset < ROWS else None


def read_inputs():
    manifest_raw = (ROOT / METADATA).read_bytes()
    if git_blob(manifest_raw) != "5063cf2fade4e0739ac35c38a90dfff1a43db960":
        raise ValueError("original resource manifest changed")
    manifest = json.loads(manifest_raw)
    table_pins = {row["name"]: row["sha256"] for row in manifest["tables"]}
    for filename in SPR_TABLES:
        if digest((RESOURCE_DIR / filename).read_bytes()) != table_pins[filename]:
            raise ValueError(f"original source-derived SPR metadata changed: {filename}")
    atlas, _ = build()
    named = [dict(zip(COLUMNS, row, strict=True)) for row in atlas]
    return manifest, table_pins, named


def build_catalog(manifest, table_pins, atlas):
    groups = list(read_gz_rows(RESOURCE_DIR / SPR_TABLES[0]))
    routed = defaultdict(list)
    metrics = Counter()
    for row in groups:
        graphic = int(row["spr_no"])
        ordinal = album_ordinal(graphic)
        if ordinal is not None:
            routed[ordinal].append(row)
    if len(groups) != 1185 or len({int(row["spr_no"]) for row in groups}) != len(groups):
        raise ValueError("unexpected original SPR group count or duplicate group ID")
    named_ordinals = {int(row["cn50_album_ordinal"]) for row in atlas}
    named_groups = {
        row["spr_no"] for ordinal in named_ordinals for row in routed[ordinal]
    }
    group_frames = Counter()
    for row in read_gz_rows(RESOURCE_DIR / SPR_TABLES[1]):
        if row["spr_no"] in named_groups:
            group_frames[row["spr_no"]] += int(row["frame_count"])
    if set(group_frames) != named_groups:
        raise ValueError("missing source animation metadata for named SPR groups")

    records = []
    for item in atlas:
        ordinal = int(item["cn50_album_ordinal"])
        alias = int(item["cn50_local_portrait_alias_u32"])
        sprite_groups = []
        for row in sorted(routed[ordinal], key=lambda row: int(row["spr_no"])):
            graphic = int(row["spr_no"])
            allowed_held = album_ordinal(graphic, held_pet=True) == ordinal
            sprite_groups.append({
                "spr_group": graphic,
                "sha256": row["segment_sha256"],
                "animation_header_count": int(row["anim_count"]),
                "frame_record_count": group_frames[row["spr_no"]],
                "held_pet_path_also_maps_to_slot": allowed_held,
            })
        held_count = sum(group["held_pet_path_also_maps_to_slot"] for group in sprite_groups)
        formula_id = int(item["cn50_formula_spr_graphic_number_UNVERIFIED"])
        formula_was_present = item["cn50_formula_spr_source_group_present"] == "YES"
        formula_agrees = any(group["spr_group"] == formula_id for group in sprite_groups)
        if not sprite_groups or not held_count:
            raise ValueError(f"named album slot without source SPR support: {ordinal}")
        metrics["old_formula_agrees"] += formula_agrees
        metrics["old_formula_present_but_does_not_select_this_slot"] += formula_was_present and not formula_agrees
        metrics["old_formula_absent_now_mapped"] += not formula_was_present
        metrics["named_slots_with_multiple_spr_groups"] += len(sprite_groups) > 1
        metrics["held_pet_path_named_spr_groups"] += held_count
        projected_bitmap = int(item["cn50_last_projected_physical_rd_bitmapno"])
        variants = [projected_bitmap]
        if alias in PORTRAIT_PREDECESSORS:
            variants.insert(0, PORTRAIT_PREDECESSORS[alias])
        records.append({
            "source_record_id": item["source_record_id"],
            "earlier_tw10_relation": item["early_tw10_relation_OPTIONAL_NOT_ENTRY_GATE"],
            "ordinal": ordinal,
            "compiled_name": item["cn50_original_compiled_name"],
            "exe_row_sha256": item["cn50_original_exe_row_sha256"],
            "formula_100250_plus_ordinal_agrees": formula_agrees,
            "spr_groups": sprite_groups,
            "portrait_alias": alias,
            "portrait_bitmap_numbers_in_file_order": variants,
            "portrait_lookup_after_ordered_load": projected_bitmap,
            "portrait_lookup_rd_sha256": item["cn50_original_rd_sha256"],
        })

    blank_slots = set(routed) - named_ordinals
    return {
        "schema": "stoneage.pet_high_first.cn50_native_spr_to_album.r1",
        "source_grade": "PRESERVED_CN50_PC_UNCERTIFIED_OFFICIAL_PRESSING",
        "source": {
            "cab_sha256_previously_verified": manifest["source"]["cab_sha256"],
            "sa_5000.exe": {
                "bytes": EXPECTED["sa_5000.exe"][0],
                "sha256": EXPECTED["sa_5000.exe"][1],
            },
            **{block["name"]: block for label, block in manifest["source"]["input_containers"].items()
               if label != "real"},
            "source_derived_spr_table_sha256": {name: table_pins[name] for name in SPR_TABLES},
        },
        "original_code_windows": [
            {"meaning": label, "start_va": hex(start), "end_va_exclusive": hex(end), "sha256": sha}
            for label, start, end, sha in WINDOWS
        ],
        "metrics": {
            **metrics,
            "named_album_slots": len(records),
            "all_spr_groups": len(groups),
            "action_object_path_named_spr_groups": len(named_groups),
            "action_object_path_spr_groups_reaching_blank_slots": sum(len(routed[i]) for i in blank_slots),
            "action_object_path_blank_slots_reached": len(blank_slots),
            "action_object_path_spr_groups_outside_album_slots": len(groups) - sum(map(len, routed.values())),
            "held_pet_path_exclusions_in_same_cab": sorted(
                HELD_PET_EXCLUSIONS.intersection(int(row["spr_no"]) for row in groups)
            ),
            "portrait_adrn_original_records_scanned": manifest["metrics"]["adrn"]["records"],
            "portrait_aliases_with_multiple_records": len(PORTRAIT_PREDECESSORS),
            "portrait_alias_adrn_records": sum(len(row["portrait_bitmap_numbers_in_file_order"]) for row in records),
        },
        "evidence_boundaries": {
            "spr_links_are_static_source_paths": True,
            "single_canonical_spr_group_per_name_established": False,
            "original_client_executed": False,
            "portrait_bitmap_observed_in_original_runtime": False,
            "official_retail_pressing_or_live_release_verified": False,
            "same_deployment_pets_stats_skills_and_acquisition_verified": False,
        },
        "records": records,
    }


def original_selection(program, graphic, *, held_pet):
    """Evaluate only register arithmetic and branches from two decoded source spans."""
    regs = {"eax": graphic}
    comparison = 0
    pc = 0x4345CF if held_pet else 0x430DEC
    accept = {0x4346D7, 0x4346DF} if held_pet else {0x430E84, 0x430E88}

    def value(token):
        if token in regs:
            return regs[token]
        unsigned = int(token, 16)
        return unsigned if unsigned < 0x80000000 else unsigned - (1 << 32)

    for _ in range(70):
        if pc in accept:
            return regs["eax"] if 0 <= regs["eax"] < ROWS else None
        if pc == 0x434838:
            return None
        row = program[pc]
        op, operands = row["instruction"].split(None, 1)
        pc += row["encoded_length"]
        if op in {"cmp", "mov", "add", "sub"}:
            dest, src = operands.split(",")
            number = value(src)
            if op == "cmp":
                comparison = regs[dest] - number
            elif op == "mov":
                regs[dest] = number
            else:
                regs[dest] += number if op == "add" else -number
        elif op in {"jmp", "je", "jne", "jg", "jle"}:
            if {"jmp": True, "je": comparison == 0, "jne": comparison != 0,
                "jg": comparison > 0, "jle": comparison <= 0}[op]:
                pc = value(operands)
        elif op == "test" and row["address"] == 0x434632:
            comparison = 1  # Evaluate the held-pet path with its activation bit set.
        else:
            raise ValueError(f"unexpected original selector instruction: {row}")
    raise ValueError("selector did not reach a confirmed exit")


def verify_originals(source_dir, result):
    program_path = source_dir / "sa_5000.exe"
    program = program_path.read_bytes()
    parsed = source_rows(program)
    base, (_, rva, raw_offset, size) = pe32_text_identity(program)
    for label, start, end, sha in WINDOWS:
        offset = raw_offset + start - base - rva
        if not raw_offset <= offset < offset + end - start <= raw_offset + size:
            raise ValueError(f"original window outside PE .text: {label}")
        if digest(program[offset:offset + end - start]) != sha:
            raise ValueError(f"original code window changed: {label}")
    for filename in ("adrn_31.bin", "spradrn_17.bin", "spr_17.bin"):
        file_pin = result["source"][filename]
        raw = (source_dir / filename).read_bytes()
        if (len(raw), digest(raw)) != (file_pin["bytes"], file_pin["sha256"]):
            raise ValueError(f"original source hash changed: {filename}")
    code = {}
    for _, start, end, _ in WINDOWS[:2]:
        output = subprocess.check_output([
            "objdump", "-d", "-M", "intel", "-w", "-j", ".text", f"--start-address={start}",
            f"--stop-address={end}", str(program_path),
        ], text=True, timeout=30)
        code.update((row["address"], row) for row in parse_objdump(output))
    sprite_index = (source_dir / "spradrn_17.bin").read_bytes()
    graphic_numbers = {graphic for graphic, *_ in struct.iter_unpack("<IIHH", sprite_index)}
    for graphic in sorted(graphic_numbers.union(range(99_000, 103_000))):
        for held in (False, True):
            if original_selection(code, graphic, held_pet=held) != album_ordinal(graphic, held_pet=held):
                raise ValueError(f"source branch replay disagrees for graphic {graphic}, held={held}")

    with tempfile.TemporaryDirectory() as directory:
        paths = [Path(directory) / filename for filename in SPR_TABLES]
        export_cn50_spr(source_dir / "spradrn_17.bin", source_dir / "spr_17.bin", *paths)
        for path in paths:
            if digest(path.read_bytes()) != result["source"]["source_derived_spr_table_sha256"][path.name]:
                raise ValueError(f"original SPR resource export changed: {path.name}")

    raw_adrn = (source_dir / "adrn_31.bin").read_bytes()
    aliases = {row["portrait_alias"]: [] for row in result["records"]}
    for bitmap, alias in struct.iter_unpack("<I72xI", raw_adrn):
        if alias in aliases:
            aliases[alias].append(bitmap)
    for row in result["records"]:
        ordinal = row["ordinal"]
        original = parsed[ordinal]
        offset = TABLE_OFFSET + ordinal * STRIDE
        if (original["name"] != row["compiled_name"] or original["raw_u32"] != row["portrait_alias"]
            or digest(program[offset:offset + STRIDE]) != row["exe_row_sha256"]
            or aliases[row["portrait_alias"]] != row["portrait_bitmap_numbers_in_file_order"]):
            raise ValueError(f"original album/portrait evidence disagrees for slot {ordinal}")


def render(result):
    header = {key: value for key, value in result.items() if key != "records"}
    rows = ",\n".join(
        "    " + json.dumps(row, ensure_ascii=False, sort_keys=True) for row in result["records"]
    )
    return json.dumps(header, ensure_ascii=False, indent=2, sort_keys=True).removesuffix("\n}") + (
        ',\n  "records": [\n' + rows + "\n  ]\n}\n"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--original-dir", type=Path, help="Private directory with the four pinned original files")
    parser.add_argument("--write", action="store_true", help="Write the derived report after original source replay")
    args = parser.parse_args()
    if args.write and args.original_dir is None:
        parser.error("--write requires --original-dir")
    result = build_catalog(*read_inputs())
    if args.original_dir is not None:
        verify_originals(args.original_dir, result)
    rendered = render(result)
    if args.write:
        TARGET.write_text(rendered, encoding="utf-8")
    elif TARGET.read_text(encoding="utf-8") != rendered:
        raise SystemExit("Committed CN50 native source catalogue does not replay")
    print(json.dumps(result["metrics"], ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
