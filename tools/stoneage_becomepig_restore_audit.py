"""Whole original default-header compliance/Exit functions with controlled dependency witnesses."""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import re
import subprocess
import tempfile

from tools.stoneage_guard_break2_source_audit import PINNED,LAYOUTS,_text,_compact
from tools.stoneage_mdfyattack_source_audit import _definition
from tools.stoneage_becomepig_native_audit import _assert_rows,_features
from tools.stoneage_becomepig_preaudit import analyze_profile as source_audit


def original_functions(name,root):
    base=root/LAYOUTS[name]
    includes=['-I',str(base/'include')]
    if name=='bismarck':includes+=['-I',str(root/'server/common'),'-I',str(root/'shared/lua51')]
    functions=[];identities={}
    for path,fn in [('char/char.c','_CHAR_complianceParameter'),('battle/battle.c','_BATTLE_Exit')]:
        raw=_definition(_text(base/path),fn,raw_window=True)
        pp=subprocess.run(['cpp','-P',*includes,'-'],input='#include "version.h"\n'+raw,text=True,capture_output=True,check=True).stdout
        body=_definition(pp,fn)
        functions.append(body)
        identities[fn]={'path':str(LAYOUTS[name]/path),'file_sha256':hashlib.sha256((base/path).read_bytes()).hexdigest(),'default_function_sha256':hashlib.sha256(_compact(body).encode()).hexdigest()}
    return functions,identities


# Symbols are witness field handles; no historical enum ordinals are selected.
def constants(functions):
    names=set(re.findall(r'\b(?:CHAR|BATTLE|ITEM|PROFESSION|SKILL)_[A-Z][A-Z0-9_]*\b','\n'.join(functions)))
    names-={'CHAR_CHECKINDEX','BATTLE_CHECKINDEX','ITEM_CHECKINDEX','BATTLE_ENTRY'}
    values={name:i+1 for i,name in enumerate(sorted(names))}
    values.update({'TRUE':1,'FALSE':0,'BOOL':1,'BATTLE_CHARMODE_NONE':0,'BATTLE_CHARMODE_FINAL':2,'CHAR_TYPEPLAYER':1,'CHAR_TYPEPET':2,'CHAR_TYPEENEMY':3,'CHAR_PETMAIL_NONE':0,'BATTLE_TYPE_P_vs_E':1,'BATTLE_TYPE_P_vs_P':2,'BATTLE_TYPE_WATCH':3,'BATTLE_ERR_NONE':0,'BATTLE_ERR_CHARAINDEX':-101,'BATTLE_ERR_BATTLEINDEX':-102,'BATTLE_ERR_NOUSE':-103,'CHAR_MAXPETHAVE':5,'CHAR_SKILLMAXHAVE':26,'BATTLE_ENTRY_MAX':10})
    for prefix in ('CHAR_P_STRING_','CHAR_K_STRING_','CHAR_FS_'):
        for i,key in enumerate(sorted(n for n in names if n.startswith(prefix))):values[key]=1<<i
    return values


