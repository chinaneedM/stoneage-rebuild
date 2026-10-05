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
FIXWOLF_NAME="_FIXWOLF"
SOURCE_PETSKILL_SYMBOL_NAME="PETSKILL_VARY"


def _active_macros(version: Path, includes: list[str]) -> set[str]:
    out=subprocess.check_output(
        ["cpp","-dM",*includes,str(version)],text=True
    )
    return set(re.findall(r"^#define\s+(\w+)",out,re.M))


def _last_brace_block(text: str, marker: str) -> str:
    start=text.rfind(marker)
    if start < 0:
        raise ValueError("missing lifecycle marker: "+marker)
    brace=text.find("{",start)
    if brace < 0:
        raise ValueError("missing lifecycle brace")
    depth=0
    index=brace
    while index < len(text):
        ch=text[index]
        if ch=="{":
            depth+=1
        elif ch=="}":
            depth-=1
            if depth==0:
                return text[start:index+1]
        index+=1
    raise ValueError("unterminated lifecycle block")


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
        "battle_magic":base/"battle/battle_magic.c",
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
    direct_use=_compact(_function(
        data["pet"],"int PETSKILL_Use"
    )).replace("char_index","charaindex")
    dexcalc=_compact(_function(
        data["battle"],"int BATTLE_DexCalc"
    )).replace("char_index","charaindex")
    magic_effect=_compact(_function(
        data["battle_magic"],"int BATTLE_MagicEffect"
    )).replace("char_index","charaindex")
    pet_compact=_compact(data["pet"])
    battle_compact=_compact(data["battle"]).replace("char_index","charaindex")
    setup_case=_bounded_case(
        battle_compact,"case"+COMMAND_NAME+":",0
    )
    action_case=_bounded_case(
        battle_compact,"case"+COMMAND_NAME+":",1
    )
    enemy_compact=_compact(data["enemy"])
    vary_lifecycle=_last_brace_block(
        battle_compact,
        "if(CHAR_getInt(charaindex,CHAR_BASEIMAGENUMBER)==101428",
    )

    expansion_active=EXPANSION_NAME in active
    fixwolf_active=FIXWOLF_NAME in active
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
        "fixwolf_active_at_fixed_pin":fixwolf_active,
        "callback_registered":
            '{"PETSKILL_Vary",PETSKILL_Vary,0}' in pet_compact,
        "source_skill_symbol_is_600":source_skill_id==600,
        "command_symbol_present":
            COMMAND_NAME in data["battle_h"],
        "mode_symbol_present":
            "BATTLE_CHARMODE_C_OK" in data["battle_h"],
        "use_blocks_recast_while_default_wolf_image":all(
            token in direct_use for token in (
                "petskillid==600",
                "CHAR_BASEIMAGENUMBER)==101428",
                "petskillid=-1",
            )
        ),
        "vary_has_no_special_dexcalc_branch":
            COMMAND_NAME not in dexcalc,
        "magic_effect_is_visual_frame_only":all(
            token in magic_effect for token in (
                '"BJ|a%X|m%X|e%X|e%X|"',
                "BATTLESTR_ADD(",
                '"FF|"',
            )
        ) and all(
            token not in magic_effect
            for token in (
                "CHAR_setWorkInt(","CHAR_setInt(",
                "BATTLE_Attack(","BATTLE_S_AttackDamage(",
            )
        ),
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
        "turn_counter_increments_while_wolf":
            "CHAR_WORKTURN)==0" in vary_lifecycle
            and "CHAR_WORKTURN)+1" in vary_lifecycle,
        "turn_counter_expires_after_five":
            "CHAR_WORKTURN)>5" in vary_lifecycle,
        "expiry_restores_base_image":
            "CHAR_BASEIMAGENUMBER,CHAR_getInt(charaindex,CHAR_BASEBASEIMAGENUMBER)" in vary_lifecycle,
        "expiry_restores_attack":
            "CHAR_WORKATTACKPOWER,CHAR_getWorkInt(charaindex,CHAR_WORKFIXSTR)" in vary_lifecycle,
        "expiry_restores_quick":
            "CHAR_WORKQUICK,CHAR_getWorkInt(charaindex,CHAR_WORKFIXDEX)" in vary_lifecycle,
        "expiry_defense_divergence_explicit":
            (
                "CHAR_WORKDEFENCEPOWER,CHAR_getWorkInt(charaindex,CHAR_WORKFIXTOUGH)"
                in vary_lifecycle
            )==(name=="bismarck"),
        "battle_end_restores_nonbase_image":
            "CHAR_BASEBASEIMAGENUMBER)!=CHAR_getInt(petindex,CHAR_BASEIMAGENUMBER)" in battle_compact,
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
        "fixwolf_active":fixwolf_active,
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
            f"fixwolf_active={int(row['fixwolf_active'])}|"
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
    print("FACT|PETSKILL_Use_blocks_recast_while_image_101428")
    print("FACT|Vary_has_no_special_BATTLE_DexCalc_branch")
    print("FACT|BATTLE_MagicEffect_is_visual_frame_only")
    print("FACT|wolf_turn_counter_reverts_after_six_actor_actions")
    print("FACT|gavin_iris_option_markers=attack,quick")
    print("FACT|bismarck_adds_defense_marker")
    print("BOUNDARY|expiry_restore=gavin_iris_attack_quick_bismarck_attack_defense_quick")
    print("BOUNDARY|EXPANSION_VARY_WOLF_inactive_at_all_three_fixed_pins")
    print("FACT|FIXWOLF_active_at_all_three_fixed_pins")
    print("BOUNDARY|bismarck_raw_expansion_image_branch_not_compiled_at_fixed_pin")
    print("BOUNDARY|original_numeric_command_and_mode_values_open")
    print("BOUNDARY|original_binary_compile_profile_and_charset_open")
    print("RESOLUTION|VARY_FIXED_SOURCE_CLOSED_BOUNDED_REFERENCE")


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
