"""Bounded complete ordinary enemy creation with actual template/stat helpers.

Original bodies remain transient. Master records, RNG stream, positive partition
sizes and empty registries are controlled; special/equipped enemies stay OPEN.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import re
import struct
import subprocess
import tempfile

from tools.stoneage_default_template_audit import (
    source_domain as template_domain, preprocess, include_args, block,
    top_entries, enums, expression, expected_data, digest,
)
from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS, _text, _compact, _function

ROOT=Path(__file__).resolve().parents[1]
PIN_PATH=ROOT/'research/recovered/STONEAGE-ENEMY-CREATION-SOURCE-DOMAINS-R1.json'
RESOLUTION='BOUNDED_ORIGINAL_ORDINARY_UNEQUIPPED_ENEMY_CREATION_PASS_ZERO_RUNTIME_PROMOTIONS'


def definition(text,name):
    match=re.search(r'\b(?:static\s+)?(?:int|void|BOOL|float|char)\s*\*?\s*'+re.escape(name)+r'\s*\([^;{}]*\)\s*\{',text,re.S)
    if not match:raise ValueError('missing original '+name)
    signature=text[match.start():text.index('(',match.start())].rstrip()
    return _function(text[match.start():],signature)


def sources(profile,root):
    default,prior,data,flags=template_domain(profile,root)
    if prior!=json.loads((PIN_PATH.parent/'STONEAGE-DEFAULT-TEMPLATE-SOURCE-DOMAINS-R1.json').read_text())['profiles'][profile]:
        raise ValueError('accepted actual template domain drift')
    base=root/LAYOUTS[profile]
    def pp(path):
        raw=re.sub(r'^\s*#\s*include[^\n]*','',_text(root/path),flags=re.M)
        return preprocess(profile,root,'#include "version.h"\n'+raw)
    paths={key:LAYOUTS[profile]/path for key,path in
           {'base':'char/char_base.c','char':'char/char.c','enemy':'char/enemy.c','item':'item/item.c','function':'function.c','data':'char/char_data.c'}.items()}
    paths['util']=Path('server/common/workspace.c') if profile=='bismarck' else LAYOUTS[profile]/'util.c'
    text={key:pp(path) for key,path in paths.items()}
    groups={
      'base':['CHAR_CHECKINTDATAINDEX','CHAR_CHECKCHARWORKDATAINDEX','CHAR_CHECKFLGDATAINDEX','CHAR_CHECKCHARFUNCTABLEINDEX',
              '_CHAR_CHECKINDEX','_CHAR_getWorkInt','_CHAR_setInt','_CHAR_setWorkInt','_CHAR_CHECKITEMINDEX',
              '_CHAR_getItemIndex','_CHAR_getFlg','_CHAR_setWorkChar','CHAR_getCharfunctable','CHAR_constructFunctable','CHAR_initCharOneArray'],
      'char':['CHAR_initcharWorkInt','_CHAR_complianceParameter'],
      'enemy':['ENEMY_CHECKINDEX','ENEMYTEMP_CHECKINDEX','ENEMYTEMP_getEnemyTempArray','ENEMY_getInt','ENEMY_getRank','ENEMY_getExp','ENEMY_RandomChange','ENEMY_createEnemy'],
      'item':['ITEM_CHECKARRAYINDEX','_ITEM_CHECKINDEX','ITEM_equipEffect','Other_DefcharWorkInt'],
      'util':['strncpysafe'] if profile=='bismarck' else ['strncpy2','strcpysafe'],
      'function':['getFunctionPointerFromName'],
      'data':['CHAR_getNewImagenumberFromEquip'],
    }
    groups['base'].append('_CHAR_getInt' if profile=='bismarck' else 'CHAR_getInt')
    if profile=='bismarck':groups['base'][:0]=['CheckCharMaxItem','CheckCharMaxItemChar']
    bodies={n:definition(text[g],n) for g,names in groups.items() for n in names}
    headers=['stdlib.h','sys/time.h','util.h','enemy.h','enemyexptbl.h','battle.h','pet_skillinfo.h','profession_skill.h','function.h','pet.h','configfile.h']
    source=default+'\n'+''.join('#include '+('<'+n+'>' if '.' in n and n in ('stdlib.h','sys/time.h') else '"'+n+'"')+'\n' for n in headers if n in ('stdlib.h','sys/time.h') or (base/'include'/n).exists())
    source+=block(text['base'],'tagRidePetTable ridePetTable')+'\n'
    source+=block(text['base'],'static char CHAR_flgbitmaskpattern')+'\n'
    source+=block(text['data'],'int CHAR_eqimagetbl')+'\n'
    if profile=='bismarck':
        source+=re.search(r'(?m)^struct\s*\{[^}]+\}\s*ranktbl\[\]\s*=\s*\{[^;]+;',text['enemy'])[0]+'\n'
    source+=block(text['enemy'],'static int EnemyGymSkill')+'\n'+block(text['enemy'],'static int gymbody')+'\n'
    # The original empty-name lookup executes before this controlled, unused table.
    source+='static struct {STRING32 functionName;int hashcode;void *functionPointer;} correspondStringAndFunctionTable[1];\n'
    source+='int EquipEffectFunction(int,int);\nint DoujyouRandomWeponSet(int);\nvoid CHAR_sendAngelMark(int,int);\nchar *DebugFunctionName;\nstatic int rng_mode,rng_count,lookup_count,diagnostics;\n'
    source+='static int audit_rand(void){int vals[]={0,1073741824,2147483647,536870912};rng_count++;return vals[rng_mode];}\n#define rand audit_rand\n'
    source+='static Char slots[7];Char *CHAR_chara=slots;static int CHAR_playernum=2,CHAR_petnum=2,CHAR_charanum=7;\n'
    source+='typedef struct {int startcnt,cnt,endcnt;} INITCHARCOUNTER;static INITCHARCOUNTER initCharCounter[3];\n'
    source+='static ENEMY_EnemyTable ENEMY_enemy[1];static ENEMYTEMP_Table ENEMYTEMP_enemy[1];static int ENEMY_enemynum=1,ENEMYTEMP_enemynum=1;\n'
    source+=('static ITEM_Exists *ITEM_gExists;static int ITEM_sItemNum=0;\n' if profile=='bismarck' else 'static ITEM_exists *ITEM_item;static int ITEM_itemnum=0;\n')
    source+='struct timeval NowTime={1000,0};\n#undef print\n#define print(...) ((void)++diagnostics)\n#undef fprint\n#define fprint(...) ((void)++diagnostics)\n#define fprintf(...) (++diagnostics,0)\n'
    # Original safe-copy and bound/getter/setter bodies, before full constructors.
    ordered=groups['util']+[n for n in groups['base'] if n not in ('CHAR_constructFunctable','CHAR_initCharOneArray')]
    ordered+=groups['function']+['CHAR_constructFunctable','CHAR_initCharOneArray']
    ordered+=groups['data']
    ordered+=['ITEM_CHECKARRAYINDEX','_ITEM_CHECKINDEX','CHAR_initcharWorkInt','ITEM_equipEffect','Other_DefcharWorkInt','_CHAR_complianceParameter']
    ordered+=groups['enemy']
    for n in ordered:
        body=bodies[n]
        # Collector counts calls but changes no functional statements of lookup.
        if n=='getFunctionPointerFromName':body=body[:body.index('{')+1]+'\nlookup_count++;\n'+body[body.index('{')+1:]
        source+=body+'\n'
    expanded=preprocess(profile,root,source)
    dependencies=subprocess.run(['cc','-MM',*include_args(profile,root),'-x','c','-'],
        input=source,text=True,capture_output=True,check=True).stdout
    header_files={}
    for name in dependencies.replace('\\\n',' ').split()[1:]:
        path=Path(name)
        if path.is_file():header_files[path.relative_to(root).as_posix()]=digest(path.read_bytes())
    ev=enums(expanded)
    exp_values=[expression(v,ev) for v in top_entries(block(expanded,'static int enemybaseexptbl'))]
    ride=[]
    for row in top_entries(block(expanded,'tagRidePetTable ridePetTable')):
        ride.append([expression(v,ev) for v in top_entries(row)])
    identity={'source_sha':PINNED[profile],'prior_actual_template':prior,
              'files':{str(path):digest((root/path).read_bytes()) for path in paths.values()},
              'header_dependency_closure':dict(sorted(header_files.items())),
              'functions':{n:digest(_compact(b)) for n,b in bodies.items()},
              'ride_table_sha256':digest(_compact(block(expanded,'tagRidePetTable ridePetTable'))),
              'experience_table_sha256':digest((base/'include/enemyexptbl.h').read_bytes()),
              'enum_values':{n:v for n,v in ev.items() if n.startswith(('CHAR_','ENEMY_','E_T_','ITEM_FIST','ITEM_WORK'))},
              'experience_table_length':len(exp_values),'ride_table_rows':len(ride),
              'empty_callback_lookup_original_early_guard':True,'ordinary_id_only':1,
              'empty_item_registry_and_zero_drop_weapon_style':True}
    return source,identity,data,flags,exp_values,ride


def vectors():
    out=list(itertools.product(range(8),range(3),(0,1,20,151),range(6),range(4),(0,1)))
    # array/temp guard selectors: 0 valid; 1 array -1; 2 array1; 3 temp -1;4 temp1.
    cases=[(0,*c) for c in out]
    cases += [(g,0,0,level,0,rng,0) for g,level,rng in itertools.product(range(1,5),(0,20),range(4))]
    return cases


BASE_SUMS=(100,95,90,85,80,79)

def base_stats(rankcase):
    total=BASE_SUMS[rankcase];return [total//4+(i<total%4) for i in range(4)]


def rng_value(mode,lo,hi):
    return lo+int((hi-lo+1)*(0,1073741824,2147483647,536870912)[mode]/2147483648.0)


def oracle(profile,identity,data,flags,exps,ride,case,sequence):
    guard,mask,cursor,baselevel,rankcase,rng,explicit=case;ev=identity['enum_values']
    if guard:return [-1,0,0,0,0,cursor+4,1],sequence
    rs=base_stats(rankcase);level=baselevel if baselevel>0 else rng_value(rng,2,4)
    first=[v+rng_value(rng,0,4)-2 for v in rs]
    packed=sum(v<<(24-8*i) for i,v in enumerate(first))
    grown=first.copy();grown[rng_value(rng,0,3)]+=10
    random_calls=14+(baselevel<=0)
    slot=next((4+(cursor+j)%3 for j in range(3) if not(mask>>(cursor+j)%3)&1),-1)
    if slot<0:return [-1,random_calls,0,2 if profile=='bismarck' else 1,0,cursor+4,1],sequence
    d=expected_data(identity['prior_actual_template'],data);w=[0]*ev['CHAR_WORKDATAINTNUM']
    def sd(n,v):d[ev[n]]=v
    def sw(n,v):w[ev[n]]=v
    sw('CHAR_WORKFD',-1)
    if profile!='bismarck':sw('CHAR_WORKCHATROOMNUM',-1)
    stat=[((level-1)*10+100)*v for v in grown]
    for n,v in zip(('CHAR_VITAL','CHAR_STR','CHAR_TOUGH','CHAR_DEX'),stat):sd(n,v)
    for n,v in {'CHAR_BASEBASEIMAGENUMBER':100250,'CHAR_BASEIMAGENUMBER':100250,
        'CHAR_WHICHTYPE':ev['CHAR_TYPEENEMY'],'CHAR_DUELPOINT':0,'CHAR_ALLOCPOINT':packed,
        'CHAR_FIREAT':0,'CHAR_WATERAT':0,'CHAR_EARTHAT':0,'CHAR_WINDAT':0,
        'CHAR_MODAI':100,'CHAR_VARIABLEAI':0,'CHAR_LV':level,'CHAR_SLOT':7,
        'CHAR_POISON':0,'CHAR_PARALYSIS':0,'CHAR_SLEEP':0,'CHAR_STONE':0,'CHAR_DRUNK':0,
        'CHAR_CONFUSION':0,'CHAR_RARE':0,'CHAR_PETID':11,'CHAR_CRITIAL':0,'CHAR_COUNTER':0,
        'CHAR_PETRANK':rankcase,'CHAR_EXP':37 if explicit else (max(1,exps[level-1]+int((2.5,2,1.5,1,0.5,0)[rankcase]*level)) if 1<=level<=len(exps) else 0)}.items():sd(n,v)
    if profile=='bismarck':sd('CHAR_PETENEMYID',1)
    vital,strength,tough,dex=stat
    atk=int(strength*.01+tough*.01*.1+vital*.01*.1+dex*.01*.05)
    defence=int(tough*.01+strength*.01*.1+vital*.01*.1+dex*.01*.05)
    hp=int(struct.unpack('f',struct.pack('f',(vital*4+strength+tough+dex)*.01))[0])
    work={'CHAR_WORKFIXVITAL':int(vital*.01),'CHAR_WORKFIXSTR':atk,'CHAR_WORKFIXTOUGH':defence,
          'CHAR_WORKFIXDEX':int(dex*.01),'CHAR_WORKMAXHP':hp,'CHAR_WORKMAXMP':d[ev['CHAR_MAXMP']],
          'CHAR_WORKFIXLUCK':min(5,max(1,d[ev['CHAR_LUCK']])),'CHAR_WORKFIXCHARM':min(100,max(0,d[ev['CHAR_CHARM']])),
          'CHAR_WORKATTACKPOWER':atk,'CHAR_WORKDEFENCEPOWER':defence,
          'CHAR_WORKQUICK':int(dex*.01),'CHAR_WORKTACTICS':17,'CHAR_WORK_PETFLG':19,
          'CHAR_WORKMODCAPTUREDEFAULT':0,'CHAR_WORKFOXROUND':-1}
    for n,v in work.items():sw(n,v)
    sd('CHAR_HP',hp);sd('CHAR_MP',min(d[ev['CHAR_MP']],w[ev['CHAR_WORKMAXMP']]))
    # Actual original table must leave this ordinary image unmapped.
    if any(row[0]==100250 for row in ride):raise ValueError('selected ordinary image is ride mapped')
    flags=flags+[0]*(3-len(flags))
    # Output all data/work/flags, native integrity predicates and callback table emptiness.
    row=[slot,random_calls,1+ev['CHAR_LASTFUNCTION']-ev['CHAR_FIRSTFUNCTION'],0,sequence,4+(slot-4+1)%3,1,
         *d,*w,*flags,1,1,1,1]
    return row,sequence+1


def native_source(profile,source,identity):
    source+=r'''
static void output(int result,int cursor,Char before[7]){
 int preserved=1;
 for(int i=0;i<7;i++)if(i!=result && memcmp(&before[i],&slots[i],sizeof(Char)))preserved=0;
 printf("%d %d %d %d %d %d %d",result,rng_count,lookup_count,diagnostics,result>=0?slots[result].CharMakeSequenceNumber:0,initCharCounter[2].cnt,preserved);
 if(result>=0){Char *ch=&slots[result];
  for(int j=0;j<CHAR_DATAINTNUM;j++)printf(" %d",ch->data[j]);
  for(int j=0;j<CHAR_WORKDATAINTNUM;j++)printf(" %d",ch->workint[j]);
  for(size_t j=0;j<sizeof(ch->flg);j++)printf(" %u",(unsigned char)ch->flg[j]);
  int empty=ch->use==1;
  for(int j=0;j<CHAR_MAXITEMHAVE;j++)if(ch->indexOfExistItems[j]!=-1)empty=0;
  for(int j=0;j<CHAR_MAXPOOLITEMHAVE;j++)if(ch->indexOfExistPoolItems[j]!=-1)empty=0;
  for(int j=0;j<CHAR_MAXPETSKILLHAVE;j++)if(ch->unionTable.indexOfPetskill[j]!=101+j)empty=0;
  for(int j=0;j<CHAR_MAXPOOLPETHAVE;j++)if(ch->indexOfPoolPet[j]!=-1)empty=0;
  for(int j=0;j<CHAR_TITLEMAXHAVE;j++)if(ch->indexOfHaveTitle[j]!=-1)empty=0;
  int funcs=1;
  for(int j=0;j<CHAR_FUNCTABLENUM;j++)if(ch->functable[j]||ch->charfunctable[j].string[0])funcs=0;
  printf(" %d %d %d %d",empty,funcs,strcmp(ch->string[CHAR_NAME].string,"witness")==0,
   strcmp(ch->workchar[CHAR_WORKBATTLE_TACTICSOPTION].string,"opt")==0 && strcmp(ch->workchar[CHAR_WORKBATTLE_ACT_CONDITION].string,"cond")==0);
 }
 printf("\n");
}
int main(void){int guard,mask,cursor,level,rankcase,mode,explicit;
 while(scanf("%d%d%d%d%d%d%d",&guard,&mask,&cursor,&level,&rankcase,&mode,&explicit)==7){
  rng_mode=mode;rng_count=lookup_count=diagnostics=0;
  memset(slots,0xa5,sizeof(slots));for(int i=0;i<7;i++)slots[i].use=1;
  for(int i=0;i<3;i++)slots[i+4].use=(mask>>i)&1;
  initCharCounter[0]=(INITCHARCOUNTER){.startcnt=0,.endcnt=2,.cnt=0};initCharCounter[1]=(INITCHARCOUNTER){.startcnt=2,.endcnt=4,.cnt=2};initCharCounter[2]=(INITCHARCOUNTER){.startcnt=4,.endcnt=7,.cnt=4+cursor};
  memset(ENEMY_enemy,0,sizeof(ENEMY_enemy));memset(ENEMYTEMP_enemy,0,sizeof(ENEMYTEMP_enemy));
  ENEMY_enemy[0].enemytemparray=guard==3?-1:guard==4?1:0;
  int *p=ENEMY_enemy[0].intdata,*t=ENEMYTEMP_enemy[0].intdata;
  int sums[]={100,95,90,85,80,79};int sum=sums[rankcase];
  for(int j=0;j<4;j++)t[E_T_BASEVITAL+j]=sum/4+(j<sum%4);
  t[E_T_INITNUM]=100;t[E_T_LVUPPOINT]=10;t[E_T_MODAI]=100;t[E_T_SLOT]=7;t[E_T_TEMPNO]=11;t[E_T_IMGNUMBER]=100250;
  for(int j=0;j<CHAR_MAXPETSKILLHAVE;j++)t[E_T_PETSKILL1+j]=101+j;
  p[ENEMY_LV_MIN]=2;p[ENEMY_LV_MAX]=4;p[ENEMY_ID]=1;p[ENEMY_EXP]=explicit?37:-1;p[ENEMY_TACTICS]=17;p[ENEMY_PETFLG]=19;
  strcpy(ENEMYTEMP_enemy[0].chardata[E_T_NAME].string,"witness");
  strcpy(ENEMY_enemy[0].chardata[ENEMY_TACTICSOPTION].string,"opt");strcpy(ENEMY_enemy[0].chardata[ENEMY_ACT_CONDITION].string,"cond");
  Char before[7];memcpy(before,slots,sizeof(before));
  int result=ENEMY_createEnemy(guard==1?-1:guard==2?1:0,level);output(result,cursor,before);
 }return 0;
}
'''
    return source


def trap_definitions(profile,root,source,names):
    expanded=preprocess(profile,root,source);definitions=[]
    for name in names:
        match=re.search(r'(?m)^[^;{}\n]*(?:\n[^;{}]*)?\b'+re.escape(name)+r'\s*\([^;{}]*\)\s*;',expanded)
        if not match:raise ValueError('missing trap prototype '+name)
        signature=match[0].strip().rstrip(';')
        signature=re.sub(r'\b(?:extern|inline|__inline__)\s+','',signature)
        definitions.append(signature+' { fputs("TRAP '+name+'\\n",stderr); abort(); }')
    return '\n'.join(definitions)+'\n'


def execute(profile,root,source,payload,opt,traps=()):
    source+=trap_definitions(profile,root,source,traps) if traps else ''
    with tempfile.TemporaryDirectory(prefix='stoneage-enemy-') as tmp:
        exe=Path(tmp)/'probe'
        r=subprocess.run(['cc','-std=gnu99','-fgnu89-inline',opt,'-fsanitize=undefined','-fno-sanitize-recover=all',
            *include_args(profile,root),'-x','c','-','-o',str(exe)],input=source,text=True,capture_output=True)
        if r.returncode:raise ValueError(r.stderr[-15000:])
        output=subprocess.run([str(exe)],input=payload,text=True,capture_output=True)
        if output.returncode or output.stderr:raise ValueError(output.stderr+' rc='+str(output.returncode))
        return output.stdout


def audit(profile,root):
    if subprocess.run(['git','-C',str(root),'rev-parse','HEAD'],capture_output=True,text=True,check=True).stdout.strip()!=PINNED[profile]:
        raise ValueError('source HEAD drift')
    if subprocess.run(['git','-C',str(root),'status','--porcelain'],capture_output=True,text=True,check=True).stdout:
        raise ValueError('dirty original source tree')
    source,identity,data,flags,exps,ride=sources(profile,root)
    pins=json.loads(PIN_PATH.read_text())['profiles'][profile]
    if identity!=pins['identity']:raise ValueError('enemy creation source drift')
    cases=vectors();expected=[];sequence=0
    for c in cases:
        row,sequence=oracle(profile,identity,data,flags,exps,ride,c,sequence);expected.append(row)
    native=native_source(profile,source,identity)
    payload=''.join(' '.join(map(str,c))+'\n' for c in cases);reference=None
    for opt in ('-O0','-O2'):
        output=execute(profile,root,native,payload,opt,pins['unreachable_traps'])
        actual=[list(map(int,line.split())) for line in output.splitlines()]
        if len(actual)!=len(expected):raise ValueError('enemy row cardinality mismatch')
        for i,(a,b) in enumerate(zip(actual,expected)):
            if a!=b:raise ValueError(f'{profile}: mismatch case{cases[i]} first differences '+str([(j,x,y) for j,(x,y) in enumerate(zip(a,b)) if x!=y][:10]))
        if reference is not None and output!=reference:raise ValueError('optimization-dependent creator state')
        reference=output
    rejected=mutations(profile,root,native,identity,data,flags,exps,ride,pins['unreachable_traps'])
    return {'profile':profile,'source_sha':PINNED[profile],'cases_per_optimization':len(cases),
            'native_creator_calls':2*len(cases),'successful_per_optimization':sequence,
            'unreachable_traps':len(pins['unreachable_traps']),'semantic_mutations_rejected':rejected,
            'semantic_sha256':digest(reference)}


def mutations(profile,root,source,identity,data,flags,exps,ride,traps):
    """Deliberate successful-creator corruption must be seen by the full oracle."""
    cases=[(0,0,0,20,5,0,0),(0,0,1,0,0,2,1)]
    expected=[];sequence=0
    for case in cases:
        row,sequence=oracle(profile,identity,data,flags,exps,ride,case,sequence);expected.append(row)
    payload=''.join(' '.join(map(str,c))+'\n' for c in cases)
    body=definition(source,'ENEMY_createEnemy')
    final=re.search(r'return\s+(\w+)\s*;\s*}$',body)
    if not final:raise ValueError('creator final return drift')
    index=final[1]
    fields=[('work',n) for n in ('CHAR_WORKTICKETTIME','CHAR_WORKTICKETTIMESTART','CHAR_WORKOBJINDEX')]
    fields+=[('data',n) for n in ('CHAR_ALLOCPOINT','CHAR_PETRANK','CHAR_EXP','CHAR_HP','CHAR_LV')]
    for kind,name in fields:
        getter='CHAR_getWorkInt' if kind=='work' else 'CHAR_getInt'
        setter='CHAR_setWorkInt' if kind=='work' else 'CHAR_setInt'
        added=f'{setter}({index},{name},{getter}({index},{name})+1);\n'
        mutated=source.replace(body,body[:final.start()]+added+body[final.start():],1)
        actual=[list(map(int,line.split())) for line in execute(profile,root,mutated,payload,'-O0',traps).splitlines()]
        if actual==expected:raise ValueError('undetected semantic mutation '+name)
    return len(fields)


def main():
    parser=argparse.ArgumentParser()
    for p in PINNED:parser.add_argument('--'+p+'-dir',type=Path,required=True)
    args=parser.parse_args();total=0
    for p in PINNED:
        row=audit(p,getattr(args,p+'_dir'));total+=row['native_creator_calls']
        print('PROFILE|'+'|'.join(f'{k}={v}' for k,v in row.items()),flush=True)
    print(f'TOTAL|ordinary_enemy_creator_calls={total}|profiles=3')
    print('MUTATIONS|semantic_mutations_rejected=24|successful_creator_state_fields=8|profiles=3')
    print('FACT|actual_default_allocator_empty_name_lookup_complete_creator_rank_exp_and_stat_helpers_execute')
    print('FACT|ordinary_unequipped_enemy_creation_zero_ticket_start_object_callbacks_after_real_stat_composition')
    print('BOUNDARY|synthetic_master_records_scripted_rand_ordinary_id1_no_drops_no_weapon_empty_items_positive_partitions_original_headers_LP64')
    print('OPEN|real_master_loader_special_enemy_items_equipment_nonempty_callbacks_world_object_Exit_reuse_original_build_JSS_Taiwan_v1_runtime')
    print('RESOLUTION|'+RESOLUTION)


if __name__=='__main__':main()
