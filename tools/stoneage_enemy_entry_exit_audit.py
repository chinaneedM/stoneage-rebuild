"""Actual-header preserved enemy birth -> original Entry/Exit -> slot reuse.

Only ordinary unequipped nonparty enemies execute Exit. Complete original bodies
remain transient; excluded actor/network/warp/profession paths abort if reached.
"""
from __future__ import annotations
import argparse
import filecmp
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile

from tools.stoneage_object_ownership_audit import domain as ownership_domain, BIRTH_DATA, BIRTH_WORK
from tools.stoneage_enemy_loader_audit import pp_file, specimen, loaded_oracle, eligible, birth_expectation, PROFILES
from tools.stoneage_enemy_creation_audit import definition, trap_definitions
from tools.stoneage_default_template_audit import include_args, preprocess, digest, block, top_entries, expression, enums
from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS, _compact

ROOT=Path(__file__).resolve().parents[1]
PIN_PATH=ROOT/'research/recovered/STONEAGE-ENEMY-ENTRY-EXIT-SOURCE-DOMAINS-R1.json'
RESOLUTION='BOUNDED_ACTUAL_HEADER_PRESERVED_ENEMY_ENTRY_EXIT_REUSE_PASS_ZERO_RUNTIME_PROMOTIONS'


def domain(profile,root):
    source,prior,data,flags,exps,ride=ownership_domain(profile,root)
    accepted=json.loads((PIN_PATH.parent/'STONEAGE-OBJECT-OWNERSHIP-SOURCE-DOMAINS-R1.json').read_text())['profiles'][profile]
    if prior!=accepted:raise ValueError('accepted ownership domain drift')
    paths={k:LAYOUTS[profile]/p for k,p in {
        'battle':'battle/battle.c','tables':'battle/battle_event.c',
        'base':'char/char_base.c','char':'char/char.c'}.items()}
    texts={k:pp_file(profile,root,p) for k,p in paths.items()}
    groups={'base':['_CHAR_setFlg','_CHAR_CHECKPETINDEX','CHAR_getCharPet'],
            'char':['CHAR_PartyUpdate'],
            'battle':['EntryInit','BATTLE_BadStatusAllClr','BATTLE_NewEntry','_BATTLE_Exit']}
    if profile=='gavin':groups['battle'].insert(2,'BATTLE_ProfessionStatus_init')
    else:groups['battle'].insert(0,'BATTLE_CHECKINDEX')
    bodies={n:definition(texts[k],n) for k,ns in groups.items() for n in ns}
    tables={n:block(texts['tables'],'int '+n) for n in ('StatusTbl','MagicTbl')}
    headers=['battle_event.h','battle_command.h','net.h','skill.h']
    if profile=='gavin':headers.append('lssproto_serv.h')
    else:headers.append('gmsv_server.h')
    source+='\n#include <time.h>\n'+''.join('#include "'+h+'"\n' for h in headers)
    source+='static BATTLE controlled_battle[1];BATTLE *BattleArray=controlled_battle;int BATTLE_battlenum=1;\n'
    source+=tables['StatusTbl']+'\n'+tables['MagicTbl']+'\n'
    source+='static int clock_count;static time_t audit_time(time_t *out){clock_count++;if(out)*out=1000;return 1000;}\n#define time audit_time\n'
    for k in ('base','char','battle'):
        for n in groups[k]:source+=bodies[n]+'\n'
    source+='#undef time\n'
    expanded=preprocess(profile,root,source);ev=enums(expanded)
    for body in re.findall(r'\benum(?:\s+\w+)?\s*\{([^{}]+)\}',expanded):
        if not any(n in body for n in ('BATTLE_ST_END','MAXSTATUSTYPE','BATTLE_ERR_NONE','BATTLE_CHARMODE_INIT','BATTLE_S_TYPE_ENEMY')):continue
        value=-1
        for entry in body.split(','):
            pair=entry.strip().split('=',1);name=pair[0].strip()
            value=expression(pair[1],ev) if len(pair)==2 else value+1;ev[name]=value
    # Macro constants are observed by the same original preprocessor, not assumed.
    probe=preprocess(profile,root,source+'\nint observed_entry_max=BATTLE_ENTRY_MAX;int observed_item_max=GETITEM_MAX;int observed_side_offset=SIDE_OFFSET;int observed_status_end=BATTLE_ST_END;int observed_magic_end=MAXSTATUSTYPE;')
    limits={n:expression(re.search(r'int observed_'+n+r'\s*=\s*([^;]+);',probe)[1],ev)
            for n in ('entry_max','item_max','side_offset','status_end','magic_end')}
    limits['flag_bytes']=(ev['CHAR_FLGNUM']+7)//8
    if limits['entry_max']!=10 or limits['side_offset']!=10:raise ValueError('entry cardinality domain drift')
    indexes={}
    for n in tables:
        match=re.search(r'(?m)^int '+n+r'\s*\[[^]]*\]\s*=\s*\{',expanded)
        if not match:raise ValueError('missing actual table initializer '+n)
        indexes[n]=[expression(v,ev) for v in top_entries(block(expanded[match.start():],'int '+n))]
    deps=subprocess.run(['cc','-MM',*include_args(profile,root),'-x','c','-'],input=source,text=True,capture_output=True,check=True).stdout
    closure={}
    for n in deps.replace('\\\n',' ').split()[1:]:
        p=Path(n)
        if p.is_file():closure[p.relative_to(root).as_posix()]=digest(p.read_bytes())
    identity={'source_sha':PINNED[profile],'accepted_ownership_identity':prior,
              'files':{str(p):digest((root/p).read_bytes()) for p in paths.values()},
              'functions':{n:digest(_compact(b)) for n,b in bodies.items()},
              'tables':{n:digest(_compact(b)) for n,b in tables.items()},
              'table_work_indexes':indexes,'limits':limits,
              'enum_values':{n:v for n,v in ev.items() if n.startswith(('CHAR_','BATTLE_'))},
              'header_dependency_closure':dict(sorted(closure.items())),
              'battle_entry_field':'char_index' if profile=='bismarck' else 'charaindex',
              'adapters':['fixed time1000 collector','inherited walk/watch/detached-node collection'],
              'matched_actor_scope':'ordinary preserved unequipped nonparty enemy only'}
    return source,identity,data,flags,exps,ride


