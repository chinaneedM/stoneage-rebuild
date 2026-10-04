"""Reproduce PETSKILL_BattleTimid facts at three pinned descendant commits."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import subprocess

from tools.stoneage_guard_break2_source_audit import (
    PINNED, LAYOUTS, _function, _sha, _text, _compact,
)
from tools.stoneage_weaken_source_audit import _enum_values
from tools.stoneage_battletimid_model import (
    CALLBACK_NAME, COMMAND_NAME, FEATURE_NAME,
)


def _case_block(text: str, marker: str) -> str:
    start=text.find(marker)
    if start < 0:
        raise ValueError("missing case "+marker)
    brace=text.find("{",start)
    if brace < 0:
        raise ValueError("missing case block")
    depth=0
    state="code"
    i=brace
    while i < len(text):
        ch=text[i]
        nxt=text[i+1] if i+1 < len(text) else ""
        if state=="code":
            if ch=="/" and nxt=="/":
                state="line"; i+=2; continue
            if ch=="/" and nxt=="*":
                state="block"; i+=2; continue
            if ch=='"':
                state="string"; i+=1; continue
            if ch=="'":
                state="char"; i+=1; continue
            if ch=="{":
                depth+=1
            elif ch=="}":
                depth-=1
                if depth==0:
                    return text[start:i+1]
        elif state=="line":
            if ch=="\n": state="code"
        elif state=="block":
            if ch=="*" and nxt=="/":
                state="code"; i+=2; continue
        elif state=="string":
            if ch=="\\": i+=2; continue
            if ch=='"': state="code"
        elif state=="char":
            if ch=="\\": i+=2; continue
            if ch=="'": state="code"
        i+=1
    raise ValueError("unterminated case block")


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
        "event":base/"battle/battle_event.c",
        "version":base/"include/version.h",
        "battle_h":base/"include/battle.h",
        "char_h":base/"include/char_base.h",
    }
    data={key:_text(path) for key,path in paths.items()}
    includes=["-I",str(base/"include")]
    if name=="bismarck":
        includes += ["-I",str(root/"server/common"),"-I",str(root/"shared/lua51")]
    macros=subprocess.check_output(
        ["cpp","-dM",*includes,str(paths["version"])],text=True
    )
    active=set(re.findall(r"^#define\s+(\w+)",macros,re.M))
    enums=_enum_values([COMMAND_NAME,"BATTLE_CHARMODE_C_OK"],includes)

    callback=_compact(_function(data["pet"],"int "+CALLBACK_NAME)).replace(
        "char_index","charaindex"
    )
    target_start=data["battle"].find("void BATTLE_TargetListSet")
    target_end=data["battle"].find("int BATTLE_GetAttackCount",target_start)
    if target_start < 0 or target_end < 0:
        raise ValueError("missing bounded TargetListSet slice")
    target_list=_compact(data["battle"][target_start:target_end]).replace(
        "char_index","charaindex"
    )
    dispatch=_compact(data["battle"]).replace("char_index","charaindex")
    start=dispatch.find("case"+COMMAND_NAME+":")
    if start < 0:
        raise ValueError("missing compiled-source dispatch case text")
    dispatch=dispatch[start:].split("#endif",1)[0]
    damage_start=data["event"].find("int BATTLE_S_AttackDamage")
    event_start=data["event"].find("case "+COMMAND_NAME+":",damage_start)
    if damage_start < 0 or event_start < 0:
        raise ValueError("missing bounded AttackDamage/TIMID slice")
    attack_damage=_compact(data["event"][damage_start:event_start]).replace(
        "char_index","charaindex"
    )
    event_case=_compact(_case_block(
        data["event"][event_start:],"case "+COMMAND_NAME+":"
    )).replace("char_index","charaindex")

    expected_same_side_guard=name in {"gavin","iris"}
    compiled_same_side_guard="_SKILLLIMIT" in active
    gates={
        "feature_active":FEATURE_NAME in active,
        "pets_selectcon_active":"_PETS_SELECTCON" in active,
        "callback_rejects_player":
            "CHAR_WHICHTYPE)==CHAR_TYPEPLAYER)returnFALSE" in callback,
        "callback_sets_command_target_mode":all(token in callback for token in (
            "CHAR_WORKBATTLECOM1,"+COMMAND_NAME,
            "CHAR_WORKBATTLECOM2,toNo",
            "CHAR_WORKBATTLEMODE,BATTLE_CHARMODE_C_OK",
        )),
        "callback_fixed_attack_70":
            "CHAR_WORKFIXSTR)*0.7" in callback,
        "callback_fixed_defence_40":
            "CHAR_WORKFIXTOUGH)*0.4" in callback,
        "callback_fixed_quick_80":
            "CHAR_WORKFIXDEX)*0.8" in callback,
        "callback_packs_skill_array_low":
            "CHAR_SETWORKINT_LOW(charaindex,CHAR_WORKBATTLECOM3,array)" in callback,
        "callback_does_not_read_option":
            "PETSKILL_getChar" not in callback,
        "target_list_source_contains_same_side_timid_gate":all(
            token in target_list for token in (
                COMMAND_NAME,
                "BATTLE_CheckSameSide",
                "BATTLE_COM_NONE",
            )
        ),
        "compiled_same_side_guard_profile_matches":
            compiled_same_side_guard==expected_same_side_guard,
        "dispatch_target_adjust_then_attackdamage":
            dispatch.find("BATTLE_TargetAdjust(") >= 0
            and dispatch.find("BATTLE_S_AttackDamage(") >
                dispatch.find("BATTLE_TargetAdjust("),
        "dispatch_passes_low_skill_and_timid_command":all(token in dispatch for token in (
            "CHAR_GETWORKINT_LOW(charaindex,CHAR_WORKBATTLECOM3)",
            "BATTLE_S_AttackDamage(",
            COMMAND_NAME,
        )),
        "attackdamage_common_requires_nonnull_option":all(
            token in attack_damage for token in (
                "PETSKILL_getChar(skill,PETSKILL_OPTION)",
                "if(pszP==NULL)returniRet",
            )
        ),
        "event_consumes_raw_rand_mod_100":
            "inttimid=rand()%100" in event_case and "RAND(" not in event_case,
        "event_draw_precedes_damage_gate":
            event_case.find("rand()%100") < event_case.find("timid<15&&damage>1"),
        "event_strict_15_and_damage_gt_1":
            "if(timid<15&&damage>1)" in event_case,
        "event_emits_hit_before_exit_gate":
            event_case.find("BH|a%X|r%X|f%X|d%X|p%X|FF|") <
            event_case.find("if(timid<15&&damage>1)"),
        "event_noaction_and_exit_frames":all(token in event_case for token in (
            "BATTLE_NoAction(battleindex,defNo)",
            '"BE|e%X|"',
            '"f%X|"',
        )),
        "pet_exit_clears_owner_default_pet":all(token in event_case for token in (
            "CHAR_TYPEPET",
            "BATTLE_PetDefaultExit(",
            "CHAR_DEFAULTPET,-1",
        )),
        "nonpet_exit_and_party_discharge":all(token in event_case for token in (
            "BATTLE_Exit(defindex,battleindex)",
            "CHAR_DischargePartyNoMsg(defindex)",
        )),
    }
    failed={key:value for key,value in gates.items() if not value}
    if failed:
        raise ValueError(f"{name} BattleTimid source gates failed: {failed}")
    return {
        "profile":name,
        "commit":actual,
        "command_value":enums[COMMAND_NAME],
        "mode_value":enums["BATTLE_CHARMODE_C_OK"],
        "same_side_guard_compiled":compiled_same_side_guard,
        "gates":gates,
        "hashes":{key:_sha(path) for key,path in paths.items()},
    }


def emit(rows):
    print("StoneAge BattleTimid fixed-source audit — R1")
    print("Derived facts only; no original source text or assets are stored.")
    print("Common runtime-safe target domain is opposite-side only.")
    for row in rows:
        print(
            "PROFILE|"
            f"name={row['profile']}|sha={row['commit']}|"
            f"command_value={row['command_value']}|"
            f"mode_value={row['mode_value']}|"
            f"same_side_guard_compiled={int(row['same_side_guard_compiled'])}"
        )
        for key,value in sorted(row["gates"].items()):
            print(f"GATE|profile={row['profile']}|name={key}|pass={int(value)}")
        for key,value in sorted(row["hashes"].items()):
            print(f"SOURCE_SHA256|profile={row['profile']}|file={key}|sha256={value}")
    print("FACT|callback_fixed_work_powers=attack70_defence40_quick80")
    print("FACT|post_damage_rng=raw_rand_mod_100_always_one_draw")
    print("FACT|forced_exit=draw_lt_15_and_damage_gt_1")
    print("FACT|pet_exit=default_pet_exit_and_owner_defaultpet_minus_one")
    print("FACT|nonpet_exit=battle_exit_and_party_discharge")
    print("BOUNDARY|same_side_gate=gavin_iris_on_bismarck_off")
    print("BOUNDARY|original_binary_compile_profile_and_numeric_command_open")
    print("RESOLUTION|BATTLETIMID_FIXED_SOURCE_CLOSED_OPPOSITE_SIDE_REFERENCE")


def main():
    parser=argparse.ArgumentParser()
    for name in PINNED:
        parser.add_argument("--"+name+"-dir",type=Path,required=True)
    args=parser.parse_args()
    emit([analyze_profile(name,getattr(args,name+"_dir")) for name in PINNED])


if __name__=="__main__":
    main()
