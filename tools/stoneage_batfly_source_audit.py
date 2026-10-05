"""Pinned BatFly callback/dispatcher/effect source and native reference audit."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import subprocess
import tempfile

from tools.stoneage_guard_break2_source_audit import (
    PINNED,LAYOUTS,_text,_sha,_compact,
)
from tools.stoneage_mdfyattack_source_audit import _definition,_strip
from tools.stoneage_battletimid_source_audit import _case_block
from tools.stoneage_weaken_source_audit import _enum_values
from tools.stoneage_batfly_reference_model import (
    CALLBACK_NAME,COMMAND_NAME,FEATURE_NAME,
    BatFlyTarget,resolve_batfly_effect,resolve_batfly_setup,
)


def _native_oracle(event_source:str) -> int:
    effect=_definition(event_source,"BATTLE_BatFly")
    prefix=r"""
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#define TRUE 1
#define FALSE 0
#define SIDE_OFFSET 10
#define TARGET_SIDE_0 20
#define TARGET_SIDE_1 21
#define CHAR_HP 0
#define CHAR_RIDEPET 1
#define CHAR_WORKMAXHP 0
#define CHAR_WORKPETFALL 1
#define BD_KIND_HP 0
static int stats[64][8],works[64][8],valids[64],targets[10];
static int target_count,requested_side,effect_calls,ride_image_changes,frame_count;
typedef struct {
  unsigned int uiSpriteNum,uiPrevMagicNum,uiPostMagicNum;
  int siSx,siSy,uiShowType,uiShowBehindChar,siPrevMagicSx,siPrevMagicSy;
} ToCallMagic;
ToCallMagic PROFESSION_magic[3];
#define CHAR_CHECKINDEX(i) ((i)>=0 && (i)<64 && valids[(i)])
int CHAR_getInt(int i,int k){return CHAR_CHECKINDEX(i)?stats[i][k]:0;}
void CHAR_setInt(int i,int k,int v){if(CHAR_CHECKINDEX(i))stats[i][k]=v;}
int CHAR_getWorkInt(int i,int k){return CHAR_CHECKINDEX(i)?works[i][k]:0;}
void CHAR_setWorkInt(int i,int k,int v){if(CHAR_CHECKINDEX(i))works[i][k]=v;}
int BATTLE_No2Index(int b,int no){return no;}
int BATTLE_MultiList(int b,int side,int *out){
  int i;requested_side=side;
  for(i=0;i<10;i++)out[i]=(i<target_count)?targets[i]:-1;
  return target_count;
}
int BATTLE_getRidePet(int i){
  if(!CHAR_CHECKINDEX(i))return -1;
  return stats[i][CHAR_RIDEPET];
}
void BATTLE_changeRideImage(int i){ride_image_changes++;}
int PROFESSION_MAGIC_ATTAIC_Effect(int b,int a,int *l,int n){
  effect_calls++;return 0;
}
void record_frame(const char *s){frame_count++;}
#define BATTLESTR_ADD(s) record_frame(s)
"""
    main=r"""
