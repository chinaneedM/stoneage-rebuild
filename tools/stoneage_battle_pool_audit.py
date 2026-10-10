"""Actual battle arena/bootstrap, bounded creation rollback and enemy-only Finish.

Original functions, headers and master bytes stay transient. Encounter table,
field and disconnected descriptor are explicit adapters; player entry traps.
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

from tools.stoneage_enemy_entry_exit_audit import domain as entry_domain, compile_probe, RowReader, entry_changes
from tools.stoneage_enemy_loader_audit import pp_file, specimen, loaded_oracle, eligible, birth_expectation, PROFILES
from tools.stoneage_enemy_creation_audit import definition, rng_value
from tools.stoneage_object_ownership_audit import BIRTH_DATA, BIRTH_WORK
from tools.stoneage_default_template_audit import digest, include_args, preprocess, expression
from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS, _compact

ROOT=Path(__file__).resolve().parents[1]
PIN_PATH=ROOT/'research/recovered/STONEAGE-BATTLE-POOL-SOURCE-DOMAINS-R1.json'
RESOLUTION='BOUNDED_ACTUAL_BATTLE_BOOTSTRAP_ROLLBACK_ENEMY_FINISH_PASS_ZERO_RUNTIME_PROMOTIONS'


def domain(profile,root):
    source,prior,data,flags,exps,ride=entry_domain(profile,root)
    accepted=json.loads((PIN_PATH.parent/'STONEAGE-ENEMY-ENTRY-EXIT-SOURCE-DOMAINS-R1.json').read_text())['profiles'][profile]['identity']
    if prior!=accepted:raise ValueError('accepted entry identity drift')
    declaration='static BATTLE controlled_battle[1];BATTLE *BattleArray=controlled_battle;int BATTLE_battlenum=1;'
    if source.count(declaration)!=1:raise ValueError('controlled battle declaration drift')
    source=source.replace(declaration,'BATTLE *BattleArray;int BATTLE_battlenum;')
    path=LAYOUTS[profile]/'battle/battle.c';text=pp_file(profile,root,path)
    names=['BATTLE_initBattleArray','BATTLE_SearchTask','BATTLE_CreateBattle','BATTLE_DeleteItem',
           'BATTLE_WatchUnLink','BATTLE_DeleteBattle','_BATTLE_ExitAll','BATTLE_CreateVsEnemy',
           'BATTLE_GetExpGold','BATTLE_GetProfit','BATTLE_Finish','Battle_getTotalBattleNum']
    bodies={n:definition(text,n) for n in names}
    rs=re.search(r'typedef\s+struct\s*\{[^{}]+\}\s*RS_LIST\s*;',text)
    if not rs:raise ValueError('RS_LIST domain drift')
    declarations=[]
    for n in ('Total_BattleNum','BATTLE_searchCnt'):
        m=re.search(r'(?m)^static\s+int\s+'+n+r'\s*=\s*0\s*;',text)
        if not m:raise ValueError('battle private declaration drift '+n)
        declarations.append(m[0])
    extra_headers=['npcutil.h','npc_npcenemy.h','log.h']
    if profile=='bismarck':extra_headers.append('config_file.h')
    source+='\n'+''.join('#include "'+h+'"\n' for h in extra_headers)
    # File-local declarations are recovered from their exact original signatures.
    prototypes={n:definition(text,n).split('{',1)[0].strip()+';' for n in
                ('BATTLE_PartyNewEntry','BATTLE_EnemyRandowSetSkill','BATTLE_GetExp','Doujyou_GetEnemy')}
    source+='\n'.join(prototypes.values())+'\n'+rs[0]+'\n'+'\n'.join(declarations)+'\n'
    source+=r'''
static int encounter_table[5],encounter_count,field_count,fd_count,netwatch_count;
static int selected_null;
static int audit_birth(int,int);
int *ENEMY_getEnemy(int actor,int x,int y){
 if(actor!=0 || x!=1 || y!=1)abort();encounter_count++;
 return selected_null?NULL:encounter_table;
}
static int BATTLE_getBattleFieldNo(int floor,int x,int y){
 if(floor!=1 || x!=1 || y!=1)abort();field_count++;return 0;
}
int getfdFromCharaIndex(int actor){if(actor!=0)abort();fd_count++;return -1;}
'''
    if profile=='bismarck':
        source+='void NETWATCH_set(const char *stage,int value,const char *detail){if(strncmp(stage,"BATTLE_Finish.",14))abort();netwatch_count++;}\n'
    source+='#define time audit_time\n'
    for n in names:
        if n=='BATTLE_CreateVsEnemy':source+='#define ENEMY_createEnemy audit_birth\n'+bodies[n]+'\n#undef ENEMY_createEnemy\n'
        else:source+=bodies[n]+'\n'
    source+='#undef time\n'
    battle_modes={}
    for body in re.findall(r'\benum(?:\s+\w+)?\s*\{([^{}]+)\}',preprocess(profile,root,source)):
        if 'BATTLE_MODE_NONE' not in body:continue
        value=-1
        for item in body.split(','):
            pair=item.strip().split('=',1);name=pair[0].strip()
            value=expression(pair[1],battle_modes) if len(pair)==2 else value+1;battle_modes[name]=value
    if not battle_modes:raise ValueError('battle mode enum drift')
    deps=subprocess.run(['cc','-MM',*include_args(profile,root),'-x','c','-'],input=source,text=True,capture_output=True,check=True).stdout
    closure={}
    for n in deps.replace('\\\n',' ').split()[1:]:
        p=Path(n)
        if p.is_file():closure[p.relative_to(root).as_posix()]=digest(p.read_bytes())
    identity={'source_sha':PINNED[profile],'accepted_entry_identity':prior,
              'file':{str(path):digest((root/path).read_bytes())},
              'functions':{n:digest(_compact(b)) for n,b in bodies.items()},
              'private_declarations_sha256':digest(_compact('\n'.join(declarations))),
              'RS_LIST_sha256':digest(_compact(rs[0])),
              'unreachable_file_local_signature_sha256':{n:digest(_compact(v)) for n,v in prototypes.items()},
              'header_dependency_closure':dict(sorted(closure.items())),
              'battle_capacity':3,'enemy_capacity':3,
              'battle_mode_enum_values':battle_modes,
              'constructor_zeroes_whole_BATTLE':profile=='bismarck',
              'adapters':['encounter table/NULL selector','field0 predicate','descriptor-1',
                          'observational birth wrapper with controlled per-birth RNG restart',
                          'inherited clock/world/walk/watch/detached-node collectors']}
    return source,identity,data,flags,exps,ride


def native_source(profile,source):
    setup='if(!configmem(64,262144))return 11;' if profile=='gavin' else 'sUnitSize=64;sUnitNumTotal=262144;'
    jump='static int controlled_jump[2]={-1,0};MAP_idjumptbl=controlled_jump;' if profile=='gavin' else 'MAP_idjumptbl[0]=-1;MAP_idjumptbl[1]=0;'
    field='char_index' if profile=='bismarck' else 'charaindex'
    birth=''.join(f'printf(" %d",ch->data[{n}]);' for n in BIRTH_DATA)+''.join(f'printf(" %d",ch->workint[{n}]);' for n in BIRTH_WORK)
    constructor_zero='memset(&expected,0,sizeof(expected));' if profile=='bismarck' else ''
    leader_setup='slots[0].workint[CHAR_WORKSTREETVENDOR]=-1;slots[0].workint[CHAR_WORKANGELMODE]=0;' if profile=='gavin' else ''
    return (source+r'''
static Char worlds[2],birth_before[3];static int born,battle_at,born_slots[3];
static void sparse(const int *work,const int *base){
 int count=0;for(int j=0;j<CHAR_WORKDATAINTNUM;j++)if(work[j]!=(base?base[j]:0))count++;
 printf(" %d",count);for(int j=0;j<CHAR_WORKDATAINTNUM;j++)if(work[j]!=(base?base[j]:0))printf(" %d %d",j,work[j]);
}
static int audit_birth(int array,int level){
 rng_count=0;int result=ENEMY_createEnemy(array,level);printf(" %d %d",result,rng_count);
 if(result<0)return result;
 if(result<4||result>=7||born>=3)abort();Char *ch=&slots[result];birth_before[result-4]=*ch;born_slots[born++]=result;
 printf(" %d",ch->CharMakeSequenceNumber);
'''+birth+r'''
 sparse(ch->workint,NULL);for(int j=0;j<sizeof(ch->flg);j++)printf(" %u",(unsigned char)ch->flg[j]);return result;
}
static void expected_entry(BATTLE_ENTRY *e){e->ENTRY_FIELD=-1;e->bid=-1;e->escape=0;for(int j=0;j<GETITEM_MAX;j++)e->getitem[j]=-1;}
static int check_constructor(int index,BATTLE before){
 BATTLE expected=before;
'''+constructor_zero+r'''
 expected.use=1;expected.mode=BATTLE_MODE_INIT;expected.turn=0;expected.dpbattle=0;
 expected.norisk=0;expected.flg=0;expected.field_att=BATTLE_ATTR_NONE;expected.att_count=0;
 for(int s=0;s<2;s++)for(int j=0;j<BATTLE_ENTRY_MAX;j++)expected_entry(&expected.Side[s].Entry[j]);
 for(int j=0;j<2*BATTLE_ENTRY_MAX;j++)expected.iEntryBack[j]=expected.iEntryBack2[j]=-1;
 expected.WinFunc=NULL;expected.pNext=expected.pBefore=NULL;expected.battleindex=index;expected.PartTime=0;
 return !memcmp(&expected,&BattleArray[index],sizeof(expected));
}
static int world_same(void){
 if(memcmp(worlds,slots,2*sizeof(Char))||watch_count!=2||reclaim_count)return 0;
 for(int i=0;i<2;i++)if(OBJECT_getType(i)!=1||OBJECT_getIndex(i)!=i||OBJECT_getFloor(i)!=1||OBJECT_getX(i)!=1||OBJECT_getY(i)!=1)return 0;
 for(int j=0;j<3;j++)if(controlled_links[j])return 0;
 MAP_Objlink *link=controlled_links[3];return link&&link->objindex==0&&link->next&&link->next->objindex==1&&!link->next->next;
}
static int battle_empty(int index){
 for(int s=0;s<2;s++)for(int j=0;j<BATTLE_ENTRY_MAX;j++){
  BATTLE_ENTRY *e=&BattleArray[index].Side[s].Entry[j];
  if(e->ENTRY_FIELD!=-1||e->bid!=-1||e->escape)return 0;
  for(int k=0;k<GETITEM_MAX;k++)if(e->getitem[k]!=-1)return 0;
 }return BattleArray[index].pNext==NULL&&BattleArray[index].pBefore==NULL;
}
static void actors(void){
 for(int i=0;i<born;i++){
  int actor=born_slots[i];Char *ch=&slots[actor];int clear=1;
  for(int j=0;j<CHAR_MAXITEMHAVE;j++)if(ch->indexOfExistItems[j]!=-1)clear=0;
  for(int j=0;j<CHAR_MAXPOOLITEMHAVE;j++)if(ch->indexOfExistPoolItems[j]!=-1)clear=0;
  BATTLE_ENTRY *e=&BattleArray[battle_at].Side[1].Entry[i];
  printf(" %d %d %d %d",actor,e->ENTRY_FIELD,e->bid,e->escape);
  for(int j=0;j<GETITEM_MAX;j++)printf(" %d",e->getitem[j]);
  printf(" %d %d %d %d %d",ch->use,clear,searchObjectFromCharaIndex(actor),
   !memcmp(ch->data,birth_before[actor-4].data,sizeof(ch->data)),!memcmp(ch->string,birth_before[actor-4].string,sizeof(ch->string)));
  sparse(ch->workint,birth_before[actor-4].workint);
  for(int j=0;j<sizeof(ch->flg);j++)printf(" %u",(unsigned char)ch->flg[j]);
 }
}
static void lifecycle(void){
 printf(" %d %d %d %d %d %d %d %d %d %d %d",battle_at,Battle_getTotalBattleNum(),BATTLE_searchCnt,
  BattleArray[battle_at].use,BattleArray[battle_at].mode,battle_empty(battle_at),world_same(),clock_count,netwatch_count,slots[4].use+slots[5].use+slots[6].use,initCharCounter[2].cnt);
 actors();
}
int main(int argc,char **argv){
 if(argc!=3||sizeof(void*)!=8||sizeof(int)!=4)return 10;
'''+setup+r'''
 if(!memInit())return 12;
 if(!ENEMYTEMP_initEnemy(argv[1])||!ENEMY_initEnemy(argv[2])||!BATTLE_initBattleArray(3))return 13;
 int zero=1;for(size_t j=0;j<3*sizeof(BATTLE);j++)if(((unsigned char*)BattleArray)[j])zero=0;
 MAP_map=controlled_map;MAP_idtblsize=1;
'''+jump+r'''
 controlled_map[0].id=1;controlled_map[0].xsiz=controlled_map[0].ysiz=2;controlled_map[0].olink=controlled_links;
 initCharCounter[0]=(INITCHARCOUNTER){0,0,2};initCharCounter[1]=(INITCHARCOUNTER){2,2,4};initCharCounter[2]=(INITCHARCOUNTER){4,4,7};
 if(!initObjectArray(2))return 14;
 for(int i=0;i<2;i++){int c,o;if(!CHAR_createCharacter(CHAR_TYPEPLAYER,1,1,1,0,&c,&o,1)||c!=i||o!=i)return 15;}
'''+leader_setup+r'''
 memcpy(worlds,slots,2*sizeof(Char));
 printf("P %d %d",zero,BATTLE_battlenum);
 for(int i=0;i<3;i++){
  BattleArray[i].createindex=71;BattleArray[i].leaderindex=72;BattleArray[i].field_no=73;BattleArray[i].Side[0].flg=8;
  BATTLE before=BattleArray[i];int index=BATTLE_CreateBattle();printf(" %d %d",index,check_constructor(i,before));
 }
 printf(" %d %d",BATTLE_CreateBattle(),Battle_getTotalBattleNum());
 for(int i=0;i<3;i++)printf(" %d",BATTLE_DeleteBattle(i));
 printf(" %d %d",Battle_getTotalBattleNum(),BATTLE_CreateVsEnemy(-1,0,-1));
 selected_null=1;encounter_count=field_count=fd_count=0;
 printf(" %d",BATTLE_CreateVsEnemy(0,0,-1));
 printf(" %d %d %d %d %d\n",Battle_getTotalBattleNum(),world_same(),encounter_count,field_count,fd_count);selected_null=0;
 int array,mode,kind,count;
 while(scanf("%d%d%d%d",&array,&mode,&kind,&count)==4){
  born=0;rng_mode=mode;clock_count=netwatch_count=0;encounter_count=field_count=fd_count=0;
  battle_at=BATTLE_searchCnt%3;printf("C %d %d %d %d",array,mode,kind,count);
  if(kind!=1){
   for(int j=0;j<count;j++)encounter_table[j]=array;encounter_table[count]=kind==2?array:ENEMY_enemynum;encounter_table[count+1]=-1;
   int ret=BATTLE_CreateVsEnemy(0,0,-1);printf(" %d %d %d %d",ret,encounter_count,field_count,fd_count);lifecycle();
  }else{
   BATTLE before=BattleArray[battle_at];int index=BATTLE_CreateBattle();printf(" %d %d",index,check_constructor(battle_at,before));
   BATTLE *b=&BattleArray[battle_at];b->Side[0].type=b->Side[1].type=BATTLE_S_TYPE_ENEMY;
   b->type=BATTLE_TYPE_P_vs_E;b->winside=1;b->WinFunc=NULL;
   for(int j=0;j<count;j++){int c=audit_birth(array,0);printf(" %d",BATTLE_NewEntry(c,battle_at,1));}
   printf(" %d %d",Battle_getTotalBattleNum(),world_same());actors();
   int ret=BATTLE_Finish(battle_at);printf(" %d",ret);lifecycle();
  }
  printf("\n");
 }
 endObjectOne(0);endObjectOne(1);memEnd();return 0;
}
''').replace('ENTRY_FIELD',field)


def cases_for(selected):
    cases=[]
    for n,(index,mode) in enumerate((i,m) for i in selected for m in range(4)):
        cases.extend([(index,mode,0,n%4),(index,mode,1,1+n%3)])
    return cases+[(selected[0],m,2,3) for m in range(4)]


def verify_pool(identity,line):
    ev=identity['accepted_entry_identity']['enum_values']
    wanted=[1,3,0,1,1,1,2,1,-1,3,0,0,0,0,ev['BATTLE_ERR_CHARAINDEX'],ev['BATTLE_ERR_NOENEMY'],0,1,1,1,1]
    if line.split()!=['P',*map(str,wanted)]:raise ValueError('battle pool bootstrap/cursor/full/constructor/no-enemy mismatch')


def actor_delta(profile,identity,before,battle,exited,abio=False):
    entry=identity['accepted_entry_identity'];ev=entry['enum_values'];after=before.copy()
    after.update(entry_changes(profile,entry,before,1,exited))
    after[ev['CHAR_WORKBATTLEINDEX']]=-1 if exited else battle
    if abio:after[ev['CHAR_WORKBATTLEFLG']]=ev['CHAR_BATTLEFLG_ABIO']
    return {k:v for k,v in sorted(after.items()) if v!=before.get(k,0)}


def natural_birth_expectation(loader,data,exps,temp,enemy,level,mode):
    """Own-level birth; the original experience helper guards its table bounds."""
    ev=loader['accepted_creator_identity']['enum_values']
    if not 1<=level<=len(exps) and enemy[1][ev['ENEMY_EXP']]==-1:
        # Oracle-only substitution selects the explicit zero result of that guard;
        # native master bytes and original helper remain completely unchanged.
        ints=enemy[1].copy();ints[ev['ENEMY_EXP']]=0
        enemy=(enemy[0],ints,enemy[2])
    return birth_expectation(loader,data,exps,temp,enemy,level,mode)


def verify_line(profile,identity,data,flags,exps,temps,enemies,case,line,number,sequence):
    rd=RowReader(line);index,mode,kind,count=case;entry=identity['accepted_entry_identity'];ev=entry['enum_values'];lim=entry['limits']
    if rd.take(4)!=list(case):raise ValueError('battle pool case order')
    battle=(1+number)%3;births=[]
    finish=kind==1
    if finish and rd.take(2)!=[battle,1]:raise ValueError('battle pool constructor/reuse mismatch')
    loader=entry['accepted_ownership_identity']['accepted_loader_identity'];e=enemies[index];creator=loader['accepted_creator_identity'];ce=creator['enum_values']
    level=rng_value(mode,e[1][ce['ENEMY_LV_MIN']],e[1][ce['ENEMY_LV_MAX']])
    d,w=natural_birth_expectation(loader,data,exps,temps[e[0]],e,level,mode)
    for j in range(count):
        if rd.take(3)!=[4+(sequence-2+j)%3,15,sequence+j]:raise ValueError('battle pool birth slot/RNG/sequence')
        if rd.take(len(BIRTH_DATA)+len(BIRTH_WORK))!=[d[n] for n in BIRTH_DATA]+[w[n] for n in BIRTH_WORK]:raise ValueError('battle pool named birth')
        before=rd.sparse(ev['CHAR_WORKDATAINTNUM']);f=rd.take(lim['flag_bytes'])
        if f!=flags+[0]*(lim['flag_bytes']-len(flags)):raise ValueError('battle pool birth flags')
        for n,v in w.items():
            if before.get(ev[n],0)!=v:raise ValueError('battle pool captured birth consistency')
        if births and births[0]!=(before,f):raise ValueError('battle pool simultaneous/recreated birth baseline')
        births.append((before,f))
        if finish and rd.take(1)!=[0]:raise ValueError('battle pool manual Entry result')
    def actors(exited):
        for j,(before,f) in enumerate(births):
            slot=4+(sequence-2+j)%3
            expected_entry=[slot,-1,-1,0] if exited else [slot,slot,10+j,0]
            if rd.take(4+lim['item_max'])!=expected_entry+[-1]*lim['item_max']:raise ValueError('battle pool named entry stage')
            if rd.take(5)!=[int(not exited),1,-1,1,1]:raise ValueError('battle pool actor lifetime/data/string/item/object')
            abio=not finish and 100466<=d['CHAR_BASEBASEIMAGENUMBER']<=100471
            if rd.sparse(ev['CHAR_WORKDATAINTNUM'])!=actor_delta(profile,identity,before,battle,exited,abio):raise ValueError('battle pool complete actor work delta')
            f=f.copy();f[ev['CHAR_ISATTACKED']//8]|=1<<(ev['CHAR_ISATTACKED']%8);f[ev['CHAR_ISDIE']//8]&=255^(1<<(ev['CHAR_ISDIE']%8))
            if rd.take(lim['flag_bytes'])!=f:raise ValueError('battle pool actor flags')
    if not finish:
        if rd.take(2)!=[-1,15 if kind==2 else 0]:raise ValueError('battle pool failing array/capacity guard')
        # Gavin resolves the descriptor twice after a non-NULL table, Bismarck once.
        if rd.take(4)!=[ev['BATTLE_ERR_NOENEMY'],1,1,2 if profile=='gavin' else 1]:raise ValueError('battle pool rollback result/adapters')
    else:
        if rd.take(2)!=[1,1]:raise ValueError('battle pool entered arena/world')
        actors(False)
        if rd.take(1)!=[0]:raise ValueError('battle pool Finish result')
    expected=[battle,0,battle+1,0,identity['battle_mode_enum_values']['BATTLE_MODE_NONE'],1,1,
              (count if profile=='gavin' else 0)+(int(not finish)),
              2*count+1 if finish and profile=='bismarck' else 0,0,4+(sequence-2+count)%3]
    if rd.take(11)!=expected:raise ValueError('battle pool final arena/count/cursor/world/clock/NETWATCH')
    actors(True);rd.done();return sequence+count


def mutation_trials(source):
    create=definition(source,'BATTLE_CreateBattle');search=definition(source,'BATTLE_SearchTask')
    delete=definition(source,'BATTLE_DeleteBattle');vs=definition(source,'BATTLE_CreateVsEnemy');finish=definition(source,'BATTLE_Finish')
    def replace_once(body,pattern,replacement):
        out,n=re.subn(pattern,replacement,body)
        if n!=1:raise ValueError('battle pool mutation anchor drift')
        return out
    yield 'cursor',source.replace(search,replace_once(search,r'BATTLE_searchCnt\s*=\s*i\s*\+\s*1\s*;', 'BATTLE_searchCnt=i;'),1),1
    yield 'total',source.replace(create,replace_once(create,r'Total_BattleNum\s*\+\+\s*;', 'Total_BattleNum+=2;'),1),1
    yield 'delete-mode',source.replace(delete,replace_once(delete,r'pBattle->mode\s*=\s*BATTLE_MODE_NONE\s*;', 'pBattle->mode=BATTLE_MODE_INIT;'),1),1
    # Replace each rollback site; only the failure site executes in this scope.
    changed,n=re.subn(r'BATTLE_ExitAll\(\s*battleindex\s*\)\s*;', '(void)0;',vs)
    if n!=2:raise ValueError('battle pool rollback sites drift')
    yield 'rollback-ExitAll',source.replace(vs,changed,1),0
    changed,n=re.subn(r'BATTLE_Exit\(\s*(?:charaindex|char_index)\s*,\s*battleindex\s*\)\s*;', '(void)0;',finish)
    if n!=1:raise ValueError('battle pool Finish Exit drift')
    yield 'Finish-Exit',source.replace(finish,changed,1),1


def execute(profile,root,source,paths,cases,opt,traps,tmp):
    exe=tmp/('probe'+opt);compile_probe(profile,root,native_source(profile,source),exe,opt,traps)
    out=tmp/('output'+opt+'.txt')
    with out.open('w') as stream:
        r=subprocess.run([str(exe),*map(str,paths)],input=''.join(' '.join(map(str,c))+'\n' for c in cases),text=True,stdout=stream,stderr=subprocess.PIPE)
    if r.returncode or r.stderr:raise ValueError('unsafe battle pool probe '+r.stderr+' rc='+str(r.returncode))
    return out


def verify_output(profile,identity,data,flags,exps,temps,enemies,cases,path):
    sequence=2
    with path.open() as stream:
        verify_pool(identity,stream.readline().strip())
        for n,c in enumerate(cases):sequence=verify_line(profile,identity,data,flags,exps,temps,enemies,c,stream.readline(),n,sequence)
        if stream.readline():raise ValueError('battle pool extra rows')


def audit(profile,root,paths):
    pins=json.loads(PIN_PATH.read_text())['profiles'][profile]
    source,identity,data,flags,exps,ride=domain(profile,root)
    if identity!=pins['identity']:raise ValueError('battle pool source drift')
    loader=identity['accepted_entry_identity']['accepted_ownership_identity']['accepted_loader_identity']
    temps,enemies=loaded_oracle(profile,loader,*[p.read_bytes() for p in paths],32,32)
    selected=eligible(loader,temps,enemies,ride);cases=cases_for(selected)
    with tempfile.TemporaryDirectory(prefix='stoneage-battle-pool-') as directory:
        tmp=Path(directory);outputs=[]
        for opt in ('-O0','-O2'):
            out=execute(profile,root,source,paths,cases,opt,pins['unreachable_traps'],tmp)
            verify_output(profile,identity,data,flags,exps,temps,enemies,cases,out);outputs.append(out)
        if not filecmp.cmp(*outputs,shallow=False):raise ValueError('battle pool optimization divergence')
        sha=hashlib.sha256(outputs[0].read_bytes()).hexdigest();rejected=0
        for name,mutant,kind in mutation_trials(source):
            case=[(selected[0],1,kind,3)]
            out=execute(profile,root,mutant,paths,case,'-O0',pins['unreachable_traps'],tmp)
            try:verify_output(profile,identity,data,flags,exps,temps,enemies,case,out)
            except ValueError:rejected+=1
            else:raise ValueError('undetected battle pool mutation '+name)
    return {'profile':profile,'source_sha':PINNED[profile],'rollback_cycles':sum(c[2]!=1 for c in cases)*2,
            'enemy_Finish_cycles':sum(c[2]==1 for c in cases)*2,'preserved_enemy_births':sum(c[3] for c in cases)*2,
            'full_actor_work_stage_comparisons':sum(c[3]*(1+int(c[2]==1)) for c in cases)*2,
            'mutations_rejected':rejected,'semantic_sha256':sha}


def main():
    parser=argparse.ArgumentParser()
    for p in PINNED:parser.add_argument('--'+p+'-dir',type=Path,required=True)
    args=parser.parse_args();roots={p:getattr(args,p+'_dir') for p in PINNED}
    for p,r in roots.items():
        if subprocess.check_output(['git','-C',str(r),'rev-parse','HEAD'],text=True).strip()!=PINNED[p] or subprocess.check_output(['git','-C',str(r),'status','--porcelain'],text=True):raise ValueError('source pin/cleanliness '+p)
    paths,receipt=specimen(roots['gavin']);pins=json.loads(PIN_PATH.read_text())
    if receipt!=pins['preserved_specimen']:raise ValueError('battle pool input drift')
    totals={k:0 for k in ('rollback_cycles','enemy_Finish_cycles','preserved_enemy_births','full_actor_work_stage_comparisons')}
    for p in PROFILES:
        row=audit(p,roots[p],paths)
        for k in totals:totals[k]+=row[k]
        print('PROFILE|'+'|'.join(f'{k}={v}' for k,v in row.items()),flush=True)
    print('TOTAL|'+'|'.join(f'{k}={v}' for k,v in totals.items())+'|executed_profiles=2')
    print('MUTATIONS|semantic_mutations_rejected=10|cursor_total_delete_mode_rollback_ExitAll_Finish_Exit|additional_cycles=10')
    print('FACT|actual_arena_allocation_zeroing_round_robin_full_pool_creation_rollback_empty_item_delete_enemy_only_Finish_execute')
    print('FACT|Gavin_constructor_retains_unlisted_fields_Bismarck_zeroes_whole_battle_no_profile_flattening')
    print('BOUNDARY|encounter_field_descriptor_birth_trace_RNG_clock_world_adapters_no_player_party_entry_no_profit_distribution_no_original_reclaimer')
    print('OPEN|successful_player_party_CreateVsEnemy_battle_Init_TaskLoop_watcher_nonempty_items_callbacks_original_ABI_JSS_Taiwan_v1_Iris_encoding')
    print('RESOLUTION|'+RESOLUTION)


if __name__=='__main__':main()
