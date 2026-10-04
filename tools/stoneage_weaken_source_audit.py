"""Audit pinned Weaken sources; compile original functions only transiently."""
import argparse
import os
from pathlib import Path
import random
import re
import subprocess
import tempfile

from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS, _sha, _text
from tools.stoneage_mdfyattack_source_audit import _definition, _strip
from tools.stoneage_weaken_model import (
    WeakenCheckInputs, parse_weaken_option, resolve_weaken_target, resolve_weaken_recalculation,
)


def _array(text, name):
    match = re.search(r'(?:char\s*\*|int)\s*' + name +
                      r'\s*\[\s*\]\s*=\s*\{.*?\};', text, re.S)
    if not match:
        raise ValueError('missing source array: ' + name)
    return match.group(0)


def _preprocess(source, includes, version):
    return subprocess.run(['cpp', '-P', *includes, '-imacros', str(version), '-'],
                          input=source, text=True, capture_output=True, check=True).stdout


def _enum_values(names, includes):
    code = ('#include <stdio.h>\n#include "char_base.h"\n#include "battle.h"\n'
            '#include "battle_event.h"\n#include "pet_skill.h"\n#include "pet_skillinfo.h"\nint main(void){\n')
    code += ''.join('printf("%d\\n",' + n + ');\n' for n in names) + 'return 0;}\n'
    with tempfile.TemporaryDirectory() as directory:
        p = Path(directory)
        (p / 'enum.c').write_text(code)
        result = subprocess.run(['cc', '-w', *includes, str(p / 'enum.c'), '-o', str(p / 'enum')],
                                capture_output=True, text=True)
        if result.returncode:
            raise ValueError('enum compilation failed: ' + result.stderr[-2500:])
        values = list(map(int, subprocess.check_output([str(p / 'enum')], text=True).split()))
    return dict(zip(names, values))


def _oracle(source, enums, marker, packed_macro):
    prefix = r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#define BOOL int
#define TRUE 1
#define FALSE 0
#define arraysizeof(a) (sizeof(a)/sizeof((a)[0]))
#define MAGIC_EFFECT_USER 9
#define SPR_hoshi 10
#define SPR_tyusya 11
static int works[2][4096], stats[2][256], draws, die_roll;
static char *option;
static struct {int type;} BattleArray[1];
int CHAR_getWorkInt(int index,int pos){return works[index][pos];}
int CHAR_getInt(int index,int pos){return stats[index][pos];}
void CHAR_setWorkInt(int index,int pos,int value){works[index][pos]=value;}
char *PETSKILL_getChar(int array,int pos){return option;}
int BATTLE_No2Index(int battle,int slot){return slot;}
void BATTLE_MultiList(int battle,int slot,int *list){list[0]=1;list[1]=-1;}
void BATTLE_MagicEffect(int battle,int actor,int *list,int a,int b){}
int print(const char *format,...){return 0;}
int RAND(int low,int high){draws++;return die_roll;}
'''
    prefix += '\n'.join('#define ' + n + ' ' + str(v) for n, v in enums.items()) + '\n'
    main = r'''
