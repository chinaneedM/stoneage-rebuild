#!/usr/bin/env python3
"""PET23: one-worker, source-pinned bounded retry for 12 PET22-unread JP web images.

Public output is original archive metadata and image SHA only; NO original GIF
bytes, client species identity, permission claims, or static image reproduction.
"""
import argparse
import json
from pathlib import Path

import stoneage_pet21_official_web_image_reaccess as p21
import stoneage_pet22_jp_official_124_archive_batch as p22

ROOT = Path(__file__).resolve().parents[1]
PET22_RECEIPT = ROOT / "research/recovered/STONEAGE-PET-MODULE-22-JP-124-ARCHIVED-IMAGE-RECOVERY-R1.json"
PINNED_PET22_GIT_BLOB = "b891006d611109fe38e91d3fe2447955b57b9f4e"
# Four deliberately spaced, previously unread website positions per page.
# All originated in the dated official operator HTML, not generated URLs.
RETRY_ORDINALS = (11, 22, 33, 43, 49, 60, 71, 84, 103, 110, 114, 124)


def source_ready_targets(catalog, original_pet22):
    """Return only previously unobserved exact source URLs; fail closed on drift."""
    if original_pet22["workflow_run_id"] != 43694793122:
        raise ValueError("PET22 source run receipt changed")
    if original_pet22["frozen_existing_pet_catalogue_git_blob"] != p21.PINNED_CATALOG_GIT_BLOB:
        raise ValueError("PET16 source pin changed")
    if original_pet22["count_summary"]["cumulative_distinct_web_positions_with_verified_archived_image_SHA"] != 28:
        raise ValueError("PET21+22 historical success total changed")
    by_number = {r["web_ordinal"]: r for r in original_pet22["records"]}
    if len(by_number) != 124 or set(by_number) != set(range(1, 125)):
        raise ValueError("PET22 original 124-position receipt incomplete or duplicated")
    all_targets = {r["web_ordinal"]: r for group in p22.all_jp_targets(catalog).values() for r in group}
    selected = []
    for ordinal in RETRY_ORDINALS:
        old = by_number[ordinal]
        target = all_targets[ordinal]
        if (old["best_archival_observation_sha256_or_null"] is not None or
                old["PET22_probe"]["kind"] == "ARCHIVED_IMAGE_BYTES_SHA256_OBSERVED"):
            raise ValueError("refuse to consume an already verified image as a new retry")
        if (old["original_image_url"] != target["original_image_url"] or
                old["original_operator_web_record_id"] != target["record_id"] or
                old["parent_page_capture"] != target["page_archive_capture"] or
                old["parent_page_sha256"] != target["page_body_sha256"]):
            raise ValueError("original operator source identity changed")
        if target["actual_client_species_id"] is not None or target["public_use_permission_verified"]:
            raise ValueError("website entry incorrectly promoted to game species or publication")
        selected.append(target)
    if len(selected) != 12 or len({x["web_ordinal"] for x in selected}) != 12:
        raise ValueError("PET23 target selection must stay finite and unique")
    return selected


def load_pinned_inputs():
    cat_raw = p21.CATALOG.read_bytes()
    if p21.git_blob(cat_raw) != p21.PINNED_CATALOG_GIT_BLOB:
        raise ValueError("PET16 catalogue original blob drift")
    prior_raw = PET22_RECEIPT.read_bytes()
    if p21.git_blob(prior_raw) != PINNED_PET22_GIT_BLOB:
        raise ValueError("PET22 observation receipt original blob drift")
    return json.loads(cat_raw), json.loads(prior_raw)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--verify-only", action="store_true")
    mode.add_argument("--probe", action="store_true")
    parser.add_argument("--timeout", type=int, default=10)
    args = parser.parse_args()
    if not 1 <= args.timeout <= 12:
        parser.error("bounded per-request timeout must be 1..12 seconds")
    catalog, receipt = load_pinned_inputs()
    selected = source_ready_targets(catalog, receipt)
    report = {
        "schema": "stoneage.pet23_single_worker_original_jp_operator_archive_retry.r1",
        "prior_pet22_original_git_blob": PINNED_PET22_GIT_BLOB,
        "prior_pet22_run_id": 43694793122,
        "prior_distinct_original_image_SHA_positions": 28,
        "previously_not_observed_jp_positions": 96,
        "retry_source_ordinals": list(RETRY_ORDINALS),
        "source_urls_verbatim_from_existing_catalogue": True,
        "runtime_workers": 1,
        "original_GIF_bytes_written_to_public_repository_or_artifacts": False,
        "private_original_image_custody_verified": False,
        "client_species_ID_or_art_license_verified": False,
        "old_success_receipts_unchanged": True,
    }
    if args.verify_only:
        report["status"] = "OFFLINE_SOURCE_TARGETS_VERIFIED_NO_NETWORK"
    else:
        probe = p21.run_probe(selected, workers=1, timeout=args.timeout)
        report["status"] = "LIVE_ARCHIVE_ATTEMPTS_RECORDED_NOT_GAME_EXECUTION"
        report["result_counts"] = probe["result_counts"]
        report["records"] = probe["records"]
        report["new_source_bytes_sha_positions_this_run"] = sum(
            r["image_result"]["kind"] == "ARCHIVED_IMAGE_BYTES_SHA256_OBSERVED"
            for r in probe["records"]
        )
        report["historical_28_sha_are_preserved_even_if_this_retry_fails"] = True
    print("PET23_RESULT_JSON_BEGIN")
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    print("PET23_RESULT_JSON_END")


if __name__ == "__main__":
    main()
