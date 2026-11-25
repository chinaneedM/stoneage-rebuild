"""Trace strict acquisition remainder skill slots to exact saved PC source rows."""

import argparse
from collections import Counter
import json
from pathlib import Path
import tempfile

from tools import stoneage_preserved_pet_skill_r45 as r45
from tools.stoneage_pet_source_lookup import ROOT, blob

TARGET = ROOT / "research/pets/PET-HIGH-FIRST-61-RESIDUAL-SKILL-DEFINITIONS-R1.json"
PINS = {
    "master": ("pets/PET-HIGH-FIRST-15-TW75-MASTER-FIELD-CATALOG-R1.json", "fec03646d7c7e4e287f9347c306119cc626d6abf"),
    "comparison": ("pets/PET-HIGH-FIRST-17-COMPARISON-SKILL-ENCOUNTER-R1.json", "63af501ab483770c5c58cb2d62152ab8923dcc2b"),
    "acquisition": ("pets/PET-HIGH-FIRST-50-ORIGINAL-ACQUISITION-R1.json", "4d0b31a7fa196cf8f227a7b0b1aea7183d9598f0"),
    "tables": ("recovered/STONEAGE-PET-MODULE-10-ORIGINAL-MIXED25-SERVER-TABLES-R1.json", "25a37aeb134fb180e322e7dc335029b7374452d8"),
    "original_r45": ("recovered/STONEAGE-PRESERVED-PET-SKILL-SOURCE-R45.json", "dd3baaf7e8edda43ef2e136d35f09d1da6717571"),
}
QUALIFICATIONS = {"official_birth_skills_verified": False, "official_acquisition_verified": False,
                  "native_runtime_verified": False, "original_table_published": False}
PAIRINGS = (("enemybase.txt", "petskill.txt"), ("enemybase2.txt", "petskill1.txt"))


def build_plan():
    sources = {}
    for key, (path, digest) in PINS.items():
        raw = (ROOT / "research" / path).read_bytes()
        if blob(raw) != digest:
            raise ValueError(f"source blob changed: {path}")
        sources[key] = json.loads(raw)
    acq = sources["acquisition"]
    if acq["input_git_blobs"]["pet10"] != PINS["tables"][1]:
        raise ValueError("acquisition and skill table archives did not match")
    master = sources["master"]["pet_flag_1_field_projections"]
    tables = sources["tables"]["source_rows"]
    base_rows = {base: {row[-1]: row for row in tables[base]} for base, _ in PAIRINGS}
    skill_rows = {skill: {row[1]: row for row in tables[skill]} for _, skill in PAIRINGS}
    counts = {skill: Counter() for _, skill in PAIRINGS}
    rows = []
    for observed in acq["projection"]["records"]:
        position = observed["tw75_row_index"]
        entry = master[position]
        key = (entry["template_id"], entry["graphic"], entry["row_sha256"])
        if key != (observed["template_id"], observed["graphic"], observed["row_sha256"]):
            raise ValueError(f"claimed template changed at position {position}")
        grade = {}
        for (base, skill), pair in zip(PAIRINGS, observed["source_pairs"], strict=True):
            if pair["base"] != base:
                raise ValueError("unexpected source pair order")
            slots = []
            if pair["match"] == "EXACT_ROW":
                original = base_rows[base][pair["base_row_sha256"]]
                if ((original[1], original[2], original[-1]) != key or
                        original[15] != entry["skill_slots"]):
                    raise ValueError(f"original template or slot drift: {base} {position}")
                for slot, skill_id in enumerate(original[15]):
                    if skill_id is not None and skill_id > 0:
                        line, _, digest = skill_rows[skill][skill_id]
                        slots.append({"slot_index": slot, "skill_id": skill_id,
                                      "definition_line": line, "definition_row_sha256": digest})
                        counts[skill][skill_id] += 1
            grade[skill] = {"template_match": pair["match"], "source_slots": slots}
        rows.append({"position": position, "template_id": key[0], "graphic": key[1],
                     "row_sha256": key[2], "scope": grade})
    summary = {skill: {"exact_templates": sum(row["scope"][skill]["template_match"] == "EXACT_ROW" for row in rows),
                       "positive_skill_slots": sum(histogram.values()),
                       "skill_ids": sorted(histogram)}
               for skill, histogram in counts.items()}
    expected = (67, 64, 135, 6, 12)
    actual = (len(rows), summary["petskill.txt"]["exact_templates"], summary["petskill.txt"]["positive_skill_slots"],
              summary["petskill1.txt"]["exact_templates"], summary["petskill1.txt"]["positive_skill_slots"])
    if actual != expected:
        raise ValueError(f"strict residual source scope changed: {actual}")
    return rows, summary, skill_rows["petskill.txt"], sources


