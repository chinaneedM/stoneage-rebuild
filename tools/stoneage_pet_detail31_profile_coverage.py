#!/usr/bin/env python3
"""PET31: re-audit original TW1 PC dossier fields, never infer server pets from art.

Read-only, deterministic, offline; a local Git checkout is the evidence source.
Run: python3 -m tools.stoneage_pet_detail31_profile_coverage --full
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


FIELDS = (
    "client_name", "sprite_segment", "source_motion", "original_portrait",
    "official_pet_id", "official_live_release", "level1_stats",
    "initial_stat_ranges", "elements", "growth", "skills", "capture",
    "award", "encyclopedia_text", "historically_complete",
)
ORIGINAL_RETAIL_ARCHIVE = (
    "3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24"
)
ORIGINAL_EXE = (
    "cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a"
)


def present(value):
    """False/zero may be measured values; only null means unknown."""
    return value is not None


def any_nonnull(values):
    return any(present(v) for v in values)


def git_blob_sha(raw):
    return hashlib.sha1(
        ("blob " + str(len(raw)) + "\0").encode("ascii") + raw
    ).hexdigest()


def _expect(condition, msg):
    if not condition:
        raise ValueError(msg)


def audit(root: Path) -> dict:
    root = Path(root)
    registry_path = root / "research/pets/PET-ID-REGISTRY-R1.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    entries = registry["catalog_entries"]
    observations = registry["source_observations"]
    _expect(registry["scope"] == "ORIGINAL_CLASSIC_2D_PC_ONLY", "PC registry scope")
    _expect(len(entries) == len(observations) == 124, "124 original observations")
    observation_by_id = {x["observation_id"]: x for x in observations}
    _expect(len(observation_by_id) == 124, "unique observation IDs")

    stats = Counter({key: 0 for key in FIELDS})
    stats.update({"original_pose_fallback_only": 0})
    records = []
    seen_ids = set()
    for idx, entry in enumerate(entries, 1):
        pet_id = "PET-" + str(idx).zfill(6)
        obs_id = "OBS-TW10-" + str(idx).zfill(4)
        _expect(entry["catalog_pet_id"] == pet_id, "catalog order: " + pet_id)
        _expect(entry["observations"] == [obs_id], "catalog observation: " + pet_id)
        path = entry["machine_dossier_path"]
        _expect(
            path.startswith("research/pets/profiles/TW10-G")
            and ".." not in Path(path).parts
            and path.endswith(".json"), "unsafe dossier path: " + path
        )
        source = root / path
        raw = source.read_bytes()
        dossier = json.loads(raw.decode("utf-8"))
        obs = observation_by_id[obs_id]
        _expect(obs["assigned_catalog_pet_id"] == pet_id, "observed pet ID")
        _expect(obs["source_key"] == entry["legacy_dossier_key"], "source key")
        _expect(obs["source_album_ordinal"] == idx - 1, "album ordinal")
        _expect(dossier["profile_id"] == pet_id, "dossier ID")
        _expect(dossier["profile_stage"] == "PARTIAL_EVIDENCE_PROFILE", "profile stage")
        _expect(dossier["version_scope"]["source_observation_id"] == obs_id, "dossier observation")
        _expect(dossier["version_scope"]["product_line"] == "CLASSIC_ORIGINAL_2D_PC", "profile PC source")
        _expect(dossier["version_scope"]["region"] == "TW", "region TW")
        _expect(dossier["version_scope"]["version"] == "TAIWAN_1_0_ORIGINAL_RETAIL", "TW1 era")
        _expect(dossier["version_scope"]["certified_live_deployment"] is False, "no original server")
        _expect(dossier["internal_id_system"]["assigned_pet_catalog_id"] == pet_id, "permanent ID")
        _expect(dossier["names"]["original_client"] == obs["client_name_literal"], "name source")
        _expect(entry["original_client_name"] == obs["client_name_literal"], "register name")
        _expect(dossier["names"]["local_name_row_sha256"] == obs["source_row_sha256"], "original name SHA")
        _expect(dossier["names"]["status"] == "VERIFIED_CLIENT_LOCAL", "name source grade")

        app = dossier["appearance"]
        motion = app["action_sequences"]
        portrait = app["portrait"]
        _expect(app["graphic_number"] == obs["source_graphic_number"], "graphic source")
        _expect(app["full_original_spr_segment_sha256"] == obs["source_spr_segment_sha256"], "SPR bytes hash")
        _expect(app["status"] == "VERIFIED_CLIENT_LOCAL", "original sprite status")
        _expect(motion["status"] == "VERIFIED_SOURCE_DERIVED", "source motion status")
        _expect(motion["source_group_index"] == app["spr_group_index"], "SPR group")
        _expect(motion["source_sequences"] == 56, "original pose cardinality")
        _expect(motion["source_directions"] == list(range(8)), "original eight directions")
        _expect(motion["source_action_codes"] == [0,1,2,3,4,9,10], "original seven action codes")
        _expect(dossier["provenance"]["source_archive_sha256"] == ORIGINAL_RETAIL_ARCHIVE, "retail source archive")
        _expect(dossier["provenance"]["original_exe_sha256"] == ORIGINAL_EXE, "original exe identity")

        official = dossier["actual_official_pet_identity"]
        combat = dossier["combat_stats"]
        grow = dossier["growth"]
        skill = dossier["skills"]
        obtain = dossier["acquisition"]
        encyclopedia = dossier["encyclopedia"]
        original_face = (
            present(portrait["source_rd_bitmap_number"])
            and present(portrait["source_rd_sha256"])
            and portrait["status"] == "VERIFIED_CLIENT_LOCAL"
        )
        pose_fallback = (
            app.get("source_SPR_pose_reference", {}).get(
                "private_source_image_alternate_available"
            ) is True
        )
        fields = {
            "client_name": True,
            "sprite_segment": bool(app["full_original_spr_segment_sha256"]),
            "source_motion": motion["source_sequences"] > 0,
            "original_portrait": original_face,
            "official_pet_id": present(official["source_pet_id"]),
            "official_live_release": official["official_living_pet_release_proven"] is True,
            "level1_stats": any_nonnull(combat["level_1"]["values"].values()),
            "initial_stat_ranges": (
                any_nonnull(combat["initial_stat_ranges"]["minimum"].values())
                or any_nonnull(combat["initial_stat_ranges"]["maximum"].values())
            ),
            "elements": any_nonnull(combat["elements"].values()),
            "growth": any_nonnull(
                grow[key] for key in (
                    "growth_rate","growth_grade","per_level_growth","level_cap","stat_growth_formula"
                )
            ),
            "skills": any_nonnull(
                skill[key] for key in (
                    "innate_at_acquisition","skill_slots","learnable_skills",
                    "skill_ids_with_same_build_master","effects_and_formula"
                )
            ),
            "capture": any_nonnull(
                [obtain["modes"],obtain["original_capture"]["can_capture"],
                 obtain["original_capture"]["map_id"],obtain["original_capture"]["map_name"],
                 obtain["original_capture"]["coordinates"],
                 obtain["original_capture"]["encounter_level_range"],
                 obtain["original_capture"]["capture_conditions"]]
            ),
            "award": any_nonnull(
                [obtain["starter_pet_award"],obtain["quest_event_reward"],
                 obtain["shop_or_exchange"]]
            ),
            "encyclopedia_text": any_nonnull(
                [encyclopedia["historical_bio"],
                 encyclopedia["original_official_encyclopedia_text"]]
            ),
            "historically_complete": dossier["status"]["all_fields_historically_complete"] is True,
        }
        _expect(
            fields["original_portrait"] or (
                portrait["source_rd_bitmap_number"] is None
                and portrait["source_rd_sha256"] is None
                and portrait["status"] == "OPEN_NOT_PROVEN"
            ), "portrait absent/present contradiction: " + pet_id
        )
        _expect(
            not fields["official_live_release"] or fields["official_pet_id"],
            "new live-release claim needs identified official pet ID: " + pet_id
        )
        _expect(
            not fields["historically_complete"] or (
                fields["official_live_release"] and fields["growth"]
                and fields["skills"] and (fields["capture"] or fields["award"])
            ), "premature full historical certification: " + pet_id
        )
        for key, val in fields.items():
            if val:
                stats[key] += 1
        if not original_face and pose_fallback:
            stats["original_pose_fallback_only"] += 1
        _expect(pet_id not in seen_ids, "duplicate ID")
        seen_ids.add(pet_id)
        records.append({
            "pet_id": pet_id,
            "source_observation": obs_id,
            "client_name_original": obs["client_name_literal"],
            "client_graphic": app["graphic_number"],
            "sprite_group": app["spr_group_index"],
            "original_portrait_rd": portrait["source_rd_bitmap_number"],
            "source_motion_sequences": motion["source_sequences"],
            "original_pose_fallback_when_face_missing": (
                pose_fallback if not original_face else False
            ),
            "field_evidence_present": [k for k, v in fields.items() if v],
            "formal_missing_fields": [
                k for k, v in fields.items() if not v and k not in (
                    "original_portrait", "historically_complete"
                )
            ],
            "dossier_git_blob": git_blob_sha(raw),
            "dossier_path": path,
        })

    _expect(registry["counts"]["assigned_catalog_pet_ids"] == len(records), "registry dossier count")
    _expect(registry["counts"]["source_observation_rows"] == len(records), "registry source count")
    _expect(registry["counts"]["fully_historically_verified_official_pet_species"] ==
            stats["historically_complete"], "registry full-history claim")
    _expect(registry["counts"]["global_original_classic_pc_pet_count"] is None, "unknown global total")
    return {
        "schema": "stoneage.pet_detail31.tw10_full_dossier_fields_audit.r1",
        "scope": "ORIGINAL_CLASSIC_2D_PC_TW10_CLIENT_LOCAL_ONLY",
        "source_registry": "research/pets/PET-ID-REGISTRY-R1.json",
        "source_registry_git_blob": git_blob_sha(registry_path.read_bytes()),
        "source_qualified_pet_dossiers": len(records),
        "field_coverage_counts_NOT_OFFICIAL_SPECIES_TOTALS": dict(sorted(stats.items())),
        "missing_original_portrait_pet_ids": [
            x["pet_id"] for x in records if x["original_portrait_rd"] is None
        ],
        "fully_historical_pet_species_certified": stats["historically_complete"],
        "stage_b": "GATED",
        "overall_project_percent": None,
        "records": records,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    args = parser.parse_args()
    result = audit(Path(args.root))
    if not args.full:
        result = {key: value for key, value in result.items() if key != "records"}
    print("PET31_JSON_START")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    print("PET31_JSON_END")


if __name__ == "__main__":
    main()
