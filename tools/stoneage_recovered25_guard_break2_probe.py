#!/usr/bin/env python3
"""Hard-probe recovered25 GuardBreak2 row/usage; never dump raw source rows."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from tools.stoneage_guard_break2_model import CALLBACK_NAME
from tools.stoneage_recovered25_enemybase_runtime import (
    load_recovered25_enemybase_runtime,
)
from tools.stoneage_recovered25_petskill_runtime import (
    load_recovered25_petskill_runtime,
)


EXPECTED_RECOVERED25_IDS=(543,)
EXPECTED_SLOT_REFERENCES=11
EXPECTED_TEMPLATES=11


def analyze_runtime_objects(petskills,enemybase):
    entries=tuple(sorted(
        (
            entry for entry in petskills.skills.values()
            if entry.function_name==CALLBACK_NAME
        ),
        key=lambda entry:int(entry.skill_id),
    ))
    ids={int(entry.skill_id) for entry in entries}
    references=0
    templates=set()
    for tempno,template in enemybase.templates.items():
        uses=sum(
            int(raw) in ids
            for raw in template.skill_slot_ids
            if int(raw)>0
        )
        references+=uses
        if uses:
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
            "option_bytes":len(raw),
            "option_sha256":hashlib.sha256(raw).hexdigest(),
            "option_nul_free":b"\0" not in raw,
        })
    population_closed=(
        tuple(row["id"] for row in rows)==EXPECTED_RECOVERED25_IDS
        and references==EXPECTED_SLOT_REFERENCES
        and len(templates)==EXPECTED_TEMPLATES
    )
    return {
        "rows":tuple(rows),
        "slot_references":references,
        "templates":len(templates),
        "population_closed":population_closed,
    }


def analyze(data_dir:Path,setup:Path|None):
    return analyze_runtime_objects(
        load_recovered25_petskill_runtime(data_dir=data_dir,setup=setup),
        load_recovered25_enemybase_runtime(data_dir=data_dir,setup=setup),
    )


def emit(result):
    print("StoneAge recovered25 GuardBreak2 domain probe — R1")
    print("No original names/comments/raw OPTION text/source rows are stored.")
    print(f"COUNT|guardbreak2_skill_rows|{len(result['rows'])}")
    print(f"COUNT|enemybase_slot_references|{result['slot_references']}")
    print(f"COUNT|enemybase_templates|{result['templates']}")
    for row in result["rows"]:
        print(
            "GUARDBREAK2_ROW|"
            + "|".join(
                f"{key}={int(value) if isinstance(value,bool) else value}"
                for key,value in row.items()
            )
        )
    print(
        "RESOLUTION|RECOVERED25_GUARDBREAK2_POPULATION_"
        + ("CLOSED" if result["population_closed"] else "OPEN")
    )


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--data-dir",type=Path,required=True)
    parser.add_argument("--setup",type=Path)
    args=parser.parse_args()
    emit(analyze(args.data_dir,args.setup))


if __name__=="__main__":
    main()