static void prep_target(int slot,int hp,int ridehp){
  int ride=20+slot;
  targets[target_count++]=slot;
  valids[slot]=1;stats[slot][CHAR_HP]=hp;
  if(ridehp<0){stats[slot][CHAR_RIDEPET]=-1;}
  else{
    stats[slot][CHAR_RIDEPET]=ride;
    valids[ride]=1;stats[ride][CHAR_HP]=ridehp;
  }
}
int main(void){
  int ah,max,h1,r1,h2,r2,side;
  while(scanf("%d%d%d%d%d%d%d",&ah,&max,&h1,&r1,&h2,&r2,&side)==7){
    memset(stats,0,sizeof(stats));memset(works,0,sizeof(works));
    memset(valids,0,sizeof(valids));target_count=requested_side=effect_calls=0;
    ride_image_changes=frame_count=0;
    valids[10]=1;stats[10][CHAR_HP]=ah;works[10][CHAR_WORKMAXHP]=max;
    prep_target(1,h1,r1);
    if(h2>0)prep_target(2,h2,r2);
    BATTLE_BatFly(0,10,side);
    printf("%d %d %d %d %d %d %d %d %d %d %d %d\n",
      stats[10][CHAR_HP],
      stats[1][CHAR_HP],r1<0?-1:stats[21][CHAR_HP],stats[1][CHAR_RIDEPET],
      works[1][CHAR_WORKPETFALL],
      h2>0?stats[2][CHAR_HP]:-1,h2>0&&r2>=0?stats[22][CHAR_HP]:-1,
      h2>0?stats[2][CHAR_RIDEPET]:-1,h2>0?works[2][CHAR_WORKPETFALL]:0,
      requested_side,effect_calls,ride_image_changes);
  }
  return 0;
}
"""
    vectors=[]
    for ah,maxhp in ((0,100),(50,100),(90,100),(95,100),(100,100)):
        for hp in (1,9,10,19,20,99,100):
            for ride in (-1,0,1,19,20,99,100):
                vectors.append((ah,maxhp,hp,ride,-1,-1,0))
    vectors += [
        (90,100,100,-1,100,-1,0),
        (95,100,100,-1,100,-1,0),
        (50,100,100,100,100,100,1),
        (0,1000,19,1,20,20,1),
    ]
    expected=[]
    for ah,maxhp,h1,r1,h2,r2,side in vectors:
        targets_py=[BatFlyTarget(h1,None if r1<0 else r1)]
        if h2>0:
            targets_py.append(BatFlyTarget(h2,None if r2<0 else r2))
        result=resolve_batfly_effect(
            attacker_hp=ah,
            attacker_max_hp=maxhp,
            targets=tuple(targets_py),
        )
        rows=result.targets
        def one(index,raw_ride):
            item=rows[index]
            ride_after=(
                -1 if raw_ride<0 else
                int(item.ride_pet_hp_after)
            )
            ride_slot=(
                -1 if raw_ride<0 else
                (-1 if item.ride_pet_fell else 20+index+1)
            )
            return (
                item.character_hp_after,
                ride_after,
                ride_slot,
                int(item.ride_pet_fell),
            )
        t1=one(0,r1)
        if h2>0:
            t2=one(1,r2)
        else:
            t2=(-1,-1,-1,0)
        expected.append((
            result.attacker_hp_after,
            *t1,
            *t2,
            TARGET_SIDE_1 if side==0 else TARGET_SIDE_0,
            1,
            int(t1[3])+int(t2[3]),
        ))

    payload="".join(" ".join(map(str,row))+"\n" for row in vectors)
    with tempfile.TemporaryDirectory(prefix="sa-batfly-native-") as directory:
        source=Path(directory)/"oracle.c"
        source.write_text(prefix+"\n"+effect+"\n"+main,encoding="utf-8")
        exe=Path(directory)/"oracle"
        result=subprocess.run(
            ["cc","-std=c99","-O0",str(source),"-o",str(exe)],
            text=True,capture_output=True,
        )
        if result.returncode:
            raise ValueError("BatFly native harness compile failure: "+result.stderr[-3000:])
        actual=[
            tuple(map(int,line.split()))
            for line in subprocess.check_output(
                [str(exe)],input=payload,text=True
            ).splitlines()
        ]
    if actual!=expected:
        at=next(i for i,pair in enumerate(zip(actual,expected)) if pair[0]!=pair[1])
        raise ValueError(
            f"BatFly native mismatch at {vectors[at]}: "
            f"{actual[at]} != {expected[at]}"
        )
    return len(actual)


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
        "magic":base/"battle/battle_magic.c",
        "battle_h":base/"include/battle.h",
        "version":base/"include/version.h",
        "petskill_h":base/"include/pet_skillinfo.h",
        "target_h":base/"include/pet_skill.h",
    }
    data={key:_text(path) for key,path in paths.items()}
    includes=["-I",str(base/"include")]
    if name=="bismarck":
        includes += ["-I",str(root/"server/common"),"-I",str(root/"shared/lua51")]

    macros=subprocess.check_output(
        ["cpp","-dM",*includes,str(paths["version"])],text=True
    )
    active=set(re.findall(r"^#define\s+(\w+)",macros,re.M))
    feature_active=FEATURE_NAME in active
    enum_includes=includes if feature_active else includes+["-D_PETSKILL_LER"]
    enums=_enum_values(
        [
            COMMAND_NAME,
            "BATTLE_CHARMODE_C_OK",
            "PETSKILL_TARGET_ALLOTHERSIDE",
        ],
        enum_includes,
    )

    callback=_compact(_strip(_definition(data["pet"],CALLBACK_NAME)))
    effect=_compact(_strip(_definition(data["event"],"BATTLE_BatFly")))
    visual=_compact(_strip(_definition(data["magic"],"PROFESSION_MAGIC_ATTAIC_Effect")))
    lerchange=_compact(_strip(_definition(data["event"],"BATTLE_LerChange")))
    at=data["battle"].find("case "+COMMAND_NAME+":")
    dispatch=_compact(_strip(_case_block(data["battle"][at:],"case "+COMMAND_NAME+":")))

    guards={
        "target3_is_all_other_side":
            enums["PETSKILL_TARGET_ALLOTHERSIDE"]==3,
        "callback_registered":
            bool(re.search(
                r'"PETSKILL_BatFly"\s*,\s*PETSKILL_BatFly',
                data["pet"],
            )),
        "callback_writes_symbolic_command_target_mode_and_low_skill":
            all(token in callback for token in (
                COMMAND_NAME,"CHAR_WORKBATTLECOM2","BATTLE_CHARMODE_C_OK",
                "CHAR_SETWORKINT_LOW","CHAR_WORKBATTLECOM3",
            )),
        "callback_has_no_option_or_rng":
            "PETSKILL_getChar" not in callback
            and "rand(" not in callback and "RAND(" not in callback,
        "dispatcher_targetadjust_gate_precedes_effect":
            dispatch.find("BATTLE_TargetAdjust")>=0
            and dispatch.find("BATTLE_TargetAdjust")<dispatch.find("BATTLE_BatFly"),
        "dispatcher_effect_ignores_adjusted_defno":
            "BATTLE_BatFly(battleindex,attackNo,myside)" in dispatch.replace(" ",""),
        "effect_rebuilds_whole_opposing_side":
            "TARGET_SIDE_0" in effect and "TARGET_SIDE_1" in effect
            and "BATTLE_MultiList" in effect,
        "effect_protocol_helper_precedes_hp_loop":
            effect.find("PROFESSION_MAGIC_ATTAIC_Effect")>=0
            and effect.find("PROFESSION_MAGIC_ATTAIC_Effect")<effect.find("for(i=0;i<SIDE_OFFSET;i++)"),
        "protocol_helper_is_output_only":
            "BATTLESTR_ADD" in visual
            and "CHAR_setInt" not in visual
            and "CHAR_setWorkInt" not in visual,
        "unmounted_drain_ten_percent_min_one":
            "(charhp/10)==0" in effect
            and "charhp-(charhp/10)" in effect,
        "mounted_rider_and_pet_five_percent_min_one":
            effect.count("/20")>=4
            and "charhp/=20" in effect
            and "pethp/=20" in effect
            and "pethp=CHAR_getInt(petidx,CHAR_HP)" in effect,
        "ride_pet_fall_clears_ride_and_marks_fall":
            "CHAR_RIDEPET,-1" in effect
            and "BATTLE_changeRideImage" in effect
            and "CHAR_WORKPETFALL,1" in effect,
        "attacker_heal_sums_all_drains":
            effect.count("addhp+=")>=2,
        "overflow_cap_sets_reported_addhp_zero":
            "CHAR_WORKMAXHP" in effect
            and "addhp=0" in effect,
        "effect_has_no_attackseq_damage_sub_reaction_or_rng":
            all(token not in effect for token in (
                "BATTLE_AttackSeq","BATTLE_DamageSub","BATTLE_GetDamageReact",
                "rand(","RAND(",
            )),
        "lerchange_is_separate_101813_101814_lifecycle":
            "101813" in lerchange and "101814" in lerchange
            and "BATTLE_Exit" in lerchange,
        "feature_source_contains_633_symbol":
            "PETSKILL_BATFLY" in data["petskill_h"] and "( 633 )" in data["petskill_h"],
    }
    if not all(guards.values()):
        raise ValueError(
            f"{name} BatFly source gates failed: "
            f"{[key for key,value in guards.items() if not value]}"
        )
    native_cases=_native_oracle(data["event"])
    return {
        "profile":name,
        "sha":sha,
        "feature_active":feature_active,
        "command_value":enums[COMMAND_NAME],
        "mode_value":enums["BATTLE_CHARMODE_C_OK"],
        "target_value":enums["PETSKILL_TARGET_ALLOTHERSIDE"],
        "fix_ler_img_source":"_FIX_LER_IMG" in data["event"],
        "gates":guards,
        "hashes":{key:_sha(path) for key,path in paths.items()},
        "native_cases":native_cases,
    }


def emit(rows):
    print("StoneAge BatFly pinned source/native reference — R1")
    print("Derived facts only; original source is recovered transiently.")
    for row in rows:
        print(
            "PROFILE|"
            f"name={row['profile']}|sha={row['sha']}|"
            f"feature_active={int(row['feature_active'])}|"
            f"command_value={row['command_value']}|"
            f"mode_value={row['mode_value']}|target_value={row['target_value']}|"
            f"fix_ler_img_source={int(row['fix_ler_img_source'])}|"
            f"native_cases={row['native_cases']}"
        )
        for key,value in row["gates"].items():
            print(
                f"GATE|profile={row['profile']}|name={key}|pass={int(value)}"
            )
        for key,value in row["hashes"].items():
            print(
                f"SOURCE_SHA256|profile={row['profile']}|file={key}|sha256={value}"
            )
    print("FACT|batfly_callback_uses_no_option_and_no_rng")
    print("FACT|target3_is_all_other_side_but_dispatch_targetadjust_is_only_an_execution_gate")
    print("FACT|effect_rebuilds_and_drains_the_whole_opposing_side")
    print("FACT|unmounted_target_drains_floor_10pct_min1_mounted_rider_and_pet_each_floor_5pct_min1")
    print("FACT|attacker_heals_sum_but_overflow_cap_sets_reported_addhp_to_zero")
    print("FACT|profession_magic_attack_effect_is_protocol_animation_only_for_this_path")
    print("BOUNDARY|recovered_positive_template_graphic101815_is_not_lerchange_graphic101813_or101814")
    print("BOUNDARY|bismarck_server_fixed_profile_keeps_ler_feature_inactive_source_is_conditional_only")
    print("BOUNDARY|fix_ler_img_changes_visual_ids_not_hp_transfer_semantics")
    print("BOUNDARY|numeric_command_is_descendant_profile_evidence_not_original_build_identity")
    print("RESOLUTION|BATFLY_FIXED_SOURCE_CLOSED_BOUNDED_REFERENCE")


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
