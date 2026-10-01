#!/usr/bin/env python3
"""Hard-probe recovered25 PETSKILL_FallGround row and enemybase pressure."""

from __future__ import annotations

import argparse
from pathlib import Path

from tools.stoneage_fall_ground_model import (
    ATTACK_MARKER,
    CALLBACK_NAME,
    parse_fall_ground_option,
)
from tools.stoneage_recovered25_enemybase_runtime import (
    load_recovered25_enemybase_runtime,
)
from tools.stoneage_recovered25_petskill_runtime import (
    load_recovered25_petskill_runtime,
)


def analyze_runtime_objects(petskills,enemybase):
    entries=tuple(sorted(
        (
            entry for entry in petskills.skills.values()
            if entry.function_name==CALLBACK_NAME
        ),
        key=lambda entry:int(entry.skill_id),
    ))
    ids={int(entry.skill_id) for entry in entries}
    refs=0
    tempnos=set()
    for tempno,template in enemybase.templates.items():
        for skill_id in template.skill_slot_ids:
            if int(skill_id) in ids:
                refs+=1
                tempnos.add(int(tempno))

    rows=[]
    for entry in entries:
        cp950_ok=big5_ok=False
        cp950_option=big5_option=None
        try:
            cp950_option=entry.option_bytes.decode("cp950","strict")
            cp950_ok=True
        except UnicodeDecodeError:
            pass
        try:
            big5_option=entry.option_bytes.decode("big5","strict")
            big5_ok=True
        except UnicodeDecodeError:
            pass

        cp950_parsed=(
            parse_fall_ground_option(cp950_option)
            if cp950_option is not None else None
        )
        big5_parsed=(
            parse_fall_ground_option(big5_option)
            if big5_option is not None else None
        )
        same_decode=bool(
            cp950_option is not None
            and big5_option is not None
            and cp950_option==big5_option
        )
        attack_percent=(
            None if cp950_parsed is None else cp950_parsed.attack_percent
        )
        rows.append({
            "skill_id":int(entry.skill_id),
            "field":int(entry.field),
            "target":int(entry.target),
            "cost":int(entry.cost),
            "illegal":int(entry.illegal),
            "option_bytes":len(entry.option_bytes),
            "cp950_ok":cp950_ok,
            "big5_ok":big5_ok,
            "same_decode":same_decode,
            "marker":bool(
                cp950_parsed is not None and cp950_parsed.marker_present
            ),
            "attack_percent":attack_percent,
            "big5_marker":bool(
                big5_parsed is not None and big5_parsed.marker_present
            ),
            "big5_attack_percent":(
                None if big5_parsed is None else big5_parsed.attack_percent
            ),
        })

    closed=bool(
        len(rows)==1
        and refs==23
        and all(
            row["cp950_ok"]
            and row["big5_ok"]
            and row["same_decode"]
            and row["marker"]
            and row["big5_marker"]
            and row["attack_percent"] is not None
            and row["attack_percent"]==row["big5_attack_percent"]
            for row in rows
        )
    )
    return {
        "rows":tuple(rows),
        "slot_references":refs,
        "templates":len(tempnos),
        "domain_closed":closed,
    }


def analyze(data_dir:Path,setup:Path|None):
    return analyze_runtime_objects(
        load_recovered25_petskill_runtime(data_dir=data_dir,setup=setup),
        load_recovered25_enemybase_runtime(data_dir=data_dir,setup=setup),
    )


def emit(result):
    print("StoneAge recovered25 FallGround probe — R1")
    print("No original names/comments/raw OPTION text are stored in this report.")
    print(f"COUNT|fall_ground_skill_rows|{len(result['rows'])}")
    print(f"COUNT|enemybase_slot_references|{result['slot_references']}")
    print(f"COUNT|enemybase_templates|{result['templates']}")
    for row in result["rows"]:
        print(
            "FALLGROUND_ROW|"
            f"id={row['skill_id']}|field={row['field']}|target={row['target']}|"
            f"cost={row['cost']}|illegal={row['illegal']}|"
            f"option_bytes={row['option_bytes']}|cp950={int(row['cp950_ok'])}|"
            f"big5={int(row['big5_ok'])}|same_decode={int(row['same_decode'])}|"
            f"attack_marker={int(row['marker'])}|"
            f"attack_percent={row['attack_percent']}"
        )
    print(
        "RESOLUTION|"
        + (
            "RECOVERED25_FALLGROUND_OPTION_DOMAIN_CLOSED"
            if result["domain_closed"]
            else "RECOVERED25_FALLGROUND_OPTION_DOMAIN_OPEN"
        )
    )


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--data-dir",type=Path,required=True)
    parser.add_argument("--setup",type=Path)
    args=parser.parse_args()
    emit(analyze(args.data_dir,args.setup))


if __name__=="__main__":
    main()
