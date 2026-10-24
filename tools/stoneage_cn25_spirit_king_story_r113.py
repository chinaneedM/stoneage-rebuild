#!/usr/bin/env python3
"""R113 source-bound story metadata only; not a 2002 binary/server replay."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"research/recovered/STONEAGE-CN25-SPIRIT-KING-STORY-R113.json"

def validate(d):
    assert d["schema"] == "stoneage.cn25.spirit_king_story.r113"
    assert d["task"] == "OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-113"
    assert d["scope"] == "TWO_17173_PAGES_2004_STORY_SYNOPSIS_AND_2002_PLAYER_QUEST_ACCOUNT_NO_ORIGINAL_CLIENT"
    a,b=d["sources"]
    assert len(d["sources"])==2 and a["id"]=="S1" and b["id"]=="S2"
    assert a["url"] == "https://news.17173.com/z/stoneage/banben/sa10/39.htm"
    assert b["url"] == "https://news.17173.com/z/stoneage/content/2002-5-20/n855_771416.html"
    assert a["webpage_display_date"]=="2004-07-02" and b["webpage_display_date"]=="2002-05-20"
    assert b["credited_author"]=="柯南"
    assert a["source_role"]=="17173_LATER_VERSION_STORY_SYNOPSIS_UNATTRIBUTED_AUTHOR_NOT_AUTHENTICATED_OFFICIAL_ORIGINAL"
    assert b["source_role"]=="CONTEMPORANEOUS_PLAYER_SUBMISSION_WITH_UNVERIFIED_SELF_REPORTED_GAMEPLAY"
    for s in (a,b):
        for k in ("original_2002_html_capture","original_html_sha256","actual_current_html_bytes","actual_current_html_sha256"):
            assert s[k] is None, (s["id"],k)
    assert a["source_authorship_authenticated"] is False
    x=d["dedupe"]
    assert x["subpage_counted_as_independent_source"] is False
    assert x["existing_r112_item_label_black_jade_not_joined"] is True
    v=d["historical_edition"]
    assert v["version_label"]=="2.5 精灵王传说" and v["region"]=="CN"
    for k in ("actual_client_build","server_build","actual_s1_first_publication_year"):
        assert v[k] is None,k
    assert v["jss1999_or_tw10_identity_proven"] is False
    assert v["original_official_operator_html_authenticated"] is False
    assert v["true_2002_server_runtime_verified"] is False
    story=d["story"]
    assert story["ancient_conflict"]=="TWO_SPIRIT_KINGS_AND_MACHINE_CIVILIZATION"
    assert story["dark_king_claims_not_reconciled"]==[
       "SELF_SEALED_PER_INTRO_TO_AVOID_DISTURBANCE",
       "SEALED_BY_LIGHT_KING_PER_QUEST_SYNOPSIS"]
    assert story["main_rescue_sequence"]==[
       "KUYI_CAVE_RED_FROG_GATE","FIND_SHINZO","RETURN_BLACK_FROG_KING_PEARL",
       "BLACK_JADE_EXCHANGE","ESCORT_AMNESIAC_MAREFIA",
       "RESTORE_MEMORY_VIA_NIS_LOCATIONS","DEFEAT_TELASOID_IN_DARK_CAVE",
       "LIGHT_KING_GRANTS_ONE_PET_REBIRTH_CHANCE"]
    assert story["landmasses_as_written"]==["吉鲁","塞伊那斯","加鲁卡"]
    assert story["person_variant_equivalence_proven"] is False
    for k in ("original_pet_master_or_rebirth_formula","original_quest_flag_names","npc_original_ids","pet_original_ids","actual_original_world_map_dat_or_tiles"):
        assert story[k] is None,k
    assert [x["relative_text"] for x in d["story_time_claims"]]==["一千五百年前","二千年","十年前","五十年前"]
    assert all(t["real_world_calendar_year"] is None for t in d["story_time_claims"])
    spell=d["disputed_spellings"]
    assert spell["s1_story"]=="地为界水为凭火为引凤为信"
    assert spell["s2_player"]=="地为界水为凭火为引风为信"
    assert spell["original_in_game_chat_trigger_verified"] is False
    assert spell["do_not_normalize_feng_glyph"] is True
    corr=d["s2_correlated_quest_observations"]
    assert corr["reported_quest_reaches_level_one_marefia"] is True
    assert corr["claimed_reincarnation_formula_not_accepted"] is True
    for k in ("actual_pixel_screenshot_authenticated","actual_server_quest_completed_independently"):
        assert corr[k] is False,k
    actors=d["actors"]
    assert len(actors)==12 and len(set(x["name_as_written"] for x in actors))==12
    assert {x["source_refs"][0] for x in actors} == {"S1"}
    for z in actors:
        assert z["game_ids"] is None if "game_ids" in z else True
        assert z["original_client_entity_id"] is None and z["original_npc_id"] is None
        assert z["original_sprite_id"] is None and z["same_build_runtime_identity_verified"] is False
        assert z["server_dialogue_verified"] is False
    edges=d["story_relations"]
    assert len(edges)==11 and len({x["record_id"] for x in edges})==11
    assert all(x["source_refs"]==["S1"] and x["same_build_entity_join_verified"] is False for x in edges)
    assert d["new_archive_claims_not_new_original_entities"] is True
    p=d["provenance_boundary"]
    for k in ("original_publisher_page_recovered","original_2_5_world_data_recovered",
              "original_2_5_npc_sprite_identity_recovered","actual_dialogue_runtime_recovered",
              "copyrighted_html_image_binary_committed","r79_savedata_reopened"):
        assert p[k] is False,k
    assert p["aggregate_restoration_percentage"] is None
    assert d["next"]=="OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-114"
    return True

if __name__=="__main__":
    validate(json.loads(DATA.read_text(encoding="utf-8")))
    print("R113 source/relationship boundary PASS; not original-client or server verification")
