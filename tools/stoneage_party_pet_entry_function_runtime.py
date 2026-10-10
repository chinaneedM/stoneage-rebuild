"""Execute unmodified original party/pet functions with explicit native C test doubles.

Scope is isolated function behavior; NOT complete original battle/Char/Exit runtime.
Original proprietary C is pulled into transient CI clones only.
"""
from __future__ import annotations
import argparse
import hashlib
from pathlib import Path
import re
import subprocess
import tempfile
from tools.stoneage_enemy_creation_audit import definition
from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS

NAMES=("BATTLE_ClearGetExp","BATTLE_PetDefaultEntry","BATTLE_PartyNewEntry")
PROFILES=("gavin","bismarck")
FEATURES=("_PLAYER_NPC","_BATTLE_GETITEM_RATE")
C_HEAD=r"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define FALSE 0
#define TRUE 1
#define CHAR_PARTYMAX 5
#define CHAR_MAXPETHAVE 5
#define CHAR_DEFAULTPET 10
#define CHAR_HP 11
#define CHAR_FLOOR 12
#define CHAR_WHICHTYPE 13
#define CHAR_TYPEPLAYERNPC 44
#define CHAR_ISDIE 14
#define CHAR_WORKGETEXP 20
#define CHAR_WORKBATTLEMODE 21
#define CHAR_WORKPARTYINDEX1 100
#define CHAR_WORK_BATTLEPK 30
#define BATTLE_CHARMODE_NONE 0
#define BATTLE_CHARMODE_FINAL 6
#define BATTLE_TYPE_P_vs_P 3
#define BATTLE_ERR_CHARAINDEX 99
typedef struct {int type;} BATTLE;
static BATTLE BattleArray[1];
typedef struct {int valid,pet[5],party[5],selection,hp,dead,mode,exp,kind,pk,entered,floor;} Actor;
static Actor actors[6];
static int attempts[10],n_attempt,ca[6],cd[6],clears[6],fail_actor=-1;
static void must(int pass,const char *reason){if(!pass){fprintf(stderr,"FAIL:%s\n",reason);exit(40);}}
int CHAR_CHECKINDEX(int i){return i>=0&&i<6&&actors[i].valid;}
int CHAR_getCharPet(int a,int i){return CHAR_CHECKINDEX(a)&&i>=0&&i<5?actors[a].pet[i]:-1;}
int CHAR_getInt(int a,int k){
 if(!CHAR_CHECKINDEX(a))abort();
 if(k==CHAR_DEFAULTPET)return actors[a].selection;
 if(k==CHAR_HP)return actors[a].hp;
 if(k==CHAR_FLOOR)return actors[a].floor;
 if(k==CHAR_WHICHTYPE)return actors[a].kind;
 abort();
}
int CHAR_getFlg(int a,int k){if(!CHAR_CHECKINDEX(a)||k!=CHAR_ISDIE)abort();return actors[a].dead;}
int CHAR_getWorkInt(int a,int k){
 if(!CHAR_CHECKINDEX(a))abort();
 if(k>=CHAR_WORKPARTYINDEX1&&k<CHAR_WORKPARTYINDEX1+5)return actors[a].party[k-CHAR_WORKPARTYINDEX1];
 if(k==CHAR_WORKBATTLEMODE)return actors[a].mode;
 if(k==CHAR_WORKGETEXP)return actors[a].exp;
 abort();
}
void CHAR_setInt(int a,int k,int v){
 if(!CHAR_CHECKINDEX(a)||k!=CHAR_DEFAULTPET)abort();actors[a].selection=v;
}
void CHAR_setWorkInt(int a,int k,int v){
 if(!CHAR_CHECKINDEX(a))abort();
 if(k==CHAR_WORKGETEXP){actors[a].exp=v;clears[a]++;return;}
 if(k==CHAR_WORK_BATTLEPK){actors[a].pk=v;return;}
 abort();
}
int BATTLE_NewEntry(int a,int b,int s){
 if(!CHAR_CHECKINDEX(a)||b!=0||s!=0||n_attempt>=10)abort();
 attempts[n_attempt++]=a;
 if(a==fail_actor)return 17;
 actors[a].entered=1;actors[a].mode=2;return 0;
}
void CAflush(int a){if(!CHAR_CHECKINDEX(a))abort();ca[a]++;}
void CDflush(int a){if(!CHAR_CHECKINDEX(a))abort();cd[a]++;}
int getPartyNum(int a){if(a!=0)abort();return 5;}
int getBattleGetItemRateMap(void){return 999;}
int BATTLE_ClearGetExp(int);
int BATTLE_PetDefaultEntry(int,int,int);
int BATTLE_PartyNewEntry(int,int,int);
"""
C_CASES=r"""
static void reset(void){
 memset(actors,0,sizeof actors);memset(attempts,0,sizeof attempts);
 memset(ca,0,sizeof ca);memset(cd,0,sizeof cd);memset(clears,0,sizeof clears);
 n_attempt=0;fail_actor=-1;
 for(int i=0;i<5;i++){
  actors[i].valid=1;actors[i].selection=-1;actors[i].hp=25;actors[i].exp=33;
  actors[i].floor=1;
  for(int k=0;k<5;k++)actors[i].party[k]=actors[i].pet[k]=-1;
 }
 actors[0].party[1]=1;actors[0].selection=0;actors[0].pet[0]=2;
 actors[0].pet[4]=4;actors[1].selection=0;actors[1].pet[0]=3;
}
static void order(const int *expect,int n){
 must(n_attempt==n,"entry attempt count");
 for(int k=0;k<n;k++)must(attempts[k]==expect[k],"entry attempt order");
}
#define ORDER(...) do{int e[]={__VA_ARGS__};order(e,sizeof(e)/sizeof(int));}while(0)
static void case_run(int id){
 reset();int r;
 switch(id){
 case 0:
  r=BATTLE_PartyNewEntry(0,0,0);must(r==0,"full party result");ORDER(0,2,1,3);
  for(int k=0;k<4;k++)must(actors[k].entered,"leader member pet occupied");
  must(!actors[4].entered,"unselected roster pet not entered");
  must(ca[0]==1&&ca[1]==1&&cd[0]==1&&cd[1]==1,"party flush");
  for(int k=0;k<5;k++)must(actors[k].exp==0&&clears[k]==1,"player and owned pet exp clear");
  must(actors[0].selection==0,"default selection preserved");
  break;
 case 1:
  actors[2].dead=1;r=BATTLE_PartyNewEntry(0,0,0);
  must(r==0&&actors[0].selection==-1&&!actors[2].entered,"dead selected pet rejected");
  ORDER(0,1,3);must(actors[2].exp==0,"dead owned pet exp reset");break;
 case 2:
  actors[2].hp=0;r=BATTLE_PartyNewEntry(0,0,0);
  must(r==0&&actors[0].selection==-1&&!actors[2].entered,"zero hp selected pet rejected");
  ORDER(0,1,3);break;
 case 3:
  actors[0].pet[0]=5;r=BATTLE_PartyNewEntry(0,0,0);
  must(r==0&&actors[0].selection==-1,"invalid selected pet revoked");ORDER(0,1,3);break;
 case 4:
  actors[0].selection=-1;r=BATTLE_PartyNewEntry(0,0,0);
  must(r==0&&!actors[2].entered&&actors[2].exp==0,"unselected owned pet exp reset");
  ORDER(0,1,3);break;
 case 5:
  actors[1].mode=BATTLE_CHARMODE_FINAL;r=BATTLE_PartyNewEntry(0,0,0);
  must(r==0,"FINAL member result");
#ifdef AUDIT_BISMARCK
  ORDER(0,2,1,3);must(actors[1].entered,"Bismarck FINAL member admitted");
#else
  ORDER(0,2);must(!actors[1].entered,"Gavin FINAL member skipped");
#endif
  break;
 case 6:
  actors[1].mode=2;r=BATTLE_PartyNewEntry(0,0,0);
  must(r==0&&!actors[1].entered&&!actors[3].entered,"busy member and pet excluded");
  ORDER(0,2);break;
 case 7:
  fail_actor=2;r=BATTLE_PartyNewEntry(0,0,0);
  must(r==0&&!actors[2].entered&&actors[0].selection==0,"pet NewEntry failure masked");
  must(actors[1].entered&&actors[3].entered,"party after failed pet");
  ORDER(0,2,1,3);break;
 case 8:
  fail_actor=0;r=BATTLE_PartyNewEntry(0,0,0);
  must(r==17&&!ca[0]&&!cd[0]&&actors[0].exp==33,"leader error early return");
  ORDER(0);break;
 case 9:
  r=BATTLE_ClearGetExp(-1);
  must(r==BATTLE_ERR_CHARAINDEX&&actors[0].exp==33,"invalid ClearGetExp");break;
 case 10:
  actors[0].pet[0]=5;r=BATTLE_PetDefaultEntry(0,0,0);
  must(r==0&&actors[0].selection==-1&&n_attempt==0,"direct invalid pet handling");break;
 case 11:
  fail_actor=2;r=BATTLE_PetDefaultEntry(0,0,0);
  must(r==0&&!actors[2].entered&&actors[0].selection==0,"standalone failed pet entry masked");
  ORDER(2);break;
 case 12:
  r=BATTLE_ClearGetExp(0);
  must(r==0&&actors[0].exp==0&&actors[2].exp==0&&actors[4].exp==0,
       "player all owned pets exp clear");
  must(actors[1].exp==33&&actors[3].exp==33,"unrelated party roster exp unchanged");break;
 default:abort();
 }
 printf("CASE|%d|PASS\n",id);
}
int main(void){
 for(int i=0;i<13;i++)case_run(i);
 puts("TOTAL|cases=13|original_bodies=3|integrated_battle=OPEN");
 return 0;
}
"""
def sha(raw):return hashlib.sha256(raw).hexdigest()
def selected(profile,root):
    if profile not in PROFILES:raise ValueError("unrecognized profile")
    commit=subprocess.check_output(["git","-C",str(root),"rev-parse","HEAD"],text=True).strip()
    if commit!=PINNED[profile]:raise ValueError("source commit drift")
    if subprocess.check_output(["git","-C",str(root),"status","--porcelain"],text=True).strip():raise ValueError("dirty source")
    p=root/LAYOUTS[profile]/"battle/battle.c"
    raw=p.read_bytes();data=raw.decode("utf-8","replace")
    functions={n:definition(data,n) for n in NAMES}
    version=root/LAYOUTS[profile]/"include/version.h"
    r=subprocess.run(["cc","-dM","-E","-x","c","-include",str(version),"-"],input="",text=True,capture_output=True,check=True)
    flags=[n for n in FEATURES if re.search(r"^#define "+re.escape(n)+r"\b",r.stdout,re.M)]
    return "\n\n".join(functions.values()),flags,sha(raw),{n:sha(v.encode()) for n,v in functions.items()}
def run(profile,source,flags,optimization,temp):
    filename=temp/(profile+optimization+".c");filename.write_text(C_HEAD+source+C_CASES)
    exe=filename.with_suffix("")
    cmd=["cc","-std=gnu99","-fgnu89-inline","-Werror=implicit-function-declaration",
         "-fsanitize=undefined","-fno-sanitize-recover=undefined",optimization,
         *(["-DAUDIT_BISMARCK"] if profile=="bismarck" else []),
         *["-D"+flag for flag in flags],str(filename),"-o",str(exe)]
    cc=subprocess.run(cmd,capture_output=True,text=True)
    if cc.returncode:raise ValueError("native compiler:"+cc.stderr[-4000:])
    p=subprocess.run([str(exe)],capture_output=True,text=True)
    if p.returncode or p.stderr:raise ValueError("native assertion/sanitizer:"+p.stderr[-4000:]+" exit="+str(p.returncode))
    if p.stdout.count("CASE|")!=13 or "integrated_battle=OPEN" not in p.stdout:
        raise ValueError("incomplete original-body native run")
    return p.stdout
def main():
    ap=argparse.ArgumentParser()
    for p in PROFILES:ap.add_argument("--"+p+"-dir",type=Path,required=True)
    a=ap.parse_args()
    with tempfile.TemporaryDirectory(prefix="stoneage-party-pet-native-") as d:
        for profile in PROFILES:
            source,flags,file_sha,func_sha=selected(profile,getattr(a,profile+"_dir"))
            x=run(profile,source,flags,"-O0",Path(d))
            y=run(profile,source,flags,"-O2",Path(d))
            if x!=y:raise ValueError("optimization trace mismatch")
            print("PROFILE|"+profile+"|source_file_sha256="+file_sha+"|function_hashes="+",".join(func_sha.values())+"|feature_flags="+",".join(flags))
            for line in x.splitlines():print(profile.upper()+"|"+line)
    print("RESOLUTION|BOUNDED_ORIGINAL_PARTY_PET_FUNCTION_EXECUTION_NO_INTEGRATED_BATTLE_PROMOTION")
if __name__=="__main__":main()
