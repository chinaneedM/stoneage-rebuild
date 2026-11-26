"""Trace all claimed TW75 templates to the selected preserved server tables."""
import argparse
from collections import Counter
import csv
import json
from pathlib import Path
import tempfile

from tools import stoneage_pet_high_first_61_skills as pet61
from tools import stoneage_preserved_pet_skill_r45 as source
from tools.stoneage_pet_source_lookup import ROOT, blob


REPORT = ROOT / "research/pets/PET-HIGH-FIRST-76-SELECTED-MASTER-FIELDS-R1.json"
REPORT_BLOB = "0005e7d7943907c01024f5dd24132b126e4bb3f3"
CLIENT_INVENTORY = ROOT / "research/recovered/STONEAGE-WAYI85-MSI-CLIENT-PAYLOAD-R1.json"
CLIENT_INVENTORY_BLOB = "18a68c9d4275763ef0ed7a347cca940cffe0fee2"
PINS = {
    "master": pet61.PINS["master"],
    "tables": pet61.PINS["tables"],
    "baseline": pet61.PINS["original_r45"],
    "birth": ("pets/PET-HIGH-FIRST-16-TW75-CONDITIONAL-BIRTH-GROWTH-R1.json", "8cb864a78f1ff2b3c89ae1739ac485968d104c10"),
    "routes": ("pets/PET-HIGH-FIRST-45-BULK-ACQUISITION-R1.json", "5273e2c3f6a71fa9ea8a2f7b51139f280a9e9808"),
    "rewards": ("pets/PET-HIGH-FIRST-42-EXACT-TEMPLATE-CROSSWALK-R1.json", "c6667a6190283f4ec3ad3813c570357b18906ccc"),
    "residual": ("pets/PET-HIGH-FIRST-61-RESIDUAL-SKILL-DEFINITIONS-R1.json", "6ec78a6e303f2e83d616a976e0c71a97330d27df"),
}
SCHEMA = "stoneage.pet76.saved_selected_master_fields.r1"
QUALIFICATION = {
    "official_deployment_verified": False,
    "official_birth_or_growth_verified": False,
    "official_birth_skills_verified": False,
    "official_acquisition_verified": False,
    "runtime_executed": False,
    "original_payload_published": False,
}


def inputs():
    result = {}
    for key, (path, digest) in PINS.items():
        raw = (ROOT / "research" / path).read_bytes()
        if blob(raw) != digest:
            raise ValueError(f"source blob mismatch: {path}")
        result[key] = json.loads(raw)
    return result


def fields(row):
    return dict(graphic=row[2], pet_flag=row[3], initnum=int(row[4]), lvup_literal=row[5],
                base=list(map(int, row[6:10])), elements=list(map(int, row[10:14])),
                skill_slot_capacity=row[14], skill_slots=row[15])


