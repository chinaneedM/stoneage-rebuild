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

from tools.stoneage_battlemodel_placement_capability import (
    CONDITIONAL_CAPABILITY_KIND, CONDITIONAL_CAPABILITY_SCOPE,
    conditional_battlemodel_placements, verify_placement_population,
)

CLOSED_PRESSURE_STATUSES = frozenset({"closed_runtime", "closed_conditional_runtime"})

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
        "PETSKILL_2BattleTimid",
        "PETSKILL_Combined",
        "PETSKILL_Vary",
        "PETSKILL_Lighttakeed",
        "PETSKILL_BatFly",
    }
)


def classify(callback:str) -> str:
    if callback in HISTORICAL_UB_CALLBACKS:
        return "historical_ub"
    if callback in CLOSED_RUNTIME_CALLBACKS:
        return "closed_runtime"
    return "open"


def analyze_runtime_objects(petskills,enemybase, *, capability_identity=None,
                            capability_scope=CONDITIONAL_CAPABILITY_SCOPE):
    ids_by_callback=defaultdict(set)
    slot_uses_by_callback=defaultdict(int)
    templates_by_callback=defaultdict(set)
    qualified = conditional_battlemodel_placements(petskills, enemybase,
        identity=capability_identity, scope=capability_scope)
    total_positive=0
    unresolved_ids=set()

    for tempno,template in enemybase.templates.items():
        for slot, raw_skill_id in enumerate(template.skill_slot_ids):
            skill_id=int(raw_skill_id)
            if skill_id <= 0:
                continue
            total_positive += 1
            entry=petskills.skills.get(skill_id)
            if entry is None:
                unresolved_ids.add(skill_id)
                continue
            callback=str(entry.function_name)
            status = "closed_conditional_runtime" if (tempno, slot, skill_id) in qualified else classify(callback)
            key = (callback, status)
            ids_by_callback[key].add(skill_id)
            slot_uses_by_callback[key]+=1
            templates_by_callback[key].add(int(tempno))

    rows=[]
    for key in sorted(slot_uses_by_callback, key=lambda key:(-slot_uses_by_callback[key], *key)):
        callback, status = key
        row = dict(callback=callback, skill_ids=tuple(sorted(ids_by_callback[key])),
            slot_uses=int(slot_uses_by_callback[key]), templates=len(templates_by_callback[key]), status=status)
        if status == "closed_conditional_runtime":
            row.update(capability_kind=CONDITIONAL_CAPABILITY_KIND, scope=CONDITIONAL_CAPABILITY_SCOPE,
                       command_entry_reachability="OPEN_SEPARATE_AXIS_NOT_INFERRED")
        rows.append(row)

    open_rows=tuple(row for row in rows if row["status"]=="open")
    return {
        "rows":tuple(rows),
        "conditional_placements":tuple(sorted(qualified)),
        "total_positive_slot_uses":total_positive,
        "unresolved_skill_ids":tuple(sorted(unresolved_ids)),
        "next_open":(None if not open_rows else open_rows[0]),
    }


def analyze(data_dir:Path,setup:Path|None):
    petskills = load_recovered25_petskill_runtime(data_dir=data_dir,setup=setup)
    enemybase = load_recovered25_enemybase_runtime(data_dir=data_dir,setup=setup)
    identity = verify_placement_population(petskills, enemybase, data_dir=data_dir, setup=setup)
    return analyze_runtime_objects(petskills, enemybase, capability_identity=identity)


def summarize_pressure(result):
    return dict(total=result["total_positive_slot_uses"],
        closed=sum(row["slot_uses"] for row in result["rows"] if row["status"] in CLOSED_PRESSURE_STATUSES),
        open=sum(row["slot_uses"] for row in result["rows"] if row["status"] == "open"),
        historical_ub=sum(row["slot_uses"] for row in result["rows"] if row["status"] == "historical_ub"))


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
    totals = summarize_pressure(result)
    print("CAPABILITY_PRESSURE|" + "|".join(f"{key}={value}" for key, value in totals.items()))
    for tempno, slot, skill_id in result["conditional_placements"]:
        print(f"CONDITIONAL_PLACEMENT|template={tempno}|runtime_slot={slot}|report_slot={slot+1}|skill_id={skill_id}|capability={CONDITIONAL_CAPABILITY_KIND}")
    if result["conditional_placements"]:
        print("REACHABILITY|conditional_capability_does_not_certify_natural_AI_or_pet_magic_NPC_script_entry")
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
