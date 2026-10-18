"""Verify bounded Wayi 2005 pet gear, mentor and quest-log source claims.

This is a *source narrative* classifier, not client/runtime reconstruction.
Original HTML is fetched only during replay and never persisted to Git.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen
from tools.stoneage_wayi_intro_detail02_probe import (
    ORIGINAL, REQUESTED, Visible, inspect
)

SHA256 = "0868e56a81d7037e434a09fd0824a6eb59747494099087f8d1eaeaaa37fb690c"
BYTES = 26414
CAPTURE = "20050614005428"
GEAR = ["頭", "牙", "爪", "胸", "背", "翅", "腳"]
FEET = ["兩隻腳", "四隻腳", "魚鰭"]
ULI = ["頭", "牙", "胸", "背", "腳"]

def require(value, message):
    if not value:
        raise ValueError(message)

def normalize(s):
    return "".join(s.split())

def anchored_sections(pieces):
    anchors = ["寵物裝備系統", "導師系統", "任務日誌"]
    loc = []
    for word in anchors:
        positions = [i for i, item in enumerate(pieces) if normalize(item) == word]
        require(len(positions) == 1, "Missing or ambiguous section anchor: " + word)
        loc.append(positions[0])
    require(loc == sorted(loc), "Original section order changed")
    return (pieces[loc[0]:loc[1]], pieces[loc[1]:loc[2]], pieces[loc[2]:])

def identify_claims(pieces):
    gear, mentor, quest = anchored_sections(pieces)
    e, m, q = [normalize(" ".join(section)) for section in (gear, mentor, quest)]
    for assertion in (
        "依照不同類型之寵物", "不同之裝備欄位", "透過合成系統製作寵物裝備",
        "七大類", "分別是頭、牙、爪、胸、背、翅、腳（兩隻腳、四隻腳、魚鰭）",
        "烏力頭盔〔水〕攻擊力+15", "烏力〔地8水2〕",
        "烏力烏力〔水4火6〕", "相生相剋", "烏力最多只能裝備：頭、牙、胸、背、腳"
    ):
        require(assertion in e, "Source equipment clause lost: " + assertion)
    for assertion in ("〔領導聲望〕", "〔導師帳號〕", "〔導師姓名〕",
                      "〔導師〕", "〔學生〕", "百分之五聲望"):
        require(assertion in m, "Source mentor clause lost: " + assertion)
    for assertion in ("曾經解過的任務", "未曾解過的任務", "〔遊戲線上說明〕"):
        require(assertion in q, "Source quest-log clause lost: " + assertion)
    return {
        "equipment": {
            "kind": "OPERATOR_DESCRIBED_SYSTEM_NOT_RUNTIME_VERIFIED",
            "number_of_slot_categories": 7,
            "slot_categories_in_source_order": GEAR,
            "foot_subtypes_in_source_order": FEET,
            "pet_body_type_changes_eligible_slots": True,
            "uli_example_eligible_slots": ULI,
            "equipment_crafting_via_synthesis_described": True,
            "water_uli_helmet_example_attack_plus": 15,
            "example_pet_elements": [
                {"地": 8, "水": 2},
                {"水": 4, "火": 6}
            ],
            "source_has_repeated_uli_token": True,
            "source_describes_element_interaction": True,
            "exact_stat_scaling_formula": None,
            "actual_equipment_inventory_id": None
        },
        "mentor": {
            "kind": "OPERATOR_DESCRIBED_SYSTEM_NOT_RUNTIME_VERIFIED",
            "student_mentor_relationship": True,
            "fields_as_written": ["領導聲望", "導師帳號", "導師姓名"],
            "leadership_prestige_described_as_student_prestige_share": "5%",
            "student_reputation_deducted_proven": False,
            "actual_mentor_contract_or_server_rule": None
        },
        "quest_log": {
            "kind": "OPERATOR_DESCRIBED_SYSTEM_NOT_RUNTIME_VERIFIED",
            "previously_completed_quests_described": True,
            "not_yet_completed_quests_described": True,
            "ui_navigation_label_as_written": "遊戲線上說明",
            "original_task_ids_or_completion_flags": None
        },
        "surrounding_website_poll_not_game_mechanic": True
    }

def build(raw, final):
    info = inspect(raw, final)
    require(info["response_sha256"] == SHA256 and info["response_bytes"] == BYTES,
            "Original page byte identity differs from qualified source")
    require(info["actual_capture"] == CAPTURE, "Different archived snapshot")
    p = Visible()
    p.feed(raw.decode("big5", errors="strict"))
    claims = identify_claims(p.pieces)
    return {
        "schema": "stoneage.wayi.official_systems.source_contract.r1",
        "source": {
            "operator": "WAYI_TAIWAN",
            "original_url": ORIGINAL,
            "parent_link": "http://www.wayi.com.tw/stoneage/game/game01.asp",
            "parent_qualified_capture": "20050614002509",
            "actual_capture": CAPTURE,
            "actual_final_url": final,
            "bytes": BYTES,
            "sha256": SHA256,
            "encoding": "big5_STRICT",
            "first_party_page_verified": True,
            "is_exact_client_build": False,
            "claim_type": "OPERATOR_PAGE_DESCRIPTION_NOT_RUNTIME_DEMONSTRATION"
        },
        "claims": claims,
        "boundaries": {
            "jss1999_or_tw1_original_client_admitted": False,
            "game_patch_version_or_release_date": None,
            "server_master_tables_available": False,
            "equipment_formula_pet_ids_or_item_ids_observed": False,
            "quest_flags_npc_scripts_or_mentor_server_actions_observed": False,
            "all_official_version_equivalence": False,
            "source_html_images_or_executables_in_git": False,
            "modern_game_implementation_started": False,
            "website_publication_started": False
        },
        "next": "CROSS_VERSION_GEAR_MENTOR_QUEST_SOURCE_GAP_REVIEW"
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    with urlopen(Request(REQUESTED, headers={"User-Agent": "Mozilla/5.0 StoneAgeHistoricalEvidence"}), timeout=35) as reply:
        final = reply.url
        raw = reply.read(300001)
    obj = build(raw, final)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    output.write_text(payload, encoding="utf-8")
    print("CONTRACT_SHA256=" + hashlib.sha256(payload.encode()).hexdigest())
    print("CONTRACT_SOURCE_SHA256=" + obj["source"]["sha256"])
    print("CONTRACT_SOURCE_CAPTURE=" + obj["source"]["actual_capture"])
    print("CONTRACT_SOURCE_BYTES=" + str(obj["source"]["bytes"]))
    print("CONTRACT_CLAIMS=" + json.dumps(obj["claims"], ensure_ascii=False, sort_keys=True))

if __name__ == "__main__":
    main()
