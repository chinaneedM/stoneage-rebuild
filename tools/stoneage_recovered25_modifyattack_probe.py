"""Derived-only exact Modifyattack population/data probe for recovered25."""

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

CALLBACK_NAME = "PETSKILL_Modifyattack"
EXPECTED_PETSKILL_SHA256 = (
    "f9cefefda40e3a5de9b8cdcb9f8d5c75cd768257bb9b12f7591e86d61fe2f6d4"
)
EXPECTED_CALLBACK_IDS = ()  # Pin after verified discovery; do not infer from pressure.
EXPECTED_REFERENCED_IDS = (544, 545, 546)
EXPECTED_SLOT_REFERENCES = 3
EXPECTED_TEMPLATES = 3
EXPECTED_EXACT_ROWS = ()
EXPECTED_TEMPLATE_ROWS = ()


def analyze_runtime_objects(
    petskills,
    enemybase,
    *,
    expected_exact_rows=EXPECTED_EXACT_ROWS,
    expected_template_rows=EXPECTED_TEMPLATE_ROWS,
):
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

    from tools.stoneage_modifyattack_reference_model import parse_modifyattack_option
    rows = []
    for entry in entries:
        raw = bytes(entry.option_bytes)
        parsed = parse_modifyattack_option(raw)
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
            "element_index": parsed.element_index if parsed else None,
            "percent": parsed.percent if parsed else None,
        })

    ids = tuple(row["id"] for row in rows)
    referenced = tuple(sorted(k for k, value in counts.items() if value))
    actual_rows = tuple(
        (
            row["id"], row["field"], row["target"], row["cost"], row["illegal"],
            row["slot_references"], row["option_bytes"], row["option_sha256"],
            row["option_contains_nul"], row["element_index"], row["percent"],
        )
        for row in rows
    )
    actual_templates = tuple(
        (
            row["tempno"], row["graphic_id"],
            row["skill_slots"], row["skill_ids"],
        )
        for row in templates
    )
    population_closed = (
        ids == EXPECTED_CALLBACK_IDS
        and referenced == EXPECTED_REFERENCED_IDS
        and sum(counts.values()) == EXPECTED_SLOT_REFERENCES
        and len(templates) == EXPECTED_TEMPLATES
    )
    return {
        "rows": tuple(rows),
        "callback_ids": ids,
        "referenced_ids": referenced,
        "slot_references": sum(counts.values()),
        "templates": tuple(templates),
        "population_closed": population_closed,
        "positive_references_closed": (
            referenced == EXPECTED_REFERENCED_IDS
            and sum(counts.values()) == EXPECTED_SLOT_REFERENCES
            and len(templates) == EXPECTED_TEMPLATES
        ),
        "exact_rows_closed": actual_rows == expected_exact_rows,
        "exact_templates_closed": actual_templates == expected_template_rows,
    }


def emit(result):
    print("StoneAge recovered25 PETSKILL_Modifyattack probe — R1")
    print("No names/descriptions/raw OPTION bytes/assets stored.")
    print(f"COUNT|modifyattack_skill_rows|{len(result['rows'])}")
    print(f"COUNT|enemybase_slot_references|{result['slot_references']}")
    print(f"COUNT|enemybase_templates|{len(result['templates'])}")
    for row in result["rows"]:
        print("MODIFYATTACK_ROW|" + "|".join(
            f"{key}={int(value) if isinstance(value, bool) else value}"
            for key, value in row.items()
        ))
    for row in result["templates"]:
        slots = ",".join(str(x) for x in row["skill_slots"])
        ids = ",".join(str(x) for x in row["skill_ids"])
        print(
            "MODIFYATTACK_TEMPLATE|"
            f"tempno={row['tempno']}|graphic_id={row['graphic_id']}|"
            f"skill_slots={slots}|skill_ids={ids}"
        )
    print("RESOLUTION|RECOVERED25_MODIFYATTACK_POSITIVE_REFERENCES_"
          + ("CLOSED" if result["positive_references_closed"] else "OPEN"))
    print(
        "RESOLUTION|RECOVERED25_MODIFYATTACK_POPULATION_"
        + ("CLOSED" if result["population_closed"] else "OPEN")
    )
    print(
        "RESOLUTION|RECOVERED25_MODIFYATTACK_EXACT_ROWS_"
        + ("CLOSED" if result["exact_rows_closed"] else "OPEN")
    )
    print(
        "RESOLUTION|RECOVERED25_MODIFYATTACK_EXACT_TEMPLATES_"
        + ("CLOSED" if result["exact_templates_closed"] else "OPEN")
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--setup", type=Path)
    parser.add_argument("--discover", action="store_true")
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
    if not result["positive_references_closed"]:
        raise SystemExit("Modifyattack positive references drift")
    if args.discover:
        print("BOUNDARY|discovery_only_exact_population_and_identity_not_accepted")
        return
    if not result["population_closed"]:
        raise SystemExit("Modifyattack callback/reference population drift")
    if not result["exact_rows_closed"]:
        raise SystemExit("Modifyattack exact row drift")
    if not result["exact_templates_closed"]:
        raise SystemExit("Modifyattack exact template/slot drift")


if __name__ == "__main__":
    main()