def derive_definitions(members, wanted):
    for path, (size, digest) in r45.EXPECTED.items():
        if (len(members[path]), r45.sha(members[path])) != (size, digest):
            raise ValueError(f"original member changed: {path}")
    config = r45.skill_config(members["setup.cf"])
    rows = r45.parse_table(members["data/petskill.txt"])
    definitions = []
    for row in rows:
        skill_id = row["numbers"]["ID"]
        if skill_id not in wanted:
            continue
        raw_name = row["fields"][0]
        name = raw_name.decode("cp950")
        if name != raw_name.decode("big5") or not 0 < len(name) <= 48:
            raise ValueError(f"ambiguous archived skill name: {skill_id}")
        definitions.append({"skill_id": skill_id, "line": row["line"], "row_sha256": r45.sha(row["body"]),
                            "name": name, "callback": row["callback"], "numeric_fields": row["numbers"]})
    return config, definitions


def verify(report, plan):
    rows, summary, original, sources = plan
    if (report["schema"] != "stoneage.pet61.same_archive_residual_skill_slots.r1" or
            report["source_git_blobs"] != {path: digest for path, digest in PINS.values()} or
            report["rows"] != rows or report["summary"] != summary or report["qualification"] != QUALIFICATIONS):
        raise ValueError("PET61 scope, provenance or derived slot relation changed")
    old = sources["original_r45"]
    if report["configured_paths"] != old["material"]["configured_skill_paths_as_written"]:
        raise ValueError("archived skill load paths changed")
    fields = ("path", "bytes", "sha256", "crc32", "header_sha256", "compressed_payload_sha256",
              "independent_decoded_bytes_equal")
    if sorted(tuple(m[k] for k in fields) for m in report["source_receipt"]["members"]) != sorted(
            tuple(m[k] for k in fields) for m in old["receipt"]["members"]):
        raise ValueError("RAR member provenance drift")
    definitions = report["configured_skill_definitions"]
    if ({x["skill_id"] for x in definitions} != set(summary["petskill.txt"]["skill_ids"]) or len(definitions) != 6):
        raise ValueError("configured Chinese skill definitions were not fully recorded")
    comparison = {x["id"]: x for x in sources["comparison"]["skill_ids"]}
    outcomes = []
    for definition in definitions:
        skill_id = definition["skill_id"]
        if [definition["line"], skill_id, definition["row_sha256"]] != original[skill_id]:
            raise ValueError(f"original skill row fingerprint changed: {skill_id}")
        peer = comparison[skill_id]
        outcomes.append({"id": skill_id, "archived_name": definition["name"], "later_name": peer["extended_name"],
                         "callback_token_equal": definition["callback"] == peer["extended_function"],
                         "later_legacy_id_defined": peer["legacy_name"] is not None})
    return {**summary, "original_vs_later": outcomes}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan-only", action="store_true")
    parser.add_argument("--read-original", action="store_true")
    parser.add_argument("--report", type=Path, default=TARGET)
    args = parser.parse_args()
    if args.plan_only and args.read_original:
        parser.error("choose either --plan-only or --read-original")
    plan = build_plan()
    if args.plan_only:
        print(json.dumps(plan[1], sort_keys=True))
        return
    if args.read_original:
        rows, summary, _, _ = plan
        receipt = {}
        with tempfile.TemporaryDirectory(prefix="pet61-skill-") as work:
            members = r45.acquire(Path(work), receipt)
        config, definitions = derive_definitions(members, summary["petskill.txt"]["skill_ids"])
        report = {"schema": "stoneage.pet61.same_archive_residual_skill_slots.r1",
                  "source_git_blobs": {path: digest for path, digest in PINS.values()},
                  "configured_paths": config, "configured_skill_definitions": definitions,
                  "source_receipt": {k: receipt[k] for k in ("members", "actual_range_bytes", "range_requests")},
                  "rows": rows, "summary": summary, "qualification": QUALIFICATIONS}
        result = verify(report, plan)
        args.report.write_text(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                               encoding="utf-8")
    else:
        result = verify(json.loads(args.report.read_bytes()), plan)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
