"""Fixed-descendant Modifyattack audit with transient native witnesses."""
import argparse
from pathlib import Path
import random
import re
import subprocess
import tempfile

from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS, _text, _sha, _compact
from tools.stoneage_mdfyattack_source_audit import _definition, _strip
from tools.stoneage_weaken_source_audit import _enum_values
from tools.stoneage_modifyattack_reference_model import (
    CALLBACK_NAME, COMMAND_NAME, FEATURE_NAME,
    parse_modifyattack_option, modifyattack_helper_damage,
)


def _native_oracle(data):
    prefix = r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define BOOL int
#define TRUE 1
#define FALSE 0
#define min(a,b) ((a)<(b)?(a):(b))
#define IS_2BYTEWORD(x) ((unsigned char)(x)>=128)
#define strncpy2 strncpy
#define CHAR_WORKBATTLECOM1 0
#define CHAR_WORKBATTLECOM2 1
#define CHAR_WORKBATTLEMODE 2
#define CHAR_WORKBATTLECOM3 3
#define BATTLE_COM_S_MODIFYATT 7
#define BATTLE_CHARMODE_C_OK 3
#define PETSKILL_OPTION 0
#define CHAR_EARTHAT 0
#define CHAR_WATERAT 1
#define CHAR_FIREAT 2
#define CHAR_WINDAT 3
static int works[4], attrs[4], draw_value, draws;
static char *option;
int CHAR_getWorkInt(int index,int pos){return works[pos];}
void CHAR_setWorkInt(int index,int pos,int value){works[pos]=value;}
int CHAR_getInt(int index,int pos){return attrs[pos];}
char *PETSKILL_getChar(int index,int pos){return option;}
int oracle_rand(void){draws++;return draw_value;}
#define rand oracle_rand
#define getStringFromIndexWithDelim(s,d,i,b,n) getStringFromIndexWithDelim_body(s,d,i,b,n,"oracle",0)
'''
    macros=[]
    for name in ('CHAR_SETWORKINT_LOW',):
        match=re.search(r'^\s*#define\s+'+name+r'(?:[^\n]*\\\n)*[^\n]*',data['battle_h'],re.M)
        if not match:
            raise ValueError('missing packed-work macro')
        macros.append(match.group(0))
    if 'workspace' in data:
        prefix += '\n#undef getStringFromIndexWithDelim\n#define getStringFromIndexWithDelim(s,d,i,b,n) GeneralSplitImpl(s,d,i,b,n,"oracle",0)\n'
        functions=[_definition(data['workspace'], n) for n in ('strncpysafe','strncpysafe2')]
        functions += [_definition(data['util'],n) for n in ('strstr_onebyte','GeneralSplitImpl')]
    else:
        functions=[_definition(data['util'],n) for n in ('strcpysafe','strncpysafe','ScanOneByte','getStringFromIndexWithDelim_body')]
    functions += [_definition(data['pet'],CALLBACK_NAME), _definition(data['event'],'BATTLE_S_Modifyattack')]
    main=r'''
