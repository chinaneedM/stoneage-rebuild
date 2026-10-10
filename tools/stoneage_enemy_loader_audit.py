"""Execute original master loaders and ordinary births from preserved CSV bytes.

No original content is committed. Gavin's configured specimen is same-pin data;
Bismarck reads those bytes as an explicit cross-profile compatibility witness.
Iris's Windows conversion remains an unexecuted boundary, not a no-op adapter.
"""
from __future__ import annotations
import argparse
import io
import json
from pathlib import Path
import re
import struct
import subprocess
import tempfile

from tools.stoneage_enemy_creation_audit import sources as creator_sources, trap_definitions, rng_value
from tools.stoneage_default_template_audit import preprocess, include_args, digest, expected_data
from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS, _text, _compact, _function

ROOT=Path(__file__).resolve().parents[1]
PIN_PATH=ROOT/'research/recovered/STONEAGE-ENEMY-LOADER-SOURCE-DOMAINS-R1.json'
PROFILES=('gavin','bismarck')
RESOLUTION='BOUNDED_ORIGINAL_MASTER_LOADING_AND_PRESERVED_ORDINARY_BIRTH_PASS_ZERO_RUNTIME_PROMOTIONS'


def definition(text,name):
    match=re.search(r'(?m)^[^;{}\n]+?\b'+re.escape(name)+r'\s*\([^;{}]*\)\s*\{',text)
    if not match:raise ValueError('missing original '+name)
    signature=text[match.start():text.index('(',match.start())].rstrip()
    return _function(text[match.start():],signature)


def pp_file(profile,root,path):
    raw=re.sub(r'^\s*#\s*include[^\n]*','',_text(root/path),flags=re.M)
    return preprocess(profile,root,'#include "version.h"\n#include "util.h"\n'+raw)


def domain(profile,root):
    source,prior,data,flags,exps,ride=creator_sources(profile,root)
    accepted=json.loads((PIN_PATH.parent/'STONEAGE-ENEMY-CREATION-SOURCE-DOMAINS-R1.json').read_text())['profiles'][profile]
    if prior!=accepted['identity']:raise ValueError('accepted creator identity drift')
    source=source.replace('static ENEMY_EnemyTable ENEMY_enemy[1];static ENEMYTEMP_Table ENEMYTEMP_enemy[1];static int ENEMY_enemynum=1,ENEMYTEMP_enemynum=1;',
                          'static ENEMY_EnemyTable *ENEMY_enemy;static ENEMYTEMP_Table *ENEMYTEMP_enemy;static int ENEMY_enemynum,ENEMYTEMP_enemynum;')
    paths={'enemy':LAYOUTS[profile]/'char/enemy.c','memory':LAYOUTS[profile]/'buf.c'}
    paths['util']=Path('server/common/utils/util_string.c') if profile=='bismarck' else LAYOUTS[profile]/'util.c'
    if profile=='bismarck':
        paths['file']=Path('server/common/utils/util_file.c')
        paths['copy']=Path('server/common/workspace.c')
    text={key:pp_file(profile,root,path) for key,path in paths.items()}
    memory=text['memory'];start=memory.index('static int ');end=memory.index('void memEnd(',start)
    memory_declarations=memory[start:end]
    source+='\n#include "buf.h"\n'
    if profile=='bismarck':source+='#include "utils/util_file.h"\n'
    source+=memory_declarations+'\n'
    groups={'memory':['memInit','allocateMemory','memEnd'],
            'enemy':['ENEMY_CHECKCHARDATAINDEX','ENEMY_setInt','ENEMY_setChar',
                     'ENEMYTEMP_CHECKCHARDATAINDEX','ENEMYTEMP_getInt','ENEMYTEMP_setInt','ENEMYTEMP_setChar']}
    if profile=='gavin':
        groups['memory'].insert(0,'configmem')
        groups['util']=['dchop','replaceString','strncpysafe','ScanOneByte','getStringFromIndexWithDelim_body']
    else:
        groups['copy']=['strncpysafe2']
        groups['util']=['strstr_onebyte','GeneralSplitImpl']
        groups['file']=['open_realop_file','get_file_line_num','get_file_lines']
        groups['enemy']+=['enemytemp_callback','enemy_callback']
    bodies={n:definition(text[g],n) for g,names in groups.items() for n in names}
    bodies.update({n:definition(text['enemy'],n) for n in ('ENEMYTEMP_initEnemy','ENEMY_initEnemy')})
    # Count otherwise irrelevant helper diagnostics, leaving functional statements.
    source+='#define printf(...) (++diagnostics,0)\n'
    for g in ('memory','copy','util','file','enemy'):
        for n in groups.get(g,[]):source+=bodies[n]+'\n'
    source+=bodies['ENEMYTEMP_initEnemy']+'\n'+bodies['ENEMY_initEnemy']+'\n#undef printf\n'
    deps=subprocess.run(['cc','-MM',*include_args(profile,root),'-x','c','-'],input=source,text=True,capture_output=True,check=True).stdout
    headers={}
    for n in deps.replace('\\\n',' ').split()[1:]:
        p=Path(n)
        if p.is_file():headers[p.relative_to(root).as_posix()]=digest(p.read_bytes())
    identity={'source_sha':PINNED[profile],'accepted_creator_identity':prior,
              'files':{str(p):digest((root/p).read_bytes()) for p in paths.values()},
              'functions':{n:digest(_compact(b)) for n,b in bodies.items()},
              'memory_declarations_sha256':digest(_compact(memory_declarations)),
              'header_dependency_closure':dict(sorted(headers.items())),
              'original_pool_initialization_allocation_and_shutdown':True,
              'controlled_pool_bytes':16777216,'original_freeMemory_not_executed':True,
              'bismarck_pool_dimensions_configured_directly':profile=='bismarck',
              'loader_kind':'callback file helpers' if profile=='bismarck' else 'two-pass fgets256',
              'unreachable_traps':accepted['unreachable_traps']}
    return source,identity,data,flags,exps,ride


