"""Verify a source-bounded Stage A portfolio checkpoint without gameplay promotion."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/recovered/STONEAGE-STAGE-A-PORTFOLIO-CHECKPOINT-R2.json"
GATES={"lineage":"PARTIAL","world":"PARTIAL","characters_pets":"PARTIAL",
       "battle":"PARTIAL","inventory_economy":"PARTIAL","npc_quests":"OPEN",
       "graphics_audio_ui":"PARTIAL","runtime_persistence":"OPEN","integration":"PARTIAL"}
SERVICE_IDS=("SAVE_POINT","MAMMOTH_BUS","VILLAGE_CARE_TRAINING",
             "VILLAGE_WORK","GROUND_ITEM_EXPIRY")
FIRST_PARTY_SECTIONS={"SAVE_POINT":"8010","MAMMOTH_BUS":"8100",
                      "VILLAGE_CARE_TRAINING":"8025/8050/8070",
                      "VILLAGE_WORK":"8025/8050/8070","GROUND_ITEM_EXPIRY":"7030"}
NO_PROMOTION=("original_1999_service_build_proven",
              "same_version_tw10_service_binding_proven",
              "original_server_transaction_or_ack_observed",
              "actual_visual_screen_or_route_replayed",
              "original_npc_quest_script_recovered",
              "stage_a_accepted","joint_user_review_completed","stage_b_started")


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def pin(path):
    require(isinstance(path,str) and path.startswith(("research/","docs/")), "unsafe evidence path")
    f=(ROOT/path).resolve()
    require(f.is_relative_to(ROOT) and f.is_file(), "missing evidence path")
    raw=f.read_bytes()
    return {"path":path,"bytes":len(raw),
            "git_blob":hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()}


def validate(report):
    require(report["schema"]=="stoneage.stage_a.portfolio_checkpoint.r2", "checkpoint schema")
    require(report["scope"]=="HISTORICAL_RESTORATION_ONLY", "scope mutation")
    for key in NO_PROMOTION:
        require(report[key] is False, "history/gameplay promotion: "+key)
    require(report["stage_b_gate"]=="GATED", "Stage B started")
    require(report["savedata_r79"]=="PAUSED_NON_BLOCKING", "R79 reopened")
    require(report["overall_percent"] is None, "invented completion percentage")
    require(report["system_gates"]==GATES, "nine-family gate drift")
    require(report["next_priority"]=="EARLY-VILLAGE-SERVICE-JOURNEY-01", "arbitrary NEXT drift")
    require(report["next_priority"]==report["package_order"][0]["id"], "first priority mismatch")
    require(report["portfolio_reassessment_trigger"]["max_consecutive_low_yield_units"]==2, "unbounded low-yield scanning")
    require(report["portfolio_reassessment_trigger"]["stop_if_no_material_outcome"] is True, "no stop rule")

    pins=report["source_pins"]
    require(set(pins)=={"consolidated","triage","portfolio","early_manual","early_crosswalk",
                       "tw10_ui","npc_flow","npc_flow_receipt"}, "missing source layer")
    require(len({v["path"] for v in pins.values()})==len(pins), "source path duplicates")
    for name,p in pins.items():
        require(p==pin(p["path"]), "source mutation: "+name)
    consolidated=json.loads((ROOT/pins["consolidated"]["path"]).read_text())
    triage=json.loads((ROOT/pins["triage"]["path"]).read_text())
    old_portfolio=json.loads((ROOT/pins["portfolio"]["path"]).read_text())
    require(report["system_gates"]==triage["system_gates"], "triage gate conflict")
    require(report["system_gates"]=={r["id"]:r["gate"] for r in consolidated["families"]},
            "review packet gate conflict")
    require(report["system_gates"]=={r["id"]:r["gate"] for r in old_portfolio["families"]},
            "old work portfolio gate conflict")
    require(len(consolidated["playflows"])==7, "seven player-flow evidence lost")
    require(len(triage["blockers"])==5, "five existing critical blockers lost")

    manual=json.loads((ROOT/pins["early_manual"]["path"]).read_text())
    ui=json.loads((ROOT/pins["tw10_ui"]["path"]).read_text())
    crosswalk=json.loads((ROOT/pins["early_crosswalk"]["path"]).read_text())
    late=json.loads((ROOT/pins["npc_flow"]["path"]).read_text())
    receipt=json.loads((ROOT/pins["npc_flow_receipt"]["path"]).read_text())
    require(manual["manual_capture"]=="20010418083149", "first-party date drift")
    require(manual["manual_is_1999_or_tw10_exact_build"] is False, "false version identity")
    require(manual["observations"]["manual_contracts"]["bus"]["stop_minutes"]==3,"bus 3 min")
    require(manual["observations"]["manual_contracts"]["bus"]["passenger_limit"]==4,"bus max 4")
    require(manual["observations"]["manual_contracts"]["bus"]["encounters_while_riding"] is False,"bus encounter")
    require(manual["observations"]["manual_contracts"]["save_point"]["first_use_offering_required"] is True,"offering gate")
    require(manual["observations"]["manual_contracts"]["save_point"]["durable_server_write_proven"] is False,"unproven save ACK")
    require(manual["observations"]["manual_contracts"]["ground_item"]["duration"] is None,"unknown expiry time")
    require(ui["stage_a_accepted"] is False and ui["baseline"].startswith("TAIWAN_V1_ORIGINAL"),"v1 origin")
    require(late["counts"]["typed_field_occurrences"]==49 and
            late["counts"]["same_record_multi_item_patterns"]==3,"late NPC flow drift")
    require(receipt["stage_b_gate"]=="GATED" and late["original_server_executed"] is False,
            "late original-game promotion")
    require(crosswalk["stage_a_accepted"] is False and crosswalk["stage_b_gate"]=="GATED",
            "manual/late-model equivalence promotion")

    services=report["early_service_journey_slices"]
    require(len(services)==5 and tuple(x["id"] for x in services)==SERVICE_IDS,
            "five-service scope change")
    surfaces={s["id"]:s for s in ui["surfaces"]}
    for row in services:
        require(row["manual_section"]==FIRST_PARTY_SECTIONS[row["id"]], "unanchored section")
        require(all(sec in manual["observations"]["manual_section_hashes"] for sec in
                    row["manual_section"].split("/")), "missing manual text section")
        require(row["manual_source_layer"]=="JSS_FIRST_PARTY_2001_04_18", "manual provenance drift")
        require(row["original_tw10_service_binding"]=="UNPROVEN", "same-game inferred from separate sources")
        require(row["original_1999_membership"]=="OPEN", "1999 data fabricated")
        require(row["runtime_or_server_trace"]=="UNAVAILABLE", "commercial trace fabricated")
        require(bool(row["business_behavior"]) and bool(row["missing_original_inputs"])
                and bool(row["stop_condition"]), "incomplete service contract")
        require(len(set(row["tw10_client_visibility_surfaces"]))==len(row["tw10_client_visibility_surfaces"]),
                "duplicate UI surface")
        require(all(x in surfaces for x in row["tw10_client_visibility_surfaces"]), "fabricated UI carrier")
    require(services[0]["id"]=="SAVE_POINT" and "original ACK" in
            " ".join(services[0]["missing_original_inputs"]), "savepoint durability understated")

    packages=report["package_order"]
    require(len(packages)==3 and len({p["id"] for p in packages})==3, "queue instability")
    require([p["decision"] for p in packages]==["START","PARK_EVIDENCE_GATED","PARK_EVIDENCE_GATED"],
            "unclear operational priority")
    for package in packages:
        require(bool(package["deliverable"]) and bool(package["material_gap"])
                and bool(package["source_scope"]) and bool(package["stop_condition"]),
                "unbounded work package")
    require(report["historical_quest_server_files_added"] is False, "fake historical content")
    require(report["production_engine_changes"] is False, "Stage B production started")
    return {"status":"PASS","families":9,"playflows":7,"blockers":5,
            "pinned_sources":len(pins),"bounded_early_services":len(services),
            "next":report["next_priority"],"stage_b":"GATED"}


def main():
    data=json.loads(REPORT.read_text(encoding="utf-8"))
    print(json.dumps(validate(data),ensure_ascii=False,sort_keys=True))


if __name__=="__main__":
    main()
