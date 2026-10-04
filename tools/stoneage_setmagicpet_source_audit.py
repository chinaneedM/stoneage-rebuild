"""Pinned descendant SetMagicPet audit; derived facts only."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import subprocess

from tools.stoneage_guard_break2_source_audit import (
    PINNED, LAYOUTS, _sha, _text, _function, _compact, _macro_int,
)
from tools.stoneage_weaken_source_audit import _enum_values
from tools.stoneage_setmagicpet_model import (
    CALLBACK_NAME, COMMAND_NAME, FEATURE_NAME, SOURCE_PETSKILL_SYMBOL_NAME,
)


def _feature_active(version_text: str, name: str) -> bool:
    return bool(re.search(
        rf"^\s*#\s*define\s+{re.escape(name)}\b",
        version_text,re.M,
    ))


def analyze_profile(name: str, root: Path):
    root=Path(root).resolve()
    actual=subprocess.check_output(
        ["git","-C",str(root),"rev-parse","HEAD"],text=True
    ).strip()
    if actual != PINNED[name]:
        raise ValueError(f"{name} source HEAD drift: {actual}")
    if subprocess.check_output(
        ["git","-C",str(root),"status","--porcelain"],text=True
    ).strip():
        raise ValueError(f"{name} source tree is dirty")

    base=root/LAYOUTS[name]
    paths={
        "pet":base/"battle/pet_skill.c",
        "event":base/"battle/battle_event.c",
        "battle":base/"battle/battle.c",
        "item":base/"item/item.c",
        "version":base/"include/version.h",
        "battle_h":base/"include/battle.h",
        "char_h":base/"include/char_base.h",
        "petskill_h":base/"include/pet_skillinfo.h",
    }
    data={key:_text(path) for key,path in paths.items()}
    callback=_compact(_function(data["pet"],f"int {CALLBACK_NAME}")).replace("char_index","charaindex")
    executor=_compact(_function(data["event"],f"int {CALLBACK_NAME}_Battle")).replace("char_index","charaindex")
    status_seq=_compact(_function(data["battle"],"static int BATTLE_StatusSeq")).replace("char_index","charaindex")
    recalc=_compact(_function(data["item"],"void Other_DefcharWorkInt"))
    battle_compact=_compact(data["battle"]).replace("char_index","charaindex")
    case=battle_compact.find("case"+COMMAND_NAME+":")
    dispatch=battle_compact[case:case+700] if case>=0 else ""

    includes=["-I",str(base/"include")]
    if name=="bismarck":
        includes += ["-I",str(root/"server/common"),"-I",str(root/"shared/lua51")]
    enums=_enum_values(
        [COMMAND_NAME,"BATTLE_CHARMODE_C_OK","PETSKILL_SETMAGICPET"],
        includes,
    )
    source_skill_id=_macro_int(data["petskill_h"],SOURCE_PETSKILL_SYMBOL_NAME)

    null_guard_safe="skillarg==NULL" in executor
    bismarck_bad_guard='skillarg=="\\0"' in executor
    gates={
        "magicpet_feature_active":_feature_active(data["version"],FEATURE_NAME),
        "suit_feature_active":_feature_active(data["version"],"_SUIT_ITEM"),
        "setduck_feature_active":_feature_active(data["version"],"_PETSKILL_SETDUCK"),
        "callback_nominal_limit_three":"nums>=3" in callback,
        "callback_counter_write_is_identity":
            "CHAR_setWorkInt(charaindex,CHAR_MAGICPETMP,nums)" in callback
            and all(token not in callback for token in ("nums++","++nums","nums+1")),
        "callback_command_target_mode_low":all(token in callback for token in (
            COMMAND_NAME,"CHAR_WORKBATTLECOM2","BATTLE_CHARMODE_C_OK",
            "CHAR_SETWORKINT_LOW")),
        "callback_ignores_option":"PETSKILL_getChar" not in callback,
        "executor_three_delimiter_reads":all(
            f'getStringFromIndexWithDelim(skillarg,"|",{index}' in executor
            for index in (1,2,3)
        ),
        "executor_parses_turn_and_amount":executor.count("atoi(buf1)")>=2,
        "executor_hp_branch_before_stat_branch":
            0 <= executor.find('strstr(buf1,"HP")') < executor.find("BATTLE_MultiList("),
        "executor_multilist_effect_for_stat_branch":
            "BATTLE_MultiList(" in executor and "BATTLE_MagicEffect(" in executor,
        "executor_blocks_existing_duck_or_three_stats":all(token in executor for token in (
            "CHAR_MYSKILLDUCK","CHAR_MYSKILLSTR","CHAR_MYSKILLTGH","CHAR_MYSKILLDEX")),
        "executor_writes_str_tgh_dex_turn_and_power":all(token in executor for token in (
            "CHAR_MYSKILLSTRPOWER","CHAR_MYSKILLTGHPOWER","CHAR_MYSKILLDEXPOWER")),
        "dispatch_direct_com2_low_without_target_adjust":
            case>=0 and "CHAR_WORKBATTLECOM2" in dispatch
            and "CHAR_GETWORKINT_LOW" in dispatch
            and CALLBACK_NAME+"_Battle" in dispatch
            and "BATTLE_TargetAdjust" not in dispatch,
        "statusseq_decrements_three_magicpet_turns":all(
            f"CHAR_setWorkInt(charaindex,{field},turns)" in status_seq
            for field in ("CHAR_MYSKILLSTR","CHAR_MYSKILLTGH","CHAR_MYSKILLDEX")
        ),
        "recalc_uses_same_mtgh_basis_three_times":
            recalc.count("mpower+=(mtgh*mdef)/100")>=3,
        "recalc_gated_by_positive_turns":all(
            f"CHAR_getWorkInt(index,{field})>0" in recalc
            for field in ("CHAR_MYSKILLSTR","CHAR_MYSKILLTGH","CHAR_MYSKILLDEX")
        ),
        "source_skill_symbol_is_601":source_skill_id==601,
        "source_macro_matches_compiled_symbol":enums["PETSKILL_SETMAGICPET"]==601,
        "profile_null_behavior_accounted":
            null_guard_safe if name!="bismarck" else bismarck_bad_guard,
    }
    if not all(gates.values()):
        raise ValueError(
            f"{name} SetMagicPet source gates failed: "
            +repr({k:v for k,v in gates.items() if not v})
        )

    return {
        "name":name,
        "commit":actual,
        "source_skill_id":source_skill_id,
        "command_value":enums[COMMAND_NAME],
        "null_guard_safe":null_guard_safe,
        "bismarck_bad_guard":bismarck_bad_guard,
        "gates":gates,
        "hashes":{key:_sha(path) for key,path in paths.items()},
    }


def emit(rows):
    print("StoneAge pinned descendant SetMagicPet source audit — R1")
    print("Derived facts only; original source/OPTION rows/assets are not stored.")
    print("Safe reference requires non-NULL three-field OPTION bytes.")
    for row in rows:
        print(
            "PROFILE|"
            f"name={row['name']}|sha={row['commit']}|"
            f"source_skill_symbol_id={row['source_skill_id']}|"
            f"command_value={row['command_value']}|"
            f"null_guard_safe={int(row['null_guard_safe'])}|"
            f"bismarck_bad_guard={int(row['bismarck_bad_guard'])}"
        )
        for key,value in sorted(row["gates"].items()):
            print(f"GATE|profile={row['name']}|name={key}|pass={int(value)}")
        for key,value in sorted(row["hashes"].items()):
            print(f"SOURCE_SHA256|profile={row['name']}|file={key}|sha256={value}")
    print("FACT|nominal_three_use_counter_is_not_incremented_in_callback")
    print("FACT|STR_TGH_DEX_all_use_pre_suit_toughness_mtgh_as_percentage_basis")
    print("FACT|source_skill_symbol_601_matches_recovered_positive_id_but_historical_identity_remains_unproved")
    print("RESOLUTION|SETMAGICPET_FIXED_SOURCE_CLOSED_BOUNDED_REFERENCE")


def main():
    parser=argparse.ArgumentParser()
    for name in PINNED:
        parser.add_argument("--"+name+"-dir",type=Path,required=True)
    args=parser.parse_args()
    emit([analyze_profile(name,getattr(args,name+"_dir")) for name in PINNED])


if __name__=="__main__":
    main()
