#!/usr/bin/env python3
"""Audit the shared Lighttakeed DamageReact counter lifecycle at fixed pins."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess

from tools.stoneage_guard_break2_source_audit import (
    PINNED, LAYOUTS, _function, _sha, _text, _compact,
)
from tools.stoneage_lighttakeed_source_audit import (
    CALLBACK_NAME,
    COMMAND_NAME,
    FEATURE_NAME,
    _case_block,
)


COUNTERS=(
    ("vanish","CHAR_WORKDAMAGEVANISH","BATTLE_MD_VANISH"),
    ("absrob","CHAR_WORKDAMAGEABSROB","BATTLE_MD_ABSROB"),
    ("reflec","CHAR_WORKDAMAGEREFLEC","BATTLE_MD_REFLEC"),
)


def analyze_profile(name: str, root: Path):
    root=Path(root).resolve()
    actual=subprocess.check_output(
        ["git","-C",str(root),"rev-parse","HEAD"],text=True
    ).strip()
    dirty=subprocess.check_output(
        ["git","-C",str(root),"status","--porcelain"],text=True
    ).strip()
    if actual != PINNED[name] or dirty:
        raise ValueError(f"{name} source identity/tree drift")

    base=root/LAYOUTS[name]
    paths={
        "battle":base/"battle/battle.c",
        "event":base/"battle/battle_event.c",
        "magic":base/"battle/battle_magic.c",
        "pet":base/"battle/pet_skill.c",
        "version":base/"include/version.h",
        "char_h":base/"include/char_base.h",
    }
    data={key:_text(path) for key,path in paths.items()}
    battle=_compact(data["battle"]).replace("char_index","charaindex")
    event=_compact(data["event"]).replace("char_index","charaindex")
    magic=_compact(data["magic"]).replace("char_index","charaindex")

    new_entry=_compact(
        _function(data["battle"],"int BATTLE_NewEntry")
    ).replace("char_index","charaindex")
    get_react=_compact(
        _function(data["event"],"int BATTLE_GetDamageReact")
    ).replace("char_index","charaindex")
    damage_sub=_compact(
        _function(data["event"],"int BATTLE_DamageSub")
    ).replace("char_index","charaindex")
    multi_magic_def=_compact(
        _function(data["magic"],"void BATTLE_MultiMagicDef")
    ).replace("char_index","charaindex")

    damage_start=event.find("intBATTLE_S_AttackDamage(")
    lighttake_start=event.find("case"+COMMAND_NAME+":",damage_start)
    if damage_start < 0 or lighttake_start < 0:
        raise ValueError("missing AttackDamage/Lighttake boundaries")
    attack_damage=event[damage_start:]
    lighttake_case=_case_block(
        event[lighttake_start:],"case"+COMMAND_NAME+":"
    )

    priority_positions=[
        get_react.find("CHAR_WORKDAMAGEVANISH"),
        get_react.find("CHAR_WORKDAMAGEABSROB"),
        get_react.find("CHAR_WORKDAMAGEREFLEC"),
    ]
    react_read=attack_damage.find("ReactType=BATTLE_GetDamageReact(defindex)")
    lifecycle_positions={
        "react_read":react_read,
        "match_zero":attack_damage.find("react=0",react_read+1),
        "attackseq":attack_damage.find("BATTLE_AttackSeq("),
        "damagesub":attack_damage.find("BATTLE_DamageSub("),
        "reflect_redirect":attack_damage.find(
            "if(react==BATTLE_MD_REFLEC)defindex=attackindex"
        ),
        "defineattack":attack_damage.find("BATTLE_DefineAttack("),
        "lighttake_case":attack_damage.find("case"+COMMAND_NAME+":"),
    }
    ordered=all(value >= 0 for value in lifecycle_positions.values()) and (
        lifecycle_positions["react_read"]
        < lifecycle_positions["match_zero"]
        < lifecycle_positions["attackseq"]
        < lifecycle_positions["damagesub"]
        < lifecycle_positions["reflect_redirect"]
        < lifecycle_positions["defineattack"]
        < lifecycle_positions["lighttake_case"]
    )

    transfer_style="copy_plus_one" if name=="bismarck" else "copy"
    transfer_ok=True
    for _,work,_ in COUNTERS:
        read=f"Typenum=CHAR_getWorkInt(defindex,{work})"
        write=(
            f"CHAR_setWorkInt(attackindex,{work},Typenum+1)"
            if transfer_style=="copy_plus_one"
            else f"CHAR_setWorkInt(attackindex,{work},Typenum)"
        )
        transfer_ok &= read in lighttake_case and write in lighttake_case

    decrements={}
    for label,work,kind in COUNTERS:
        decrements[label]=(
            f"CHAR_getWorkInt(defindex,{work})-1" in damage_sub
            and f"CHAR_setWorkInt(defindex,{work},max(work,0))" in damage_sub
            and kind in damage_sub
        )

    gates={
        "entry_zeroes_all_three":all(
            f"CHAR_setWorkInt(charaindex,{work},0)" in new_entry
            for _,work,_ in COUNTERS
        ),
        "magicdef_direct_overwrite":
            "CHAR_setWorkInt(toindex,MagicDefTbl[kind],count)" in multi_magic_def,
        "reaction_priority_vanish_absrob_reflec":
            all(x >= 0 for x in priority_positions)
            and priority_positions==sorted(priority_positions),
        "damage_sub_zero_damage_returns_before_reaction":
            damage_sub.find("if(damage<=0)return0")
            < damage_sub.find("BATTLE_GetDamageReact(defindex)"),
        "damage_sub_refetches_reaction_when_preflect_not_minus_one":
            "if(*pRefrect!=-1){react=BATTLE_GetDamageReact(defindex);}"
            in damage_sub,
        "damage_sub_decrements_all_three":
            all(decrements.values()),
        "reflect_throwing_bypass_precedes_reflect_decrement":
            damage_sub.find("BATTLE_IsThrowWepon(")
            < damage_sub.find("CHAR_WORKDAMAGEREFLEC)-1"),
        "attackdamage_lighttake_full_order":ordered,
        "post_damage_transfer_profile_matches":transfer_ok,
        "lighttake_case_has_no_damage_guard":
            "damage>0" not in lighttake_case and "damage<=0" not in lighttake_case,
        "lighttake_case_no_rng":
            "RAND(" not in lighttake_case and "rand(" not in lighttake_case,
    }
    failed={key:value for key,value in gates.items() if not value}
    if failed:
        raise ValueError(f"{name} Lighttakeed lifecycle gates failed: {failed}")

    return {
        "profile":name,
        "commit":actual,
        "transfer_style":transfer_style,
        "gates":gates,
        "hashes":{key:_sha(path) for key,path in paths.items()},
    }


def emit(rows):
    print("StoneAge Lighttakeed DamageReact lifecycle source audit — R1")
    print("Derived facts only; no original source text/assets stored.")
    for row in rows:
        print(
            "PROFILE|"
            f"name={row['profile']}|sha={row['commit']}|"
            f"counter_transfer_style={row['transfer_style']}"
        )
        for key,value in sorted(row["gates"].items()):
            print(
                f"GATE|profile={row['profile']}|name={key}|pass={int(value)}"
            )
        for key,value in sorted(row["hashes"].items()):
            print(
                f"SOURCE_SHA256|profile={row['profile']}|"
                f"file={key}|sha256={value}"
            )

    print("FACT|battle_entry_initializes_absrob_reflec_vanish_to_zero")
    print("FACT|magic_def_application_overwrites_selected_counter_with_count")
    print("FACT|active_reaction_priority=VANISH_then_ABSROB_then_REFLEC")
    print("FACT|positive_damage_reloads_active_reaction_inside_DamageSub")
    print("FACT|ordinary_nonthrowing_active_reaction_consumes_one_counter_clamped_zero")
    print("FACT|matching_Lighttake_local_react_zero_does_not_skip_DamageSub_refetch")
    print("FACT|positive_damage_VANISH_ABSROB_transfer_observes_defender_after_one_charge_consumption")
    print("FACT|positive_damage_REFLEC_nonthrowing_redirects_defindex_to_attacker_before_Lighttake_post_branch")
    print("FACT|positive_damage_REFLEC_gavin_iris_post_branch_is_attacker_counter_self_copy")
    print("FACT|positive_damage_REFLEC_bismarck_post_branch_increments_attacker_counter_by_one")
    print("FACT|zero_damage_returns_before_refetch_and_Lighttake_post_branch_still_has_no_damage_guard")
    print("BOUNDARY|throwing_weapon_REFLEC_bypasses_charge_consumption_and_redirect_then_post_branch_reads_defender")
    print("BOUNDARY|recovered25_positive_users_are_enemybase_rows_but_original_binary_profile_remains_open")
    print("RESOLUTION|LIGHTTAKEED_DAMAGEREACT_LIFECYCLE_FIXED_SOURCE_CLOSED")


def main():
    parser=argparse.ArgumentParser()
    for name in PINNED:
        parser.add_argument("--"+name+"-dir",type=Path,required=True)
    args=parser.parse_args()
    emit([
        analyze_profile(name,getattr(args,name+"_dir"))
        for name in PINNED
    ])


if __name__=="__main__":
    main()
