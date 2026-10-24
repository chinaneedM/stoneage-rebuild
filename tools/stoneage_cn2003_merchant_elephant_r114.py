#!/usr/bin/env python3
"""R114 source-boundary validation. Evidence metadata only, never original-server replay."""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "research/recovered/STONEAGE-CN2003-MERCHANT-ELEPHANT-R114.json"

def validate(d):
    assert d["schema"] == "stoneage.cn2003.merchant_elephant_quest.r114"
    assert d["task"] == "OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-114"
    assert len(d["sources"]) == 3
    s1, s2, late = d["sources"]
    assert s1["url"] == "https://games.sina.com.cn/z/sta/rwgl/fs.shtml?from=wap"
    assert s1["publication_date"] == "2003-06-30" and s1["publication_time"] == "11:55"
    assert s1["byline"] == "新浪游戏"
    assert s1["tier"] == "CONTEMPORANEOUS_MEDIA_GUIDE_NOT_AUTHENTICATED_OPERATOR_MASTER"
    assert s1["article_text_accessible"] is True
    for key in ("original_article_html_bytes", "original_article_html_sha256", "historical_capture_sha256", "actual_original_game_build"):
        assert s1[key] is None
    assert s1["official_server_implementation_authenticated"] is False
    assert s2["tier"] == "SAME_SITE_LATER_CATEGORY_INDEX_NOT_INDEPENDENT_GAMEPLAY_WITNESS"
    assert s2["list_entry"] == "富商的货物"
    assert s2["labelled_version"] == "石器时代6.0海贼王遗迹"
    assert s2["original_2003_release_build_authenticated"] is False
    assert s2["independent_contemporary_server_eyewitness"] is False
    assert late["publication_date"] == "2018-06-01" and late["independent_original_2003_witness"] is False
    assert late["current_repost_not_used_to_raise_historical_rule_certainty"] is True
    e = d["edition"]
    assert e["market"] == "CN_MAINLAND" and e["source_year"] == 2003
    assert e["sina_index_version_label"] == "6.0"
    for key in ("confirmed_original_client_build", "confirmed_original_server_build", "exact_earliest_release_version"):
        assert e[key] is None
    assert e["jss1999_or_tw10_identity_proven"] is False
    assert e["original_operator_quest_master_proven"] is False
    q = d["quest"]
    assert q["precondition_adult_ceremony"] == "REQUIRED_AS_GUIDE_STATES"
    assert q["level55"] == "RECOMMENDED_NOT_MANDATORY_AS_GUIDE_STATES"
    assert q["feather_items"] == ["福尔德村的羽毛", "达那村的羽毛"]
    assert q["feather_status"] == "RECOMMENDED_NOT_PROVEN_QUEST_DEPENDENCIES"
    assert q["repeatability"] == "REPEATABLE_AS_REPORTED_NO_SERVER_LOG"
    loc = q["request_location"]
    assert [loc["island"], loc["village"], loc["npc_name_first"], loc["coordinate_original"]] == ["沙姆岛", "奇努伊村", "盖落比", "54。76"]
    for key in ("original_npc_id", "original_map_id", "original_sprite_id"):
        assert loc[key] is None
    assert q["npc_return_spelling"] == "盖洛比"
    assert q["original_npc_identity_equivalence_verified"] is False
    assert q["gives_cargo_item_name"] == "富商的货物" and q["original_cargo_item_id"] is None
    cap = q["capture_location"]
    assert cap["island"] == "吉鲁岛" and cap["zone_as_written"] == "5X级小象区"
    assert cap["target_name"] == "巨大玛恩摩" and cap["target_level_reported"] == 60
    assert cap["actual_encounter_spawn_table"] is None and cap["original_pet_species_id"] is None
    assert q["reported_cargo_disappears_after_successful_capture"] is True
    assert q["original_cargo_consumption_transaction_verified"] is False
    assert q["returns_to_npc_for_reward"] is True
    assert q["reward_item_name"] == "宠物忠诚肉片" and q["original_reward_item_id"] is None
    assert q["reward_effect_loyalty_delta_reported"] == 10
    assert q["actual_original_loyalty_effect_verified"] is False
    assert q["capture_advice_hp_below_100"] == "PLAYER_GUIDE_TIP_NOT_CAPTURING_PROBABILITY_FORMULA"
    for key in ("original_capture_chance_formula", "original_quest_flag_names",
                "original_reward_delivery_log", "original_save_state_fields"):
        assert q[key] is None
    assert len(d["text_flow"]) == 3
    assert len(d["conflicts_to_preserve"]) == 5 and len(d["next_reopen_if"]) == 4
    b = d["evidence_boundary"]
    assert b["image_placeholders_count"] == 9
    assert b["original_nine_image_bytes_captured"] is False
    assert b["original_nine_image_sha256"] is None and b["pixel_content_identity_verified"] is False
    assert b["same_build_spr_or_npc_visual_join"] is None
    assert b["original_server_script_or_runtime_trace"] is None
    assert b["original_client_same_build_executable_trace"] is None
    assert b["claims_are_media_guide_not_implemented_original_game_entities"] is True
    assert b["no_original_proprietary_html_or_images_committed"] is True
    assert b["overall_restoration_percentage"] is None
    assert b["cross_version_projection_to_1999_or_tw10"] is False
    assert d["archive_record_not_original_entity_count"] is True
    assert d["stage_a_system_families"] == "7_PARTIAL_2_OPEN"
    assert d["stage_b_and_wiki"] == "GATED"
    assert d["tw10_savedata_r79"] == "PAUSED_NON_BLOCKING"
    return True

if __name__ == "__main__":
    assert validate(json.loads(DATA.read_text(encoding="utf-8")))
    print("R114 bounded media-claim contract PASS")
