#!/usr/bin/env python3
"""Exact R113 content-custody receipt verification. Requires full git history."""
import json
import subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/recovered/STONEAGE-CN25-SPIRIT-KING-STORY-ACCEPTANCE-R113.json"
def git(*args):
    return subprocess.check_output(["git",*args],cwd=ROOT)
def verify():
    q=json.loads(REPORT.read_text(encoding="utf-8"))
    assert q["schema"]=="stoneage.cn25.spirit_king_story.acceptance.r113"
    assert q["source_content"]["document_commit"]=="292c6f278659b5dccb553b6bf806b6142896da9b"
    assert q["source_content"]["changed_files"]==9 and q["source_content"]["lines_deleted"]==0
    assert q["candidate_ci"]["initial_source_run"]["conclusion"]=="success"
    assert q["candidate_ci"]["status"]=="completed" and q["candidate_ci"]["conclusion"]=="success"
    assert q["main_ci"]["head_sha"]==q["source_content"]["document_commit"]
    assert q["main_ci"]["status"]=="completed" and q["main_ci"]["conclusion"]=="success"
    assert len(q["candidate_ci"]["run_ids"])==10 and len(q["main_ci"]["run_ids"])==12
    assert len(set([q["candidate_ci"]["initial_source_run"]["id"]]+q["candidate_ci"]["run_ids"]+q["main_ci"]["run_ids"]))==23
    assert q["distinct_actions_count"]==23
    assert q["provenance"]["original_publisher_html_sha256"] is None
    assert q["provenance"]["actual_current_media_html_sha256"] is None
    assert q["provenance"]["original_client_or_server_replay"] is False
    assert q["provenance"]["source_zip_artifact_sha256"] is None
    assert q["ci_original_source_html_replayed"] is False and q["ci_original_server_runtime_replayed"] is False
    assert q["provenance"]["source_42_is_duplicate_of_39_character_excerpt"] is True
    assert q["boundaries"]["dark_king_seal_conflict_preserved"] is True
    assert q["boundaries"]["feng_feng_orthography_conflict_preserved"] is True
    assert q["boundaries"]["old_2001_black_jade_identity_not_joined"] is True
    assert q["boundaries"]["aggregate_restoration_percentage"] is None
    assert q["next"]=="OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-114"
    target=q["source_content"]["document_commit"]
    assert git("rev-parse",f"{target}^{{tree}}").decode().strip()==q["source_content"]["document_tree"]
    blobs=q["verified_tree"]["blob_pins"]
    assert len(blobs)==9
    for path,sha in blobs.items():
        assert git("rev-parse",f"HEAD:{path}").decode().strip()==sha, path
        assert git("rev-parse",f"{target}:{path}").decode().strip()==sha, path
    for e in q["history_prefixes"]:
        old=git("show",f"{q['source_content']['base_main_head']}:{e['path']}")
        new=git("show",f"HEAD:{e['path']}")
        assert len(new)>len(old) and new.startswith(old), e["path"]
        assert old.decode("utf-8").__len__()==e["old_chars"]
        assert new.decode("utf-8").__len__()==e["new_chars"]
        assert git("rev-parse",f"{q['source_content']['base_main_head']}:{e['path']}").decode().strip()==e["old_blob"]
        assert git("rev-parse",f"HEAD:{e['path']}").decode().strip()==e["new_blob"]
    assert git("rev-parse",f"HEAD:research/recovered/STONEAGE-CN25-SPIRIT-KING-STORY-R113.json").decode().strip()==blobs["research/recovered/STONEAGE-CN25-SPIRIT-KING-STORY-R113.json"]
    print("R113 permanently verified nine source-derived Git blobs, 4 full prefixes and CI receipts; historical original/source runtime remain OPEN")
    return True
if __name__=="__main__":verify()
