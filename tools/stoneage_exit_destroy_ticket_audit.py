"""Complete original nonplayer Exit + real slot invalidation/party/ticket helpers.

Original code remains transient. Warp and item-end internals are explicit hooks;
the gate proves ordered invocation/state, not successful world movement.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import re
import subprocess

from tools.stoneage_exit_lifetime_watch_audit import source_domain as prior_domain, _definition
from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS, _text, _compact
from tools.stoneage_becomepig_restore_audit import original_functions, constants, run_native
from tools.stoneage_becomepig_native_audit import _assert_rows

PIN_PATH = Path(__file__).resolve().parents[1]/'research/recovered/STONEAGE-EXIT-DESTROY-TICKET-SOURCE-DOMAINS-R1.json'
RESOLUTION = 'BOUNDED_ORIGINAL_EXIT_DESTROY_PARTY_TICKET_PASS_ZERO_RUNTIME_PROMOTIONS'


def source_domain(profile, root):
    functions, prior = prior_domain(profile, root)
    base=root/LAYOUTS[profile]
    inc=['-I',str(base/'include')]
    if profile=='bismarck':
        inc+=['-I',str(root/'server/common'),'-I',str(root/'shared/lua51')]
    raw=re.sub(r'^\s*#\s*include[^\n]*','',_text(base/'char/char_base.c'),flags=re.M)
    pp=subprocess.run(['cpp','-P',*inc,'-'],input='#include "version.h"\n'+raw,
                      text=True,capture_output=True,check=True).stdout
    for name in ('_CHAR_setInt','_CHAR_setWorkInt'):
        functions[name]=_definition(pp,name)
        if 'CHAR_CHECKINDEX' not in _compact(functions[name]):
            raise ValueError('original setter liveness guard drift')
    callers, caller_identity=original_functions(profile,root)
    functions['_BATTLE_Exit']=callers[1]
    expected=json.loads((PIN_PATH.parent/'STONEAGE-BECOMEPIG-RESTORATION-SOURCE-DOMAINS-R1.json').read_text())['profiles'][profile]['functions']
    if caller_identity!=expected:
        raise ValueError('accepted complete caller identity drift')
    return functions,{'source_sha':PINNED[profile],'prior_domain':prior,
        'callers':caller_identity,'setters':{n:hashlib.sha256(_compact(functions[n]).encode()).hexdigest()
            for n in ('_CHAR_setInt','_CHAR_setWorkInt')},
        'contracts':{'integer_and_work_setters_guard_live_slot':True,
                     'ticket_subject_guard':profile=='bismarck'}}


def handles(functions):
    c=constants([functions['_BATTLE_Exit'],functions['party']])
    c.pop('BOOL',None)
    c.update({'CHAR_WORKBATTLEMODE':0,'CHAR_WORKPARTYMODE':600,'CHAR_WORKPARTYINDEX1':610,
              'CHAR_DATAPLACENUMBER':0,'CHAR_DATAINTNUM':1024,'CHAR_WORKDATAINTNUM':1024,
              'CHAR_PARTY_NONE':0,'CHAR_PARTY_LEADER':1,'CHAR_PARTYMAX':5,'CHAR_CDKEY':0})
    return c


def vectors():
    cases=set()
    positions=[(-1,0)]+list(itertools.product((0,1),range(10)))
    for kind,(side,pos),ptr,party,owner,ticket,start,pattern,fox in itertools.product(
        (2,3),positions,(0,1),range(3),(0,1),(-1,0,999,1000,1001),(0,900),range(3),(-1,2)):
        cases.add((kind,1,1,1,side,pos,ptr,party,owner,ticket,start,pattern,fox,1))
    # Live unmatched player is a positive ticket control, never a matched player.
    for ptr,party,owner,ticket,start,pattern,fox,mode in itertools.product(
        (0,1),range(3),(0,1),(-1,0,999,1000,1001),(0,900),range(3),(-1,2),(1,2,3)):
        cases.add((1,1,1,1,-1,0,ptr,party,owner,ticket,start,pattern,fox,mode))
    # Explicit guard cases cannot reach the excluded matched-player cleanup.
    for kind,guard,fox,ticket,mode in itertools.product(
        (1,2,3),((0,1,1),(1,0,1),(1,1,0)),(-1,2),(0,999),(1,2,3)):
        cases.add((kind,*guard,1,4,1,1,1,ticket,900,2,fox,mode))
    # All nonplayer positions at other types, exercising active battle validity.
    for kind,(side,pos),mode,ptr in itertools.product((2,3),positions,(2,3),(0,1)):
        cases.add((kind,1,1,1,side,pos,ptr,1,1,999,900,2,2,mode))
    return sorted(cases)


class Oracle:
    def __init__(self, profile,c,limits,case):
        self.profile,self.c,self.limits,self.case=profile,c,limits,case
        (self.kind,self.vc,self.vb,self.buse,self.side,self.pos,self.ptr,self.party,
         self.owner,self.ticket,self.start,self.pattern,self.fox,self.mode)=case
        self.live=[self.vc,self.owner,1]
        self.work=[{'CHAR_WORKBATTLEMODE':1,'CHAR_WORKBATTLEINDEX':0,'CHAR_WORKFOXROUND':self.fox,
                    'CHAR_WORKTICKETTIME':self.ticket,'CHAR_WORKTICKETTIMESTART':self.start}]
        self.image=100250
        self.entries=[[-1]*10 for _ in range(2)];self.escape=[[0]*10 for _ in range(2)]
        if self.side>=0:
            self.entries[self.side][self.pos]=0;self.escape[self.side][self.pos]=7
        self.trace=[];self.ends=self.badorder=self.stale_read=self.stale_write=0
        total=limits['items']+limits['pool']
        self.cleared=total if self.pattern==0 else total-4 if self.pattern==1 else 0

    def event(self,code,actor,value=0):
        self.trace.extend((code,actor,value))

    def get(self,actor,key,value):
        if not self.live[actor]:
            self.stale_read+=1;self.event(45,actor,self.c[key])
            if self.profile=='bismarck':return -1
        return value

    def set(self,key,value):
        if not self.live[0]:
            self.stale_write+=1;self.event(47,0,self.c[key]);return
        self.work[0][key]=value

    def party_update(self):
        if self.profile=='bismarck' and not self.live[0]:return
        mode=self.get(0,'CHAR_WORKPARTYMODE',self.party)
        if mode==0:return
        owner=0 if mode==1 else self.get(0,'CHAR_WORKPARTYINDEX1',1)
        if self.profile=='bismarck' and not self.live[owner]:return
        roster=[0,1,2,-1,-1] if owner==0 else [1,0,2,-1,-1]
        pno=roster.index(0)
        for j in range(pno+1):
            self.get(owner,'CHAR_WORKPARTYINDEX1',roster[j]) if j==0 else self.get_index(owner,j,roster[j])
        for j,p in enumerate(roster):
            self.get_index(owner,j,p)
            if p>=0 and p!=0:self.event(42,p,pno)

    def get_index(self,actor,j,value):
        if not self.live[actor]:
            self.stale_read+=1;self.event(45,actor,self.c['CHAR_WORKPARTYINDEX1']+j)
            if self.profile=='bismarck':return -1
        return value

    def exit(self):
        if not self.live[0]:return -101
        if not self.vb or (self.profile=='bismarck' and not self.buse):return -102
        if self.fox!=-1:
            self.image=100000;self.event(10,0,100000);self.fox=-1
            self.work[0]['CHAR_WORKFOXROUND']=-1
        if self.kind==1:self.event(28,0,0)
        if not self.buse:return -103
        matched=False
        for s in range(2):
            for pos,actor in enumerate(self.entries[s]):
                if actor==0:
                    matched=True;self.entries[s][pos]=-1;self.escape[s][pos]=0
                    self.work[0]['CHAR_WORKBATTLEMODE']=2;self.work[0]['CHAR_WORKBATTLEINDEX']=-1
                    break
        if matched and self.kind==3:
            self.event(31,0)
            if self.ptr:
                for category,size in ((100,self.limits['items']),(200,self.limits['pool'])):
                    for j in range(size):
                        value=category+j if self.pattern==2 or (self.pattern==1 and j in (0,size-1)) else -1
                        self.event(40,0,value);self.ends+=1
                self.cleared=self.limits['items']+self.limits['pool'];self.live[0]=0
            self.event(41,0,self.live[0])
        self.party_update()
        if self.profile!='bismarck' or self.live[0]:
            ticket=self.get(0,'CHAR_WORKTICKETTIME',self.work[0]['CHAR_WORKTICKETTIME'])
            if 0<ticket<1000:
                self.event(32,0,self.live[0])
                start=self.get(0,'CHAR_WORKTICKETTIMESTART',self.work[0]['CHAR_WORKTICKETTIMESTART'])
                if start>0:
                    self.get(0,'CHAR_WORKTICKETTIMESTART',start)
                    self.event(32,0,self.live[0])
                self.set('CHAR_WORKTICKETTIME',0);self.set('CHAR_WORKTICKETTIMESTART',0)
                self.event(33,0,self.live[0])
        return 0

    def run(self):
        ret1=self.exit();ret2=self.exit()
        w=self.work[0]
        return tuple([ret1,ret2,self.live[0],self.ends,self.cleared,self.stale_read,self.stale_write,
            self.badorder,self.image,w['CHAR_WORKBATTLEMODE'],w['CHAR_WORKBATTLEINDEX'],
            w['CHAR_WORKFOXROUND'],w['CHAR_WORKTICKETTIME'],w['CHAR_WORKTICKETTIMESTART'],
            *(x for row in self.entries for x in row),*(x for row in self.escape for x in row),
            len(self.trace),*self.trace])


def native_source(profile,functions,c,limits):
    h='#include <stdio.h>\n#include <stdlib.h>\n#include <string.h>\n#include <time.h>\n#define TRUE 1\n#define FALSE 0\n#define BOOL int\n'
    h+='\n'.join('#define '+k+' '+str(v) for k,v in c.items())+'\n'
    h+=f'#define CHAR_MAXITEMHAVE {limits["items"]}\n#define CHAR_MAXPOOLITEMHAVE {limits["pool"]}\n'
    h+=r'''
#define print(...) ((void)0)
#define fprint(...) ((void)0)
#define fprintf(...) ((void)0)
typedef int CHAR_DATAINT;typedef int CHAR_WORKDATAINT;
typedef struct {int use,data[1024],workint[1024],indexOfExistItems[CHAR_MAXITEMHAVE],indexOfExistPoolItems[CHAR_MAXPOOLITEMHAVE];} Char;
static Char CHAR_chara[3];static int CHAR_charanum=3;
typedef struct {int charaindex,char_index,escape;} BATTLE_ENTRY;
typedef struct {int use,type;unsigned int CreateTime;int flgTime;struct {BATTLE_ENTRY Entry[10];} Side[2];} BATTLE;
static BATTLE BattleArray[1];static int BATTLE_battlenum,ptr,trace[1024],nt,ends,badorder,stale_read,stale_write,cursor;
static void event(int code,int actor,int value){if(nt+3>1024)abort();trace[nt++]=code;trace[nt++]=actor;trace[nt++]=value;}
char *CHAR_getChar(int i,int f){(void)i;(void)f;return "x";}
'''
    h+=functions['_CHAR_CHECKINDEX']+'\n#define CHAR_CHECKINDEX(i) _CHAR_CHECKINDEX("w",0,i)\n'
    for label,name in (('get_int','CHAR_getInt'),('get_work','CHAR_getWorkInt')):
        body=functions[label]
        actual=re.search(r'int\s+(\w+)\s*\(',body).group(1)
        h+=body+'\n' if actual.startswith('_') else '#define '+actual+' original_'+actual+'\n'+body+'\n#undef '+actual+'\n'
        call=actual+'("w",0,i,f)' if actual.startswith('_') else 'original_'+actual+'(i,f)'
        code=46 if label=='get_int' else 45
        h+='int '+name+'(int i,int f){if(!CHAR_chara[i].use){stale_read++;event('+str(code)+',i,f);}return '+call+';}\n'
    h+=functions['_CHAR_setInt']+'\n'+functions['_CHAR_setWorkInt']+'\n'
    h+=r'''
int CHAR_setInt(int i,int f,int v){if(!CHAR_chara[i].use){stale_write++;event(47,i,f);}int r=_CHAR_setInt("w",0,i,f,v);if(f==CHAR_BASEIMAGENUMBER&&CHAR_chara[i].use)event(10,i,v);return r;}
int CHAR_setWorkInt(int i,int f,int v){if(!CHAR_chara[i].use){stale_write++;event(47,i,f);}return _CHAR_setWorkInt("w",0,i,f,v);}
Char *CHAR_getCharPointer(int i){return ptr&&CHAR_CHECKINDEX(i)?&CHAR_chara[i]:NULL;}
void ITEM_endExistItemsOne(int item){int value=cursor<CHAR_MAXITEMHAVE?CHAR_chara[0].indexOfExistItems[cursor]:CHAR_chara[0].indexOfExistPoolItems[cursor-CHAR_MAXITEMHAVE];
 if(value!=-1||!CHAR_chara[0].use)badorder++;cursor++;ends++;event(40,0,item);}
void CHAR_send_N_StatusString(int i,int p,int value){(void)value;event(42,i,p);}
int getPartyNum(int i){(void)i;return 5;}
'''
    if profile=='bismarck':h+=functions['CheckCharMaxItemChar']+'\n'
    for n in ('CHAR_removeHaveItem','CHAR_removeHavePoolItem','CHAR_endCharData','end_one','party'):
        h+=functions[n]+'\n'
    endcall='_CHAR_endCharOneArray(i,"w",0)' if profile=='bismarck' else 'original_CHAR_endCharOneArray(i)'
    if profile!='bismarck':
        # Rename only its definition, not the retained original body.
        body=functions['end_one']
        h=h.replace(body,'#define CHAR_endCharOneArray original_CHAR_endCharOneArray\n'+body+'\n#undef CHAR_endCharOneArray')
    h+='void CHAR_endCharOneArray(int i){event(31,i,0);'+endcall+';event(41,i,CHAR_chara[i].use);}\n'
    if profile=='bismarck':h+=functions['BATTLE_CHECKINDEX']+'\n'
    else:h+='#define BATTLE_CHECKINDEX(i) ((i)>=0&&(i)<BATTLE_battlenum)\n'
    h+=r'''
int CHAR_getFlg(int i,int f){(void)i;(void)f;abort();}
void CHAR_setFlg(int i,int f,int v){(void)i;(void)f;(void)v;abort();}
int CHAR_getCharPet(int i,int slot){(void)i;(void)slot;abort();}
void CHAR_complianceParameter(int i){(void)i;abort();}
void CHAR_sendCToArroundCharacter(int i){(void)i;abort();}
void CHAR_send_P_StatusString(int i,int f){(void)i;(void)f;abort();}
void CHAR_send_K_StatusString(int i,int slot,int f){(void)i;(void)slot;(void)f;abort();}
void CHAR_sendStatusString(int i,const char *s){(void)i;(void)s;abort();}
void BATTLE_BadStatusAllClr(int i){(void)i;abort();}
void CHAR_Skillupsend(int i){(void)i;abort();}
int getfdFromCharaIndex(int i){return i;}
int getfdFromchar_index(int i){return i;}
int CONNECT_checkfd(int i){(void)i;abort();}
void CheckDefBTime(int i,int fd,unsigned int a,unsigned int b,int extra){(void)i;(void)fd;(void)a;(void)b;(void)extra;abort();}
void lssproto_NC_send(int i,int value){event(28,i,value);}
void GmsvServer_NC_send(int i,int value){lssproto_NC_send(i,value);}
void lssproto_FS_send(int i,int f){(void)i;(void)f;abort();}
void GmsvServer_FS_send(int i,int f){lssproto_FS_send(i,f);}
void lssproto_XYD_send(int i,int x,int y,int d){(void)i;(void)x;(void)y;(void)d;abort();}
void GmsvServer_XYD_send(int i,int x,int y,int d){lssproto_XYD_send(i,x,y,d);}
void CHAR_talkToCli(int i,int a,const char *s,int color){(void)a;(void)s;(void)color;event(32,i,CHAR_chara[i].use);}
void CHAR_warpToSpecificPoint(int i,int floor,int x,int y){if(floor!=7001||x!=41||y!=6)abort();event(33,i,CHAR_chara[i].use);}
static time_t clock_read(time_t *p){if(p)*p=1000;return 1000;}
#define time clock_read
'''
    h+=functions['_BATTLE_Exit']+r'''
int main(void){int kind,vc,vb,use,side,pos,party,owner,ticket,start,pattern,fox,mode;
while(scanf("%d%d%d%d%d%d%d%d%d%d%d%d%d%d",&kind,&vc,&vb,&use,&side,&pos,&ptr,&party,&owner,&ticket,&start,&pattern,&fox,&mode)==14){
 memset(CHAR_chara,0,sizeof(CHAR_chara));memset(BattleArray,0,sizeof(BattleArray));nt=ends=badorder=stale_read=stale_write=cursor=0;
 for(int i=0;i<3;i++){CHAR_chara[i].use=1;CHAR_chara[i].data[CHAR_WHICHTYPE]=i?CHAR_TYPEPLAYER:kind;
 CHAR_chara[i].data[CHAR_BASEIMAGENUMBER]=100250;CHAR_chara[i].data[CHAR_BASEBASEIMAGENUMBER]=100000;CHAR_chara[i].data[CHAR_BECOMEPIG]=-1;
 CHAR_chara[i].workint[CHAR_WORKBATTLEMODE]=1;CHAR_chara[i].workint[CHAR_WORKFOXROUND]=-1;
 int roster0[5]={0,1,2,-1,-1},roster1[5]={1,0,2,-1,-1};for(int j=0;j<5;j++)CHAR_chara[i].workint[CHAR_WORKPARTYINDEX1+j]=i?roster1[j]:roster0[j];}
 CHAR_chara[0].use=vc;CHAR_chara[1].use=owner;CHAR_chara[0].workint[CHAR_WORKPARTYMODE]=party;
 if(party==2)CHAR_chara[0].workint[CHAR_WORKPARTYINDEX1]=1;
 CHAR_chara[0].workint[CHAR_WORKFOXROUND]=fox;CHAR_chara[0].workint[CHAR_WORKTICKETTIME]=ticket;CHAR_chara[0].workint[CHAR_WORKTICKETTIMESTART]=start;
 for(int j=0;j<CHAR_MAXITEMHAVE;j++)CHAR_chara[0].indexOfExistItems[j]=(pattern==2||(pattern==1&&(j==0||j==CHAR_MAXITEMHAVE-1)))?100+j:-1;
 for(int j=0;j<CHAR_MAXPOOLITEMHAVE;j++)CHAR_chara[0].indexOfExistPoolItems[j]=(pattern==2||(pattern==1&&(j==0||j==CHAR_MAXPOOLITEMHAVE-1)))?200+j:-1;
 BATTLE_battlenum=vb?1:0;BattleArray[0].use=use;BattleArray[0].type=mode;
 for(int s=0;s<2;s++)for(int j=0;j<10;j++){BattleArray[0].Side[s].Entry[j].charaindex=-1;BattleArray[0].Side[s].Entry[j].char_index=-1;}
 if(side>=0){BattleArray[0].Side[side].Entry[pos].charaindex=0;BattleArray[0].Side[side].Entry[pos].char_index=0;BattleArray[0].Side[side].Entry[pos].escape=7;}
 int ret1=_BATTLE_Exit("w",0,0,0),ret2=_BATTLE_Exit("w",0,0,0),cleared=0;
 for(int j=0;j<CHAR_MAXITEMHAVE;j++)cleared+=CHAR_chara[0].indexOfExistItems[j]==-1;
 for(int j=0;j<CHAR_MAXPOOLITEMHAVE;j++)cleared+=CHAR_chara[0].indexOfExistPoolItems[j]==-1;
 printf("%d %d %d %d %d %d %d %d %d",ret1,ret2,CHAR_chara[0].use,ends,cleared,stale_read,stale_write,badorder,CHAR_chara[0].data[CHAR_BASEIMAGENUMBER]);
 int fields[]={CHAR_WORKBATTLEMODE,CHAR_WORKBATTLEINDEX,CHAR_WORKFOXROUND,CHAR_WORKTICKETTIME,CHAR_WORKTICKETTIMESTART};for(int j=0;j<5;j++)printf(" %d",CHAR_chara[0].workint[fields[j]]);
'''
    field='char_index' if profile=='bismarck' else 'charaindex'
    h+='for(int s=0;s<2;s++)for(int j=0;j<10;j++)printf(" %d",BattleArray[0].Side[s].Entry[j].'+field+');\n'
    return h+r'''
 for(int s=0;s<2;s++)for(int j=0;j<10;j++)printf(" %d",BattleArray[0].Side[s].Entry[j].escape);
 printf(" %d",nt);for(int j=0;j<nt;j++)printf(" %d",trace[j]);printf("\n");}return 0;}
'''


def audit(profile,root):
    f,identity=source_domain(profile,root)
    if identity!=json.loads(PIN_PATH.read_text())['profiles'][profile]:raise ValueError('source domain drift')
    c=handles(f);limits=identity['prior_domain']['limits'];cases=vectors()
    expected=[Oracle(profile,c,limits,v).run() for v in cases]
    source=native_source(profile,f,c,limits)
    payload=''.join(' '.join(map(str,v))+'\n' for v in cases)
    for opt in ('-O0','-O2'):_assert_rows(run_native(source,payload,opt),expected,profile+' Exit destroy ticket')
    rejected=reject_mutations(profile,f,c,limits,source)
    return {'profile':profile,'source_sha':PINNED[profile],'cases_per_optimization':len(cases),
            'native_comparisons':2*len(cases),'semantic_mutations_rejected':rejected,
            'semantic_sha256':hashlib.sha256(json.dumps(expected,separators=(',',':')).encode()).hexdigest()}


def reject_mutations(profile,f,c,limits,source):
    case=(3,1,1,1,0,9,1,1,1,999,900,2,2,1)
    end=f['CHAR_endCharData']
    changed_end=re.sub(r'ch->use\s*=\s*(?:FALSE|0);','((void)0);',end)
    if profile=='bismarck':
        body=f['_BATTLE_Exit']
        changed=re.sub(r'if\s*\(CHAR_CHECKINDEX\(char_index\)\s*==\s*1\)\s*\{',
                       'if (1) {',body,count=1)
    else:
        body=f['_CHAR_setWorkInt']
        changed=re.sub(r'if\s*\(\s*!CHAR_CHECKINDEX\(\s*index\s*\)\s*\)\s*\{',
                       'if (0) {',body,count=1)
    mutations=(source.replace(end,changed_end),source.replace(body,changed))
    rejected=0
    for mutated in mutations:
        if mutated==source:raise ValueError('unapplied native mutation')
        for opt in ('-O0','-O2'):
            actual=run_native(mutated,' '.join(map(str,case))+'\n',opt)
            try:_assert_rows(actual,[Oracle(profile,c,limits,case).run()],profile+' mutation')
            except ValueError:rejected+=1
            else:raise ValueError('lifetime/guard mutation escaped oracle')
    return rejected


def main():
    p=argparse.ArgumentParser()
    for profile in PINNED:p.add_argument('--'+profile+'-dir',type=Path,required=True)
    args=p.parse_args();total=0
    for profile in PINNED:
        row=audit(profile,getattr(args,profile+'_dir'));total+=row['native_comparisons']
        print('PROFILE|'+'|'.join(f'{k}={v}' for k,v in row.items()),flush=True)
    print(f'TOTAL|exit_destroy_ticket_comparisons={total}|profiles=3')
    print('FACT|matched_enemy_actual_end_data_clears_item_slots_then_use_false_second_Exit_rejects_dead_subject')
    print('FACT|gavin_iris_stale_ticket_reads_can_invoke_talk_and_warp_hooks_after_destroy_setters_reject_ticket_clear')
    print('FACT|Bismarck_party_and_ticket_subject_guards_skip_destroyed_subjects_all_three_setters_guard_live_slot')
    print('BOUNDARY|complete_original_Exit_nonplayer_safe_positions_unmatched_player_control_actual_getters_setters_end_data_party_fixed_slots_symbolic_ABI')
    print('OPEN|actual_warp_world_object_item_end_network_stats_ownership_reuse_concurrency_original_build_JSS_Taiwan_v1_runtime')
    print('RESOLUTION|'+RESOLUTION)


if __name__=='__main__':main()