def derive(d):
    tables = d["tables"]["source_rows"]
    primary = {row[1]: row for row in tables["enemybase.txt"]}
    alternate = {row[1]: row for row in tables["enemybase2.txt"]}
    definitions = {skill_id: (line, digest) for line, skill_id, digest in tables["petskill.txt"]}
    master = d["master"]["pet_flag_1_field_projections"]
    birth = d["birth"]["rows"]
    routes = d["routes"]["projection"]["claimed_tw75_rows"]
    rewards = {row["tw75_row_index"]: row for row in d["rewards"]["rows"]}
    assert len(master) == len(birth) == len(routes) == 467 and len(rewards) == 36

    result = []
    used_skills = Counter()
    match_counts = Counter()
    diff_counts = Counter()
    for i, (claim, model, route) in enumerate(zip(master, birth, routes, strict=True)):
        tid, graphic, digest = claim["template_id"], claim["graphic"], claim["row_sha256"]
        assert (model["template_id"], model["source_row_sha256"]) == (tid, digest)
        assert (route["tw75_row_index"], route["template_id"], route["graphic"], route["tw75_row_sha256"]) == (i, tid, graphic, digest)
        saved = primary.get(tid)
        diff = {k: v for k, v in fields(saved).items() if claim[k] != v} if saved else None
        if saved is None:
            grade = "NO_SAME_ID_IN_SELECTED_MIXED25_TABLE"
        elif saved[-1] == digest:
            grade = "EXACT_SHARED_TEMPLATE_ROW"
            assert not diff and saved[3] == claim["pet_flag"] == 1
        else:
            grade = "SAME_ID_NONIDENTICAL_ROW"
            diff_counts.update(diff.keys())
        assert grade == route["match_status"]
        if saved:
            assert saved[0] - 1 == route["mixed25_template_row_index"]
        match_counts[grade] += 1

        slots = []
        if grade == "EXACT_SHARED_TEMPLATE_ROW":
            for slot, skill_id in enumerate(saved[15]):
                if skill_id is not None and skill_id > 0:
                    line, row_hash = definitions[skill_id]
                    slots.append(dict(slot_index=slot, skill_id=skill_id, definition_line=line,
                                      definition_row_sha256=row_hash))
                    used_skills[skill_id] += 1
        reward = rewards.get(i)
        if reward:
            assert grade == "EXACT_SHARED_TEMPLATE_ROW"
            assert (reward["template_id"], reward["graphic"], reward["shared_template_row_sha256"]) == (tid, graphic, digest)
        backup = alternate.get(tid)
        result.append(dict(
            position=i, template_id=tid, graphic=graphic, row_sha256=digest,
            selected_table_grade=grade,
            selected_row_index=saved[0] - 1 if saved else None,
            selected_row_sha256=saved[-1] if saved else None,
            selected_fields_differing_from_claim=diff,
            alternate_exact_row=bool(backup and backup[-1] == digest),
            configured_skill_slots=slots,
            conditional_range_index=i,
            positive_route_count=route["positive_route_count"],
            double_pet_flag_route_count=route["double_pet_flag_route_count"],
            lv1_double_pet_flag_route_count=route["lv1_double_flag_route_count"],
            saved_reward_instance_id=reward["award_instance_id"] if reward else None,
        ))

    # Prior residual work is an independent exact per-slot guard.
    for previous in d["residual"]["rows"]:
        row = result[previous["position"]]
        assert previous["scope"]["petskill.txt"]["source_slots"] == row["configured_skill_slots"]

    summary = dict(
        template_positions=len(result), selected_template_matches=dict(match_counts),
        nonexact_selected_projected_differences=dict(diff_counts),
        alternate_exact_rows=sum(r["alternate_exact_row"] for r in result),
        configured_positive_slots=sum(used_skills.values()),
        configured_skill_ids=sorted(used_skills),
        positive_encounter_templates=sum(r["positive_route_count"] > 0 for r in result),
        double_pet_flag_encounter_templates=sum(r["double_pet_flag_route_count"] > 0 for r in result),
        double_pet_flag_lv1_templates=sum(r["lv1_double_pet_flag_route_count"] > 0 for r in result),
        saved_reward_template_links=len(rewards),
    )
    assert (match_counts["EXACT_SHARED_TEMPLATE_ROW"], match_counts["SAME_ID_NONIDENTICAL_ROW"],
            match_counts["NO_SAME_ID_IN_SELECTED_MIXED25_TABLE"]) == (440, 26, 1)
    assert diff_counts == {"base": 6}
    assert not any(r["alternate_exact_row"] and r["selected_table_grade"] != "EXACT_SHARED_TEMPLATE_ROW" for r in result)
    assert (summary["alternate_exact_rows"], summary["configured_positive_slots"], len(used_skills)) == (57, 941, 38)
    assert (summary["positive_encounter_templates"], summary["double_pet_flag_encounter_templates"],
            summary["double_pet_flag_lv1_templates"]) == (123, 118, 94)
    return result, summary, definitions