COMMON=r'''
#include <stdio.h>
#include <string.h>
#include <time.h>
#define min(a,b) ((a)<(b)?(a):(b))
#define arraysizeof(a) (sizeof(a)/sizeof((a)[0]))
static int ints[2][160],works[2][160],flags[2][160],trace[256],nt,bad,validchar,validbattle,eqresult,ridekind;
static struct {long tv_sec;} NowTime={1000};
static struct {int charNo,petNo,rideNo;} ridePetTable[1];
typedef struct {int charaindex;int char_index;int escape;} BATTLE_ENTRY;
typedef struct {int use,type;unsigned int CreateTime;int flgTime;struct {BATTLE_ENTRY Entry[10];} Side[2];} BATTLE;
static BATTLE BattleArray[1];
static void event(int code,int actor,int value){if(nt+3>256){bad++;return;}trace[nt++]=code;trace[nt++]=actor;trace[nt++]=value;}
static int checked(int i){if(i<0||i>1){bad++;return 0;}return i;}
int CHAR_CHECKINDEX(int i){return i==1||(i==0&&validchar);}
int BATTLE_CHECKINDEX(int i){return i==0&&validbattle;}
int CHAR_getInt(int i,int f){return ints[checked(i)][f];}
void CHAR_setInt(int i,int f,int v){i=checked(i);ints[i][f]=v;if(f==CHAR_BASEIMAGENUMBER)event(10,i,v);if(f==CHAR_RIDEPET)event(11,i,v);}
int CHAR_getWorkInt(int i,int f){return works[checked(i)][f];}
void CHAR_setWorkInt(int i,int f,int v){works[checked(i)][f]=v;}
int CHAR_getFlg(int i,int f){return flags[checked(i)][f];}
void CHAR_setFlg(int i,int f,int v){flags[checked(i)][f]=v;}
void CHAR_initcharWorkInt(int i){event(1,i,0);works[i][CHAR_WORKFIXSTR]=10;works[i][CHAR_WORKFIXTOUGH]=20;works[i][CHAR_WORKFIXDEX]=30;works[i][CHAR_WORKFIXARRANGE]=40;works[i][CHAR_WORKFIXSEQUENCE]=50;works[i][CHAR_WORKMAXHP]=100;works[i][CHAR_WORKMAXMP]=80;}
void ITEM_equipEffect(int i){event(2,i,0);works[i][CHAR_WORKFIXSTR]+=5;works[i][CHAR_WORKFIXTOUGH]+=6;}
void Other_DefcharWorkInt(int i){event(3,i,0);}
int CHAR_getItemIndex(int i,int f){(void)i;(void)f;return eqresult<0?-1:0;}
int ITEM_CHECKINDEX(int i){return i==0;}
int ITEM_getInt(int i,int f){(void)i;(void)f;return 7;}
int CHAR_getIntPSkill(int i,int j,int f){(void)i;(void)j;(void)f;return -1;}
int CHAR_getCharPet(int i,int slot){return i==0&&slot==0?1:-1;}
int RIDEPET_getPETindex(int n,int low){(void)n;(void)low;event(5,0,0);return ridekind==2?0:-1;}
int RIDEPET_getNOindex(int n){(void)n;event(6,0,0);return 0;}
int RIDEPET_getRIDEno(int n,int p){(void)n;(void)p;event(7,0,0);return 300002;}
void CHAR_sendCToArroundCharacter(int obj){if(obj<100||obj>101){bad++;return;}event(20,obj-100,0);}
void CHAR_send_P_StatusString(int i,int f){event(21,i,f);}
void CHAR_send_K_StatusString(int i,int slot,int f){event(22,i,slot);(void)f;}
void CHAR_sendStatusString(int i,const char *s){event(23,i,s[0]);}
void CHAR_Skillupsend(int i){event(24,i,0);}
void BATTLE_BadStatusAllClr(int i){event(25,i,0);}
void CHAR_PartyUpdate(int i,int f){event(26,i,0);(void)f;}
void CheckDefBTime(int i,int fd,unsigned int a,unsigned int b,int lost){(void)fd;(void)a;(void)b;event(27,i,lost);}
int getfdFromCharaIndex(int i){return 100+i;}
int getfdFromchar_index(int i){return 100+i;}
int CONNECT_checkfd(int fd){return fd==100;}
void lssproto_NC_send(int fd,int n){event(28,fd-100,n);}
void GmsvServer_NC_send(int fd,int n){event(28,fd-100,n);}
void lssproto_XYD_send(int fd,int x,int y,int d){(void)x;(void)y;(void)d;event(29,fd-100,0);}
void GmsvServer_XYD_send(int fd,int x,int y,int d){lssproto_XYD_send(fd,x,y,d);}
void lssproto_FS_send(int fd,int f){event(30,fd-100,f);}
void GmsvServer_FS_send(int fd,int f){lssproto_FS_send(fd,f);}
void CHAR_endCharOneArray(int i){event(31,i,0);}
void CHAR_talkToCli(int i,int a,const char *s,int c){(void)a;(void)s;(void)c;event(32,i,0);}
void CHAR_warpToSpecificPoint(int i,int a,int b,int c){(void)a;(void)b;(void)c;event(33,i,0);}
static time_t clock_read(time_t *p){if(p)*p=1000;return 1000;}
#define time clock_read
'''


