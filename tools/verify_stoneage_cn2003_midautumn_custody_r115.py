#!/usr/bin/env python3
"""R115 permanent derived-data custody: exact Git objects and preserved historical prefixes.
No original copyrighted HTML/JPEG or original-game execution is claimed.
"""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RECEIPT=ROOT/"research/recovered/STONEAGE-CN2003-MIDAUTUMN-CUSTODY-R115.json"
SOURCE=ROOT/"research/recovered/STONEAGE-CN2003-MIDAUTUMN-R115.json"
EXPECTED_HEAD="0d8f6491159adc193372f4df97afae2526af4b61"
EXPECTED_TREE="d9276790bc0b7b974fd3609beafed33c46013db1"
EXPECTED_OLD_MAIN="58387170b956205497ce959b3881a9ff50678e78"
EXPECTED_SOURCE_BLOB="ba8f5caf05e00bcf57da47884c794cbec2cfa15f"
EXPECTED_SOURCE_SHA256="41bb39aaa43d6d112a1f3a00822875954970344d99753b322bec6a7dfcf371f3"
EXPECTED_BLOBS={".github/workflows/stoneage-cn2003-midautumn-r115.yml":"c87f98447ddebda34ae936fdaeae5bb380998eec","docs/CURRENT-STATE.md":"11263d3630c09a2115fe6ae8ab81cf586a813c1d","docs/HISTORICAL-TIMELINE.md":"d1812252bf0a1888944e5720609421b702491989","docs/RESTORATION-ROADMAP-R2.md":"8baf06e2786524f908cf95f822279c6563e61037","docs/SOURCE-REGISTRY.md":"a678ec225069662deb3a110b0ee58cfca5a0db0a","docs/specs/STONEAGE-CN2003-MIDAUTUMN-R115.md":"97e84a26c8d4f225058fb1ef7a9a77801632fabe","research/recovered/STONEAGE-CN2003-MIDAUTUMN-R115.json":"ba8f5caf05e00bcf57da47884c794cbec2cfa15f","tests/test_stoneage_cn2003_midautumn_r115.py":"ca87882c29fc6ab346742dcac7988568127bb156","tools/stoneage_cn2003_midautumn_r115.py":"ada69248fe202f9f96621715a445e1433e5f3ada"}
EXPECTED_PREFIX={"docs/CURRENT-STATE.md":{"bytes":2577712,"git_blob":"0f96b6e70aa83bd26a1dd02e22e7dda9c144a14f"},"docs/HISTORICAL-TIMELINE.md":{"bytes":695183,"git_blob":"3eb4229c102b104d51d983d29e09cb17998f65c6"},"docs/RESTORATION-ROADMAP-R2.md":{"bytes":429143,"git_blob":"e168dac0579a82aea0d96f01f02d9a13dc44bd36"},"docs/SOURCE-REGISTRY.md":{"bytes":990908,"git_blob":"cb00263c710e327242f9e7a5c4633fb041956e29"}}
EXPECTED_CANDIDATE_IDS=[40060490636,40060490647,40060490673,40060490708,40060490709,40060490725,40060490739,40060490743,40060490792,40060490906]
EXPECTED_MAIN_IDS=[40060550927,40060550928,40060550930,40060550945,40060550958,40060550974,40060550987,40060550992,40060551006,40060551022,40060551044,40060551059]

def git_blob_sha(content: bytes)->str:
    return hashlib.sha1(("blob %d\x00"%len(content)).encode("ascii")+content).hexdigest()

def validate(d,root=ROOT):
    assert d["schema"]=="stoneage.cn2003.midautumn.custody.r115"
    assert d["repo"]=="chinaneedM/stoneage-rebuild"
    assert d["original_main_before_r115"]==EXPECTED_OLD_MAIN
    assert d["candidate_final_commit_and_main_head"]==EXPECTED_HEAD
    assert d["candidate_final_tree_and_main_tree"]==EXPECTED_TREE
    assert d["publish_method"]=="NON_FORCE_FAST_FORWARD_WITH_EXPECTED_SHA"
    assert d["changed_file_count"]==9 and d["deleted_file_count"]==0
    assert d["versioned_github_git_blobs"]==EXPECTED_BLOBS
    assert d["preserved_original_docs"]==EXPECTED_PREFIX
    for path,pin in EXPECTED_BLOBS.items():
        content=(root/path).read_bytes()
        assert git_blob_sha(content)==pin, f"Git blob mismatch: {path}"
        if path in EXPECTED_PREFIX:
            old=EXPECTED_PREFIX[path]
            prefix=content[:old["bytes"]]
            assert len(prefix)==old["bytes"]
            assert git_blob_sha(prefix)==old["git_blob"],f"History prefix mismatch: {path}"
    proof=d["source_provenance"]
    assert proof["original_2003_website_html_sha256"] is None
    assert proof["original_2003_operator_html"] is None
    assert proof["original_server_quest_transaction_verified"] is False
    assert proof["original_runtime_sprites"] is None
    assert proof["historical_web_html_bytes_archived"] is False
    assert proof["original_source_ci_zip_sha256"] is None
    assert proof["reason_no_source_zip"]=="NO_BYTE_EXACT_ORIGINAL_HTTP_RESOURCE_ACQUIRED_ONLY_PUBLIC_WEB_TEXT"
    v=d["derived_report_provenance"]
    raw=SOURCE.read_bytes() if root==ROOT else (root/v["json_path"]).read_bytes()
    assert v["json_path"]=="research/recovered/STONEAGE-CN2003-MIDAUTUMN-R115.json"
    assert v["json_sha256"]==EXPECTED_SOURCE_SHA256
    assert hashlib.sha256(raw).hexdigest()==EXPECTED_SOURCE_SHA256
    assert v["json_git_blob_sha"]==EXPECTED_SOURCE_BLOB
    assert v["test_case_count"]==30
    assert v["content_candidate_workflow_run"]==40060300925
    assert v["content_candidate_workflow_job"]==120772126075
    assert v["candidate_final_workflow_runs"]==EXPECTED_CANDIDATE_IDS
    assert v["main_workflow_runs"]==EXPECTED_MAIN_IDS
    assert len(set(EXPECTED_CANDIDATE_IDS+EXPECTED_MAIN_IDS))==22
    assert v["candidate_final_count"]==10 and v["main_count"]==12
    assert v["runs_distinct_and_all_success"] is True
    assert v["main_specific_workflow_run"]==40060550927
    assert v["main_specific_workflow_job"]==120772906615
    assert v["main_specific_workflow_name"]=="Validate R115 CN2003 Mid-Autumn narrative and reward evidence boundary"
    assert v["source_raw_html_replayed"] is False and v["original_server_script_replayed"] is False
    g=d["scope_guards"]
    for k in ("only_archived_2003_cn_media_text","narrative_characters_not_validated_original_npcs",
        "reward_item_ids_unknown","random_reward_probabilities_unknown","no_cross_promotion_to_1999_or_tw10"):
        assert g[k] is True
    assert g["stage_a_systems"]=="7_PARTIAL_2_OPEN"
    assert g["stage_b_wiki"]=="GATED" and g["savedata_r79"]=="PAUSED_NON_BLOCKING"
    assert g["overall_restoration_percentage"] is None
    assert g["next"]=="OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-116"
    return True

if __name__=="__main__":
    assert validate(json.loads(RECEIPT.read_text(encoding="utf-8")))
    print("R115 full-prefix, nine Git blobs, SHA256 and dual Actions custody PASS")
