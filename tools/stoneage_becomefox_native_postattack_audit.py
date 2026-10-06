"""Execute exact pinned BecomeFox post-attack source block against the R1 model."""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import tempfile

from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS, _text
from tools.stoneage_becomefox_execution_order_source_audit import _postattack_window
from tools.stoneage_becomefox_reference_model import (
    FOX_IMAGE,
    FoxState,
    resolve_postattack_transform,
)

RESULT_CODE={
    "HIT":0,
    "MISS":1,
    "DODGE":2,
    "ALLGUARD":3,
    "ARRANGE":4,
}


def _c_source(block: str, *, arrange_guard_active: bool) -> str:
    block=block.replace("char_index","charaindex")
    feature="#define _EQUIT_ARRANGE 1\n" if arrange_guard_active else ""
    return r"""
#include <stdio.h>
#include <string.h>
#define SIDE_OFFSET 10
#define BATTLE_COM_S_BECOMEFOX 100
#define BATTLE_RET_MISS 1
#define BATTLE_RET_DODGE 2
#define BATTLE_RET_ALLGUARD 3
#define BATTLE_RET_ARRANGE 4
#define CHAR_WHICHTYPE 1
#define CHAR_TYPEPLAYER 1
#define CHAR_WORK_PETFLG 2
#define CHAR_BECOMEPIG 3
#define CHAR_WORKFOXROUND 4
#define CHAR_RIDEPET 5
#define CHAR_WORKPETFALL 6
#define CHAR_BASEIMAGENUMBER 7
#define _PETSKILL_BECOMEPIG 1
""" + feature + r"""
typedef struct { int Battle_Attack_ReturnData; } AttackReturn;
typedef struct { int turn; } Battle;
static AttackReturn Battle_Attack_ReturnData_x;
static Battle battle_store;
static Battle *pBattle=&battle_store;
static int g_alive,g_draw,g_player,g_petflag,g_pig,g_ride,g_turn;
static int g_foxround,g_image,g_petfall;
static int g_target_checks,g_draw_calls,g_type_reads,g_petflag_reads,g_pig_reads;
static int g_magic_calls,g_ride_changes;

static int harness_rand(void){g_draw_calls++;return g_draw;}
#define rand harness_rand
int BATTLE_TargetCheck(int battleindex,int slot){
  (void)battleindex;(void)slot;g_target_checks++;return g_alive;
}
int BATTLE_No2Index(int battleindex,int slot){(void)battleindex;return slot;}
int CHAR_getInt(int index,int field){
  if(field==CHAR_WHICHTYPE){g_type_reads++;return g_player?CHAR_TYPEPLAYER:2;}
  if(field==CHAR_BECOMEPIG){g_pig_reads++;return g_pig;}
  if(field==CHAR_RIDEPET)return g_ride;
  if(field==CHAR_BASEIMAGENUMBER)return g_image;
  return 0;
}
int CHAR_getWorkInt(int index,int field){
  (void)index;
  if(field==CHAR_WORK_PETFLG){g_petflag_reads++;return g_petflag;}
  if(field==CHAR_WORKFOXROUND)return g_foxround;
  if(field==CHAR_WORKPETFALL)return g_petfall;
  return 0;
}
void CHAR_setInt(int index,int field,int value){
  (void)index;
  if(field==CHAR_RIDEPET)g_ride=value;
  else if(field==CHAR_BASEIMAGENUMBER)g_image=value;
}
void CHAR_setWorkInt(int index,int field,int value){
  (void)index;
  if(field==CHAR_WORKFOXROUND)g_foxround=value;
  else if(field==CHAR_WORKPETFALL)g_petfall=value;
}
int BATTLE_MultiList(int battleindex,int slot,int *out){
  (void)battleindex;(void)slot;if(out)out[0]=-1;return 0;
}
int BATTLE_MagicEffect(int battleindex,int slot,int *list,int a,int b){
  (void)battleindex;(void)slot;(void)list;(void)a;(void)b;g_magic_calls++;return 0;
}
void BATTLE_changeRideImage(int index){(void)index;g_ride_changes++;}

static void one(int command,int result,int alive,int draw,int player,int petflag,
                int pig,int ride,int turn){
  int battleindex=0,defNo=5,charaindex=10;
  int COM=command?BATTLE_COM_S_BECOMEFOX:0;
  g_alive=alive;g_draw=draw;g_player=player;g_petflag=petflag;
  g_pig=pig;g_ride=ride;g_turn=turn;g_foxround=-1;g_image=101743;g_petfall=0;
  g_target_checks=g_draw_calls=g_type_reads=g_petflag_reads=g_pig_reads=0;
  g_magic_calls=g_ride_changes=0;
  battle_store.turn=turn;
  Battle_Attack_ReturnData_x.Battle_Attack_ReturnData=result;
""" + block + r"""
  printf("%d %d %d %d %d %d %d %d %d %d %d %d\n",
    g_target_checks,g_draw_calls,g_type_reads,g_petflag_reads,g_pig_reads,
    g_magic_calls,g_ride_changes,g_foxround,g_image,g_ride,g_petfall,
    (g_image==101749));
}
int main(void){
  int command,result,alive,draw,player,petflag,pig,ride,turn;
  while(scanf("%d%d%d%d%d%d%d%d%d",
              &command,&result,&alive,&draw,&player,&petflag,&pig,&ride,&turn)==9){
    one(command,result,alive,draw,player,petflag,pig,ride,turn);
  }
  return 0;
}
"""