class Witness:
    def __init__(self,name,c,v):
        self.name=name;self.c=c;self.trace=[];self.v=v
        self.ints=[{},{}];self.works=[{},{}];self.flags=[{},{}]
        self.i=self.ints[0];self.w=self.works[0];self.f=self.flags[0]
        (action,validchar,validbattle,use,side,pos,pig,old,eq,meta,ride,kind,dead,fox,fall)=v
        self.valid=validchar;self.eq=eq;self.ride=ride
        for actor in (0,1):
            self.ints[actor].update({'CHAR_WHICHTYPE':kind if actor==0 else 2,'CHAR_BASEIMAGENUMBER':old if actor==0 else 100800,'CHAR_BASEBASEIMAGENUMBER':100000 if actor==0 else 100800,'CHAR_BECOMEPIG':pig if actor==0 else -1,'CHAR_BECOMEPIG_BBI':100388,'CHAR_HP':150 if actor==0 else 40,'CHAR_MP':90,'CHAR_RIDEPET':0 if actor==0 and ride else -1,'CHAR_MAILMODE':0})
            self.works[actor].update({'CHAR_WORKBATTLEMODE':1,'CHAR_WORKBATTLEINDEX':0,'CHAR_WORKOBJINDEX':100+actor,'CHAR_WORKPETFOLLOW':-1,'CHAR_WORKFOXROUND':fox if actor==0 else -1,'CHAR_WORKPETFALL':fall if actor==0 else 0,'CHAR_WORKITEMMETAMO':(999,1000,1001,0)[meta] if actor==0 else 0,'CHAR_WORKNPCMETAMO':int(meta==3) if actor==0 else 0})
            self.flags[actor]['CHAR_ISDIE']=dead if actor==0 else 0
        self.entries=[[-1]*10,[-1]*10];self.escapes=[[0]*10,[0]*10]
        if side>=0:self.entries[side][pos]=0;self.entries[side][pos+5]=1;self.escapes[side][pos]=7

    def event(self,code,actor,value=0):self.trace.extend((code,actor,value))
    def setint(self,actor,key,value):
        self.ints[actor][key]=value
        if key=='CHAR_BASEIMAGENUMBER':self.event(10,actor,value)
        if key=='CHAR_RIDEPET':self.event(11,actor,value)

    def compliance(self,actor):
        i,w,f=self.ints[actor],self.works[actor],self.flags[actor]
        if actor==0 and not self.valid:return 0
        self.event(1,actor);self.event(2,actor)
        w.update({'CHAR_WORKATTACKPOWER':15,'CHAR_WORKDEFENCEPOWER':26,'CHAR_WORKQUICK':30,'CHAR_WORKARRANGEPOWER':40,'CHAR_WORKSEQUENCEPOWER':50})
        self.event(3,actor);i['CHAR_HP']=min(i['CHAR_HP'],100);i['CHAR_MP']=min(i['CHAR_MP'],80)
        if f['CHAR_ISDIE']:return 1
        old=i['CHAR_BASEIMAGENUMBER'];self.event(4,actor,7 if self.eq>=0 else self.c['ITEM_FIST'])
        new=self.eq if actor==0 else i['CHAR_BASEBASEIMAGENUMBER']
        item=w['CHAR_WORKITEMMETAMO']>1000;npc=w['CHAR_WORKNPCMETAMO']>0
        if item or npc or i['CHAR_BECOMEPIG']>-1:new=old
        if old==100259 or (self.name=='bismarck' and old==100362):new=old
        if i['CHAR_WHICHTYPE']==2 and w['CHAR_WORKBATTLEMODE']!=0 and old==101428:new=old
        if i['CHAR_WHICHTYPE']==3:return 0
        if self.name!='bismarck' or i['CHAR_RIDEPET']==-1:self.setint(actor,'CHAR_BASEIMAGENUMBER',i['CHAR_BASEBASEIMAGENUMBER'] if new==-1 else new)
        if self.name=='bismarck':return 1
        if item or npc:return 0
        if i['CHAR_RIDEPET']!=-1:
            found=self.ride==1
            if found:self.setint(actor,'CHAR_BASEIMAGENUMBER',300001)
            self.event(5,0)
            if self.ride==2:
                self.event(6,0);self.event(7,0);self.setint(actor,'CHAR_BASEIMAGENUMBER',300002);found=True
            if not found:
                self.setint(actor,'CHAR_RIDEPET',-1);self.setint(actor,'CHAR_BASEIMAGENUMBER',i['CHAR_BASEBASEIMAGENUMBER']);self.event(20,actor);self.event(21,actor,self.c['CHAR_P_STRING_RIDEPET'])
        return 1

    def execute(self):
        action,validchar,validbattle,use,side,pos,*_=self.v
        if action==0:return self.compliance(0)
        if not validchar:return -101
        if not validbattle:return -102
        if self.i['CHAR_BASEIMAGENUMBER']==101749 or self.w['CHAR_WORKFOXROUND']!=-1:
            self.setint(0,'CHAR_BASEIMAGENUMBER',100000);self.w['CHAR_WORKFOXROUND']=-1
        if self.i['CHAR_BECOMEPIG']>-1:
            self.setint(0,'CHAR_BASEIMAGENUMBER',100388);self.compliance(0);self.event(20,0);self.event(21,0,self.c['CHAR_P_STRING_BASEBASEIMAGENUMBER'])
        self.event(28,0)
        if not use:return -103
        if side>=0:
            self.entries[side][pos]=-1;self.escapes[side][pos]=0
            self.w['CHAR_WORKBATTLEMODE']=2;self.w['CHAR_WORKBATTLEINDEX']=-1
            lost=bool(self.f['CHAR_ISDIE'] or (self.name!='bismarck' and self.i['CHAR_HP']==1));self.event(27,0,10 if lost else 0)
            if lost:self.f['CHAR_ISDIE']=0;self.i['CHAR_HP']=1
            self.entries[side][pos+5]=-1;self.works[1]['CHAR_WORKBATTLEMODE']=0;self.works[1]['CHAR_WORKBATTLEINDEX']=-1
            self.event(25,0);self.compliance(0);self.event(24,0)
            if self.w['CHAR_WORKPETFALL']:
                self.w['CHAR_WORKPETFALL']=0;self.setint(0,'CHAR_RIDEPET',-2)
            status=0
            for key in ('HP','EXP','MP','DUELPOINT','CHARM','EARTH','WATER','FIRE','WIND','RIDEPET'):status|=self.c['CHAR_P_STRING_'+key]
            self.event(21,0,status)
            if self.i['CHAR_RIDEPET']==-2:self.setint(0,'CHAR_RIDEPET',-1)
            # Only owned slot0 contains a live pet; mail/oblivion are inactive.
            self.works[1]['CHAR_WORKBATTLEMODE']=0
            if self.ints[1]['CHAR_BASEIMAGENUMBER']!=100800:self.setint(1,'CHAR_BASEIMAGENUMBER',100800);self.event(23,0,ord('K'))
            self.event(25,1);self.compliance(1);self.event(22,0,0);self.event(29,0)
        self.event(26,0)
        return 0

    def row(self,ret):
        values=[ret,0]
        for actor in (0,1):
            for key in ('CHAR_BASEIMAGENUMBER','CHAR_RIDEPET','CHAR_BECOMEPIG','CHAR_HP','CHAR_MP'):values.append(self.ints[actor].get(key,0))
            for key in ('CHAR_WORKBATTLEMODE','CHAR_WORKBATTLEINDEX','CHAR_WORKFOXROUND','CHAR_WORKPETFALL','CHAR_WORKATTACKPOWER','CHAR_WORKDEFENCEPOWER','CHAR_WORKQUICK','CHAR_WORKARRANGEPOWER','CHAR_WORKSEQUENCEPOWER'):values.append(self.works[actor].get(key,0))
            values.append(self.flags[actor].get('CHAR_ISDIE',0))
        values.extend(self.entries[0]+self.entries[1]+self.escapes[0]+self.escapes[1]);values.append(len(self.trace));values.extend(self.trace)
        return tuple(values)


