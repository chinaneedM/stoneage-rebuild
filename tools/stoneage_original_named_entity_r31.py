"""Bounded, fully offline R31 source provenance gate; never reads original commercial bytes."""
from __future__ import annotations

from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT = "research/recovered/STONEAGE-ORIGINAL-SAME-BUILD-NAMED-ENTITY-R31.json"
INPUTS = [
    "research/recovered/STONEAGE-WAYI85-MSI-CLIENT-PAYLOAD-R1.json",
    "research/recovered/tw85-rd-private-r30/PLAN-R30.json",
    "research/recovered/tw85-rd-private-r30/SOURCE-R30.json",
    "research/recovered/STONEAGE-PET-IDENTITY-SAME-BUILD-TRIAGE-R1.json",
    "research/recovered/tw10-resource-metadata/MANIFEST-R1.txt",
]
# This is intentionally a filename *hint*, not a semantic file-content classifier.
EXPLICIT_MASTER_LEAF = re.compile(r"(pet|npc|species|enemybase|petbase|quest|script|master)", re.I)


def original_git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def evaluate(msi: dict, plan: dict, observed: dict, pet: dict, tw1_manifest: str) -> dict:
    if msi.get("official_clean_client_authenticated") is not False:
        raise ValueError("TW85 original clean-client certification cannot be promoted")
    if msi["inspection"].get("original_server_quest_pet_master_data_proven") is not False:
        raise ValueError("original server master provenance not evidenced")
    inv = msi["inspection"]["inventory"]["samples"][0]
    files = inv["files"]
    if inv.get("file_count") != len(files) or len(files) != 557:
        raise ValueError("557-file original inventory incomplete")
    paths = [row["path"] for row in files]
    if len(set(paths)) != len(paths):
        raise ValueError("original inventory duplicate paths")
    for row in files:
        if not re.fullmatch(r"[0-9a-f]{64}", row["sha256"]):
            raise ValueError("invalid original file SHA256")
    leaves = [s.rsplit("/", 1)[-1] for s in paths]
    explicit = sorted(x for x in leaves if EXPLICIT_MASTER_LEAF.search(x))
    if explicit:
        raise ValueError("a newly visible explicit master filename requires investigation")
    hist = dict(sorted(Counter(x.rsplit(".", 1)[-1].lower() for x in leaves).items()))
    expected_hist = {"ani": 24, "bin": 9, "bmp": 5, "dat": 52, "exe": 6,
                     "ico": 1, "sab": 220, "sap": 16, "txt": 4, "wav": 220}
    if hist != expected_hist:
        raise ValueError("historical inventory extension composition changed")

    a, b = plan["sample"], observed["sample"]
    identifying = ["original_spr_no", "source_group_index", "original_animation_index",
                   "original_direction_numeric", "original_action_numeric",
                   "original_duration_word", "source_group_full_spr_segment_sha256"]
    if any(a.get(k) != b.get(k) for k in identifying):
        raise ValueError("original sampled SPR identity mismatch")
    frames = a["sample_frames"]
    observed_frames = observed["frames"]
    if len(frames) != a["original_animation_frame_count"] or len(frames) != 8:
        raise ValueError("R30 original eight frames not preserved")
    expected_numbers = list(range(303039, 303047))
    if [row["bitmapno"] for row in frames] != expected_numbers:
        raise ValueError("R30 original bitmap sequence changed")
    for i, (f, v) in enumerate(zip(frames, observed_frames)):
        if (f["bitmapno"] != v["bitmapno"] or
                f["rd_block_sha256"] != v["source_RD_sha256"] or
                f["native_adrn_record_sha256"] != v["source_record_sha256"] or
                f["width"] != v["width"] or f["height"] != v["height"]):
            raise ValueError(f"original frame/REAL source mismatch at {i}")
    if len(observed_frames) != len(frames):
        raise ValueError("R30 source has extra original frames")
    if observed.get("named_pet_or_avatar_verified") is not False:
        raise ValueError("cannot infer the named species from a grey silhouette")
    if plan["limits"]["true_sprite_identity_proven"] is not False:
        raise ValueError("R30 identity original research gate violated")
    if pet.get("disposition") != "OPEN_EVIDENCE_LIMITED_SAME_BUILD_PET_IDENTITY_NOT_OBTAINED":
        raise ValueError("past same-build named pet master gap has changed")
    ids = pet["identity_fields"]
    if ids.get("original_pet_master_id") is not None or ids.get("original_spr_no_for_any_named_pet") is not None:
        raise ValueError("same-build original named pet source may have appeared")

    metrics = {}
    for line in tw1_manifest.splitlines():
        fields = line.split("|")
        if len(fields) == 3 and fields[0] == "METRIC":
            metrics[fields[1]] = fields[2]
    if metrics.get("adrn_records") != "125996" or metrics.get("spr_groups") != "464":
        raise ValueError("TW10 original sample manifest changed")
    return {
        "inventory": {
            "declared_files": len(files), "unique_paths": len(set(paths)),
            "unique_sha256": len(set(row["sha256"] for row in files)),
            "extension_counts": hist, "explicit_named_master_leaf_hits": explicit,
        },
        "sample": {
            "spr_no": a["original_spr_no"], "group_index": a["source_group_index"],
            "frame_bitmapnos": [f["bitmapno"] for f in frames],
            "matched_original_RD_sha256_count": len(frames),
            "matched_original_ADRN_record_sha256_count": len(frames),
            "named_original_entity_id": None,
        },
        "tw10_scope": {
            "original_adrn_records": int(metrics["adrn_records"]),
            "all_sample_bitmap_numbers_outside_tw10_id_range":
                all(f["bitmapno"] >= int(metrics["adrn_records"]) for f in frames),
        },
        "evidence": {
            "tw85_clean_official_build_proven": False,
            "original_server_quest_pet_master_data_proven": False,
            "same_build_pet_identity_proven": False,
        },
        "status": "OPEN_EVIDENCE_LIMITED_FIVE_PINNED_INPUTS",
        "next": "ORIGINAL_WORLD_MAP_CONTENT_MATERIAL_32",
    }


def verify():
    report = json.loads((ROOT / REPORT).read_text(encoding="utf-8"))
    observed = []
    for p in INPUTS:
        data = (ROOT / p).read_bytes()
        sha = original_git_blob_sha(data)
        if report["source_git_blobs"].get(p) != sha:
            raise ValueError("upstream original evidence Git blob changed: " + p)
        observed.append(json.loads(data) if p.endswith(".json") else data.decode("utf-8"))
    if set(report["source_git_blobs"]) != set(INPUTS):
        raise ValueError("source pin inventory changed")
    computed = evaluate(*observed)
    if computed != report["result"]:
        raise ValueError("R31 published result differs from original evidence replay")
    if not report["limits"] or report["remote_base_head"] == "":
        raise ValueError("missing source boundaries")
    return computed


if __name__ == "__main__":
    print(json.dumps(verify(), ensure_ascii=False, sort_keys=True, indent=2))
