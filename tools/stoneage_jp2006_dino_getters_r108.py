#!/usr/bin/env python3
"""R108 bounded source-metadata guard. Does NOT replay unavailable 2006 HTML."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "research/recovered/STONEAGE-JP2006-DINO-GETTERS-R108.json"
PREFIX = "jp-gaiax-stoneage-2006:r108:"
PROFILE = "LATER_OFFICIAL:JP_GAIAX_STONEAGE_2006_4GAMER_CONTEMPORANEOUS_NOT_EXACT_CLIENT_BUILD"
STATUS = "CONTEMPORANEOUS_PRESS_DESCRIPTION_NOT_OPERATOR_RAW_BYTES_OR_RUNTIME"

def verify(data):
    assert data["schema"] == "stoneage.jp2006.dino_getters.r108"
    assert data["task"] == "OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-108"
    s = data["source"]
    assert s["id"] == "S1"
    assert s["url"] == "https://www.4gamer.net/news/history/2006.05/20060523181644detail.html"
    assert s["article_publication"] == "2006-05-23 18:16"
    assert s["provenance_level"] == "CONTEMPORANEOUS_SECONDARY_PRESS_WEB_RENDER_ONLY_NO_BYTE_REPLAY"
    assert s["actual_raw_html_bytes"] is None
    assert s["actual_raw_html_sha256"] is None
    assert s["exact_historical_capture"] is None
    assert s["operator_original_html"] is None
    assert len(data["records"]) == 4
    a = {r["record_id"][len(PREFIX):]: r for r in data["records"]}
    assert len(a) == 4
    assert set(a) == {"event", "npc-handin", "capture-ranks", "per-server-reward"}
    for r in data["records"]:
        assert r["record_id"].startswith(PREFIX)
        for key in ("record_id","entity_type","collection","version_profile","source_refs",
                    "verification_status","rights_status","record_revision","game_ids"):
            assert key in r, (r.get("record_id"), key)
        assert r["version_profile"] == PROFILE
        assert r["source_refs"] == ["S1"]
        assert r["verification_status"] == STATUS
        assert r["rights_status"] == "RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED"
        assert r["game_ids"] is None
    event, npc, tiers, agg = (a[k] for k in
                                  ("event","npc-handin","capture-ranks","per-server-reward"))
    assert event["collection"] == "quests"
    assert event["event_name_as_written"] == "GMからの挑戦状 ～ダイノ ゲッターズ～"
    assert event["start_date_reported"] == "2006-05-23"
    assert event["end_date_reported"] == "2006-06-06"
    assert event["actual_live_dates_verified"] is False
    assert event["server_script"] is None and event["client_build"] is None
    assert event["npc_service_ref"] == npc["record_id"]
    assert event["rank_ref"] == tiers["record_id"]
    assert event["server_progress_ref"] == agg["record_id"]
    assert npc["collection"] == "npcs" and npc["reported_npc_count"] == 3
    assert npc["location_as_written"] == "カルターナの村"
    assert npc["npc_names_as_written"] == []
    assert npc["npc_original_ids"] is None and npc["coordinates"] is None
    assert npc["dialogue_text"] is None and npc["successful_handoff_observed"] is False
    assert npc["consumes_captured_pet"] is None
    assert tiers["collection"] == "pets"
    assert tiers["tier_names_as_written"] == ["下級","中級","上級"]
    assert tiers["tier_count"] == 3
    assert tiers["capture_ease_and_points_differ_by_tier_reported"] is True
    assert tiers["tier_point_values"] is None
    assert tiers["eligible_species_names"] == []
    assert tiers["species_master_ids"] is None and tiers["catch_probabilities"] is None
    assert agg["collection"] == "quests"
    assert agg["aggregation_scope"] == "SAME_SERVER_ALL_PLAYERS"
    assert agg["claimed_beneficiary_scope"] == "ALL_PLAYERS_ON_SAME_SERVER"
    assert agg["point_target_value"] is None
    assert agg["threshold_comparator_executable"] is None
    assert agg["points_credit_rule"] is None
    assert agg["award_content"] is None and agg["award_distribution_schedule"] is None
    assert agg["observed_total_points"] is None and agg["actual_reward_granted"] is False
    assert agg["npc_service_ref"] == npc["record_id"] and agg["rank_ref"] == tiers["record_id"]
    assert data["continuation"]["next"] == "OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-109"
    assert data["continuation"]["stage_a"] == "7_PARTIAL_2_OPEN"
    assert data["continuation"]["stage_b_and_wiki"] == "GATED"
    assert data["continuation"]["savedata_r79"] == "PAUSED_NON_BLOCKING"
    assert data["continuation"]["overall_restoration_percent"] is None
    return True

if __name__ == "__main__":
    verify(json.loads(PATH.read_text(encoding="utf-8")))
    print("R108: source-bounded Japanese 2006 event metadata PASS (NOT raw-source or runtime replay)")
