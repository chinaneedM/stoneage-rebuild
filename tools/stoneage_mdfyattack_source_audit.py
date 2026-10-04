"""Reproduce Mdfyattack at three pinned descendants, emitting derived facts.

The numerical oracle compiles original functions only in a temporary directory.
It isolates the declared no-property-hook attribute domain; it is not a claim
that every active later extension is supported by the reconstruction runtime.
"""
import argparse
from pathlib import Path
import random
import re
import subprocess
import tempfile

from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS, _function, _sha, _text, _compact
from tools.stoneage_mdfyattack_model import (
    CALLBACK_NAME, COMMAND_NAME, FEATURE_NAME, ELEMENT_NAMES,
    parse_mdfyattack_option, mdfyattack_attribute_damage,
)


def _strip(text):
    return re.sub(r'/\*.*?\*/|//[^\n]*', '', text, flags=re.S)


def _definition(text, name, *, raw_window=False):
    match = re.search(r'\b(?:static\s+)?(?:int|void|BOOL|float|char\s*\*)\s*' +
                      re.escape(name) + r'\s*\([^;{}]*\)\s*\{', text, re.S)
    if not match:
        raise ValueError('missing definition: ' + name)
    signature = text[match.start():text.index('(', match.start())].rstrip()
    if raw_window:
        # Raw mutually exclusive preprocessor branches can have unbalanced
        # braces. End at the next top-level definition for semantic gates.
        next_fn = re.search(r'^\s*(?:static\s+)?(?:int|void|BOOL|float)\s+\w+\s*\([^;{}]*\)\s*\{',
                            text[match.end():], re.M | re.S)
        end = match.end() + next_fn.start() if next_fn else len(text)
        return text[match.start():end]
    return _function(text, signature)


def _native_oracle(data):
    """Actual callback/parser and AttrAdjust/AttrCalc/FieldAttAdjust witnesses."""
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
#define CHAR_WORKBATTLECOM4 4
#define CHAR_WORKBATTLEINDEX 5
#define PETSKILL_OPTION 0
#define BATTLE_COM_S_MDFYATTACK 1
#define BATTLE_CHARMODE_C_OK 1
#define BATTLE_ATTR_EARTH 1
#define BATTLE_ATTR_WATER 2
#define BATTLE_ATTR_FIRE 3
#define BATTLE_ATTR_WIND 4
#define _PSKILL_MDFYATTACK
static int works[6];
static char *option;
static int vectors[2][5];
static struct {int field_att;int att_pow;} BattleArray[1];
int CHAR_getWorkInt(int index,int pos){return works[pos];}
void CHAR_setWorkInt(int index,int pos,int value){works[pos]=value;}
char *PETSKILL_getChar(int array,int pos){return option;}
void BATTLE_GetAttr(int index,int *v){memcpy(v,vectors[index],5*sizeof(int));}
#define getStringFromIndexWithDelim(s,d,i,b,n) getStringFromIndexWithDelim_body(s,d,i,b,n,"oracle",0)
'''
    macros = []
    for name in ('CHAR_GETWORKINT_LOW', 'CHAR_GETWORKINT_HIGH', 'CHAR_SETWORKINT_LOW', 'CHAR_SETWORKINT_HIGH'):
        m = re.search(r'^\s*#define\s+' + name + r'(?:[^\n]*\\\n)*[^\n]*', data['battle_h'], re.M)
        if not m:
            raise ValueError('missing packed-work macro: ' + name)
        macros.append(m.group(0))
    for name in ('AJ_SAME', 'AJ_UP', 'AJ_DOWN', 'ATTR_MAX', 'D_ATTR'):
        m = re.search(r'^\s*#define\s+' + name + r'[^\n]*', data['battle_event'], re.M)
        if not m:
            raise ValueError('missing attribute constant: ' + name)
        macros.append(m.group(0))
    if 'workspace' in data:
        prefix += '\n#undef getStringFromIndexWithDelim\n#define getStringFromIndexWithDelim(s,d,i,b,n) GeneralSplitImpl(s,d,i,b,n,"oracle",0)\n'
        functions = [_definition(data['workspace'], n) for n in ('strncpysafe', 'strncpysafe2')]
        functions += [_definition(data['util'], n) for n in ('strstr_onebyte', 'GeneralSplitImpl')]
    else:
        functions = [_definition(data['util'], n) for n in
                     ('strcpysafe', 'strncpysafe', 'ScanOneByte', 'getStringFromIndexWithDelim_body')]
    functions += [_definition(data['pet_skill'], CALLBACK_NAME),
                  _definition(data.get('battle_magic', data['battle_event']), 'BATTLE_AttrCalc')] + [
        _definition(data['battle_event'], n) for n in
        ('BATTLE_FieldAttAdjust', 'BATTLE_AttrAdjust')
    ]
    main = r'''