def vectors():
    fixtures=itertools.product((-2,-1,0,180),(100250,100259,100362,101428),(-1,100015),range(4),range(4),(1,2,3),(0,1))
    for pig,old,eq,meta,ride,kind,dead in fixtures:
        yield (0,1,1,1,-1,0,pig,old,eq,meta,ride,kind,dead,-1,0)
        if kind==1:
            for (validchar,validbattle,use,side,pos),fox,fall in itertools.product(((0,1,1,0,0),(1,0,1,0,0),(1,1,0,0,0),(1,1,1,-1,0),(1,1,1,0,0),(1,1,1,1,4)),(-1,2),(0,1)):
                yield (1,validchar,validbattle,use,side,pos,pig,old,eq,meta,ride,kind,dead,fox,fall)
    for dead in (0,1):yield (0,0,1,1,-1,0,180,100250,-1,0,0,1,dead,-1,0)


def native_source(name,functions,c):
    defs='\n'.join('#define '+key+' '+('int' if key=='BOOL' else str(value)) for key,value in c.items())
    mapping='int CHAR_getNewImagenumberFromEquip('+('int index,' if name=='bismarck' else '')+'int base,int category){event(4,'+('index' if name=='bismarck' else '(base==100800?1:0)')+',category);return base==100800?base:eqresult;}\n'
    source=defs+'\n'+COMMON+'\n'+mapping+functions[0]+'\n#define CHAR_complianceParameter(i) _CHAR_complianceParameter(i,"witness",0)\n'+functions[1]
    source+=r'''
int main(void){int action,vc,vb,use,side,pos,pig,old,eq,meta,ride,kind,dead,fox,fall;
while(scanf("%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d",&action,&vc,&vb,&use,&side,&pos,&pig,&old,&eq,&meta,&ride,&kind,&dead,&fox,&fall)==15){
 memset(ints,0,sizeof(ints));memset(works,0,sizeof(works));memset(flags,0,sizeof(flags));memset(BattleArray,0,sizeof(BattleArray));nt=bad=0;validchar=vc;validbattle=vb;eqresult=eq;ridekind=ride;
 for(int i=0;i<2;i++){
 ints[i][CHAR_WHICHTYPE]=i==0?kind:CHAR_TYPEPET;ints[i][CHAR_BASEIMAGENUMBER]=i==0?old:100800;ints[i][CHAR_BASEBASEIMAGENUMBER]=i==0?100000:100800;
 ints[i][CHAR_BECOMEPIG]=i==0?pig:-1;ints[i][CHAR_BECOMEPIG_BBI]=100388;ints[i][CHAR_HP]=i==0?150:40;ints[i][CHAR_MP]=90;ints[i][CHAR_RIDEPET]=i==0&&ride?0:-1;
 works[i][CHAR_WORKBATTLEMODE]=1;works[i][CHAR_WORKOBJINDEX]=100+i;works[i][CHAR_WORKPETFOLLOW]=-1;works[i][CHAR_WORKFOXROUND]=i==0?fox:-1;works[i][CHAR_WORKPETFALL]=i==0?fall:0;
 int mt[4]={999,1000,1001,0};works[i][CHAR_WORKITEMMETAMO]=i==0?mt[meta]:0;works[i][CHAR_WORKNPCMETAMO]=i==0&&meta==3;
 flags[i][CHAR_ISDIE]=i==0?dead:0;
 }
 ridePetTable[0].charNo=ride==1?100000:-99;ridePetTable[0].petNo=100800;ridePetTable[0].rideNo=300001;
 BattleArray[0].use=use;BattleArray[0].type=1;BattleArray[0].CreateTime=500;BattleArray[0].flgTime=1000;
 for(int s=0;s<2;s++)for(int j=0;j<10;j++){BattleArray[0].Side[s].Entry[j].charaindex=-1;BattleArray[0].Side[s].Entry[j].char_index=-1;}
 if(side>=0){BattleArray[0].Side[side].Entry[pos].charaindex=0;BattleArray[0].Side[side].Entry[pos].char_index=0;BattleArray[0].Side[side].Entry[pos].escape=7;BattleArray[0].Side[side].Entry[pos+5].charaindex=1;BattleArray[0].Side[side].Entry[pos+5].char_index=1;}
 int result=action?_BATTLE_Exit("witness",0,0,0):_CHAR_complianceParameter(0,"witness",0);printf("%d %d",result,bad);
 int inf[]={CHAR_BASEIMAGENUMBER,CHAR_RIDEPET,CHAR_BECOMEPIG,CHAR_HP,CHAR_MP};
 int wf[]={CHAR_WORKBATTLEMODE,CHAR_WORKBATTLEINDEX,CHAR_WORKFOXROUND,CHAR_WORKPETFALL,CHAR_WORKATTACKPOWER,CHAR_WORKDEFENCEPOWER,CHAR_WORKQUICK,CHAR_WORKARRANGEPOWER,CHAR_WORKSEQUENCEPOWER};
 for(int i=0;i<2;i++){for(int j=0;j<5;j++)printf(" %d",ints[i][inf[j]]);for(int j=0;j<9;j++)printf(" %d",works[i][wf[j]]);printf(" %d",flags[i][CHAR_ISDIE]);}
'''
    source+='for(int s=0;s<2;s++)for(int j=0;j<10;j++)printf(" %d",BattleArray[0].Side[s].Entry[j].'+('char_index' if name=='bismarck' else 'charaindex')+');\n'
    return source+r'''
 for(int s=0;s<2;s++)for(int j=0;j<10;j++)printf(" %d",BattleArray[0].Side[s].Entry[j].escape);
 printf(" %d",nt);for(int j=0;j<nt;j++)printf(" %d",trace[j]);puts("");
}return 0;}
'''