def c_atoi(token):
    m=re.match(rb'\s*([+-]?\d+)',token)
    value=int(m[1]) if m else 0
    if not -2147483648<=value<=2147483647:raise ValueError('out-of-domain atoi overflow')
    return value


def input_lines(profile,content):
    stream=io.BytesIO(content)
    # Real specimen lines are shorter than both original capacities.
    limit=255 if profile=='gavin' else 1023
    while chunk:=stream.readline(limit):
        if b'\0' in chunk:raise ValueError('embedded NUL outside declared corpus')
        if profile=='gavin':
            if chunk[:1] in (b'#',b'\n'):continue
            line=(chunk[:-1] if chunk.endswith(b'\n') else chunk).replace(b'\t',b' ')
            leading=len(line)-len(line.lstrip(b' '))
            if leading==len(line) and leading:raise ValueError('space-only legacy trim outside safe corpus')
            if leading:line=line[leading-1:] # actual legacy loop keeps one space
        else:
            line=re.split(rb'[\r\n]',chunk.replace(b'\r',b''),maxsplit=1)[0]
            if not line or line.startswith(b'#'):continue
        yield line


def fields(profile,line):
    # Original gavin ScanOneByte skips a following byte after any high byte.
    if profile=='bismarck':return line.split(b',')
    start=0;i=0;out=[]
    while i<len(line):
        if line[i]>=128:i+=2;continue
        if line[i]==44:out.append(line[start:i]);start=i+1
        i+=1
    out.append(line[start:]);return out


