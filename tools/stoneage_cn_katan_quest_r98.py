"""R98 Katan NPC quest cross-guide conflict and nonexecuted state contract."""
import hashlib
import json
from pathlib import Path

P=Path(__file__).resolve().parents[1]/"research/recovered/STONEAGE-CN-KATAN-QUEST-SOURCE-CONFLICTS-R98.json"
SHA="e92c249a74582ba6f5af5b41f49540ec9d1cd1d2"
FISH=["加格","邦恩吉","克邦凯斯","加克拉"]
BIRDS=["火鸡","奇宝","克克洛斯","霍尔克"]

def git_sha(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode("ascii")+b"\0"+raw).hexdigest()

def verify(d):
    assert git_sha(P.read_bytes())==SHA, "immutable R98 source changed"
    assert d==json.loads(P.read_text(encoding="utf-8")), "source mutation or injected authority"
    assert d["schema"]=="stoneage.cn2001_2003_katan_quest_source_disagreements.r98"
    assert d["task"]=="OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-98"
    s=d["sources"]
    assert len(s)==2 and [x["id"] for x in s]==["R98-S1","R98-S2"]
    assert s[0]["display_date"]=="2001-06-14" and s[0]["byline"]=="陶陶"
    assert s[1]["display_date"]=="2003-05-29 14:24" and s[1]["byline"] is None
    assert all(x["original_game_build"] is None and x["original_publication_bytes_verified"] is False and x["original_server_authority"] is False for x in s)
    assert [x["name"] for x in d["npcs"]]==["卡坦","樵夫巴尔","哈恩"]
    assert all(x["native_npc_id"] is None and x["original_dialogue_assets"] is None for x in d["npcs"])
    n=d["npc_search"]
    assert (n["s1_player_search_south_coordinate"],n["s2_player_search_south_coordinate"])==(198,190)
    assert [(x["name"],x["east"],x["south"]) for x in n["s2_village_landmarks"]]==[("卡坦村",259,170),("霍特尔村",622,193)]
    assert n["exact_spawn_locations"] is None and n["fixed_original_npc_position_proven"] is False
    f=d["quest"]["fish_stage"];q=d["quest"]["bird_stage"]
    assert f["pet_names"]==FISH and f["first_pair"]==FISH[:2] and f["second_pair"]==FISH[2:]
    assert q["pet_names"]==BIRDS and q["first_pair"]==BIRDS[:2] and q["second_pair"]==BIRDS[2:]
    assert f["required_level_for_each_pet"]==q["required_level_for_each_pet"]==25
    assert f["intermediate_item_s1"]=="未记名称的戒指" and f["intermediate_item_s2"]=="火鸡的戒指"
    assert "无法继续" in f["guide_drop_ring_s1"] and "再次向卡坦索取" in f["guide_drop_ring_s2"]
    assert f["reward_name_both"]=="修宝" and f["reward_color_both"]=="金色"
    assert (f["s2_ring_claimed_charm"],f["s2_ring_claimed_critical"])==(2,5)
    assert f["original_item_consumption_trace"] is False and f["original_give_back_transaction_proven"] is False
    assert f["s2_ring_critical_as_percentage_proven"] is False
    assert q["intermediate_item_s1"]=="火难戒指" and q["intermediate_item_s2"]=="火鸡的戒指"
    assert q["reward_name_both"]=="朵拉比斯" and q["reward_color_both"]=="金色"
    assert q["item_equivalence_proven"] is False and q["s1_repeat_condition_verified"] is False
    assert q["original_second_cycle_execution_proven"] is False
    assert d["quest"]["s2_suggested_player_level"]==35 and d["quest"]["suggested_level_is_hard_server_gate"] is False
    c=d["conflicts"]
    assert [x["id"] for x in c]==["NPC_SEARCH_LINE","INTERMEDIATE_FISH_RING","FISH_RING_LOSS","BIRD_RING_NAME","BIRD_RING_EFFECT_WORDING"]
    assert all(x["resolved"] is False for x in c)
    assert c[2]["server_recovery_contract"] is None and c[3]["official_item_id"] is None and c[4]["effect_opcode"] is None
    i=d["illustrated_guide"]
    assert i["captions_observed_in_page"] is True
    assert all(i[k] is False for k in ("article_specific_image_bytes_verified","screenshot_original_build_authenticated","npc_pixels_identified","screenshot_proves_server_transaction"))
    assert all(d["dedup"][k] is False for k in ("modern_reposts_counted_as_independent_sources","old_cn2003_mengde_r81_is_same_katan_quest","cross_2001_2003_exact_game_build_match"))
    pub=d["publication"]
    assert pub["metadata_only"] is True
    assert all(pub[k] is False for k in ("original_html_committed","images_committed","commercial_server_executed","stage_a_closed","stage_b_started"))
    assert pub["overall_restoration_percent"] is None and pub["next"]=="OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-99"
    return True

if __name__=="__main__":
    assert verify(json.loads(P.read_text(encoding="utf-8")))
    print("R98 PASS: two source-scoped Katan handover stages; unresolved ring loss/name/location; no server or visual claim")
