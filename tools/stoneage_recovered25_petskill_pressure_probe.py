#!/usr/bin/env python3
"""Rank recovered25 enemybase pet-skill callback pressure from active data."""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

from tools.stoneage_recovered25_petskill_runtime import (
    STABLE_COMMON_CALLBACKS,
    load_recovered25_petskill_runtime,
)
from tools.stoneage_recovered25_enemybase_runtime import (
    load_recovered25_enemybase_runtime,
)


HISTORICAL_UB_CALLBACKS=frozenset({"PETSKILL_Merge"})
CLOSED_RUNTIME_CALLBACKS=frozenset(
    (set(STABLE_COMMON_CALLBACKS)-set(HISTORICAL_UB_CALLBACKS))
    | {
        "PETSKILL_AttackMagic",
        "ENEMYSKILL_ReHP",
        "ENEMYSKILL_ReLife",
        "PETSKILL_DamageToHp",
        "PETSKILL_MpDamage",
        "PETSKILL_FallGround",
        "PETSKILL_BattleTearDamage",
        "PETSKILL_Nocast",
        "PETSKILL_GuardBreak2",
        "PETSKILL_Barrier",
        "PETSKILL_AttackCrazed",
        "PETSKILL_Mdfyattack",
        "PETSKILL_Modifyattack",
        "PETSKILL_Weaken",
        "PETSKILL_WildViolentAttack",
        "PETSKILL_Refresh",
        "PETSKILL_SetMagicPet",
        "PETSKILL_BattleTimid",
        "PETSKILL_Combined",
        "PETSKILL_Vary",
        "PETSKILL_Lighttakeed",
    }
)


def classify(callback:str) -> str:
    if callback in HISTORICAL_UB_CALLBACKS:
        return "historical_ub"
    if callback in CLOSED_RUNTIME_CALLBACKS:
        return "closed_runtime"
    return "open"


def analyze_runtime_objects(petskills,enemybase):
    ids_by_callback=defaultdict(set)
    slot_uses_by_callback=defaultdict(int)
    templates_by_callback=defaultdict(set)
    total_positive=0
    unresolved_ids=set()

    for tempno,template in enemybase.templates.items():
        for raw_skill_id in template.skill_slot_ids:
            skill_id=int(raw_skill_id)
            if skill_id <= 0:
                continue
            total_positive += 1
            entry=petskills.skills.get(skill_id)
            if entry is None:
                unresolved_ids.add(skill_id)
                continue
            callback=str(entry.function_name)
            ids_by_callback[callback].add(skill_id)
            slot_uses_by_callback[callback]+=1
            templates_by_callback[callback].add(int(tempno))

    rows=[]
    for callback in sorted(
        slot_uses_by_callback,
        key=lambda name:(-slot_uses_by_callback[name],name),
    ):
        rows.append({
            "callback":callback,
            "skill_ids":tuple(sorted(ids_by_callback[callback])),
            "slot_uses":int(slot_uses_by_callback[callback]),
            "templates":len(templates_by_callback[callback]),
            "status":classify(callback),
        })

    open_rows=tuple(row for row in rows if row["status"]=="open")
    return {
        "rows":tuple(rows),
        "total_positive_slot_uses":total_positive,
        "unresolved_skill_ids":tuple(sorted(unresolved_ids)),
        "next_open":(None if not open_rows else open_rows[0]),
    }


def analyze(data_dir:Path,setup:Path|None):
    return analyze_runtime_objects(
        load_recovered25_petskill_runtime(data_dir=data_dir,setup=setup),
        load_recovered25_enemybase_runtime(data_dir=data_dir,setup=setup),
    )


def emit(result):
    print("StoneAge recovered25 enemybase pet-skill callback pressure — R1")
    print("No original names, descriptions, OPTION text, or source rows are stored.")
    print(f"TOTAL|positive_skill_slot_uses|{result['total_positive_slot_uses']}")
    print(f"TOTAL|unresolved_skill_ids|{len(result['unresolved_skill_ids'])}")
    for rank,row in enumerate(result["rows"],1):
        ids=",".join(str(x) for x in row["skill_ids"])
        print(
            "RANK|"
            f"rank={rank}|callback={row['callback']}|"
            f"ids={ids}|slot_uses={row['slot_uses']}|"
            f"templates={row['templates']}|status={row['status']}"
        )
    nxt=result["next_open"]
    if nxt is None:
        print("NEXT_OPEN|none")
    else:
        ids=",".join(str(x) for x in nxt["skill_ids"])
        print(
            "NEXT_OPEN|"
            f"callback={nxt['callback']}|ids={ids}|"
            f"slot_uses={nxt['slot_uses']}|templates={nxt['templates']}"
        )


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--data-dir",type=Path,required=True)
    parser.add_argument("--setup",type=Path)
    args=parser.parse_args()
    emit(analyze(args.data_dir,args.setup))


if __name__=="__main__":
    main()
