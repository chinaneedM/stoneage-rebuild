#!/usr/bin/env python3
"""R109 bounded cross-version guide-claims guard. Not a live HTML/server replay."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "research/recovered/STONEAGE-CN2003-2006-DRAGON-FLIGHT-R109.json"

def verify(d):
    assert d["schema"] == "stoneage.cn_dragon_flight.r109"
    assert d["task"].endswith("-109")
    assert len(d["sources"]) == 2 and [s["id"] for s in d["sources"]] == ["S1","S2"]
    assert d["sources"][0]["url"] == "https://games.sina.com.cn/zhqu/sta/article/2003-06-03/10634.shtml"
    assert d["sources"][1]["url"] == "https://news.17173.com/z/stoneage/content/2006-05-14/1147617360.shtml"
    for s in d["sources"]:
        assert s["observed_mode"] == "WEB_TEXT_ONLY"
        assert s["raw_html_bytes"] is None and s["raw_html_sha256"] is None
        assert s["archival_capture"] is None
        assert "NOT_OPERATOR_PRIMARY" in s["provenance_class"]
    v = d["version_constraints"]
    assert v["s1_exact_build"] is None and v["s2_exact_build"] is None
    assert v["s2_title_claim_is_build_proof"] is False
    assert v["early_taiwan_1_0_lineage_proven"] is False
    assert v["mutual_independence_of_guides_proven"] is False
    x = d["claim_crosswalk"]
    assert x["required_levels"]["S1_literal"] == "80级"
    assert x["required_levels"]["S2_literal"] == "80级以上(不包含80级)"
    assert x["required_levels"]["shared_runtime_threshold"] is None
    assert x["adult_ceremony"]["identical_runtime_flag_proven"] is False
    assert x["accepted_flyer_names_as_written"] == ["帖拉格恩","洛卡伦恩","加宝格恩","朵拉比斯"]
    c = x["flyer_delivery_count"]
    assert {q["count"] for q in c["S1_one_claims"]} == {1}
    assert {q["count"] for q in c["S1_three_claims"]} == {3}
    assert len(c["S1_one_claims"]) == 2 and len(c["S1_three_claims"]) == 2
    assert c["S1_conflict"] == "UNRESOLVED_SAME_2003_GUIDE_ONE_VS_THREE_FLYERS"
    assert c["S2_claimed_count"] == 1
    assert c["S1_actual_consumption"] is None and c["S2_actual_consumption"] is None
    assert c["cross_version_retroactive_resolution"] is False
    tr = x["transport"]
    assert tr["S1_reported_repeat_fare_stone"] == 10000
    assert tr["S1_reported_reward_stone"] == 200000
    assert tr["S2_reported_reward_stone"] == 200000
    assert tr["real_transaction_verified"] is False
    assert x["fictional_worldline"]["universal_official_canon_verified"] is False
    records = d["records"]
    assert len(records) == 10
    ids = [q["record_id"].split(":")[-1] for q in records]
    assert len(set(ids)) == len(ids)
    for q in records:
        for f in ("record_id","entity_type","collection","version_profile","source_refs",
                  "verification_status","rights_status","record_revision","game_ids"):
            assert f in q
        assert q["game_ids"] is None
        assert q["version_profile"] == "LATER_CN_GUIDE_2003_WITH_CN8_PLAYER_COMPARISON_NO_EXACT_BUILD"
        assert q["rights_status"] == "RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED"
        assert q["verification_status"] == "PUBLISHED_GUIDE_CLAIM_NOT_ORIGINAL_SERVER_EXECUTION"
        assert set(q["source_refs"]).issubset({"S1","S2"}) and q["source_refs"]
    by_id = {q["record_id"].split(":")[-1]: q for q in records}
    assert by_id["clark-referral"]["name_as_written"] == "打工名人克拉克"
    assert by_id["hortledun"]["name_as_written"] == "霍特雷敦"
    assert by_id["pc-thief-chief"]["name_as_written"] == "PC盗贼团老大"
    assert by_id["bruce"]["name_as_written"] == "飞龙总教练布鲁斯"
    for i in ("clark-referral","hortledun","pc-thief-chief","bruce","loli-caption"):
        assert by_id[i]["original_npc_id"] is None
    assert by_id["loli-caption"]["caption_visual_acquired"] is False
    assert by_id["four-flyer-names"]["all_original_species_ids"] is None
    assert by_id["four-flyer-names"]["consumed_flyer_count"] is None
    assert by_id["flight-gate"]["exact_level_rule"] is None
    assert by_id["flight-gate"]["guide_count_conflict"] == c["S1_conflict"]
    assert by_id["flight-story-chain"]["server_state_machine"] is None
    assert by_id["dragon-airline"]["actual_travel_proven"] is False
    assert by_id["dragon-airline"]["actual_save_format"] is None
    assert by_id["eden-nis-story"]["official_canonical_status"] is None
    assert by_id["eden-nis-story"]["links_to_original_1999"] is None
    assert d["continuation"]["overall_restoration_percent"] is None
    assert d["continuation"]["savedata_r79"] == "PAUSED_NON_BLOCKING"
    assert d["continuation"]["stage_b_and_wiki"] == "GATED"
    return True

if __name__ == "__main__":
    assert verify(json.loads(PATH.read_text(encoding="utf-8")))
    print("R109 cross-version source boundaries: PASS (not original HTML/runtime replay)")
