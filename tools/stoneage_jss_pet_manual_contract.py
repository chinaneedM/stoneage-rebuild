"""Derive bounded JSS 2001 pet interactions from the already authenticated manual.

No game, client binary, server, or proprietary image is executed/retained.
The raw manual is a temporary input; only hashes and structured observations survive.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import urllib.request

from tools.stoneage_early_content_probe import section

CAPTURE = "20010418083149"
URL = f"https://web.archive.org/web/{CAPTURE}id_/http://www.titan.co.jp/stoneage/manual02.html"
SOURCE_SHA256 = "50b9771ec501067136629c8e083a190e979e53dd9ba141903f78b76d43b602cc"
ANCHORS = ("3050", "3051", "3080", "4010", "4020", "6010", "6015", "6020", "6030", "6040", "8026", "8090")


def require(ok, message):
    if not ok:
        raise ValueError(message)


def derive(document):
    """Read source assertions, keeping thresholds separate from unknown formulas."""
    parts = {a: section(document, a) for a in ANCHORS}

    def mentions(anchor, *tokens):
        require(all(t in parts[anchor] for t in tokens), f"{anchor}: missing business assertion")

    def number(anchor, pattern):
        match = re.search(pattern, parts[anchor])
        require(match is not None, f"{anchor}: missing numeric assertion")
        return int(match.group(1))

    mentions("3050", "[バトル]", "一匹のみ", "[待機]", "[休み]", "[メール]", "[Ctrl]+[P]")
    mentions("3051", "付けたプレイヤーしか", "標準の名前に戻した後", "他のプレイヤー", "クリックすると")
    mentions("3080", "所有したことのある", "戦闘で出会った", "名前が", "写真をとる", "イラスト", "簡単なステータス")
    mentions("4010", "カウント", "ペットのコマンド", "決定ボタン", "待機時間が終了", "入力待ちに戻ります")
    mentions("4020", "応援要請", "HELP", "待機中のペットのみ", "グループは解散", "装備の変更もできます")
    mentions("6010", "魅力", "残り耐久力が少ないほど", "所有最大数を越えて", "捕獲できません")
    capture_gap = number("6010", r"プレイヤーよりも(\d+)レベル以上")
    loyalty_cap = number("6010", r"忠誠度は最大でも(\d+)")
    mentions("6015", "名前変更", "右クリック", "標準の名前に戻した後", "変更できます")
    mentions("6020", "名前を右クリック", "一定時間", "野良ペット", "やがて消滅")
    mentions("6030", "隣接", "右クリック", "所有最大数を越えて", "拾うことはできません")
    pickup_gap = number("6030", r"キャラクターよりも(\d+)レベル以上")
    mentions("6040", "覚えられる数が決まって", "ブリーダー", "忘れさせることはできません", "上書き", "順番を入れ替えることはできません")
    mentions("8026", "逃げ出す", "魅力", "レベルアップ", "回復させ続ける", "ペットの気絶", "ペットを攻撃", "特定のアイテム")
    mentions("8090", "二つ以上", "右クリック", "同じクラス", "苦手", "壊れ", "素材として使用")
    synthesis_max = number("8090", r"最大で(\d+)個まで")
    require((capture_gap, pickup_gap, loyalty_cap, synthesis_max) == (6, 6, 60, 15), "manual numeric contracts changed")
    return {
        "pet_action_selection": {"anchor": "3050", "modes": ["BATTLE", "STANDBY", "REST", "MAIL"], "initial_battle_pet_limit": 1, "shortcut": "CTRL_P", "mode_wire_values": None},
        "capture": {"anchor": "6010", "blocked_if_target_level_minus_player_level_at_least": capture_gap, "initial_loyalty_upper_bound": loyalty_cap, "lower_remaining_hp_improves_chance_described": True, "charm_influences_chance_described": True, "cannot_exceed_ownership_capacity": True, "capacity_number": None, "probability_formula": None, "initial_loyalty_formula": None},
        "release": {"anchor": "6020", "control": "RIGHT_CLICK_PET_NAME", "sequence": ["PLACED_ON_FIELD", "OWNERLESS_AFTER_UNSPECIFIED_TIME", "EVENTUAL_DISAPPEARANCE"], "seconds": None},
        "pickup": {"anchor": "6030", "control": "ADJACENT_AND_RIGHT_CLICK", "blocked_if_pet_level_minus_player_level_at_least": pickup_gap, "cannot_exceed_ownership_capacity": True, "capacity_number": None},
        "rename": {"anchors": ["3051", "6015"], "only_naming_player_can_rename_named_pet_described": True, "reset_to_default_before_transfer_allows_next_owner_rename_described": True, "button_wording": {"3051": "CLICK_UNSPECIFIED_BUTTON", "6015": "RIGHT_CLICK_RENAME_BUTTON"}, "button_uniformity_proven": False, "persistent_owner_field_or_wire_value": None},
        "skills": {"anchor": "6040", "learnable_slot_count_is_bounded_per_pet": True, "slot_count": None, "trainer": "PET_SHOP_BREEDER", "forget_without_replacement_described_as_available": False, "overwrite_with_other_skill_described": True, "reorder_described_as_available": False, "skill_ids_prices_and_learning_predicates": None},
        "album": {"anchor": "3080", "name_records": ["PREVIOUSLY_OWNED_PETS", "BATTLE_ENCOUNTERED_CREATURES"], "photo_action_adds": ["ILLUSTRATION", "BRIEF_STATUS"], "all_encounters_automatically_include_photo": False, "bitmap_or_species_ids": None},
        "battle_flow": {"anchor": "4010", "sequence": ["COUNTED_COMMAND_INPUT", "PLAYER_COMMAND", "PARTICIPATING_PET_COMMAND", "CONFIRM_OR_TIMEOUT", "NEXT_INPUT_IF_UNRESOLVED"], "timeout_seconds": None},
        "battle_pet_and_help": {"anchor": "4020", "join_or_swap_requires_standby_pet_described": True, "help_request_enables_outside_participation": True, "leader_escape_dissolves_party_described": True, "equipment_change_during_battle_described": True, "turn_cost_or_network_ack_proven": False},
        "loyalty": {"anchor": "8026", "increase_examples": ["OWNER_LEVEL_UP", "OWNER_CHARM_UP", "REPEATED_IN_BATTLE_HEALING", "SPECIFIC_ITEMS"], "decrease_examples": ["OWNER_CHARM_DOWN", "PET_UNCONSCIOUS", "ATTACKING_PET_IN_BATTLE", "SPECIFIC_ITEMS"], "low_loyalty_can_disobey_or_escape_described": True, "numeric_deltas_or_formula": None},
        "crafting": {"anchor": "8090", "processing_minimum_selected_materials": 2, "maximum_selected_materials": synthesis_max, "control": "RIGHT_CLICK_INPUTS_THEN_PET_SKILL", "same_class_inputs_described_as_easier": True, "pet_aptitude_difference_described": True, "broken_output_can_be_used_as_material_described": True, "recipes_item_ids_success_formula": None},
    }, parts


def report(raw, final_url):
    require(final_url == URL, "capture/original URL changed; requalify source")
    require(len(raw) == 28434 and hashlib.sha256(raw).hexdigest() == SOURCE_SHA256, "authenticated manual bytes changed")
    document = raw.decode("shift_jis", errors="strict")
    contracts, parts = derive(document)
    return {
        "schema": "stoneage.jss2001.pet_manual_contract.r1",
        "task": "JSS2001-PET-INTERACTION-MANUAL-01",
        "source": {"url": URL, "final_url": final_url, "actual_capture": CAPTURE, "sha256": SOURCE_SHA256, "bytes": len(raw), "encoding": "shift_jis", "replacement_characters": 0, "role": "FIRST_PARTY_MANUAL_DESCRIPTION", "newly_discovered_source": False},
        "section_sha256": {a: hashlib.sha256(t.encode()).hexdigest() for a, t in parts.items()},
        "contracts": contracts,
        "boundaries": {"scope": "JSS_JAPAN_2001_MANUAL_DESCRIPTION_ONLY", "jss1999_or_tw10_same_build_proven": False, "original_server_executed": False, "species_graphic_ids_or_original_world_recovered": False, "ownership_capacity_number_recovered": False, "original_assets_retained": False, "stage_a_family_status_changed": False, "stage_b_production": "GATED", "r79": "PAUSED_NON_BLOCKING"},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.input:
        raw, final_url = args.input.read_bytes(), URL
    else:
        request = urllib.request.Request(URL, headers={"User-Agent": "StoneAge historical evidence research"})
        with urllib.request.urlopen(request, timeout=40) as response:
            require(response.status == 200, "manual HTTP response")
            raw, final_url = response.read(2_000_001), response.url
    result = report(raw, final_url)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"sections": len(result["section_sha256"]), "contracts": len(result["contracts"]), "same_build_promoted": False}))


if __name__ == "__main__":
    main()
