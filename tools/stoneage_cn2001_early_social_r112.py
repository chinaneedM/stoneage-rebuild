#!/usr/bin/env python3
"""R112 historical-source boundary checks, not a server or HTML replay."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "research/recovered/STONEAGE-CN2001-EARLY-SOCIAL-R112.json"

def validate(d):
    assert d["schema"] == "stoneage.cn2001.early_social.r112"
    assert d["task"] == "OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-112"
    src = d["sources"]
    assert len(src) == 1 and src[0]["id"] == "S1"
    assert src[0]["url"] == "https://www.shiqi.me/pt_25.htm"
    assert src[0]["webpage_republication_date"] == "2016-02-12"
    assert src[0]["source_rank"] == "LATER_THIRD_PARTY_REPRINT_CLAIMING_VERBATIM_OPERATOR_NOTICES_UNAUTHENTICATED"
    for key in ("original_2001_official_site_url","original_2001_html_capture",
                "original_2001_html_sha256","actual_2016_reprint_html_bytes",
                "actual_2016_reprint_html_sha256"):
        assert src[0][key] is None, key
    assert src[0]["independent_2001_confirmation"] is False
    assert d["version"]["tw10_or_jss1999_identity_proven"] is False
    assert d["version"]["client_build"] is None
    assert d["version"]["original_server_scripts_authenticated"] is False
    e = d["valentine"]
    assert e["notice_announcement_date"] == "2001-02-06"
    assert e["notice_results_date"] == "2001-02-14"
    assert sum(x["winners_per_server_listed"] for x in e["reward_tiers"]) == 10
    assert [t["source_label"] for t in e["reward_tiers"]] == ["玉之骨","黑玉","深翠","纪念奖"]
    assert e["reward_tiers"][-1]["listed_names"] == ["绿玉","青玉","蓝骨","绿骨"]
    assert e["claimed_winner_slots_per_server"] == 10 and e["claimed_listed_server_count"] == 6
    rooms = e["claimed_rooms"]
    assert [(r["server"],r["time"],r["chatroom"]) for r in rooms] == [
       ("世纪互联一","10:00","水星聊天室"),("世纪互联二","12:00","优拉纳聊天室"),
       ("世纪互联三","14:00","天府聊天室"),("世纪互联四","16:00","心宿聊天室"),
       ("世纪互联五","18:00","北极星聊天室"),("世纪互联六","20:00","织女聊天室")]
    assert e["room_event_timezone"] is None and e["server_reward_confirmation"] is None
    assert e["gm_character_name"] is None and e["npc_master_id"] is None
    assert e["usernames_intentionally_not_copied"] is True
    assert e["reward_handoff_sequence"] == [
       "REPORTED_WINNER_VISITS_ASSIGNED_CHATROOM","REPORTED_GM_EXCHANGES_BUSINESS_CARD",
       "REPORTED_GM_CHECKS_IDENTITY","REPORTED_RING_CLAIM"]
    m = d["migration"]
    assert m["notice_date"] == "2001-02-17" and m["planned_date"] == "2001-02-27"
    assert m["source_server"] == "世纪互联1" and m["target_server"] == "世纪互联7"
    assert m["reported_destination_bands"] == ["1-10","16-20","26-30","36-40","46-50","56-60"]
    assert m["reported_remain_bands"] == ["11-15","21-25","31-35","41-45","51-55"]
    assert m["higher_bands_unspecified"] is True
    assert m["claimed_compensation_shibi"] == 1000 and m["compensation_actual_delivery"] is None
    assert m["friend_card_persistence_schema"] is None and m["network_migration_log"] is None
    assert m["not_local_savedata_deduction"] is True
    rec = d["records"]
    assert len(rec) == 5 and len({x["record_id"] for x in rec}) == len(rec)
    assert {x["collection"] for x in rec} == {"social","items"}
    for x in rec:
        assert x["source_refs"] == ["S1"] and x["game_ids"] is None
        assert x["original_game_entity_id"] is None and x["actual_server_execution"] is None
        assert x["visual_identity_verified"] is False
        assert x["rights_status"] == "DERIVED_METADATA_ONLY_NOT_PRODUCTION_ASSET"
    a = d["acceptance"]
    for key in ("runtime_implementation_restored","original_first_party_bytes_restored",
                "proprietary_html_or_images_committed","privacy_sensitive_winner_usernames_committed"):
        assert a[key] is False, key
    assert a["game_total_completion_percentage"] is None
    assert d["next"] == "OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-113"
    return True

if __name__ == "__main__":
    validate(json.loads(DATA.read_text(encoding="utf-8")))
    print("R112 source-boundary metadata: PASS (not historical runtime verification)")
