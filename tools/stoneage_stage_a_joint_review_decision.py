"""Validate evidence-bounded Stage A joint decision without implying acceptance."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
from tools.stoneage_stage_a_review_packet import validate as validate_review
from tools.stoneage_stage_a_early_source_gap_triage import validate as validate_gap
ROOT=Path(__file__).resolve().parents[1]
DEFAULT=ROOT/"research/recovered/STONEAGE-STAGE-A-JOINT-REVIEW-DECISION-R1.json"
SOURCE_PINS={
"review":("research/recovered/STONEAGE-STAGE-A-CONSOLIDATED-REVIEW-R1.json","1a31c094bdd1c4b64b2f6510270c111be2c9415c"),
"gap":("research/recovered/STONEAGE-STAGE-A-EARLY-SOURCE-GAP-TRIAGE-R1.json","927293c09bc04097e013bb96ad1ead5d654ce82d"),
"gap_acceptance":("research/recovered/STONEAGE-STAGE-A-EARLY-SOURCE-GAP-ACCEPTANCE-R1.json","ec25c68367f5135976c642287801d44cb958a5f5"),
"roadmap":("docs/RESTORATION-ROADMAP-R2.md","b7f035623b450ed2b4eb516841978f2f1e7490d8"),
"review_document":("docs/STAGE-A-CONSOLIDATED-REVIEW-R1.md","07c9950a40d110d4dabb80b11412db8b4ea64ba9")
}
IDS=("SAVE_POINT","MAMMOTH_BUS","VILLAGE_CARE_TRAINING","VILLAGE_WORK","GROUND_ITEM_EXPIRY")
def req(ok,msg):
    if not ok:raise ValueError(msg)
def hash_git(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
def validate(p):
    req(p["schema"]=="stoneage.stage_a_joint_review_decision.r1","schema")
    req(p["task"]=="STAGE-A-JOINT-REVIEW-DECISION-01","wrong task")
    req(p["crosswalk_kind"]=="DERIVED_REVIEW_CAUSAL_LINKS_NOT_NEW_HISTORICAL_EVIDENCE","historical promotion")
    req(set(p["source_pins"])==set(SOURCE_PINS),"missing pinned source")
    for k,(path,sha) in SOURCE_PINS.items():
        req(p["source_pins"][k]=={"path":path,"git_blob":sha},"pin meta: "+k)
        raw=(ROOT/path).read_bytes()
        if k=="roadmap":
            # Append-only continuity: pin the exact old historical blob, not
            # the whole mutable living roadmap after this work-unit append.
            req(len(raw)>33851 and hash_git(raw[:33851])==sha,"roadmap original prefix")
            req(b"STAGE-A-JOINT-REVIEW-DECISION-01" in raw[33851:],"roadmap append missing")
        else:
            req(hash_git(raw)==sha,"pin bytes: "+k)
    rev=json.loads((ROOT/SOURCE_PINS["review"][0]).read_text(encoding="utf-8"))
    gap=json.loads((ROOT/SOURCE_PINS["gap"][0]).read_text(encoding="utf-8"))
    accepted=json.loads((ROOT/SOURCE_PINS["gap_acceptance"][0]).read_text(encoding="utf-8"))
    req(validate_review(rev)["status"]=="PASS","review source")
    req(validate_gap(gap)["status"]=="PASS","gap source")
    req(accepted["later_main_ci"]["stage_a_user_accepted"] is False,"false historical review acceptance")
    gates={x["id"]:x["gate"] for x in rev["families"]}
    req(len(gates)==p["family_count"]==9,"nine systems")
    req({k:sum(1 for x in gates.values() if x==k) for k in ("PARTIAL","OPEN")}==p["family_gate_counts"]=={"PARTIAL":7,"OPEN":2},"system gate change")
    blocked={x["id"] for x in rev["blockers"]}
    knownflows=[x["id"] for x in rev["playflows"]]
    rows=p["flow_to_blockers"]
    req([x["id"] for x in rows]==knownflows and len(rows)==p["playflow_count"]==7,"flow omission or order")
    req(len(blocked)==p["blocker_count"]==5,"missing historical blockers")
    for src,row in zip(rev["playflows"],rows):
        req(src["original_playthrough_certified"] is False,"real replay claim")
        req(bool(row["result"]) and row["blockers"] and set(row["blockers"])<=blocked,"flow evidence")
    services=p["service_to_blockers"]
    req([x["id"] for x in services]==list(IDS)==[x["id"] for x in gap["gaps"]],"service omission")
    req(len(services)==p["early_service_count"]==5,"service count")
    for src,row in zip(gap["gaps"],services):
        req(src["verified_original_value"] is None and src["recovered_by_this_package"] is False,"misstated original service")
        req(row["blockers"] and set(row["blockers"])<=blocked and bool(row["decision"]),"service blocker")
    opts=p["decision_options"]
    req([x["id"] for x in opts]==["CONTINUE_STAGE_A_NAMED_EVIDENCE","ACCEPT_EVIDENCE_LIMITED_STAGE_A_REVIEW","PAUSE_PENDING_PRIMARY_SOURCE"],"decision options")
    req(all(bool(x["meaning"]) for x in opts),"missing option explanations")
    state=p["approval_state"]
    for k in ("user_explicit_decision_received","stage_a_user_review_completed","stage_a_accepted","stage_b_started","production_engine_started"):
        req(state[k] is False,"unauthorized stage transition: "+k)
    req(state["selected_option"] is None and state["stage_b_gate"]=="GATED","stage gate")
    guard=p["evidence_guard"]
    for k in ("original_1999_exact_build_covered","original_early_server_world_npc_quest_recovered",
              "complete_v1_original_playthrough_certified","original_saac_durable_write_relogin_verified",
              "original_ui_rendering_verified"):
        req(guard[k] is False,"historical overclaim: "+k)
    req(guard["restoration_total_percent"] is None,"unjustified percentage")
    req(guard["client_local_savedata_r79"]=="PAUSED_NON_BLOCKING","savedata R79 mistakenly reopened")
    req(guard["no_new_original_game_binary_or_server_payload"] is True,"original source acquisition overclaim")
    req(p["next"]=="AWAIT_EXPLICIT_USER_STAGE_A_REVIEW_DECISION","wrong next")
    req(p["default_on_ordinary_continue"]=="REMAIN_STAGE_A_NOT_STAGE_B","silent stage advance")
    doc=(ROOT/p["review_document_path"]).read_text(encoding="utf-8")
    req(all(x in doc for x in ["7 PARTIAL","2 OPEN","B0","B1","B2","B3","B4","Stage B","Stage A"]),"review document incomplete")
    return {"status":"PASS","families":9,"flows":7,"blockers":5,"early_services":5,"stage_a_accepted":False,"stage_b":"GATED"}
if __name__=="__main__":
    print(json.dumps(validate(json.loads(DEFAULT.read_text(encoding="utf-8"))),ensure_ascii=False,sort_keys=True))