def loaded_oracle(profile,identity,temp_bytes,enemy_bytes,temp_cap,enemy_cap):
    ev=identity['accepted_creator_identity']['enum_values'];td=ev['E_T_DATAINTNUM'];tc=ev['E_T_DATACHARNUM'];ed=ev['ENEMY_DATAINTNUM'];ec=ev['ENEMY_DATACHARNUM']
    temps=[];ints=[-1]*td;chars=[b'']*tc
    for line in input_lines(profile,temp_bytes):
        tokens=fields(profile,line)
        for i in range(tc):
            if i<len(tokens):chars[i]=tokens[i][:temp_cap-1]
        for i in range(td):
            if tc+i>=len(tokens):break
            if tokens[tc+i]:ints[i]=c_atoi(tokens[tc+i])
        if len(tokens)<tc+td:continue
        temps.append((ints.copy(),chars.copy()));ints=[-1]*td;chars=[b'']*tc
    enemies=[];ints=[-1]*ed;chars=[b'']*ec
    for line in input_lines(profile,enemy_bytes):
        tokens=fields(profile,line)
        if len(tokens)<ec:continue
        for i in range(ec):chars[i]=tokens[i][:enemy_cap-1]
        for i in range(ed):
            if ec+i>=len(tokens):break
            ints[i]=c_atoi(tokens[ec+i])
        if len(tokens)<ec+ed:continue
        ti=next((j for j,(t,_c) in enumerate(temps) if t[ev['E_T_TEMPNO']]==ints[ev['ENEMY_TEMPNO']]),-1)
        if ti<0:continue
        lo=ints[ev['ENEMY_LV_MIN']];hi=ints[ev['ENEMY_LV_MAX']]
        if lo==0:lo=hi
        ints[ev['ENEMY_LV_MIN']]=min(lo,hi);ints[ev['ENEMY_LV_MAX']]=max(lo,hi)
        enemies.append((ti,ints.copy(),chars.copy()));ints=[-1]*ed;chars=[b'']*ec
    return temps,enemies


def fixture(identity,kind):
    ev=identity['accepted_creator_identity']['enum_values'];td=ev['E_T_DATAINTNUM'];tc=ev['E_T_DATACHARNUM'];ed=ev['ENEMY_DATAINTNUM'];ec=ev['ENEMY_DATACHARNUM']
    def row(chars,values):return b','.join([*chars,*(str(v).encode() if v is not None else b'' for v in values)])+b'\r\n'
    t=[0]*td;t[ev['E_T_TEMPNO']]=11;t[ev['E_T_BASEVITAL']]=25
    t[ev['E_T_BASESTR']]=25;t[ev['E_T_BASETGH']]=25;t[ev['E_T_BASEDEX']]=25
    t[ev['E_T_INITNUM']]=100;t[ev['E_T_LVUPPOINT']]=10;t[ev['E_T_IMGNUMBER']]=100250
    e=[0]*ed;e[ev['ENEMY_ID']]=1;e[ev['ENEMY_TEMPNO']]=11;e[ev['ENEMY_LV_MIN']]=4;e[ev['ENEMY_LV_MAX']]=2;e[ev['ENEMY_EXP']]=-1
    chars=[b'witness']+[b'']*(tc-1);echars=[b'variant',b'opt',b'cond'][:ec]
    if kind=='empty':return b'# comment\n\n',b'# comment\n\n'
    if kind=='valid':return b'# comment\n\n'+row(chars,t),row(echars,e)
    if kind=='partial':
        # Rejected prefix writes survive if the next accepted template leaves an int empty.
        partial=t.copy();partial[ev['E_T_BASEVITAL']]=77
        blank=t.copy();blank[ev['E_T_BASEVITAL']]=None
        orphan=e.copy();orphan[ev['ENEMY_TEMPNO']]=999
        zero=e.copy();zero[ev['ENEMY_LV_MIN']]=0;zero[ev['ENEMY_LV_MAX']]=7
        return row(chars,partial[:8])+row(chars,blank),row(echars,orphan)+row(echars,zero)
    if kind=='duplicate':
        t2=t.copy();t2[ev['E_T_BASEVITAL']]=35
        return row(chars,t)+row([b'second']+[b'']*(tc-1),t2),row(echars,e)
    if kind=='spacing':return b'  '+row(chars,t),b'\t'+row(echars,e)
    raise ValueError(kind)


def specimen(gavin_root):
    setup=gavin_root/'gmsv/setup.cf';raw=setup.read_bytes();names={}
    for k in ('enemybasefile','enemyfile'):
        matches=re.findall(rb'^\s*'+k.encode()+rb'\s*=\s*([^\r\n#]+)',raw,re.M)
        if len(matches)!=1:raise ValueError('configured specimen ambiguity')
        names[k]=matches[0].decode('ascii').strip()
    paths=[(setup.parent/names[k]).resolve() for k in ('enemybasefile','enemyfile')]
    if any(not p.is_relative_to(gavin_root.resolve()) for p in paths):raise ValueError('specimen escapes pinned tree')
    return paths,{'source_sha':PINNED['gavin'],'setup_file':'gmsv/setup.cf','setup_sha256':digest(raw),
                  'files':{p.relative_to(gavin_root).as_posix():digest(p.read_bytes()) for p in paths},
                  'gavin_own_configured_specimen':True,'bismarck_cross_profile_bytes_not_own_historical_data':True}


