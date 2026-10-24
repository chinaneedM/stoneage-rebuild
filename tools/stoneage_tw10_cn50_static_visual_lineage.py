#!/usr/bin/env python3
"""Physical lineage bridge for TW1.0 player-labeled static-NPC bitmap band.

Exact bytes have been independently hashed: this report ONLY projects qualified
source rows through the exhaustive TW1.0->CN5 resource comparison. A graphics
resource identifier is not an original NPC identifier or a pet species.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATHS = {
    "tw10_static": "research/recovered/STONEAGE-TW10-NPC-STATIC-RESOURCE-JOIN-R99.json",
    "tw10_cn50_records": "research/recovered/STONEAGE-TW10-CN50-REAL-RECORD-DIFF-R1.json",
    "tw10_cn50_source_custody": "research/recovered/STONEAGE-TW10-CN50-REAL-RESOURCE-CUSTODY-R1.json",
    "tw10_resource_manifest": "research/recovered/tw10-resource-metadata/MANIFEST-R1.txt",
}
SOURCE_BLOBS = {
    "tw10_static": "21d49800a1191f87a006aaa5af4a6f7975f91bf7",
    "tw10_cn50_records": "7eef214be6f6b4f70e96c5c04c5fe31dd36165b3",
}


def git_blob_sha(content: bytes) -> str:
    header = ("blob " + str(len(content)) + "\0").encode("ascii")
    return hashlib.sha1(header + content).hexdigest()


def load_sources(root: Path) -> tuple[dict, dict, dict, str, dict]:
    sources = {name: (root / path).read_bytes()
               for name, path in SOURCE_PATHS.items()}
    for name, sha in SOURCE_BLOBS.items():
        if git_blob_sha(sources[name]) != sha:
            raise ValueError("source-immutable-blob-pin-mismatch:" + name)
    return (
        json.loads(sources["tw10_static"]),
        json.loads(sources["tw10_cn50_records"]),
        json.loads(sources["tw10_cn50_source_custody"]),
        sources["tw10_resource_manifest"].decode("utf-8"),
        {name: {"path": SOURCE_PATHS[name], "git_blob_sha": git_blob_sha(data),
                "sha256": hashlib.sha256(data).hexdigest(),
                "bytes": len(data)}
         for name, data in sorted(sources.items())},
    )


def verify_complete_old_inheritance(diff: dict, custody: dict, manifest: str) -> None:
    if diff.get("result") != "DERIVED_RECORD_LEVEL_DIFF_OF_REACQUIRED_ORIGINAL_RESOURCE_BYTES":
        raise ValueError("no-actual-resource-byte-evidence")
    if custody.get("result") != "ACTUAL_CI_ZIP_JSON_EQUAL_IMMUTABLE_GIT_REPORT":
        raise ValueError("no-independent-source-artifact-custody")
    if custody.get("report_blob_sha") != SOURCE_BLOBS["tw10_cn50_records"]:
        raise ValueError("custody-is-not-of-the-selected-source-report")
    if custody.get("source_run") != 40091960688:
        raise ValueError("unrecognized-source-run")
    if not diff["prerequisites"]["cn50_413_files_rehashed_again"]:
        raise ValueError("cn50-full-cab-not-rehashed")
    if not diff["prerequisites"]["old_tw10_four_files_rehashed_again"]:
        raise ValueError("tw10-four-containers-not-rehashed")
    if diff["evidence_boundaries"]["original_server_npc_quest_growth_master_recovered"] is not False:
        raise ValueError("unjustified-original-server-master-claim")
    family = diff["families"]["bitmap_rd"]
    old = family["old"]
    new = family["new"]
    comp = family["comparison"]
    expected = {
        "old_total_ids": 125996,
        "new_total_ids": 303197,
        "old_duplicate_ids": 0,
        "new_duplicate_ids": 0,
        "ambiguous_shared_id_count": 0,
        "common_unique_id_count": 125996,
        "old_unique_ids_absent_in_new_count": 0,
        "exact_payload_or_segment_count": 125996,
        "changed_payload_or_segment_count": 0,
        "same_index_descriptor_or_frame_count": 125996,
        "same_geometry_or_animation_count": 125996,
        "new_unique_ids_absent_in_old_count": 177201,
    }
    for key, value in expected.items():
        if comp.get(key) != value:
            raise ValueError("incomplete-or-changed-inheritance-matrix:" + key)
    if old["index_count"] != 125996 or new["index_count"] != 303197:
        raise ValueError("bad-native-index-count")
    original_sha = diff["source_claims"]["TW10"]["files"]["adrn"]["sha256"]
    if ("SOURCE|name=adrn_1.bin|bytes=10079680|sha256=" + original_sha) not in manifest:
        raise ValueError("tw10-original-index-not-the-static-bridge-source")
    # The equality assertion spans all original unique IDs. Each separately
    # source-qualified 5846-5946 ID is therefore in the proven intersection,
    # without inventing any CN5 entity name or separate pixel asset.
    if diff["source_claims"]["CN50"]["official_clean_release_mastering_authenticated"] is not False:
        raise ValueError("source-release-provenance-overstated")


def build_bridge(static: dict, diff: dict, custody: dict, manifest: str, pins: dict) -> dict:
    verify_complete_old_inheritance(diff, custody, manifest)
    if static.get("schema") != "stoneage.tw10_original_static_candidate_resource_join.r99":
        raise ValueError("unrecognized-original-static-projection")
    if static["historical_scope"] != "ORIGINAL_TAIWAN_1_0_RETAIL_ADRN_COLLISION_METADATA_ONLY":
        raise ValueError("unqualified-region-or-release")
    measured = static["measured"]
    if (measured["bitmap_rows"] != 101 or measured["sprite_frame_refs_to_this_band"] != 0 or
        measured["original_bitmap_records_total"] != 125996 or
        measured["original_spr_frames_checked"] != 242085):
        raise ValueError("changed-original-static-source-coverage")
    for flag in ("player_bitmap_range_is_official_category",
                 "same_build_npc_identity_available",
                 "original_client_render_execution_observed",
                 "server_spawn_coordinates_available",
                 "map_resource_number_is_npc_entity_id"):
        if static["limits"].get(flag) is not False:
            raise ValueError("historic-category-boundary-promoted:" + flag)
    records = static["rows"]
    if len(records) != 101:
        raise ValueError("not-101-original-source-records")
    record_ids = [r["bitmapno"] for r in records]
    if record_ids != list(range(5846, 5947)):
        raise ValueError("unexpected-source-id-range-or-duplicate")
    links = []
    for r in records:
        bitmap_id = r["bitmapno"]
        map_resource = r["map_number"]
        expected_map_number = bitmap_id - 5846 + 16000 if bitmap_id <= 5919 else bitmap_id - 5920 + 16200
        if map_resource != expected_map_number:
            raise ValueError("static-map-resource-index-not-as-pinned")
        if (r["npc_name"] is not None or r["original_npc_id"] is not None or
            r["world_floor_id"] is not None or r["drawn_npc_role_verified"] is not False):
            raise ValueError("historically-unsupported-npc-attribution")
        if (len(r["rd_block_sha256"]) != 64 or
            any(c not in "0123456789abcdef" for c in r["rd_block_sha256"]) or
            r["encoded_bytes"] < 16 or r["width"] <= 0 or r["height"] <= 0):
            raise ValueError("invalid-physical-rd-evidence")
        links.append({
            "tw10_bitmap_id": bitmap_id,
            "tw10_map_resource_number": map_resource,
            "tw10_rd_sha256": r["rd_block_sha256"],
            "tw10_rd_bytes": r["encoded_bytes"],
            "tw10_dimensions": [r["width"], r["height"]],
            "tw10_draw_offset": [r["xoff"], r["yoff"]],
            "tw10_collision": {
                "atari_x": r["atari_x"], "atari_y": r["atari_y"],
                "hit_flag": r["hit_flag"], "priority_type": r["priority_type"],
                "height_flag": r["height_flag"]
            },
            "cn50_same_bitmap_id": bitmap_id,
            "cn50_rd_identical_to_tw10": True,
            "cn50_full_adrn_descriptor_identical_to_tw10": True,
            "identity_classification": "PLAYER_NPC_BITMAP_BAND_ONLY_UNCONFIRMED",
            "verified_original_npc_id": None,
            "verified_npc_name": None,
            "verified_original_map_floor": None,
            "verified_original_npc_spawn": None,
            "verified_original_npc_script": None,
            "verified_pet_species_id": None,
        })
    return {
        "schema": "stoneage.tw10_cn50.static_visual_candidate_lineage_p2b_r1",
        "status": "101_STATIC_BITMAP_CANDIDATE_PHYSICAL_LINEAGE_PROVED",
        "scope": "SOURCE_DERIVED_CLIENT_GRAPHICS_ONLY",
        "source_pins": pins,
        "source_custody": {
            "source_run": custody["source_run"],
            "source_head": custody["source_head"],
            "source_report_blob": custody["report_blob_sha"],
            "artifact_zip_sha256": custody["artifact_zip_sha256"],
        },
        "metrics": {
            "candidate_bitmap_rows": 101,
            "identical_cn50_rd_blocks": 101,
            "identical_cn50_adrn_descriptors": 101,
            "direct_tw10_spr_frame_references_in_band": 0,
            "cn50_verified_named_npc_entities": 0,
            "tw10_verified_named_npc_entities": 0,
            "nonduplicated_original_bitmap_ids": 101,
        },
        "records": links,
        "limits": {
            "original_player_label_is_canonical_official_npc_type": False,
            "map_number_is_world_map_or_npc_id": False,
            "same_bitmap_is_same_npc_or_pet_instance": False,
            "zero_spr_reference_disproves_other_render_paths": False,
            "all_game_npc_content_is_recovered": False,
            "original_server_data_recovered": False,
            "new_named_entities_verified": False,
            "new_proprietary_pixels_published": False,
            "official_cn50_publisher_pressing_independently_proven": False,
        },
        "reopen_evidence": [
            "same-build original NPC master/spawn table explicitly binding bitmap/resource IDs to named NPCs",
            "original client visual selector callsite with reproducible version-specific binding",
            "authenticated original version screenshot or manual tying a specific character label to a specific resource",
        ],
        "next": "CLIENT-RESOURCE-ENTITY-BRIDGE-P2B_NAMED_SELECTOR_SOURCE",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    report = build_bridge(*load_sources(ROOT))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print("SOURCE_BRIDGE|rows=101|identical_rd=101|named_npcs_verified=0|unqualified_name_promotions=0")


if __name__ == "__main__":
    main()
