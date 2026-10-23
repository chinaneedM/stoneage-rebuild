"""R95 evidence-only 2003 JP revival trade-window/map/character boundary."""
import hashlib
import json
from pathlib import Path

P=Path(__file__).resolve().parents[1] / "research/recovered/STONEAGE-JP2003-REVIVAL-TRADE-MAP-SOURCE-R95.json"
PINNED_SHA1="c491542dbeb7523169615482bfbfefff728ea9f5"

def _sha(data):
    return hashlib.sha1(b"blob "+str(len(data)).encode("ascii")+b"\0"+data).hexdigest()

def verify(data):
    raw=P.read_bytes()
    assert _sha(raw)==PINNED_SHA1, "source-derived immutable Git blob drift"
    assert data==json.loads(raw.decode("utf-8")), "unexpected mutation or new source claim"
    assert set(data)=={"schema","task","source_scope","source_category","sources","claims",
        "ordered_announcement_dates","cross_reference","version_promotion_guards",
        "material_gaps","source_assets","acceptance"}
    assert data["schema"]=="stoneage.jp2003_revival_prebeta_ui_map_source.r95"
    assert data["task"]=="OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-95"
    assert data["source_scope"]=="JP_2003_BOTHTEC_NHN_REVIVAL_PRESS_PREVIEW_NOT_1999_JSS_RUNTIME_NOT_TW10"
    assert data["source_category"]=="CONTEMPORARY_PRESS_REPORTED_CLAIMS_NOT_EXECUTED_SERVER_TRACE"
    ss=data["sources"]
    assert [x["id"] for x in ss]==["R95-S1","R95-S2","R95-S3"]
    assert [x["displayed_date"] for x in ss]==[
        "2003-07-26 00:18","2003-11-25 20:35","2003-12-12 00:00"]
    assert all(not s["raw_html_bytes_authenticated"] and s["original_html_sha256"] is None
               and s["original_build_sha"] is None for s in ss)
    cl=data["claims"]
    assert [x["id"] for x in cl]==["R95-C%02d"%i for i in range(1,8)]
    assert [x["topic"] for x in cl]==["historical_product_lineage","planned_version_delta",
        "editorial_speculation","beta_window_change","prelaunch_download",
        "trade_window_ui","postbeta_world_avatar_plan"]
    assert all(c["runtime_proven"] is False for c in cl)
    assert cl[2]["reported_state"]=="REPORTER_HYPOTHESIS"
    assert cl[3]["reported_state"]=="REVISED_SCHEDULE_ANNOUNCEMENT"
    assert cl[5]["reported_state"]=="REPORTED_ADDITION_NOT_SCREEN_EXECUTION"
    assert cl[6]["reported_state"]=="LATER_UPDATE_PLAN_NOT_BETA_DEPLOYMENT"
    assert [(r["reported"],r["precision"]) for r in data["ordered_announcement_dates"]]==[
        ("2003-11","MONTH_ONLY"),("2003-12","MONTH_ONLY"),("2003-12-16","DAY")]
    ref=data["cross_reference"]
    assert ref["existing_git_blob_sha1"]=="63b274f5bc8e1508eb1e8f9dfe2a1e27544ea093"
    assert ref["gallery_images_labeled_in_development"] is True
    assert ref["existing_actual_first_two_jpeg_restored_in_R63"] is True
    assert ref["trade_window_observable_in_first_two_R63_frames"] is False
    assert ref["full_trade_transaction_trace_recovered"] is False
    assert ref["gallery_extra_images_fetched_in_R95"] is False
    assert all(v is False for v in data["version_promotion_guards"].values())
    assert len(data["version_promotion_guards"])==13
    assert len(data["material_gaps"])==6
    assert data["source_assets"]=={
        "original_html_saved_in_git":False,"original_screenshots_copied":False,
        "original_client_binary_saved":False,"derived_metadata_only":True}
    assert data["acceptance"]=={"stage_a_accepted":False,"stage_b_started":False,
        "public_wiki_open":False,"overall_restoration_percentage":None,
        "next":"OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-96"}
    return True

if __name__=="__main__":
    verify(json.loads(P.read_text(encoding="utf-8")))
    print("R95 PASS: 2003 press delta only; beta/1999 original game not executed")
