"""Certify original Taiwan v1.0 SPR→animation→frame→ADRN links.

This analyzes already-committed deterministic TSV metadata, not original
proprietary imagery and NOT original pet-species identity or growth values.
"""
from __future__ import annotations
import argparse
import collections
import csv
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
META = ROOT / "research/recovered/tw10-resource-metadata"
SOURCE_GZIP_SHA256 = {
    "ADRN-R1.tsv.gz": "c8669789de1cc6e3575c2412ed86354a49c2b3e90cd2854c1e7b2fc71b0fe9ea",
    "SPR-GROUP-R1.tsv.gz": "4db7809de4197eb90cca6dc04bda8550025e022c8232e2ebb902db0e9faf0175",
    "SPR-ANIMATION-R1.tsv.gz": "25f8039e6c6ca47d94289b269d5ff74a67fde999c6b6d4dbb08af297ddcaa567",
    "SPR-FRAME-R1.tsv.gz": "2bbfb2db4a866445085d98934fd475cbd72e034fe1155b2e17ae802ffdc5fe80",
}
SELECTED_GROUP_INDICES = (0, 1, 2, 3, 4, 5, 102, 373, 463)
ROOT_MANIFEST_BLOB = "6154dcf806163b82cb96af344e6a644143d15f56"
LATER_ENEMY_PROBE_BLOB = "c1ea9f239b7377e630b2fc09d0c470d44fc6f786"
LATER_GROWTH_PROBE_BLOB = "5c528fb382ad13484572bd49905480a6b5775e18"
LATER_NAME_ENCODING_BLOB = "34fc56b2d614d6ba1a31f04c58a3a217326fdfe1"
LATER_GRAPHIC_MAPPING_BLOB = "9ff1133a5bb62d4b3e07e2d6e955c54c0e30dd33"

