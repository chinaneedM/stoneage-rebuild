#!/usr/bin/env python3
"""PET22: all 124 *already archived* JP operator web image references, 3 bounded groups.

No guessed URL, no original media persistently written, no gameplay identity claim.
Only output original-archive image SHA/capture and source-blocker evidence.
"""
import argparse
import json
import re
from pathlib import Path

import stoneage_pet21_official_web_image_reaccess as p21

ROOT = Path(__file__).resolve().parents[1]
PET21_RECEIPT = ROOT / "research/recovered/STONEAGE-PET-MODULE-21-OFFICIAL-WEB-ARCHIVED-IMAGE-REACCESS-R1.json"

GROUPS = {
    1: tuple(range(1, 46)),
    2: tuple(range(46, 91)),
    3: tuple(range(91, 125)),
}
SOURCE_HISTORICAL_IMAGE_HOST = "images.hangame.co.jp"
OLD_REFERENCE_IMAGE_SHA = "593345c3edf78ebcaa2dff0c27a2d10a92b4eefcc4aef4db14aee2efdc5e013f"


def all_jp_targets(catalog):
    rows = catalog["datasets"]["jp_official_web"]
    if len(rows) != 124 or len({r["web_ordinal"] for r in rows}) != 124:
        raise ValueError("expect exactly 124 unique original historic operator web positions")
    expected_page_names = {
        1: "chara2.asp", 2: "chara2-2.asp", 3: "chara2-3.asp",
    }
    out = {}
    for group, ordinals in GROUPS.items():
        part = []
        for i, ordinal in enumerate(ordinals, 1):
            r = next((x for x in rows if x["web_ordinal"] == ordinal), None)
            if r is None:
                raise ValueError("historic JP official web ordinal missing")
            url = p21.verify_reference(r["image_reference_url"], "jp_official_web")
            if not url.endswith(f"/petpicgroup{group}-{i}.gif"):
                raise ValueError("source referenced URL / original ordinal mismatch")
            ref = r["source_refs"][0]
            if (not ref["url"].endswith(expected_page_names[group]) or
                    not re.fullmatch(r"\d{14}", ref["capture"]) or
                    not re.fullmatch(r"[a-f0-9]{64}", ref["sha256"])):
                raise ValueError("original dated Hangame HTML page source provenance mismatch")
            if (r["actual_client_species_id"] is not None or
                    r["rights_status"] != "RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED"):
                raise ValueError("source mistaken for client species ID or public use right")
            part.append({
                "source_namespace": "jp_official_web",
                "web_ordinal": ordinal,
                "record_id": r["id"],
                "name_as_written": r["name_as_written"],
                "original_image_url": url,
                "original_page_url": ref["url"],
                "page_archive_capture": ref["capture"],
                "page_body_sha256": ref["sha256"],
                "previously_verified_image_sha256": r["image_actual_sha256"],
                "original_page_era_not_exact_client_build": True,
                "actual_client_species_id": None,
                "public_use_permission_verified": False,
            })
        out[group] = part
    if sum(map(len, out.values())) != 124:
        raise ValueError("not all 124 original JP web image URLs are accounted for")
    return out


def comparison_to_pet21(report, pet21):
    old_by_position = {
        x["web_ordinal"]: x for x in pet21["records"]
        if x["source_namespace"] == "jp_official_web"
        and x["probe_status"] == "ARCHIVED_IMAGE_BYTES_SHA256_OBSERVED"
    }
    compare = []
    for r in report["records"]:
        earlier = old_by_position.get(r["web_ordinal"])
        if not earlier:
            continue
        new = r["image_result"]
        if new["kind"] != "ARCHIVED_IMAGE_BYTES_SHA256_OBSERVED":
            state = "EARLIER_PET21_SHA_EXISTS_BUT_THIS_REPLAY_FAILED"
        elif new["sha256"] == earlier["returned_original_media_image_sha256_or_null"]:
            state = "SAME_IMAGE_SHA_ACROSS_INDEPENDENT_GITHUB_ACTIONS"
        else:
            state = "DIFFERENT_ARCHIVE_CAPTURE_OR_IMAGE_BYTES_MUST_NOT_OVERWRITE_HISTORY"
        compare.append({
            "web_ordinal": r["web_ordinal"],
            "pet21_previous_image_sha256": earlier["returned_original_media_image_sha256_or_null"],
            "pet22_retrieved_image_sha256_or_null":
                new.get("sha256") if new["kind"] == "ARCHIVED_IMAGE_BYTES_SHA256_OBSERVED" else None,
            "comparison": state,
        })
    return compare


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--verify-only", action="store_true")
    p.add_argument("--probe", action="store_true")
    p.add_argument("--group", type=int, choices=(1, 2, 3))
    p.add_argument("--timeout", type=int, default=6)
    p.add_argument("--workers", type=int, default=3)
    args = p.parse_args()
    if args.verify_only == args.probe:
        p.error("select exactly one of --verify-only or --probe")
    if args.probe and args.group is None:
        p.error("--group 1|2|3 required with --probe")
    if args.timeout < 1 or args.timeout > 20 or args.workers < 1 or args.workers > 4:
        p.error("bounded timeout 1..20 and workers 1..4 required")
    raw = p21.CATALOG.read_bytes()
    if p21.git_blob(raw) != p21.PINNED_CATALOG_GIT_BLOB:
        p.error("PET16 original catalogue git blob changed")
    catalog = json.loads(raw)
    groups = all_jp_targets(catalog)
    with PET21_RECEIPT.open(encoding="utf-8") as f:
        prior = json.load(f)
    if prior["probe_workflow_run_id"] != 43693853890:
        p.error("PET21 original observed run was replaced")
    if args.verify_only:
        output = {
            "schema": "stoneage.pet22_all_existing_124_jp_operator_source_reference_validation.r1",
            "status": "OFFLINE_ALL_124_OPERATOR_REFERENCED_URLS_VALIDATED",
            "group_counts": {str(k): len(v) for k, v in groups.items()},
            "source_catalogue_sha": p21.PINNED_CATALOG_GIT_BLOB,
            "previous_pet21_probe_run": prior["probe_workflow_run_id"],
            "no_media_downloaded_or_original_early_game_id_proven": True,
        }
    else:
        output = p21.run_probe(groups[args.group], workers=args.workers, timeout=args.timeout)
        output["schema"] = "stoneage.pet22_archived_jp_web_image_group_source_bytes_observations.r1"
        output["source_group_number"] = args.group
        output["group_page_origin_url"] = groups[args.group][0]["original_page_url"]
        output["pet21_prior_image_comparison"] = comparison_to_pet21(output, prior)
        output["original_website_full_124_positions_verified_offline"] = True
        output["all_124_original_image_bytes_acquired"] = False
        output["gif_bytes_stored_or_published"] = False
        output["no_sprite_or_pet_identity_promotion"] = True
        output["no_archive_bytes_does_not_prove_permanent_loss"] = True
    print("PET22_RESULT_JSON_BEGIN")
    print(json.dumps(output, ensure_ascii=False, sort_keys=True))
    print("PET22_RESULT_JSON_END")


if __name__ == "__main__":
    main()
