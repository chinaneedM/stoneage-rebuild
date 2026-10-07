"""Transient original BecomePig scheduler-control projection, not whole-server execution."""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import re

from tools.stoneage_guard_break2_source_audit import PINNED, _text
from tools.stoneage_mdfyattack_source_audit import _definition, _strip
from tools.stoneage_becomepig_native_audit import _features, _if_with, _run_c, _assert_rows
from tools.stoneage_becomepig_native_lifecycle_audit import _net_path
from tools.stoneage_becomepig_preaudit import analyze_profile as source_audit

MAPS=((0,1,2,3),(3,2,1,0),(0,0,2,3),(-1,1,7,3),(1,2,3,0),(2,2,2,2))
COUNTERS=(-2,-1,0,1,2,9,10,11,60)
EXPECTED_EXCLUDED={'gavin':{1},'iris':{1,2},'bismarck':set()}
EXPECTED_PROJECTIONS={
    'gavin':'15a58856c1d09821cd875c01348df8e3a041d33706b82ad323b06a0dd5adf9f9',
    'iris':'44a2617df2da4e7fa810dd5866a2869f4d5b4ac0ec11029fcece25e4b7bd2b06',
    'bismarck':'2fbbc0ef40b23a5464a5e750e7fda7c4f46e0dc713d938e9a69c89782f4769f6',
}
TRACES=(
 ((0,0),(1,1),(9,9),(10,10),(10,10),(20,20),(60,60),(61,61)),
 ((10,10),(10,10),(9,9),(70,70),(80,80),(90,90),(100,100),(110,110)),
 ((10,11),(11,11),(21,22),(22,22),(32,31),(31,31),(42,42),(1000,1000)),
)

PREFIX=r'''
#include <stdio.h>
#include <string.h>
#include <time.h>
#define _PETSKILL_BECOMEPIG
#define CHAR_BECOMEPIG 0
#define CHAR_WORKBATTLEMODE 0
#define CHAR_WORKOBJINDEX 1
#define BATTLE_CHARMODE_NONE 0
#define CHAR_P_STRING_BASEBASEIMAGENUMBER 1
#define CHAR_COLORWHITE 0
static int pig[4],mode[4],validmask,cleanup[4],sendc[4],sendp[4],talks[4],bad;
static struct {int use;int charaindex;} Connect[4];
static int ConnectLen=4,acfd=1,mfd=2,npcfd=3;
static int sampled,stored,reads;
static time_t clock_read(time_t *p){time_t v=reads++?stored:sampled;if(p)*p=v;return v;}
#define time clock_read
int CHAR_CHECKINDEX(int i){return i>=0&&i<4&&(validmask&(1<<i));}
static int checked(int i){if(i<0||i>=4){bad++;return 0;}return i;}
int CHAR_getPlayerMaxNum(void){return 4;}
int CHAR_getInt(int i,int f){(void)f;return pig[checked(i)];}
void CHAR_setInt(int i,int f,int v){(void)f;pig[checked(i)]=v;}
int CHAR_getWorkInt(int i,int f){return f==CHAR_WORKBATTLEMODE?mode[checked(i)]:100+checked(i);}
void CHAR_complianceParameter(int i){cleanup[checked(i)]++;}
void CHAR_sendCToArroundCharacter(int object){if(object<100||object>103){bad++;return;}sendc[object-100]++;}
void CHAR_send_P_StatusString(int i,int f){(void)f;sendp[checked(i)]++;}
void CHAR_talkToCli(int i,int a,const char *s,int color){(void)a;(void)s;(void)color;talks[checked(i)]++;}
'''


