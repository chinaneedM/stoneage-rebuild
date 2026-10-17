"""Bounded first-party village-service claims and original-client carrier audit.

This is a documentation/evidence validator, NOT a game simulation or a
transaction interpreter. A described JSS-2001 manual claim never asserts
an original TW1.0 server event, account balance or client rendering.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "research/recovered/STONEAGE-EARLY-VILLAGE-SERVICE-JOURNEY-R1.json"
SERVICE_IDS = ("SAVE_POINT", "MAMMOTH_BUS", "VILLAGE_CARE_TRAINING",
               "VILLAGE_WORK", "GROUND_ITEM_EXPIRY")
MANUAL_CLAIMS = {
    "SAVE_POINT": {
        "FIRST_USE_OFFERING_REQUIRED": "save_point.first_use_offering_required",
        "NEXT_LOGIN_USES_RECORDED_POINT": "save_point.next_login_uses_recorded_point",
    },
    "MAMMOTH_BUS": {
        "STOP_MINUTES": "bus.stop_minutes",
        "PASSENGER_LIMIT": "bus.passenger_limit",
        "ENCOUNTER_DURING_RIDE": "bus.encounters_while_riding",
        "ROUTE_VILLAGE_GROUPS": "bus.route_village_sets",
        "BOARD_EXIT_CONTROL": "bus.boarding_and_exit_control",
    },
    "VILLAGE_CARE_TRAINING": {
        "PAID_PET_SKILL_TRAINING": "services.paid_pet_skill_training",
        "PET_BUYBACK": "services.pet_buyback",
        "EVERY_VILLAGE_HAS_EVERY_FACILITY": "services.every_village_has_every_facility",
    },
    "VILLAGE_WORK": {
        "WORK_EXAMPLES": "services.work_examples",
    },
    "GROUND_ITEM_EXPIRY": {
        "ORDINARY_GROUND_ITEM_EXPIRES": "ground_item.ordinary_ground_item_expires_after_unspecified_time",
        "QUEST_DROP_LOGOUT_FLAG_PROVEN": "ground_item.quest_specific_immediate_drop_or_logout_flag_proven",
    }
}
MANUAL_SECTIONS = {
    "SAVE_POINT": "8010",
    "MAMMOTH_BUS": "8100",
    "VILLAGE_CARE_TRAINING": "8025/8050/8070",
    "VILLAGE_WORK": "8025/8050/8070",
    "GROUND_ITEM_EXPIRY": "7030",
}
SOURCE_FILES = {
    "checkpoint": ("research/recovered/STONEAGE-STAGE-A-PORTFOLIO-CHECKPOINT-R2.json",
                   "1666ab6597ed9a35de38a16ba6ee84761f8132c5"),
    "manual": ("research/recovered/STONEAGE-EARLY-CONTENT-GUIDE-MANUAL-R1.json",
               "54404a8118f125a9a53eabbb8bad8c4a0d07b190"),
    "original_ui": ("research/recovered/STONEAGE-TW10-UI-SEMANTICS-R1.json",
                    "ee3d230317c47b13e3513f25c3feba2ff9305e1c"),
    "historical_crosswalk": ("research/recovered/STONEAGE-EARLY-CONTENT-MODEL-CROSSWALK-R1.json",
                             "f2fa2e6dc90131f4a37040700b4a6bb0371db4d1"),
    "checkpoint_spec": ("docs/STAGE-A-PORTFOLIO-CHECKPOINT-R2.md",
                        "c5db7c1416121d2337baacd6132eae4daf23fd20")
}
OBSERVED_RECORDS = {
    "SAVE_POINT": {"status_location", "npc_window_session"},
    "MAMMOTH_BUS": {"status_location", "status_party_member"},
    "VILLAGE_CARE_TRAINING": {"status_compact_progress", "status_pet_full",
                              "pet_skill_view_slot", "npc_window_session"},
    "VILLAGE_WORK": {"inventory_full_slot", "npc_window_session"},
    "GROUND_ITEM_EXPIRY": {"world_ground_item_record", "inventory_full_slot"}
}
REQUIRED_FLAGS_FALSE = ("stage_a_accepted", "stage_b_started",
                        "original_1999_or_tw10_service_identity_proven",
                        "original_server_actions_observed", "original_client_executed",
                        "original_world_quest_data_recovered",
                        "production_gameplay_changed")


def require(ok, message):
    if not ok:
        raise ValueError(message)


def git_blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def load_pin(pin):
    path, expected_sha = SOURCE_FILES[pin]
    raw = (ROOT / path).read_bytes()
    require(git_blob(raw) == expected_sha, "source changed: " + pin)
    return json.loads(raw) if path.endswith(".json") else raw.decode("utf-8")


def manual_get(manual, path):
    value = manual["observations"]["manual_contracts"]
    for part in path.split("."):
        require(isinstance(value, dict) and part in value, "missing manual claim path: " + path)
        value = value[part]
    return value


def claim_result(packet, service_id, claim_key, value, *, source_layer="JSS_2001_04_18"):
    """Compare a proposed statement with one archived manual, not gameplay.

    Typed equality excludes bool/int confusion; unknown source fields never
    become false or zeros. An assertion about another build is out of scope.
    """
    if source_layer != "JSS_2001_04_18":
        return "OUTSIDE_SOURCE_SCOPE"
    if service_id not in SERVICE_IDS or claim_key not in MANUAL_CLAIMS[service_id]:
        return "NO_SOURCE_ASSERTION"
    row = next((r for r in packet["services"] if r["service_id"] == service_id), None)
    require(row is not None, "service missing")
    claim = next((x for x in row["manual_claims"] if x["key"] == claim_key), None)
    require(claim is not None, "contract claim missing")
    manual = load_pin("manual")
    expected = manual_get(manual, claim["manual_path"])
    if expected is None:
        return "UNKNOWN_SOURCE_VALUE"
    if type(expected) is type(value) and expected == value:
        return "MATCHES_ARCHIVED_MANUAL_DESCRIPTION"
    return "DIFFERS_FROM_ARCHIVED_MANUAL_NOT_EXECUTION_RESULT"


def validate(packet):
    require(packet["schema"] == "stoneage.early_village_service_journey.r1", "schema")
    require(packet["scope"] ==
            "FIRST_PARTY_BEHAVIOR_DESCRIPTIONS_PLUS_SEPARATELY_VERIFIED_ORIGINAL_CLIENT_CARRIERS",
            "scope drift")
    require(packet["manual_snapshot"] == "20010418083149", "capture date drift")
    require(packet["stage_a_gates"] == "7_PARTIAL_2_OPEN", "nine-family gate changed")
    require(packet["stage_b_gate"] == "GATED" and packet["r79"] == "PAUSED_NON_BLOCKING",
            "stage or R79 drift")
    for name in REQUIRED_FLAGS_FALSE:
        require(packet[name] is False, "historical execution promotion: " + name)
    require(packet["next"] == "STAGE-A-EARLY-SOURCE-GAP-TRIAGE-01", "next work scope")

    require(set(packet["source_pins"]) == set(SOURCE_FILES), "source inventory drift")
    for key, (path, blob) in SOURCE_FILES.items():
        require(packet["source_pins"][key] == {"path": path, "blob": blob}, "pin drift: " + key)
    manual = load_pin("manual")
    ui = load_pin("original_ui")
    checkpoint = load_pin("checkpoint")
    crosswalk = load_pin("historical_crosswalk")
    _ = load_pin("checkpoint_spec")
    require(manual["manual_capture"] == packet["manual_snapshot"], "not first party capture")
    require(manual["manual_is_1999_or_tw10_exact_build"] is False, "original version forged")
    require(ui["baseline"].startswith("TAIWAN_V1_ORIGINAL_COMPILED_SHAPES"),
            "original client mismatch")
    require(checkpoint["next_priority"] == "EARLY-VILLAGE-SERVICE-JOURNEY-01", "priority superseded")
    require(crosswalk["stage_a_accepted"] is False, "version boundary lost")
    source_rows = {x["id"]: x for x in checkpoint["early_service_journey_slices"]}
    indexed = {x["schema_record"]: x for surface in ui["surfaces"]
               for x in surface["record_contracts"]}
    records = packet["services"]
    require(len(records) == 5 and
            tuple(x["service_id"] for x in records) == SERVICE_IDS, "wrong five service scope")
    for row in records:
        ident = row["service_id"]
        require(row["manual_section"] == MANUAL_SECTIONS[ident], "manual section drift: " + ident)
        for sec in row["manual_section"].split("/"):
            require(sec in manual["observations"]["manual_section_hashes"], "no section pin")
        require(row["version_identity"] == "JSS_2001_MANUAL_NOT_PROVEN_TW10_OR_1999",
                "false same-version join")
        require(row["manual_date"] == "2001-04-18", "publication identity")
        require(bool(row["player_action"]) and bool(row["stop_condition"]), "incomplete behavior")
        require(row["source_aligned_journey_executable"] is False and
                row["server_or_runtime_result"] == "NOT_OBSERVED", "fake game execution")
        require(row["preconditions_not_resolved"] == source_rows[ident]["missing_original_inputs"],
                "hidden missing preconditions")
        claims = row["manual_claims"]
        require({x["key"] for x in claims} == set(MANUAL_CLAIMS[ident]) and
                len(claims) == len(MANUAL_CLAIMS[ident]), "incomplete evidence claims")
        for claim in claims:
            key, path = claim["key"], claim["manual_path"]
            require(path == MANUAL_CLAIMS[ident][key], "wrong source statement")
            expected_kind = ("EVIDENCE_BOUNDARY" if key == "QUEST_DROP_LOGOUT_FLAG_PROVEN"
                             else "MANUAL_BEHAVIOR")
            require(claim["claim_kind"] == expected_kind, "negative flag treated as gameplay")
            require(manual_get(manual, path) is not None, "selected manual field unknown")
        observable = row["tw10_generic_observables"]
        require({o["record"] for o in observable} == OBSERVED_RECORDS[ident] and
                len(observable) == len(OBSERVED_RECORDS[ident]), "missing or invented UI record")
        for o in observable:
            require(o["service_event_binding"] == "UNPROVEN", "unsupported exact service join")
            require(o["source"] ==
                    "ORIGINAL_TW10_COMPILED_SHAPE_WITH_EARLY_LINEAGE_FIELD_NAMES",
                    "wrong field semantic attribution")
            require(bool(o["fields"]) and len(o["fields"]) == len(set(o["fields"])), "bad fields")
            require(set(o["fields"]) <= {f["name"] for f in indexed[o["record"]]["fields"]},
                    "invented original field name")
    require(packet["unknown_handling"]["null_values"] == "UNKNOWN_NOT_FALSE",
            "unknown null collapsed")
    require(packet["unknown_handling"]["wrong_version"] == "OUTSIDE_SOURCE_SCOPE",
            "original v1 assumed")
    return {"status":"PASS","five_services":len(records),
            "qualified_manual_statements":sum(len(x["manual_claims"]) for x in records),
            "generic_v1_client_records":sum(len(x["tw10_generic_observables"]) for x in records),
            "source_blobs":len(SOURCE_FILES),"original_server_executed":False,"stage_b":"GATED"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, default=DEFAULT)
    args = parser.parse_args()
    data = json.loads(args.report.read_text(encoding="utf-8"))
    print(json.dumps(validate(data),ensure_ascii=False,sort_keys=True))


if __name__ == "__main__":
    main()
