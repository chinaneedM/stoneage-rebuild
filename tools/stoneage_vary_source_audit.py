"""Pinned descendant PETSKILL_Vary source audit; derived facts only."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import subprocess

from tools.stoneage_guard_break2_source_audit import (
    PINNED, LAYOUTS, _sha, _text, _function, _compact, _macro_int,
)
CALLBACK_NAME="PETSKILL_Vary"
COMMAND_NAME="BATTLE_COM_S_VARY"
FEATURE_NAME="_VARY_WOLF"
EXPANSION_NAME="_EXPANSION_VARY_WOLF"
SOURCE_PETSKILL_SYMBOL_NAME="PETSKILL_VARY"


def _active_macros(version: Path, includes: list[str]) -> set[str]:
    out=subprocess.check_output(
        ["cpp","-dM",*includes,str(version)],text=True
    )
    return set(re.findall(r"^#define\s+(\w+)",out,re.M))


def _bounded_case(text: str, marker: str, occurrence: int) -> str:
    positions=[]
    pos=0
    while True:
        pos=text.find(marker,pos)
        if pos < 0:
            break
        positions.append(pos)
        pos+=len(marker)
    if len(positions) <= occurrence:
        raise ValueError(f"missing case occurrence {occurrence}: {marker}")
    start=positions[occurrence]
    next_case=text.find("case",start+len(marker))
    if next_case < 0:
        next_case=min(len(text),start+12000)
    return text[start:next_case]


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
        "pet":base/"battle/pet_skill.c",
        "battle":base/"battle/battle.c",
        "enemy":base/"char/enemy.c",
        "version":base/"include/version.h",
        "battle_h":base/"include/battle.h",
        "petskill_h":base/"include/pet_skillinfo.h",
    }
    data={key:_text(path) for key,path in paths.items()}
    includes=["-I",str(base/"include")]
    if name=="bismarck":
        includes += ["-I",str(root/"server/common"),"-I",str(root/"shared/lua51")]
    active=_active_macros(paths["version"],includes)
    source_skill_id=_macro_int(
        data["petskill_h"],SOURCE_PETSKILL_SYMBOL_NAME
    )
    callback=_compact(_function(
        data["pet"],"int "+CALLBACK_NAME
    )).replace("char_index","cindex")
    pet_compact=_compact(data["pet"])
    battle_compact=_compact(data["battle"]).replace("char_index","charaindex")
    setup_case=_bounded_case(
        battle_compact,"case"+COMMAND_NAME+":",0
    )
    action_case=_bounded_case(
        battle_compact,"case"+COMMAND_NAME+":",1
    )
    enemy_compact=_compact(data["enemy"])

    expansion_active=EXPANSION_NAME in active
    expected_expansion=False
    option_guard=(
        "string_literal_nul"
        if name=="bismarck"
        else "null_pointer"
    )
    expected_guard=(
        'strcmp(pszOption,"\\0")==0'
        if name=="bismarck"
        else "pszOption==NULL"
    )
    expected_effect=(
        False if name=="bismarck" and not expansion_active else True
    )
    has_effect="BATTLE_MagicEffect(" in action_case
    # Raw Bismarck source contains the expansion branch even when it is
    # compiled out. The compiled profile truth is captured separately.
    raw_effect_guarded=(
        name=="bismarck"
        and "#ifdef_EXPANSION_VARY_WOLF" in action_case
    )

    gates={
        "feature_active":FEATURE_NAME in active,
        "expansion_profile_is_explicit":
            expansion_active==expected_expansion,
        "callback_registered":
            '{"PETSKILL_Vary",PETSKILL_Vary,0}' in pet_compact,
        "source_skill_symbol_is_600":source_skill_id==600,
        "command_symbol_present":
            COMMAND_NAME in data["battle_h"],
        "mode_symbol_present":
            "BATTLE_CHARMODE_C_OK" in data["battle_h"],
        "callback_sets_command_target_mode":all(
            token in callback for token in (
                "CHAR_WORKBATTLECOM1,"+COMMAND_NAME,
                "CHAR_WORKBATTLECOM2,tindex",
                "CHAR_WORKBATTLEMODE,BATTLE_CHARMODE_C_OK",
            )
        ),
        "base_profile_restricts_tempno_981_984":all(
            token in callback
            for token in (
                "981","982","983","984","CHAR_PETID"
            )
        ) and "i>=4" in callback,
        "petid_is_loaded_from_enemy_tempno":
            "CharNew.data[CHAR_PETID]=*(tp+E_T_TEMPNO)" in enemy_compact,
        "option_guard_matches_profile":expected_guard in callback,
        "attack_marker_present":'strstr(pszOption,"攻%")' in callback,
        "quick_marker_present":'strstr(pszOption,"敏%")' in callback,
        "bismarck_defense_divergence_explicit":
            ('strstr(pszOption,"防%")' in callback)==(name=="bismarck"),
        "fixed_default_image_101428":
            "CHAR_BASEIMAGENUMBER,101428" in callback,
        "workturn_reset_zero":"CHAR_WORKTURN,0" in callback,
        "setup_case_is_noop":
            "先用不到" in setup_case or "break;" in setup_case,
        "action_target_adjust":
            "BATTLE_TargetAdjust(" in action_case,
        "action_has_no_physical_attack":
            "BATTLE_Attack(" not in action_case
            and "BATTLE_S_AttackDamage(" not in action_case,
        "action_effect_profile_accounted":
            (
                (name!="bismarck" and has_effect)
                or (
                    name=="bismarck"
                    and raw_effect_guarded
                    and not expansion_active
                )
            ),
    }
    failed={k:v for k,v in gates.items() if not v}
    if failed:
        raise ValueError(f"{name} Vary source gates failed: {failed}")

    return {
        "profile":name,
        "commit":actual,
        "source_skill_id":source_skill_id,
        "command_symbol":COMMAND_NAME,
        "mode_symbol":"BATTLE_CHARMODE_C_OK",
        "expansion_active":expansion_active,
        "option_guard":option_guard,
        "defense_marker":'strstr(pszOption,"防%")' in callback,
        "compiled_magic_effect":expected_effect,
        "gates":gates,
        "hashes":{key:_sha(path) for key,path in paths.items()},
    }


def emit(rows):
    print("StoneAge PETSKILL_Vary fixed-source audit — R1")
    print("Derived facts only; no original source text/assets stored.")
    for row in rows:
        print(
            "PROFILE|"
            f"name={row['profile']}|sha={row['commit']}|"
            f"source_skill_id={row['source_skill_id']}|"
            f"command_symbol={row['command_symbol']}|"
            f"mode_symbol={row['mode_symbol']}|"
            f"expansion_active={int(row['expansion_active'])}|"
            f"option_guard={row['option_guard']}|"
            f"defense_marker={int(row['defense_marker'])}|"
            f"compiled_magic_effect={int(row['compiled_magic_effect'])}"
        )
        for key,value in sorted(row["gates"].items()):
            print(f"GATE|profile={row['profile']}|name={key}|pass={int(value)}")
        for key,value in sorted(row["hashes"].items()):
            print(f"SOURCE_SHA256|profile={row['profile']}|file={key}|sha256={value}")
    print("FACT|runtime_CHAR_PETID_is_enemybase_TEMPNO")
    print("FACT|base_allowed_tempnos=981,982,983,984")
    print("FACT|callback_writes_command_target_mode_and_resets_workturn")
    print("FACT|gavin_iris_option_markers=attack,quick")
    print("FACT|bismarck_adds_defense_marker")
    print("BOUNDARY|EXPANSION_VARY_WOLF_inactive_at_all_three_fixed_pins")
    print("BOUNDARY|bismarck_raw_expansion_image_branch_not_compiled_at_fixed_pin")
    print("BOUNDARY|original_numeric_command_and_mode_values_open")
    print("BOUNDARY|original_binary_compile_profile_and_charset_open")
    print("RESOLUTION|VARY_FIXED_SOURCE_FIRST_PASS_CLOSED_BOUNDED_REFERENCE")


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
