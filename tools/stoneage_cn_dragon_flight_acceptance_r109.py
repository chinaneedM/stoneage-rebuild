#!/usr/bin/env python3
"""Immutable R109 commit-blob evidence pins; no source-HTML replay."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/"research/recovered/STONEAGE-CN2003-2006-DRAGON-FLIGHT-ACCEPTANCE-R109.json"

def blob_sha(data):
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()

def verify(d, check_local=True):
    assert d["schema"]=="stoneage.cn_dragon_flight.acceptance.r109"
    rr=d["research"]
    assert rr["candidate_research_commit"]=="208b2af542cea42fb5f64ccab1c22e881af1c696"
    assert rr["candidate_accepted_commit"]=="458682ab04e0dcc26ec60e1c24a514165fc18c22"
    assert rr["main_fast_forward_commit"]==rr["candidate_accepted_commit"]
    assert rr["candidate_accepted_tree"]=="b1522092dff569b1dffee77db154e2f67f829066"
    assert rr["compare_ahead"]==3 and rr["compare_behind"]==0
    assert rr["changed_files"]==9 and rr["total_deleted_lines"]==0
    s=d["source_custody"]
    assert len(s["source_page_urls"])==2
    for key in ("original_raw_html_retrieved","original_image_bytes_retrieved","source_byte_replay_performed"):
        assert s[key] is False
    for key in ("source_html_sha256","original_historical_capture","source_zip_digest"):
        assert s[key] is None
    a=d["acceptance"]
    assert len(set(a["candidate_run_ids"]))==11
    assert len(set(a["main_run_ids"]))==12
    assert len(set(a["candidate_run_ids"]+a["main_run_ids"]))==a["unique_runs_expected"]==23
    assert a["candidate_dedicated_run_id"]==40048210484
    assert a["main_dedicated_run_id"]==40048431998
    assert a["candidate_dedicated_job_id"]==120734651861
    assert a["main_dedicated_job_id"]==120735372458
    assert a["candidate_dedicated_run_id"] in a["candidate_run_ids"]
    assert a["main_dedicated_run_id"] in a["main_run_ids"]
    assert a["candidate_expected_completed_success"]==11 and a["main_expected_completed_success"]==12
    assert a["not_raw_html_replay_or_live_server_test"] is True
    pins=d["file_pins"]
    assert len(pins)==9 and len({p["path"] for p in pins})==9
    assert set(d["historical_prefix"]["files"])<= {p["path"] for p in pins}
    assert d["historical_prefix"]["preserved"] is True
    for item in pins:
        assert len(item["git_blob_sha"])==40
        if check_local:
            path=ROOT/item["path"]
            assert path.is_file(),path
            assert blob_sha(path.read_bytes())==item["git_blob_sha"],path
    c=d["continuation"]
    assert c["next"].endswith("-110")
    assert c["stage_a"]=="7_PARTIAL_2_OPEN"
    assert c["stage_b_and_wiki"]=="GATED"
    assert c["savedata_r79"]=="PAUSED_NON_BLOCKING"
    assert c["overall_restoration_percent"] is None
    return True

if __name__=="__main__":
    assert verify(json.loads(PATH.read_text(encoding="utf-8")))
    print("R109 immutable source-uncertainty and nine Git-blob pins: PASS")
