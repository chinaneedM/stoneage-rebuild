"""Bounded original world registration beside preserved ordinary enemy births.

Original bodies/headers/data remain transient. Map storage is controlled; actual
linked-list helpers execute. Link reclamation is an explicit collector adapter,
not the old LP64-unsafe freeMemory implementation or full server bootstrap.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import subprocess
import tempfile

from tools.stoneage_enemy_loader_audit import (
    domain as loader_domain, definition, pp_file, specimen, loaded_oracle,
    eligible, birth_expectation, compile_probe, PROFILES,
)
from tools.stoneage_default_template_audit import include_args, digest
from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS, _compact

ROOT=Path(__file__).resolve().parents[1]
PIN_PATH=ROOT/'research/recovered/STONEAGE-OBJECT-OWNERSHIP-SOURCE-DOMAINS-R1.json'
RESOLUTION='BOUNDED_ORIGINAL_OBJECT_REGISTRATION_AND_PRESERVED_ENEMY_NONOWNERSHIP_PASS_ZERO_RUNTIME_PROMOTIONS'
BIRTH_DATA=('CHAR_VITAL','CHAR_STR','CHAR_TOUGH','CHAR_DEX','CHAR_LV','CHAR_ALLOCPOINT',
            'CHAR_HP','CHAR_EXP','CHAR_PETRANK','CHAR_PETID','CHAR_BASEIMAGENUMBER',
            'CHAR_BASEBASEIMAGENUMBER','CHAR_WHICHTYPE')
BIRTH_WORK=('CHAR_WORKTICKETTIME','CHAR_WORKTICKETTIMESTART','CHAR_WORKOBJINDEX',
            'CHAR_WORKMAXHP','CHAR_WORKTACTICS','CHAR_WORK_PETFLG',
            'CHAR_WORKMODCAPTUREDEFAULT','CHAR_WORKFOXROUND')


def domain(profile,root):
    source,prior,data,flags,exps,ride=loader_domain(profile,root)
    accepted=json.loads((PIN_PATH.parent/'STONEAGE-ENEMY-LOADER-SOURCE-DOMAINS-R1.json').read_text())['profiles'][profile]['identity']
    if prior!=accepted:raise ValueError('accepted loader domain drift')
    paths={k:LAYOUTS[profile]/p for k,p in {
        'object':'object.c','map':'map/readmap.c','base':'char/char_base.c',
        'char':'char/char.c','item':'item/item.c'}.items()}
    text={k:pp_file(profile,root,p) for k,p in paths.items()}
    groups={
        'object':['initObjectArray','_initObjectOne','endObjectOne','CHECKOBJECT',
                  'CHECKOBJECTUSE','OBJECT_getType','OBJECT_getIndex','OBJECT_getFloor',
                  'OBJECT_getX','OBJECT_getY','searchObjectFromCharaIndex'],
        'map':['MAP_getfloorIndex','_MAP_getTopObj','MAP_appendTailObj','MAP_addNewObj','MAP_removeObj'],
        'base':['CHAR_getPlayerMaxNum','CHAR_getCharPointer','CHAR_removeHaveItem',
                'CHAR_removeHavePoolItem','CHAR_endCharData',
                '_CHAR_endCharOneArray' if profile=='bismarck' else 'CHAR_endCharOneArray'],
        'char':['CHAR_createCharacter'],'item':['_ITEM_endExistItemsOne'],
    }
    bodies={n:definition(text[k],n) for k,names in groups.items() for n in names}
    # Exact original private declarations; initialization is controlled below.
    declarations=[]
    for key,names in {'object':['obj','objnum'],'map':['MAP_map','MAP_idjumptbl','MAP_idtblsize']}.items():
        for n in names:
            match=re.search(r'(?m)^static[^;\n]*\b'+n+r'\b[^;]*;',text[key])
            if not match:raise ValueError('private declaration drift '+n)
            declarations.append(match[0])
    source+='\n#include "object.h"\n#include "readmap.h"\n#include "map_deal.h"\n'
    source+='\n'.join(declarations)+'\n'
    source+='static int '+('ITEM_sUseItemNum' if profile=='bismarck' else 'ITEM_UseItemnum')+';\n'
    source+='int MAP_appendTailObj(int,int,int,int);\n'
    source+=r'''
static int watch_count,walk_count,reclaim_count;
static MAP_Map controlled_map[1];static MAP_Objlink *controlled_links[4];
static MAP_Objlink *reclaimed[4];
/* Only detached original map nodes are collected. Pool released by memEnd. */
void freeMemory(void *p){
 if(!p || reclaim_count>=4)abort();
 for(int c=0;c<4;c++)for(MAP_Objlink *n=controlled_links[c];n;n=n->next)if(n==p)abort();
 for(int i=0;i<reclaim_count;i++)if(reclaimed[i]==p)abort();
 reclaimed[reclaim_count++]=p;
}
int MAP_walkAble(int index,int floor,int x,int y){
 walk_count++;return floor==1 && x>=0 && x<2 && y>=0 && y<2;
}
void CHAR_sendWatchEvent(int index,int act,int *opt,int len,int mine){
 if(index<0 || index>=2 || act!=CHAR_ACTSTAND || opt || len || !mine)abort();
 watch_count++;
}
'''
    for key in ('map','object','base','item','char'):
        for n in groups[key]:source+=bodies[n]+'\n'
    deps=subprocess.run(['cc','-MM',*include_args(profile,root),'-x','c','-'],input=source,text=True,capture_output=True,check=True).stdout
    headers={}
    for name in deps.replace('\\\n',' ').split()[1:]:
        p=Path(name)
        if p.is_file():headers[p.relative_to(root).as_posix()]=digest(p.read_bytes())
    identity={'source_sha':PINNED[profile],'accepted_loader_identity':prior,
              'files':{str(p):digest((root/p).read_bytes()) for p in paths.values()},
              'functions':{n:digest(_compact(b)) for n,b in bodies.items()},
              'private_declarations_sha256':digest(_compact('\n'.join(declarations))),
              'header_dependency_closure':dict(sorted(headers.items())),
              'object_capacity':2,'controlled_map':'floor1 2x2 actual MAP_Map/MAP_Objlink',
              'adapters':['MAP_walkAble controlled predicate','CHAR_sendWatchEvent collector',
                          'freeMemory detached-map-node collector, no original reclamation'],
              'original_freeMemory_executed':False,'uninitialized_object_fields_observed':False,
              'object_fields_observed':['type','index','floor','x','y'],
              'actual_empty_registry_item_release_guard_executed':True}
    return source,identity,data,flags,exps,ride


class ObjectModel:
    """Independent allocation/list oracle; cursors advance even on map rejection."""
    def __init__(self,capacity=2):
        if capacity<=0:raise ValueError('positive object capacity required')
        self.slots=[[0,0,0,0,0] for _ in range(capacity)]
        self.links=[[] for _ in range(4)];self.cursor=0;self.reclaimed=0

    def add(self,owner,floor=1,x=1,y=1,kind=1):
        cap=len(self.slots)
        for step in range(cap):
            index=(self.cursor+step)%cap
            if self.slots[index][0]:continue
            self.cursor=(index+1)%cap
            if floor!=1 or not 0<=x<2 or not 0<=y<2:return -1
            cell=self.links[2*y+x]
            if index in cell:return -1
            cell.append(index);self.slots[index]=[kind,owner,floor,x,y];return index
        return -1

    def remove(self,index):
        if not 0<=index<len(self.slots):return
        _kind,_owner,floor,x,y=self.slots[index]
        if floor==1 and 0<=x<2 and 0<=y<2:
            cell=self.links[2*y+x]
            if index in cell:cell.remove(index);self.reclaimed+=1
        self.slots[index][0]=0

    def search(self,owner):
        return next((i for i,s in enumerate(self.slots) if s[0]==1 and s[1]==owner),-1)

    def state(self):
        out=[v for s in self.slots for v in s]
        for cell in self.links:
            out.append(len(cell));out+=cell+[-1]*(2-len(cell))
        return out


def cycle_oracle(sequence,cursor=0):
    """Expected complete named state after each independently specified operation."""
    m=ObjectModel();m.cursor=cursor;use=[1,1,1];work=[cursor,1-cursor];watch=2;walk=2;out=[]
    if m.add(0)!=cursor or m.add(1)!=1-cursor:raise ValueError('oracle initial registration')
    def state(stage):out.extend([stage,*use,watch,walk,m.reclaimed,m.search(0),m.search(1),m.search(4),*work,*m.state()])
    state(0)                              # world0/1 owns object0; fresh enemy does not
    if m.add(6)!=-1:raise ValueError('oracle full object allocation')
    state(1)
    use[2]=0;state(2)                     # original Char-only release leaves world objects
    use[2]=1;state(3)                     # accepted creator reuses slot4, still no registration
    use[0]=0;state(4)                     # Char-only world release leaves object0 and link
    work[0]=0;walk+=1;state(5)            # failed constructor copied default work before rollback
    m.remove(cursor);state(6)             # explicit release of world0's object removes map node
    if m.add(0)!=cursor:raise ValueError('oracle object slot reuse')
    work[0]=cursor;use[0]=1;watch+=1;walk+=1;state(7)
    m.remove(cursor);m.remove(1-cursor);use=[0,0,0];state(8)
    # Two births separated by a release; three successful world allocations and
    # one world rollback also consume the original character sequence counter.
    return out,[sequence+2,sequence+3],sequence+6


def native_source(profile,source):
    setup='if(!configmem(64,262144))return 11;' if profile=='gavin' else 'sUnitSize=64;sUnitNumTotal=262144;'
    jump='static int controlled_jump[2]={-1,0};MAP_idjumptbl=controlled_jump;' if profile=='gavin' else 'MAP_idjumptbl[0]=-1;MAP_idjumptbl[1]=0;'
    birth=''.join(f'printf(" %d",ch->data[{n}]);' for n in BIRTH_DATA)+''.join(f'printf(" %d",ch->workint[{n}]);' for n in BIRTH_WORK)
    return source+r'''
static void state(int stage){
 printf(" %d %d %d %d %d %d %d %d %d %d",stage,slots[0].use,slots[1].use,slots[4].use,
 watch_count,walk_count,reclaim_count,searchObjectFromCharaIndex(0),searchObjectFromCharaIndex(1),searchObjectFromCharaIndex(4));
 printf(" %d %d",slots[0].workint[CHAR_WORKOBJINDEX],slots[1].workint[CHAR_WORKOBJINDEX]);
 for(int i=0;i<2;i++)printf(" %d %d %d %d %d",OBJECT_getType(i),OBJECT_getIndex(i),OBJECT_getFloor(i),OBJECT_getX(i),OBJECT_getY(i));
 for(int c=0;c<4;c++){
  int n=0,indices[2]={-1,-1};for(MAP_Objlink *p=controlled_links[c];p;p=p->next){if(n>=2)abort();indices[n++]=p->objindex;}
  printf(" %d %d %d",n,indices[0],indices[1]);
 }
}
static void birth(int result){
 if(result!=4 || rng_count!=14)abort();Char *ch=&slots[result];
 printf(" %d %d %d %d %d",result,rng_count,ch->CharMakeSequenceNumber,
        OBJECT_getIndex(CHAR_getWorkInt(result,CHAR_WORKOBJINDEX)),CHECKOBJECTUSE(0));
'''+birth+r'''
}
int main(int argc,char **argv){
 if(argc!=3 || sizeof(void*)!=8 || sizeof(int)!=4)return 10;
'''+setup+r'''
 if(!memInit())return 12;
 int a=ENEMYTEMP_initEnemy(argv[1]),b=ENEMY_initEnemy(argv[2]);
 if(!a || !b || ENEMYTEMP_enemynum!=1816 || ENEMY_enemynum!=2935)return 13;
 MAP_map=controlled_map;MAP_idtblsize=1;
'''+jump+r'''
 controlled_map[0].id=1;controlled_map[0].xsiz=controlled_map[0].ysiz=2;controlled_map[0].olink=controlled_links;
 int array,level,mode;
 while(scanf("%d%d%d",&array,&level,&mode)==3){
  memset(slots,0,sizeof(slots));memset(controlled_links,0,sizeof(controlled_links));
  initCharCounter[0]=(INITCHARCOUNTER){0,0,2};initCharCounter[1]=(INITCHARCOUNTER){2,2,4};initCharCounter[2]=(INITCHARCOUNTER){4,4,7};
  watch_count=walk_count=reclaim_count=0;
  if(!initObjectArray(2))return 14;
  int c=-1,o=-1;
  if(!CHAR_createCharacter(CHAR_TYPEPLAYER,1,1,1,0,&c,&o,1)||c!=0||o<0||o>1)return 15;
  int world0object=o;
  if(!CHAR_createCharacter(CHAR_TYPEPLAYER,1,1,1,0,&c,&o,1)||c!=1||o!=1-world0object)return 16;
  int world1object=o;
  rng_mode=mode;rng_count=0;int r=ENEMY_createEnemy(array,level);
  printf("C %d %d %d",array,level,mode);birth(r);state(0);
  Object probe={0};probe.type=OBJTYPE_CHARA;probe.index=6;probe.floor=probe.x=probe.y=1;
  if(initObjectOne(&probe)!=-1)return 17;state(1);
  CHAR_endCharOneArray(4);state(2);
  initCharCounter[2].cnt=4;rng_count=0;r=ENEMY_createEnemy(array,level);birth(r);state(3);
  CHAR_endCharOneArray(0);state(4);
  initCharCounter[0].cnt=0;c=o=-1;
  if(CHAR_createCharacter(CHAR_TYPEPLAYER,1,1,1,0,&c,&o,1)||c!=0||o!=-1)return 18;state(5);
  endObjectOne(world0object);state(6);
  initCharCounter[0].cnt=0;c=o=-1;
  if(!CHAR_createCharacter(CHAR_TYPEPLAYER,1,1,1,0,&c,&o,1)||c!=0||o!=world0object)return 19;state(7);
  endObjectOne(world0object);endObjectOne(world1object);CHAR_endCharOneArray(0);CHAR_endCharOneArray(1);CHAR_endCharOneArray(4);state(8);
  printf("\n");
 }
 memEnd();return 0;
}
'''


def verify_output(identity,data,exps,temps,enemies,cases,output):
    lines=output.splitlines()
    if len(lines)!=len(cases):raise ValueError('ownership cardinality mismatch')
    sequence=0
    for case_number,(line,(index,level,mode)) in enumerate(zip(lines,cases)):
        row=line.split()
        if row[0]!='C' or list(map(int,row[1:4]))!=[index,level,mode]:raise ValueError('ownership case ordering')
        values=list(map(int,row[4:]));cursor=case_number%2;want_states,sequences,sequence=cycle_oracle(sequence,cursor)
        # Birth fields are interleaved with stages0..2, then stage3..8.
        width=5+len(BIRTH_DATA)+len(BIRTH_WORK);stagewidth=34
        birth1=values[:width];prefix=values[width:width+3*stagewidth]
        birth2=values[width+3*stagewidth:2*width+3*stagewidth];suffix=values[2*width+3*stagewidth:]
        if prefix+suffix!=want_states:raise ValueError('ownership named state/list/owner mismatch')
        d,w=birth_expectation(identity['accepted_loader_identity'],data,exps,temps[enemies[index][0]],enemies[index],level,mode)
        for birth,seq in zip((birth1,birth2),sequences):
            want=[4,14,seq,cursor,1]+[d[n] for n in BIRTH_DATA]+[w[n] for n in BIRTH_WORK]
            if birth!=want:raise ValueError('ownership birth fields/sequence mismatch')
    return len(lines)


def mutations(profile,root,source,identity,data,exps,temps,enemies,case,paths,tmp):
    constructor=definition(source,'CHAR_createCharacter')
    changed,n=re.subn(r'CHAR_setWorkInt\s*\([^;]+CHAR_WORKOBJINDEX[^;]+;', '',constructor)
    if n!=1:raise ValueError('world work write drift')
    allocator=definition(source,'_initObjectOne')
    copier=re.search(r'memcpy\s*\(\s*&obj\[i\]\s*,\s*ob\s*,\s*sizeof\(\s*Object\s*\)\s*\)\s*;',allocator)
    if not copier:raise ValueError('object copy drift')
    map_remove=definition(source,'MAP_removeObj')
    no_map,n=re.subn(r'freeMemory\(\s*c\s*\)\s*;', '',map_remove)
    if n!=1:raise ValueError('map node reclamation drift')
    search=definition(source,'searchObjectFromCharaIndex')
    wrong_search,n=re.subn(r'return\s+i\s*;', 'return -1;',search)
    if n!=1:raise ValueError('owner search drift')
    creator=definition(source,'ENEMY_createEnemy');last=re.search(r'return\s+(\w+)\s*;\s*}$',creator)
    if not last:raise ValueError('enemy creator final return drift')
    enemy_owned=creator[:last.start()]+f'CHAR_setWorkInt({last[1]},CHAR_WORKOBJINDEX,1);'+creator[last.start():]
    trials=[('world-work',source.replace(constructor,changed,1)),
            ('object-owner',source.replace(allocator,allocator[:copier.end()]+'obj[i].index=6;'+allocator[copier.end():],1)),
            ('map-reclaim',source.replace(map_remove,no_map,1)),
            ('owner-search',source.replace(search,wrong_search,1)),
            ('enemy-object-work',source.replace(creator,enemy_owned,1))]
    payload=' '.join(map(str,case))+'\n'
    for name,mutant in trials:
        exe=tmp/'mutant';compile_probe(profile,root,native_source(profile,mutant),exe,'-O0')
        r=subprocess.run([str(exe),*map(str,paths)],input=payload,text=True,capture_output=True)
        if r.returncode or r.stderr:raise ValueError('unsafe ownership mutation '+name+': '+r.stderr+' rc='+str(r.returncode))
        try:verify_output(identity,data,exps,temps,enemies,[case],r.stdout)
        except ValueError as error:
            if 'ownership named state' not in str(error) and 'ownership birth fields' not in str(error):raise
        else:raise ValueError('undetected ownership mutation '+name)
    return len(trials)


def audit(profile,root,paths):
    if subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()!=PINNED[profile] or subprocess.check_output(['git','-C',str(root),'status','--porcelain'],text=True):raise ValueError('source pin/cleanliness drift')
    source,identity,data,flags,exps,ride=domain(profile,root)
    if identity!=json.loads(PIN_PATH.read_text())['profiles'][profile]:raise ValueError('ownership identity drift')
    loader=identity['accepted_loader_identity'];temps,enemies=loaded_oracle(profile,loader,*[p.read_bytes() for p in paths],32,32)
    cases=[(i,l,m) for i in eligible(loader,temps,enemies,ride) for l in (1,20) for m in range(4)]
    payload=''.join(' '.join(map(str,c))+'\n' for c in cases);reference=None;total=0
    with tempfile.TemporaryDirectory(prefix='stoneage-ownership-') as tmp:
        tmp=Path(tmp)
        for opt in ('-O0','-O2'):
            exe=tmp/('probe'+opt);compile_probe(profile,root,native_source(profile,source),exe,opt)
            r=subprocess.run([str(exe),*map(str,paths)],input=payload,text=True,capture_output=True)
            if r.returncode or r.stderr:raise ValueError(r.stderr+' rc='+str(r.returncode))
            total+=verify_output(identity,data,exps,temps,enemies,cases,r.stdout)
            if reference is not None and r.stdout!=reference:raise ValueError('optimization-dependent ownership state')
            reference=r.stdout
        rejected=mutations(profile,root,source,identity,data,exps,temps,enemies,cases[0],paths,tmp)
    return {'profile':profile,'source_sha':PINNED[profile],'registration_cycles':total,
            'preserved_enemy_births':2*total,'successful_world_constructors':3*total,
            'full_object_constructor_rollbacks':total,'named_stage_comparisons':9*total,
            'mutations_rejected':rejected,'semantic_sha256':digest(reference)}


def main():
    parser=argparse.ArgumentParser()
    for p in PINNED:parser.add_argument('--'+p+'-dir',type=Path,required=True)
    args=parser.parse_args();roots={p:getattr(args,p+'_dir') for p in PINNED}
    pins=json.loads(PIN_PATH.read_text());paths,receipt=specimen(roots['gavin'])
    if receipt!=pins['preserved_specimen']:raise ValueError('ownership input specimen drift')
    totals=[0]*5
    for p in PROFILES:
        row=audit(p,roots[p],paths)
        totals=[a+row[k] for a,k in zip(totals,('registration_cycles','preserved_enemy_births','successful_world_constructors','full_object_constructor_rollbacks','named_stage_comparisons'))]
        print('PROFILE|'+'|'.join(f'{k}={v}' for k,v in row.items()),flush=True)
    print('TOTAL|'+'|'.join(f'{k}={v}' for k,v in zip(('registration_cycles','preserved_enemy_births','successful_world_constructors','full_object_constructor_rollbacks','named_stage_comparisons'),totals))+'|executed_profiles=2')
    print('MUTATIONS|semantic_mutations_rejected=10|world_work_object_owner_map_reclaim_owner_search_enemy_object_work|additional_cycles=10')
    print('FACT|actual_world_constructor_object_allocator_original_headers_pool_map_link_helpers_and_empty_registry_character_release_execute')
    print('FACT|object0_is_live_world_player0_or1_owned_loaded_enemy_work0_does_not_establish_ownership_owner_search_is_minus1')
    print('FACT|Char_only_release_retains_world_object_and_map_link_explicit_object_release_unlinks_reuse_appends_tail')
    print('BOUNDARY|controlled_positive_partitions_floor1_2x2_map_walk_watch_collectors_and_detached_node_reclamation_adapter_no_original_freeMemory')
    print('OPEN|actual_battle_entry_full_Exit_to_reuse_original_reclamation_bootstrap_Iris_encoding_original_ABI_JSS_Taiwan_v1')
    print('RESOLUTION|'+RESOLUTION)


if __name__=='__main__':main()