def run_native(source,payload,opt):
    with tempfile.TemporaryDirectory(prefix='sa-pig-restore-') as d:
        p=Path(d);(p/'w.c').write_text(source)
        result=subprocess.run(['cc','-std=gnu99',opt,'-fsanitize=undefined','-fno-sanitize-recover=all',str(p/'w.c'),'-o',str(p/'w')],text=True,capture_output=True)
        if result.returncode:raise ValueError('whole original function compile failed: '+result.stderr[-4000:])
        result=subprocess.run([str(p/'w')],input=payload,text=True,capture_output=True)
        if result.returncode or result.stderr:raise ValueError('whole original function native/UBSan failed: '+result.stderr[-2000:])
        return [tuple(map(int,line.split())) for line in result.stdout.splitlines()]


def audit_restore(name,root):
    source_audit(name,root);active=_features(name,root)
    if (('_NEW_RIDEPETS' in active)!=(name!='bismarck')) or not {'_ITEM_METAMO','_NPCCHANGE_PLAYERIMG','_ENEMY_FALLGROUND','_ITEMSET5_TXT','_VARY_WOLF'}<=active:raise ValueError('restoration default feature drift')
    functions,identities=original_functions(name,root);c=constants(functions)
    pins=json.loads((Path(__file__).resolve().parents[1]/'research/recovered/STONEAGE-BECOMEPIG-RESTORATION-SOURCE-DOMAINS-R1.json').read_text())['profiles'][name]
    if identities!=pins['functions'] or {f:f in active for f in pins['features']}!=pins['features']:
        raise ValueError('default function or restoration feature identity drift')
    if '_MULTIPLAYER_' in active:raise ValueError('larger original entry topology excluded')
    c['CHAR_SKILLMAXHAVE']=26 if '_PROFESSION_SKILL' in active else 5
    vs=list(vectors());payload=''.join(' '.join(map(str,v))+'\n' for v in vs)
    expected=[]
    for v in vs:
        state=Witness(name,c,v);ret=state.execute();expected.append(state.row(ret))
    source=native_source(name,functions,c)
    for opt in ('-O0','-O2'):_assert_rows(run_native(source,payload,opt),expected,name+' whole compliance and Exit')
    return {'profile':name,'cases_per_optimization':len(vs),'compliance_cases':sum(v[0]==0 for v in vs),'exit_cases':sum(v[0]==1 for v in vs),'optimizations':2,'identities':identities}