def verify(report, d, derived):
    rows, summary, original = derived
    pins = {path: digest for path, digest in PINS.values()}
    if (report["schema"], report["source_git_blobs"], report["rows"], report["summary"],
            report["qualification"]) != (SCHEMA, pins, rows, summary, QUALIFICATION):
        raise ValueError("template projection or source boundaries changed")
    baseline = d["baseline"]
    assert report["configured_paths"] == baseline["material"]["configured_skill_paths_as_written"]
    fields = ("path", "bytes", "sha256", "crc32", "header_sha256", "compressed_payload_sha256",
              "independent_decoded_bytes_equal")
    found = sorted(tuple(member[k] for k in fields) for member in report["source_receipt"]["members"])
    expected = sorted(tuple(member[k] for k in fields) for member in baseline["receipt"]["members"])
    if found != expected:
        raise ValueError("original configured skill members or RAR custody changed")
    definitions = {row["skill_id"]: row for row in report["configured_skill_definitions"]}
    assert len(definitions) == len(report["configured_skill_definitions"]) == 38
    assert set(definitions) == set(summary["configured_skill_ids"])
    for skill_id, row in definitions.items():
        assert (row["line"], row["row_sha256"]) == original[skill_id]
        assert row["numeric_fields"]["ID"] == skill_id
        assert 0 < len(row["name"]) <= 48
    for earlier in d["residual"]["configured_skill_definitions"]:
        assert earlier == definitions[earlier["skill_id"]]


def verify_client_inventory():
    raw = CLIENT_INVENTORY.read_bytes()
    if blob(raw) != CLIENT_INVENTORY_BLOB:
        raise ValueError("saved TW85 MSI inventory changed")
    table = json.loads(raw)["inspection"]["msi_tables"]["File"].splitlines()
    # MSI tables have two schema rows after the column names.
    files = list(csv.DictReader([table[0], *table[3:]], delimiter="\t"))
    assert len(files) == len({row["File"] for row in files}) == 557
    assert sum(int(row["FileSize"]) for row in files) == 1808555613
    names = {row["FileName"].split("|")[-1].casefold() for row in files}
    server_names = {"enemybase.txt", "enemybase1.txt", "enemybase2.txt", "enemy.txt", "enemy2.txt",
                    "petskill.txt", "petskill1.txt", "petskill2.txt", "encount.txt", "group1.txt", "setup.cf"}
    assert not (names & server_names)
    print("PET76_TW85_MSI: 557 file rows verified; no standalone file under the checked server table names")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--plan-only", action="store_true")
    modes.add_argument("--read-original", action="store_true")
    parser.add_argument("--report", type=Path, default=REPORT)
    args = parser.parse_args()
    d = inputs()
    derived = derive(d)
    rows, summary, _ = derived
    if args.read_original:
        receipt = {}
        with tempfile.TemporaryDirectory(prefix="pet76-original-") as work:
            members = source.acquire(Path(work), receipt)
        config, definitions = pet61.derive_definitions(members, summary["configured_skill_ids"])
        report = dict(schema=SCHEMA, source_git_blobs={path: digest for path, digest in PINS.values()},
                      configured_paths=config, configured_skill_definitions=definitions,
                      source_receipt={k: receipt[k] for k in ("members", "range_requests", "actual_range_bytes")},
                      rows=rows, summary=summary, qualification=QUALIFICATION)
        verify(report, d, derived)
        data = json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
        args.report.write_text(data, encoding="utf-8")
        raw = data.encode()
        print("PET76_RECEIPT", len(raw), source.sha(raw), blob(raw))
    elif not args.plan_only:
        raw = args.report.read_bytes()
        if args.report == REPORT and blob(raw) != REPORT_BLOB:
            raise ValueError("accepted original derived report blob has changed")
        verify(json.loads(raw), d, derived)
        verify_client_inventory()
    print("PET76_SUMMARY=" + json.dumps(summary, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
