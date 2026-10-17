"""Validate a delegated, evidence-limited Stage A review acceptance.

The historical snapshots are *not* rewritten. This is an independent later
decision, not a new historical discovery or permission to start production.
"""
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DEFAULT=ROOT/"research/recovered/STONEAGE-STAGE-A-EVIDENCE-LIMITED-ACCEPTANCE-R1.json"
PINS={
  "review": {
    "path": "research/recovered/STONEAGE-STAGE-A-CONSOLIDATED-REVIEW-R1.json",
    "blob": "1a31c094bdd1c4b64b2f6510270c111be2c9415c"
  },
  "review_doc": {
    "path": "docs/STAGE-A-CONSOLIDATED-REVIEW-R1.md",
    "blob": "07c9950a40d110d4dabb80b11412db8b4ea64ba9"
  },
  "early_gap": {
    "path": "research/recovered/STONEAGE-STAGE-A-EARLY-SOURCE-GAP-TRIAGE-R1.json",
    "blob": "927293c09bc04097e013bb96ad1ead5d654ce82d"
  },
  "joint_crosswalk": {
    "path": "research/recovered/STONEAGE-STAGE-A-JOINT-REVIEW-DECISION-R1.json",
    "blob": "01bb88954bd9331a132accfa1a27d92a1c827aad"
  },
  "joint_report": {
    "path": "docs/STAGE-A-JOINT-REVIEW-DECISION-R1.md",
    "blob": "4164f42e545bd8b50cf67506d3e28dda0ef59719"
  },
  "joint_acceptance": {
    "path": "research/recovered/STONEAGE-STAGE-A-JOINT-REVIEW-ACCEPTANCE-R1.json",
    "blob": "aac5246755136f40c1b7289025360d2a1ec33806"
  }
}
PREFIXES=[
  {
    "path": "docs/CURRENT-STATE.md",
    "bytes": 1879000,
    "blob": "1451d4882e4e9eb6986c8a036f32ffa2fb9b2f53"
  },
  {
    "path": "docs/RESTORATION-ROADMAP-R2.md",
    "bytes": 34969,
    "blob": "223c6c48801310ada3d5c9bb2badbb2f8b419964"
  },
  {
    "path": "docs/DESIGN-DECISIONS.md",
    "bytes": 32783,
    "blob": "bf0b51536b7bfb5b3f19c93171f3aada365ccbac"
  },
  {
    "path": "docs/RESTORATION-PHASE-GATE-R1.md",
    "bytes": 74172,
    "blob": "9e51c1d33abbaa27cee3a5a070f59639fd16b7f5"
  },
  {
    "path": "README.md",
    "bytes": 7369,
    "blob": "d362e5a1cc591158b049056b2bd438f2a64dabf5"
  }
]
FAMILIES=["lineage","world","characters_pets","battle","inventory_economy","npc_quests","graphics_audio_ui","runtime_persistence","integration"]
BLOCKERS=["B0_ORIGINAL_SERVER_CONTENT","B1_ORIGINAL_PLAYER_PET_AND_EXP","B2_ORIGINAL_QUEST_ITEM_DURABILITY","B3_ORIGINAL_UI_VISUAL_BINDING","B4_ORIGINAL_LOCAL_SAVEDATA_R79"]
SERVICES=["SAVE_POINT","MAMMOTH_BUS","VILLAGE_CARE_TRAINING","VILLAGE_WORK","GROUND_ITEM_EXPIRY"]
def require(v,m):
    if not v:raise ValueError(m)