def compile_probe(profile,root,source,exe,opt,traps=None):
    """Discover unresolved symbols once, then pin the unreachable trap closure."""
    prior=json.loads((PIN_PATH.parent/'STONEAGE-ENEMY-CREATION-SOURCE-DOMAINS-R1.json').read_text())['profiles'][profile]['unreachable_traps']
    remaining=[]
    for name in prior:
        try:definition(source,name)
        except ValueError:remaining.append(name)
    source+=trap_definitions(profile,root,source,remaining)
    args=['cc','-std=gnu99','-fgnu89-inline',opt,'-fsanitize=undefined','-fno-sanitize-recover=all',*include_args(profile,root),'-x','c','-','-o',str(exe)]
    if traps is None:
        r=subprocess.run(args,input=source,text=True,capture_output=True)
        if r.returncode:
            traps=sorted(set(re.findall(r'undefined reference to [`\u2018]([^\u2019\'`]+)',r.stderr)))
            if not traps:raise ValueError(r.stderr[-15000:])
        else:traps=[]
    source+=trap_definitions(profile,root,source,traps)
    r=subprocess.run(args,input=source,text=True,capture_output=True)
    if r.returncode:raise ValueError(r.stderr[-15000:])
    return traps


def native_source(profile,source,identity):
    setup='if(!configmem(64,262144))return 11;' if profile=='gavin' else 'sUnitSize=64;sUnitNumTotal=262144;'
    jump='static int controlled_jump[2]={-1,0};MAP_idjumptbl=controlled_jump;' if profile=='gavin' else 'MAP_idjumptbl[0]=-1;MAP_idjumptbl[1]=0;'
    field='char_index' if profile=='bismarck' else 'charaindex'
    birth=''.join(f'printf(" %d",ch->data[{n}]);' for n in BIRTH_DATA)+''.join(f'printf(" %d",ch->workint[{n}]);' for n in BIRTH_WORK)
    seed=','.join(map(str,seed_targets(profile,identity)))
    return (source+r'''
static Char worlds[2],before_char;static int before_work[CHAR_WORKDATAINTNUM];static BATTLE battle_before;
static void guards(int actor,int side){
 Char saved=slots[actor];BATTLE saved_battle=controlled_battle[0];
 printf(" %d %d %d",BATTLE_NewEntry(actor,0,2),BATTLE_NewEntry(actor,-1,side),BATTLE_NewEntry(-1,0,side));
 controlled_battle[0].use=0;printf(" %d",BATTLE_NewEntry(actor,0,side));controlled_battle[0]=saved_battle;
 controlled_battle[0].Side[side].type=BATTLE_S_TYPE_PLAYER;printf(" %d",BATTLE_NewEntry(actor,0,side));controlled_battle[0]=saved_battle;
 for(int i=0;i<BATTLE_ENTRY_MAX;i++)controlled_battle[0].Side[side].Entry[i].ENTRY_FIELD=200+i;
 printf(" %d",BATTLE_NewEntry(actor,0,side));controlled_battle[0]=saved_battle;
 printf(" %d",!memcmp(&saved,&slots[actor],sizeof(saved))&&!memcmp(&saved_battle,&controlled_battle[0],sizeof(saved_battle)));
}
static void sparse(const int *work,const int *base){
 int n=0;for(int j=0;j<CHAR_WORKDATAINTNUM;j++)if(work[j]!=(base?base[j]:0))n++;
 printf(" %d",n);for(int j=0;j<CHAR_WORKDATAINTNUM;j++)if(work[j]!=(base?base[j]:0))printf(" %d %d",j,work[j]);
}
static void birth(int result){
 if(result<4 || result>=7)abort();Char *ch=&slots[result];
 printf(" %d %d %d",result,rng_count,ch->CharMakeSequenceNumber);
'''+birth+r'''
 sparse(ch->workint,NULL);for(int j=0;j<sizeof(ch->flg);j++)printf(" %u",(unsigned char)ch->flg[j]);
}
static void state(int actor,int side,int pos){
 Char *ch=&slots[actor];BATTLE_ENTRY *entry=&BattleArray[0].Side[side].Entry[pos];
 BATTLE compare=controlled_battle[0];compare.Side[side].Entry[pos]=battle_before.Side[side].Entry[pos];
 int same=!memcmp(&compare,&battle_before,sizeof(compare));
 int world_same=!memcmp(&worlds[0],&slots[0],sizeof(Char))&&!memcmp(&worlds[1],&slots[1],sizeof(Char));
 int map_same=controlled_links[0]==NULL&&controlled_links[1]==NULL&&controlled_links[2]==NULL;
 MAP_Objlink *link=controlled_links[3];map_same=map_same&&link&&link->objindex==0&&link->next&&link->next->objindex==1&&!link->next->next;
 int cleared=1;for(int j=0;j<CHAR_MAXITEMHAVE;j++)if(ch->indexOfExistItems[j]!=-1)cleared=0;
 for(int j=0;j<CHAR_MAXPOOLITEMHAVE;j++)if(ch->indexOfExistPoolItems[j]!=-1)cleared=0;
 printf(" %d %d %d %d %d %d %d %d %d",ch->use,same,world_same,map_same,cleared,clock_count,searchObjectFromCharaIndex(actor),watch_count,reclaim_count);
 printf(" %d %d",!memcmp(ch->data,before_char.data,sizeof(ch->data)),!memcmp(ch->string,before_char.string,sizeof(ch->string)));
 for(int i=0;i<2;i++)printf(" %d %d %d %d %d",OBJECT_getType(i),OBJECT_getIndex(i),OBJECT_getFloor(i),OBJECT_getX(i),OBJECT_getY(i));
 printf(" %d %d %d",entry->'''+field+r''',entry->bid,entry->escape);
 for(int j=0;j<GETITEM_MAX;j++)printf(" %d",entry->getitem[j]);
 sparse(ch->workint,before_work);
 for(int j=0;j<sizeof(ch->flg);j++)printf(" %u",(unsigned char)ch->flg[j]);
}
int main(int argc,char **argv){
 if(argc!=3||sizeof(void*)!=8||sizeof(int)!=4)return 10;
'''+setup+r'''
 if(!memInit())return 12;
 if(!ENEMYTEMP_initEnemy(argv[1])||!ENEMY_initEnemy(argv[2]))return 13;
 MAP_map=controlled_map;MAP_idtblsize=1;
'''+jump+r'''
 controlled_map[0].id=1;controlled_map[0].xsiz=controlled_map[0].ysiz=2;controlled_map[0].olink=controlled_links;
 initCharCounter[0]=(INITCHARCOUNTER){0,0,2};initCharCounter[1]=(INITCHARCOUNTER){2,2,4};initCharCounter[2]=(INITCHARCOUNTER){4,4,7};
 if(!initObjectArray(2))return 14;
 for(int i=0;i<2;i++){int c,o;if(!CHAR_createCharacter(CHAR_TYPEPLAYER,1,1,1,0,&c,&o,1)||c!=i||o!=i)return 15;worlds[i]=slots[i];}
 int array,level,mode,side,pos,dirty;
 while(scanf("%d%d%d%d%d%d",&array,&level,&mode,&side,&pos,&dirty)==6){
  memset(controlled_battle,0,sizeof(controlled_battle));controlled_battle[0].use=1;controlled_battle[0].type=BATTLE_TYPE_P_vs_E;
  for(int s=0;s<2;s++){
   controlled_battle[0].Side[s].type=BATTLE_S_TYPE_ENEMY;
   for(int i=0;i<BATTLE_ENTRY_MAX;i++){
    BATTLE_ENTRY *e=&controlled_battle[0].Side[s].Entry[i];e->'''+field+r'''=100+s*10+i;e->bid=-9;e->escape=7;
    for(int j=0;j<GETITEM_MAX;j++)e->getitem[j]=900+j;
   }
  }
  for(int i=pos;i<BATTLE_ENTRY_MAX;i++)controlled_battle[0].Side[side].Entry[i].'''+field+r'''=-1;
  battle_before=controlled_battle[0];clock_count=0;
  printf("C %d %d %d %d %d %d",array,level,mode,side,pos,dirty);
  for(int repeat=0;repeat<2;repeat++){
   initCharCounter[2].cnt=4;rng_mode=mode;rng_count=0;int actor=ENEMY_createEnemy(array,level);birth(actor);
   before_char=slots[actor];if(dirty){int seeded[]={SEED_INDEXES};for(int j=0;j<sizeof(seeded)/sizeof(seeded[0]);j++)slots[actor].workint[seeded[j]]=777;
    CHAR_setFlg(actor,CHAR_ISATTACKED,0);CHAR_setFlg(actor,CHAR_ISDIE,1);}
   guards(actor,side);memcpy(before_work,slots[actor].workint,sizeof(before_work));
   int entered=BATTLE_NewEntry(actor,0,side);printf(" %d",entered);state(actor,side,pos);
   int exited=BATTLE_Exit(actor,0);printf(" %d",exited);state(actor,side,pos);
   printf(" %d %d",BATTLE_Exit(actor,0),BATTLE_NewEntry(actor,0,side));
  }
  printf("\n");
 }
 endObjectOne(0);endObjectOne(1);CHAR_endCharOneArray(0);CHAR_endCharOneArray(1);memEnd();return 0;
}
''').replace('ENTRY_FIELD',field).replace('SEED_INDEXES',seed)