def provenance(roots):
    """Static object callers and Windows conversion are separate from execution."""
    rows={}
    for profile,root in roots.items():
        if subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()!=PINNED[profile]:
            raise ValueError('provenance source HEAD drift')
        if subprocess.check_output(['git','-C',str(root),'status','--porcelain'],text=True):raise ValueError('dirty provenance source')
        bodies={};files={}
        for path,name in (('char/char.c','CHAR_createCharacter'),('battle/battle.c','BATTLE_CreateVsEnemy'),('object.c','_initObjectOne')):
            p=LAYOUTS[profile]/path;files[str(p)]=digest((root/p).read_bytes());bodies[name]=definition(pp_file(profile,root,p),name)
        rows[profile]={'source_sha':PINNED[profile],'files':files,
            'functions':{n:digest(_compact(b)) for n,b in bodies.items()},
            'static_only_not_transitive_ownership_proof':True,
            'world_constructor_calls_object_allocator_and_writes_character_object_field':
                'initObjectOne' in bodies['CHAR_createCharacter'] and 'CHAR_WORKOBJINDEX' in bodies['CHAR_createCharacter'],
            'object_allocator_calls_MAP_addNewObj':'MAP_addNewObj' in bodies['_initObjectOne'],
            'battle_creation_calls_enemy_creator_and_BATTLE_NewEntry':all(n in bodies['BATTLE_CreateVsEnemy'] for n in ('ENEMY_createEnemy','BATTLE_NewEntry')),
            'battle_creation_direct_character_object_field_writes':len(re.findall(r'CHAR_setWorkInt\s*\([^;]*?CHAR_WORKOBJINDEX',bodies['BATTLE_CreateVsEnemy']))}
    root=roots['iris'];paths=[LAYOUTS['iris']/p for p in ('char/enemy.c','util.c')]
    text=[pp_file('iris',root,p) for p in paths]
    rows['iris']['unexecuted_windows_conversion']={'status':'OPEN','files':{str(p):digest((root/p).read_bytes()) for p in paths},
        'functions':{n:digest(_compact(definition(t,n))) for t,n in ((text[0],'ENEMYTEMP_initEnemy'),(text[0],'ENEMY_initEnemy'),(text[1],'utf8ToBig5'))},
        'Windows_API_dependencies':['MultiByteToWideChar','WideCharToMultiByte'],'conversion_adapter_supplied':False}
    return rows


def eligible(identity,temps,enemies,ride):
    ev=identity['accepted_creator_identity']['enum_values'];out=[]
    mapped={r[0] for r in ride}
    for i,(ti,p,_c) in enumerate(enemies):
        t=temps[ti][0];eid=p[ev['ENEMY_ID']]
        if any(a<=eid<=b for a,b in ((564,580),(739,750),(895,906),(655,720),(859,894),(907,940))):continue
        if p[ev['ENEMY_STYLE']] or any(p[ev['ENEMY_ITEMPROB1']+j] for j in range(10)):continue
        base=[t[ev[n]] for n in ('E_T_BASEVITAL','E_T_BASESTR','E_T_BASETGH','E_T_BASEDEX')]
        if not all(3<=v<=120 for v in base):continue
        if not 1<=t[ev['E_T_INITNUM']]<=10000 or not 0<=t[ev['E_T_LVUPPOINT']]<=10000:continue
        if t[ev['E_T_IMGNUMBER']] in mapped:continue
        out.append(i)
    return out


def f32(v):return struct.unpack('f',struct.pack('f',v))[0]


