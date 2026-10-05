#!/usr/bin/env python3
"""Pinned BattleModel callback/dispatcher/effect source audit.

Only source hashes, descendant enum values, and semantic booleans are emitted.
Original source text is recovered transiently by CI and is never copied into
this reconstruction repository.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import subprocess

from tools.stoneage_guard_break2_source_audit import (
    PINNED, LAYOUTS, _text, _sha, _compact,
)
from tools.stoneage_mdfyattack_source_audit import _definition, _strip
from tools.stoneage_battletimid_source_audit import _case_block
from tools.stoneage_weaken_source_audit import _enum_values

CALLBACK_NAME="PETSKILL_BattleModel"
COMMAND_NAME="BATTLE_COM_S_BATTLE_MODEL"
FEATURE_NAME="_PETSKILL_BATTLE_MODEL"


def _normalized_identifier(text:str)->str:
    return text.replace("char_index","charaindex")


def analyze_profile(name:str,root:Path):
    root=Path(root).resolve()
    sha=subprocess.check_output(
        ["git","-C",str(root),"rev-parse","HEAD"],text=True
    ).strip()
    dirty=subprocess.check_output(
        ["git","-C",str(root),"status","--porcelain"],text=True
    ).strip()
    if sha!=PINNED[name] or dirty:
        raise ValueError("pinned source commit/tree drift")

    base=root/LAYOUTS[name]
    paths={
        "pet":base/"battle/pet_skill.c",
        "battle":base/"battle/battle.c",
        "event":base/"battle/battle_event.c",
        "battle_h":base/"include/battle.h",
        "version":base/"include/version.h",
    }
    data={key:_text(path) for key,path in paths.items()}
    includes=["-I",str(base/"include")]
    if name=="bismarck":
        includes += [
            "-I",str(root/"server/common"),
            "-I",str(root/"shared/lua51"),
        ]
    macros=subprocess.check_output(
        ["cpp","-dM",*includes,str(paths["version"])],text=True
    )
    active=set(re.findall(r"^#define\s+(\w+)",macros,re.M))
    feature_active=FEATURE_NAME in active
    enum_includes=includes if feature_active else includes+["-D"+FEATURE_NAME]
    enums=_enum_values(
        [COMMAND_NAME,"BATTLE_CHARMODE_C_OK"],
        enum_includes,
    )

    callback=_compact(_strip(_definition(data["pet"],CALLBACK_NAME)))
    callback=_normalized_identifier(callback)
    # raw_window avoids the shared helper's prefix re-search accidentally
    # resolving the earlier BATTLE_BattleModel_ATTACK definition.
    effect=_compact(_strip(_definition(
        data["event"],"BATTLE_BattleModel",raw_window=True
    )))
    effect=_normalized_identifier(effect)
    attack=_compact(_strip(_definition(data["event"],"BATTLE_BattleModel_ATTACK")))
    attack=_normalized_identifier(attack)
    damage=_compact(_strip(_definition(data["event"],"BATTLE_DamageSub")))
    damage=_normalized_identifier(damage)

    case_at=data["battle"].find("case "+COMMAND_NAME+":")
    if case_at < 0:
        raise ValueError("missing BattleModel dispatcher case")
    dispatch=_compact(_strip(
        _case_block(data["battle"][case_at:],"case "+COMMAND_NAME+":")
    ))

    guards={
        "feature_active":feature_active,
        "callback_registered":bool(re.search(
            r'"PETSKILL_BattleModel"\s*,\s*PETSKILL_BattleModel',
            data["pet"],
        )),
        "callback_reads_option":
            "PETSKILL_getChar(array,PETSKILL_OPTION)" in callback,
        "callback_field1_is_type":
            'getStringFromIndexWithDelim(pszOption,"|",1,szData,sizeof(szData))'
            in callback and "iType=atoi(szData)" in callback,
        "callback_field2_is_object_count":
            'getStringFromIndexWithDelim(pszOption,"|",2,szData,sizeof(szData))'
            in callback and "iObjectNum=atoi(szData)" in callback,
        "nonpositive_object_count_owns_rand_1_10":
            "if(iObjectNum<=0)iObjectNum=RAND(1,10)" in callback,
        "object_count_clamps_above_10":
            "elseif(iObjectNum>10)iObjectNum=10" in callback,
        "callback_field6_is_stat_adjustment":
            'getStringFromIndexWithDelim(pszOption,"|",6,szData,sizeof(szData))'
            in callback,
        "field6_uses_two_byte_fixed_offsets":
            'szWord[3][3]={"攻","防","敏"}' in callback
            and 'strstr(szData2,szWord[i])' in callback
            and 'strstr(szData2,"%")' in callback
            and 'sscanf(szData2+3,"%f",&fPer)' in callback
            and 'sscanf(szData2+2,"%f",&fPer)' in callback,
        "all_stat_adjustments_start_from_attackpower":
            "iValue=CHAR_getWorkInt(charaindex,CHAR_WORKATTACKPOWER)" in callback
            and "CHAR_setWorkInt(charaindex,iAddPowerType[i],iValue)" in callback,
        "callback_writes_mode_symbolic_command_type_count_and_array":
            all(token in callback for token in (
                "CHAR_WORKBATTLEMODE,BATTLE_CHARMODE_C_OK",
                "CHAR_WORKBATTLECOM1,BATTLE_COM_S_BATTLE_MODEL",
                "CHAR_SETWORKINT_LOW(charaindex,CHAR_WORKBATTLECOM2,iType)",
                "CHAR_SETWORKINT_HIGH(charaindex,CHAR_WORKBATTLECOM2,iObjectNum)",
                "CHAR_WORKBATTLECOM3,array",
            )),
        "dispatcher_calls_effect_without_targetadjust":
            "BATTLE_BattleModel(battleindex,attackNo,myside)" in dispatch
            and "BATTLE_TargetAdjust" not in dispatch,
        "effect_field3_maps_status_prefix":
            'getStringFromIndexWithDelim(pszOption,"|",3,szData,sizeof(szData))'
            in effect
            and "for(i=1;i<BATTLE_ST_END;i++)" in effect
            and "strncmp(szData,aszStatus[i],2)==0" in effect,
        "effect_fields4_and5_are_turn_and_hit":
            'getStringFromIndexWithDelim(pszOption,"|",4,szData,sizeof(szData))'
            in effect
            and 'getStringFromIndexWithDelim(pszOption,"|",5,szData,sizeof(szData))'
            in effect
            and "iTurn=atoi(szData)" in effect
            and "iEffectHit=atoi(szData)" in effect,
        "effect_field7_requires_one_to_four_action_numbers":
            'getStringFromIndexWithDelim(pszOption,"|",7,szData,sizeof(szData))'
            in effect
            and "for(i=0;i<4;i++)" in effect
            and "iActionNumber[i]=atoi(szData2)" in effect,
        "missing_field7_is_noaction":
            'getStringFromIndexWithDelim(pszOption,"|",7,szData,sizeof(szData))==FALSE'
            in effect
            and "BATTLE_NoAction(battleindex,attackNo)" in effect,
        "action_numbers_cycle_across_attack_objects":
            "AAttackObject[i].actionNumber=iActionNumber[i1]" in effect
            and "if(++i1>=iActionAmount)i1=0" in effect,
        "effect_rebuilds_living_opposing_side":
            "BATTLE_MultiList(battleindex,TARGET_SIDE_0,iToList)" in effect
            and "BATTLE_MultiList(battleindex,TARGET_SIDE_1,iToList)" in effect,
        "effect_reads_type_and_count_from_packed_com2":
            "iType=CHAR_GETWORKINT_LOW(charaindex,CHAR_WORKBATTLECOM2)" in effect
            and "iObjectNum=CHAR_GETWORKINT_HIGH(charaindex,CHAR_WORKBATTLECOM2)"
            in effect,
        "excess_objects_use_one_rand_per_extra_object":
            "AAttackObject[i].target=iToList[RAND(0,i0-1)]" in effect
            and effect.count("RAND(0,i0-1)")==1,
        "type_bit0_extends_coverage_when_objects_are_fewer":
            "if(iType&0x00000001)" in effect,
        "attack_helper_rechecks_target_and_runs_attackseq":
            "BATTLE_TargetCheck(battleindex,pAAttackObject->target)" in attack
            and "BATTLE_AttackSeq(charaindex,iToindex,&iDamage,&iGuardian,-1)"
            in attack,
        "type_bit2_controls_physical_guardian_route":
            attack.count("iType&0x00000004")>=2
            and "iGuardian>=0" in attack,
        "damage_sub_is_marked_with_battlemodel_command":
            "CHAR_setWorkInt(iDefindex,CHAR_NPCWORKINT1,BATTLE_COM_S_BATTLE_MODEL)"
            in attack
            and "CHAR_setWorkInt(iDefindex,CHAR_NPCWORKINT1,iTemp2)" in attack,
        "nonphysical_path_disables_damage_reaction_redirect":
            "else{iTemp=-1;iUltimate=BATTLE_DamageSub" in attack,
        "positive_damage_wakes_before_post_status":
            "BATTLE_DamageWakeUp(battleindex,iDefindex)" in attack
            and attack.find("BATTLE_DamageWakeUp")
                < attack.find("BATTLE_StatusAttackCheck"),
        "post_status_requires_survival_and_positive_damage":
            "if(CHAR_getInt(iDefindex,CHAR_HP)<=0)" in attack
            and "if(iDamage>0&&BATTLE_StatusAttackCheck" in attack,
        "status_check_uses_option_hit_with_fixed_per30":
            "BATTLE_StatusAttackCheck(charaindex,iDefindex,iEffect,iEffectHit,30,1.0,&iTemp)"
            in attack,
        "status_turn_written_and_hard_statuses_clear_command":
            "CHAR_setWorkInt(iDefindex,StatusTbl[iEffect],iTurn)" in attack
            and "BATTLE_ST_PARALYSIS" in attack
            and "BATTLE_ST_SLEEP" in attack
            and "BATTLE_ST_STONE" in attack
            and "BATTLE_ST_BARRIER" in attack
            and "CHAR_WORKBATTLECOM1,BATTLE_COM_NONE" in attack,
        "critical_nonplayer_death_can_own_rand50_ultimate":
            "RAND(1,100)<50" in attack,
        "reflect_return_damage_is_suppressed_for_battlemodel":
            "CHAR_WORKDAMAGEREFLEC" in damage
            and "CHAR_getWorkInt(defindex,CHAR_NPCWORKINT1)==BATTLE_COM_S_BATTLE_MODEL"
            in damage,
        "trap_return_damage_is_suppressed_when_compiled":
            "CHAR_WORKTRAP,0" in damage
            and "CHAR_WORKMODTRAP,0" in damage
            and "BATTLE_COM_S_BATTLE_MODEL" in damage,
        "acupuncture_return_damage_is_suppressed_when_compiled":
            "CHAR_getWorkInt(defindex,CHAR_NPCWORKINT1)!=BATTLE_COM_S_BATTLE_MODEL"
            in damage,
    }
    if not all(guards.values()):
        raise ValueError(
            f"{name} BattleModel source gates failed: "
            f"{[key for key,value in guards.items() if not value]}"
        )
    return {
        "profile":name,
        "sha":sha,
        "feature_active":feature_active,
        "command_value":enums[COMMAND_NAME],
        "mode_value":enums["BATTLE_CHARMODE_C_OK"],
        "gates":guards,
        "hashes":{key:_sha(path) for key,path in paths.items()},
    }


def emit(rows):
    print("StoneAge BattleModel pinned source reference — R1")
    print("Derived facts only; original source is recovered transiently.")
    for row in rows:
        print(
            "PROFILE|"
            f"name={row['profile']}|sha={row['sha']}|"
            f"feature_active={int(row['feature_active'])}|"
            f"command_value={row['command_value']}|"
            f"mode_value={row['mode_value']}"
        )
        for key,value in row["gates"].items():
            print(
                f"GATE|profile={row['profile']}|name={key}|pass={int(value)}"
            )
        for key,value in row["hashes"].items():
            print(
                f"SOURCE_SHA256|profile={row['profile']}|file={key}|sha256={value}"
            )
    print("FACT|callback_OPTION_fields_1_2_drive_type_and_object_count")
    print("FACT|nonpositive_object_count_owns_callback_RAND_1_10_and_count_above10_clamps")
    print("FACT|field6_attack_defense_quick_writes_all_compute_from_current_attackpower_baseline")
    print("FACT|field6_parser_uses_fixed_plus2_plus3_byte_offsets_for_two_byte_literals")
    print("FACT|dispatcher_calls_BATTLE_BattleModel_without_TargetAdjust")
    print("FACT|effect_OPTION_fields_3_4_5_drive_status_turn_hit_and_field7_drives_one_to_four_action_numbers")
    print("FACT|effect_rebuilds_living_opposing_side_and_reads_type_count_from_packed_COM2")
    print("FACT|excess_attack_objects_choose_random_living_targets_with_replacement")
    print("FACT|type_bit0_extends_coverage_when_object_count_is_below_living_target_count")
    print("FACT|each_attack_object_rechecks_target_then_enters_AttackSeq_and_DamageSub")
    print("FACT|type_bit2_controls_physical_guardian_route")
    print("FACT|nonphysical_path_passes_reaction_sentinel_minus1_to_DamageSub")
    print("FACT|BattleModel_marker_suppresses_reflect_trap_acupuncture_return_damage_paths_when_present")
    print("FACT|status_application_requires_positive_damage_and_surviving_target")
    print("FACT|critical_nonplayer_death_can_consume_RAND_1_100_for_ultimate")
    print("FACT|DamageSub_has_BattleModel_specific_reaction_suppression_paths")
    print("BOUNDARY|descendant_numeric_command_is_not_original_build_identity")
    print("BOUNDARY|recovered25_OPTION_semantics_require_explicit_two_byte_profile_cross_audit")
    print("BOUNDARY|no_living_target_with_positive_object_count_reaches_source_RAND_0_minus1_hazard")
    print("RESOLUTION|BATTLEMODEL_FIXED_SOURCE_CLOSED_BOUNDED_REFERENCE")


def main():
    parser=argparse.ArgumentParser()
    for name in PINNED:
        parser.add_argument("--"+name+"-dir",type=Path,required=True)
    args=parser.parse_args()
    rows=[
        analyze_profile(name,getattr(args,name+"_dir"))
        for name in PINNED
    ]
    emit(rows)


if __name__=="__main__":
    main()
