"""Original isolated BecomePig timer/Exit sites; scheduler boundaries stay explicit."""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS, _text, _compact
from tools.stoneage_mdfyattack_source_audit import _definition, _strip
from tools.stoneage_becomepig_preaudit import analyze_profile as source_audit
from tools.stoneage_becomepig_native_audit import _if_with, _features, _run_c, _assert_rows


PREFIX = r'''
#include <stdio.h>
#include <string.h>
#include <time.h>
#define CHAR_BECOMEPIG 1
#define CHAR_BECOMEPIG_BBI 2
#define CHAR_BASEIMAGENUMBER 4
#define CHAR_WHICHTYPE 0
#define CHAR_TYPEPLAYER 1
#define CHAR_WORKBATTLEMODE 2
#define CHAR_WORKOBJINDEX 3
#define BATTLE_CHARMODE_NONE 0
#define CHAR_P_STRING_BASEBASEIMAGENUMBER 1
#define CHAR_COLORWHITE 0
#define _PETSKILL_BECOMEPIG
static int ints[8],works[8],cleanup,sendc,sendp,talks;
static int g_valid;
static time_t g_now,checkT2;
static int chikulatime2;
static struct {int use;int charaindex;} Connect[1];
static int ConnectLen=1,acfd=1,mfd=2,npcfd=3;
int CHAR_getInt(int i,int f){(void)i;return ints[f];}
void CHAR_setInt(int i,int f,int v){(void)i;ints[f]=v;}
int CHAR_getWorkInt(int i,int f){(void)i;return works[f];}
int CHAR_CHECKINDEX(int i){return i==5&&g_valid;}
void CHAR_complianceParameter(int i){(void)i;cleanup++;}
void CHAR_sendCToArroundCharacter(int i){(void)i;sendc++;}
void CHAR_send_P_StatusString(int i,int f){(void)i;(void)f;sendp++;}
void CHAR_talkToCli(int i,int a,const char *s,int c){(void)i;(void)a;(void)s;(void)c;talks++;}
static time_t harness_time(time_t *p){if(p)*p=g_now;return g_now;}
#define time harness_time
static void init(int pig,int mode){memset(ints,0,sizeof(ints));memset(works,0,sizeof(works));
 ints[1]=pig;ints[2]=999;ints[4]=777;ints[0]=1;works[2]=mode;
 cleanup=sendc=sendp=talks=0;
}
'''


def _exit_block(source):
    body = _definition(source, "_BATTLE_Exit")
    return _if_with(body, r'if\s*\(\s*CHAR_getInt\s*\(\s*(?:charaindex|char_index)\s*,\s*CHAR_BECOMEPIG\s*\)', "CHAR_BECOMEPIG_BBI")


def _net_path(name, root):
    return root/LAYOUTS[name]/("net/net.c" if name=="bismarck" else "net.c")


def _timer_source(name, root, active):
    source = _text(_net_path(name,root))
    prefix = PREFIX+"\n"+"\n".join("#define "+x for x in ("_M_SERVER","_NPCSERVER_NEW") if x in active)+"\n"
    if name != "bismarck":
        block = _if_with(source, r'if\s*\(\s*checkT2\s*!=', "CHAR_BECOMEPIG")
        c = prefix+r'''
static void one(int pig,int mode,int use,int valid,int last,int now,int cycles){
 init(pig,mode);Connect[0].use=use;Connect[0].charaindex=5;g_valid=valid;
 checkT2=last;g_now=now;chikulatime2=cycles;int NowTimes=now;
'''+block+r'''
 printf("%d %d %d %d %d %ld %d\n",ints[1],cleanup,sendc,sendp,talks,(long)checkT2,chikulatime2);
}
int main(void){int a,b,c,d,e,f,g;while(scanf("%d%d%d%d%d%d%d",&a,&b,&c,&d,&e,&f,&g)==7)one(a,b,c,d,e,f,g);return 0;}
'''
    else:
        expiry = _if_with(source, r'if\s*\(\s*CHAR_getInt\s*\(\s*char_index\s*,\s*CHAR_BECOMEPIG\s*\)', "CHAR_complianceParameter")
        outside = _if_with(source, r'if\s*\(\s*CHAR_getWorkInt\s*\(\s*char_index\s*,\s*CHAR_WORKBATTLEMODE', "CHAR_BECOMEPIG)-1")
        body = _compact(_strip(_definition(source,"CONNECT_SysEvent_Loop",raw_window=True)))
        if "checkT2" in body or "(checkT+10)<=NowTimes" not in body or "chikulatime%6==0" not in body:
            raise ValueError("Bismarck timer-site placement profile drift")
        c = prefix+r'''
static void one(int pig,int mode,int trigger6){
 init(pig,mode);int charaindex=5;
 if(trigger6){
'''+expiry+r'''
 }
'''+outside+r'''
 printf("%d %d %d %d %d\n",ints[1],cleanup,sendc,sendp,talks);
}
int main(void){int a,b,c;while(scanf("%d%d%d",&a,&b,&c)==3)one(a,b,c);return 0;}
'''
    return c.replace("char_index","charaindex")


