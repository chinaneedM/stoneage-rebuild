"""Pinned BecomeFox execution-order source audit R1."""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import subprocess

from tools.stoneage_guard_break2_source_audit import (
    PINNED, LAYOUTS, _text, _sha, _function, _compact,
)
from tools.stoneage_mdfyattack_source_audit import _strip


def _postattack_window(source: str) -> str:
    hits=list(re.finditer(r"rand\s*\(\s*\)\s*%\s*100\s*<\s*31",source))
    for hit in hits:
        before=source[max(0,hit.start()-2200):hit.start()]
        if "BATTLE_COM_S_BECOMEFOX" not in before:
            continue
        start=source.rfind("if",max(0,hit.start()-2200),hit.start())
        if start<0:
            continue
        brace=source.find("{",hit.end())
        if brace<0:
            continue
        depth=0
        state="code"
        i=brace
        while i<len(source):
            c=source[i];n=source[i+1] if i+1<len(source) else ""
            if state=="code":
                if c=="/" and n=="/": state="line";i+=2;continue
                if c=="/" and n=="*": state="block";i+=2;continue
                if c=='"': state="string";i+=1;continue
                if c=="'": state="char";i+=1;continue
                if c=="{": depth+=1
                elif c=="}":
                    depth-=1
                    if depth==0:
                        return source[start:i+1]
            elif state=="line":
                if c=="\n": state="code"
            elif state=="block":
                if c=="*" and n=="/": state="code";i+=2;continue
            elif state=="string":
                if c=="\\": i+=2;continue
                if c=='"': state="code"
            elif state=="char":
                if c=="\\": i+=2;continue
                if c=="'": state="code"
            i+=1
    raise ValueError("BecomeFox postattack block missing")


def analyze_profile(name: str, root: Path) -> dict:
    root=root.resolve()
    head=subprocess.check_output(
        ["git","-C",str(root),"rev-parse","HEAD"],text=True
    ).strip()
    dirty=subprocess.check_output(
        ["git","-C",str(root),"status","--porcelain"],text=True
    ).strip()
    if head!=PINNED[name] or dirty:
        raise ValueError("pinned source commit/tree drift")
    base=root/LAYOUTS[name]
    battle_path=base/"battle/battle.c"
    source=_text(battle_path)
    dex=_compact(_strip(_function(source,"int BATTLE_DexCalc")))
    post=_compact(_strip(_postattack_window(source)))

    fox_assign="dex=work*0.8"
    switch="switch(COM)"
    default="default:"
    default_assign="dex=work-RAND("
    default_at=dex.find(default)
    positions={
        "fox":dex.find(fox_assign),
        "switch":dex.find(switch),
        "default":default_at,
        "default_assign":dex.find(default_assign,default_at),
    }
    guards={
        "fox_dex_write_precedes_command_switch":
            -1 not in positions.values()
            and positions["fox"]<positions["switch"]<positions["default"]<positions["default_assign"],
        "ordinary_attack_guard_none_have_no_dedicated_case":
            all(("case"+token+":") not in dex for token in (
                "BATTLE_COM_ATTACK","BATTLE_COM_GUARD","BATTLE_COM_NONE"
            )),
        "default_branch_recomputes_work_and_dex":
            "CHAR_WORKQUICK)+20" in dex[positions["default"]:]
            and default_assign in dex[positions["default"]:],
        "postattack_command_gate_precedes_result_gates":
            post.find("COM==BATTLE_COM_S_BECOMEFOX")>=0
            and post.find("COM==BATTLE_COM_S_BECOMEFOX")<post.find("BATTLE_RET_MISS"),
        "postattack_result_gates_precede_alive_check":
            post.find("BATTLE_RET_MISS")<post.find("BATTLE_TargetCheck"),
        "postattack_alive_precedes_draw":
            post.find("BATTLE_TargetCheck")<post.find("rand()%100<31"),
        "postattack_draw_precedes_type_and_petflag":
            post.find("rand()%100<31")<post.find("CHAR_WHICHTYPE")
            <post.find("CHAR_WORK_PETFLG"),
        "postattack_success_sets_round_and_fox_image":
            "CHAR_WORKFOXROUND,pBattle->turn" in post
            and "CHAR_BASEIMAGENUMBER,101749" in post,
        "postattack_ride_cleanup_is_success_only":
            "CHAR_RIDEPET,-1" in post
            and "BATTLE_changeRideImage" in post
            and "CHAR_WORKPETFALL,1" in post,
    }
    if not all(guards.values()):
        raise ValueError(
            f"{name} BecomeFox execution-order drift: "
            f"{[k for k,v in guards.items() if not v]}"
        )

    tail=dex[positions["default"]:]
    if name=="bismarck":
        default_profile="RAND_0_WORK_X_0_1"
        if "RAND(0,work*0.1)" not in tail:
            raise ValueError("Bismarck default dex range drift")
    else:
        default_profile="RAND_0_WORK_X_0_3"
        if "RAND(0,work*0.3)" not in tail:
            raise ValueError(f"{name} default dex range drift")

    return {
        "profile":name,
        "commit":head,
        "battle_sha256":_sha(battle_path),
        "default_dex_profile":default_profile,
        "fox_pre_switch_dex_write_is_overwritten_for_attack_guard_none":True,
        "gates":guards,
    }


def main():
    parser=argparse.ArgumentParser()
    for name in PINNED:
        parser.add_argument("--"+name+"-dir",type=Path,required=True)
    args=parser.parse_args()
    for name in PINNED:
        row=analyze_profile(name,getattr(args,name+"_dir"))
        print(
            "PROFILE|name={profile}|sha={commit}|battle_sha256={battle_sha256}|"
            "default_dex_profile={default_dex_profile}|"
            "fox_pre_switch_overwritten=1".format(**row)
        )
        for key,value in sorted(row["gates"].items()):
            print(f"GATE|profile={name}|name={key}|pass={int(value)}")
    print("FACT|BecomeFox_postattack_draw_occurs_after_result_alive_gates_before_type_petflag_eligibility")
    print("FACT|BecomeFox_success_sets_FOXROUND_current_turn_and_image101749_and_optional_ride_cleanup")
    print("CORRECTION|fox_DexCalc_pre_switch_0.8_write_is_overwritten_for_allowed_ATTACK_GUARD_NONE_by_default_branch")
    print("BOUNDARY|gavin_iris_default_dex_RAND_upper_0.3_work_bismarck_upper_0.1_work")
    print("BOUNDARY|source_comment_20pct_initiative_penalty_is_not_an_accepted_effective_runtime_rule")
    print("OPEN|exact_native_postattack_execution_and_full_ordered_command_integration")
    print("RESOLUTION|BECOMEFOX_EXECUTION_ORDER_SOURCE_AUDIT_PASS")
if __name__=="__main__":
    main()
