#!/usr/bin/env python3
"""R111 immutable Git file-identity and negative source provenance receipt validator."""
from pathlib import Path
import json, hashlib
ROOT=Path(__file__).resolve().parents[1]
RECEIPT=ROOT/"research/recovered/STONEAGE-JP2009-MYSTERY-DUNGEON-ACCEPTANCE-R111.json"
EXPECTED={
".github/workflows/verify-stoneage-jp2009-mystery-r111.yml":"1d46f80dbc600686eeaa0688965d8c89d394f74e",
"docs/CURRENT-STATE.md":"ea98fd0b4ea031cc69a3a32cb68e108651395bef",
"docs/HISTORICAL-TIMELINE.md":"26d2231eedafa2922d2da30f8c2752546dcf9735",
"docs/RESTORATION-ROADMAP-R2.md":"e449fd480a63a865ceafd70506d18219b4e0b568",
"docs/SOURCE-REGISTRY.md":"d81be0454ac2b05f753f91d971cade53d287e4bd",
"docs/specs/STONEAGE-JP2009-MYSTERY-DUNGEON-R111.md":"798c5ac1edaf9c21770cb2219c348ade6f940407",
"research/recovered/STONEAGE-JP2009-MYSTERY-DUNGEON-R111.json":"359cd848ac91430595e255b327d7fd61e6c67dcc",
"tools/stoneage_jp2009_mystery_dungeon_r111.py":"33ad2ab1e26cfad672df89caa2e40c157a3874fc",
"tests/test_stoneage_jp2009_mystery_dungeon_r111.py":"b85581d54c11242ad5034691c7676b0c020bd4c6"
}
def git_hash(content):
    return hashlib.sha1(b"blob "+str(len(content)).encode()+b"\0"+content).hexdigest()
def verify(d, inspect_files=True):
    assert d["schema"]=="stoneage.jp2009.mystery_dungeon.acceptance.r111"
    assert d["repository"]=="chinaneedM/stoneage-rebuild"
    c=d["content"]
    assert c["start_main_head"]=="554a0ec1ab53823496eee75ebe8f8c58ef7f4efb"
    assert c["initial_source_commit"]=="5ee78dc02cac14b407ce099f54ccdc4a8fc6356e"
    assert c["integrated_commit"]=="549a3c82bf1121259fe6cb50bee7437ebe997aaf"
    assert c["integrated_tree"]=="f58c08c983d79ce422568e54659c7b25091ff9e6"
    assert c["candidate_merge_ahead"]==3 and c["candidate_merge_behind"]==0
    assert c["changed_file_count"]==9 and c["deleted_lines"]==0
    assert c["published_to_main"] is True and c["four_history_full_old_prefixes_preserved"] is True
    ci=d["ci"]
    assert ci["candidate_source_only_run"]=={"id":40051427341,"head":"5ee78dc02cac14b407ce099f54ccdc4a8fc6356e","job_id":120744747526,"status":"completed","conclusion":"success"}
    assert ci["candidate_final"]["head"]==c["integrated_commit"]
    assert ci["main_final"]["head"]==c["integrated_commit"]
    assert len(ci["candidate_final"]["runs"])==10 and ci["candidate_final"]["run_count"]==10
    assert len(ci["main_final"]["runs"])==12 and ci["main_final"]["run_count"]==12
    assert ci["main_final"]["source_specific_run"]==40051647303
    assert ci["main_final"]["source_specific_job_id"]==120745408273
    assert ci["distinct_run_count_including_initial_source_ci"]==23
    assert len(set(ci["candidate_final"]["runs"]+ci["main_final"]["runs"]+[ci["candidate_source_only_run"]["id"]]))==23
    assert ci["candidate_final"]["conclusion"]=="success" and ci["main_final"]["conclusion"]=="success"
    assert ci["acceptance_run_status_observed_through_remote_api"] is True
    assert ci["actual_original_2009_webpage_fetched_by_ci"] is False
    assert ci["actual_game_runtime_executed_by_ci"] is False
    assert d["files"]["type"]=="exact_git_blob_sha1"
    assert d["files"]["pins"]==EXPECTED
    if inspect_files:
        for name,expected in EXPECTED.items():
            assert git_hash((ROOT/name).read_bytes())==expected, name
    h=d["history_prefixes"]
    assert set(h)=={"docs/CURRENT-STATE.md","docs/HISTORICAL-TIMELINE.md","docs/RESTORATION-ROADMAP-R2.md","docs/SOURCE-REGISTRY.md"}
    for p,v in h.items():
        assert v["exact_prefix"] is True
        assert v["old_blob"]!=v["new_blob"]
        assert v["new_blob"]==EXPECTED[p]
        assert v["old_char_count"]>100000 and v["appended_char_count"]>0
    s=d["source_custody"]
    assert s["source_url"]=="https://www.4gamer.net/games/013/G001377/20091019025/"
    assert s["source_rank"]=="CONTEMPORARY_PUBLISHER_PRESS_TEXT_REPRODUCED_AT_4GAMER"
    for k in ("actual_2009_original_html_sha256","actual_current_html_sha256","original_2009_archive_capture","thumbnail_local_jpeg_sha256","ci_source_zip_digest","ci_source_raw_replay_digest"):
        assert s[k] is None
    assert s["original_media_material_archived_to_git"] is False
    assert s["server_script_or_rewards_verified"] is False
    assert s["provenance_quality"]=="TEXT_ONLY_SOURCE_ASSERTIONS_WITH_PERMANENT_DERIVED_GIT_BLOBS"
    z=d["continuation"]
    assert z["next"]=="OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-112"
    assert z["stage_a"]=="7_PARTIAL_2_OPEN" and z["stage_b_and_wiki"]=="GATED"
    assert z["savedata_r79"]=="PAUSED_NON_BLOCKING" and z["overall_restoration_percent"] is None
    return True
if __name__=="__main__":
    assert verify(json.loads(RECEIPT.read_text(encoding="utf-8")))
    print("R111 Git-blob receipt PASS (remote Actions observed, original source bytes absent)")
