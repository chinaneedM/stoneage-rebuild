"""Derived-only first-pass Lighttakeed population/data probe for recovered25."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from tools.stoneage_recovered25_petskill_runtime import (
    load_recovered25_petskill_runtime,
)
from tools.stoneage_recovered25_enemybase_runtime import (
    load_recovered25_enemybase_runtime,
)

CALLBACK_NAME = "PETSKILL_Lighttakeed"
EXPECTED_PETSKILL_SHA256 = (
    "f9cefefda40e3a5de9b8cdcb9f8d5c75cd768257bb9b12f7591e86d61fe2f6d4"
)
EXPECTED_CALLBACK_IDS = (610, 611)
EXPECTED_REFERENCED_IDS = (610, 611)
EXPECTED_SLOT_REFERENCES = 3
EXPECTED_TEMPLATES = 2


def analyze_runtime_objects(petskills, enemybase):
    entries = tuple(sorted(
        (
            entry for entry in petskills.skills.values()
            if entry.function_name == CALLBACK_NAME
        ),
        key=lambda entry: entry.skill_id,
    ))
    counts = {entry.skill_id: 0 for entry in entries}
    templates = []
    for tempno, template in sorted(enemybase.templates.items()):
        slots = tuple(
            index
            for index, raw_skill_id in enumerate(template.skill_slot_ids, 1)
            if int(raw_skill_id) in counts
        )
        if not slots:
            continue
        for index in slots:
            counts[int(template.skill_slot_ids[index - 1])] += 1
        templates.append({
            "tempno": int(tempno),
            "graphic_id": int(template.graphic_id),
            "skill_slots": slots,
            "skill_ids": tuple(
                int(template.skill_slot_ids[index - 1]) for index in slots
            ),
        })

    rows = []
    for entry in entries:
        raw = bytes(entry.option_bytes)
        rows.append({
            "id": int(entry.skill_id),
            "field": int(entry.field),
            "target": int(entry.target),
            "cost": int(entry.cost),
            "illegal": int(entry.illegal),
            "slot_references": int(counts[entry.skill_id]),
            "option_bytes": len(raw),
            "option_sha256": hashlib.sha256(raw).hexdigest(),
            "option_contains_nul": b"\0" in raw,
            "marker_vanish": b"VANISH" in raw,
            "marker_absrob": b"ABSROB" in raw,
            "marker_reflec": b"REFLEC" in raw,
        })

    ids = tuple(row["id"] for row in rows)
    referenced = tuple(sorted(k for k, value in counts.items() if value))
    return {
        "rows": tuple(rows),
        "callback_ids": ids,
        "referenced_ids": referenced,
        "slot_references": sum(counts.values()),
        "templates": tuple(templates),
        "population_closed": (
            ids == EXPECTED_CALLBACK_IDS
            and referenced == EXPECTED_REFERENCED_IDS
            and sum(counts.values()) == EXPECTED_SLOT_REFERENCES
            and len(templates) == EXPECTED_TEMPLATES
        ),
    }


def emit(result):
    print("StoneAge recovered25 PETSKILL_Lighttakeed probe — R1 first pass")
    print("No names/descriptions/raw OPTION bytes/assets stored.")
    print(f"COUNT|lighttakeed_skill_rows|{len(result['rows'])}")
    print(f"COUNT|enemybase_slot_references|{result['slot_references']}")
    print(f"COUNT|enemybase_templates|{len(result['templates'])}")
    for row in result["rows"]:
        print("LIGHTTAKEED_ROW|" + "|".join(
            f"{key}={int(value) if isinstance(value, bool) else value}"
            for key, value in row.items()
        ))
    for row in result["templates"]:
        slots = ",".join(str(x) for x in row["skill_slots"])
        ids = ",".join(str(x) for x in row["skill_ids"])
        print(
            "LIGHTTAKEED_TEMPLATE|"
            f"tempno={row['tempno']}|graphic_id={row['graphic_id']}|"
            f"skill_slots={slots}|skill_ids={ids}"
        )
    print(
        "RESOLUTION|RECOVERED25_LIGHTTAKEED_POPULATION_"
        + ("CLOSED" if result["population_closed"] else "OPEN")
    )
    print("RESOLUTION|RECOVERED25_LIGHTTAKEED_EXACT_ROWS_OPEN")
    print("RESOLUTION|RECOVERED25_LIGHTTAKEED_EXACT_TEMPLATES_OPEN")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--setup", type=Path)
    args = parser.parse_args()
    pets = load_recovered25_petskill_runtime(
        data_dir=args.data_dir, setup=args.setup
    )
    enemies = load_recovered25_enemybase_runtime(
        data_dir=args.data_dir, setup=args.setup
    )
    digest = hashlib.sha256(
        (args.data_dir / pets.source_file).read_bytes()
    ).hexdigest()
    if digest != EXPECTED_PETSKILL_SHA256:
        raise SystemExit("full petskill hash drift")
    result = analyze_runtime_objects(pets, enemies)
    emit(result)
    print("DATA_SHA256|file=petskill|sha256=" + digest)
    if not result["population_closed"]:
        raise SystemExit("Lighttakeed callback/reference population drift")


if __name__ == "__main__":
    main()