def entry_changes(profile,identity,before,side,exited=False):
    """Independent complete work-delta oracle over the captured accepted birth."""
    ev=identity['enum_values'];after=before.copy()
    values={'CHAR_WORKBATTLEINDEX':0,'CHAR_WORKBATTLEMODE':ev['BATTLE_CHARMODE_INIT'],
            'CHAR_WORKBATTLESIDE':side,'CHAR_WORKBATTLECOM1':-1,
            'CHAR_WORKBATTLECOM2':-1,'CHAR_WORKBATTLECOM3':-1,'CHAR_WORKFOXROUND':-1}
    zeros=['CHAR_WORKBATTLEFLG','CHAR_WORKMODATTACK','CHAR_WORKMODDEFENCE','CHAR_WORKMODQUICK',
           'CHAR_WORKDAMAGEABSROB','CHAR_WORKDAMAGEREFLEC','CHAR_WORKDAMAGEVANISH',
           'CHAR_WORKMODCAPTURE','CHAR_OTHERSTATUSNUMS','CHAR_MYSKILLDUCK','CHAR_MYSKILLDUCKPOWER',
           'CHAR_MYSKILLSTR','CHAR_MYSKILLSTRPOWER','CHAR_MYSKILLTGH','CHAR_MYSKILLTGHPOWER',
           'CHAR_MYSKILLDEX','CHAR_MYSKILLDEXPOWER','CHAR_MAGICPETMP','CHAR_WORKBATTLEWATCH',
           'CHAR_WORKRETRACE']
    if profile=='gavin':zeros+=['CHAR_WORKTRAP','CHAR_WORKACUPUNCTURE','CHAR_WORKFIXEARTHAT_BOUNDARY',
        'CHAR_WORKFIXWATERAT_BOUNDARY','CHAR_WORKFIXFIREAT_BOUNDARY','CHAR_WORKFIXWINDAT_BOUNDARY',
        'CHAR_DOOMTIME','CHAR_WORK_com1','CHAR_WORK_toNo','CHAR_WORK_mode','CHAR_WORK_skill_level',
        'CHAR_WORK_array','CHAR_MYSKILLHIT','CHAR_WORK_P_DUCK','CHAR_WORKMOD_P_DUCK','CHAR_WORK_WEAPON']
    else:zeros.append('CHAR_WORKDBATTLEESCAPE')
    values.update({n:0 for n in zeros})
    for n,v in values.items():after[ev[n]]=v
    for n,limit in (('StatusTbl','status_end'),('MagicTbl','magic_end')):
        indexes=identity['table_work_indexes'][n]
        if len(indexes)!=identity['limits'][limit]:raise ValueError('status table coverage drift')
        for index in indexes[1:]:after[index]=0
    for j in range(3):after[ev['CHAR_WORKIMPRECATENUM1']+j]=0
    if profile=='gavin':
        for j in range(3):after[ev['CHAR_WORK_F_RESIST']+j]=0
    if exited:after[ev['CHAR_WORKBATTLEMODE']]=ev['BATTLE_CHARMODE_FINAL'];after[ev['CHAR_WORKBATTLEINDEX']]=-1
    return {k:v for k,v in sorted(after.items()) if v!=before.get(k,0)}


