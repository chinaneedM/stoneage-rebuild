"""Hash/gate/native audit of clean pinned WildViolentAttack descendants.

Original functions are compiled only in temporary storage. CP950 execution
charset is an explicit conditional build, never an original binary identity.
"""
import argparse
from pathlib import Path
import random
import re
import subprocess
import tempfile

from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS, _sha, _text, _compact, _macro_int
from tools.stoneage_mdfyattack_source_audit import _definition, _strip
from tools.stoneage_wildviolent_model import (
    CALLBACK_NAME, COMMAND_NAME, FEATURE_NAME, SOURCE_PETSKILL_SYMBOL_NAME,
    resolve_wildviolent_setup, plan_wildviolent_nonbow_action,
    wildviolent_divided_damage,
)


def _native_oracle(data, profile, *, recovered_options=()):
    callback = _definition(data['pet_skill'], CALLBACK_NAME)
    packed_macros=[]
    for name in ('CHAR_GETWORKINT_HIGH','CHAR_SETWORKINT_HIGH'):
        macro=re.search(r'^\s*#define\s+'+name+r'(?:[^\n]*\\\n)*[^\n]*',data['battle_h'],re.M)
        if not macro:raise ValueError('missing actual packed HIGH macro')
        packed_macros.append(macro.group())
    battle = _strip(data['battle'])
    match = re.search(r'case\s+' + COMMAND_NAME + r'\s*:(.*?)break;', battle, re.S)
    if not match:
        raise ValueError('missing action count case')
    setup = match.group(1)
    attack = _strip(_definition(data['event'], 'BATTLE_Attack', raw_window=True))
    division = re.search(r'if\s*\(\s*gDamageDiv\s*!=\s*0\.0\s*&&\s*damage\s*>\s*0\s*\)\s*\{[^{}]*\}', attack)
    if not division:
        raise ValueError('missing actual positive-damage division seam')
    prefix = r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include <float.h>
_Static_assert(CHAR_BIT==8 && INT_MAX==2147483647 && sizeof(float)==4 && FLT_RADIX==2 && FLT_MANT_DIG==24,"requires int32/IEEE binary32");
#define BOOL int
#define TRUE 1
#define FALSE 0
#define print(...) 0
#define CHAR_WORKBATTLECOM1 0
#define CHAR_WORKBATTLECOM2 1
#define CHAR_WORKBATTLEMODE 2
#define CHAR_WORKBATTLECOM3 3
#define CHAR_WORKFIXSTR 4
#define CHAR_WORKFIXTOUGH 5
#define CHAR_WORKATTACKPOWER 6
#define CHAR_WORKDEFENCEPOWER 7
#define PETSKILL_OPTION 0
#define BATTLE_COM_S_WILDVIOLENTATTACK 1
#define BATTLE_CHARMODE_C_OK 1
static int works[8], witnessed_roll, rng_calls;
static char *option;
static float gDamageDiv;
static int gBattleDuckModyfy;
int CHAR_getWorkInt(int index,int pos){return works[pos];}
void CHAR_setWorkInt(int index,int pos,int value){works[pos]=value;}
char *PETSKILL_getChar(int array,int pos){return option;}
int RAND(int lo,int hi){if(lo!=3||hi!=10)abort();rng_calls++;return witnessed_roll;}
'''
    main = r'''
