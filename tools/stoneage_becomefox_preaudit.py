"""Pinned BecomeFox source preaudit; no data or runtime acceptance implied."""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import subprocess

from tools.stoneage_guard_break2_source_audit import (
    PINNED, LAYOUTS, _text, _sha, _compact, _function,
)
from tools.stoneage_mdfyattack_source_audit import _definition, _strip


def _if_block(source: str, pattern: str, required: str="") -> str:
    for match in re.finditer(pattern,source):
        block=_function(source[match.start():],match.group())
        if required in _compact(_strip(block)):
            return _compact(_strip(block))
    raise ValueError("source conditional block missing")


def analyze_profile(name: str, root: Path) -> dict:
    root=root.resolve()
    sha=subprocess.check_output(["git","-C",str(root),"rev-parse","HEAD"],text=True).strip()
    dirty=subprocess.check_output(["git","-C",str(root),"status","--porcelain"],text=True).strip()
    if sha!=PINNED[name] or dirty:
        raise ValueError("pinned source commit/tree drift")
    base=root/LAYOUTS[name]
    paths={
        "pet":base/"battle/pet_skill.c",
        "battle":base/"battle/battle.c",
        "event":base/"battle/battle_event.c",
        "command":base/"battle/battle_command.c",
        "char":base/"char/char.c",
        "char_base":base/"include/char_base.h",
    }
    data={k:_text(p).replace("char_index","charaindex") for k,p in paths.items()}
    compact={k:_compact(_strip(s)) for k,s in data.items()}
    callback=_compact(_strip(_definition(data["pet"],"PETSKILL_BecomeFox")))
    hit=_if_block(data["battle"],r'if\s*\(\s*\(?\s*COM\s*==\s*BATTLE_COM_S_BECOMEFOX')
    recovery=_if_block(
        data["battle"],
        r'if\s*\(\s*CHAR_getWorkInt\s*\(\s*charaindex\s*,\s*CHAR_WORKFOXROUND\s*\)\s*!=\s*-1\s*\)',
        'pBattle->turn-CHAR_getWorkInt(charaindex,CHAR_WORKFOXROUND)>2',
    )
    petin=_compact(_strip(_definition(data["event"],"BATTLE_PetIn")))
    exitbody=_compact(_strip(_definition(data["battle"],"_BATTLE_Exit")))
    getint='CHAR_getInt(petindex,CHAR_WORKFOXROUND)'
    setint='CHAR_setInt(petindex,CHAR_WORKFOXROUND,-1)'
    getwork='CHAR_getWorkInt(petindex,CHAR_WORKFOXROUND)'
    setwork='CHAR_setWorkInt(petindex,CHAR_WORKFOXROUND,-1)'
    checks={
        "callback_symbolic_command_target_mode_and_low_array":all(x in callback for x in (
            'CHAR_WORKBATTLECOM1,BATTLE_COM_S_BECOMEFOX',
            'CHAR_WORKBATTLECOM2,toNo','CHAR_WORKBATTLEMODE,BATTLE_CHARMODE_C_OK',
            'CHAR_SETWORKINT_LOW(charaindex,CHAR_WORKBATTLECOM3,array)',
        )),
        "callback_owns_no_option_or_rng":'PETSKILL_OPTION' not in callback and 'rand(' not in callback and 'RAND(' not in callback,
        "postattack_rejects_miss_dodge_allguard":all('!=BATTLE_RET_'+r in hit for r in ('MISS','DODGE','ALLGUARD')),
        "living_check_before_one_mod100_draw":'BATTLE_TargetCheck(battleindex,defNo)' in hit and hit.index('BATTLE_TargetCheck')<hit.index('rand()%100<31') and hit.count('rand()%100')==1,
        "draw_precedes_nonplayer_and_petflag_checks":hit.index('rand()%100<31')<hit.index('CHAR_WHICHTYPE')<hit.index('CHAR_WORK_PETFLG'),
        "nonplayer_not_exact_pet_type_check":'CHAR_WHICHTYPE)!=CHAR_TYPEPLAYER' in hit,
        "petflag_must_be_nonzero":'CHAR_WORK_PETFLG)!=0' in hit,
        "pig_guard_reads_attacker":'CHAR_getInt(charaindex,CHAR_BECOMEPIG)==-1' in hit,
        "successful_effect_records_current_battle_turn":'CHAR_setWorkInt(defindex,CHAR_WORKFOXROUND,pBattle->turn)' in hit,
        "successful_effect_uses_fox_image":'CHAR_setInt(defindex,CHAR_BASEIMAGENUMBER,101749)' in hit,
        "effect_can_clear_ride_and_set_petfall":'CHAR_setInt(defindex,CHAR_RIDEPET,-1)' in hit and 'CHAR_WORKPETFALL,1' in hit,
        "recovery_requires_strict_turn_difference_above2":'pBattle->turn-CHAR_getWorkInt(charaindex,CHAR_WORKFOXROUND)>2' in recovery,
        "recovery_restores_image_three_fixed_powers_and_work_marker":all(x in recovery for x in ('CHAR_BASEBASEIMAGENUMBER','CHAR_WORKFIXSTR','CHAR_WORKFIXTOUGH','CHAR_WORKFIXDEX','CHAR_WORKFOXROUND,-1')),
        "recovery_notifies_defaultpet_of_slot_minus5_owner":'toNo=defNo-5' in recovery and 'CHAR_DEFAULTPET' in recovery and 'CHAR_sendStatusString' in recovery,
        "action_time_three_powers_use_fixed_baselines_times_point8":all(x in compact['battle'] for x in (
            'CHAR_WORKATTACKPOWER,CHAR_getWorkInt(charaindex,CHAR_WORKFIXSTR)*0.8',
            'CHAR_WORKDEFENCEPOWER,CHAR_getWorkInt(charaindex,CHAR_WORKFIXTOUGH)*0.8',
            'CHAR_WORKQUICK,CHAR_getWorkInt(charaindex,CHAR_WORKFIXDEX)*0.8',
        )),
        "initiative_has_an_additional_quick_plus20_times_point8_site":'work=CHAR_getWorkInt(charaindex,CHAR_WORKQUICK)+20;dex=work*0.8' in compact['battle'],
        "exit_restores_fox_image_and_work_marker":'CHAR_BASEIMAGENUMBER)==101749' in exitbody and 'CHAR_WORKFOXROUND,-1' in exitbody and 'CHAR_BASEBASEIMAGENUMBER' in exitbody,
        "petin_fox_reset_precedes_noreturn_guard":petin.index('CHAR_WORKFOXROUND')<petin.index('CHAR_BATTLEFLG_NORETURN'),
        "petin_reset_restores_attack_quick_but_not_defence":all(x in petin[:petin.index('CHAR_BATTLEFLG_NORETURN')] for x in ('CHAR_WORKFIXSTR','CHAR_WORKFIXDEX')) and 'CHAR_WORKFIXTOUGH' not in petin[:petin.index('CHAR_BATTLEFLG_NORETURN')],
        "foxround_is_declared_as_work_state":'CHAR_WORKFOXROUND,' in compact['char_base'],
        "menu_restriction_uses_marker_not_image":'CHAR_getWorkInt(pindex,CHAR_WORKFOXROUND)!=-1' in compact['command'],
    }
    if not all(checks.values()):
        raise ValueError(f"{name} preaudit gates failed: {[k for k,v in checks.items() if not v]}")
    if name in ('gavin','iris'):
        accessor='int_accessor_for_work_field'
        if getint not in petin or setint not in petin:
            raise ValueError("expected descendant work/int mismatch drift")
    else:
        accessor='work_accessor_for_work_field'
        if getwork not in petin or setwork not in petin:
            raise ValueError("expected corrected descendant accessor drift")
    return {"profile":name,"sha":sha,"gates":checks,"petin_accessor_profile":accessor,"hashes":{k:_sha(p) for k,p in paths.items()}}


def main():
    parser=argparse.ArgumentParser()
    for name in PINNED:
        parser.add_argument('--'+name+'-dir',required=True,type=Path)
    args=parser.parse_args()
    print('StoneAge BecomeFox source preaudit R1; derived-only, no runtime admission.')
    for name in PINNED:
        r=analyze_profile(name,getattr(args,name+'_dir'))
        print(f"PROFILE|name={name}|sha={r['sha']}|passed_gates={len(r['gates'])}|petin_accessor={r['petin_accessor_profile']}")
        for gate in r['gates']:
            print(f'GATE|profile={name}|name={gate}|pass=1')
        for kind,digest in r['hashes'].items():
            print(f'SOURCE_SHA256|profile={name}|file={kind}|sha256={digest}')
    print('OPEN|exact_recovered25_population_metadata_OPTION_and_placements')
    print('OPEN|native_ordered_hit_cross_round_recall_and_persistence_semantics')
    print('OPEN|work_int_accessor_mismatch_requires_separate_versioned_profiles')
    print('RESOLUTION|BECOMEFOX_PINNED_SOURCE_PREAUDIT_PASS_NOT_REFERENCE_OR_RUNTIME_ACCEPTANCE')


if __name__=='__main__':
    main()
