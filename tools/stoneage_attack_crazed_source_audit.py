"""Reproduce AttackCrazed behavior at three pinned descendant commits."""
import argparse
import re
import subprocess
import tempfile
from pathlib import Path
from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS, _function, _sha, _text, _compact, _macro_int
from tools.stoneage_attack_crazed_model import CALLBACK_NAME, COMMAND_NAME, FEATURE_NAME, SOURCE_PETSKILL_SYMBOL_NAME


def analyze_profile(name, root):
    root = Path(root).resolve()
    head = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()
    if head != PINNED[name] or subprocess.check_output(['git', '-C', str(root), 'status', '--porcelain'], text=True).strip():
        raise ValueError('source HEAD/tree drift')
    base = root / LAYOUTS[name]
    include = base / 'include'
    flags = ['-I', str(include)]
    if name == 'bismarck':
        flags += ['-I', str(root/'server/common'), '-I', str(root/'shared/lua51')]
    macros = subprocess.check_output(['cpp', '-dM', *flags, str(include/'version.h')], text=True)
    active = set(re.findall(r'^#define\s+(\w+)', macros, re.M))
    paths = {'pet_skill':base/'battle/pet_skill.c', 'battle':base/'battle/battle.c',
             'battle_h':include/'battle.h', 'petskill_h':include/'pet_skillinfo.h', 'version':include/'version.h'}
    data = {k:_text(p) for k,p in paths.items()}
    fn = _compact(_function(data['pet_skill'], 'int '+CALLBACK_NAME)).replace('char_index', 'charaindex')
    battle = _compact(re.sub(r'/\*.*?\*/|//[^\n]*', '', data['battle'], flags=re.S)).replace('char_index', 'charaindex')
    start = battle.index('voidBATTLE_TargetListSet(')
    listing = battle[start:battle.index('if(BATTLE_GetWepon(', start)]
    setup = battle.index('case'+COMMAND_NAME+':attack_max=')
    list_call = battle.index('BATTLE_TargetListSet(charaindex,attackNo,aDefList)', setup)
    common = battle.index('case'+COMMAND_NAME+':', list_call)
    body = battle[common:]
    first_adjust = body.index('BATTLE_TargetAdjust(')
    first_attack = body.index('ContFlg=BATTLE_Attack(')
    next_list = body.index('defNo=aDefList[++k]')
    next_adjust = body.index('BATTLE_TargetAdjust(', next_list)
    gates = {
        'feature_active':FEATURE_NAME in active,
        'reject_player':'CHAR_TYPEPLAYER)returnFALSE' in fn,
        'writes_command_target_mode':all(s in fn for s in (COMMAND_NAME,'CHAR_WORKBATTLECOM2,toNo','BATTLE_CHARMODE_C_OK')),
        'setup_attack_08':'CHAR_WORKFIXSTR)*0.8' in fn,
        'setup_defense_07':'CHAR_WORKFIXTOUGH)*0.7' in fn,
        'setup_before_option':fn.index('CHAR_WORKDEFENCEPOWER') < fn.index('PETSKILL_getChar'),
        'low_array_high_atoi':all(s in fn for s in ('CHAR_SETWORKINT_LOW(charaindex,CHAR_WORKBATTLECOM3,array)', 'CHAR_SETWORKINT_HIGH(charaindex,CHAR_WORKBATTLECOM3,atoi(pszOption))')),
        'initial_fill_20':'i<BATTLE_ENTRY_MAX*2;i++' in listing and 'pList[i]=defNo' in listing,
        'excludes_side_last':all(s in listing for s in ('deftop=9','deftop=19','i=defsub;i<deftop;i++')),
        'candidate_targetcheck':'BATTLE_TargetCheck(battleindex,i)==FALSE' in listing,
        'replacement_rng_and_sentinel':all(s in listing for s in ('i=0;i<n;i++','pList[i]=plive[RAND(0,j-1)]','pList[i]=-1')),
        'no_candidate_early_return':'if(j==0)return' in listing,
        'invalid_target_index1_sentinel':'pList[1]=-1;return' in listing,
        'same_side_gate_under_shootchestnut':'#ifdef_SHOOTCHESTNUTif(BATTLE_CheckSameSide' in listing,
        'count_without_damage_division':'gDamageDiv' not in battle[setup:list_call].split('break;',1)[0],
        'preselect_before_first_adjust':setup < list_call < common and first_adjust < first_attack,
        'later_targets_skip_index_zero':first_attack < next_list < next_adjust,
        'ordinary_attack_command_before_hit':'CHAR_WORKBATTLECOM1,BATTLE_COM_ATTACK' in body[:first_attack],
        'counter_after_multihit':body.index('k<5&&ContFlg==TRUE') > next_adjust,
    }
    if not all(gates.values()):
        raise ValueError(f'{name} source audit failed: {gates}')
    # Inspect the actual headers with their active compile profile.
    code = '#include <stdio.h>\n#include "char_base.h"\n#include "battle.h"\nint main(void){printf("%d",BATTLE_COM_S_ATTCRAZED);return 0;}\n'
    with tempfile.TemporaryDirectory() as d:
        src=Path(d)/'p.c'; exe=Path(d)/'p';src.write_text(code)
        subprocess.run(['cc','-w',*flags,str(src),'-o',str(exe)],check=True,capture_output=True)
        command=int(subprocess.check_output([str(exe)],text=True))
    null_kind = 'null_pointer' if 'if(pszOption==NULL)' in fn else 'empty_literal_pointer_comparison'
    if null_kind == 'empty_literal_pointer_comparison' and 'if(pszOption=="\\0")' not in fn:
        raise ValueError('unrecognized OPTION pointer gate')
    return {'profile':name,'commit':head,'command':command,'source_skill_symbol_id':_macro_int(data['petskill_h'],SOURCE_PETSKILL_SYMBOL_NAME),
            'shootchestnut_active':'_SHOOTCHESTNUT' in active,'option_pointer_gate':null_kind,
            'gates':gates,'hashes':{k:_sha(p) for k,p in paths.items()}}


def emit(rows):
    print('StoneAge AttackCrazed fixed-source audit — R1')
    print('No original source text is stored. Closure covers non-null safe-count reference domain only.')
    for r in rows:
        print('PROFILE|'+'|'.join(f'{k}={int(v) if isinstance(v,bool) else v}' for k,v in r.items() if k not in {'gates','hashes'}))
        for k,v in sorted(r['gates'].items()):print(f"GATE|profile={r['profile']}|name={k}|pass={int(v)}")
        for k,v in sorted(r['hashes'].items()):print(f"SOURCE_SHA256|profile={r['profile']}|file={k}|sha256={v}")
    closed=len(rows)==3 and {r['source_skill_symbol_id'] for r in rows}=={608} and all(all(r['gates'].values()) for r in rows)
    print('RESOLUTION|ATTACKCRAZED_FIXED_SOURCE_'+('CLOSED_SAFE_REFERENCE' if closed else 'OPEN'))


def main():
    p=argparse.ArgumentParser()
    for name in PINNED:p.add_argument('--'+name+'-dir',type=Path,required=True)
    a=p.parse_args();emit([analyze_profile(n,getattr(a,n+'_dir')) for n in PINNED])
if __name__=='__main__':main()