def main():
    parser=argparse.ArgumentParser()
    for name in PINNED:parser.add_argument('--'+name+'-dir',type=Path,required=True)
    args=parser.parse_args();total=0
    for name in PINNED:
        r=audit_restore(name,getattr(args,name+'_dir').resolve());total+=r['cases_per_optimization']*2
        print('PROFILE|'+'|'.join(f'{k}={v}' for k,v in r.items() if k!='identities'))
        for fn,identity in r['identities'].items():print('SOURCE|profile='+name+'|function='+fn+'|'+'|'.join(f'{k}={v}' for k,v in identity.items()))
    print(f'TOTAL|whole_compliance_exit_native_comparisons={total}')
    print('BOUNDARY|entire_default_header_function_bodies_no_projection_controlled_equipment_ride_lookup_stats_badstatus_network_helpers')
    print('BOUNDARY|valid_owned_pet_and_player_entry_slots0_or4_PvE_inactive_profession_follow_mail_ticket_domains')
    print('OPEN|original_helper_bodies_actual_equipment_ride_tables_PvP_watch_invalid_rider_enemy_deletion_attack_order_and_runtime')
    print('RESOLUTION|BECOMEPIG_BOUNDED_WHOLE_COMPLIANCE_EXIT_NATIVE_PASS_ZERO_RUNTIME_PROMOTIONS')


if __name__=='__main__':main()