int main(void){
 char mode,hex[2048],bytes[1024];int damage,count;
 while(scanf(" %c",&mode)==1){
  if(mode=='C'){
   if(scanf("%2047s%d%d%d%d%d",hex,&works[4],&works[5],&works[6],&works[7],&works[3])!=6)abort();
   works[0]=works[1]=works[2]=-99;
   if(strcmp(hex,"NULL")==0)option=NULL;
   else{size_t n=strlen(hex)/2;for(size_t i=0;i<n;i++){unsigned v;sscanf(hex+2*i,"%2x",&v);bytes[i]=(char)v;}bytes[n]=0;option=bytes;}
   int ok=PETSKILL_WildViolentAttack(0,7,23,NULL);
   printf("C %d %d %d %d %d %d %d\n",ok,works[0],works[1],works[2],works[6],works[7],works[3]);
  }else if(mode=='D'){
   if(scanf("%d%d",&damage,&count)!=2)abort();gDamageDiv=count;
   DIVISION_FRAGMENT
   printf("D %d\n",damage);
  }else if(mode=='P'){
   int charaindex=0,char_index=0,attack_max=1;
   if(scanf("%d%d",&witnessed_roll,&works[3])!=2)abort();rng_calls=0;
   SETUP_FRAGMENT
   printf("P %d %.0f %d %d\n",attack_max,gDamageDiv,gBattleDuckModyfy,rng_calls);
  }else abort();
 }
 return 0;
}
'''.replace('DIVISION_FRAGMENT', division.group()).replace('SETUP_FRAGMENT', setup)
    cases = []
    # Independent scanner fixtures include failed-scanf state reuse, duplicate
    # markers, decimals, exact binary32 halfway values and charset mismatch.
    texts = ('', 'plain', '攻%50', '防%-50', '避12', '攻%50防%bad避12',
             '攻%bad防%bad', '防%50攻%25避0', '攻%25攻%99防%-20避32767',
             '攻%1.000000059604644775390625',
             '攻%1.000000059604644775390626', '攻%.125防%2e1避+7',
             '攻%-1.25防%50避bad', '攻%200防%-100避 0', '避', '攻%防%')
    for charset in ('utf-8', 'cp950'):
        callback_lines, expected = [], []
        options=[text.encode(encoding) for text in texts for encoding in ('utf-8','cp950')]
        options+=list(recovered_options)
        for raw in options:
            for strength,toughness,before_a,before_d,packed in (
                (0,0,19,23,0x1234abcd), (100,101,77,79,-65535),
                (10001,9999,3,5,65535), (1000000,1000000,77,79,1234),
                (16777217,16777219,8,9,0x12345678)):
                result = resolve_wildviolent_setup(
                    option=raw, execution_charset=charset, profile=profile,
                    target_slot=7, fixed_strength=strength, fixed_toughness=toughness,
                    attack_power_before=before_a, defense_power_before=before_d,
                    packed_com3_before=packed)
                callback_lines.append(f'C {raw.hex() or "EMPTY"} {strength} {toughness} {before_a} {before_d} {packed}')
                expected.append(f'C {int(result.source_return_value)} 1 7 1 {result.attack_power} {result.defense_power} {result.packed_com3}')
        if profile != 'bismarck':
            callback_lines.append('C NULL 100 100 77 79 1234')
            expected.append('C 0 1 7 1 77 79 1234')
        # EMPTY is handled as the zero-length byte string, not a literal word.
        callback_lines = [line.replace('C EMPTY ', 'C x ') for line in callback_lines]
        lines = list(callback_lines)
        rng = random.Random(541)
        damages = [0,-1,-2147483648,1,2,3,10,3000,16777215,16777217,2147483647]
        damages += [rng.randrange(1,2**31) for _ in range(128)]
        for damage in damages:
            for count in range(3,11):
                lines.append(f'D {damage} {count}')
                expected.append(f'D {wildviolent_divided_damage(damage,count)}')
        for count in range(3,11):
            for packed in (0,65535,0x7fff1234,-65535):
                plan=plan_wildviolent_nonbow_action(count_roll_3_10=count,packed_com3=packed,target_slot=7)
                lines.append(f'P {count} {packed}')
                expected.append(f'P {plan.attack_count} {plan.damage_divisor} {plan.additive_dodge_percent_points} 1')
        with tempfile.TemporaryDirectory() as directory:
            source=Path(directory)/'oracle.c'; exe=Path(directory)/'oracle'
            source.write_text(prefix+'\n'+'\n'.join(packed_macros)+'\n'+callback+'\n'+main)
            command=['cc','-O0','-fsanitize=undefined','-fno-sanitize-recover=all',
                     '-fexec-charset='+('UTF-8' if charset=='utf-8' else 'CP950'),str(source),'-o',str(exe)]
            subprocess.run(command,check=True,capture_output=True)
            run=subprocess.run([str(exe)],input='\n'.join(lines)+'\n',text=True,capture_output=True,check=True)
            observed=run.stdout.splitlines()
            if observed != expected:
                difference=next((i for i,(a,b) in enumerate(zip(observed,expected)) if a!=b), min(len(observed),len(expected)))
                raise ValueError(f'{profile}/{charset} native oracle differs at {difference}: {observed[difference:difference+1]} vs {expected[difference:difference+1]}')
            diagnostics=0
            if charset=='cp950':
                for duck in (-10,32768):
                    raw=('避'+str(duck)).encode('cp950')
                    run=subprocess.run([str(exe)],input=f'C {raw.hex()} 100 100 77 79 1234\n',text=True,capture_output=True)
                    if run.returncode==0 or 'left shift' not in run.stderr:
                        raise ValueError('actual HIGH macro UB diagnostic missing')
                    diagnostics+=1
        cases.append({'execution_charset':charset,'callback_cases':len(callback_lines),
                      'division_cases':len(damages)*8,'action_plan_cases':32,
                      'recovered_callback_cases':len(recovered_options)*5,
                      'expected_undefined_shift_diagnostics':diagnostics})
    return cases


def analyze_profile(name, root, *, recovered_options=()):
    root=Path(root).resolve()
    head=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()
    if head!=PINNED[name] or subprocess.check_output(['git','-C',str(root),'status','--porcelain'],text=True).strip():
        raise ValueError('pinned source HEAD/tree drift')
    base=root/LAYOUTS[name]; include=base/'include'
    flags=['-I',str(include)]
    if name=='bismarck':flags+=['-I',str(root/'server/common'),'-I',str(root/'shared/lua51')]
    macros=subprocess.check_output(['cpp','-dM',*flags,str(include/'version.h')],text=True)
    active=set(re.findall(r'^#define\s+(\w+)',macros,re.M))
    paths={'pet_skill':base/'battle/pet_skill.c','battle':base/'battle/battle.c',
           'event':base/'battle/battle_event.c','battle_h':include/'battle.h',
           'petskill_h':include/'pet_skillinfo.h','version':include/'version.h'}
    data={k:_text(p) for k,p in paths.items()}
    fn=_compact(_strip(_definition(data['pet_skill'],CALLBACK_NAME))).replace('char_index','charaindex')
    battle=_compact(_strip(data['battle'])).replace('char_index','charaindex')
    setup=battle.index('case'+COMMAND_NAME+':attack_max=RAND(3,10);')
    listing_call=battle.index('BATTLE_TargetListSet(charaindex,attackNo,aDefList)',setup)
    common=battle.index('case'+COMMAND_NAME+':',listing_call)
    body=battle[common:]
    attack=_compact(_strip(_definition(data['event'],'BATTLE_Attack',raw_window=True)))
    listing=_compact(_strip(_definition(data['battle'],'BATTLE_TargetListSet',raw_window=True)))
    listing=listing[:listing.index('if(BATTLE_GetWepon(')]
    first_hit=body.index('ContFlg=BATTLE_Attack(')
    later_target=body.index('defNo=aDefList[++k]')
    counter=body.index('k<5&&ContFlg==TRUE')
    gates={
        'feature_active':FEATURE_NAME in active,
        'callback_no_actor_kind_gate':'CHAR_getInt' not in fn,
        'command_target_mode_before_option':all(x in fn[:fn.index('PETSKILL_getChar')] for x in (COMMAND_NAME,'CHAR_WORKBATTLECOM2,toindex','BATTLE_CHARMODE_C_OK')),
        'float_initial_and_shared_fallback':'floatfPer=0.01' in fn and fn.count('fPer=(fPer/100)')==2,
        'fixed_byte_offsets':all(x in fn for x in ('"攻%"','"防%"','sscanf(pszP+3,"%f",&fPer)','"避"','sscanf(pszP+2,"%d",&iDuck)')),
        'only_high_com3_write':'CHAR_SETWORKINT_HIGH(charaindex,CHAR_WORKBATTLECOM3,iDuck)' in fn and 'CHAR_SETWORKINT_LOW' not in fn,
        'power_fixed_plus_truncated_float_delta':fn.count('strdef=(int)(strdef*fPer)')==2 and all(x in fn for x in ('CHAR_WORKFIXSTR)+strdef','CHAR_WORKFIXTOUGH)+strdef')),
        'action_count_divisor_duck':all(x in battle[setup:listing_call] for x in ('attack_max=RAND(3,10)','gDamageDiv=attack_max','gBattleDuckModyfy=CHAR_GETWORKINT_HIGH(charaindex,CHAR_WORKBATTLECOM3)')),
        'count_before_listing_before_adjust':setup<listing_call<common and body.index('BATTLE_TargetAdjust(')<first_hit,
        'nonbow_original_target_fill':'pList[i]=defNo' in listing and 'i<BATTLE_ENTRY_MAX*2' in listing,
        'random_target_preselection_excludes_wild':COMMAND_NAME not in listing[listing.index('for(i=0;'):],
        'ordinary_command_before_hits':'CHAR_WORKBATTLECOM1,BATTLE_COM_ATTACK' in body[:first_hit],
        'loop_not_guarded_by_continuation_flag':'for(attack_count=0,k=0;;)' in body[:first_hit],
        'later_original_target_write_before_adjust':first_hit<later_target<body.index('CHAR_WORKBATTLECOM2,defNo',later_target)<body.index('BATTLE_TargetAdjust(',later_target)<counter,
        'duck_reset_before_final_counter':body.index('gBattleDuckModyfy=0',later_target)<counter,
        'divide_after_attackseq_before_damagesub':attack.index('BATTLE_AttackSeq(')<attack.index('damage/=gDamageDiv')<attack.index('BATTLE_DamageSub('),
        'positive_damage_minimum_one':'if(damage<=0)damage=1' in attack,
        'duck_modifier_adds_before_clamp':'per+=gBattleDuckModyfy;' in _compact(_strip(data['event'])),
    }
    if not all(gates.values()):raise ValueError(f'{name} source gates failed: {gates}')
    code='#include <stdio.h>\n#include "char_base.h"\n#include "battle.h"\nint main(void){printf("%d",'+COMMAND_NAME+');return 0;}\n'
    with tempfile.TemporaryDirectory() as directory:
        src=Path(directory)/'enum.c';exe=Path(directory)/'enum';src.write_text(code)
        subprocess.run(['cc','-w',*flags,str(src),'-o',str(exe)],check=True,capture_output=True)
        command=int(subprocess.check_output([str(exe)],text=True))
    return {'profile':name,'commit':head,'compiled_command':command,
            'source_skill_symbol_id':_macro_int(data['petskill_h'],SOURCE_PETSKILL_SYMBOL_NAME),
            'same_side_limit_active':'_SKILLLIMIT' in active,
            'option_failure_gate':'strcmp_empty_NULL_undefined' if name=='bismarck' else 'NULL_false_empty_accepted',
            'hashes':{k:_sha(p) for k,p in paths.items()},'gates':gates,
            'native':_native_oracle(data,name,recovered_options=recovered_options)}


def emit(rows):
    print('StoneAge WildViolentAttack fixed-source conditional reference — R1')
    print('Original compiler execution charset and recovered numeric command remain UNKNOWN.')
    print('Non-bow opposite-side action-plan/finite-int32/nonnegative-HIGH domain; ordered runtime OPEN.')
    print('No original source, raw recovered OPTION rows or assets are stored.')
    for row in rows:
        print('PROFILE|'+'|'.join(f'{k}={int(v) if isinstance(v,bool) else v}' for k,v in row.items() if k not in {'hashes','gates','native'}))
        for key,value in sorted(row['gates'].items()):print(f"GATE|profile={row['profile']}|name={key}|pass={int(value)}")
        for key,value in sorted(row['hashes'].items()):print(f"SOURCE_SHA256|profile={row['profile']}|file={key}|sha256={value}")
        for witness in row['native']:print('NATIVE|profile='+row['profile']+'|'+'|'.join(f'{k}={v}' for k,v in witness.items())+'|UBSan=PASS')
    print('RESOLUTION|WILDVIOLENT_FIXED_SOURCE_CLOSED_CONDITIONAL_CHARSET_REFERENCE')
    print('RESOLUTION|WILDVIOLENT_ORIGINAL_BUILD_CHARSET_OPEN')
    print('RESOLUTION|WILDVIOLENT_ORDERED_RUNTIME_OPEN')


def main():
    parser=argparse.ArgumentParser()
    for name in PINNED:parser.add_argument('--'+name+'-dir',type=Path,required=True)
    args=parser.parse_args()
    emit([analyze_profile(name,getattr(args,name+'_dir')) for name in PINNED])


if __name__=='__main__':main()
