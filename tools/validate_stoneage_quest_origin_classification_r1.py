#!/usr/bin/env python3
"""Quest-origin archival overlay guard. Checks document boundaries, not original server behavior."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FILE=ROOT/"research/recovered/STONEAGE-QUEST-ORIGIN-SEPARATION-R1.json"
PIN={
"R110":("OPERATOR_EVENT_QUEST","EVENT_ACTIVITY_CLAIM","eb22c2c7b918088e386f5fea90104549c81a6183"),
"R111":("OPERATOR_EVENT_QUEST","EVENT_QUEST_CLAIM","359cd848ac91430595e255b327d7fd61e6c67dcc"),
"R112":("OPERATOR_EVENT_QUEST","EVENT_ACTIVITY_CLAIM","77149e798d11976ccb0fa9bffdff7bc7cab1f835"),
"R115":("OPERATOR_EVENT_QUEST","EVENT_QUEST_CLAIM","ba8f5caf05e00bcf57da47884c794cbec2cfa15f"),
"R114":("ORIGIN_UNRESOLVED","QUEST_CLAIM","1fb238ea9352adc2e144529b1ef5bd6d5765bb13"),
"R113":("ORIGIN_UNRESOLVED","STORY_AND_QUEST_CLAIM","a753fe2416d1209929d9e3e5a49c7d55a3c04ad7"),
}
def validate(d,check_repository=True):
    assert d["schema"]=="stoneage.quest_origin_separation.r1"
    assert d["baseline"]=={"head":"d25080929a8839838c07aa3bcb8744d17f99278c","tree":"4771baebbb6f139b864dfa9397f53bb2cbc2e652"}
    p=d["policy"]
    assert p["categories"]==["BASE_GAME_QUEST","PERMANENT_VERSION_QUEST","OPERATOR_EVENT_QUEST","ORIGIN_UNRESOLVED"]
    assert p["separate_material_views"]==["game_base_quests","version_permanent_quests","operator_event_quests_and_activities","unresolved_origin"]
    for key in ("event_archive_is_not_baseline_quest","source_claim_is_not_actual_server_execution",
                "release_time_is_not_worldline_time","cross_region_name_is_not_same_entity",
                "festival_theming_alone_not_sufficient_to_prove_duration",
                "event_reward_may_persist_after_event_without_quest_becoming_base_game",
                "not_every_operator_activity_is_a_playable_quest",
                "original_history_records_preserved_without_inplace_mutation"):
        assert p[key] is True
    assert set(p["requirements"])==set(p["categories"])
    assert len(d["records"])==6
    ids=[x["id"] for x in d["records"]]
    assert len(set(ids))==6 and set(ids)==set(PIN)
    for r in d["records"]:
        origin,kind,sha=PIN[r["id"]]
        assert r["origin"]==origin and r["record_kind"]==kind
        assert r["source_git_blob"]==sha
        assert r["source"].startswith("research/recovered/STONEAGE-")
        assert r["origin_evidence"] and r["version"] and r["region"] and r["operator"]
        assert r["baseline_core_admission"] is False
        assert r["is_event_archive"] is (origin=="OPERATOR_EVENT_QUEST")
        if origin=="ORIGIN_UNRESOLVED": assert r["event_window"] is None
        if r["id"]=="R115": assert r["event_window"] is None
        if check_repository:
            f=ROOT/r["source"]
            assert f.is_file(),r["source"]
            import hashlib
            raw=f.read_bytes()
            git_hash=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
            assert git_hash==sha,(r["id"],git_hash)
    assert d["base_game_quest_entries_verified_this_overlay"]==0
    assert d["permanent_version_quest_entries_verified_this_overlay"]==0
    assert d["contains_any_new_original_runtime_quest_ids"] is False
    assert d["current_source_reports_immutable"] is True
    assert d["global_restoration_percent"] is None
    assert d["next_queue"]=="OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-116"
    return True
if __name__=="__main__":
    assert validate(json.loads(FILE.read_text(encoding="utf-8")))
    print("quest origin overlay R1 PASS (six immutable source blobs)")
