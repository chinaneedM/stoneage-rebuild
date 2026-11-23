#!/usr/bin/env python3
"""Replay high-version-first CN50 original PC named source atlas, not pet roster.

The old Taiwan 1.0 relationship is OPTIONAL, never the candidate entry gate.
SPR group numbers are unverified 100250+ordinal formula hypotheses; RD is the
same-CAB last-record ADRN alias projection, not the full native selector.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PINS = {
  "research/pets/PET-DETAIL-EVIDENCE36-CN50-ALBUM-ADRN-RD-PROJECTION-R1.json": "8e06ddfcf1a080c7591c0a8300811b0b770cd425",
  "research/pets/PET-DETAIL-EVIDENCE37-TW10-CN50-ORIGINAL-RD-OVERLAP-R1.json": "6872532e344f08633d37222bff8df108398b034e",
  "research/recovered/STONEAGE-PET126R-CN50-PC-ORIGINAL-ALBUM-FULL-362-SLOT-SOURCE-CATALOGUE-R1.json": "8b1058a43c267dfeaa298d4c2c472209cebd24d9",
  "research/pets/PET-DETAIL-EVIDENCE35-CN2002-2003-NAME-TO-CN50-ALBUM-BRIDGE-R1.json": "deb54b65593014d7b019b93ecf0cefb280bf004e"
}
COLUMNS = [
  "source_record_id",
  "cn50_album_ordinal",
  "cn50_original_compiled_name",
  "cn50_original_exe_row_sha256",
  "cn50_local_portrait_alias_u32",
  "cn50_last_projected_physical_rd_bitmapno",
  "cn50_original_rd_sha256",
  "cn50_source_rd_dimensions",
  "cn50_formula_spr_graphic_number_UNVERIFIED",
  "cn50_formula_spr_source_group_present",
  "cn50_formula_spr_segment_sha256_UNVERIFIED",
  "cn50_formula_spr_sha_duplicate_group_size",
  "early_tw10_relation_OPTIONAL_NOT_ENTRY_GATE",
  "earlier_tw10_name_if_evidenced",
  "period_name_attestation_year_NOT_FIRST_RELEASE",
  "period_name_attestation_grade",
  "native_name_to_spr_identity",
  "same_build_original_server_pet_id",
  "official_live_release",
  "birth_growth_skill_capture",
  "source_grade"
]
GRADES = {
    "TW10_ORIGINAL_RD_SHA256_EXACT_CN50": "EARLY_TW10_PORTRAIT_FULL_RD_SHA_EXACT",
    "TW10_NATIVE_PORTRAIT_ABSENT_TWO_LATER_VARIANTS": "EARLY_TW10_NAMED_SPR_PORTRAIT_ABSENT",
    "CN50_NAMED_LOCAL_ONLY_NO_TW10_BRIDGE": "EARLY_TW10_NOT_LINKED",
}
TARGET = ROOT / "research/pets/PET-HIGH-FIRST-CN50-305-SOURCE-ASSET-CATALOG-R1.tsv"


def git_blob(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def build(root: Path = ROOT):
    data = {}
    for path, sha in PINS.items():
        raw = (root / path).read_bytes()
        if git_blob(raw) != sha:
            raise ValueError("Pinned source modified: " + path)
        data[path] = json.loads(raw)
    album, comparison, native, chronology = (data[k] for k in PINS)
    by_early = {r["cn50_album_ordinal"]: r for r in comparison["records"]}
    by_native = {r["ordinal"]: r for r in native["records"]}
    by_period = {r["local_album_ordinal"]: r for r in chronology["records"]}
    if len(album["records"]) != 305 or len(comparison["records"]) != 305:
        raise AssertionError("Expected 305 original named rows")
    if len(native["records"]) != 362 or len(chronology["records"]) != 7:
        raise AssertionError("Native album slot count or historical name crosswalk changed")

    spr_sha_counts = {}
    for a in album["records"]:
        z = by_native[a["album_ordinal"]]
        if z["same_CAB_SPR_group_for_hypothesis_present"]:
            h = z["same_CAB_SPR_group_hash_for_hypothesis"]
            if not h:
                raise AssertionError("Present formula SPR has no source digest")
            spr_sha_counts[h] = spr_sha_counts.get(h, 0) + 1

    records, stats = [], {}
    for a in album["records"]:
        ordinal = a["album_ordinal"]
        d, z = by_early[ordinal], by_native[ordinal]
        p = by_period.get(ordinal)
        if not (
            a["source_exe_row_sha256"] == d["cn50_original_exe_row_sha256"] == z["source_exe_row_sha256"]
            and a["source_compiled_alias_u32"] == d["cn50_compiled_portrait_alias_u32"] == z["source_raw_trailing_u32"]
            and a["client_compiled_name"] == d["cn50_compiled_name"] == z["label_as_compiled_GB18030"]
            and a["same_CAB_rd_block_sha256"] == d["cn50_last_projected_rd_sha256"]
            and a["last_projected_physical_rd_bitmapno"] == d["cn50_last_projected_rd_bitmapno"]
        ):
            raise AssertionError("Source names, native fields or SHA disagreement: " + str(ordinal))
        if p and (p["name"] != a["client_compiled_name"]
                  or p["original_exe_row_sha256"] != a["source_exe_row_sha256"]):
            raise AssertionError("Historical name not the exact original source row")
        present = z["same_CAB_SPR_group_for_hypothesis_present"]
        h = z["same_CAB_SPR_group_hash_for_hypothesis"] if present else ""
        grade = GRADES[d["comparison_grade"]]
        vals = [
            "OBS-CN50-SLOT-" + str(ordinal).zfill(4),
            ordinal,
            a["client_compiled_name"],
            a["source_exe_row_sha256"],
            a["source_compiled_alias_u32"],
            a["last_projected_physical_rd_bitmapno"],
            a["same_CAB_rd_block_sha256"],
            str(a["same_CAB_rd_width"]) + "x" + str(a["same_CAB_rd_height"]),
            z["TW10_ordinal_based_graphic_hypothesis"]
                if z["TW10_ordinal_based_graphic_hypothesis"] is not None else "",
            "YES" if present else "NO",
            h,
            spr_sha_counts[h] if h else "",
            grade,
            d["tw10_original_name"] or "",
            p["year"] if p else "",
            p["grade"] if p else "",
            "NOT_VERIFIED",
            "NOT_VERIFIED",
            "NOT_VERIFIED",
            "NOT_VERIFIED",
            "PRESERVED_CN50_PC_UNCERTIFIED_OFFICIAL_PRESSING",
        ]
        vals = [str(v) for v in vals]
        if len(vals) != len(COLUMNS) or any(
            "\t" in cell or "\r" in cell or "\n" in cell for cell in vals
        ):
            raise AssertionError("Invalid source cell or schema")
        records.append(vals)
        stats[grade] = stats.get(grade, 0) + 1
        k = "has_formula_spr" if present else "no_formula_spr"
        stats[k] = stats.get(k, 0) + 1
        if grade == "EARLY_TW10_NOT_LINKED":
            k = "unlinked_has_spr" if present else "unlinked_no_spr"
            stats[k] = stats.get(k, 0) + 1
        if p:
            stats["period"] = stats.get("period", 0) + 1
        if h and spr_sha_counts[h] > 1:
            stats["duplicate_spr_hash_rows"] = stats.get("duplicate_spr_hash_rows", 0) + 1
    assert (
        stats["EARLY_TW10_PORTRAIT_FULL_RD_SHA_EXACT"],
        stats["EARLY_TW10_NAMED_SPR_PORTRAIT_ABSENT"],
        stats["EARLY_TW10_NOT_LINKED"],
        stats["has_formula_spr"],
        stats["no_formula_spr"],
        stats["unlinked_has_spr"],
        stats["unlinked_no_spr"],
        stats["period"],
        stats["duplicate_spr_hash_rows"],
    ) == (120, 4, 181, 190, 115, 66, 115, 7, 5)
    return records, stats


def render(rows):
    return "\n".join(["\t".join(COLUMNS)] + ["\t".join(r) for r in rows]) + "\n"


if __name__ == "__main__":
    rows, stats = build()
    if render(rows) != TARGET.read_text(encoding="utf-8"):
        raise SystemExit("High-first source atlas does not replay from pinned original data")
    print(json.dumps(stats, ensure_ascii=False, sort_keys=True))
