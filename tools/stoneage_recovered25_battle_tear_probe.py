#!/usr/bin/env python3
"""Hard-probe recovered25 PETSKILL_BattleTearDamage domain."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from tools.stoneage_battle_tear_damage_model import CALLBACK_NAME,c_atoi
from tools.stoneage_recovered25_enemybase_runtime import (
    load_recovered25_enemybase_runtime,
)
from tools.stoneage_recovered25_petskill_runtime import (
    load_recovered25_petskill_runtime,
)


EXPECTED_IDS=(615,616)


def analyze_runtime_objects(petskills,enemybase):
    rows=tuple(sorted(
        (
            entry for entry in petskills.skills.values()
            if entry.function_name==CALLBACK_NAME
        ),
        key=lambda e:int(e.skill_id),
    ))
    ids=tuple(int(e.skill_id) for e in rows)
    idset=set(ids)
    refs=0; templates=set()
    for tempno,template in enemybase.templates.items():
        used=False
        for raw in template.skill_slot_ids:
            if int(raw) in idset:
                refs+=1; used=True
        if used:
            templates.add(int(tempno))

    result_rows=[]
    for entry in rows:
        ascii_ok=True
        try:
            option=entry.option_bytes.decode("ascii","strict")
        except UnicodeDecodeError:
            ascii_ok=False; option=""
        has_leading_int=bool(re.match(
            r"^[\t\n\v\f\r ]*[+-]?\d+",option
        )) if ascii_ok else False
        result_rows.append({
            "skill_id":int(entry.skill_id),
            "field":int(entry.field),
            "target":int(entry.target),
            "cost":int(entry.cost),
            "illegal":int(entry.illegal),
            "option_bytes":len(entry.option_bytes),
            "ascii_ok":ascii_ok,
            "has_leading_int":has_leading_int,
            "atoi_percent":c_atoi(option) if ascii_ok else None,
        })

    closed=bool(
        ids==EXPECTED_IDS
        and refs==19
        and len(templates)==19
        and all(
            row["ascii_ok"] and row["has_leading_int"]
            for row in result_rows
        )
    )
    return {
        "rows":tuple(result_rows),
        "slot_references":refs,
        "templates":len(templates),
        "domain_closed":closed,
    }


def analyze(data_dir:Path,setup:Path|None):
    return analyze_runtime_objects(
        load_recovered25_petskill_runtime(data_dir=data_dir,setup=setup),
        load_recovered25_enemybase_runtime(data_dir=data_dir,setup=setup),
    )


def emit(result):
    print("StoneAge recovered25 BattleTearDamage probe — R1")
    print("No original names/comments/raw OPTION text are stored in this report.")
    print(f"COUNT|tear_skill_rows|{len(result['rows'])}")
    print(f"COUNT|enemybase_slot_references|{result['slot_references']}")
    print(f"COUNT|enemybase_templates|{result['templates']}")
    for row in result["rows"]:
        print(
            "TEAR_ROW|"
            f"id={row['skill_id']}|field={row['field']}|target={row['target']}|"
            f"cost={row['cost']}|illegal={row['illegal']}|"
            f"option_bytes={row['option_bytes']}|ascii={int(row['ascii_ok'])}|"
            f"leading_int={int(row['has_leading_int'])}|"
            f"atoi_percent={row['atoi_percent']}"
        )
    print(
        "RESOLUTION|"
        + (
            "RECOVERED25_BATTLETEAR_OPTION_DOMAIN_CLOSED"
            if result["domain_closed"]
            else "RECOVERED25_BATTLETEAR_OPTION_DOMAIN_OPEN"
        )
    )


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--data-dir",type=Path,required=True)
    p.add_argument("--setup",type=Path)
    a=p.parse_args()
    emit(analyze(a.data_dir,a.setup))


if __name__=="__main__":
    main()
