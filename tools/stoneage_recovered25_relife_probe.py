"""Derived-only recovered25 ENEMYSKILL_ReLife population/data probe."""

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

CALLBACK_NAME="ENEMYSKILL_ReLife"
EXPECTED_PETSKILL_SHA256=(
    "f9cefefda40e3a5de9b8cdcb9f8d5c75cd768257bb9b12f7591e86d61fe2f6d4"
)
EXPECTED_CALLBACK_IDS=(500,)
EXPECTED_REFERENCED_IDS=(500,)
EXPECTED_SLOT_REFERENCES=3
EXPECTED_TEMPLATES=3
EXPECTED_EXACT_ROW=(
    500,1,2,2,0,3,0,
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    False,
)
EXPECTED_TEMPLATE_ROWS=(
    (39,100370,(5,)),
    (909,100071,(2,)),
    (1165,101814,(4,)),
)


def analyze_runtime_objects(petskills,enemybase):
    entries=tuple(sorted(
        (
            entry for entry in petskills.skills.values()
            if entry.function_name==CALLBACK_NAME
        ),
        key=lambda entry:entry.skill_id,
    ))
    counts={entry.skill_id:0 for entry in entries}
    templates=[]
    for tempno,template in sorted(enemybase.templates.items()):
        slots=tuple(
            index
            for index,raw_skill_id in enumerate(template.skill_slot_ids,1)
            if int(raw_skill_id) in counts
        )
        if not slots:
            continue
        for index in slots:
            counts[int(template.skill_slot_ids[index-1])]+=1
        templates.append({
            "tempno":int(tempno),
            "graphic_id":int(template.graphic_id),
            "skill_slots":slots,
        })

    rows=[]
    for entry in entries:
        raw=bytes(entry.option_bytes)
        rows.append({
            "id":int(entry.skill_id),
            "field":int(entry.field),
            "target":int(entry.target),
            "cost":int(entry.cost),
            "illegal":int(entry.illegal),
            "slot_references":int(counts[entry.skill_id]),
            "option_bytes":len(raw),
            "option_sha256":hashlib.sha256(raw).hexdigest(),
            "option_contains_nul":b"\0" in raw,
        })

    ids=tuple(row["id"] for row in rows)
    referenced=tuple(sorted(k for k,v in counts.items() if v))
    exact_row_closed=False
    if len(rows)==1:
        row=rows[0]
        actual=(
            row["id"],row["field"],row["target"],row["cost"],
            row["illegal"],row["slot_references"],row["option_bytes"],
            row["option_sha256"],row["option_contains_nul"],
        )
        exact_row_closed=actual==EXPECTED_EXACT_ROW
    actual_templates=tuple(
        (
            row["tempno"],row["graphic_id"],row["skill_slots"],
        )
        for row in templates
    )
    return {
        "rows":tuple(rows),
        "callback_ids":ids,
        "referenced_ids":referenced,
        "slot_references":sum(counts.values()),
        "templates":tuple(templates),
        "population_closed":(
            ids==EXPECTED_CALLBACK_IDS
            and referenced==EXPECTED_REFERENCED_IDS
            and sum(counts.values())==EXPECTED_SLOT_REFERENCES
            and len(templates)==EXPECTED_TEMPLATES
        ),
        "exact_row_closed":exact_row_closed,
        "exact_templates_closed":actual_templates==EXPECTED_TEMPLATE_ROWS,
    }


def emit(result):
    print("StoneAge recovered25 ENEMYSKILL_ReLife probe — R1 first pass")
    print("No names/descriptions/raw OPTION bytes/assets stored.")
    print(f"COUNT|relife_skill_rows|{len(result['rows'])}")
    print(f"COUNT|enemybase_slot_references|{result['slot_references']}")
    print(f"COUNT|enemybase_templates|{len(result['templates'])}")
    for row in result["rows"]:
        print("RELIFE_ROW|"+"|".join(
            f"{key}={int(value) if isinstance(value,bool) else value}"
            for key,value in row.items()
        ))
    for row in result["templates"]:
        slots=",".join(str(x) for x in row["skill_slots"])
        print(
            "RELIFE_TEMPLATE|"
            f"tempno={row['tempno']}|graphic_id={row['graphic_id']}|"
            f"skill_slots={slots}"
        )
    print(
        "RESOLUTION|RECOVERED25_RELIFE_POPULATION_"
        +("CLOSED" if result["population_closed"] else "OPEN")
    )
    print(
        "RESOLUTION|RECOVERED25_RELIFE_EXACT_ROW_"
        +("CLOSED" if result["exact_row_closed"] else "OPEN")
    )
    print(
        "RESOLUTION|RECOVERED25_RELIFE_EXACT_TEMPLATES_"
        +("CLOSED" if result["exact_templates_closed"] else "OPEN")
    )


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--data-dir",type=Path,required=True)
    parser.add_argument("--setup",type=Path)
    args=parser.parse_args()
    pets=load_recovered25_petskill_runtime(
        data_dir=args.data_dir,setup=args.setup
    )
    enemies=load_recovered25_enemybase_runtime(
        data_dir=args.data_dir,setup=args.setup
    )
    digest=hashlib.sha256(
        (args.data_dir/pets.source_file).read_bytes()
    ).hexdigest()
    if digest!=EXPECTED_PETSKILL_SHA256:
        raise SystemExit("full petskill hash drift")
    result=analyze_runtime_objects(pets,enemies)
    emit(result)
    print("DATA_SHA256|file=petskill|sha256="+digest)
    if not result["population_closed"]:
        raise SystemExit("ReLife callback/reference population drift")
    if not result["exact_row_closed"]:
        raise SystemExit("ReLife exact row drift")
    if not result["exact_templates_closed"]:
        raise SystemExit("ReLife exact template/slot drift")


if __name__=="__main__":
    main()
