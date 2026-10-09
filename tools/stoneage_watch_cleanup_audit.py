"""Original watcher Stop/Loop cleanup under explicit controlled Exit semantics.

Original source stays transient. Pinned hashes, independent state/trace oracle,
and derived results are the only repository evidence.
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
from tools.stoneage_becomepig_restore_audit import run_native
from tools.stoneage_becomepig_native_audit import _assert_rows

PIN_PATH = Path(__file__).resolve().parents[1] / 'research/recovered/STONEAGE-WATCH-CLEANUP-SOURCE-DOMAINS-R1.json'
RESOLUTION = 'BOUNDED_ORIGINAL_WATCH_STOP_LOOP_CLEANUP_PASS_ZERO_RUNTIME_PROMOTIONS'
NAMES = ('BATTLE_Stop', 'BATTLE_StopSet', 'BATTLE_FinishSet', 'BATTLE_CountAlive',
         'BATTLE_WatchStop', 'BATTLE_Loop')
MODES = dict(zip(('NONE','INIT','BATTLE','FINISH','STOP','WATCHBC','WATCHPRE',
                 'WATCHWAIT','WATCHMOVIE','WATCHAFTER'), range(10)))


def source_domain(profile, root):
    functions, prior = prior_domain(profile, root)
    base = root / LAYOUTS[profile]
    inc = ['-I', str(base/'include')]
    if profile == 'bismarck':
        inc += ['-I', str(root/'server/common'), '-I', str(root/'shared/lua51')]
    raw = re.sub(r'^\s*#\s*include[^\n]*', '', _text(base/'battle/battle.c'), flags=re.M)
    pp = subprocess.run(['cpp','-P',*inc,'-'], input='#include "version.h"\n'+raw,
                        text=True, capture_output=True, check=True).stdout
    extra = {n: _definition(pp,n) for n in NAMES}
    functions.update(extra)
    c = {n:_compact(b) for n,b in extra.items()}
    loop = c['BATTLE_Loop']
    if not (loop.index('BATTLE_CountAlive(i,0)') < loop.index('BATTLE_FinishSet(i)') < loop.index('switch(')):
        raise ValueError('empty-watch cleanup dispatch order drift')
    if 'i<BATTLE_battlenum' not in loop or 'cnt++' not in loop:
        raise ValueError('ascending task scan drift')
    stop = c['BATTLE_WatchStop']
    if not (stop.index('BATTLE_Exit(') < stop.index('CHAR_DischargePartyNoMsg(') < stop.index('CHAR_talkToCli(')):
        raise ValueError('WatchStop ordering drift')
    if 'BATTLE_DeleteBattle(' in stop or 'BATTLE_WatchUnLink(' in stop:
        raise ValueError('WatchStop deferred cleanup contract drift')
    if ('CHAR_WATCHBATTLETYPE' in stop) != (profile == 'bismarck'):
        raise ValueError('WatchStop profile flag drift')
    return functions, {'source_sha':PINNED[profile], 'prior_domain':prior,
        'functions':{n:hashlib.sha256(_compact(b).encode()).hexdigest() for n,b in extra.items()},
        'contracts':{'empty_watch_finish_before_dispatch':True, 'ascending_array_task_scan':True,
                     'watch_stop_does_not_delete_or_unlink':True,
                     'watch_stop_clears_watch_type':profile == 'bismarck'}}


def vectors():
    # All physical placements of a root + 0..3 acyclic watcher nodes in five slots.
    for count in range(4):
        for order in itertools.permutations(range(5), count+1):
            padded = (*order, *([-1]*(4-len(order))))
            for action, kind, slot in itertools.product(range(5), range(3), (0,4,9)):
                yield (action,count,kind,slot,*padded)


class Oracle:
    """Independent list/state model; never executes or parses C for expectations."""
    def __init__(self, profile, case):
        self.profile = profile
        self.action,self.count,self.kind,self.slot,*padded = case
        self.order = padded[:self.count+1]
        self.root = self.order[0]
        self.chain = self.order.copy()
        self.use = [int(i in self.order) for i in range(5)]
        self.mode = [5 if i in self.order[1:] else 0 for i in range(5)]
        self.entries = [i+1 if self.use[i] else -1 for i in range(5)]
        self.workindex = [i if self.use[i] else -1 for i in range(5)]
        self.workmode = [1 if self.use[i] else 0 for i in range(5)]
        self.watchtype = [9]*5
        self.trace = []
        self.profit = self.exits = self.deleted = 0

    def event(self, code, node):
        self.trace.extend((code,node))

    def exit(self,node):
        self.event(2,node)
        self.exits |= 1<<node
        self.entries[node] = -1
        self.workindex[node] = -1
        self.workmode[node] = 2

    def profit_exit(self,node):
        if self.entries[node] >= 0:
            self.profit |= 1<<node
            self.event(1,node)
            self.exit(node)

    def delete(self,node):
        if node in self.chain:
            self.chain.remove(node)
        self.use[node] = 0
        self.mode[node] = 0
        self.entries[node] = -1
        self.deleted |= 1<<node
        self.event(3,node)

    def finish(self,node):
        self.profit_exit(node)
        if node == self.root:
            watches = self.chain[self.chain.index(node)+1:]
            for w in watches:
                if self.entries[w] >= 0:
                    self.exit(w)
                    self.workmode[w] = 2
            # Retain original first-only traversal defect, without patching it.
            if watches:
                self.delete(watches[0])
        self.delete(node)

    def watch_stop(self,node):
        b = self.workindex[node]
        if b < 0 or (self.profile == 'bismarck' and not self.use[b]):
            return
        self.exit(b)
        self.event(4,node)
        self.event(5,node)
        if self.profile == 'bismarck':
            self.watchtype[node] = 0
        self.event(6,node)

    def loop(self):
        processed = 0
        for node in range(5):
            if not self.use[node]:
                continue
            # CountAlive ignores pets and dead flags; root is always a live player.
            if node != self.root and (self.entries[node] < 0 or self.kind != 0):
                self.mode[node] = 3
            if self.mode[node] == 3:
                self.finish(node)
            elif self.mode[node] == 4:
                self.profit_exit(node)
                self.delete(node)
            processed += 1
        return processed

    def snapshot(self,processed):
        row = [processed,sum(self.use)]
        for node in range(5):
            if node in self.chain:
                pos = self.chain.index(node)
                before = self.chain[pos-1] if pos else -1
                after = self.chain[pos+1] if pos+1 < len(self.chain) else -1
            else:
                before = after = -1
            row.extend((self.use[node],self.mode[node],before,after,self.entries[node],
                        self.workindex[node],self.workmode[node],self.watchtype[node]))
        row.extend((self.profit,self.exits,self.deleted,len(self.trace),*self.trace))
        return row

    def run(self):
        if self.action == 0:
            self.finish(self.root)
        elif self.action in (1,2):
            self.mode[self.root] = 3 if self.action == 1 else 4
        elif self.action == 3:
            self.watch_stop(self.order[-1])
        else:
            for node in self.order[1:]:
                self.watch_stop(node)
        row = self.snapshot(-1)
        row.extend(self.snapshot(self.loop()))
        row.extend(self.snapshot(self.loop()))
        return tuple(row)


def native_source(profile, functions):
    names = ('BATTLE_WatchUnLink','BATTLE_DeleteBattle','BATTLE_Finish',*NAMES)
    bodies = '\n'.join(functions[n] for n in names)
    symbols = set(re.findall(r'\b(?:CHAR|BATTLE)_[A-Z][A-Z0-9_]*\b',bodies))
    constants = {n:j+30 for j,n in enumerate(sorted(symbols)) if n not in
                 ('CHAR_CHECKINDEX','BATTLE_CHECKINDEX','BATTLE_CHECKSIDE','BATTLE_CHECKADDRESS','BATTLE_ENTRY')}
    constants.update({'BATTLE_ENTRY_MAX':10,'BATTLE_TYPE_P_vs_E':1,'BATTLE_TYPE_P_vs_P':2,
                      'BATTLE_TYPE_WATCH':3,'BATTLE_CHARMODE_FINAL':2,'CHAR_TYPEPET':2,
                      'CHAR_TYPEPLAYER':1,'CHAR_WORKBATTLEINDEX':0,'CHAR_WORKBATTLEMODE':1,
                      'CHAR_WATCHBATTLETYPE':2,'CHAR_WHICHTYPE':0,'CHAR_ISDIE':0})
    constants.update({'BATTLE_MODE_'+k:v for k,v in MODES.items()})
    head = '#include <stdio.h>\n#include <string.h>\n#include <stdlib.h>\n#define TRUE 1\n#define FALSE 0\n#define BOOL int\n'
    head += '\n'.join('#define '+k+' '+str(v) for k,v in constants.items())+'\n'
    head += r'''
typedef struct {int charaindex,char_index,escape;} BATTLE_ENTRY;
typedef struct BATTLE {int use,mode,battleindex,type,winside,createindex;void (*WinFunc)(int,int);struct BATTLE *pNext,*pBefore;struct {BATTLE_ENTRY Entry[10];} Side[2];} BATTLE;
static BATTLE BattleArray[5];static int BATTLE_battlenum=5,Total_BattleNum;
static int work[6][3],kinds[6],dead[6],trace[256],nt,profitmask,exitmask,deletemask;
static void event(int code,int node){trace[nt++]=code;trace[nt++]=node;}
#define BATTLE_CHECKADDRESS(a) ((&BattleArray[0])<=(a)&&(a)<=(&BattleArray[4]))
#define BATTLE_CHECKSIDE(s) ((s)==0||(s)==1)
#define fprint(...) ((void)0)
int CHAR_CHECKINDEX(int i){return i>=1&&i<=5;}
int CHAR_getWorkInt(int i,int f){return work[i][f];}
void CHAR_setWorkInt(int i,int f,int v){work[i][f]=v;}
int CHAR_getInt(int i,int f){(void)f;return kinds[i];}
void CHAR_setInt(int i,int f,int v){(void)i;(void)f;(void)v;}
int CHAR_getFlg(int i,int f){(void)f;return dead[i];}
void NETWATCH_set(const char *s,int i,const char *v){(void)s;(void)i;(void)v;}
void EntryInit(BATTLE_ENTRY *e){e->char_index=e->charaindex=-1;e->escape=0;}
void BATTLE_DeleteItem(int i){deletemask|=1<<i;event(3,i);}
void BATTLE_GetProfit(int b,int s,int p){(void)s;(void)p;profitmask|=1<<b;event(1,b);}
void BATTLE_Exit(int actor,int b){exitmask|=1<<b;event(2,b);work[actor][0]=-1;work[actor][1]=2;
 for(int s=0;s<2;s++)for(int p=0;p<10;p++)if(BattleArray[b].Side[s].Entry[p].charaindex==actor)EntryInit(&BattleArray[b].Side[s].Entry[p]);}
void CHAR_DischargePartyNoMsg(int i){event(4,i-1);}
void CHAR_talkToCli(int i,int a,const char *s,int c){(void)a;(void)s;(void)c;event(5,i-1);}
int getfdFromCharaIndex(int i){return i;}
int getfdFromchar_index(int i){return i;}
void lssproto_B_send(int fd,const char *s){(void)s;event(6,fd-1);}
void GmsvServer_B_send(int fd,const char *s){lssproto_B_send(fd,s);}
int BATTLE_Init(int i){(void)i;abort();}
int BATTLE_Command(int i){(void)i;abort();}
int BATTLE_WatchBC(int i){(void)i;return 0;}
int BATTLE_WatchPre(int i){(void)i;abort();}
int BATTLE_WatchWait(int i){(void)i;abort();}
int BATTLE_WatchMovie(int i){(void)i;abort();}
int BATTLE_WatchAfter(int i){(void)i;abort();}
'''
    if profile == 'bismarck':
        head += functions['BATTLE_CHECKINDEX']+'\n'
    else:
        head += '#define BATTLE_CHECKINDEX(a) (((a)>=5||(a)<0)?FALSE:TRUE)\n'
    head += bodies+r'''
static void snapshot(int processed){printf(" %d %d",processed,Total_BattleNum);
 for(int b=0;b<5;b++){int e=-1;for(int p=0;p<10;p++)if(BattleArray[b].Side[0].Entry[p].charaindex>=0)e=BattleArray[b].Side[0].Entry[p].charaindex;
 printf(" %d %d %d %d %d %d %d %d",BattleArray[b].use,BattleArray[b].mode,
 BattleArray[b].pBefore?(int)(BattleArray[b].pBefore-BattleArray):-1,
 BattleArray[b].pNext?(int)(BattleArray[b].pNext-BattleArray):-1,
 e,work[b+1][0],work[b+1][1],work[b+1][2]);}
 printf(" %d %d %d %d",profitmask,exitmask,deletemask,nt);for(int j=0;j<nt;j++)printf(" %d",trace[j]);}
int main(void){int action,count,kind,slot,order[4];
 while(scanf("%d%d%d%d%d%d%d%d",&action,&count,&kind,&slot,&order[0],&order[1],&order[2],&order[3])==8){
 memset(BattleArray,0,sizeof(BattleArray));memset(work,0,sizeof(work));memset(dead,0,sizeof(dead));nt=profitmask=exitmask=deletemask=0;Total_BattleNum=count+1;
 for(int b=0;b<5;b++){BattleArray[b].battleindex=b;work[b+1][0]=-1;work[b+1][2]=9;kinds[b+1]=1;
 for(int s=0;s<2;s++)for(int p=0;p<10;p++)EntryInit(&BattleArray[b].Side[s].Entry[p]);}
 for(int j=0;j<=count;j++){int b=order[j];BattleArray[b].use=1;BattleArray[b].type=j?3:1;BattleArray[b].mode=j?5:0;
 BattleArray[b].pBefore=j?&BattleArray[order[j-1]]:NULL;BattleArray[b].pNext=j<count?&BattleArray[order[j+1]]:NULL;
 BattleArray[b].Side[0].Entry[slot].charaindex=BattleArray[b].Side[0].Entry[slot].char_index=b+1;
 work[b+1][0]=b;work[b+1][1]=1;if(j){dead[b+1]=kind==1;kinds[b+1]=kind==2?2:1;}}
 int root=order[0];
 if(action==0)BATTLE_Finish(root);else if(action==1)BATTLE_FinishSet(root);else if(action==2)BATTLE_StopSet(root);
 else if(action==3)BATTLE_WatchStop(order[count]+1);else for(int j=1;j<=count;j++)BATTLE_WatchStop(order[j]+1);
 snapshot(-1);int p=BATTLE_Loop();snapshot(p);p=BATTLE_Loop();snapshot(p);printf("\n");
 }return 0;}
'''
    return head


def audit(profile, root):
    functions, identity = source_domain(profile, root)
    if identity != json.loads(PIN_PATH.read_text())['profiles'][profile]:
        raise ValueError('watch-cleanup source identity drift')
    cases = list(vectors())
    expected = [Oracle(profile,v).run() for v in cases]
    payload = ''.join(' '.join(map(str,v))+'\n' for v in cases)
    for opt in ('-O0','-O2'):
        _assert_rows(run_native(native_source(profile,functions),payload,opt),expected,profile+' watch cleanup')
    rejected = reject_mutations(profile, functions)
    return {'profile':profile,'source_sha':PINNED[profile],'cases_per_optimization':len(cases),
            'native_comparisons':2*len(cases),
            'semantic_mutations_rejected':rejected,
            'semantic_sha256':hashlib.sha256(json.dumps(expected,separators=(',',':')).encode()).hexdigest()}


def reject_mutations(profile, functions):
    # Only transient generated witness C is altered; pinned source remains clean.
    source = native_source(profile, functions)
    no_finish = re.sub(r'BATTLE_FinishSet\(\s*i\s*\);', '((void)0);', source)
    stop = functions['BATTLE_WatchStop']
    no_exit = re.sub(r'\bBATTLE_Exit\([^;]+;', '((void)0);', stop)
    experiments = ((no_finish,(0,3,0,4,4,0,1,2)),
                   (source.replace(stop,no_exit),(4,3,0,4,4,0,1,2)))
    rejected = 0
    for changed, case in experiments:
        if changed == source:
            raise ValueError('native mutation did not alter witness')
        for opt in ('-O0','-O2'):
            actual = run_native(changed,' '.join(map(str,case))+'\n',opt)
            try:
                _assert_rows(actual,[Oracle(profile,case).run()],profile+' mutation')
            except ValueError:
                rejected += 1
            else:
                raise ValueError('semantic mutation escaped independent oracle')
    return rejected


def main():
    p = argparse.ArgumentParser()
    for profile in PINNED:
        p.add_argument('--'+profile+'-dir',type=Path,required=True)
    args=p.parse_args();total=0
    for profile in PINNED:
        row=audit(profile,getattr(args,profile+'_dir'));total+=row['native_comparisons']
        print('PROFILE|'+'|'.join(f'{k}={v}' for k,v in row.items()),flush=True)
    print(f'TOTAL|watch_cleanup_comparisons={total}|profiles=3')
    print('FACT|empty_residual_watch_nodes_are_reclaimed_by_original_Loop_within_two_controlled_scans')
    print('FACT|root_Finish_in_Loop_can_leave_earlier_physical_watch_slots_until_next_scan')
    print('FACT|WatchStop_exits_actor_without_immediate_node_delete_then_empty_watch_is_reclaimed_by_Loop')
    print('FACT|root_Stop_does_not_exit_linked_watch_actors_living_watchers_remain_used')
    print('BOUNDARY|original_default_Stop_Finish_CountAlive_Loop_WatchStop_bodies_symbolic_ABI_generic_Exit_Profit_network_stubs_acyclic_five_slot_arrays')
    print('OPEN|full_original_Exit_actual_character_destruction_watch_creation_reuse_concurrency_corrupt_pointers_original_build_JSS_Taiwan_v1_runtime')
    print('RESOLUTION|'+RESOLUTION)


if __name__ == '__main__':
    main()
