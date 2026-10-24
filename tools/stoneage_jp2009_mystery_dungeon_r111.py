#!/usr/bin/env python3
"""R111 conservative source-claim verifier. Not a 2009 source-byte or game-runtime replay."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/"research/recovered/STONEAGE-JP2009-MYSTERY-DUNGEON-R111.json"

def verify(d):
    assert d["schema"]=="stoneage.jp2009.mystery_dungeon.r111"
    assert d["task"]=="OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-111"
    s=d["source"]
    assert s["url"]=="https://www.4gamer.net/games/013/G001377/20091019025/"
    assert s["publisher_announced"]=="デジパーク"
    assert s["source_rank"]=="CONTEMPORARY_PUBLISHER_PRESS_TEXT_REPRODUCED_AT_4GAMER"
    assert s["media_says_verbatim_release"] and s["live_opened_article_as_text"]
    assert s["actual_media_html_bytes"] is None and s["actual_media_html_sha256"] is None
    assert s["original_2009_html_capture"] is None and s["original_2009_html_sha256"] is None
    assert s["operator_hosted_original_page"] is None
    v=d["historical_version"]
    assert v["region"]=="JP" and v["specific_client_build"] is None
    assert v["tw10_1999_equivalence"] is False and v["server_script_authenticated"] is False
    ev=d["event"]
    assert ev["scheduled_start"]=="2009-10-20" and ev["scheduled_end"]=="2009-11-04"
    assert ev["chronological_status"]=="ANNOUNCED_SCHEDULE_NOT_DEPLOYMENT_LOG"
    assert ev["other_first_second_phase_events_not_imported"] is True
    g=d["gameplay"]
    assert g["entrance_npc_as_written"]=="レテ" and g["entrance_location"]=="チャットルーム"
    assert g["interaction"]=="TALK_TO_NPC_FOR_DUNGEON_TRANSFER"
    assert g["floor_or_room_count"]==10
    assert g["room_number_semantics"]=="TEN_ROOMS_ANNOUNCED_NOT_TEN_SEPARATE_MAP_PAYLOADS"
    assert g["puzzle_progression"]=="ANSWER_ROOM_QUESTION_TO_ADVANCE"
    assert g["puzzle_theme_examples"]==["STONEAGE_KNOWLEDGE","IN_SCENE_WHO_DID_IT_MYSTERY"]
    assert g["puzzle_bank_or_exact_answers"] is None
    assert g["failure_branch"]=={"condition":"ANSWER_INCORRECT","destination":"チャットルーム","restart":"BEGIN_FROM_FIRST_ROOM"}
    assert g["success_branch"]["condition"]=="ALL_TEN_QUESTIONS_CORRECT"
    assert g["success_branch"]["reward_item_ids"] is None
    e=g["encounters"]
    assert e["claim"]=="NO_HOSTILE_DINOSAUR_SPAWNS_INSIDE_MYSTERY_DUNGEON"
    assert e["non_dinosaur_battles_excluded"] is False and e["all_combat_disabled_proven"] is False
    assert g["exact_entry_eligibility_predicate"] is None
    for k in ("original_npc_id","actual_map_floor_ids","original_server_transitions"):
        assert g[k] is None
    assert g["actual_portal_working_verified"] is False
    m=d["media_visual"]
    assert m["one_link_actually_opened"]=="https://www.4gamer.net/games/013/G001377/20091019025/TN/002.jpg"
    assert m["observed_through_retrieval_tool"] is True
    for k in ("actual_image_bytes_local","actual_image_sha256","original_sprite_or_bitmap_id","republication_permission"):
        assert m[k] is None
    assert m["caption_group_mentions_lete"] and not m["this_thumbnail_shows_lete_proven"]
    assert not m["in_game_screenshot_same_build_proven"] and not m["original_art_committed"]
    rs=d["records"]
    assert len(rs)==6 and len({r["record_id"] for r in rs})==6
    byid={r["record_id"].split(":")[-1]:r for r in rs}
    assert set(byid)=={"lete-npc","mystery-dungeon-place","puzzle-state-machine","wild-encounter-boundary","unnamed-reward","thumbnail-caption"}
    for r in rs:
        for field in ("record_id","entity_type","collection","version_profile","source_refs","verification_status","rights_status","record_revision","game_ids"):
            assert field in r
        assert r["game_ids"] is None
        assert r["version_profile"]=="LATER_OFFICIAL:JP_DIGIPARK_2009_TENTH_ANNIVERSARY_NOT_EARLY_TW10"
        assert r["source_refs"]==["S1"]
        assert r["verification_status"]=="PUBLISHER_PRESS_TEXT_REPRODUCED_IN_CONTEMPORARY_MEDIA_NOT_RUNTIME"
        assert r["rights_status"]=="RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED"
    assert byid["lete-npc"]["name_as_written"]=="レテ" and byid["lete-npc"]["npc_original_id"] is None
    assert byid["mystery-dungeon-place"]["reported_room_count"]==10
    assert byid["mystery-dungeon-place"]["is_ten_game_maps_proven"] is False
    assert byid["puzzle-state-machine"]["fail"]=="WRONG_BACK_TO_CHATROOM_AND_RESTART"
    assert byid["puzzle-state-machine"]["actual_server_script"] is None
    assert byid["wild-encounter-boundary"]["all_battles_absent_proven"] is False
    assert byid["unnamed-reward"]["actual_item_name"] is None and not byid["unnamed-reward"]["grant_verified"]
    assert byid["thumbnail-caption"]["pixel_to_named_npc_binding"] is None
    nxt=d["continuation"]
    assert nxt["next"]=="OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-112"
    assert nxt["overall_restoration_percent"] is None
    assert nxt["savedata_r79"]=="PAUSED_NON_BLOCKING" and nxt["stage_b_and_wiki"]=="GATED"
    return True

if __name__=="__main__":
    assert verify(json.loads(PATH.read_text(encoding="utf-8")))
    print("R111 press-source metadata bounds: PASS; no original-byte or runtime execution")
