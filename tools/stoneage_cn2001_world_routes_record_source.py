"""R96 evidence boundary for 2001 player world routes and record points."""
import hashlib
import json
from pathlib import Path

P=Path(__file__).resolve().parents[1] / "research/recovered/STONEAGE-CN2001-WORLD-ROUTES-RECORD-SOURCE-R96.json"
BLOB_SHA1="e2bc3c5e1dc3eae4ee61b9c6ab85de7cb9f82538"

def git_blob_sha(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode("ascii")+b"\0"+raw).hexdigest()

def verify(data):
    raw=P.read_bytes()
    assert git_blob_sha(raw)==BLOB_SHA1, "immutable R96 source JSON changed"
    assert data==json.loads(raw.decode("utf-8")), "unsourced modification or new fields"
    assert data["schema"]=="stoneage.cn2001_world_routes_record_gates.r96"
    assert data["task"]=="OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-96"
    assert data["scope"]=="2001_17173_MIGRATED_PLAYER_GUIDES_NOT_ORIGINAL_1999_JSS_OR_TW10_MASTER"
    s1,s2=data["sources"]
    assert [s1["id"],s2["id"]]==["R96-S1","R96-S2"]
    assert [s1["page_title"] if "page_title" in s1 else s1["title"], s2["title"]]==["石器之练功篇（一）","石器之练功篇（二）"]
    assert s1["byline"]=="正伟" and s2["byline"] is None
    assert s1["display_date"]==s2["display_date"]=="2001-06-14"
    assert all(x["original_html_authenticated"] is False and x["raw_original_sha256"] is None and x["exact_game_build"] is None for x in data["sources"])
    g=data["geography"]
    assert g["islands"]==["南岛","北岛","沙姆岛","吉鲁岛"]
    assert g["reported_subsea_passages"]==3 and g["passage_endpoints_identified"] is False
    assert g["original_map_ids"] is None and g["actual_geometry_recovered"] is False
    assert [(x["island"],x["name"]) for x in data["birthplaces"]]==[
        ("南岛","加加村"),("南岛","卡鲁它那村"),("北岛","玛丽娜斯渔村"),("北岛","萨姆吉尔村")]
    S,N=data["suggested_routes"]
    assert S["stops"]==["加加村","多多村","乌鲁力村","霍特尔村","沙姆岛奇努伊村","吉鲁岛达那村"]
    assert N["stops"]==["萨姆吉尔村","霍特尔村","沙姆岛奇努伊村","吉鲁岛达那村"]
    assert S["strict_game_gate"] is False and N["strict_game_gate"] is False
    r=data["statue_record_claims"]
    assert len(r)==4
    assert "初次" in r[0]["claim"] and r[0]["original_server_ack"] is False
    assert r[1]["actual_save_reentry_trace"] is False
    assert (r[2]["reported_meat"],r[2]["count"],r[2]["all_statues_same_meat"])==("奇宝的肉",2,False)
    assert r[3]["entire_game_has_no_other_record_points"] is False
    t=data["transport"]
    assert t["pass_price_stones"]==200 and t["pass_location"]=="卡鲁它那村"
    assert t["all_three_passages_same_gate"] is False and t["original_pass_item_id"] is None
    assert t["live_server_transaction_verified"] is False and t["merchant_identity"] is None
    assert [(v["name"],v["element"],v["reported_status"]) for v in data["elemental_caves"]]==[
        ("深红洞窟","火","称已开放"),("玄黄洞窟","地","称已开放"),
        ("琉璃洞窟","风","称已开放"),("碧青洞窟","水","称尚未开放")]
    assert all(v["original_operation_log_verified"] is False for v in data["elemental_caves"])
    assert data["cross_reference"]["r96_no_reimport_of_old_indexed_guide"] is True
    assert data["cross_reference"]["same_version_as_r95_jp2003_verified"] is False
    assert set(data["evidence_guards"].values())=={False}
    assert len(data["unknowns"])==7
    assert data["publication"]=={
        "derived_metadata_only":True,"original_copyright_html_saved":False,
        "original_images_saved":False,"original_client_executed":False,
        "stage_a_closed":False,"stage_b_started":False,"overall_restoration_percent":None,
        "next":"OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-97"}
    return True

if __name__=="__main__":
    verify(json.loads(P.read_text(encoding="utf-8")))
    print("R96 PASS: 2001 four-island text, two routes, record-point claims and dated cave-status assertions remain source bounded")