def blob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
def validate(p):
    require(p["schema"]=="stoneage.stage_a_evidence_limited_acceptance.r1","schema")
    require(p["task"]=="STAGE-A-EVIDENCE-LIMITED-REVIEW-ACCEPTANCE-01","task")
    require(p["remote_baseline"]=={"head":"abf584d7858c4089aef0b103c41270665f2c8219","tree":"b030c04102f35608c538721e92d687528ea515b8","verified_main_successful_runs":[39003331521,39003331699,39003331763]},"remote baseline not pinned")
    require(p["source_pins"]==PINS,"source pin metadata")
    for name,row in PINS.items():
        require(blob((ROOT/row["path"]).read_bytes())==row["blob"],"source custody: "+name)
    require(p["append_only_prefixes"]==PREFIXES,"lost continuity metadata")
    for row in PREFIXES:
        raw=(ROOT/row["path"]).read_bytes()
        require(len(raw)>row["bytes"] and blob(raw[:row["bytes"]])==row["blob"],"historical prefix corrupted: "+row["path"])
    rev=json.loads((ROOT/PINS["review"]["path"]).read_text(encoding="utf-8"))
    gap=json.loads((ROOT/PINS["early_gap"]["path"]).read_text(encoding="utf-8"))
    old=json.loads((ROOT/PINS["joint_crosswalk"]["path"]).read_text(encoding="utf-8"))
    # Historical immutable snapshots MUST stay "not yet user accepted"; this
    # later delegated decision doesn't retroactively change earlier snapshots.
    require(rev["stage_a_accepted"] is False and old["approval_state"]["stage_a_accepted"] is False,"prior evidence snapshot changed")
    d=p["decision"]
    require(d["selected_option"]=="ACCEPT_EVIDENCE_LIMITED_STAGE_A_REVIEW","wrong decision")
    require(d["delegated_by_user"] is True and d["authorization_utterance"]=="按照你认为的最优解选择就行 哪怕后续出现错误需要补充改正我们还可以改 我相信你的选择","user delegation missing")
    require(d["scope"]=="RESEARCH_REVIEW_CHECKPOINT_ONLY" and d["stage_a_review_accepted"] is True and d["stage_a_research_queue"]=="CLOSED_EVIDENCE_LIMITED" and d["reversible_by_new_evidence"] is True,"acceptance scope invalid")
    h=p["historical_status"]
    for flag in ("full_original_game_restored","complete_original_commercial_playthrough","original_1999_exact_build_restored","original_server_world_npc_quest_rewards_recovered","commercial_saac_durable_relogin_verified","original_ui_real_execution_restored","new_original_content_this_decision"):
        require(h[flag] is False,"historical completion falsely promoted: "+flag)
    require(h["overall_restoration_percent"] is None and h["r79"]=="PAUSED_NON_BLOCKING","percent or R79")
    require(h["system_families"]==len(rev["families"])==9 and h["family_gates"]=={"PARTIAL":7,"OPEN":2},"family count/gate")
    require([r["id"] for r in rev["families"]]==p["family_ids"]==FAMILIES,"family IDs changed")
    require(h["family_gates"]=={x:sum(r["gate"]==x for r in rev["families"]) for x in ("PARTIAL","OPEN")},"system source gates diverged")
    require(h["player_flows"]==len(rev["playflows"])==7 and h["material_blockers"]==len(rev["blockers"])==5,"playflow/blocker count")
    require(p["blocker_ids"]==[x["id"] for x in rev["blockers"]]==BLOCKERS,"blockers changed")
    require(h["early_services_open"]==len(gap["gaps"])==5 and p["early_service_ids"]==[x["id"] for x in gap["gaps"]]==SERVICES,"service scope")
    require(all(x["recovered_by_this_package"] is False for x in gap["gaps"]),"misstated source recovery")
    b=p["stage_b"]
    require(b["discussion_brief_prepared"] is True,"no brief")
    for flag in ("collaborative_new_game_design_ratified","production_approved","engine_final_selected","engine_build_started","new_world_story_assets_authorized_for_production"):
        require(b[flag] is False,"unauthorized Stage B production: "+flag)
    require(b["status"]=="DESIGN_DISCUSSION_READY_PRODUCTION_GATED" and b["next"]=="STAGE-B-JOINT-DESIGN-DIRECTION-01","Stage B gate")
    require(p["reopen_policy"]["trigger"]=="AUTHENTICATED_SAME_ERA_PRIMARY_DATA_OR_MATERIAL_CONTRADICTION","unjustified historical closure")
    require(p["reopen_policy"]["action"]=="REOPEN_NAMED_STAGE_A_SPEC_WHILE_RETAINING_CURRENT_DECISION_AS_HISTORY","reopen policy")
    design=p["design_scope"]
    require(set(design["source_roles"])=={"V1_DIRECT","EARLY_LINEAGE","LATER_RECOVERED","MODERN_SYNTHETIC","NEW_DESIGN"},"evidence/design conflation")
    require(design["first_mount"]=="POST_FIRST_SLICE_DESIGN_MILESTONE_NOT_AUTHENTICATED_TW10_FACT","first riding historical promotion")
    require(design["engine_selection"]=="DEFERRED_TO_COLLABORATIVE_DESIGN_GATE","engine locked")
    require(design["proprietary_binaries_or_assets_added"] is False,"proprietary content claimed")
    docs=p["handoff_docs"]
    require(docs==["docs/STAGE-A-EVIDENCE-LIMITED-ACCEPTANCE-R1.md","docs/STAGE-B-COLLABORATIVE-DESIGN-BRIEF-R1.md"],"handoff docs")
    text="\n".join((ROOT/x).read_text(encoding="utf-8") for x in docs)
    for s in ("7 PARTIAL","2 OPEN","Stage A","Stage B","R79","NEW_DESIGN","V1_DIRECT","首次骑宠"):
        require(s in text or (s=="首次骑宠" and "第一次骑" in text),"missing acceptance/design guard: "+s)
    require(p["approved_despite_old_snapshot_false"] is True and p["old_pre_decision_files_immutable"] is True,"old snapshot not preserved")
    return {"status":"PASS","bounded_review_accepted":True,"nine_systems":"7 PARTIAL + 2 OPEN","stage_b":"DESIGN_DISCUSSION_READY_PRODUCTION_GATED","original_game_restored":False,"production_started":False}
if __name__=="__main__":
    print(json.dumps(validate(json.loads(DEFAULT.read_text(encoding="utf-8"))),sort_keys=True,ensure_ascii=False))