int main(int argc,char **argv){
  if(argc==2){
    option=argv[1];works[3]=0x12340000;works[4]=0x45670003;
    int ok=PETSKILL_Mdfyattack(0,7,23,NULL);
    printf("%d %d %d %d %d\n",ok,works[1],works[3]&65535,works[4]&65535,works[4]>>16);
    return 0;
  }
  int damage,kind,amount,field,power;
  while(scanf("%d%d%d%d%d%d%d%d%d",&damage,&kind,&amount,
        &vectors[1][0],&vectors[1][1],&vectors[1][2],&vectors[1][3],&field,&power)==9){
    int sum=0;for(int i=0;i<4;i++)sum+=vectors[1][i];
    vectors[1][4]=sum<100?100-sum:0;
    for(int i=0;i<5;i++)vectors[0][i]=20;
    works[0]=BATTLE_COM_S_MDFYATTACK;works[4]=(amount<<16)|kind;
    BattleArray[0].field_att=field;BattleArray[0].att_pow=power;
    printf("%d\n",BATTLE_AttrAdjust(0,1,damage));
  }
  return 0;
}
'''
    options = [b'EA|100', b'WA|60', b'FI|0', b'WI|32767', b'EA|', b'WA|abc',
               b'FI| \t+72suffix|ignored', b'WI|01', b'ea|100', b'EA', b' EA|100',
               b'EA |100', b'|100', b'EA||100', b'EA|' + b'0' + b'x' * 300]
    rng = random.Random(548551)
    cases = [(137, 2, 150, (30, 20, 10, 0), 3, 73)]
    # Samples intentionally include sub-100 amounts, overflowing the usual
    # attribute-total normalization, and field-rounding boundaries.
    for _ in range(1024):
        damage = rng.randrange(0, 3001)
        kind = rng.randrange(4)
        amount = rng.choice((0, 1, 30, 60, 99, 100, 101, 150, 255))
        defense = tuple(rng.randrange(101) for _ in range(4))
        field = rng.randrange(5)
        power = rng.randrange(101)
        cases.append((damage, kind, amount, defense, field, power))
    with tempfile.TemporaryDirectory() as d:
        src = Path(d) / 'oracle.c'
        exe = Path(d) / 'oracle'
        src.write_text(prefix + '\n'.join(macros + functions) + main)
        result = subprocess.run(['cc', '-w', '-O0', '-fsanitize=undefined',
                                 '-fno-sanitize-recover=all', str(src), '-o', str(exe)],
                                capture_output=True, text=True)
        if result.returncode:
            raise ValueError('native oracle failed to compile: ' + result.stderr[-2500:])
        for raw in options:
            actual = tuple(map(int, subprocess.check_output([str(exe), raw.decode('ascii')], text=True).split()))
            try:
                parsed = parse_mdfyattack_option(raw)
            except ValueError:
                if actual[0] != 0:
                    raise ValueError('native callback accepted rejected grammar')
            else:
                if actual != (1, 7, 23, parsed.element_index, parsed.amount):
                    raise ValueError('native callback/parser mismatch')
        lines = [' '.join(map(str, (damage, kind, amount, *defense, field, power)))
                 for damage, kind, amount, defense, field, power in cases]
        result = subprocess.run([str(exe)], input='\n'.join(lines) + '\n',
                                capture_output=True, text=True, check=True)
        actuals = list(map(int, result.stdout.split()))
        if len(actuals) != len(cases):
            raise ValueError('native oracle case count drift')
        for actual, (damage, kind, amount, defense, field, power) in zip(actuals, cases):
            option = parse_mdfyattack_option((('EA', 'WA', 'FI', 'WI')[kind] + '|' + str(amount)).encode())
            expected = mdfyattack_attribute_damage(damage, option, defense,
                        field_attr='none' if field == 0 else ELEMENT_NAMES[field - 1], field_power=power)
            if actual != expected:
                raise ValueError(f'native attribute oracle mismatch: {actual} != {expected}, case={damage,kind,amount,defense,field,power}')
    return {'callback_cases': len(options), 'attribute_cases': len(cases), 'ubsan_pass': True}


def analyze_profile(name, root):
    root = Path(root).resolve()
    head = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()
    if head != PINNED[name] or subprocess.check_output(['git', '-C', str(root), 'status', '--porcelain'], text=True).strip():
        raise ValueError('pinned source HEAD/tree drift')
    base = root / LAYOUTS[name]
    include = base / 'include'
    flags = ['-I', str(include)]
    if name == 'bismarck':
        flags += ['-I', str(root / 'server/common'), '-I', str(root / 'shared/lua51')]
    macros = subprocess.check_output(['cpp', '-dM', *flags, str(include / 'version.h')], text=True)
    active = set(re.findall(r'^#define\s+(\w+)', macros, re.M))
    paths = {'pet_skill': base / 'battle/pet_skill.c', 'battle': base / 'battle/battle.c',
             'battle_event': base / 'battle/battle_event.c', 'util': base / 'util.c',
             'battle_h': include / 'battle.h', 'event_h': include / 'battle_event.h',
             'petskill_h': include / 'pet_skillinfo.h', 'version': include / 'version.h'}
    if name == 'bismarck':
        paths['util'] = root / 'server/common/utils/util_string.c'
        paths['workspace'] = root / 'server/common/workspace.c'
        paths['battle_magic'] = base / 'battle/battle_magic.c'
    data = {k: _text(p) for k, p in paths.items()}
    fn = _compact(_strip(_definition(data['pet_skill'], CALLBACK_NAME))).replace('char_index', 'charaindex')
    attr = _compact(_strip(_definition(data['battle_event'], 'BATTLE_AttrAdjust')))
    event = _compact(_strip(_definition(data['battle_event'], 'BATTLE_S_AttackDamage', raw_window=True)))
    battle = _compact(_strip(data['battle']))
    counter = _compact(_strip(_definition(data['battle_event'], 'BATTLE_Counter', raw_window=True)))
    start = battle.index('case' + COMMAND_NAME + ':')
    branch = battle[start:battle.index('case', start + 4)]
    mark = event[event.index('case' + COMMAND_NAME + ':'):]
    mark = mark[:mark.index('break;')]
    rewrite = attr.index('At_pow[i]=0')
    hooks = attr.index('CHAR_getFunctionPointer')
    field = attr.index('At_FieldPow=BATTLE_FieldAttAdjust')
    calc = attr.index('damage=BATTLE_AttrCalc')
    gates = {
        'feature_active': FEATURE_NAME in active,
        'distinct_registered_callbacks': '"PETSKILL_Mdfyattack"' in data['pet_skill'] and '"PETSKILL_Modifyattack"' in data['pet_skill'],
        'writes_command_target_mode_low_array_before_option': all(s in fn for s in
            (COMMAND_NAME, 'CHAR_WORKBATTLECOM2,toNo', 'BATTLE_CHARMODE_C_OK', 'CHAR_SETWORKINT_LOW(charaindex,CHAR_WORKBATTLECOM3,array)')) and fn.index('CHAR_WORKBATTLECOM3') < fn.index('PETSKILL_getChar'),
        'no_actor_gate_or_work_power_mutation': all(s not in fn for s in ('CHAR_WHICHTYPE', 'CHAR_WORKATTACKPOWER', 'CHAR_WORKDEFENCEPOWER')),
        'exact_codes_and_256_byte_buffer': '"EA","WA","FI","WI"' in fn and 'buf1[256]' in fn and 'strcmp(buf1,MNodify[i])' in fn,
        'low_kind_before_second_field_high_atoi': fn.index('CHAR_WORKBATTLECOM4,i') < fn.index('"|",2,buf1') < fn.index('nums=atoi(buf1)') < fn.index('CHAR_WORKBATTLECOM4,nums'),
        'clear_five_then_selected_with_neutral_zero': all(s in attr for s in ('i<5;i++', 'At_pow[i]=0', 'At_pow[MKind]=MODS', 'At_pow[4]=0')),
        'override_before_properties_before_field_before_calc': rewrite < hooks < field < calc,
        'attacker_and_defender_property_hooks': all(s in attr for s in ('loopfunc(attackindex,defindex,&damage,At_pow,5)', 'loopfunc(defindex,attackindex,&damage,Dt_pow,5)')),
        'dispatch_targetadjust_specialized_single_hit': 'BATTLE_TargetAdjust' in branch and ('BATTLE_S_AttackDamage(battleindex,attackNo,defNo,' + COMMAND_NAME + ',skill)') in branch and 'BATTLE_COM_ATTACK' not in branch and 'BATTLE_Counter' not in branch,
        'native_counter_rejects_specialized_command_before_rng': all(x in counter for x in
            ('CHAR_WORKBATTLECOM1)==BATTLE_COM_ATTACK', 'CHAR_WORKBATTLECOM1)==BATTLE_COM_S_NOGUARD')) and
            counter.index('BATTLE_COM_S_NOGUARD') < counter.index('BATTLE_CounterCheck') and
            'returnFALSE' in counter[counter.index('BATTLE_COM_S_NOGUARD'):counter.index('BATTLE_CounterCheck')],
        'reaction_disables_event_skill_before_attackseq': event.index('skill_type=-1') < event.index('BATTLE_AttackSeq'),
        'damage_sub_after_attackseq': event.index('BATTLE_AttackSeq') < event.index('BATTLE_DamageSub'),
        'guardian_not_reassigned_by_specialized_wrapper': 'Guardian=-1' in event and '&Guardian,skill_type' in event and 'if(Guardian>=0)' not in event,
        'positive_damage_event_gate_before_modify_mark': event.index('if(damage<=0)') < event.index('case' + COMMAND_NAME),
        'modify_flag_and_skill_array_witness': 'flg|=BCF_MODIFY' in mark and 'g%X|FF|' in mark and 'petdamage,skill' in mark,
        'no_modifyattack_post_damage_transform': ('case' + COMMAND_NAME) not in event[:event.index('ultimate=BATTLE_DamageSub')],
    }
    if not all(gates.values()):
        raise ValueError(f'{name} Mdfyattack source gate failure: {gates}')
    probe = '#include <stdio.h>\n#include "char_base.h"\n#include "battle.h"\n#include "battle_event.h"\nint main(void){printf("%d %d %d",BATTLE_COM_S_MDFYATTACK,BATTLE_COM_S_MODIFYATT,BCF_MODIFY);}\n'
    with tempfile.TemporaryDirectory() as d:
        src = Path(d) / 'header.c'; exe = Path(d) / 'header'; src.write_text(probe)
        subprocess.run(['cc', '-w', *flags, str(src), '-o', str(exe)], check=True, capture_output=True)
        command, other_command, event_flag = map(int, subprocess.check_output([str(exe)], text=True).split())
    null_kind = 'null_pointer' if 'if(pszOption==NULL)' in fn else 'empty_literal_pointer_comparison'
    if null_kind == 'empty_literal_pointer_comparison' and 'if(pszOption=="\\0")' not in fn:
        raise ValueError('unrecognized OPTION pointer gate')
    return {'profile': name, 'commit': head, 'command': command, 'modifyattack_command': other_command,
            'modify_event_flag': event_flag, 'option_pointer_gate': null_kind,
            'delimiter_helper': 'GeneralSplitImpl' if name == 'bismarck' else 'getStringFromIndexWithDelim_body',
            'property_feature_active': '_BATTLE_PROPERTY' in active,
            'suit_feature_active': '_SUIT_TWFWENDUM' in active,
            'gates': gates, 'oracle': _native_oracle(data), 'hashes': {k: _sha(p) for k, p in paths.items()}}


def emit(rows):
    print('StoneAge Mdfyattack fixed-source audit — R1')
    print('No original source text is stored. Numerical oracle excludes property/suit extensions.')
    for row in rows:
        print('PROFILE|' + '|'.join(f'{k}={int(v) if isinstance(v, bool) else v}'
              for k, v in row.items() if k not in {'gates', 'hashes', 'oracle'}))
        for key, value in sorted(row['gates'].items()):
            print(f"GATE|profile={row['profile']}|name={key}|pass={int(value)}")
        for key, value in sorted(row['oracle'].items()):
            print(f"ORACLE|profile={row['profile']}|name={key}|value={int(value)}")
        for key, value in sorted(row['hashes'].items()):
            print(f"SOURCE_SHA256|profile={row['profile']}|file={key}|sha256={value}")
    closed = len(rows) == 3 and all(all(r['gates'].values()) and r['oracle']['ubsan_pass'] for r in rows)
    print('RESOLUTION|MDFYATTACK_FIXED_SOURCE_' + ('CLOSED_SAFE_REFERENCE' if closed else 'OPEN'))
    if not closed:
        raise ValueError('Mdfyattack source reference remains open')


def main():
    parser = argparse.ArgumentParser()
    for name in PINNED:
        parser.add_argument('--' + name + '-dir', type=Path, required=True)
    args = parser.parse_args()
    emit([analyze_profile(name, getattr(args, name + '_dir')) for name in PINNED])


if __name__ == '__main__':
    main()
