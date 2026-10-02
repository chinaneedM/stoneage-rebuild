#!/usr/bin/env python3
"""Reproduce Barrier semantics from three pinned StoneAge source profiles."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import subprocess
import tempfile

from tools.stoneage_barrier_model import (
    CALLBACK_NAME,
    COMMAND_NAME,
    FEATURE_NAME,
    MAGIC_FEATURE_NAME,
    SOURCE_PETSKILL_SYMBOL_NAME,
)


PROFILES={
    "gavin":(
        "1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56",
        "gmsv/src",
    ),
    "iris":(
        "9e6c8ce2cd8ed532a7157773acd1c61582c178b5",
        "Source/gmsv",
    ),
    "bismarck":(
        "999ffdf1d220ec6666eb65339180689c9caf1876",
        "server/gmsv",
    ),
}
FEATURES=(
    FEATURE_NAME,
    MAGIC_FEATURE_NAME,
    "_SUIT_ADDENDUM",
    "_EQUIT_RESIST",
    "_SUIT_ADDPART3",
    "_MO_LUA_RESIST",
)


def _sha(path:Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _text(path:Path) -> str:
    return path.read_bytes().decode("utf-8","replace")


def _compact(text:str) -> str:
    return re.sub(r"\s+","",text)


def _definition_window(
    text:str,
    function_name:str,
    *,
    max_chars:int=12000,
) -> str:
    pattern=re.compile(
        rf"\b(?:static\s+)?(?:int|void|BOOL)\s+"
        rf"{re.escape(function_name)}\s*\([^;{{}}]*\)\s*\{{",
        re.DOTALL,
    )
    match=pattern.search(text)
    if match is None:
        raise ValueError(f"missing function definition: {function_name}")
    return text[match.start():match.start()+int(max_chars)]


def _macro_int(text:str,name:str) -> int:
    match=re.search(
        rf"^\s*#\s*define\s+{re.escape(name)}\s*\(\s*(-?\d+)\s*\)",
        text,
        re.MULTILINE,
    )
    if match is None:
        raise ValueError(f"missing integer macro: {name}")
    return int(match.group(1))


def _enum_probe(name:str,root:Path,base:Path):
    include=base/"include"
    includes=["-I",str(include)]
    if name=="bismarck":
        includes += [
            "-I",str(root/"server/common"),
            "-I",str(root/"shared/lua51"),
        ]
    code=(
        '#include <stdio.h>\n'
        '#include "char_base.h"\n'
        '#include "battle.h"\n'
        '#include "battle_event.h"\n'
        'int main(void){'
        'printf("%d %d %d %d",'
        'BATTLE_ST_BARRIER,CHAR_WORKBARRIER,'
        'CHAR_WORKWEAKEN,CHAR_WORKNOCAST);'
        '#ifdef _SKILL_BARRIER\n'
        'printf(" %d",BATTLE_COM_S_BARRIER);\n'
        '#endif\n'
        'return 0;}\n'
    ).replace(';#ifdef',';\n#ifdef')
    with tempfile.TemporaryDirectory() as directory:
        temp=Path(directory)
        src=temp/"probe.c"
        exe=temp/"probe"
        src.write_text(code)
        subprocess.run(
            ["cc","-w",*includes,str(src),"-o",str(exe)],
            check=True,
            capture_output=True,
        )
        values=tuple(map(
            int,
            subprocess.check_output([str(exe)],text=True).split(),
        ))
    return values


def analyze_profile(name:str,root:Path):
    expected,base_rel=PROFILES[name]
    root=Path(root).resolve()
    actual=subprocess.check_output(
        ["git","-C",str(root),"rev-parse","HEAD"],
        text=True,
    ).strip()
    if actual != expected:
        raise ValueError(f"{name} source HEAD drift")
    if subprocess.check_output(
        ["git","-C",str(root),"status","--porcelain"],
        text=True,
    ).strip():
        raise ValueError(f"{name} source tree is dirty")

    base=root/base_rel
    include=base/"include"
    includes=["-I",str(include)]
    if name=="bismarck":
        includes += [
            "-I",str(root/"server/common"),
            "-I",str(root/"shared/lua51"),
        ]
    definitions=subprocess.check_output(
        ["cpp","-dM",*includes,str(include/"version.h")],
        text=True,
    )
    active=set(re.findall(r"^#define\s+(\w+)\b",definitions,re.M))
    features={feature:feature in active for feature in FEATURES}

    paths={
        "version":include/"version.h",
        "char_base":include/"char_base.h",
        "battle_h":include/"battle.h",
        "battle_event_h":include/"battle_event.h",
        "petskill_h":include/"pet_skillinfo.h",
        "pet_skill":base/"battle/pet_skill.c",
        "battle":base/"battle/battle.c",
        "battle_event":base/"battle/battle_event.c",
    }
    data={key:_text(path) for key,path in paths.items()}

    callback=_compact(_definition_window(
        data["pet_skill"],CALLBACK_NAME,max_chars=2200
    ))
    executor=_compact(_definition_window(
        data["battle_event"],"BATTLE_S_Barrier",max_chars=10000
    ))
    status_seq=_compact(_definition_window(
        data["battle"],"BATTLE_StatusSeq",max_chars=15000
    )).replace("char_index","charaindex")
    can_move=_compact(_definition_window(
        data["battle"],"BATTLE_CanMoveCheck",max_chars=5000
    )).replace("char_index","charaindex")

    dispatch_compact=_compact(data["battle"])
    case=dispatch_compact.find(f"case{COMMAND_NAME}:")
    dispatch=(
        ""
        if case < 0
        else dispatch_compact[case:case+1300]
    )

    dec=status_seq.find(
        "CHAR_setWorkInt(charaindex,StatusTbl[i],--cnt)"
    )
    barrier_check=status_seq.find(
        "CHAR_getWorkInt(charaindex,CHAR_WORKBARRIER)>0",
        dec,
    )
    restore=status_seq.find(
        "CHAR_setWorkInt(charaindex,StatusTbl[i],cnt+1)",
        barrier_check,
    )
    expiry=status_seq.find("if(cnt<=0)",restore)

    gates={
        "skill_feature_active":features[FEATURE_NAME],
        "magic_feature_active":features[MAGIC_FEATURE_NAME],
        "callback_command":COMMAND_NAME in callback,
        "callback_target":"CHAR_WORKBATTLECOM2" in callback,
        "callback_skill_array_low":(
            "CHAR_SETWORKINT_LOW" in callback
            and "CHAR_WORKBATTLECOM3" in callback
            and "array" in callback
        ),
        "dispatch_uses_com2_directly":(
            "CHAR_WORKBATTLECOM2" in dispatch
            and "BATTLE_S_Barrier(" in dispatch
        ),
        "executor_reads_option":(
            "PETSKILL_getChar(" in executor
            and "PETSKILL_OPTION" in executor
        ),
        "executor_sequential_turn_success":(
            executor.find('strstr(pszP,szTurn)') >= 0
            and executor.find('strstr(pszP,szSuccess)')
                > executor.find('strstr(pszP,szTurn)')
        ),
        "executor_multilist":"BATTLE_MultiList(" in executor,
        "executor_status_check":(
            "BATTLE_StatusAttackCheck(" in executor
            and "BATTLE_ST_BARRIER" in executor
        ),
        "executor_turn_plus_one":(
            "CHAR_WORKBARRIER,turn+1" in executor
        ),
        "executor_returns_false":(
            "BOOLiRet=FALSE" in executor
            and "returniRet" in executor
        ),
        "status_self_freeze_order":(
            dec >= 0
            and barrier_check > dec
            and restore > barrier_check
            and expiry > restore
        ),
        "can_move_blocks_barrier":(
            "CHAR_WORKBARRIER" in can_move
            and "returnFALSE" in can_move
        ),
        "status_table_barrier_before_nocast":(
            "CHAR_WORKBARRIER,CHAR_WORKNOCAST" in
            _compact(data["battle_event"])
        ),
    }
    if not all(gates.values()):
        raise ValueError(
            f"{name} Barrier source audit did not converge: {gates}"
        )

    enums=_enum_probe(name,root,base)
    status_barrier,work_barrier,work_weaken,work_nocast,*command=enums
    if status_barrier == work_barrier:
        raise ValueError(
            "Barrier status index unexpectedly equals work-field enum"
        )

    source_skill_id=_macro_int(
        data["petskill_h"],
        SOURCE_PETSKILL_SYMBOL_NAME,
    )
    return {
        "name":name,
        "commit":actual,
        "features":features,
        "gates":gates,
        "status_barrier":status_barrier,
        "work_barrier":work_barrier,
        "work_weaken":work_weaken,
        "work_nocast":work_nocast,
        "command":(command[0] if command else None),
        "source_skill_id":source_skill_id,
        "hashes":{
            key:_sha(path) for key,path in paths.items()
        },
    }


def emit(rows):
    print("StoneAge Barrier fixed-source audit — R1")
    print("No original source text is stored.")
    for row in rows:
        print(
            "PROFILE|"
            f"name={row['name']}|commit={row['commit']}|"
            f"status_barrier={row['status_barrier']}|"
            f"work_barrier={row['work_barrier']}|"
            f"work_weaken={row['work_weaken']}|"
            f"work_nocast={row['work_nocast']}|"
            f"command_barrier="
            f"{row['command'] if row['command'] is not None else 'not_compiled'}|"
            f"source_skill_symbol_id={row['source_skill_id']}"
        )
        for key,value in sorted(row["features"].items()):
            print(
                f"FEATURE|profile={row['name']}|name={key}|active={int(value)}"
            )
        for key,value in sorted(row["gates"].items()):
            print(
                f"GATE|profile={row['name']}|name={key}|pass={int(value)}"
            )
        for key,digest in sorted(row["hashes"].items()):
            print(
                "SOURCE_SHA256|"
                f"profile={row['name']}|file={key}|sha256={digest}"
            )
    closed=(
        len(rows)==3
        and {row["status_barrier"] for row in rows}=={9}
        and {row["source_skill_id"] for row in rows}=={546}
        and all(
            row["status_barrier"] != row["work_barrier"]
            for row in rows
        )
        and all(all(row["gates"].values()) for row in rows)
    )
    print(
        "RESOLUTION|BARRIER_FIXED_SOURCE_"
        + ("CLOSED" if closed else "OPEN")
    )


def main():
    parser=argparse.ArgumentParser()
    for name in PROFILES:
        parser.add_argument(f"--{name}-dir",type=Path,required=True)
    args=parser.parse_args()
    emit(tuple(
        analyze_profile(name,getattr(args,name+"_dir"))
        for name in PROFILES
    ))


if __name__=="__main__":
    main()
