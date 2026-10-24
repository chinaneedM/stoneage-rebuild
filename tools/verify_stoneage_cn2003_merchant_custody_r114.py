#!/usr/bin/env python3
"""Verify R114 immutable Git source custody; not a proof of the original game."""
import json
import subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"research/recovered/STONEAGE-CN2003-MERCHANT-ELEPHANT-ACCEPTANCE-R114.json"
HISTORICAL={
"docs/CURRENT-STATE.md":"e5eba6014658de032edb5e348643bb6b26b134c9",
"docs/HISTORICAL-TIMELINE.md":"d940a51ab2b616e7f50af44b1e3671bc1911213d",
"docs/RESTORATION-ROADMAP-R2.md":"85b4f7681e08cb19167e0c7306e609ffb87f48ab",
"docs/SOURCE-REGISTRY.md":"6b7de5b20e11a46330ee34a365b29ea78d1b8a9c"}
NINE={
".github/workflows/stoneage-cn2003-merchant-elephant-r114.yml":"93b9ff49050f0b4e2525466dea02a1b303f28135",
"docs/CURRENT-STATE.md":"12dca26bd907c73edc94415bdacefa678133263a",
"docs/HISTORICAL-TIMELINE.md":"3eb4229c102b104d51d983d29e09cb17998f65c6",
"docs/RESTORATION-ROADMAP-R2.md":"2b32106ec77e3e5a0c9d9cfba31b92f60826bca8",
"docs/SOURCE-REGISTRY.md":"cb00263c710e327242f9e7a5c4633fb041956e29",
"docs/specs/STONEAGE-CN2003-MERCHANT-ELEPHANT-R114.md":"616491c19221c3e66a2876c33e54609ad09a047b",
"research/recovered/STONEAGE-CN2003-MERCHANT-ELEPHANT-R114.json":"1fb238ea9352adc2e144529b1ef5bd6d5765bb13",
"tests/test_stoneage_cn2003_merchant_elephant_r114.py":"7b557f46b118731a2d03f717df87e8b8098e6e4d",
"tools/stoneage_cn2003_merchant_elephant_r114.py":"0812334029645c5fc04e57891e3ab781ad55c781"}
HEAD="aac31addabbaf8ac23bd7df8488c8679a63ae57d"
TREE="e1bffd75587400de747ab6f755f273cdec188e86"
PARENT="33091550d0a2beed10e2bccfe8d97b0ff765080a"

def git(*args):
    return subprocess.check_output(["git", *args],cwd=ROOT)

def validate(d,check_git=False):
    assert d["schema"]=="stoneage.r114.nine_file_git_custody.receipt.r1"
    assert d["repo"]=="chinaneedM/stoneage-rebuild"
    assert d["content_head"]==HEAD and d["content_tree"]==TREE
    assert d["previous_main_head"]==PARENT
    assert d["candidate_content_commit"]=="0f468798056679a39324975bb6578c3f27e512cb"
    assert d["continuity_commit"]==HEAD
    assert d["candidate_content_ci"]["run_id"]==40055929518
    assert d["candidate_content_ci"]["job_id"]==120758795903
    assert d["candidate_content_ci"]["conclusion"]=="success"
    assert d["candidate_content_ci"]["head_sha"]==d["candidate_content_commit"]
    assert d["main_content_ci"]["run_id"]==40056110228
    assert d["main_content_ci"]["job_id"]==120759341359
    assert d["main_content_ci"]["conclusion"]=="success"
    assert d["main_content_ci"]["head_sha"]==HEAD
    nine=d["nine_files"]
    assert len(nine)==9 and len({x["path"] for x in nine})==9
    assert {x["path"]:x["blob_sha"] for x in nine}==NINE
    assert {x["path"]:x["existing_historical_prefix_blob"] for x in nine if x["path"] in HISTORICAL}==HISTORICAL
    assert all(x["existing_historical_prefix_blob"] is None for x in nine if x["path"] not in HISTORICAL)
    assert d["zero_deletions_in_remote_compare"] is True
    assert d["all_previous_historical_prefixes_byte_preserved"] is True
    for field,branch,count in [
      ("candidate_continuity_actions","agent/cn2003-merchant-elephant-r114-20261024",10),
      ("main_content_actions","main",12)]:
        runs=d[field]
        assert len(runs)==count and len({r["run_id"] for r in runs})==count
        assert runs==sorted(runs,key=lambda x:x["run_id"])
        assert all(r["head_branch"]==branch and r["head_sha"]==HEAD for r in runs)
        assert all(r["status"]=="completed" and r["conclusion"]=="success" and r["run_id"]>0 and r["url"].startswith("https://github.com/") for r in runs)
    assert d["main_content_ci"]["run_id"] in {r["run_id"] for r in d["main_content_actions"]}
    p=d["provenance_limit"]
    for key in ("original_2003_html_sha256","original_quest_images_sha256","original_client_build","original_server_execution_proof","restore_percentage"):
        assert p[key] is None
    assert p["real_capture_cargo_and_loyalty_transaction_proven"] is False
    assert p["html_or_pixels_archived_in_git"] is False
    assert p["original_game_entity_count_newly_recovered"]==0
    assert d["receipt_role"]=="EXACT_DERIVED_GIT_BLOBS_AND_CI_ACCEPTANCE_NOT_ORIGINAL_GAME_EXECUTION"
    assert d["highest_next"]=="OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-115"
    if check_git:
        assert git("rev-parse",HEAD+"^{tree}").decode().strip()==TREE
        for path,sha in NINE.items():
            assert git("rev-parse",HEAD+":"+path).decode().strip()==sha,(path,"blob mismatch")
        for path,sha in HISTORICAL.items():
            assert git("rev-parse",PARENT+":"+path).decode().strip()==sha,(path,"old SHA")
            old=git("show",PARENT+":"+path)
            new=git("show",HEAD+":"+path)
            assert len(new)>len(old) and new.startswith(old),(path,"history prefix lost")
    return True

if __name__=="__main__":
    assert validate(json.loads(DATA.read_text(encoding="utf-8")),check_git=True)
    print("R114 all nine Git blobs, four full historical prefixes and CI receipt PASS")
