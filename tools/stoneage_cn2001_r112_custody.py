#!/usr/bin/env python3
"""Independently replay R112 exact Git blob custody (NOT 2001 HTML or game runtime)."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "research/recovered/STONEAGE-CN2001-EARLY-SOCIAL-ACCEPTANCE-R112.json"

def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)

def check():
    o=json.loads(PATH.read_text(encoding="utf-8"))
    assert o["schema"] == "stoneage.cn2001.early_social.acceptance.r112"
    c=o["content"]; ci=o["ci"]; custody=o["source_custody"]
    assert c["integrated_commit"] == o["files"]["at_integrated_commit"]
    assert c["published_to_main"] is True
    assert c["candidate_merge_ahead"] == 2 and c["candidate_merge_behind"] == 0
    assert c["changed_file_count"] == 9 and c["deleted_lines"] == 0
    assert c["four_history_full_old_prefixes_preserved"] is True
    tree=git("rev-parse",c["integrated_commit"]+"^{tree}").decode().strip()
    assert tree == c["integrated_tree"],"wrong integrated tree"
    pins=o["files"]["pins"]
    assert len(pins) == 9
    assert set(pins) == {
        ".github/workflows/stoneage-cn2001-early-social-r112.yml",
        "docs/CURRENT-STATE.md","docs/HISTORICAL-TIMELINE.md",
        "docs/SOURCE-REGISTRY.md","docs/RESTORATION-ROADMAP-R2.md",
        "docs/specs/STONEAGE-CN2001-EARLY-SOCIAL-R112.md",
        "research/recovered/STONEAGE-CN2001-EARLY-SOCIAL-R112.json",
        "tools/stoneage_cn2001_early_social_r112.py",
        "tests/test_stoneage_cn2001_early_social_r112.py"
    }
    for path,sha in sorted(pins.items()):
        actual=git("rev-parse",f'{c["integrated_commit"]}:{path}').decode().strip()
        assert sha == actual,(path,sha,actual)
        assert git("cat-file","-t",sha).strip() == b"blob"
    assert len(o["history_prefixes"]) == 4
    for path,record in o["history_prefixes"].items():
        assert record["new_blob"] == pins[path] and record["exact_prefix"] is True
        before=git("cat-file","blob",record["old_blob"]).decode("utf-8")
        after=git("cat-file","blob",record["new_blob"]).decode("utf-8")
        assert after.startswith(before),path
        assert len(before) == record["old_char_count"],path
        assert len(after)-len(before) == record["appended_char_count"],path
    assert ci["candidate_source_only_run"]["conclusion"] == "success"
    assert ci["candidate_source_only_run"]["head"] == c["initial_source_commit"]
    assert len(ci["candidate_final"]["runs"]) == ci["candidate_final"]["run_count"] == 10
    assert len(ci["main_final"]["runs"]) == ci["main_final"]["run_count"] == 12
    allruns=ci["candidate_final"]["runs"]+ci["main_final"]["runs"]+[ci["candidate_source_only_run"]["id"]]
    assert len(set(allruns)) == len(allruns) == ci["distinct_run_count_including_initial_source_ci"] == 23
    assert ci["main_final"]["source_specific_run"] in ci["main_final"]["runs"]
    assert ci["actual_original_2001_webpage_fetched_by_ci"] is False
    assert ci["actual_game_runtime_executed_by_ci"] is False
    for name in ("actual_2001_original_html_sha256","actual_current_2016_reprint_html_sha256",
                 "original_2001_archive_capture","ci_source_zip_digest","ci_raw_html_replay_digest"):
        assert custody[name] is None,name
    assert custody["operator_notice_text_authenticated_to_2001"] is False
    assert custody["server_delivery_or_migration_verified"] is False
    assert custody["original_copyrighted_html_or_player_names_committed"] is False
    assert o["continuation"]["overall_restoration_percent"] is None
    print("R112 exact 9 Git blobs / 4 full history prefixes / 23 observed CI runs: PASS")
    print("Original 2001 HTML, server execution, actual reward/migration: NOT VERIFIED")
    return True

if __name__ == "__main__":
    check()