def _vectors():
    rows=[]
    for command in (0,1):
      for result in ("HIT","MISS","DODGE","ALLGUARD","ARRANGE"):
        for alive in (0,1):
          for draw in (0,30,31,99):
            for player in (0,1):
              for petflag in (0,1):
                for pig in (-1,0):
                  for ride in (-1,55):
                    rows.append((command,result,alive,draw,player,petflag,pig,ride,9))
    return tuple(rows)


def _expected(vector, *, arrange_guard_active: bool):
    command,result,alive,draw,player,petflag,pig,ride,turn=vector
    pre_rng=bool(
        command
        and result not in {"MISS","DODGE","ALLGUARD"}
        and not (arrange_guard_active and result=="ARRANGE")
        and alive
    )
    state=FoxState(
        base_image=101743,base_base_image=101743,
        attack_power=40,defence_power=26,quick=30,
        fix_str=40,fix_tough=26,fix_dex=30,
        fox_round=-1,ride_pet=ride,petfall=0,
    )
    decision=resolve_postattack_transform(
        state,
        command_is_becomefox=bool(command),
        attack_result=result,
        target_alive=bool(alive),
        draw_mod_100=(draw if pre_rng else None),
        target_is_player=bool(player),
        target_petflag=petflag,
        attacker_pig_marker=pig,
        arrange_guard_active=arrange_guard_active,
        pig_guard_active=True,
        current_turn=turn,
    )
    type_reads=petflag_reads=pig_reads=0
    if decision.draw_consumed and draw < 31:
        type_reads=1
        if not player:
            petflag_reads=1
            if petflag!=0:
                pig_reads=1
    return (
        int(decision.target_check_consumed),
        int(decision.draw_consumed),
        type_reads,
        petflag_reads,
        pig_reads,
        int(decision.magic_effect),
        int(decision.ride_image_changed),
        int(decision.state.fox_round),
        int(decision.state.base_image),
        int(decision.state.ride_pet),
        int(decision.state.petfall),
        int(decision.transformed),
    )


def analyze_profile(name: str, root: Path) -> dict:
    root=root.resolve()
    actual=subprocess.check_output(
        ["git","-C",str(root),"rev-parse","HEAD"],text=True
    ).strip()
    dirty=subprocess.check_output(
        ["git","-C",str(root),"status","--porcelain"],text=True
    ).strip()
    if actual!=PINNED[name] or dirty:
        raise ValueError("pinned source commit/tree drift")
    source=_text(root/LAYOUTS[name]/"battle/battle.c")
    block=_postattack_window(source)
    arrange_guard_active=name in {"gavin","iris"}
    c=_c_source(block,arrange_guard_active=arrange_guard_active)
    vectors=_vectors()
    payload="".join(
        f"{command} {RESULT_CODE[result]} {alive} {draw} {player} {petflag} {pig} {ride} {turn}\n"
        for command,result,alive,draw,player,petflag,pig,ride,turn in vectors
    )
    with tempfile.TemporaryDirectory(prefix="sa-becomefox-native-") as directory:
        source_path=Path(directory)/"oracle.c"
        exe=Path(directory)/"oracle"
        source_path.write_text(c,encoding="utf-8")
        compiled=subprocess.run(
            ["cc","-std=c99","-O0",str(source_path),"-o",str(exe)],
            text=True,capture_output=True,
        )
        if compiled.returncode:
            raise ValueError(
                f"{name} BecomeFox native compile failed: {compiled.stderr[-4000:]}"
            )
        out=subprocess.check_output([str(exe)],input=payload,text=True)
    actual_rows=[tuple(map(int,line.split())) for line in out.splitlines()]
    expected_rows=[
        _expected(vector,arrange_guard_active=arrange_guard_active)
        for vector in vectors
    ]
    if actual_rows!=expected_rows:
        for index,(got,want) in enumerate(zip(actual_rows,expected_rows)):
            if got!=want:
                raise ValueError(
                    f"{name} native mismatch at {vectors[index]}: {got} != {want}"
                )
        raise ValueError(f"{name} native output length mismatch")
    transformed=sum(row[-1] for row in actual_rows)
    draw_cases=sum(row[1] for row in actual_rows)
    return {
        "profile":name,
        "commit":actual,
        "native_cases":len(actual_rows),
        "draw_cases":draw_cases,
        "transformed_cases":transformed,
        "arrange_guard_active":arrange_guard_active,
    }


def main():
    parser=argparse.ArgumentParser()
    for name in PINNED:
        parser.add_argument("--"+name+"-dir",type=Path,required=True)
    args=parser.parse_args()
    total=0
    for name in PINNED:
        row=analyze_profile(name,getattr(args,name+"_dir"))
        total+=row["native_cases"]
        print(
            "PROFILE|name={profile}|sha={commit}|native_cases={native_cases}|"
            "draw_cases={draw_cases}|transformed_cases={transformed_cases}|"
            "arrange_guard_active={arrange_guard_active}".format(
                **{**row,"arrange_guard_active":int(row["arrange_guard_active"])}
            )
        )
    print(f"TOTAL|native_postattack_model_comparisons={total}")
    print("FACT|native_short_circuit_reads_match_draw_before_type_petflag_pig_order")
    print("FACT|native_success_state_matches_FOXROUND_image_and_success_only_ride_cleanup")
    print("BOUNDARY|original_rand_generator_identity_not_claimed_controlled_rand_mod_100_only")
    print("RESOLUTION|BECOMEFOX_EXACT_POSTATTACK_NATIVE_MODEL_PASS")


if __name__=="__main__":
    main()
