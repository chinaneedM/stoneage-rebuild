#!/usr/bin/env python3
"""PET126L: source-pinned, static CN5 name-table to CN5 resource-key crosswalk.

The original 5.0 program is NEVER executed, copied to Git, or treated as an
official-server roster. Integer equality is a locator, not native selector proof.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import struct
from pathlib import Path

from tools.stoneage_pet126k_cn50_original_exe_probe import EXPECTED, parse_row

ROOT = Path(__file__).resolve().parents[1]
RESOURCE_DIR = ROOT / "research/recovered/cn50-resource-metadata"
TABLE_OFFSET, STRIDE, ROWS = 536424, 28, 362
TABLE_SHA = "ba3ad4db233971ee5d9603cdbded6b871f73082445f1ca51d02f0fdf0314d39b"
TABLES = ("SPR-GROUP-R1.tsv.gz", "SPR-FRAME-R1.tsv.gz", "ADRN-R1.tsv.gz")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_gz_rows(path: Path):
    with gzip.open(path, "rt", encoding="utf-8", newline="") as handle:
        yield from csv.DictReader(handle, delimiter="\t")


def qualified_resources():
    manifest = json.loads((RESOURCE_DIR / "MANIFEST-R1.json").read_text(encoding="utf-8"))
    prior = json.loads((ROOT / "research/recovered/STONEAGE-STONEAGE5-REAL-CAB-PAYLOAD-R1.json").read_text(encoding="utf-8"))
    if manifest["status"] != "COMPLETE_VERIFIED_5_0_BITMAP_AND_SPR_RESOURCE_METADATA":
        raise ValueError("unqualified-original-resource-index")
    if not manifest["source"]["source_413_files_rehashed"]:
        raise ValueError("original-source-hash-gate")
    if manifest["source"]["cab_sha256"] != prior["source"]["cab_sha256"]:
        raise ValueError("cross-build-cab-mismatch")
    pinned = {x["name"]: x for x in manifest["tables"]}
    for name in TABLES:
        row = pinned[name]
        data = (RESOURCE_DIR / name).read_bytes()
        if (len(data), digest(data)) != (row["bytes"], row["sha256"]):
            raise ValueError("derived-resource-index-tampered:" + name)
    return manifest


def source_rows(program: bytes):
    if (len(program), digest(program)) != EXPECTED["sa_5000.exe"]:
        raise ValueError("5.0-original-program-identity-mismatch")
    span = program[TABLE_OFFSET: TABLE_OFFSET + STRIDE * ROWS]
    if len(span) != STRIDE * ROWS or digest(span) != TABLE_SHA:
        raise ValueError("362-row-name-span-identity-mismatch")
    result = []
    for i in range(ROWS):
        row = parse_row(program, TABLE_OFFSET + i * STRIDE, "gb18030")
        if row is None:
            raise ValueError("compiled-typed-row-invalid:" + str(i))
        # Use raw numeric terms: PET ID, SPR key and portrait semantics are not proven.
        result.append({"ordinal": i, "name": row["name"],
                       "raw_i32": row["slot"], "raw_u32": row["face"]})
    if (sum(r["raw_i32"] != -1 for r in result), sum(r["raw_i32"] == -1 for r in result)) != (305, 57):
        raise ValueError("source-name-table-topology-differs")
    return result


def exact_pointer_literals(program: bytes, source_offset: int):
    """Count raw PE32 .text immediate literals; NOT control-flow/data-flow evidence."""
    pe = struct.unpack_from("<I", program, 0x3c)[0]
    if program[pe:pe + 4] != b"PE\x00\x00":
        raise ValueError("not-pe")
    section_count = struct.unpack_from("<H", program, pe + 6)[0]
    optional_bytes = struct.unpack_from("<H", program, pe + 20)[0]
    optional = pe + 24
    if struct.unpack_from("<H", program, optional)[0] != 0x10b:
        return {"pe32_supported": False, "table_rva": None, "literal_va_hits": None,
                "literal_rva_hits": None, "proves_selector": False}
    image_base = struct.unpack_from("<I", program, optional + 28)[0]
    entries = []
    for i in range(section_count):
        off = optional + optional_bytes + i * 40
        name = program[off:off + 8].rstrip(b"\x00").decode("ascii", "replace")
        virt_size, rva, size, file_off = struct.unpack_from("<IIII", program, off + 8)
        if file_off + size > len(program):
            raise ValueError("pe-section-outside-program")
        entries.append((name, virt_size, rva, size, file_off))
    matching = [x for x in entries if x[4] <= source_offset < x[4] + x[3]]
    if len(matching) != 1:
        return {"pe32_supported": True, "table_rva": None, "literal_va_hits": 0,
                "literal_rva_hits": 0, "proves_selector": False}
    table_rva = matching[0][2] + source_offset - matching[0][4]
    code = b"".join(program[x[4]:x[4] + x[3]] for x in entries if x[0] == ".text")
    return {"pe32_supported": True, "table_rva": table_rva,
            "literal_va_hits": code.count(struct.pack("<I", image_base + table_rva)),
            "literal_rva_hits": code.count(struct.pack("<I", table_rva)),
            "proves_selector": False}


def crosswalk(rows, groups, frames, bitmapnos):
    """Exact 5.0 integer-key overlaps, preserving all alternative interpretations."""
    present = [row for row in rows if row["raw_i32"] != -1]
    if len(present) != 305:
        raise ValueError("unexpected-name-population")
    matched_group_indices = set()
    counts = {}
    for field in ("raw_i32", "raw_u32"):
        counts[field] = {
            "spr_key_rows": sum(row[field] in groups for row in present),
            "bitmap_key_rows": sum(row[field] in bitmapnos for row in present),
            "distinct_spr_keys": len({row[field] for row in present if row[field] in groups}),
            "distinct_bitmap_keys": len({row[field] for row in present if row[field] in bitmapnos})
        }
        matched_group_indices.update(groups[row[field]]["index"] for row in present if row[field] in groups)
    chosen = [f for f in frames if f["group_index"] in matched_group_indices]
    bmp_refs = {f["bmp_no"] for f in chosen if f["bmp_no"] != 0xffffffff}
    samples = []
    for row in present:
        if len(samples) >= 12:
            break
        samples.append({
            "ordinal": row["ordinal"], "original_compiled_label": row["name"],
            "first_i32": row["raw_i32"], "trailing_u32": row["raw_u32"],
            "i32_exact_spr_key": row["raw_i32"] in groups,
            "u32_exact_spr_key": row["raw_u32"] in groups,
            "i32_exact_adrn_bitmap_key": row["raw_i32"] in bitmapnos,
            "u32_exact_adrn_bitmap_key": row["raw_u32"] in bitmapnos
        })
    return {
        "source_name_rows": len(rows), "populated_name_rows": len(present),
        "placeholder_rows": len(rows) - len(present),
        "numeric_source_key_overlaps": counts,
        "spr_groups_selected_by_either_numeric_field": len(matched_group_indices),
        "selected_spr_frame_occurrences": len(chosen),
        "selected_spr_distinct_frame_bitmap_numbers": len(bmp_refs),
        "selected_spr_frame_bitmaps_present_in_same_cab_adrn": len(bmp_refs & bitmapnos),
        "selected_spr_frame_bitmaps_missing_same_cab_adrn": len(bmp_refs - bitmapnos),
        "sample_only": samples,
        "native_pet_graphic_selector_proven": False,
        "official_live_pet_issuance_proven": False,
        "species_count_inferable": False,
    }


def audit(original_program: Path):
    manifest = qualified_resources()
    blob = original_program.read_bytes()
    rows = source_rows(blob)
    groups = {}
    all_group_indices = set()
    for row in read_gz_rows(RESOURCE_DIR / "SPR-GROUP-R1.tsv.gz"):
        key, index = int(row["spr_no"]), int(row["index"])
        if key in groups or index in all_group_indices:
            raise ValueError("duplicate-original-spr-index")
        groups[key] = {"index": index, "sha256": row["segment_sha256"]}
        all_group_indices.add(index)
    bitmapnos = set()
    for row in read_gz_rows(RESOURCE_DIR / "ADRN-R1.tsv.gz"):
        number = int(row["bitmapno"])
        if number in bitmapnos:
            raise ValueError("duplicate-original-bitmap-key")
        bitmapnos.add(number)
    if len(groups) != manifest["metrics"]["spr"]["groups"] or len(bitmapnos) != manifest["metrics"]["adrn"]["records"]:
        raise ValueError("original-index-count-differs")
    candidate_indices = {groups[r[f]]["index"] for r in rows if r["raw_i32"] != -1
                         for f in ("raw_i32", "raw_u32") if r[f] in groups}
    frames = []
    frame_total = 0
    for row in read_gz_rows(RESOURCE_DIR / "SPR-FRAME-R1.tsv.gz"):
        frame_total += 1
        index = int(row["group_index"])
        if index in candidate_indices:
            frames.append({"group_index": index, "bmp_no": int(row["bmp_no"])})
    if frame_total != manifest["metrics"]["spr"]["frames"]:
        raise ValueError("original-frame-total-differs")
    result = crosswalk(rows, groups, frames, bitmapnos)
    return {
        "schema": "stoneage.pet126l.cn50_original_compiled_names_same_cab_graphics_crosswalk.r1",
        "date": "2026-11-21", "active_module": "PET", "scope": "CLASSIC_ORIGINAL_PC_ONLY",
        "original_program_sha256": EXPECTED["sa_5000.exe"][1],
        "original_table_sha256": TABLE_SHA, "source_cab_sha256": manifest["source"]["cab_sha256"],
        "authenticated_source_type": "THIRD_PARTY_PRESERVED_CN50_PC_CAB_NOT_INDEPENDENTLY_ORIGINAL_PRESSING_CERTIFIED",
        "static_PE_pointer_literals": exact_pointer_literals(blob, TABLE_OFFSET),
        "same_carrier_source_numeric_crosswalk": result,
        "guard": {
            "no_original_program_executed": True,
            "no_proprietary_binary_published": True,
            "no_original_server_pet_master": True,
            "numeric_key_overlap_is_not_control_flow_or_pet_species_ID": True,
            "original_client_graphic_selection_not_yet_proven": True,
            "no_official_live_release_from_compiled_names": True,
            "no_mobile_or_paid_marketplace_sources": True,
        },
        "pet_module_closed": False, "year_2026": "NOT_YEAR_AUDITED",
        "official_new_species_verified": 0, "overall_percent": None,
        "next": "Disassemble and independently verify native compiled-table field-to-sprite selector or matching same-deployment master; preserve inferred numeric overlap as source-key candidate only"
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--program", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.program)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("PET126L_SOURCE_PINNED|name_rows=362|filled=305|official_live_pet_count_not_inferred", flush=True)


if __name__ == "__main__":
    main()
