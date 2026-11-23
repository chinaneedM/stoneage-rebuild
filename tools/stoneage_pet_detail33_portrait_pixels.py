"""Replay eight source-matched PC portrait candidates and emit metadata only."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import mmap
from pathlib import Path
import struct
from zipfile import ZipFile

from tools.stoneage_pet_detail32_higher_pc_portrait_probe import (
    CN_DIR, ROOT, select_rows, verified_gzip,
)
from tools.stoneage_private_scene_graphic_join_r1 import (
    ADRN_SHA, ADRN_SIZE, REAL_SHA, REAL_SIZE, authenticate, resolve_ids,
)
from tools.stoneage_private_scene_source_r2 import BUNDLE_SHA, BUNDLE_SIZE
from tools.stoneage_rd_codec import decode_rd_block

PET23 = "research/pets/PET-DETAIL-EVIDENCE23-TW10-124-ORIGINAL-PRIVATE-VISUAL-ATLAS-R1.json"
PET32 = "research/pets/PET-DETAIL-EVIDENCE32-HIGHER-PC-PORTRAIT-ALIAS-R1.json"
RECEIPT = "research/pets/PET-DETAIL-EVIDENCE33-FOUR-PC-PORTRAIT-PIXEL-PAIRS-R1.json"
PORTRAIT_SIZE = (96, 104)
TW10_ADRN_MEMBER = "source/data/adrn_1.bin"
TW10_ADRN_BYTES = 10_079_680


def sha(data):
    return hashlib.sha256(data).hexdigest()


def alias_record_hashes(adrn, aliases):
    records = {alias: [] for alias in aliases}
    for index, (alias,) in enumerate(struct.iter_unpack("<76xI", adrn)):
        if alias in records:
            offset = index * 80
            records[alias].append(sha(adrn[offset:offset + 80]))
    return records


def compare_album_cohort(tw10, cn50, mixed, aliases, targeted_aliases):
    original = alias_record_hashes(tw10, aliases)
    mainland = alias_record_hashes(cn50, aliases)
    preserved = alias_record_hashes(mixed, aliases)
    missing = sorted(alias for alias, rows in original.items() if not rows)
    duplicates = sorted(alias for alias, rows in mainland.items() if len(rows) > 1)
    if (
        missing != sorted(targeted_aliases)
        or duplicates != missing
        or mainland != preserved
        or any(rows != mainland[alias] for alias, rows in original.items() if rows)
    ):
        raise ValueError("album cohort contains an unexpected missing, duplicate or changed record")

    return {
        "logical_aliases": len(aliases),
        "tw10_match_count_by_alias": dict(Counter(map(len, original.values()))),
        "cn50_match_count_by_alias": dict(Counter(map(len, mainland.values()))),
        "mixed25_match_count_by_alias": dict(Counter(map(len, preserved.values()))),
        "tw10_missing_aliases": missing,
        "later_sources_duplicate_aliases": duplicates,
        "tw10_single_records_equal_in_both_later_sources": len(aliases) - len(missing),
        "cn50_and_mixed25_same_ordered_full_adrn_records_for_all_aliases": True,
    }


def observed_variant(real, mixed, tw85, cn50):
    from tools.stoneage_scene07_independent_pixels import independent_rd

    patch = tw85["original_2005_official_patch"]
    bitmap = mixed["bitmapno"]
    if (
        not tw85["same_saved_tw85_native_RD_exact_original_record"]
        or [mixed["index"]] != tw85["saved_tw85_native_indexes"]
        or mixed["source_record_sha256"] != patch["record_sha256"]
        or (bitmap, mixed["map_number"]) != (int(patch["bitmapno"]), int(patch["map_number"]))
    ):
        raise ValueError(f"mixed25 ADRN does not match the exact patch record for {bitmap}")

    offset, size = mixed["offset"], mixed["size"]
    block = real[offset:offset + size]
    digest = sha(block)
    if (
        len(block) != size
        or digest != tw85["saved_tw85_native_RD_sha256_if_source_exact"]
        or digest != cn50["rd_block_sha256"]
        or (offset, size) != (int(cn50["adder"]), int(cn50["size"]))
    ):
        raise ValueError(f"mixed25 RD does not match both preserved samples for {bitmap}")

    header, indices = decode_rd_block(block)
    width, height = PORTRAIT_SIZE
    if (
        (mixed["width"], mixed["height"]) != PORTRAIT_SIZE
        or (header["width_s"], header["height_s"], header["stored_size"]) != (width, height, size)
        or independent_rd(block) != (width, height, indices)
    ):
        raise ValueError(f"portrait dimensions or independent decode differ for {bitmap}")

    return {
        "mixed25_adrn_index": mixed["index"],
        "mixed25_adrn_record_sha256": mixed["source_record_sha256"],
        "physical_bitmap_number": bitmap,
        "real_byte_offset": offset,
        "rd_bytes": size,
        "rd_sha256": digest,
        "rd_flag": header["flag"],
        "indexed_pixels_sha256": sha(indices),
        "indexed_pixel_count": len(indices),
        "palette_index_minimum": min(indices),
        "palette_index_maximum": max(indices),
        "palette_index_zero_count": indices.count(0),
        "matches_wayi_patch_80_byte_record_and_preserved_tw85_rd": True,
        "matches_preserved_cn50_physical_rd": True,
    }, indices


def audit(source, cn50_adrn, tw10_archive, root=ROOT):
    pins = {
        "stoneage-preserved-mixed25-original.rar": (BUNDLE_SIZE, BUNDLE_SHA),
        "adrn_15.bin": (ADRN_SIZE, ADRN_SHA),
        "real_15.bin": (REAL_SIZE, REAL_SHA),
    }
    for filename, (size, digest) in pins.items():
        authenticate(source / filename, size, digest)

    evidence = (root / PET32).read_bytes()
    baseline = json.loads(evidence)
    atlas = (root / PET23).read_bytes()
    atlas_source = json.loads(atlas)
    tw10_pin = atlas_source["source_archive"]
    authenticate(tw10_archive, tw10_pin["bytes"], tw10_pin["sha256"])
    with ZipFile(tw10_archive) as archive:
        if archive.namelist().count(TW10_ADRN_MEMBER) != 1:
            raise ValueError("TW10 original ADRN archive member is ambiguous")
        tw10_bytes = archive.read(TW10_ADRN_MEMBER)
    tw10_adrn_sha = tw10_pin["original_adrn_sha256"]
    if len(tw10_bytes) != TW10_ADRN_BYTES or sha(tw10_bytes) != tw10_adrn_sha:
        raise ValueError("TW10 original ADRN member size/SHA conflict")

    manifest = json.loads((root / CN_DIR / "MANIFEST-R1.json").read_bytes())
    table = next(row for row in manifest["tables"] if row["name"] == "ADRN-R1.tsv.gz")
    metadata = verified_gzip(root, f"{CN_DIR}/ADRN-R1.tsv.gz", table)
    cn50_pin = manifest["source"]["input_containers"]["adrn"]
    authenticate(cn50_adrn, cn50_pin["bytes"], cn50_pin["sha256"])

    aliases = {row["album_logical_alias_original_both_versions"] for row in baseline["records"]}
    atlas_aliases = {row["original_portrait_logical_alias"] for row in atlas_source["profiles"]}
    if len(atlas_aliases) != 124 or len(aliases) != 4 or not aliases <= atlas_aliases:
        raise ValueError("portrait alias scope changed")
    mixed_bytes = (source / "adrn_15.bin").read_bytes()
    cn50_bytes = cn50_adrn.read_bytes()
    cohort = compare_album_cohort(tw10_bytes, cn50_bytes, mixed_bytes, atlas_aliases, aliases)
    mixed_by_alias = resolve_ids(mixed_bytes, aliases, REAL_SIZE)
    cn50_real = manifest["source"]["input_containers"]["real"]
    cn50_by_alias = resolve_ids(cn50_bytes, aliases, cn50_real["bytes"])
    if cn50_by_alias != mixed_by_alias:
        raise ValueError("CN50 and mixed25 full ADRN matches differ")
    wanted = sorted({row["bitmapno"] for rows in mixed_by_alias.values() for row in rows})
    if len(wanted) != 8:
        raise ValueError("expected eight distinct RD blocks")
    cn50_rows = select_rows(metadata, "bitmapno", wanted)
    records = []
    with (source / "real_15.bin").open("rb") as f, mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as real:
        for row in baseline["records"]:
            alias = row["album_logical_alias_original_both_versions"]
            candidates = row["tw85_saved_8_5_native_exact_RD_from_official_patch"]
            mixed_rows = mixed_by_alias[alias]
            if len(mixed_rows) != len(candidates) or len(mixed_rows) != 2:
                raise ValueError(f"unexpected ADRN alias multiplicity for {alias}")

            variants, pixels = [], []
            collision_row, = row["cn50_saved_5_0_ADRN_plus76_alias_candidate_rows"]
            projected_bitmap = int(collision_row["source_RD"]["bitmapno"])
            if projected_bitmap != cn50_by_alias[alias][-1]["bitmapno"]:
                raise ValueError(f"CN50 last-row projection changed for {alias}")
            for candidate, mixed in zip(candidates, mixed_rows, strict=True):
                cn50, = cn50_rows[mixed["bitmapno"]]
                variant, indices = observed_variant(real, mixed, candidate, cn50)
                variants.append(variant)
                pixels.append(indices)
            first, second = pixels
            records.append({
                "pet_id": row["pet_id"],
                "tw10_graphic": row["tw10_original_graphic"],
                "tw10_compiled_name": row["tw10_original_name"],
                "logical_portrait_alias": alias,
                "variants": variants,
                "cn50_collision_projection_last_bitmap": projected_bitmap,
                "differing_index_positions": sum(a != b for a, b in zip(first, second, strict=True)),
                "tw10_original_portrait_recovered": False,
            })

    return {
        "schema": "stoneage.pet_detail33.cross_version_portrait_pixel_replay.r1",
        "source_grade": "MIXED25_PRESERVED_PC_SOURCE_EXACT_BLOCKS_NOT_OFFICIAL_DEPLOYMENT",
        "sources": {
            **{name: {"bytes": size, "sha256": digest} for name, (size, digest) in pins.items()},
            "verified_tw10_retail_zip": {"bytes": tw10_pin["bytes"], "sha256": tw10_pin["sha256"]},
            TW10_ADRN_MEMBER: {"bytes": len(tw10_bytes), "sha256": tw10_adrn_sha},
            "adrn_31.bin": cn50_pin,
            PET23: {"bytes": len(atlas), "sha256": sha(atlas)},
            PET32: {"bytes": len(evidence), "sha256": sha(evidence)},
            f"{CN_DIR}/ADRN-R1.tsv.gz": {"bytes": table["bytes"], "sha256": table["sha256"]},
        },
        "album_cohort": cohort,
        "records": records,
        "verified_pixel_blocks": sum(len(row["variants"]) for row in records),
        "full_cn50_adrn_scan_matches_mixed25_and_wayi_patch_80_byte_records": True,
        "cn50_collision_tsv_records_only_last_alias_occurrence": True,
        "identical_independent_decoders": True,
        "tw10_native_portraits_newly_verified": 0,
        "original_game_or_native_portrait_selection_observed": False,
        "cn50_or_tw85_full_real_reread": False,
        "official_pet_identity_or_release_newly_verified": False,
        "proprietary_pixels_published_in_git": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="private directory of the pinned archive and mixed25 members")
    parser.add_argument("cn50_adrn", type=Path, help="private original adrn_31.bin from the preserved CN50 disc")
    parser.add_argument("tw10_archive", type=Path, help="private pinned TW10 retail source ZIP")
    args = parser.parse_args()
    report = audit(args.source, args.cn50_adrn, args.tw10_archive)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
