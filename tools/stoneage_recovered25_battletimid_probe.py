"""Derived-only BattleTimid population/metadata probe for recovered25."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from tools.stoneage_recovered25_petskill_runtime import load_recovered25_petskill_runtime
from tools.stoneage_recovered25_enemybase_runtime import load_recovered25_enemybase_runtime
from tools.stoneage_battletimid_model import CALLBACK_NAME

EXPECTED_PETSKILL_SHA256="f9cefefda40e3a5de9b8cdcb9f8d5c75cd768257bb9b12f7591e86d61fe2f6d4"
EXPECTED_CALLBACK_IDS=(606,)
EXPECTED_REFERENCED_IDS=(606,)
EXPECTED_SLOT_REFERENCES=5
EXPECTED_TEMPLATES=5
EXPECTED_EXACT_ROW=(
    606,1,6,2,3000,0,
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    False,
)


def analyze_runtime_objects(petskills,enemybase,*,expected_exact_row=EXPECTED_EXACT_ROW):
    entries=tuple(sorted(
        (entry for entry in petskills.skills.values()
         if entry.function_name==CALLBACK_NAME),
        key=lambda entry:entry.skill_id,
    ))
    counts={entry.skill_id:0 for entry in entries}
    templates=set()
    for tempno,template in enemybase.templates.items():
        hit=False
        for raw_skill_id in template.skill_slot_ids:
            skill_id=int(raw_skill_id)
            if skill_id>0 and skill_id in counts:
                counts[skill_id]+=1
                hit=True
        if hit:
            templates.add(int(tempno))
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
    population_closed=(
        ids==EXPECTED_CALLBACK_IDS
        and referenced==EXPECTED_REFERENCED_IDS
        and sum(counts.values())==EXPECTED_SLOT_REFERENCES
        and len(templates)==EXPECTED_TEMPLATES
    )
    exact_row_closed=False
    if expected_exact_row is not None and len(rows)==1:
        row=rows[0]
        actual=(
            row["id"],row["field"],row["target"],row["cost"],row["illegal"],
            row["option_bytes"],row["option_sha256"],row["option_contains_nul"],
        )
        exact_row_closed=actual==expected_exact_row
    return {
        "rows":tuple(rows),
        "callback_ids":ids,
        "referenced_ids":referenced,
        "slot_references":sum(counts.values()),
        "templates":len(templates),
        "population_closed":population_closed,
        "exact_row_closed":exact_row_closed,
    }


def emit(result):
    print("StoneAge recovered25 BattleTimid probe — R1")
    print("No names/descriptions/raw OPTION bytes/assets stored.")
    print(f"COUNT|battletimid_skill_rows|{len(result['rows'])}")
    print(f"COUNT|enemybase_slot_references|{result['slot_references']}")
    print(f"COUNT|enemybase_templates|{result['templates']}")
    for row in result["rows"]:
        print("BATTLETIMID_ROW|"+"|".join(
            f"{key}={int(value) if isinstance(value,bool) else value}"
            for key,value in row.items()
        ))
    print(
        "RESOLUTION|RECOVERED25_BATTLETIMID_POPULATION_"
        +("CLOSED" if result["population_closed"] else "OPEN")
    )
    print(
        "RESOLUTION|RECOVERED25_BATTLETIMID_EXACT_ROW_"
        +("CLOSED" if result["exact_row_closed"] else "OPEN")
    )
    print("RESOLUTION|RECOVERED25_BATTLETIMID_ORDERED_RUNTIME_OPEN")


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--data-dir",type=Path,required=True)
    parser.add_argument("--setup",type=Path)
    args=parser.parse_args()
    pets=load_recovered25_petskill_runtime(data_dir=args.data_dir,setup=args.setup)
    enemies=load_recovered25_enemybase_runtime(data_dir=args.data_dir,setup=args.setup)
    digest=hashlib.sha256((args.data_dir/pets.source_file).read_bytes()).hexdigest()
    if digest!=EXPECTED_PETSKILL_SHA256:
        raise SystemExit("full petskill hash drift")
    result=analyze_runtime_objects(pets,enemies)
    emit(result)
    print("DATA_SHA256|file=petskill|sha256="+digest)
    if not result["population_closed"]:
        raise SystemExit("BattleTimid callback/reference population drift")
    if EXPECTED_EXACT_ROW is not None and not result["exact_row_closed"]:
        raise SystemExit("BattleTimid exact metadata/OPTION drift")


if __name__=="__main__":
    main()