def scheduler_projection(name, source):
    """Retain exact executable controls; omit unrelated source subsystem bodies."""
    body=_strip(_definition(source,'CONNECT_SysEvent_Loop',raw_window=True))
    variables=('checkT','chikulatime') if name=='bismarck' else ('checkT2','chikulatime2')
    declarations=[]
    for var in variables:
        matches=re.findall(r'static\s+(?:time_t|int)\s+'+var+r'\s*=\s*0\s*;',body)
        if len(matches)!=1:raise ValueError('scheduler static identity drift')
        declarations.extend(matches)
    samples=re.findall(r'int\s+NowTimes\s*=\s*time\s*\(\s*NULL\s*\)\s*;',body)
    if len(samples)!=1:raise ValueError('scheduler sample identity drift')
    if name!='bismarck':
        block=_if_with(body,r'if\s*\(\s*checkT2\s*!=','CHAR_BECOMEPIG')
    else:
        control=re.search(r'if\s*\(\s*checkT\s*!=\s*NowTimes\s*&&\s*\(\s*checkT\s*\+\s*10\s*\)\s*<=\s*NowTimes\s*\)\s*\{\s*int\s+i\s*;\s*checkT\s*=\s*time\s*\(\s*NULL\s*\)\s*;\s*chikulatime\+\+\s*;\s*if\s*\(\s*chikulatime\s*>\s*10000\s*\)\s*chikulatime\s*=\s*0\s*;',body)
        player=re.search(r'int\s+playernum\s*=\s*CHAR_getPlayerMaxNum\s*\(\s*\)\s*;\s*int\s+char_index\s*;\s*for\s*\(\s*char_index\s*=\s*0\s*;\s*char_index\s*<\s*playernum\s*;\s*char_index\+\+\s*\)\s*\{\s*if\s*\(\s*!CHAR_CHECKINDEX\s*\(\s*char_index\s*\)\s*\)\s*continue\s*;',body)
        sixth=re.search(r'if\s*\(\s*chikulatime\s*%\s*6\s*==\s*0\s*\)\s*\{',body)
        expiry=_if_with(body,r'if\s*\(\s*CHAR_getInt\s*\(\s*char_index\s*,\s*CHAR_BECOMEPIG\s*\)','CHAR_complianceParameter')
        outside=_if_with(body,r'if\s*\(\s*CHAR_getWorkInt\s*\(\s*char_index\s*,\s*CHAR_WORKBATTLEMODE','CHAR_BECOMEPIG)-1')
        if not control or not player or not sixth or not (control.start()<player.start()<sixth.start()<body.index(expiry)<body.index(outside)):
            raise ValueError('scheduler recipient/order identity drift')
        # Structural braces close the retained original control projection.
        block=control.group()+'\n'+player.group()+'\n'+sixth.group()+'\n'+expiry+'\n}\n'+outside+'\n}\n}'
    return '\n'.join(declarations),samples[0]+'\n'+block


def step_expected(name, pigs, modes, validmask, usemask, mapping, last, cycles, now, store_now, excluded):
    """Independent state oracle; each eligible connection remains a separate visit."""
    pigs=list(pigs)
    calls=[[0]*4 for _ in range(4)]
    tick=(last!=now and (last+10<=now if name=='bismarck' else last<=now))
    if tick:
        last=store_now;cycles+=1
        if cycles>(10000 if name=='bismarck' else 1000):cycles=0
        recipients=range(4) if name=='bismarck' else [actor for slot,actor in enumerate(mapping) if usemask&(1<<slot) and slot not in excluded]
        for actor in recipients:
            if not 0<=actor<4 or not validmask&(1<<actor):continue
            if name!='bismarck' or cycles%6==0:
                if pigs[actor]>-1:
                    if pigs[actor]<=1:
                        pigs[actor]=0
                        if modes[actor]==0:
                            pigs[actor]=-1
                            calls[actor]=[v+1 for v in calls[actor]]
                    else:pigs[actor]-=10 if name=='bismarck' else 1
            if name=='bismarck' and modes[actor]==0 and pigs[actor]>-1:
                pigs[actor]-=1;calls[actor][3]+=1
    return pigs,last,cycles,calls,1+int(tick)


def corpus(name, active):
    excluded={1}
    if '_M_SERVER' in active:excluded.add(2)
    if '_NPCSERVER_NEW' in active:excluded.add(3)
    payload=[];expected=[]
    cycles_seeds=(0,5,10000 if name=='bismarck' else 1000)
    scenarios=0
    for pig,modebits,validmask,usemask,mapid,seed,traceid in itertools.product(COUNTERS,(0,15,5),(15,5),(15,5,0),range(len(MAPS)),cycles_seeds,range(len(TRACES))):
        header=(pig,modebits,validmask,usemask,mapid,seed)
        payload.append(' '.join(map(str,header))+'\n')
        pigs=[pig]*4;last=0;cycles=seed;accum=[[0]*4 for _ in range(4)]
        for j,(now,store_now) in enumerate(TRACES[traceid]):
            # Controlled battle/world transition, not original Exit execution.
            bits=0 if traceid==2 and j>=4 else modebits
            payload.append(f'{now} {store_now} {bits}\n')
            modes=[int(bool(bits&(1<<i))) for i in range(4)]
            pigs,last,cycles,calls,reads=step_expected(name,pigs,modes,validmask,usemask,MAPS[mapid],last,cycles,now,store_now,excluded)
            for i in range(4):accum[i]=[a+b for a,b in zip(accum[i],calls[i])]
            expected.append((last,cycles,reads,0)+tuple(v for i in range(4) for v in (pigs[i],*accum[i])))
        scenarios+=1
    return ''.join(payload),expected,scenarios,excluded


