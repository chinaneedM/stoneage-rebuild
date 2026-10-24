#!/usr/bin/env python3
"""Validate R115 limited publisher-byline archived media claims; not a historical runtime."""
import json
from pathlib import Path
FILE=Path(__file__).resolve().parents[1]/"research/recovered/STONEAGE-CN2003-MIDAUTUMN-R115.json"

def validate(d):
    assert d["schema"]=="stoneage.cn2003.midautumn_quest_notice.r115"
    assert d["task"]=="OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-115"
    s=d["source"]
    assert s["url"]=="https://news.17173.com/z/stoneage/content/2003-9-11/n631_547722.html"
    assert s["title"]=="任务攻略:石器时代中秋任务"
    assert s["page_date"]=="2003-09-11" and s["page_byline"]=="华义"
    assert s["authority"]=="CONTEMPORANEOUS_MEDIA_ARCHIVE_WITH_PUBLISHER_BYLINE_NOT_AUTHENTICATED_ORIGINAL_OPERATOR_BYTES"
    assert s["currently_readable_web_text"] is True and s["byline_independently_authenticated"] is False
    for k in ("original_2003_operator_site_html","original_2003_article_capture_html_sha256",
              "current_http_raw_html_bytes","current_http_raw_html_sha256","original_game_client_build","original_server_build"):
        assert s[k] is None
    link=s["linked_related_article"]
    assert link["label"]=="石器中秋任务开放及奖品追加"
    assert link["relative_link_malformed_by_media_rewrite"] is True
    assert link["corrected_historical_content_verified"] is False
    assert link["independent_source_count_increment"]==0
    e=d["edition"]
    assert e["region"]=="CN" and e["era"]=="2003_MEDIA_DATE"
    assert e["exact_official_patch_version"] is None
    assert e["claimed_game_server_deployment_verified"] is False
    assert e["jss1999_or_tw10_same_version_proven"] is False
    assert e["taiwan2002_werewolf_or_jp2004_christmas_identity_join"] is False
    n=d["narrative"]
    assert n["participants_as_text"]==["后羿","嫦娥","月兔"]
    assert n["original_server_npc_ids"] is None
    assert n["original_dialogue_and_quest_script"] is None and n["in_world_year"] is None
    assert len(n["steps_as_reported"])==4
    assert "捉迷藏" in n["steps_as_reported"][1]["claim"]
    assert n["steps_as_reported"][1]["quest_condition_id"] is None
    assert n["steps_as_reported"][2]["permit_name"] is None
    assert n["steps_as_reported"][2]["warp_map_id"] is None
    assert n["unknown_double_asterisk_terms_in_2003_archive"]==["月兔和**","得到**许可"]
    assert n["redacted_terms_restored"] is False
    assert n["repeatability"]=="PAGE_CLAIMS_CAN_REPEAT_NOT_VERIFIED_RUNTIME"
    assert n["actual_quest_replay_verified"] is False
    r=d["rewards"]
    assert r["distribution_label"]=="随机得到"
    assert r["random_probabilities"] is None
    assert r["exclusive_one_reward_across_all_categories_proven"] is False
    assert len(r["entries"])==4
    a,b,c,f=r["entries"]
    assert a["label"]=="变身镜子lv1" and a["stated_effect"]=="变身成自己的宠物一分钟"
    assert a["item_master_id"] is None and a["actual_runtime_duration_verified"] is False
    assert b["label"]=="宠物技能罐头"
    assert b["skills_as_reported"]==["旅途伙伴2","狂乱暴走"]
    assert b["one_can_teaches_both_proven"] is False
    assert b["item_master_id"] is None and b["skill_runtime_verified"] is False
    assert c["label"]=="爱相随戒指" and c["stated_uses"]==10
    assert c["teleport_target_formula"] is None and c["actual_server_uses_verified"] is False
    assert f["label"]=="14~16级精灵武器装备中的一个"
    assert f["level_range"]==[14,16] and f["precise_item_list"] is None
    assert f["random_draw_range_exactness_verified"] is False
    for x in r["entries"]: assert x["item_master_id"] is None
    assert r["original_server_item_and_pet_master_verified"] is False
    c=d["classification"]
    assert c["world_story"]=="LATER_CN_EVENT_NARRATIVE_NOT_EARLY_UNIVERSAL_CANON"
    assert c["documented_ui"]=="TEXT_DESCRIPTION_ONLY"
    assert c["images_in_task_article"]=="NO_SOURCE_VERIFIED_NPC_OR_MAP_SCREENSHOT"
    assert c["new_original_game_entity_identifiers"]==0
    assert c["research_archival_claims_only"] is True and c["version_source_boundary_preserved"] is True
    assert len(d["reopen_requirements"])==4
    g=d["hard_gates"]
    for k in ("original_1999_or_tw10_quest_identity","item_or_npc_original_game_ids_populated",
              "runtime_executed","server_rewards_redeemed","source_html_replayed_byte_exact",
              "copyright_proprietary_html_or_images_committed"):
        assert g[k] is False
    assert g["stage_a"]=="7_PARTIAL_2_OPEN"
    assert g["stage_b_and_wiki"]=="GATED"
    assert g["savedata_r79"]=="PAUSED_NON_BLOCKING"
    assert g["overall_completion_percent"] is None
    assert g["highest_next"]=="OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-116"
    return True

if __name__=="__main__":
    assert validate(json.loads(FILE.read_text(encoding="utf-8")))
    print("R115 bounded contemporary media-byline contract PASS")
