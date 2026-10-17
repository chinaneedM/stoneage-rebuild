"""Fail-closed Stage A historical-source feasibility packet validator.

This module verifies documented source custody and prohibited provenance
promotions; it does not execute StoneAge or test original-server absence.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/recovered/STONEAGE-STAGE-A-EARLY-SOURCE-GAP-TRIAGE-R1.json"
SOURCES = {
    "journey": ("research/recovered/STONEAGE-EARLY-VILLAGE-SERVICE-JOURNEY-R1.json","7b6c724999e52a421af77d8c8e1e9351288e11ff"),
    "manual": ("research/recovered/STONEAGE-EARLY-CONTENT-GUIDE-MANUAL-R1.json","54404a8118f125a9a53eabbb8bad8c4a0d07b190"),
    "review": ("docs/STAGE-A-CONSOLIDATED-REVIEW-R1.md","07c9950a40d110d4dabb80b11412db8b4ea64ba9"),
}
IDS = ("SAVE_POINT","MAMMOTH_BUS","VILLAGE_CARE_TRAINING","VILLAGE_WORK","GROUND_ITEM_EXPIRY")
NO_PROMOTION = ("original_1999_membership_proven","original_tw10_same_build_service_execution_proven",
    "commercial_server_durable_ack_proven","original_map_npc_item_reward_acquired",
    "original_client_executed_this_package","original_server_executed_this_package",
    "whole_stage_a_accepted","stage_b_started","production_engine_work_started")
def require(ok, msg):
    if not ok:
        raise ValueError(msg)
def blob_sha(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
def validate(data):
    require(data["schema"]=="stoneage.stage_a_early_source_gap_triage.r1", "wrong schema")
    require(data["task"]=="STAGE-A-EARLY-SOURCE-GAP-TRIAGE-01", "scope changed")
    require(data["scope"]=="FIVE_ALREADY_SOURCE_QUALIFIED_FIRST_PARTY_VILLAGE_SERVICES_ONLY","expanded audit")
    require(data["family_gates"]=={"PARTIAL":7,"OPEN":2}, "stage families promoted")
    require(data["player_flow_profiles"]==7 and data["material_blockers"]==5,"review matrix changed")
    for key in NO_PROMOTION:
        require(data[key] is False, "unsupported historical promotion: "+key)
    require(data["overall_restoration_percentage"] is None, "invented overall percent")
    require(data["r79"]=="PAUSED_NON_BLOCKING","unsanctioned savedata work")
    require(data["unsupported_history_assertions"]==[], "unsupported historical assertions")
    for key,(path,sha) in SOURCES.items():
        require(data["source_pins"][key]=={"path":path,"blob":sha}, "pin changed: "+key)
        require(blob_sha((ROOT/path).read_bytes())==sha, "source custody failed: "+key)
    journey=json.loads((ROOT/SOURCES["journey"][0]).read_text(encoding="utf-8"))
    require([x["service_id"] for x in journey["services"]]==list(IDS),"source services changed")
    require(journey["original_1999_or_tw10_service_identity_proven"] is False,
            "old source provenance invalid")
    gaps=data["gaps"]
    require(len(gaps)==5 and [x["id"] for x in gaps]==list(IDS),"missing finite service gap")
    for old,new in zip(journey["services"],gaps):
        require(new["id"]==old["service_id"] and len(new["missing"])>=2,"gap incomplete")
        require(new["source_status"]=="OPEN_EVIDENCE_LIMITED","invented recovery")
        require(new["same_build_service_binding"]=="UNPROVEN","fake v1 server linkage")
        require(new["verified_original_value"] is None,"invented original value")
        require(new["recovered_by_this_package"] is False,"claimed original acquisition")
        require(bool(new["why"]) and bool(new["reopen"]) and bool(new["notEvidence"]),"missing source boundary")
        require(new["kind"]=="ORIGINAL_SERVER_OR_SAME_BUILD_MISSING_INPUT","source category drift")
    discovery=data["public_discovery"]
    for key in ("exhaustive_global_search","source_unavailable_worldwide_claim",
                "new_raw_source_verified","new_original_game_value_obtained"):
        require(discovery[key] is False, "inflated search result: "+key)
    require(discovery["proof_status"]=="LIMITED_DISCOVERY_NOT_NEGATIVE_HISTORICAL_EVIDENCE",
            "negative search treated as proof")
    require(len(discovery["routes"])>=4,"incomplete finite search ledger")
    require(any("ACCESS_ERROR_NOT_ABSENCE" in x["result"] for x in discovery["routes"]),
            "archive reader error misclassified")
    decision=data["portfolio_decision"]
    require(decision["EARLY_VILLAGE_SERVICE_DEEPENING"]=="STOP_UNTIL_NAMED_SOURCE_REOPENER",
            "open-ended speculative service work")
    require(decision["NEXT"]=="STAGE-A-JOINT-REVIEW-DECISION-01",
            "lost stage-A handoff")
    require(decision["NEXT_REQUIRES_USER_ACCEPTANCE"] is True, "implicit stage promotion")
    require(decision["TW10_SAVEDATA_R79"]=="PAUSED_NON_BLOCKING", "R79 restored")
    review=(ROOT/SOURCES["review"][0]).read_text(encoding="utf-8")
    require("7项 PARTIAL、2项 OPEN" in review, "portfolio review no longer matches")
    return {"status":"PASS","finite_services":len(gaps),"source_blobs":len(SOURCES),
        "new_original_values":0,"next":decision["NEXT"],"stage_b":"GATED"}
if __name__=="__main__":
    print(json.dumps(validate(json.loads(REPORT.read_text(encoding="utf-8"))),
                     ensure_ascii=False,sort_keys=True))
