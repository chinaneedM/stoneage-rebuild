#!/usr/bin/env python3
"""PET32: cross-version PC-only portrait lookup by the *ADRN+76 map_number*.

The TW1 retail album has four unresolved logical aliases 28085..28088.
Do not confuse physical ADRN bitmapno with a logical portrait alias. Existing
CN50 / TW85 source-derived metadata are source-qualified but their PC builds
are *not* authenticated official contemporaneous pressings. This is a read-only
candidate search; never publishes proprietary RD payload or claims TW1 portrait.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALIAS_TO_PET = ((28085, "PET-000116", 100389),
                (28086, "PET-000117", 100390),
                (28087, "PET-000118", 100391),
                (28088, "PET-000119", 100392))
CN_DIR = "research/recovered/cn50-resource-metadata"
TW85_DIR = "research/recovered/adrn129-tw85-real-pair"
CN_CATALOG = "research/recovered/STONEAGE-PET126R-CN50-PC-ORIGINAL-ALBUM-FULL-362-SLOT-SOURCE-CATALOGUE-R1.json"
TW_CROSS = "research/recovered/STONEAGE-PET126W-TW10-CN50-ALL-124-ORIGINAL-PC-NAME-VARIANTS-R1.json"


def verified_gzip(root, rel, info):
    path = root / rel
    st = path.stat()
    if st.st_size != int(info["bytes"]):
        raise ValueError("original-derived table size drift: " + rel)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != info["sha256"]:
        raise ValueError("original-derived table SHA drift: " + rel)
    return path


def select_rows(path, key, values):
    wanted = set(values)
    hits = {i: [] for i in values}
    with gzip.open(path, "rt", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        if key not in (reader.fieldnames or []):
            raise ValueError("missing field: " + key)
        for row in reader:
            n = int(row[key])
            if n in wanted:
                hits[n].append(row)
    return hits


def brief_rd(row):
    if row is None:
        return None
    return {key: row.get(key) for key in (
        "index", "bitmapno", "width", "height", "xoff", "yoff",
        "size", "rd_flag", "rd_block_sha256", "rd_sha256",
        "rd_status", "record_sha256", "map_number"
    ) if key in row}


def audit(root=ROOT):
    root = Path(root)
    manifest = json.loads((root / CN_DIR / "MANIFEST-R1.json").read_text(encoding="utf-8"))
    tw85 = json.loads((root / TW85_DIR / "REPORT-R1.json").read_text(encoding="utf-8"))
    cat = json.loads((root / CN_CATALOG).read_text(encoding="utf-8"))
    cross = json.loads((root / TW_CROSS).read_text(encoding="utf-8"))
    assert manifest["status"] == "COMPLETE_VERIFIED_5_0_BITMAP_AND_SPR_RESOURCE_METADATA"
    assert manifest["source"]["official_clean_pressing_verified"] is False
    assert tw85["boundaries"]["official_clean_tw85_pressing_authenticated"] is False
    assert cat["metrics"]["named_TW10_pairs_with_exact_CN50_source_sprite_hash"] == 124

    md = {x["name"]: x for x in manifest["tables"]}
    cn_collision_path = verified_gzip(root, f"{CN_DIR}/COLLISION-ATTR-R1.tsv.gz", md["COLLISION-ATTR-R1.tsv.gz"])
    cn_adrn_path = verified_gzip(root, f"{CN_DIR}/ADRN-R1.tsv.gz", md["ADRN-R1.tsv.gz"])
    tw85_path = verified_gzip(root, f"{TW85_DIR}/NATIVE-R1.tsv.gz", tw85["tables"]["NATIVE-R1.tsv.gz"])
    # Native TW8.5 index preserves original 28-byte header/whole-record hash
    # but NOT parsed +76 alias. WAEI's archived official patch carries all
    # 80-byte fields. Only exact patch-record -> saved native-record matches
    # allow a sourced 8.5 native RD claim.
    patch_meta = json.loads((root / "research/recovered/wayi-adrn129-patch-metadata/REPORT-R1.json").read_text(encoding="utf-8"))
    patch_info = patch_meta["indexes"][0]["derived_pin"]
    patch_path = verified_gzip(root, "research/recovered/wayi-adrn129-patch-metadata/INDEX-1-R1.tsv.gz", patch_info)
    pairs_path = verified_gzip(root, f"{TW85_DIR}/PAIRS-R1.tsv.gz", tw85["tables"]["PAIRS-R1.tsv.gz"])

    aliases = [p[0] for p in ALIAS_TO_PET]
    cn_alias = select_rows(cn_collision_path, "map_number", aliases)
    cn_by_physical = select_rows(cn_adrn_path, "bitmapno", aliases)
    # If map_number maps to physical 7xxx, resolve via native full source
    chosen = [int(r["bitmapno"]) for arr in cn_alias.values() for r in arr]
    cn_mapped_rd = select_rows(cn_adrn_path, "bitmapno", chosen) if chosen else {}
    patch_alias = select_rows(patch_path, "map_number", aliases)
    patch_indices = [int(row["index"]) for rows in patch_alias.values() for row in rows]
    pair_by_patch = select_rows(pairs_path, "patch_index", patch_indices) if patch_indices else {}
    tw85_alias = {alias: [] for alias in aliases}
    for alias in aliases:
        for patch_row in patch_alias[alias]:
            pair = pair_by_patch.get(int(patch_row["index"]), [])
            if len(pair) != 1:
                raise ValueError("patch-native RD pairing must preserve record multiplicity exactly")
            pair = pair[0]
            if pair["patch_record_sha256"] != patch_row["record_sha256"]:
                raise ValueError("official patch original 80-byte record changed across source tables")
            exact = pair["qualification"] == "EXACT_NATIVE_RECORD_AND_RD_STRUCTURE"
            tw85_alias[alias].append({
                "original_2005_official_patch": brief_rd(patch_row),
                "same_saved_tw85_native_RD_exact_original_record": exact,
                "saved_tw85_native_indexes": [
                    int(i) for i in pair["native_exact_indices"].split(",") if i
                ],
                "saved_tw85_native_RD_sha256_if_source_exact": pair["rd_sha256"] if exact else None,
                "original_pairing_grade": pair["qualification"],
            })
    tw85_by_physical = select_rows(tw85_path, "bitmapno", aliases)
    tw10_rows = {int(r["ordinal_graphic_hypothesis"]): r for r in cross["records"]}
    cn_rows = {int(r["TW10_ordinal_based_graphic_hypothesis"]): r for r in cat["records"]
               if r.get("TW10_ordinal_based_graphic_hypothesis") is not None}
    entries = []
    for alias, petid, graphic in ALIAS_TO_PET:
        orig = tw10_rows[graphic]
        cnrow = cn_rows[graphic]
        if not (orig["shared_full_original_spr_segment_sha256"]
                == cnrow["same_CAB_SPR_group_hash_for_hypothesis"]):
            raise ValueError("the 4 source graphics differ in later preserved CN50")
        if not (cnrow["source_raw_trailing_u32"] == alias
                and cnrow["TW10_retail_exact_same_SPR_segment_at_this_ordinal"]):
            raise ValueError("source album alias/link mismatch")
        refs = cn_alias[alias]
        raw_matches = []
        for ref in refs:
            candidates = cn_mapped_rd.get(int(ref["bitmapno"]), [])
            if len(candidates) != 1:
                raise ValueError("CN50 mapped RD reference not unique")
            raw_matches.append({
                "logical_alias_map_number": alias,
                "source_collision_metadata": {
                    "adrn_index": int(ref["adrn_index"]),
                    "bitmapno": int(ref["bitmapno"])
                },
                "source_RD": brief_rd(candidates[0])
            })
        entries.append({
            "pet_id": petid,
            "tw10_original_graphic": graphic,
            "tw10_original_name": orig["tw10_original_literal"],
            "cn50_saved_compiled_name": cnrow["label_as_compiled_GB18030"],
            "album_logical_alias_original_both_versions": alias,
            "tw10_original_portrait_alias_missing_in_tw10_ADRN_plus76": True,
            "tw10_cn50_full_SPR_segment_SHA256_exact": orig["shared_full_original_spr_segment_sha256"],
            "cn50_saved_5_0_ADRN_plus76_alias_candidate_rows": raw_matches,
            "cn50_saved_5_0_ADRN_physical_bitmapno_same_integer_NOT_alias": [
                brief_rd(x) for x in cn_by_physical[alias]
            ],
            "tw85_official_2005_patch_plus76_alias_candidates": tw85_alias[alias],
            "tw85_saved_8_5_native_exact_RD_from_official_patch": [
                x for x in tw85_alias[alias]
                if x["same_saved_tw85_native_RD_exact_original_record"]
            ],
            "tw85_saved_8_5_ADRN_physical_bitmapno_same_integer_NOT_alias": [
                brief_rd(x) for x in tw85_by_physical[alias]
            ],
            "cross_version_portrait_source_candidate_found": bool(
                raw_matches or any(x["same_saved_tw85_native_RD_exact_original_record"]
                                   for x in tw85_alias[alias])
            ),
            "source_pixel_actually_decoded_this_audit": False,
            "tw10_original_album_face_recovered_this_audit": False,
            "official_original_pet_issuance_certified": False
        })
    return {
        "schema": "stoneage.pet_detail32.classic_pc_higher_version_face_alias_research.r1",
        "method": "exact source SHA verified client metadata: original 28-byte +24 face alias -> same saved version ADRN +76 map_number -> native RD record, not physical bitmapno equality",
        "source_scope": ["AUTHENTICATED_TW10_RETAIL_ORIGINAL_ASSET_MISSING_FOUR_FACES",
                         "CN50_THIRD_PARTY_PRESERVED_SAVED_PC_5_0_UNVERIFIED_PRESSING",
                         "TW85_THIRD_PARTY_PRESERVED_SAVED_PC_8_5_UNVERIFIED_PRESSING"],
        "sources": {
            "CN50_ADRN_SHA256": md["ADRN-R1.tsv.gz"]["sha256"],
            "CN50_COLLISION_SHA256": md["COLLISION-ATTR-R1.tsv.gz"]["sha256"],
            "TW85_NATIVE_SHA256": tw85["tables"]["NATIVE-R1.tsv.gz"]["sha256"],
            "TW85_OFFICIAL_2005_PATCH_ADRN_INDEX_SHA256": patch_info["sha256"],
            "TW85_NATIVE_PATCH_EXACT_RD_PAIRS_SHA256": tw85["tables"]["PAIRS-R1.tsv.gz"]["sha256"],
            "CN50_album_362_slots_source": CN_CATALOG,
            "TW10_CN50_cross_version_names": TW_CROSS
        },
        "records": entries,
        "stats": {
            "tw10_original_missing_album_portraits": 4,
            "cn50_adRN_aliases_with_at_least_one_candidate": sum(bool(x["cn50_saved_5_0_ADRN_plus76_alias_candidate_rows"]) for x in entries),
            "tw85_official_patch_aliases_present": sum(bool(x["tw85_official_2005_patch_plus76_alias_candidates"]) for x in entries),
            "tw85_saved_client_source_exact_native_RD_matches": sum(bool(x["tw85_saved_8_5_native_exact_RD_from_official_patch"]) for x in entries),
            "cross_version_face_candidates_found": sum(x["cross_version_portrait_source_candidate_found"] for x in entries),
            "original_TW10_album_faces_newly_authenticated": 0
        },
        "boundaries": {
            "same_number_at_physical_ADRN_bitmapno_NOT_a_portrait_alias": True,
            "historical_official_live_species_certified": 0,
            "raw_original_pixels_copied_to_public_git": False,
            "tw10_portrait_map_number_misses_unaltered": True,
            "no_higher_version_official_same_deployment_inferred": True,
            "overall_completion_percent": None
        }
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=ROOT)
    args = p.parse_args()
    print("PET32_JSON_START")
    print(json.dumps(audit(args.root), ensure_ascii=False, sort_keys=True))
    print("PET32_JSON_END")


if __name__ == "__main__":
    main()
