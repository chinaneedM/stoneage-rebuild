#!/usr/bin/env python3
"""R110 source claim guards; media-only, not original-source or runtime replay."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/"research/recovered/STONEAGE-JP2004-XMAS-PARTY-COMBAT-R110.json"

def verify(data):
    assert data["schema"]=="stoneage.jp2004.xmas_party_damage.r110"
    assert data["task"]=="OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-110"
    s=data["sources"]
    assert len(s)==2 and [x["id"] for x in s]==["S1","S2"]
    assert s[0]["url"]=="https://www.4gamer.net/news/history/2004.12/20041215210314detail.html"
    assert s[1]["url"]=="https://game.watch.impress.co.jp/docs/20041224/on1224.htm"
    for x in s:
        assert x["first_party_authorship"] is False
        assert x["actual_html_bytes"] is None and x["actual_html_sha256"] is None
        assert x["original_operator_announcement_bytes"] is None
        assert x["source_role"].startswith("CONTEMPORARY_MEDIA_")
    sr=data["source_relationship"]
    assert sr["separate_media_outlets"] is True
    assert sr["operator_labels_differ"] is True and sr["operator_identity_fully_reconciled"] is False
    assert sr["first_party_webpage_access"]=="UNAVAILABLE_IN_THIS_SESSION"
    assert sr["original_game_build"] is None and sr["original_taiwan_v1_0_equivalence"] is False
    ch=data["observations"]["christmas"]
    assert ch["s1_announced_window"]=={"start":"2004-12-20","end":"2004-12-27"}
    assert ch["s1_required_quest"]=="成人の儀"
    assert ch["s2_four_villages"]==["マリナス","ジャジャ","カルターナ","サムギル"]
    assert ch["npc_original_id"] is None and ch["exact_spawn_coordinates"] is None
    assert ch["reward_item_ids"] is None and ch["reward_frequency"] is None
    assert ch["worldwide_unrestricted_access"] is False
    assert ch["server_activity_confirmed"] is False
    assert ch["independent_identification_of_santa_and_santa_girl_same_entity"] is False
    assert ch["s1_absent_from_s2_requirements_not_evidence_of_removal"] is True
    patch=data["observations"]["combat_patch"]
    assert patch["s2_reported_update_date"]=="2004-12-20"
    assert patch["target_group"]=="自パーティメンバー（ペットを含む）"
    assert patch["normal_reported_damage"]==1
    assert patch["confusion_exception"]=="混乱" and patch["confusion_damage"]=="NORMAL_DAMAGE"
    assert patch["actual_formula_verified"] is False and patch["live_client_execution_proven"] is False
    assert patch["original_taiwan_v1_0_supported"] is False
    new=data["observations"]["new_year"]
    assert new["s1_window"]=={"start":"2005-01-01","end":"2005-01-07"}
    assert new["mechanism"]=="おみくじ" and new["eligibility_as_written"]=="特になし"
    assert new["exact_impact_on_gameplay"] is None and new["confirmed_live"] is False
    rs=data["records"]
    assert len(rs)==6 and len({x["record_id"] for x in rs})==6
    for x in rs:
        for k in ("record_id","entity_type","collection","version_profile","source_refs","verification_status","rights_status","record_revision","game_ids"):
            assert k in x
        assert x["game_ids"] is None
        assert x["version_profile"]=="JP_BOTHTEC_2004_DEC_MEDIA_UPDATE_NOT_EXACT_BUILD"
        assert x["verification_status"]=="CONTEMPORARY_MEDIA_REPORT_NOT_RUNTIME"
        assert x["rights_status"]=="RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED"
        assert x["source_refs"] and set(x["source_refs"])<= {"S1","S2"}
    ids={x["record_id"].split(":")[-1]:x for x in rs}
    assert set(ids)=={"santa-girl","four-village-appearances","christmas-claim","friendly-fire-patch","new-year-shrine","operator-role-attribution"}
    assert ids["santa-girl"]["name_as_reported"]=="サンタガール"
    assert ids["santa-girl"]["original_npc_id"] is None and ids["santa-girl"]["actual_screenshot_obtained"] is False
    assert ids["four-village-appearances"]["place_names"]==ch["s2_four_villages"]
    assert ids["four-village-appearances"]["not_four_new_maps"] is True
    assert ids["christmas-claim"]["free_for_everyone_verified"] is False
    assert ids["christmas-claim"]["actual_reward_transaction"] is None
    assert ids["friendly-fire-patch"]["reported_non_confused_damage"]==1
    assert ids["friendly-fire-patch"]["reported_confused_damage"]=="NORMAL_DAMAGE"
    assert ids["friendly-fire-patch"]["effective_damage_formula"] is None
    assert ids["friendly-fire-patch"]["same_as_TW10_runtime"] is False
    assert ids["new-year-shrine"]["fortune_effect_on_state"] is None
    assert ids["operator-role-attribution"]["unified_company_role"] is None
    assert data["continuation"]["overall_restoration_percent"] is None
    assert data["continuation"]["savedata_r79"]=="PAUSED_NON_BLOCKING"
    assert data["continuation"]["stage_b_and_wiki"]=="GATED"
    return True

if __name__=="__main__":
    assert verify(json.loads(PATH.read_text(encoding="utf-8")))
    print("R110 bounded JP2004 source claims PASS; no original HTML or runtime replay")
