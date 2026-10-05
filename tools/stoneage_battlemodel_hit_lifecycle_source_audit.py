"""Native fixed-descendant BattleModel hit-helper lifecycle witnesses.

Shared AttackSeq/DamageSub/status arithmetic is stubbed, not re-certified.
Only call order, branch ownership and authoritative target routing are audited.
The original function is recovered transiently and never stored in this repo.
"""
from __future__ import annotations

import argparse
from itertools import product
from pathlib import Path
import subprocess
import tempfile

from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS, _text, _sha
from tools.stoneage_mdfyattack_source_audit import _definition
from tools.stoneage_battlemodel_source_audit import _normalized_identifier


PREFIX = r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
/* Presentation is outside this lifecycle oracle. In particular the source
 * can leave iPetDamage uninitialised on DODGE. Suppress argument evaluation
 * rather than reading that undefined presentation value in this harness. */
#define snprintf(...) ((void)0)
#define TRUE 1
#define FALSE 0
#define SIDE_OFFSET 10
#define CHAR_HP 0
#define CHAR_WHICHTYPE 1
#define CHAR_TYPEPLAYER 1
#define CHAR_TYPEPET 2
#define CHAR_BASEBASEIMAGENUMBER 2
#define CHAR_NPCWORKINT1 0
#define CHAR_WORKBATTLEFLG 1
#define CHAR_WORKDRUNK 2
#define CHAR_WORKBATTLECOM1 3
#define CHAR_BATTLEFLG_ABIO 1
#define BATTLE_COM_S_BATTLE_MODEL 900
#define BATTLE_COM_NONE 0
#define BATTLE_RET_ALLGUARD 1
#define BATTLE_RET_MISS 2
#define BATTLE_RET_DODGE 3
#define BATTLE_RET_NORMAL 4
#define BATTLE_RET_CRITICAL 5
#define BATTLE_RET_ARRANGE 6
#define BATTLE_MD_ABSROB 1
#define BATTLE_MD_VANISH 2
#define BATTLE_ST_PARALYSIS 2
#define BATTLE_ST_SLEEP 3
#define BATTLE_ST_STONE 4
#define BATTLE_ST_DRUNK 5
#define BATTLE_ST_BARRIER 9
#define BCF_GUARD 1
#define BCF_DODGE 2
#define BCF_NORMAL 4
#define BCF_KAISHIN 8
#define BCF_B_ARRANGE 16
#define BCF_DEATH 32
#define BCF_ULTIMATE_1 64
#define BCF_ULTIMATE_2 128
#define BCF_CRUSH 256
#define BCF_GUARDIAN 512
#define BENT_FLG_ULTIMATE 1
typedef struct {int flg;} Entry;
typedef struct {Entry Entry[10];} Side;
typedef struct {Side Side[2];} Battle;
Battle BattleArray[1];
typedef struct {int index,target,actionNumber;} AttackObject;
static int stats[20][4],works[20][16],StatusTbl[16];
static int seq_state,seq_damage,seq_guardian,reaction,status_hit,damage_roll;
static int target_live,guardian_live,seq_calls,damage_calls,wake_calls;
static int status_calls,badstatus_slot,rng_calls,damage_target,marker_ok;
static int sentinel,protocol_calls,crush_calls;
float gDamageDiv;
int CHAR_getInt(int i,int k){return stats[i][k];}
int CHAR_getWorkInt(int i,int k){return works[i][k];}
void CHAR_setWorkInt(int i,int k,int v){works[i][k]=v;}
int BATTLE_No2Index(int b,int n){return n;}
int BATTLE_Index2No(int b,int n){return n;}
int BATTLE_TargetCheck(int b,int n){
  if(n==0)return target_live;
  if(n==1)return guardian_live;
  return 0;
}
int BATTLE_getRidePet(int i){return -1;}
int BATTLE_AttackSeq(int a,int d,int *damage,int *guardian,int ignored){
  seq_calls++;*damage=seq_damage;*guardian=seq_guardian;return seq_state;
}
int BATTLE_DamageSub(int a,int d,int *damage,int *pet,int *react){
  damage_calls++;damage_target=d;marker_ok=(works[d][CHAR_NPCWORKINT1]==900);
  sentinel=*react;*pet=0;
  if(*react!=-1)*react=reaction;
  if(*react==BATTLE_MD_ABSROB)stats[d][CHAR_HP]+=*damage;
  else if(*react!=BATTLE_MD_VANISH)stats[d][CHAR_HP]-=*damage;
  return 0;
}
int BATTLE_getReactFlg(int d,int r){return 0;}
void BATTLE_DamageWakeUp(int b,int d){wake_calls++;}
int BATTLE_ItemCrushSeq(int d){crush_calls++;return 0;}
int BATTLE_StatusAttackCheck(int a,int d,int e,int h,int p,float f,int *out){
  status_calls++;
  if(h!=30||p!=30||f!=1.0f)exit(94);
  return status_hit;
}
void BATTLE_BadStatusString(int slot,int effect){badstatus_slot=slot;}
int RAND(int lo,int hi){rng_calls++;if(lo!=1||hi!=100)exit(95);return damage_roll;}
void record_protocol(const char *s){protocol_calls++;}
#define BATTLESTR_ADD(s) record_protocol(s)
'''

MAIN = r'''
int main(void){
  int type,hp,guardian,live,guardlive,ret,dmg,react,hit,effect,roll,abio;
  while(scanf("%d%d%d%d%d%d%d%d%d%d%d%d",&type,&hp,&guardian,&live,
              &guardlive,&ret,&dmg,&react,&hit,&effect,&roll,&abio)==12){
    memset(stats,0,sizeof(stats));memset(works,0,sizeof(works));
    memset(BattleArray,0,sizeof(BattleArray));
    for(int i=0;i<16;i++)StatusTbl[i]=i+4;
    for(int i=0;i<20;i++){
      stats[i][CHAR_HP]=hp;stats[i][CHAR_WHICHTYPE]=CHAR_TYPEPLAYER;
      works[i][CHAR_NPCWORKINT1]=77;works[i][CHAR_WORKBATTLECOM1]=88;
    }
    works[0][CHAR_WORKBATTLEFLG]=abio;
    works[1][CHAR_WORKBATTLEFLG]=abio;
    seq_state=ret;seq_damage=dmg;seq_guardian=guardian;
    target_live=live;guardian_live=guardlive;reaction=react;status_hit=hit;
    damage_roll=roll;gDamageDiv=0.0;
    seq_calls=damage_calls=wake_calls=status_calls=rng_calls=protocol_calls=0;
    crush_calls=0;badstatus_slot=damage_target=-1;marker_ok=0;sentinel=99;
    AttackObject object={2,0,123};
    BATTLE_BattleModel_ATTACK(0,10,&object,effect,4,30,type);
    int actual=(type&4)&&guardian==1&&guardlive?1:0;
    printf("%d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d\n",
      seq_calls,damage_calls,damage_target,marker_ok,sentinel,
      wake_calls,status_calls,badstatus_slot,rng_calls,protocol_calls,
      crush_calls,works[actual][CHAR_NPCWORKINT1],
      works[actual][CHAR_WORKBATTLECOM1],works[actual][StatusTbl[effect]],
      stats[0][CHAR_HP],stats[1][CHAR_HP]);
  }
  return 0;
}
'''


def expected_lifecycle(v: tuple[int,...]) -> tuple[int,...]:
    ty,hp,guardian,live,guardlive,ret,dmg,react,hit,effect,roll,abio=v
    if not live:
        return (0,0,-1,0,99,0,0,-1,0,0,0,77,88,0,hp,hp)
    physical=bool(ty&4)
    if physical and not guardlive:
        guardian=-1
    actual=1 if physical and guardian==1 else 0
    damage_called=ret!=3
    effective_reaction=react if physical else -1
    hp_after=hp
    if damage_called:
        if effective_reaction==1:
            hp_after+=dmg
        elif effective_reaction!=2:
            hp_after-=dmg
    reported_damage=0 if ret in (2,3) else dmg
    wake=int(reported_damage>0 and effective_reaction not in (1,2))
    survival=hp_after>0
    status=int(survival and reported_damage>0)
    applied=bool(status and hit)
    command=0 if applied and effect in (2,3,4,9) else 88
    return (
        1,int(damage_called),actual if damage_called else -1,
        int(damage_called),(0 if physical else -1) if damage_called else 99,
        wake,status,(guardian if guardian>=0 else 0) if applied else -1,
        0,1,int(survival),77,command,4 if applied else 0,
        hp_after if actual==0 else hp,hp_after if actual==1 else hp,
    )


def analyze_profile(name: str, root: Path) -> dict:
    root=root.resolve()
    sha=subprocess.check_output(["git","-C",str(root),"rev-parse","HEAD"],text=True).strip()
    dirty=subprocess.check_output(["git","-C",str(root),"status","--porcelain"],text=True).strip()
    if sha!=PINNED[name] or dirty:
        raise ValueError("pinned source commit/tree drift")
    path=root/LAYOUTS[name]/"battle/battle_event.c"
    helper=_normalized_identifier(_definition(_text(path),"BATTLE_BattleModel_ATTACK"))
    vectors=[
        (ty,hp,g,live,gl,ret,10,react,hit,2,49,0)
        for ty,hp,(g,gl),live,ret,react,hit in product(
            (0,4),(5,100),((-1,0),(1,0),(1,1)),(0,1),(2,3,4),(0,1,2),(0,1)
        )
    ]
    with tempfile.TemporaryDirectory(prefix="sa-battlemodel-hit-") as folder:
        source=Path(folder)/"oracle.c";exe=Path(folder)/"oracle"
        source.write_text(PREFIX+"\n"+helper+"\n"+MAIN)
        result=subprocess.run(["cc","-std=c99","-O0",str(source),"-o",str(exe)],capture_output=True,text=True)
        if result.returncode:
            raise ValueError("native helper compile failed: "+result.stderr[-3000:])
        rows=subprocess.check_output([str(exe)],input="".join(" ".join(map(str,v))+"\n" for v in vectors),text=True).splitlines()
    if len(rows)!=len(vectors):
        raise ValueError("native helper output count drift")
    for v,row in zip(vectors,rows):
        actual=tuple(map(int,row.split()));wanted=expected_lifecycle(v)
        if actual!=wanted:
            raise ValueError(f"helper lifecycle mismatch {v}: {actual} != {wanted}")
    return {"profile":name,"sha":sha,"source_sha256":_sha(path),"native_cases":len(vectors)}


def main():
    parser=argparse.ArgumentParser()
    for name in PINNED:
        parser.add_argument("--"+name+"-dir",required=True,type=Path)
    args=parser.parse_args()
    print("StoneAge BattleModel hit-helper lifecycle — bounded source R1")
    for name in PINNED:
        result=analyze_profile(name,getattr(args,name+"_dir"))
        print("PROFILE|"+"|".join(f"{k}={v}" for k,v in result.items()))
    print("FACT|physical_guardian_redirect_selects_authoritative_defender")
    print("FACT|nonphysical_hit_bypasses_redirect_but_retains_AttackSeq_guardian_protocol_witness")
    print("FACT|absorb_and_vanish_suppress_wakeup_but_do_not_independently_suppress_positive_damage_status_check")
    print("FACT|miss_sets_reported_damage_zero_after_DamageSub_and_dodge_skips_DamageSub")
    print("FACT|defender_BattleModel_marker_is_restored_after_the_hit")
    print("OPEN|source_dodge_path_can_leave_pet_damage_presentation_value_uninitialised")
    print("BOUNDARY|common_AttackSeq_DamageSub_status_probability_and_critical_nonplayer_ultimate_are_not_certified_by_this_stubbed_helper_audit")
    print("RESOLUTION|BATTLEMODEL_HIT_HELPER_LIFECYCLE_LOCAL_NATIVE_PASS")


if __name__=="__main__":
    main()
