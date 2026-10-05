"""Reproduce PETSKILL_Combined facts at three pinned descendant commits."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import subprocess

from tools.stoneage_guard_break2_source_audit import (
    PINNED,LAYOUTS,_function,_sha,_text,_compact,
)
from tools.stoneage_weaken_source_audit import _enum_values
from tools.stoneage_combined_model import (
    CALLBACK_NAME,COMMAND_NAME,FEATURE_NAME,COMMAND_VALUE,
)

EXPECTED_MARKER_SHA256={
    "gavin":"a077a91706a9ecd7af495bdccd4379ae619e99ee4e46c57d2cda9919fe18209d",
    "iris":"261cf7737e93ae7a8839c59da3d198fb1d92f02f7301b39595ae90a8307db467",
    "bismarck":"a077a91706a9ecd7af495bdccd4379ae619e99ee4e46c57d2cda9919fe18209d",
}


def _normalize(text:str)->str:
    return _compact(text).replace("char_index","charaindex").replace(
        "from_charaindex","charaindex"
    ).replace("from_char_index","charaindex").replace(
        "to_char_index","toindex"
    ).replace("item_index","itemindex")


def _marker_sha(callback_raw:str)->str:
    match=re.search(
        r'strcmp\s*\(\s*combined\s*,\s*"([^"]*)"\s*\)\s*==\s*0',
        callback_raw,
    )
    if match is None:
        raise ValueError("missing Combined marker comparison")
    return hashlib.sha256(match.group(1).encode("utf-8")).hexdigest()


def _dispatch_case(compact_battle:str)->str:
    marker="case"+COMMAND_NAME+":"
    pos=0
    while True:
        start=compact_battle.find(marker,pos)
        if start < 0:
            raise ValueError("missing Combined dispatcher case")
        window=compact_battle[start:start+1300]
        if "MAGIC_DirectUse(" in window:
            return window
        pos=start+len(marker)


def analyze_profile(name:str,root:Path):
    root=Path(root).resolve()
    actual=subprocess.check_output(
        ["git","-C",str(root),"rev-parse","HEAD"],text=True
    ).strip()
    dirty=subprocess.check_output(
        ["git","-C",str(root),"status","--porcelain"],text=True
    ).strip()
    if actual!=PINNED[name] or dirty:
        raise ValueError(f"{name} source identity/tree drift")

    base=root/LAYOUTS[name]
    paths={
        "pet":base/"battle/pet_skill.c",
        "battle":base/"battle/battle.c",
        "event":base/"battle/battle_event.c",
        "magic":base/"magic/magic.c",
        "version":base/"include/version.h",
        "battle_h":base/"include/battle.h",
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

    callback_raw=_function(data["pet"],"int "+CALLBACK_NAME)
    callback=_normalize(callback_raw)
    battle=_normalize(data["battle"])
    event=_normalize(data["event"])
    magic=_normalize(_function(data["magic"],"int MAGIC_DirectUse"))
    dispatch=_dispatch_case(battle)
    marker_sha=_marker_sha(callback_raw)

    expected_option_guard=(
        'if(pszOption=="\\0")returnFALSE;'
        if name=="bismarck"
        else "if(pszOption==NULL)returnFALSE;"
    )
    option_guard_style=(
        "pointer_literal_nul" if name=="bismarck" else "null_pointer"
    )
    count_init_style=(
        "initialized_zero" if "intkill[10],count=0,i;" in callback
        else "uninitialized"
    )
    initiative_style=(
        "fixed_0_15" if name=="bismarck" else "scaled_0_30pct"
    )
    expected_initiative=(
        "dex=work-RAND(0,15);"
        if name=="bismarck"
        else "dex=work-RAND(0,work*0.3);"
    )

    selection="CHAR_SETWORKINT_LOW(charaindex,CHAR_WORKBATTLECOM3,kill[rand()%count]);"
    gates={
        "feature_active":FEATURE_NAME in active,
        "battle_newpower_active":"_BATTLE_NEWPOWER" in active,
        "magic_nocast_active":"_MAGIC_NOCAST" in active,
        "command_value_2000":enums[COMMAND_NAME]==COMMAND_VALUE,
        "callback_registered":
            '{"'+CALLBACK_NAME+'",'+CALLBACK_NAME+',0}' in _compact(data["pet"]),
        "callback_reads_option":
            "pszOption=PETSKILL_getChar(array,PETSKILL_OPTION);" in callback,
        "callback_option_guard_profile_matches":
            expected_option_guard in callback,
        "callback_marker_profile_hash_matches":
            marker_sha==EXPECTED_MARKER_SHA256[name],
        "callback_reads_declared_count":
            'getStringFromIndexWithDelim(pszOption,"|",2,countstr,sizeof(countstr))==FALSE'
            in callback and "count=atoi(countstr);" in callback,
        "callback_clamps_count_above_ten":
            "if(count>10)count=10;" in callback,
        "callback_has_no_nonpositive_count_guard":
            all(token not in callback for token in (
                "count<=0","count<1","count==0",
            )),
        "callback_missing_magic_token_is_nonfatal":
            'if(getStringFromIndexWithDelim(pszOption,"|",3+i,killstr,sizeof(killstr)))'
            in callback and "kill[i]=atoi(killstr);" in callback,
        "callback_consumes_raw_rand_mod_count":
            selection in callback and "RAND(" not in callback,
        "callback_sets_target_command_mode":all(token in callback for token in (
            "CHAR_WORKBATTLECOM2,toNo",
            "CHAR_WORKBATTLECOM1,"+COMMAND_NAME,
            "CHAR_WORKBATTLEMODE,BATTLE_CHARMODE_C_OK",
        )),
        "callback_clears_high_com3":
            "CHAR_SETWORKINT_HIGH(charaindex,CHAR_WORKBATTLECOM3,0);" in callback,
        "dispatch_magic_direct_use_low_target_high":all(token in dispatch for token in (
            "MAGIC_DirectUse(charaindex,",
            "CHAR_GETWORKINT_LOW(charaindex,CHAR_WORKBATTLECOM3)",
            "CHAR_getWorkInt(charaindex,CHAR_WORKBATTLECOM2)",
            "CHAR_GETWORKINT_HIGH(charaindex,CHAR_WORKBATTLECOM3)",
        )),
        "initiative_profile_matches":
            "case"+COMMAND_NAME+":" in battle
            and "work=CHAR_getWorkInt(charaindex,CHAR_WORKQUICK)+20;" in battle
            and expected_initiative in battle,
        "defender_command_changes_dodge_parameter":all(token in event for token in (
            "CHAR_WORKBATTLECOM1)=="+COMMAND_NAME,
            "gKawashiPara=0.027;",
            "gKawashiPara=0.02;",
        )),
        "magic_direct_nocast_gate":all(token in magic for token in (
            "CHAR_WORKNOCAST)>0",
            "returnFALSE;",
        )),
        "magic_direct_nonplayer_itemnum_path":
            "else{itemindex=itemnum;}" in magic,
        "magic_direct_resolves_id_then_function":all(token in magic for token in (
            "marray=MAGIC_getMagicArray(magicid);",
            "MAGIC_getMagicFuncPointer(MAGIC_getChar(marray,MAGIC_FUNCNAME))",
        )),
    }
    failed={key:value for key,value in gates.items() if not value}
    if failed:
        raise ValueError(f"{name} Combined source gates failed: {failed}")
    return {
        "profile":name,
        "commit":actual,
        "command_value":enums[COMMAND_NAME],
        "mode_value":enums["BATTLE_CHARMODE_C_OK"],
        "marker_sha256":marker_sha,
        "option_guard_style":option_guard_style,
        "count_init_style":count_init_style,
        "initiative_style":initiative_style,
        "gates":gates,
        "hashes":{key:_sha(path) for key,path in paths.items()},
    }


def emit(rows):
    print("StoneAge Combined fixed-source audit — R1")
    print("Derived facts only; no original source text or assets are stored.")
    for row in rows:
        print(
            "PROFILE|"
            f"name={row['profile']}|sha={row['commit']}|"
            f"command_value={row['command_value']}|"
            f"mode_value={row['mode_value']}|"
            f"marker_sha256={row['marker_sha256']}|"
            f"option_guard_style={row['option_guard_style']}|"
            f"count_init_style={row['count_init_style']}|"
            f"initiative_style={row['initiative_style']}"
        )
        for key,value in sorted(row["gates"].items()):
            print(f"GATE|profile={row['profile']}|name={key}|pass={int(value)}")
        for key,value in sorted(row["hashes"].items()):
            print(f"SOURCE_SHA256|profile={row['profile']}|file={key}|sha256={value}")
    print("FACT|command_value=2000")
    print("FACT|option_declared_count_clamped_to_max_10")
    print("FACT|selection_rng=raw_rand_mod_effective_count_one_draw")
    print("FACT|selected_magic=LOW_COM3_and_HIGH_COM3_zero")
    print("FACT|dispatch=MAGIC_DirectUse_selected_magic_target_high_zero")
    print("FACT|defender_using_combined_changes_dodge_parameter_0.02_to_0.027")
    print("BOUNDARY|marker_lexeme=profile_localized_hashes")
    print("BOUNDARY|option_guard=gavin_iris_null_pointer_bismarck_pointer_literal_nul")
    print("BOUNDARY|malformed_nonpositive_count=historical_modulo_or_index_ub")
    print("BOUNDARY|missing_magic_token=historical_uninitialized_read_ub")
    print("BOUNDARY|count_init=gavin_iris_uninitialized_bismarck_zero")
    print("BOUNDARY|initiative=gavin_iris_workquick_plus20_minus_rand_0_30pct_bismarck_workquick_plus20_minus_rand_0_15")
    print("BOUNDARY|magic_directuse_player_and_nonplayer_itemnum_semantics_differ")
    print("BOUNDARY|original_binary_compile_profile_and_jss_membership_open")
    print("RESOLUTION|COMBINED_FIXED_SOURCE_CLOSED_WELLFORMED_OPTION_REFERENCE")


def main():
    parser=argparse.ArgumentParser()
    for name in PINNED:
        parser.add_argument("--"+name+"-dir",type=Path,required=True)
    args=parser.parse_args()
    emit([analyze_profile(name,getattr(args,name+"_dir")) for name in PINNED])


if __name__=="__main__":
    main()