def seed_targets(profile,identity):
    count=identity['enum_values']['CHAR_WORKDATAINTNUM']
    changes=entry_changes(profile,identity,{i:777 for i in range(count)},0)
    return [i for i,v in changes.items() if v==0]


class RowReader:
    def __init__(self,line):
        tokens=line.split()
        if not tokens or tokens[0]!='C':raise ValueError('entry/exit row tag')
        self.tokens=list(map(int,tokens[1:]));self.at=0
    def take(self,n):
        out=self.tokens[self.at:self.at+n];self.at+=n
        if len(out)!=n:raise ValueError('entry/exit truncated row')
        return out
    def sparse(self,limit):
        n=self.take(1)[0]
        if not 0<=n<=limit:raise ValueError('entry/exit sparse cardinality')
        pairs=self.take(2*n);keys=pairs[::2]
        if keys!=sorted(set(keys)) or any(not 0<=k<limit for k in keys):raise ValueError('entry/exit sparse key domain')
        return dict(zip(keys,pairs[1::2]))
    def done(self):
        if self.at!=len(self.tokens):raise ValueError('entry/exit extra row values')


def verify_line(profile,identity,data,flags,exps,temps,enemies,case,line,case_number=0):
    rd=RowReader(line);index,level,mode,side,pos,dirty=case
    if rd.take(6)!=list(case):raise ValueError('entry/exit case order')
    loader=identity['accepted_ownership_identity']['accepted_loader_identity'];ev=identity['enum_values'];lim=identity['limits']
    d,w=birth_expectation(loader,data,exps,temps[enemies[index][0]],enemies[index],level,mode)
    first_birth=None
    for repeat in range(2):
        control=rd.take(3)
        if control!=[4,14,2+2*case_number+repeat]:raise ValueError('entry/exit birth control/slot reuse')
        if rd.take(len(BIRTH_DATA)+len(BIRTH_WORK))!=[d[n] for n in BIRTH_DATA]+[w[n] for n in BIRTH_WORK]:raise ValueError('entry/exit named birth fields')
        before=rd.sparse(ev['CHAR_WORKDATAINTNUM']);birth_flags=rd.take(lim['flag_bytes'])
        if birth_flags!=flags+[0]*(lim['flag_bytes']-len(flags)):raise ValueError('entry/exit birth flags')
        for n,v in w.items():
            if before.get(ev[n],0)!=v:raise ValueError('entry/exit sparse birth consistency')
        if repeat and (before,birth_flags)!=first_birth:raise ValueError('entry/exit recreated birth work/flags differ')
        first_birth=(before,birth_flags)
        if dirty:
            before=before.copy();before.update({k:777 for k in seed_targets(profile,identity)})
            birth_flags=birth_flags.copy();birth_flags[ev['CHAR_ISATTACKED']//8]&=255^(1<<(ev['CHAR_ISATTACKED']%8))
            birth_flags[ev['CHAR_ISDIE']//8]|=1<<(ev['CHAR_ISDIE']%8)
        inactive=ev['BATTLE_ERR_BATTLEINDEX'] if profile=='bismarck' else ev['BATTLE_ERR_NOUSE']
        wanted_guards=[ev['BATTLE_ERR_PARAM'],ev['BATTLE_ERR_BATTLEINDEX'],ev['BATTLE_ERR_CHARAINDEX'],inactive,ev['BATTLE_ERR_TYPE'],ev['BATTLE_ERR_ENTRYMAX'],1]
        if rd.take(7)!=wanted_guards:raise ValueError('entry/exit guard/no-change mismatch')
        changed_flags=birth_flags.copy();changed_flags[ev['CHAR_ISATTACKED']//8]|=1<<(ev['CHAR_ISATTACKED']%8)
        changed_flags[ev['CHAR_ISDIE']//8]&=255^(1<<(ev['CHAR_ISDIE']%8))
        for exited in (False,True):
            if rd.take(1)!=[ev['BATTLE_ERR_NONE']]:raise ValueError('entry/exit result mismatch')
            clock=(repeat+int(exited)) if profile=='gavin' else 0
            expected=[int(not exited),1,1,1,1,clock,-1,2,0,1,1]
            expected+=[1,0,1,1,1,1,1,1,1,1]
            expected+=[-1 if exited else 4,pos+side*lim['side_offset'],0]+[-1]*lim['item_max']
            if rd.take(len(expected))!=expected:raise ValueError('entry/exit lifecycle/entry/world/clock mismatch')
            if rd.sparse(ev['CHAR_WORKDATAINTNUM'])!=entry_changes(profile,identity,before,side,exited):raise ValueError('entry/exit complete work delta mismatch')
            if rd.take(lim['flag_bytes'])!=changed_flags:raise ValueError('entry/exit flags mismatch')
        if rd.take(2)!=[ev['BATTLE_ERR_CHARAINDEX']]*2:raise ValueError('entry/exit destroyed-slot guards')
    rd.done()
    return 1


def cases_for(selected):
    natural=[(i,l,m,0,0,0) for i in selected for l in (1,20) for m in range(4)]
    natural=[(*c[:3],(n//10)%2,n%10,0) for n,c in enumerate(natural)]
    return natural+[(selected[0],20,1,s,p,1) for s in (0,1) for p in range(10)]


def mutations(profile,root,source,identity,data,flags,exps,temps,enemies,case,paths,tmp,traps):
    enter=definition(source,'BATTLE_NewEntry');exit_body=definition(source,'_BATTLE_Exit')
    end=definition(source,'CHAR_endCharData');clear=definition(source,'BATTLE_BadStatusAllClr')
    bid,n=re.subn(r'(pEntry\[i\]\.bid\s*=\s*[^;]+);',r'\1 + 1;',enter)
    if n!=1:raise ValueError('entry bid statement drift')
    ret=re.search(r'return\s+0\s*;\s*}$',enter)
    if not ret:raise ValueError('entry return drift')
    actor='char_index' if profile=='bismarck' else 'charaindex'
    own=enter[:ret.start()]+f'CHAR_setWorkInt({actor},CHAR_WORKOBJINDEX,1);'+enter[ret.start():]
    status,n=re.subn(r'i\s*<\s*BATTLE_ST_END','i < 1',clear)
    if n!=1:raise ValueError('status loop drift')
    final,n=re.subn(r'(CHAR_WORKBATTLEMODE\s*,\s*)BATTLE_CHARMODE_FINAL',r'\1(BATTLE_CHARMODE_FINAL+1)',exit_body)
    if n!=1:raise ValueError('Exit final mode drift')
    field=identity['battle_entry_field']
    retained,n=re.subn(r'(pEntry\[i\]\.'+field+r'\s*=\s*)-1\s*;',r'\g<1>'+actor+';',exit_body)
    if n!=1:raise ValueError('Exit entry removal drift')
    live,n=re.subn(r'ch->use\s*=\s*0\s*;', 'ch->use=1;',end)
    if n!=1:raise ValueError('character invalidation drift')
    trials=[('entry-bid',source.replace(enter,bid,1)),('entry-object',source.replace(enter,own,1)),
            ('status-clear',source.replace(clear,status,1)),('Exit-mode',source.replace(exit_body,final,1)),
            ('Exit-entry-removal',source.replace(exit_body,retained,1)),('slot-invalidation',source.replace(end,live,1))]
    payload=' '.join(map(str,case))+'\n'
    for name,mutant in trials:
        exe=tmp/'mutant';compile_probe(profile,root,native_source(profile,mutant,identity),exe,'-O0',traps)
        r=subprocess.run([str(exe),*map(str,paths)],input=payload,text=True,capture_output=True)
        if r.returncode or r.stderr:raise ValueError('unsafe entry/exit mutation '+name+': '+r.stderr+' rc='+str(r.returncode))
        try:verify_line(profile,identity,data,flags,exps,temps,enemies,case,r.stdout.strip())
        except ValueError as error:
            if not str(error).startswith('entry/exit '):raise
        else:raise ValueError('undetected entry/exit mutation '+name)
    return len(trials)


def audit(profile,root,paths):
    pins=json.loads(PIN_PATH.read_text());source,identity,data,flags,exps,ride=domain(profile,root)
    if identity!=pins['profiles'][profile]['identity']:raise ValueError('entry/exit source domain drift')
    loader=identity['accepted_ownership_identity']['accepted_loader_identity']
    temps,enemies=loaded_oracle(profile,loader,*[p.read_bytes() for p in paths],32,32)
    selected=eligible(loader,temps,enemies,ride);cases=cases_for(selected);payload=''.join(' '.join(map(str,c))+'\n' for c in cases)
    streams=[]
    with tempfile.TemporaryDirectory(prefix='stoneage-entry-exit-') as directory:
        tmp=Path(directory)
        for opt in ('-O0','-O2'):
            exe=tmp/('probe'+opt);compile_probe(profile,root,native_source(profile,source,identity),exe,opt,pins['profiles'][profile]['unreachable_traps'])
            out=tmp/('output'+opt+'.txt')
            with out.open('w') as stream:
                r=subprocess.run([str(exe),*map(str,paths)],input=payload,text=True,stdout=stream,stderr=subprocess.PIPE)
            if r.returncode or r.stderr:raise ValueError(r.stderr+' rc='+str(r.returncode))
            with out.open() as stream:
                for n,case in enumerate(cases):
                    line=stream.readline()
                    if not line:raise ValueError('entry/exit missing cycle')
                    verify_line(profile,identity,data,flags,exps,temps,enemies,case,line,n)
                if stream.readline():raise ValueError('entry/exit extra cycles')
            streams.append(out)
        if not filecmp.cmp(*streams,shallow=False):raise ValueError('entry/exit optimization divergence')
        sha=hashlib.sha256()
        with streams[0].open('rb') as stream:
            while chunk:=stream.read(1048576):sha.update(chunk)
        rejected=mutations(profile,root,source,identity,data,flags,exps,temps,enemies,cases[-1],paths,tmp,pins['profiles'][profile]['unreachable_traps'])
    total=len(cases)*2
    return {'profile':profile,'source_sha':PINNED[profile],'natural_cycles':len(cases[:-20])*2,
            'dirty_status_cycles':40,'entry_exit_reuse_cycles':total,'preserved_enemy_births':total*2,
            'full_work_delta_and_stage_comparisons':total*4,'rejected_guard_calls':total*16,
            'mutations_rejected':rejected,'semantic_sha256':sha.hexdigest()}


def main():
    parser=argparse.ArgumentParser()
    for p in PINNED:parser.add_argument('--'+p+'-dir',type=Path,required=True)
    args=parser.parse_args();roots={p:getattr(args,p+'_dir') for p in PINNED}
    for p,r in roots.items():
        if subprocess.check_output(['git','-C',str(r),'rev-parse','HEAD'],text=True).strip()!=PINNED[p] or subprocess.check_output(['git','-C',str(r),'status','--porcelain'],text=True):raise ValueError('source pin/cleanliness drift '+p)
    paths,receipt=specimen(roots['gavin']);pins=json.loads(PIN_PATH.read_text())
    if receipt!=pins['preserved_specimen']:raise ValueError('entry/exit specimen drift')
    totals={k:0 for k in ('natural_cycles','dirty_status_cycles','entry_exit_reuse_cycles','preserved_enemy_births','full_work_delta_and_stage_comparisons','rejected_guard_calls')}
    for p in PROFILES:
        row=audit(p,roots[p],paths)
        for k in totals:totals[k]+=row[k]
        print('PROFILE|'+'|'.join(f'{k}={v}' for k,v in row.items()),flush=True)
    print('TOTAL|'+'|'.join(f'{k}={v}' for k,v in totals.items())+'|executed_profiles=2')
    print('MUTATIONS|semantic_mutations_rejected=12|entry_bid_object_status_clear_Exit_mode_entry_removal_slot_invalidation|additional_cycles=12')
    print('FACT|actual_BATTLE_NewEntry_complete_Exit_bad_status_tables_checked_accessors_empty_registry_destruction_and_preserved_birth_reuse_execute')
    print('FACT|entry_INIT_is1_Exit_FINAL_is6_removes_entry_invalidates_enemy_slot_rebirth_restores_work_flags_world_objects_links_unchanged')
    print('FACT|Gavin_dead_enemy_ticket_tail_reads_zero_with_clock_call_Bismarck_liveness_guard_skips_clock_no_warp')
    print('BOUNDARY|controlled_battle_array_entry_holes_fixed_clock_world_walk_watch_reclaim_adapters_full_work_delta_from_captured_birth_not_all_birth_field_oracle')
    print('OPEN|full_BATTLE_CreateVsEnemy_bootstrap_Finish_player_pet_special_party_watcher_original_reclaimer_Iris_encoding_original_ABI_JSS_Taiwan_v1')
    print('RESOLUTION|'+RESOLUTION)


if __name__=='__main__':main()