def sha256file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def gitblob(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()

def require(flag, message):
    if not flag: raise ValueError(message)

def tsv(path):
    with gzip.open(path, "rt", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            yield row

def validate_fixed_evidence():
    manifest = (META / "MANIFEST-R1.txt").read_bytes()
    require(gitblob(manifest) == ROOT_MANIFEST_BLOB, "TW10 manifest SHA changed")
    text = manifest.decode("utf-8")
    for name, sha in SOURCE_GZIP_SHA256.items():
        require("DATASET|name=" + name + "|" in text and "sha256=" + sha in text, "manifest missing dataset " + name)
        require(sha256file(META / name) == sha, "gzip provenance changed " + name)
    historical = {
        "research/recovered/STONEAGE-25-ENEMYBASE-PROBE-R1.txt": LATER_ENEMY_PROBE_BLOB,
        "research/recovered/STONEAGE-25-PET-GROWTH-R1.txt": LATER_GROWTH_PROBE_BLOB,
        "research/recovered/STONEAGE-25-ENEMYBASE-NAME-ENCODING-R1.txt": LATER_NAME_ENCODING_BLOB,
        "research/recovered/STONEAGE-25-RUNTIME-GRAPHIC-MAPPING-R1.txt": LATER_GRAPHIC_MAPPING_BLOB
    }
    for name, sha in historical.items():
        require(gitblob((ROOT / name).read_bytes()) == sha, "fixed previous research changed: " + name)

def inspect_repository_metadata():
    validate_fixed_evidence()
    bitmapids = set()
    adrn_records = 0
    for row in tsv(META/"ADRN-R1.tsv.gz"):
        adrn_records += 1
        image_id = int(row["bitmapno"])
        require(image_id not in bitmapids, "duplicate original ADRN bitmap no")
        bitmapids.add(image_id)
    require(adrn_records == len(bitmapids) == 125996, "original ADRN census changed")

    groups = {}
    for row in tsv(META/"SPR-GROUP-R1.tsv.gz"):
        idx = int(row["index"])
        require(idx not in groups, "duplicate original SPR group index")
        require(int(row["offset"]) < int(row["end_offset"]) == int(row["next_offset"]), "incomplete original SPR group")
        groups[idx] = {"spr_no": int(row["spr_no"]), "anim_count": int(row["anim_count"]),
                       "segment_sha256": row["segment_sha256"], "offset": int(row["offset"])}
    require(len(groups) == 464 and set(groups) == set(range(464)), "original SPR group census changed")
    require(len(set(v["spr_no"] for v in groups.values())) == 464, "ambiguous original SPR group IDs")
    sample = {idx: {"group_index": idx, "spr_no": groups[idx]["spr_no"],
                     "animation_records": groups[idx]["anim_count"],
                     "frame_records": 0, "sentinel_frames": 0,
                     "adrn_bitmap_references": 0, "missing_bitmap_references": 0,
                     "example_bitmap_nos": [], "example_direction_anim_codes": [],
                     "species_identity": None, "original_growth_config": None,
                     "original_encounter_map": None, "original_pet_graphic_id": None,
                     "status": "TW10_ASSET_IDENTITY_AND_FRAME_JOIN_ONLY_NOT_PET_IDENTITY"}
              for idx in SELECTED_GROUP_INDICES}
    animations = {}
    group_animation_counts = collections.Counter()
    total_anim = 0
    total_frame_expected = 0
    for row in tsv(META/"SPR-ANIMATION-R1.tsv.gz"):
        idx = int(row["group_index"]); n = int(row["anim_index"]); sn = int(row["spr_no"])
        require(idx in groups and sn == groups[idx]["spr_no"], "animation group mismatch")
        key = (idx,n)
        require(key not in animations, "duplicate group animation")
        duration = int(row["duration"]); frame_count = int(row["frame_count"])
        require(frame_count >= 0 and duration >= 0, "bad original animation")
        animations[key] = frame_count
        group_animation_counts[idx] += 1
        total_anim += 1
        total_frame_expected += frame_count
        if idx in sample and len(sample[idx]["example_direction_anim_codes"]) < 4:
            sample[idx]["example_direction_anim_codes"].append(
                [int(row["direction"]), int(row["anim_no"]), frame_count])
    require(total_anim == 39065, "original animation count changed")
    require(set(animations) == {(idx,n) for idx,g in groups.items() for n in range(g["anim_count"])}, "animation joins not complete")
    require(all(group_animation_counts[idx] == g["anim_count"] for idx,g in groups.items()), "group animation counts")
    require(total_frame_expected == 242085, "original animation frame census changed")

    frame_positions = {}
    total = sentinel = linked = missing = 0
    for row in tsv(META/"SPR-FRAME-R1.tsv.gz"):
        idx = int(row["group_index"]); n = int(row["anim_index"])
        sn = int(row["spr_no"]); frame = int(row["frame_index"])
        bitmap = int(row["bmp_no"]); is_sentinel = int(row["sentinel"])
        require(idx in groups and sn == groups[idx]["spr_no"], "frame SPR group mismatch")
        require((idx,n) in animations, "frame animation not found")
        key = (idx,n)
        require(frame == frame_positions.get(key,0), "frame sequence damaged")
        require(frame < animations[key], "frame exceeds animation")
        frame_positions[key] = frame+1
        require(is_sentinel in (0,1), "bad sentinel marker")
        if idx in sample: sample[idx]["frame_records"] += 1
        total += 1
        if is_sentinel:
            require(bitmap == 4294967295, "sentinel ID is not 0xFFFFFFFF")
            sentinel += 1
            if idx in sample: sample[idx]["sentinel_frames"] += 1
        elif bitmap in bitmapids:
            linked += 1
            if idx in sample:
                sample[idx]["adrn_bitmap_references"] += 1
                if bitmap not in sample[idx]["example_bitmap_nos"] and len(sample[idx]["example_bitmap_nos"]) < 5:
                    sample[idx]["example_bitmap_nos"].append(bitmap)
        else:
            missing += 1
            if idx in sample: sample[idx]["missing_bitmap_references"] += 1
    require(total == total_frame_expected == 242085, "frame-count mismatch")
    require(sentinel == 3492, "original sentinel count differs")
    require(all(frame_positions.get(key,0) == count for key,count in animations.items()), "unfilled animation frame")
    require(linked + sentinel + missing == total, "frame classification invariant")
    report = {
        "schema": "stoneage.tw10.asset_frame_join.r1",
        "source_profile": "TW10_DIRECT_RESOURCE_METADATA",
        "source_manifest_sha": ROOT_MANIFEST_BLOB,
        "record_counts": {"adrn_bitmap_records": adrn_records, "spr_groups": len(groups),
                          "animations": total_anim, "frames": total,
                          "sentinel_frames": sentinel, "frames_joined_to_original_adrn": linked,
                          "frames_without_adrn_or_sentinel": missing},
        "sample_groups": [sample[idx] for idx in SELECTED_GROUP_INDICES],
        "source_scope": "Original retail graphics and animation indexes only; no species roster, pet-name, pet-stat or growth attestation",
        "later_enemybase_status": {"source_profile": "RECOVERED25_LATER_NOT_TW10",
             "active_rows": 988, "other_rows": 640, "source_name_hashes_distinct": 662,
             "render_graphic_runtime_map": "ABSENT", "pet_species_count_original": None},
        "historical_pet_identity_verified_count": 0,
        "new_historical_species_names": [],
        "version_promotion": False,
    }
    return report

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--emit-samples", action="store_true")
    a=parser.parse_args()
    r=inspect_repository_metadata()
    if a.emit_samples: print("CERTIFIED_RESOURCE_SAMPLE_JSON="+json.dumps(r,ensure_ascii=False,sort_keys=True,separators=(",",":")))
    else: print(json.dumps({**r,"sample_groups":r["sample_groups"][:2]},ensure_ascii=False,sort_keys=True))
if __name__ == "__main__":main()