int main(int argc,char **argv){
  if(argc==2){
    option=argv[1];
    int ok=PETSKILL_Weaken(0,8,23,NULL);
    works[0][CHAR_WORKBATTLECOM3]=works[0][CHAR_WORKBATTLECOM3]&65535;
    int ret=BATTLE_S_Weaken(0,0,1,23);
    printf("%d %d %d %d %d %d %d\n",ok,works[0][CHAR_WORKBATTLECOM1],
      works[0][CHAR_WORKBATTLECOM2],works[0][CHAR_WORKBATTLECOM3],
      ret,draws,works[1][CHAR_WORKWEAKEN]);return 0;
  }
  if(argc==3){
    int a,b,c,w,bar;
    while(scanf("%d%d%d%d%d",&a,&b,&c,&w,&bar)==5){
      memset(works,0,sizeof(works));memset(stats,0,sizeof(stats));
      works[0][CHAR_WORKFIXSTR]=a;works[0][CHAR_WORKFIXTOUGH]=b;works[0][CHAR_WORKFIXDEX]=c;
      works[0][CHAR_WORKWEAKEN]=w;works[0][CHAR_WORKBARRIER]=bar;
      Other_DefcharWorkInt(0);
      printf("%d %d %d %d %d %d %d %d\n",works[0][CHAR_WORKFIXSTR],
        works[0][CHAR_WORKFIXTOUGH],works[0][CHAR_WORKFIXDEX],works[0][CHAR_WORKWEAKEN],
        works[0][CHAR_WORKBARRIER],works[0][CHAR_WORKATTACKPOWER],
        works[0][CHAR_WORKDEFENCEPOWER],works[0][CHAR_WORKQUICK]);
    }return 0;
  }
  int al,dl,pvp,luck,v,s,t,d,res,suit,active,roll,success,turn,kind;
  while(scanf("%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d",
      &al,&dl,&pvp,&luck,&v,&s,&t,&d,&res,&suit,&active,&roll,&success,&turn,&kind)==15){
    memset(works,0,sizeof(works));memset(stats,0,sizeof(stats));draws=0;die_roll=roll;
    stats[0][CHAR_LV]=al;stats[1][CHAR_LV]=dl;
    stats[1][CHAR_VITAL]=v;stats[1][CHAR_STR]=s;stats[1][CHAR_TOUGH]=t;stats[1][CHAR_DEX]=d;
    stats[1][CHAR_WHICHTYPE]=kind;
    works[0][CHAR_WORKFIXLUCK]=luck;works[1][CHAR_WORKMODWEAKEN]=res;
    works[1][CHAR_WORKRESIST]=suit;
    // These named equipment fields must not be charged for status index 7.
#ifdef CHAR_WORKEQUITWEAKEN
    works[1][CHAR_WORKEQUITWEAKEN]=700;
#endif
#ifdef CHAR_WORKRENOCAST
    works[1][CHAR_WORKRENOCAST]=900;
#endif
    if(active)works[1][CHAR_WORKPOISON]=2;
    BattleArray[0].type=pvp?BATTLE_TYPE_P_vs_P:0;
    int per=-999;
    int hit=BATTLE_StatusAttackCheck(0,1,BATTLE_ST_WEAKEN,success,30,1.0,&per);
    printf("%d %d %d\n",per,draws,hit);
    if(hit){
      // Full shared writer calls the same checker once; separate its RNG witness.
      draws=0;BATTLE_MultiParamChangeTurn(0,0,1,BATTLE_ST_WEAKEN,9,10,turn,success);
      printf("%d\n",works[1][CHAR_WORKWEAKEN]);
    }else printf("-999\n");
  }
  return 0;
}
'''
    options = [marker + ' turn=3 成=50', marker + ' turn=5 成=70',
               marker + ' turn=abc 成=55', marker + ' turn=3',
               marker + ' turn=12 成=abc', marker + ' turn=345 成=70',
               marker + ' 成=90 turn=3', marker + ' turn=3 成=+9tail']
    rng = random.Random(575576)
    cases = []
    for _ in range(512):
        inp = WeakenCheckInputs(rng.randrange(1,150), rng.randrange(1,150), bool(rng.randrange(2)),
            rng.randrange(61), *(rng.randrange(1,10001) for _ in range(4)),
            rng.randrange(61), rng.randrange(41), bool(rng.randrange(4)==0),
            rng.choice(('player','pet','enemy')))
        cases.append((inp,rng.randrange(1,101),rng.randrange(101),rng.randrange(1,8)))
    sanitizer_env = dict(os.environ, ASAN_OPTIONS='detect_leaks=0')
    with tempfile.TemporaryDirectory() as directory:
        p = Path(directory)
        (p / 'oracle.c').write_text(prefix + packed_macro + '\n' + source + '\n' + main)
        result = subprocess.run(['cc','-w','-O0','-fsanitize=undefined,address',
            '-fno-sanitize-recover=all',str(p / 'oracle.c'),'-o',str(p / 'oracle')],
            capture_output=True,text=True)
        if result.returncode:
            raise ValueError('oracle compilation failed: ' + result.stderr[-3000:])
        for text in options:
            raw = text.encode('utf-8')
            option_model = parse_weaken_option(raw,encoding='utf-8',simplified_utf8=marker=='虚')
            # Choose fixed equal stats, luck 60, so positive options hit.
            # Missing success retains zero; the negative probability misses.
            # Defaults in the native argv path are set below in its prefix.
            expected = resolve_weaken_target(WeakenCheckInputs(1,1,False,60,100,100,100,100,
                0,0,False,'player'),option_model,roll_1_100=1)
            output = subprocess.check_output([str(p / 'oracle'),text],text=True,env=sanitizer_env)
            actual = tuple(map(int,output.split()))
            wanted = (1,enums['BATTLE_COM_S_WEAKEN'],8,23,0,1,expected.counter_written or 0)
            if actual != wanted:
                raise ValueError(f'callback/executor oracle mismatch: {actual} != {wanted}')
        lines=[]
        for inp,roll,success,turn in cases:
            kind=enums['CHAR_TYPE'+inp.target_kind.upper()]
            lines.append(' '.join(map(str,(inp.attacker_level,inp.defender_level,int(inp.pvp),
                inp.attacker_fixed_luck,inp.defender_vital,inp.defender_strength,
                inp.defender_toughness,inp.defender_dexterity,inp.defender_mod_weaken,
                inp.defender_suit_resist,int(inp.any_existing_status),roll,success,turn,kind))))
        result = subprocess.run([str(p / 'oracle')],input='\n'.join(lines)+'\n',
                                capture_output=True,text=True,check=True,env=sanitizer_env)
        values=list(map(int,result.stdout.split()))
        if len(values)!=4*len(cases):
            raise ValueError('oracle witness count drift')
        for n,(inp,roll,success,turn) in enumerate(cases):
            from tools.stoneage_weaken_model import WeakenOption
            expected=resolve_weaken_target(inp,WeakenOption(turn,success),
                roll_1_100=None if inp.any_existing_status else roll)
            wanted=(expected.probability_value if expected.probability_value is not None else -999,
                    int(expected.rng_consumed),int(expected.hit_check_succeeded),
                    expected.counter_written if expected.counter_written is not None else -999)
            if tuple(values[4*n:4*n+4])!=wanted:
                raise ValueError('native probability/shared-writer mismatch at case '+str(n))
        recalcs=[(n,n,n,w,b) for n,w,b in ((0,0,0),(1,1,0),(5,2,1),(105,3,2),
                                                  (2147483647,1,1),(2147483647,0,0))]
        for _ in range(122):
            recalcs.append((rng.randrange(100001),rng.randrange(100001),rng.randrange(100001),
                            rng.randrange(8),rng.randrange(8)))
        result=subprocess.run([str(p/'oracle'),'--recalc','fixture'],
            input='\n'.join(' '.join(map(str,x)) for x in recalcs)+'\n',
            capture_output=True,text=True,check=True,env=sanitizer_env)
        actuals=list(map(int,result.stdout.split()))
        if len(actuals)!=8*len(recalcs):
            raise ValueError('recalculation oracle witness count drift')
        for n,(a,b,c,w,bar) in enumerate(recalcs):
            out=resolve_weaken_recalculation(a,b,c,weaken_counter=w,barrier_counter=bar)
            powers=(out.strength,out.toughness,out.dexterity)
            if tuple(actuals[8*n:8*n+8])!=(*powers,out.weaken_counter,out.barrier_counter,*powers):
                raise ValueError('native recalculation mismatch at case '+str(n))
    return {'recalculation_cases':len(recalcs),'callback_executor_cases':len(options),'probability_writer_cases':len(cases),
            'ubsan_asan_pass':True}


def analyze_profile(name, root):
    root=Path(root).resolve()
    actual=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()
    if actual!=PINNED[name] or subprocess.check_output(
            ['git','-C',str(root),'status','--porcelain'],text=True).strip():
        raise ValueError('pinned clean source identity failed: '+name)
    base=root/LAYOUTS[name]
    paths={k:base/v for k,v in {'pet':'battle/pet_skill.c','event':'battle/battle_event.c',
        'magic':'battle/battle_magic.c','battle':'battle/battle.c','version':'include/version.h',
        'char':'include/char_base.h','bh':'include/battle.h','eh':'include/battle_event.h',
        'ph':'include/pet_skillinfo.h','item':'item/item.c','char_c':'char/char.c'}.items()}
    data={k:_text(v) for k,v in paths.items()}
    includes=['-I',str(base/'include')]
    if name=='bismarck':
        includes += ['-I',str(root/'server/common'),'-I',str(root/'shared/lua51')]
    definitions=subprocess.check_output(['cpp','-dM',*includes,str(paths['version'])],text=True)
    active=set(re.findall(r'^#define\s+(\w+)\b',definitions,re.M))
    features={x:x in active for x in ('_SKILL_WEAKEN','_MAGIC_WEAKEN','_MAGIC_BARRIER',
              '_MAGIC_NOCAST','_SUIT_ADDENDUM','_EQUIT_RESIST','_SUIT_ADDPART3','_MO_LUA_RESIST')}
    functions=[_definition(data['pet'],'PETSKILL_Weaken'),
        _definition(data['event'],'BATTLE_StatusAttackCheck'),
        _definition(data['magic'],'BATTLE_MultiParamChangeTurn'),
        _definition(data['event'],'BATTLE_S_Weaken'),
        _definition(data['item'],'Other_DefcharWorkInt')]
    arrays=[_array(data['event'],n) for n in ('aszStatus','StatusTbl','RegTbl')]
    # Inject explicit RAND(1,100) witness after profile preprocessing.
    source=_preprocess('#undef RAND\n'+'\n'.join(arrays+functions),includes,paths['version'])
    names=sorted(set(re.findall(r'\b(?:CHAR_[A-Z_0-9]+|BATTLE_ST_[A-Z_0-9]+|'
        r'BATTLE_COM_S_WEAKEN|BATTLE_CHARMODE_C_OK|BATTLE_TYPE_P_vs_P|PETSKILL_OPTION)\b',source)))
    names=[n for n in names if n != 'CHAR_SETWORKINT_LOW']
    names=sorted(set(names+['SIDE_OFFSET','BATTLE_ST_WEAKEN','CHAR_TYPEPLAYER',
                           'CHAR_TYPEPET','CHAR_TYPEENEMY','PETSKILL_WEAKEN']))
    enums=_enum_values(names,includes)
    compact=re.sub(r'\s+','',_strip(source))
    callback=re.sub(r'\s+','',_strip(functions[0]))
    status_seq=re.sub(r'\s+','',_strip(_definition(data['battle'],
        'BATTLE_StatusSeq',raw_window=True))).replace('char_index','charaindex')
    dispatch=re.sub(r'\s+','',_strip(data['battle']))
    dispatch=dispatch[dispatch.index('caseBATTLE_COM_S_WEAKEN:'):][:600]
    gates={
        'skill_magic_features_active':features['_SKILL_WEAKEN'] and features['_MAGIC_WEAKEN'],
        'callback_command_target_mode_low_array':all(x in callback for x in (
            'BATTLE_COM_S_WEAKEN','CHAR_WORKBATTLECOM2','BATTLE_CHARMODE_C_OK','CHAR_SETWORKINT_LOW')),
        'callback_no_power_mutation':all(x not in callback for x in (
            'CHAR_WORKATTACKPOWER','CHAR_WORKDEFENCEPOWER','CHAR_WORKQUICK')),
        'dispatch_direct_com2_without_targetadjust':'CHAR_WORKBATTLECOM2' in dispatch
            and 'BATTLE_S_Weaken' in dispatch and 'BATTLE_TargetAdjust' not in dispatch,
        'leading_status_scan_two_bytes':'strncmp(pszP,aszStatus[i],2)' in compact,
        'turn_initialized_three':'turn=3' in compact,
        'shared_writer_turn_plus_one':'CHAR_WORKWEAKEN,turn+1' in compact,
        'shared_writer_no_pet_exclusion':'CHAR_WHICHTYPE' not in
            re.sub(r'\s+','',_strip(functions[2])),
        'status_index_not_equipment_work_enum':enums['BATTLE_ST_WEAKEN']!=enums['CHAR_WORKWEAKEN'],
        'status_order_weaken_before_barrier_nocast':
            'CHAR_WORKWEAKEN,CHAR_WORKDEEPPOISON,CHAR_WORKBARRIER,CHAR_WORKNOCAST' in
            re.sub(r'\s+','',_strip(arrays[1])),
        'decrement_before_weaken_freeze':0 <= status_seq.find('StatusTbl[i],--cnt') <
            status_seq.find('CHAR_WORKWEAKEN)>0') < status_seq.find('StatusTbl[i],cnt+1'),
        'executor_keeps_false_return':all(x in re.sub(r'\s+','',_strip(functions[3])) for x in ('BOOLiRet=FALSE','returniRet;')),
        'compliance_calls_recalc_after_base_equipment':
            'Other_DefcharWorkInt(index)' in re.sub(r'\s+','',_strip(data['char_c']))
            and 'CHAR_initcharWorkInt(index)' in re.sub(r'\s+','',_strip(data['char_c'])),
        'recalc_three_power_reductions_and_counter_decrement':all(x in
            re.sub(r'\s+','',_strip(functions[-1])) for x in (
                'CHAR_WORKFIXSTR)*0.8','CHAR_WORKFIXTOUGH)*0.8','CHAR_WORKFIXDEX)*0.8',
                'CHAR_WORKWEAKEN)-1','CHAR_WORKBARRIER)-1')),
        'lua_extra_resist_inactive':not features['_MO_LUA_RESIST'],
    }
    if not all(gates.values()):
        raise ValueError('Weaken source gates failed: '+repr({k:v for k,v in gates.items() if not v}))
    packed=re.search(r'^\s*#define\s+CHAR_SETWORKINT_LOW(?:[^\n]*\\\n)*[^\n]*',data['bh'],re.M)
    if packed is None:
        raise ValueError('packed work macro missing')
    # Some extended profiles have aszStatus shorter than END. Do not
    # run arbitrary/no-match scans; the admitted leading marker stops at 7.
    marker='虛' if name=='iris' else '虚'
    oracle_source=source
    # Initialize standalone fixture before native callback/executor, not source.
    # Insert into harness main with a dedicated synthetic fixture initializer.
    oracle_source += '\nstatic void initialize_fixture(void) __attribute__((constructor));\n'
    oracle_source += ('static void initialize_fixture(void){die_roll=1;'
        'works[0][CHAR_WORKFIXLUCK]=60;stats[0][CHAR_LV]=stats[1][CHAR_LV]=1;'
        'stats[1][CHAR_VITAL]=stats[1][CHAR_STR]=stats[1][CHAR_TOUGH]=stats[1][CHAR_DEX]=100;}\n')
    oracle=_oracle(oracle_source,enums,marker,packed.group(0))
    oracle['status_label_count']=len(re.findall(r'"[^"]*"',_array(source,'aszStatus')))
    oracle['status_work_count']=len(re.findall(r'CHAR_WORK[A-Z_0-9]+',_array(source,'StatusTbl')))+1
    return {'name':name,'sha':actual,'features':features,'gates':gates,'enums':enums,
            'oracle':oracle,'hashes':[(str(p.relative_to(root)),_sha(p)) for p in paths.values()]}


def emit(results):
    print('StoneAge pinned descendant Weaken source audit — R1')
    print('Derived hashes/profile facts only; no original source or OPTION rows stored.')
    print('Leading WEAKEN-marker and no-Lua-extra-resistance domain only; numeric recovered COM1 unassigned.')
    for r in results:
        print(f"PROFILE|name={r['name']}|sha={r['sha']}")
        for k,v in r['features'].items():
            print(f"FEATURE|profile={r['name']}|name={k}|active={int(v)}")
        for k in ('BATTLE_ST_WEAKEN','CHAR_WORKWEAKEN','BATTLE_COM_S_WEAKEN','PETSKILL_WEAKEN','BATTLE_ST_END'):
            print(f"ENUM|profile={r['name']}|name={k}|value={r['enums'][k]}")
        for k,v in r['gates'].items():
            print(f"GATE|profile={r['name']}|name={k}|pass={int(v)}")
        for k,v in r['oracle'].items():
            print(f"ORACLE|profile={r['name']}|name={k}|value={int(v)}")
        for p,h in r['hashes']:
            print(f"SOURCE_HASH|profile={r['name']}|path={p}|sha256={h}")
    print('RESOLUTION|WEAKEN_FIXED_SOURCE_CLOSED_SAFE_REFERENCE')


def main():
    parser=argparse.ArgumentParser()
    for name in PINNED:
        parser.add_argument('--'+name+'-dir',type=Path,required=True)
    args=parser.parse_args()
    emit([analyze_profile(n,getattr(args,n+'_dir')) for n in PINNED])


if __name__=='__main__':
    main()
