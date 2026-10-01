#!/usr/bin/env python3
"""Hard-probe recovered25 PETSKILL_DamageToHp rows and enemybase pressure.

The report stores mechanics-only derived values. Raw OPTION text and recovered
display strings are deliberately excluded.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from tools.stoneage_damage_to_hp_model import (
    CALLBACK_NAME,
    c_atoi,
    c_int_div,
)
from tools.stoneage_recovered25_enemybase_runtime import (
    load_recovered25_enemybase_runtime,
)
from tools.stoneage_recovered25_petskill_runtime import (
    load_recovered25_petskill_runtime,
)


def _decimal_prefix_present(token: str) -> bool:
    s=str(token)
    i=0
    while i < len(s) and s[i].isspace():
        i+=1
    if i < len(s) and s[i] in "+-":
        i+=1
    return i < len(s) and s[i].isdigit()


def analyze_runtime_objects(petskills, enemybase):
    entries=tuple(
        sorted(
            (
                entry
                for entry in petskills.skills.values()
                if entry.function_name == CALLBACK_NAME
            ),
            key=lambda entry:int(entry.skill_id),
        )
    )
    skill_ids={int(entry.skill_id) for entry in entries}
    refs=0
    tempnos=set()
    for tempno,template in enemybase.templates.items():
        for skill_id in template.skill_slot_ids:
            if int(skill_id) in skill_ids:
                refs+=1
                tempnos.add(int(tempno))

    rows=[]
    for entry in entries:
        ascii_ok=bool(entry.option_bytes.isascii())
        tokens=()
        token1=token2=None
        prefix1=prefix2=False
        if ascii_ok:
            text=entry.option_bytes.decode("ascii","strict")
            tokens=tuple(text.split("|"))
            if len(tokens)>=1:
                token1=c_atoi(tokens[0])
                prefix1=_decimal_prefix_present(tokens[0])
            if len(tokens)>=2:
                token2=c_atoi(tokens[1])
                prefix2=_decimal_prefix_present(tokens[1])
        rows.append({
            "skill_id":int(entry.skill_id),
            "field":int(entry.field),
            "target":int(entry.target),
            "cost":int(entry.cost),
            "illegal":int(entry.illegal),
            "option_bytes":len(entry.option_bytes),
            "ascii":ascii_ok,
            "token_count":len(tokens),
            "token1_decimal_prefix":prefix1,
            "token2_decimal_prefix":prefix2,
            "attack_adjust_token":token1,
            "callback_integer_ratio":(
                None if token1 is None else c_int_div(token1,100)
            ),
            "recovery_percent":token2,
        })

    domain_closed=bool(
        len(rows)==3
        and refs==30
        and all(
            row["ascii"]
            and row["token_count"]>=2
            and row["token1_decimal_prefix"]
            and row["token2_decimal_prefix"]
            for row in rows
        )
    )
    return {
        "rows":tuple(rows),
        "slot_references":refs,
        "templates":len(tempnos),
        "domain_closed":domain_closed,
    }


def analyze(data_dir: Path, setup: Path | None):
    return analyze_runtime_objects(
        load_recovered25_petskill_runtime(data_dir=data_dir,setup=setup),
        load_recovered25_enemybase_runtime(data_dir=data_dir,setup=setup),
    )


def emit(result) -> None:
    print("StoneAge recovered25 DamageToHp probe — R1")
    print("No original names/comments/raw OPTION text are stored in this report.")
    print(f"COUNT|damage_to_hp_skill_rows|{len(result['rows'])}")
    print(f"COUNT|enemybase_slot_references|{result['slot_references']}")
    print(f"COUNT|enemybase_templates|{result['templates']}")
    for row in result["rows"]:
        print(
            "DAMAGETOHP_ROW|"
            f"id={row['skill_id']}|field={row['field']}|target={row['target']}|"
            f"cost={row['cost']}|illegal={row['illegal']}|"
            f"option_bytes={row['option_bytes']}|ascii={int(row['ascii'])}|"
            f"token_count={row['token_count']}|"
            f"token1_decimal={int(row['token1_decimal_prefix'])}|"
            f"token2_decimal={int(row['token2_decimal_prefix'])}|"
            f"attack_adjust_token={row['attack_adjust_token']}|"
            f"callback_integer_ratio={row['callback_integer_ratio']}|"
            f"recovery_percent={row['recovery_percent']}"
        )
    print(
        "RESOLUTION|"
        + (
            "RECOVERED25_DAMAGETOHP_OPTION_DOMAIN_CLOSED"
            if result["domain_closed"]
            else "RECOVERED25_DAMAGETOHP_OPTION_DOMAIN_OPEN"
        )
    )


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument("--data-dir",type=Path,required=True)
    parser.add_argument("--setup",type=Path)
    args=parser.parse_args()
    emit(analyze(args.data_dir,args.setup))


if __name__ == "__main__":
    main()