def _timer_expected(name, vector):
    if name != "bismarck":
        pig,mode,use,valid,last,now,cycles=vector
        tick = last != now and last <= now
        cleanup = 0
        if tick and use and valid and pig > -1:
            if pig <= 1:
                pig = 0
                if mode==0:
                    pig=-1;cleanup=1
            else:
                pig-=1
        cycles = cycles+1 if tick else cycles
        if tick and cycles>1000:
            cycles=0
        return (pig,cleanup,cleanup,cleanup,cleanup,now if tick else last,cycles)
    pig,mode,trigger6=vector
    cleanup=talks=0
    if trigger6 and pig > -1:
        if pig<=1:
            pig=0
            if mode==0:
                pig=-1;cleanup=1;talks+=1
        else:
            pig-=10
    if mode==0 and pig > -1:
        pig-=1;talks+=1
    return (pig,cleanup,cleanup,cleanup,talks)


def audit_lifecycle(name, root):
    source_audit(name,root)
    active=_features(name,root)
    receipt=json.loads((Path(__file__).resolve().parents[1]/"research/recovered/STONEAGE-BECOMEPIG-LIFECYCLE-PRELIMINARY-OBSERVATION-R1.json").read_text())
    identities=next(row for row in receipt["profiles"] if row["profile"]==name)["files"]
    for row in identities.values():
        if hashlib.sha256((root/row["path"]).read_bytes()).hexdigest()!=row["sha256"]:
            raise ValueError("timer/getter/default-header source identity drift")
    counters=(-2,-1,0,1,2,9,10,11,60)
    if name != "bismarck":
        clocks=((0,0),(1,0),(0,1),(0,10),(4,4),(5,8))
        vectors=tuple((pig,mode,use,valid,last,now,cycles) for pig,mode,use,valid,(last,now),cycles in itertools.product(counters,(0,1),(0,1),(0,1),clocks,(0,999,1000)))
    else:
        vectors=tuple(itertools.product(counters,(0,1),(0,1)))
    payload="".join(" ".join(map(str,v))+"\n" for v in vectors)
    expected=[_timer_expected(name,v) for v in vectors]
    c=_timer_source(name,root,active)
    block=_exit_block(_text(root/LAYOUTS[name]/"battle/battle.c"))
    exit_c=PREFIX+r'''
static void one(int pig,int player){
 init(pig,0);ints[0]=player?1:2;int charaindex=5;
'''+block+r'''
 printf("%d %d %d %d %d\n",ints[4],cleanup,sendc,sendp,talks);
}
int main(void){int a,b;while(scanf("%d%d",&a,&b)==2)one(a,b);return 0;}
'''
    exit_c=exit_c.replace("char_index","charaindex")
    exit_vectors=tuple(itertools.product(counters,(0,1)))
    exit_payload="".join(f"{pig} {player}\n" for pig,player in exit_vectors)
    exit_expected=[(999,1,1,1,0) if pig>-1 and player else (777,0,0,0,0) for pig,player in exit_vectors]
    for optimization in ("-O0","-O2"):
        _assert_rows(_run_c(c,payload,optimization=optimization),expected,name+" timer")
        _assert_rows(_run_c(exit_c,exit_payload,optimization=optimization),exit_expected,name+" isolated Exit pig site")
    return {"profile":name,"timer_cases_per_optimization":len(vectors),
            "exit_site_cases_per_optimization":len(exit_vectors),"optimizations":2,
            "timer_scope":"original_checkT2_with_one_valid_client_slot" if name!="bismarck" else "original_counter_mutation_sites_with_explicit_sixth_tick_witness",
            "network_sha256":identities["network"]["sha256"]}


def main():
    parser=argparse.ArgumentParser()
    for name in PINNED:
        parser.add_argument("--"+name+"-dir",type=Path,required=True)
    args=parser.parse_args()
    total=0
    for name in PINNED:
        r=audit_lifecycle(name,getattr(args,name+"_dir").resolve())
        total+=2*(r["timer_cases_per_optimization"]+r["exit_site_cases_per_optimization"])
        print("PROFILE|"+"|".join(f"{k}={v}" for k,v in r.items()))
    print(f"TOTAL|timer_and_exit_site_native_comparisons={total}")
    print("FACT|gavin_iris_counter_zero_stays_active_in_battle_world_expiry_calls_cleanup_one_tick_per_qualifying_poll")
    print("FACT|bismarck_subtract10_and_world_subtract1_sites_can_leave_negative_markers_without_cleanup")
    print("BOUNDARY|Bismarck_outer_network_clock_and_recipient_iteration_not_executed_explicit_trigger6_only")
    print("BOUNDARY|Exit_original_pig_image_site_only_not_whole_Exit_or_parameter_compliance")
    print("OPEN|whole_clock_Exit_equipment_ride_ordered_round_persistent_and_coordinator_composition")
    print("RESOLUTION|BECOMEPIG_ISOLATED_NATIVE_TIMER_EXIT_SITES_PASS_ZERO_RUNTIME_PROMOTIONS")


if __name__=="__main__":
    main()