def birth_expectation(identity,default_data,exps,temp,enemy,level,mode):
    ev=identity['accepted_creator_identity']['enum_values'];t=temp[0];p=enemy[1]
    get=lambda n:t[ev[n]];eg=lambda n:p[ev[n]]
    raw=[get(n) for n in ('E_T_BASEVITAL','E_T_BASESTR','E_T_BASETGH','E_T_BASEDEX')]
    initial=[v+rng_value(mode,0,4)-2 for v in raw];grown=initial.copy();grown[rng_value(mode,0,3)]+=10
    factor=(level-1)*get('E_T_LVUPPOINT')+get('E_T_INITNUM');v,s,h,d=[factor*v for v in grown]
    hp=max(0,min(10000000,int(f32((v*4+s+h+d)*.01))))
    rank=next(j for j,n in enumerate((100,95,90,85,80,0)) if sum(raw)>=n)
    exp=expected_data(identity['accepted_creator_identity']['prior_actual_template'],default_data)[ev['CHAR_EXP']]
    if eg('ENEMY_DUELPOINT')<=0:
        exp=eg('ENEMY_EXP')
        if exp==-1:
            alpha=f32(sum(get(n) for n in ('E_T_CRITICAL','E_T_COUNTER','E_T_GET','E_T_POISON','E_T_PARALYSIS','E_T_SLEEP','E_T_STONE','E_T_DRUNK','E_T_CONFUSION'))/100.0+get('E_T_RARE'))
            exp=max(1,int(f32(exps[level-1]+f32(f32((2.5,2,1.5,1,.5,0)[rank]+alpha)*level))))
    data={'CHAR_VITAL':v,'CHAR_STR':s,'CHAR_TOUGH':h,'CHAR_DEX':d,'CHAR_LV':level,
          'CHAR_ALLOCPOINT':sum(n<<(24-8*j) for j,n in enumerate(initial)),
          'CHAR_HP':hp,'CHAR_EXP':exp,'CHAR_PETRANK':rank,'CHAR_PETID':get('E_T_TEMPNO'),
          'CHAR_BASEIMAGENUMBER':get('E_T_IMGNUMBER'),'CHAR_BASEBASEIMAGENUMBER':get('E_T_IMGNUMBER'),
          'CHAR_WHICHTYPE':ev['CHAR_TYPEENEMY']}
    work={'CHAR_WORKTICKETTIME':0,'CHAR_WORKTICKETTIMESTART':0,'CHAR_WORKOBJINDEX':0,
          'CHAR_WORKMAXHP':hp,'CHAR_WORKTACTICS':eg('ENEMY_TACTICS'),'CHAR_WORK_PETFLG':eg('ENEMY_PETFLG'),
          'CHAR_WORKMODCAPTUREDEFAULT':get('E_T_GET'),'CHAR_WORKFOXROUND':-1}
    return data,work


def native_source(profile,source):
    setup='if(!configmem(64,262144))return 11;' if profile=='gavin' else 'sUnitSize=64;sUnitNumTotal=262144;'
    return source+r'''
static void hex(const char *s){if(!*s){printf("-");return;}for(;*s;s++)printf("%02x",(unsigned char)*s);}
int main(int argc,char **argv){
 if(argc!=3 || sizeof(void*)!=8 || sizeof(int)!=4)return 10;
'''+setup+r'''
 if(!memInit())return 12;
 int a=ENEMYTEMP_initEnemy(argv[1]),b=ENEMY_initEnemy(argv[2]);
 printf("H %d %d %d %d %zu %zu\n",a,b,ENEMYTEMP_enemynum,ENEMY_enemynum,sizeof(ENEMYTEMP_enemy[0].chardata[0].string),sizeof(ENEMY_enemy[0].chardata[0].string));
 for(int i=0;i<ENEMYTEMP_enemynum;i++){
  printf("T %d",i);for(int j=0;j<E_T_DATAINTNUM;j++)printf(" %d",ENEMYTEMP_enemy[i].intdata[j]);
  for(int j=0;j<E_T_DATACHARNUM;j++){printf(" ");hex(ENEMYTEMP_enemy[i].chardata[j].string);}printf("\n");
 }
 for(int i=0;i<ENEMY_enemynum;i++){
  printf("E %d %d",i,ENEMY_enemy[i].enemytemparray);for(int j=0;j<ENEMY_DATAINTNUM;j++)printf(" %d",ENEMY_enemy[i].intdata[j]);
  for(int j=0;j<ENEMY_DATACHARNUM;j++){printf(" ");hex(ENEMY_enemy[i].chardata[j].string);}printf("\n");
 }
 int array,level,mode;
 while(scanf("%d%d%d",&array,&level,&mode)==3){
  memset(slots,0xa5,sizeof(slots));for(int i=0;i<7;i++)slots[i].use=1;slots[4].use=0;
  initCharCounter[2]=(INITCHARCOUNTER){.startcnt=4,.cnt=4,.endcnt=7};
  rng_mode=mode;rng_count=lookup_count=diagnostics=0;
  int result=ENEMY_createEnemy(array,level);
  if(result!=4)return 13;
  Char *ch=&slots[result];printf("B %d %d %d %d %d %d",array,level,mode,result,rng_count,ch->CharMakeSequenceNumber);
  for(int j=0;j<CHAR_DATAINTNUM;j++)printf(" %d",ch->data[j]);
  for(int j=0;j<CHAR_WORKDATAINTNUM;j++)printf(" %d",ch->workint[j]);
  printf(" ");hex(ch->string[CHAR_NAME].string);printf("\n");
 }
 memEnd();return 0;
}
'''


