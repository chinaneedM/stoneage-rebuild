"""Pinned normal-pet PetIn -> PetDefaultExit -> BATTLE_Exit lifecycle facts.

Textual source audit only; no full-server/native exit execution is claimed.
"""
import argparse
from pathlib import Path
import subprocess

from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS, _sha, _compact
from tools.stoneage_mdfyattack_source_audit import _definition, _strip


def lifecycle_gates(battle, event):
    normalize=lambda s: _compact(_strip(s)).replace('char_index','charaindex')
    default=normalize(_definition(battle,'BATTLE_PetDefaultExit'))
    exit_body=normalize(_definition(battle,'_BATTLE_Exit',raw_window=True))
    recall=normalize(_definition(event,'BATTLE_PetIn'))
    return {
        'default_exit_validates_owner': 'CHAR_CHECKINDEX(charaindex)==FALSE' in default,
        'default_exit_requires_player_owner': 'CHAR_WHICHTYPE)!=CHAR_TYPEPLAYER' in default,
        'default_exit_reads_selected_roster_slot': 'pno=CHAR_getInt(charaindex,CHAR_DEFAULTPET)' in default,
        'default_exit_negative_selection_noop': 'if(pno<0)return0' in default,
        'default_exit_resolves_selected_pet': 'pindex=CHAR_getCharPet(charaindex,pno)' in default,
        'default_exit_delegates_to_battle_exit': 'iRet=BATTLE_Exit(pindex,battleindex)' in default,
        'default_exit_has_no_hp_or_owned_pet_deletion': all(t not in default for t in ('CHAR_HP','CHAR_endCharOneArray','CHAR_setCharPet')),
        'battle_exit_clears_matching_entry': 'if(pEntry[i].charaindex!=charaindex)continue;pEntry[i].charaindex=-1' in exit_body,
        'battle_exit_resets_entry_escape': 'pEntry[i].escape=0' in exit_body,
        'battle_exit_sets_final_mode_and_invalid_battle': all(t in exit_body for t in ('CHAR_WORKBATTLEMODE,BATTLE_CHARMODE_FINAL','CHAR_WORKBATTLEINDEX,-1')),
        'recall_noreturn_precedes_default_exit': 0<=recall.find('CHAR_BATTLEFLG_NORETURN')<recall.find('BATTLE_PetDefaultExit('),
        'recall_clears_selection_after_default_exit': 0<=recall.find('BATTLE_PetDefaultExit(')<recall.find('CHAR_setInt(attackindex,CHAR_DEFAULTPET,-1)'),
    }


def audit_profile(name, root):
    root=Path(root).resolve()
    head=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()
    dirty=subprocess.check_output(['git','-C',str(root),'status','--porcelain'],text=True).strip()
    if head!=PINNED[name] or dirty:
        raise ValueError('clean exact pinned checkout required: '+name)
    base=root/LAYOUTS[name]
    battle=(base/'battle/battle.c').read_text(encoding='utf-8')
    event=(base/'battle/battle_event.c').read_text(encoding='utf-8')
    gates=lifecycle_gates(battle,event)
    if not all(gates.values()):
        raise ValueError('lifecycle gates failed: '+name+' '+str([k for k,v in gates.items() if not v]))
    return [f'PROFILE|name={name}|sha={head}',
        *[f'GATE|profile={name}|name={k}|pass=1' for k in gates],
        f'SOURCE_SHA256|profile={name}|file=battle|sha256={_sha(base/"battle/battle.c")}',
        f'SOURCE_SHA256|profile={name}|file=event|sha256={_sha(base/"battle/battle_event.c")}']


def main():
    parser=argparse.ArgumentParser()
    for name in PINNED: parser.add_argument('--'+name+'-dir',type=Path,required=True)
    args=parser.parse_args()
    rows=['StoneAge 2BattleTimid normal-pet recall lifecycle source audit — R1',
          'Derived facts only; original source remains transient.']
    for name in PINNED: rows.extend(audit_profile(name,getattr(args,name+'_dir')))
    rows.extend([
        'FACT|default_pet_exit_requires_player_owner_and_selected_roster_slot',
        'FACT|pet_exit_clears_battle_entry_escape_mode_and_battle_index_not_owned_pet_membership',
        'FACT|noreturn_skips_exit_before_owner_defaultpet_clear',
        'BOUNDARY|textual_source_gates_only_not_full_native_server_execution',
        'BOUNDARY|normal_nontransformed_valid_owner_selected_pet_and_live_battle_only',
        'RESOLUTION|2BATTLETIMID_NORMAL_PET_RECALL_LIFECYCLE_SOURCE_CLOSED',
    ])
    print('\n'.join(rows))


if __name__=='__main__': main()
