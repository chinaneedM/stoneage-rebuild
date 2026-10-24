#!/usr/bin/env python3
"""R110 immutable Git blob checks; never claims original 2004 bytes or server replay."""
import json
import subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/"research/recovered/STONEAGE-JP2004-XMAS-PARTY-COMBAT-ACCEPTANCE-R110.json"

EXPECTED={
    ".github/workflows/verify-stoneage-jp2004-xmas-r110.yml": "351d88069d068e98803cfe4a3f03b9f5ad33ede5",
    "docs/CURRENT-STATE.md": "52ebf1b7447be49a5f9cd9705b72ac4b7b959f2d",
    "docs/HISTORICAL-TIMELINE.md": "1c293af9f8aa43b65c24e5dd234a277f492a6356",
    "docs/RESTORATION-ROADMAP-R2.md": "e6faa544e07468b10ce7b9a457915789235e055d",
    "docs/SOURCE-REGISTRY.md": "91637151358411b49519077f8d0bb7fa72b4bf89",
    "docs/specs/STONEAGE-JP2004-XMAS-PARTY-COMBAT-R110.md": "0e91012445f246597ce441fe6db9f8d9d302c8ee",
    "research/recovered/STONEAGE-JP2004-XMAS-PARTY-COMBAT-R110.json": "eb22c2c7b918088e386f5fea90104549c81a6183",
    "tests/test_stoneage_jp2004_xmas_party_r110.py": "e8adfc2399609c1039a7eaea15d8a71601f7c748",
    "tools/stoneage_jp2004_xmas_party_r110.py": "85f8722ade91d08ced0f983a100906aa438b372b",
}
CANDIDATE=[40050097867,40050098085,40050097924,40050098010,40050097979,40050098063,40050097985,40050098048,40050098033,40050098055]
MAIN=[40050164106,40050164119,40050164006,40050163982,40050163956,40050163822,40050164095,40050164128,40050164117,40050163757,40050164069,40050163703]

def verify(d, check_worktree=False):
    assert d["schema"]=="stoneage.jp2004.xmas_party_custody.r110"
    assert d["evidence_class"]=="DERIVED_METADATA_AND_GITHUB_ACTIONS_CUSTODY_NO_HISTORICAL_SOURCE_BYTES"
    assert d["content_main_commit"]=="e2d272115c0aa6b27b87b44a22f6481f3dea699a"
    assert d["content_git_tree"]=="0abd564cc7fd47ac07fee77792bf4d9e92b00850"
    assert d["content_files_git_blob_sha"]==EXPECTED
    assert d["content_files_count"]==len(EXPECTED)==9
    for field,n,ids in (("candidate_latest_commit_suite",10,CANDIDATE),("main_content_suite",12,MAIN)):
        record=d[field]
        assert record["head_sha"]==d["content_main_commit"]
        assert record["run_count"]==n and record["run_ids"]==ids and len(set(ids))==n
        assert record["all_status"]=="completed" and record["all_conclusion"]=="success"
    g=d["bounded_source_guard"]
    assert g["candidate_source_run_id"]==40049979655
    assert g["candidate_source_job_id"]==120740292094
    assert g["main_source_run_id"]==40050164006
    assert g["main_source_job_id"]==120740842371
    assert g["main_source_head"]==d["content_main_commit"]
    assert g["observed_test_count"]==21
    assert g["code_status"]=="COMPLETED_SUCCESS_METADATA_ONLY"
    s=d["source_provenance"]
    assert s["first_media_url"]=="https://www.4gamer.net/news/history/2004.12/20041215210314detail.html"
    assert s["second_media_url"]=="https://game.watch.impress.co.jp/docs/20041224/on1224.htm"
    assert s["original_operator_page"]=="http://stoneage.to/event/Xmas04.html"
    for x in ("operator_page_retrieved","original_image_recovered","source_replay_performed","original_server_activity_verified"):
        assert s[x] is False
    for x in ("original_html_raw_sha256","original_raw_bytes","historical_capture_sha256"):
        assert s[x] is None
    for x in ("raw_source_artifact_id","source_artifact_zip_sha256","source_raw_json_sha256"):
        assert d["artifact_custody"][x] is None
    assert d["history_integrity"]["four_existing_long_files_were_appended_not_replaced"] is True
    assert d["history_integrity"]["non_force_merge"] is True
    assert d["history_integrity"]["compare_ahead"]==3 and d["history_integrity"]["compare_behind"]==0
    assert d["history_integrity"]["changed_paths"]==9
    assert d["historical_status"]["restoration_percent"] is None
    assert d["historical_status"]["stage_b_and_wiki"]=="GATED"
    if check_worktree:
        for path,expected in EXPECTED.items():
            p=ROOT/path
            assert p.is_file(), path
            got=subprocess.check_output(["git","hash-object",str(p)],cwd=ROOT,text=True).strip()
            assert got==expected,(path,got,expected)
    return True

if __name__=="__main__":
    verify(json.loads(PATH.read_text(encoding="utf-8")),True)
    print("R110 provenance custody PASS, 9 git blobs intact; original HTML/runtime remains UNVERIFIED")
