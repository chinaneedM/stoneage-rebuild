"""Classify one pinned first-party web description, never a game implementation.

The source body remains transient. Digests, labels, paraphrased relationships
and explicit unknowns are the permanent research deliverable.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from tools.stoneage_wayi_intro_detail02_probe import Visible

ORIGINAL = "http://www.wayi.com.tw/stoneage/game/game01_03.asp"
REQUESTED = "https://web.archive.org/web/20050614002509id_/" + ORIGINAL
FINAL = "https://web.archive.org/web/20050614005817id_/" + ORIGINAL
SHA256 = "f021c32b042dbbea480f67aeb3fbc50ba9dfab919de6c04b3240400e5b41c684"
BYTES = 26642
CAPTURE = "20050614005817"
REPORT = "research/recovered/STONEAGE-WAYI-MARINE-SOCIAL-CRAFTING-R1.json"
ANCHORS = ("新增海底融合系統", "名片數量增加", "合成精工強化", "公關新聞")
SECTION_PINS = (
    (90, "7cfcb4a24e48160691a57c151cb5ad109ec4fdcfb91857350354a00558f679f3"),
    (207, "f586ad9da5c266056d8f5c34dabd5a32d4ada774a2445a2e685a0d1944bd17bc"),
    (171, "5ed812458f1817b93d131032f3660ec329ab2dd317a798254bfbdee50e8c61b5"),
)


def require(value, message):
    if not value:
        raise ValueError(message)


def normalize(value):
    return "".join(value.split())


def section_fingerprints(pieces):
    """Exclude the account form/poll before content and corporate footer after it."""
    positions = []
    for anchor in ANCHORS:
        found = [i for i, s in enumerate(pieces) if normalize(s) == anchor]
        require(len(found) == 1, "Missing or duplicate content anchor: " + anchor)
        positions.append(found[0])
    require(positions == sorted(positions), "Content anchors reordered")
    fingerprints = []
    for start, end in zip(positions, positions[1:]):
        s = normalize("".join(pieces[start:end]))
        fingerprints.append((len(s), hashlib.sha256(s.encode()).hexdigest()))
    require(tuple(fingerprints) == SECTION_PINS, "Content changed; new source review required")
    return [{"normalized_characters": n, "sha256": sha} for n, sha in fingerprints]


def build(raw, final_url):
    require(final_url == FINAL, "Not the exact qualified official archive capture")
    require(len(raw) == BYTES and hashlib.sha256(raw).hexdigest() == SHA256,
            "Original source body identity mismatch")
    text = raw.decode("big5", errors="strict")
    require(bool(re.search(r"<html|<body", text, re.I)), "Non-HTML response")
    visible = Visible()
    visible.feed(text)
    require(visible.title == ["石器時代--精靈的召喚"], "Unexpected source title")
    fingerprints = section_fingerprints(visible.pieces)
    return {
        "schema": "stoneage.wayi.marine_social_crafting.source_contract.r1",
        "task": "ALL_OFFICIAL_VERSIONS_NEW_NAMED_FIRSTPARTY_DOMAIN-01",
        "source": {
            "operator": "WAYI_TAIWAN", "original_url": ORIGINAL,
            "requested_url": REQUESTED, "final_url": final_url,
            "actual_capture": CAPTURE, "bytes": BYTES, "sha256": SHA256,
            "encoding": "BIG5_STRICT", "source_kind": "FIRST_PARTY_WEBSITE_DESCRIPTION",
            "parent_report": "research/recovered/STONEAGE-WAYI-OFFICIAL-WORLDLINE-R1.json",
            "parent_json_pointer": "/world/detail_links/2",
            "parent_capture": "20050614002509",
            "parent_sha256": "c0a2f96c1d0232eb3f94328481ff512c3efed63daeab912fcc5dd0c397f1ba0d",
            "page_title_is_client_build": False,
            "capture_is_publication_or_deployment_date": False,
            "section_fingerprints": fingerprints,
        },
        "marine_fusion": {
            "evidence": "OPERATOR_PLANNED_CONTENT_AND_RETROSPECTIVE_ASSERTION",
            "operator_prior_marine_pet_version_label": "6.0",
            "operator_new_fusion_version_label": "8.0",
            "planned_class_count": 5, "planned_pet_count": 20,
            "named_classes_in_source_order": ["水母", "一角鯨", "海蠍", "滄龍"],
            "named_class_count": 4, "unlisted_class_count": 1,
            "missing_class_name": None, "named_classes_are_complete_species_roster": False,
            "four_pets_per_class_proven": False,
            "fusion_recipe_or_inputs": None, "pet_ids_or_graphic_bindings": None,
            "stat_growth_or_eligibility_formula": None,
            "actual_release_or_server_execution_proven": False,
        },
        "business_cards": {
            "evidence": "OPERATOR_DESCRIBED_SOCIAL_STATE_NOT_RUNTIME_TRACE",
            "ordinary_capacity_before_described": 40,
            "ordinary_capacity_after_described": 79,
            "additional_dedicated_slot_described": 1,
            "dedicated_roles_as_written": ["勇者", "使者"],
            "display_context": "MISSION_ACCEPTANCE_AND_LAST_CARD_PAGE",
            "end_of_summoning_task": "DEDICATED_CARDS_DESCRIBED_AS_RETAINED",
            "next_role_assignment": "DEDICATED_CARDS_DESCRIBED_AS_AUTOMATICALLY_OVERWRITTEN",
            "ordinary_reexchange_advice": True,
            "reexchange_is_automatic_copy_proven": False,
            "two_roles_imply_two_extra_slots": False,
            "protocol_capacity_or_save_layout": None,
            "logout_persistence_or_server_transaction": None,
        },
        "crafting": {
            "evidence": "OPERATOR_DESCRIBED_FUNCTIONS_NOT_RECIPES_OR_FORMULAS",
            "functions_in_source_order": [
                {"label": "強化系統", "assertion": "PET_ENHANCEMENT_SKILL_UPGRADES_FORMER_TOP_TIER_CRAFTED_EQUIPMENT"},
                {"label": "鑿孔系統", "assertion": "INCREASES_GEM_SOCKET_CAPACITY_OF_NEW_CRAFTED_ITEMS"},
                {"label": "新合成裝備", "assertion": "MATERIAL_SYNTHESIS_DESCRIBED_AS_STRONGER_THAN_SYNTHESIZED_ARMOR_20"},
                {"label": "鑑定系統", "assertion": "PAGE_ATTRIBUTES_HIGH_GRADE_MATERIAL_AND_SYNTHESIS_SUCCESS_IMPROVEMENT"},
                {"label": "精鍊系統", "assertion": "PRODUCES_NEW_HIGH_GRADE_MATERIALS_FOR_EQUIPMENT_SYNTHESIS"},
            ],
            "armor_20_is_item_id_or_numeric_stat": False,
            "identification_label_normalized_to_other_version_rule": False,
            "recipes_item_ids_success_rates_socket_limits_or_costs": None,
            "npc_or_learnable_skill_ids": None,
        },
        "boundaries": {
            "website_poll_is_gameplay_rule": False,
            "images_or_animation_acquired": False,
            "client_build_authenticated": False,
            "original_server_state_recovered": False,
            "jss1999_or_tw10_rule_promoted": False,
            "same_name_cross_region_identity_assumed": False,
            "source_html_or_assets_in_git": False,
            "stage_a_historical_families": "7_PARTIAL_2_OPEN_UNCHANGED",
            "stage_b_and_wiki_production": "GATED", "r79": "PAUSED_NON_BLOCKING",
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="Transient local source for initial qualification")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    if args.input:
        raw, final = Path(args.input).read_bytes(), FINAL
    else:
        for attempt in range(2):
            try:
                with urlopen(Request(REQUESTED, headers={"User-Agent": "Mozilla/5.0 StoneAgeHistoricalEvidence"}), timeout=40) as r:
                    raw, final = r.read(300001), r.url
                break
            except HTTPError as exc:
                if attempt or exc.code not in (502, 503, 504):
                    raise
    obj = build(raw, final)
    payload = json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload, encoding="utf-8")
    print("SOURCE_SHA256=" + SHA256)
    print("SOURCE_CAPTURE=" + CAPTURE)
    print("DERIVED_SHA256=" + hashlib.sha256(payload.encode()).hexdigest())


if __name__ == "__main__":
    main()