int main(int argc,char **argv){
  if(argc<2)return 2;
  option=argv[1];
  works[3]=0x12340000;
  int ok=PETSKILL_Modifyattack(0,17,23,NULL);
  printf("%d %d %d %d %d\n",ok,works[0],works[1],works[2],works[3]);
  int damage;
  while(scanf("%d%d%d%d%d%d",&damage,&attrs[0],&attrs[1],&attrs[2],&attrs[3],&draw_value)==6){
    draws=0;
    BATTLE_S_Modifyattack(0,0,1,&damage,23);
    printf("%d %d\n",damage,draws);
  }
  return 0;
}
'''
    options=[b'EA|20',b'WA|80',b'FI|100',b'WI|33',b'ALL|100',b'ea|50',b' EA|20',b'EA |20',b'EA',b'EA|',b'EA||80',b'FI|abc',b'WI| \t+72suffix|ignored',b'EA|-20',b'FI|0',b'WA|'+b'0'+b'x'*300]
    rng=random.Random(544546)
    cases=[(137,(95,95,95,95),99),(137,(96,96,96,96),100),(137,(100,100,100,100),104),(137,(100,100,100,100),105),(137,(0,0,0,0),100)]
    cases += [(rng.randrange(3001),tuple(rng.randrange(101) for _ in range(4)),rng.randrange(2**31)) for _ in range(128)]
    count=0
    with tempfile.TemporaryDirectory() as directory:
        root=Path(directory);src=root/'oracle.c';exe=root/'oracle'
        src.write_text(prefix+'\n'.join(macros+functions)+main)
        built=subprocess.run(['cc','-w','-O0','-fsanitize=undefined','-fno-sanitize-recover=all',str(src),'-o',str(exe)],capture_output=True,text=True)
        if built.returncode:
            raise ValueError('native compile failed: '+built.stderr[-2500:])
        lines='\n'.join(' '.join(map(str,(damage,*attrs,roll))) for damage,attrs,roll in cases)+'\n'
        for raw in options:
            result=subprocess.run([str(exe),raw.decode('ascii')],input=lines,capture_output=True,text=True,check=True)
            outputs=result.stdout.splitlines()
            if tuple(map(int,outputs[0].split())) != (1,7,17,3,0x12340017):
                raise ValueError('native callback carrier mismatch')
            if len(outputs)!=len(cases)+1:
                raise ValueError('native helper case count drift')
            option=parse_modifyattack_option(raw)
            for output,(damage,attrs,roll) in zip(outputs[1:],cases):
                owns=option is not None and option.element_index is not None and attrs[option.element_index]>0
                expected=modifyattack_helper_damage(damage,option,attrs,raw_rand=roll if owns else None)
                actual=tuple(map(int,output.split()))
                if actual!=expected:
                    raise ValueError(f'native helper differs: {actual} != {expected}')
                count+=1
    return {'callback_cases':len(options),'helper_cases':count,'ubsan_pass':True}


def analyze_profile(name,root):
    root=Path(root).resolve()
    head=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()
    if head!=PINNED[name] or subprocess.check_output(['git','-C',str(root),'status','--porcelain'],text=True).strip():
        raise ValueError('pinned HEAD/tree drift')
    base=root/LAYOUTS[name];include=base/'include'
    flags=['-I',str(include)]
    if name=='bismarck':
        flags+=['-I',str(root/'server/common'),'-I',str(root/'shared/lua51')]
    paths={'pet':base/'battle/pet_skill.c','event':base/'battle/battle_event.c','battle':base/'battle/battle.c',
           'battle_h':include/'battle.h','petskill_h':include/'pet_skillinfo.h','version':include/'version.h','util':base/'util.c'}
    if name=='bismarck':
        paths['util']=root/'server/common/utils/util_string.c'
        paths['workspace']=root/'server/common/workspace.c'
    data={key:_text(path) for key,path in paths.items()}
    active=set(re.findall(r'^#define\s+(\w+)',subprocess.check_output(['cpp','-dM',*flags,str(paths['version'])],text=True),re.M))
    fn=_compact(_strip(_definition(data['pet'],CALLBACK_NAME))).replace('char_index','charaindex')
    helper=_compact(_strip(_definition(data['event'],'BATTLE_S_Modifyattack')))
    event=_compact(_strip(_definition(data['event'],'BATTLE_S_AttackDamage',raw_window=True)))
    battle=_compact(_strip(data['battle'])).replace('char_index','charaindex')
    start=battle.index('case'+COMMAND_NAME+':');dispatch=battle[start:battle.index('case',start+4)]
    counter=_compact(_strip(_definition(data['event'],'BATTLE_Counter',raw_window=True)))
    gates={
        'feature_active':FEATURE_NAME in active,
        'distinct_registered_callback': '{"PETSKILL_Modifyattack",PETSKILL_Modifyattack,0}' in _compact(data['pet']) and '"PETSKILL_Mdfyattack"' in data['pet'],
        'callback_symbol_target_mode_low_array':all(s in fn for s in (COMMAND_NAME,'CHAR_WORKBATTLECOM2,toNo','BATTLE_CHARMODE_C_OK','CHAR_SETWORKINT_LOW(charaindex,CHAR_WORKBATTLECOM3,array)')),
        'callback_no_option_rng_or_power_writes':all(s not in fn for s in ('PETSKILL_getChar','rand(','RAND(','CHAR_WORKATTACKPOWER','CHAR_WORKDEFENCEPOWER','CHAR_WHICHTYPE')),
        'targetadjust_before_single_attackdamage':dispatch.index('BATTLE_TargetAdjust')<dispatch.index('BATTLE_S_AttackDamage') and 'BATTLE_NoAction' in dispatch,
        'reaction_demotion_before_attackseq':event.index('skill_type=-1')<event.index('BATTLE_AttackSeq'),
        'helper_after_attackseq_before_damagesub':event.index('BATTLE_AttackSeq')<event.index('BATTLE_S_Modifyattack')<event.index('ultimate=BATTLE_DamageSub'),
        'positive_damage_gate': 'case'+COMMAND_NAME+':if(damage>0){BATTLE_S_Modifyattack' in event,
        'only_four_codes_all_unvisited': 'KModKind[5]' in helper and '{"ALL",100}' in helper and 'i<4;i++' in helper,
        'two_256_byte_fields_and_float_percent':all(s in helper for s in ('buf1[256],buf2[256]','"|",1,buf1','"|",2,buf2','def=((float)(atoi(buf2))/100)')),
        'positive_target_raw_attribute_required': '(ModNum=CHAR_getInt(defindex,KModKind[i].Kind))>0' in helper,
        'one_rand_integer_division_before_float': 'def+=(float)((rand()%(ModNum+5))/100)' in helper and helper.count('rand(')==1,
        'compound_float_to_int_damage': '*damage+=*damage*def' in helper,
        'no_attribute_or_actor_mutation': 'CHAR_setInt' not in helper and 'CHAR_setWorkInt' not in helper,
        'attdouble_visual_flag_not_second_attack': 'flg|=BCF_ATTDOUBLE' in event and 'g%X|FF|' in event,
        'zero_damage_demotion_before_visual':event.index('if(damage<=0)')<event.index('flg|=BCF_ATTDOUBLE'),
        'no_wrapper_counter_or_guardian_redirect': 'BATTLE_Counter(' not in dispatch and 'if(Guardian>=0)' not in event,
        'native_counter_rejects_special_command_before_rng':all(s in counter for s in ('CHAR_WORKBATTLECOM1)==BATTLE_COM_ATTACK','CHAR_WORKBATTLECOM1)==BATTLE_COM_S_NOGUARD')) and 'returnFALSE' in counter[counter.index('BATTLE_COM_S_NOGUARD'):counter.index('BATTLE_CounterCheck')],
    }
    if not all(gates.values()):
        raise ValueError(f'{name} source gate failure: {gates}')
    enums=_enum_values([COMMAND_NAME,'BATTLE_COM_S_MDFYATTACK','BATTLE_CHARMODE_C_OK','BCF_ATTDOUBLE'],flags)
    pointer='null_pointer' if 'if(pszOption==NULL)' in helper else 'empty_literal_pointer_comparison'
    if pointer=='empty_literal_pointer_comparison' and 'if(pszOption=="\\0")' not in helper:
        raise ValueError('unknown pointer guard')
    return {'profile':name,'commit':head,'gates':gates,'enums':enums,'pointer_guard':pointer,
            'oracle':_native_oracle(data),'hashes':{key:_sha(path) for key,path in paths.items()}}


def emit(rows):
    print('StoneAge PETSKILL_Modifyattack fixed-source audit — R1')
    print('Derived facts only; source and native oracle remain transient.')
    for row in rows:
        print(f"PROFILE|name={row['profile']}|sha={row['commit']}|pointer_guard={row['pointer_guard']}")
        for key,value in sorted(row['enums'].items()):
            print(f"DESCENDANT_ENUM|profile={row['profile']}|symbol={key}|value={value}")
        for key,value in sorted(row['gates'].items()):
            print(f"GATE|profile={row['profile']}|name={key}|pass={int(value)}")
        for key,value in sorted(row['oracle'].items()):
            print(f"NATIVE|profile={row['profile']}|name={key}|value={int(value)}")
        for key,value in sorted(row['hashes'].items()):
            print(f"SOURCE_SHA256|profile={row['profile']}|file={key}|sha256={value}")
    print('FACT|helper_order=AttackSeq_then_positive_damage_modify_then_DamageSub')
    print('FACT|active_reaction_demotes_modify_before_AttackSeq')
    print('FACT|random_increment=integer_division_remainder_by_100_then_float')
    print('FACT|ALL_table_entry_not_visited_by_four_entry_loop')
    print('BOUNDARY|non_null_ASCII_options_and_bounded_0_to_100_attributes')
    print('BOUNDARY|original_binary_profile_numeric_command_and_libc_PRNG_open')
    print('RESOLUTION|MODIFYATTACK_FIXED_SOURCE_CLOSED_BOUNDED_REFERENCE')


def main():
    parser=argparse.ArgumentParser()
    for name in PINNED:
        parser.add_argument('--'+name+'-dir',type=Path,required=True)
    args=parser.parse_args()
    emit([analyze_profile(name,getattr(args,name+'_dir')) for name in PINNED])


if __name__=='__main__':
    main()