def compile_probe(profile,root,source,exe,opt):
    source+=trap_definitions(profile,root,source,json.loads(PIN_PATH.read_text())['profiles'][profile]['identity']['unreachable_traps'])
    result=subprocess.run(['cc','-std=gnu99','-fgnu89-inline',opt,'-fsanitize=undefined','-fno-sanitize-recover=all',
                          *include_args(profile,root),'-x','c','-','-o',str(exe)],input=source,text=True,capture_output=True)
    if result.returncode:raise ValueError(result.stderr[-12000:])


def mutations(profile,root,source,identity,default_data,exps,ride,paths,tmp):
    """Each functional mutation must compile/run cleanly and fail the oracle."""
    target='ENEMY_initEnemy' if profile=='gavin' else 'enemy_callback'
    body=definition(source,target)
    link=re.search(r'(ENEMY_enemy\[[^;]+?\]\.enemytemparray\s*=\s*)i\s*;',body)
    if not link:raise ValueError('loader link statement drift')
    linked=body[:link.start()]+link[1]+'i+1;'+body[link.end():]
    counter=re.search(r'enemy_readlen\s*\+\+\s*;',body) if profile=='gavin' else re.search(r'\+\+\s*\(\s*\*line_num\s*\)\s*;',body)
    if not counter:raise ValueError('loader acceptance counter drift')
    index='enemy_readlen' if profile=='gavin' else '*line_num'
    normalized=body[:counter.start()]+f'ENEMY_setInt({index},ENEMY_LV_MIN,ENEMY_getInt({index},ENEMY_LV_MIN)+1);'+body[counter.start():]
    target_t='ENEMYTEMP_initEnemy' if profile=='gavin' else 'enemytemp_callback'
    template_body=definition(source,target_t)
    changed,n=re.subn(r'if\s*\(\s*strlen\(\s*token\s*\)\s*!=\s*0\s*\)', 'if(1)',template_body)
    if n!=1:raise ValueError('template empty-cell guard drift')
    trials=[('link',source.replace(body,linked,1),'duplicate'),('level',source.replace(body,normalized,1),'duplicate'),
            ('empty-cell',source.replace(template_body,changed,1),'partial')]
    creator=definition(source,'ENEMY_createEnemy');final=re.search(r'return\s+(\w+)\s*;\s*}$',creator)
    if not final:raise ValueError('creator final return drift')
    for name in ('CHAR_WORKTICKETTIME','CHAR_WORKTICKETTIMESTART','CHAR_WORKOBJINDEX'):
        injection=f'CHAR_setWorkInt({final[1]},{name},1);'
        trials.append((name,source.replace(creator,creator[:final.start()]+injection+creator[final.start():],1),'preserved'))
    for name,mutant,kind in trials:
        if kind=='preserved':
            tb,eb=[p.read_bytes() for p in paths];temps,enemies=loaded_oracle(profile,identity,tb,eb,32,32)
            cases=[(eligible(identity,temps,enemies,ride)[0],20,1)]
        else:tb,eb=fixture(identity,kind);cases=[]
        tp=tmp/'mutant-template.txt';ep=tmp/'mutant-enemy.txt';tp.write_bytes(tb);ep.write_bytes(eb)
        exe=tmp/'mutant';compile_probe(profile,root,native_source(profile,mutant),exe,'-O0')
        r=subprocess.run([str(exe),str(tp),str(ep)],input=''.join(' '.join(map(str,c))+'\n' for c in cases),text=True,capture_output=True)
        if r.returncode or r.stderr:raise ValueError('unsafe mutant '+name+': '+r.stderr)
        try:verify_output(profile,identity,default_data,exps,tb,eb,r.stdout,cases)
        except ValueError as error:
            if 'complete loaded records mismatch' not in str(error) and 'birth ' not in str(error):raise
        else:raise ValueError('undetected mutation '+name)
    return len(trials)


