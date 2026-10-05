"""Pinned descendant ENEMYSKILL_ReLife source audit; derived facts only."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import subprocess

from tools.stoneage_guard_break2_source_audit import (
    PINNED, LAYOUTS, _sha, _text, _function, _compact,
)
from tools.stoneage_weaken_source_audit import _enum_values

CALLBACK_NAME="ENEMYSKILL_ReLife"
COMMAND_NAME="BATTLE_COM_S_ENEMYRELIFE"
FEATURE_NAME="_PRO_BATTLEENEMYSKILL"
RELIFE_ITEM_FEATURE="_Item_ReLifeAct"


def _active_macros(version: Path, includes: list[str]) -> set[str]:
    out=subprocess.check_output(
        ["cpp","-dM",*includes,str(version)],text=True
    )
    return set(re.findall(r"^#define\s+(\w+)",out,re.M))


def _case_slice(text: str, marker: str) -> str:
    start=text.find(marker)
    if start < 0:
        raise ValueError("missing dispatch case: "+marker)
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
        "event":base/"battle/battle_event.c",
        "magic":base/"battle/battle_magic.c",
        "version":base/"include/version.h",
        "battle_h":base/"include/battle.h",
        "event_h":base/"include/battle_event.h",
        "petskill_h":base/"include/pet_skillinfo.h",
    }
    data={key:_text(path) for key,path in paths.items()}
    includes=["-I",str(base/"include")]
    if name=="bismarck":
        includes += ["-I",str(root/"server/common"),"-I",str(root/"shared/lua51")]
    active=_active_macros(paths["version"],includes)
    enums=_enum_values([COMMAND_NAME,"BATTLE_CHARMODE_C_OK"],includes)

    pet_compact=_compact(data["pet"]).replace("enemy_index","enemyindex")
    callback=_compact(_function(
        data["pet"],"int "+CALLBACK_NAME
    )).replace("enemy_index","enemyindex")
    event=_compact(_function(
        data["event"],"int BATTLE_E_ENEMYREFILE"
    )).replace("char_index","charaindex")
    dead_index=_compact(_function(
        data["battle"],"int BATTLE_getBattleDieIndex"
    )).replace("char_index","charaindex")
    dead_check=_compact(_function(
        data["battle"],"int BATTLE_TargetCheckDead"
    )).replace("char_index","charaindex")
    resurrect=_compact(_function(
        data["magic"],"void BATTLE_MultiRessurect"
    )).replace("char_index","charaindex")
    battle_compact=_compact(data["battle"]).replace("char_index","charaindex")
    dispatch=_case_slice(
        battle_compact,"case"+COMMAND_NAME+":"
    )

    gates={
        "feature_active":FEATURE_NAME in active,
        "item_relifeflag_active":RELIFE_ITEM_FEATURE in active,
        "callback_registered":
            '{"ENEMYSKILL_ReLife",ENEMYSKILL_ReLife,0}' in pet_compact,
        "callback_sets_command_target_mode":all(
            token in callback for token in (
                "CHAR_WORKBATTLECOM1,"+COMMAND_NAME,
                "CHAR_WORKBATTLECOM2,toNo",
                "CHAR_WORKBATTLEMODE,BATTLE_CHARMODE_C_OK",
            )
        ),
        "callback_does_not_read_option_or_skill_array":
            "PETSKILL_getChar" not in callback
            and "CHAR_SETWORKINT_LOW" not in callback,
        "dispatch_target_adjusts_first":all(
            token in dispatch for token in (
                "BATTLE_TargetAdjust(",
                "BATTLE_NoAction(",
                "BATTLE_E_ENEMYREFILE(",
            )
        ) and dispatch.find("BATTLE_TargetAdjust(") < dispatch.find(
            "BATTLE_E_ENEMYREFILE("
        ),
        "dispatch_falls_back_to_physical_attack":all(
            token in dispatch for token in (
                "if(ContFlg==FALSE)",
                "CHAR_ISATTACKED,1",
                "BATTLE_Attack(",
            )
        ),
        "enemy_helper_scans_enemy_side_dead_slots":all(
            token in event for token in (
                "for(k=10;k<20;k++)",
                "BATTLE_getBattleDieIndex(battleindex,k)",
                "CHAR_ISDIE)==TRUE",
                "ToNoList[j]=k",
            )
        ),
        "enemy_helper_consumes_target_rng":
            "RAND(0,j-1)" in event,
        "pet_helper_uses_carried_target":
            "CHAR_TYPEPET" in event and "toNo=defNo" in event,
        "helper_rejects_other_actor_types":
            "else{returniRet;}" in event,
        "helper_uses_half_target_maxhp":all(
            token in event for token in (
                "CHAR_WORKMAXHP)/2",
                "BATTLE_MultiRessurect(",
                "pow,0,SPR_item3,ReceveEffect",
            )
        ),
        "dead_index_excludes_ultimate":all(
            token in dead_index for token in (
                "BATTLE_CHECKNO(bid)==FALSE",
                "BENT_FLG_ULTIMATE",
                "return-1",
            )
        ),
        "dead_target_check_requires_actionable_dead":all(
            token in dead_check for token in (
                "CHAR_WORKBATTLEMODE)==0",
                "BATTLE_CHARMODE_RESCUE",
                "CHAR_ISATTACKED)==FALSE",
                "CHAR_ISDIE)==FALSE",
            )
        ),
        "resurrect_revalidates_dead_targets":
            "BATTLE_MultiListDead(battleindex,toNo,ToList)" in resurrect
            and "CHAR_ISDIE)==FALSE" in resurrect,
        "resurrect_emits_magic_effect_before_mutation":
            resurrect.find("BATTLE_MagicEffect(") >= 0
            and resurrect.find("BATTLE_MagicEffect(") <
                resurrect.find("CHAR_setInt(toindex,CHAR_HP"),
        "resurrect_uses_90_110_rng_for_nonzero_power":
            "RAND((power*0.9),(power*1.1))" in resurrect,
        "resurrect_minimum_one_and_hp_cap":all(
            token in resurrect for token in (
                "UpPoint=max(1,UpPoint)",
                "min(workhp,CHAR_getWorkInt(toindex,CHAR_WORKMAXHP))",
            )
        ),
        "resurrect_clears_die_flag":
            "CHAR_setFlg(toindex,CHAR_ISDIE,0)" in resurrect,
        "resurrect_blocks_player_revive_in_pvp":all(
            token in resurrect for token in (
                "BATTLE_TYPE_P_vs_P",
                "CHAR_TYPEPLAYER",
                "continue",
            )
        ),
    }
    failed={key:value for key,value in gates.items() if not value}
    if failed:
        raise ValueError(f"{name} ReLife source gates failed: {failed}")

    return {
        "profile":name,
        "commit":actual,
        "command_value":enums[COMMAND_NAME],
        "mode_value":enums["BATTLE_CHARMODE_C_OK"],
        "bismarck_power_minus_one_extension":(
            "power==-1" in resurrect
        ),
        "gates":gates,
        "hashes":{key:_sha(path) for key,path in paths.items()},
    }


def emit(rows):
    print("StoneAge ENEMYSKILL_ReLife fixed-source audit — R1")
    print("Derived facts only; no original source text/assets stored.")
    for row in rows:
        print(
            "PROFILE|"
            f"name={row['profile']}|sha={row['commit']}|"
            f"command_value={row['command_value']}|"
            f"mode_value={row['mode_value']}|"
            f"power_minus_one_extension="
            f"{int(row['bismarck_power_minus_one_extension'])}"
        )
        for key,value in sorted(row["gates"].items()):
            print(
                f"GATE|profile={row['profile']}|"
                f"name={key}|pass={int(value)}"
            )
        for key,value in sorted(row["hashes"].items()):
            print(
                f"SOURCE_SHA256|profile={row['profile']}|"
                f"file={key}|sha256={value}"
            )
    print("FACT|enemy_actor_candidate_slots=10..19")
    print("FACT|candidate_requires_nonultimate_actionable_ISDIE")
    print("FACT|enemy_actor_target_selection=one_RAND_0_to_dead_count_minus_1")
    print("FACT|revive_base_power=target_WORKMAXHP_integer_div_2")
    print("FACT|nonzero_revive_power=one_RAND_90_to_110_percent_band")
    print("FACT|revive_hp_is_capped_and_ISDIE_is_cleared")
    print("FACT|no_enemy_dead_candidate_returns_false")
    print("FACT|false_helper_result_falls_back_to_physical_attack")
    print("BOUNDARY|pet_actor_uses_carried_target_instead_of_enemy_scan")
    print("BOUNDARY|pvp_player_revive_is_skipped_by_MultiRessurect")
    print("BOUNDARY|original_binary_compile_profile_and_command_number_open")
    print("RESOLUTION|RELIFE_FIXED_SOURCE_CLOSED_BOUNDED_REFERENCE")


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