def audit_clock(name, root):
    source_audit(name,root)
    receipt=json.loads((Path(__file__).resolve().parents[1]/'research/recovered/STONEAGE-BECOMEPIG-LIFECYCLE-PRELIMINARY-OBSERVATION-R1.json').read_text())
    identity=next(p for p in receipt['profiles'] if p['profile']==name)['files']['network']
    path=_net_path(name,root)
    if hashlib.sha256(path.read_bytes()).hexdigest()!=identity['sha256']:raise ValueError('network identity drift')
    active=_features(name,root)
    declarations,body=scheduler_projection(name,_text(path))
    projection_hash=hashlib.sha256(body.encode()).hexdigest()
    if projection_hash!=EXPECTED_PROJECTIONS[name]:raise ValueError('retained control projection drift')
    c=PREFIX+'\n'+'\n'.join('#define '+m for m in ('_M_SERVER','_NPCSERVER_NEW') if m in active)+'\n'+declarations+'\nstatic void poll(void){\n'+body+'\n}\n'
    clock,cycles=('checkT','chikulatime') if name=='bismarck' else ('checkT2','chikulatime2')
    c+=r'''
static int maps[6][4]={{0,1,2,3},{3,2,1,0},{0,0,2,3},{-1,1,7,3},{1,2,3,0},{2,2,2,2}};
int main(void){int initial,bits,usemask,mapid,seed;
while(scanf("%d%d%d%d%d%d",&initial,&bits,&validmask,&usemask,&mapid,&seed)==6){
 memset(cleanup,0,sizeof(cleanup));memset(sendc,0,sizeof(sendc));memset(sendp,0,sizeof(sendp));memset(talks,0,sizeof(talks));bad=0;
'''+clock+'=0;'+cycles+'=seed;'+r'''
 for(int i=0;i<4;i++){pig[i]=initial;Connect[i].use=!!(usemask&(1<<i));Connect[i].charaindex=maps[mapid][i];}
 for(int j=0;j<8;j++){
  if(scanf("%d%d%d",&sampled,&stored,&bits)!=3)return 2;
  for(int i=0;i<4;i++)mode[i]=!!(bits&(1<<i));reads=0;poll();
'''+f'printf("%ld %d %d %d",(long){clock},{cycles},reads,bad);'+r'''
  for(int i=0;i<4;i++)printf(" %d %d %d %d %d",pig[i],cleanup[i],sendc[i],sendp[i],talks[i]);puts("");
 }
}return 0;}
'''
    payload,expected,scenarios,excluded=corpus(name,active)
    if name!='bismarck' and excluded!=EXPECTED_EXCLUDED[name]:raise ValueError('default service connection exclusions drift')
    for opt in ('-O0','-O2'):_assert_rows(_run_c(c,payload,optimization=opt),expected,name+' scheduler control and recipients')
    return {'profile':name,'scenarios_per_optimization':scenarios,'polls_per_scenario':8,'snapshots_per_optimization':len(expected),'optimizations':2,'excluded_connection_slots':','.join(map(str,sorted(excluded))) if name!='bismarck' else 'not_connection_owned','network_sha256':identity['sha256'],'projection_sha256':projection_hash}


def main():
    parser=argparse.ArgumentParser()
    for name in PINNED:parser.add_argument('--'+name+'-dir',type=Path,required=True)
    args=parser.parse_args();total=0
    for name in PINNED:
        r=audit_clock(name,getattr(args,name+'_dir').resolve());total+=2*r['snapshots_per_optimization']
        print('PROFILE|'+'|'.join(f'{k}={v}' for k,v in r.items()))
    print(f'TOTAL|scheduler_recipient_native_snapshots={total}')
    print('FACT|gavin_iris_visits_used_valid_nonservice_connections_in_slot_order_no_character_deduplication')
    print('FACT|Bismarck_visits_valid_player_array_slots_independently_of_connection_mapping')
    print('FACT|one_tick_per_qualifying_poll_no_gap_catchup_clock_store_is_second_time_sample')
    print('BOUNDARY|exact_retained_scheduler_controls_only_unrelated_subsystem_bodies_omitted_compliance_stubbed')
    print('OPEN|full_server_cross_subsystem_interactions_Exit_compliance_attack_order_runtime_and_original_executable')
    print('RESOLUTION|BECOMEPIG_CLOCK_RECIPIENT_CONTROL_PROJECTION_NATIVE_PASS_ZERO_RUNTIME_PROMOTIONS')


if __name__=='__main__':main()