def verify_output(profile,identity,default_data,exps,temp_bytes,enemy_bytes,output,cases):
    lines=[l.split() for l in output.splitlines() if l[:2] in ('H ','T ','E ','B ')]
    h=lines[0];tr,er,tn,en,tc,ec=map(int,h[1:]);temps,enemies=loaded_oracle(profile,identity,temp_bytes,enemy_bytes,tc,ec)
    if (tr,er,tn,en)!=(int(bool(list(input_lines(profile,temp_bytes)))),int(bool(list(input_lines(profile,enemy_bytes)))) ,len(temps),len(enemies)):
        raise ValueError(f'{profile}: loader status/count mismatch {h}')
    ev=identity['accepted_creator_identity']['enum_values'];td=ev['E_T_DATAINTNUM'];ed=ev['ENEMY_DATAINTNUM'];nd=ev['CHAR_DATAINTNUM'];nw=ev['CHAR_WORKDATAINTNUM']
    expected=[]
    for i,(ints,chars) in enumerate(temps):expected.append(['T',str(i),*map(str,ints),*(c.hex() or '-' for c in chars)])
    for i,(ti,ints,chars) in enumerate(enemies):expected.append(['E',str(i),str(ti),*map(str,ints),*(c.hex() or '-' for c in chars)])
    actual=[l for l in lines if l[0] in ('T','E')]
    if actual!=expected:
        difference=next((i for i,(a,b) in enumerate(zip(actual,expected)) if a!=b),min(len(actual),len(expected)))
        raise ValueError(f'{profile}: complete loaded records mismatch at {difference}: {actual[difference:difference+1]} != {expected[difference:difference+1]}')
    births=[l for l in lines if l[0]=='B']
    if len(births)!=len(cases):raise ValueError('birth cardinality mismatch')
    for sequence,(line,(index,level,mode)) in enumerate(zip(births,cases)):
        if list(map(int,line[1:7]))!=[index,level,mode,4,14,sequence]:raise ValueError('birth control state mismatch')
        data=list(map(int,line[7:7+nd]));work=list(map(int,line[7+nd:7+nd+nw]))
        want_d,want_w=birth_expectation(identity,default_data,exps,temps[enemies[index][0]],enemies[index],level,mode)
        for name,value in want_d.items():
            if data[ev[name]]!=value:raise ValueError(f'{profile} birth {index}: {name} {data[ev[name]]}!={value}')
        for name,value in want_w.items():
            if work[ev[name]]!=value:raise ValueError(f'{profile} birth {index}: {name} {work[ev[name]]}!={value}')
        if line[-1]!=(temps[enemies[index][0]][1][0][:31].hex() or '-'):raise ValueError('birth name mismatch')
    return len(temps),len(enemies),len(births)


def audit(profile,root,paths,receipt):
    if subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()!=PINNED[profile] or subprocess.check_output(['git','-C',str(root),'status','--porcelain'],text=True):raise ValueError('source pin/cleanliness drift')
    source,identity,data,flags,exps,ride=domain(profile,root)
    if identity!=json.loads(PIN_PATH.read_text())['profiles'][profile]['identity']:raise ValueError('loader identity drift')
    inputs=[(name,*fixture(identity,name)) for name in ('valid','partial','duplicate','spacing','empty')]
    inputs.append(('preserved-configured-gavin',paths[0].read_bytes(),paths[1].read_bytes()))
    totals=[0,0,0];reference=[]
    with tempfile.TemporaryDirectory(prefix='stoneage-loader-') as tmp:
        tmp=Path(tmp)
        for opt in ('-O0','-O2'):
            exe=tmp/('probe'+opt);compile_probe(profile,root,native_source(profile,source),exe,opt)
            observed=[];counts=[0,0,0]
            for name,tbytes,ebytes in inputs:
                tp=tmp/'enemybase.txt';ep=tmp/'enemy.txt';tp.write_bytes(tbytes);ep.write_bytes(ebytes)
                temps,enemies=loaded_oracle(profile,identity,tbytes,ebytes,32,32)
                # Only preserved source bytes supply birth witnesses; controlled fixtures audit loading.
                selected=eligible(identity,temps,enemies,ride) if name.startswith('preserved') else []
                cases=[(i,level,mode) for i in selected for level in (1,20) for mode in range(4)]
                payload=''.join(' '.join(map(str,c))+'\n' for c in cases)
                r=subprocess.run([str(exe),str(tp),str(ep)],input=payload,text=True,capture_output=True)
                if r.returncode or r.stderr:raise ValueError(r.stderr+' rc='+str(r.returncode))
                n=verify_output(profile,identity,data,exps,tbytes,ebytes,r.stdout,cases)
                counts=[a+b for a,b in zip(counts,n)];observed.append(r.stdout)
            if reference and observed!=reference:raise ValueError('optimization-dependent loading/birth state')
            reference=observed;totals=[a+b for a,b in zip(totals,counts)]
        rejected=mutations(profile,root,source,identity,data,exps,ride,paths,tmp)
    return {'profile':profile,'source_sha':PINNED[profile],'loader_scenarios_per_optimization':len(inputs),
            'loaded_template_comparisons':totals[0],'loaded_enemy_comparisons':totals[1],
            'preserved_ordinary_birth_calls':totals[2],'semantic_mutations_rejected':rejected,'semantic_sha256':digest(''.join(reference))}


def main():
    parser=argparse.ArgumentParser()
    for p in PINNED:parser.add_argument('--'+p+'-dir',type=Path,required=True)
    args=parser.parse_args();roots={p:getattr(args,p+'_dir') for p in PINNED}
    if provenance(roots)!=json.loads(PIN_PATH.read_text())['static_provenance']:raise ValueError('static provenance drift')
    paths,receipt=specimen(roots['gavin'])
    if receipt!=json.loads(PIN_PATH.read_text())['preserved_specimen']:raise ValueError('preserved specimen drift')
    totals=[0,0,0]
    for p in PROFILES:
        row=audit(p,roots[p],paths,receipt);totals=[a+row[k] for a,k in zip(totals,('loaded_template_comparisons','loaded_enemy_comparisons','preserved_ordinary_birth_calls'))]
        print('PROFILE|'+'|'.join(f'{k}={v}' for k,v in row.items()),flush=True)
    print(f'TOTAL|loaded_template_comparisons={totals[0]}|loaded_enemy_comparisons={totals[1]}|preserved_ordinary_birth_calls={totals[2]}|executed_profiles=2')
    print('MUTATIONS|semantic_mutations_rejected=12|loader_link_level_empty_cell_and_birth_ticket_start_object|additional_birth_calls=6')
    print('FACT|actual_file_loaders_original_pool_tokenizers_sets_links_level_normalization_and_ordinary_birth_helpers_execute')
    print('FACT|partial_template_empty_cells_retain_rejected_prefix_duplicate_tempno_maps_first_ordinary_birth_ticket_start_object_zero')
    print('BOUNDARY|same_pin_gavin_configured_data_bismarck_cross_profile_plaintext_LP64_controlled_pool_no_equipment_or_special_births')
    print('STATIC|world_constructor_allocates_object_battle_entry_reads_player_party_objects_without_direct_enemy_object_write_not_ownership_proof')
    print('OPEN|iris_Windows_encoding_encrypted_files_object_registration_ownership_full_Exit_reuse_original_build_JSS_Taiwan_v1')
    print('RESOLUTION|'+RESOLUTION)


if __name__=='__main__':main()
