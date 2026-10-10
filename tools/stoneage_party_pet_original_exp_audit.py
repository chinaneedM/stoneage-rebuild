"""Bounded native original EXP transfer; no full Finish or historical promotion."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re
from tools import stoneage_party_pet_original_attack_audit as attack
from tools import stoneage_party_pet_original_lethal_loop_audit as lethal

ANCHOR='memcpy(slots,round_baseline,sizeof round_baseline);*battle=round_arena;rng_count=round_rng;rng_mode=round_rng_mode;'
EXP_OBSERVATIONS=r'''
  {
    Char saved_exp[7];memcpy(saved_exp,slots,sizeof saved_exp);
    BATTLE saved_exp_arena=*battle;
    for(int case_id=0;case_id<9;case_id++){
      memcpy(slots,saved_exp,sizeof saved_exp);
      int recipient=(case_id==2||case_id==6)?2:0;
      int raw=(case_id==3)?-1:((case_id==4)?0:13);
      int bonus=(case_id==1||case_id==2)?50:0;
      slots[0].workint[CHAR_WORKITEM_ADDEXP]=bonus;
      slots[2].workint[CHAR_WORKITEM_ADDEXP]=99;
      slots[recipient].workint[CHAR_WORKGETEXP]=raw;
      slots[recipient].data[CHAR_EXP]=(case_id==5)?(PROFILE_EXP_CAP-5):100;
      slots[recipient].data[CHAR_LV]=(case_id==7)?CHAR_MAXUPLEVEL:10;
      slots[2].data[CHAR_PETID]=(case_id==6)?1163:1;
      SET_MULTIPLIER
      Char expected_exp[7];memcpy(expected_exp,slots,sizeof expected_exp);
      int expected_add=PROFILE_EXPECTED;
      int expected_total=(case_id==5&&expected_add>5)?PROFILE_EXP_CAP:slots[recipient].data[CHAR_EXP]+expected_add;
      expected_exp[recipient].data[CHAR_EXP]=expected_total;
      expected_exp[recipient].workint[CHAR_WORKGETEXP]=expected_add;
      int actual_add=BATTLE_GetExp(recipient,0);
      demand(actual_add==expected_add,"original source-profile EXP return oracle");
      demand(!memcmp(expected_exp,slots,sizeof expected_exp),"complete seven actor EXP write oracle");
      demand(!memcmp(&saved_exp_arena,battle,sizeof saved_exp_arena),"EXP preserves full arena");
      printf("REAL_HEADER_EXP_TRANSFER|mode=%d|battle=%d|case=%d|recipient=%d|raw=%d|bonus=%d|returned=%d|persistent=%d|whole_actor_oracle=1|arena_unchanged=1\n",mode,battle_at,case_id,recipient,raw,bonus,actual_add,slots[recipient].data[CHAR_EXP]);fflush(stdout);
    }
    memcpy(slots,saved_exp,sizeof saved_exp);
    demand(BATTLE_GetExp(-1,0)==0,"invalid EXP recipient returns zero");
    demand(!memcmp(saved_exp,slots,sizeof saved_exp),"invalid EXP recipient has no actor effect");
    demand(!memcmp(&saved_exp_arena,battle,sizeof saved_exp_arena),"invalid EXP recipient preserves arena");
  }
'''

def getter_definition(cfg):
    body=attack.definition(cfg,'getBattleexp')
    index=cfg.index(body)
    if cfg[max(0,index-9):index]=='unsigned ':body='unsigned '+body
    return body

def original_exp_parts(profile,battle,root):
    base=attack.pp_file(profile,root,attack.LAYOUTS[profile]/'char/char_base.c')
    cfg=attack.pp_file(profile,root,attack.LAYOUTS[profile]/('configfile.c' if profile=='gavin' else 'config_file.c'))
    bodies={'BATTLE_GetExp':attack.definition(battle,'BATTLE_GetExp'),
            'CHAR_AddMaxExp':attack.definition(base,'CHAR_AddMaxExp'),
            'getBattleexp':getter_definition(cfg)}
    declarations=''
    if profile=='gavin':
        m=re.search(r'typedef struct tagConfig\s*\{[^{}]+\}\s*Config\s*;',cfg)
        if not m:raise ValueError('original config structure missing')
        declarations=m[0]+'\nConfig config;\n'
    else:
        data=attack.pp_file(profile,root,attack.LAYOUTS[profile]/'char/char_data.c')
        m=re.search(r'static int LevelUpTbl\s*\[[^;]*?;',data,re.S)
        if not m:raise ValueError('original level EXP table missing')
        declarations=m[0]+'\n'
        bodies['CHAR_GetLevelExp']=attack.definition(data,'CHAR_GetLevelExp')
    frozen=json.loads((Path(__file__).resolve().parents[1]/'research/recovered/STONEAGE-PARTY-PET-ORIGINAL-EXP-SOURCE-R1.json').read_text())[profile]
    validate_parts(declarations,bodies,frozen)
    return declarations,bodies

def validate_parts(declarations,bodies,frozen):
    actual={'declarations_sha256':hashlib.sha256(declarations.encode()).hexdigest(),
            'bodies':{n:hashlib.sha256(b.encode()).hexdigest() for n,b in bodies.items()}}
    if actual!=frozen:raise ValueError('original EXP body/config/level-table drift')
    return actual

def exp_observations(profile):
    text=EXP_OBSERVATIONS
    if profile=='gavin':
        text=text.replace('SET_MULTIPLIER','config.battleexp=(case_id==8)?3:1;')
        oracle='(case_id==6||case_id==7||raw<0)?0:(raw+(raw*bonus)/100)*((case_id==8)?3:1)'
    else:
        text=text.replace('SET_MULTIPLIER','')
        oracle='(case_id==6||case_id==7||raw<0)?0:1000000'
    return text.replace('PROFILE_EXPECTED',oracle).replace('PROFILE_EXP_CAP','1073741824' if profile=='bismarck' else '1224160000')

def exp_native(profile,source,battle,event,root):
    native,has_lua=lethal.lethal_round_native(profile,source,battle,event,root)
    # Only the dedicated lethal observation contains this restoration anchor.
    previous=lethal.LETHAL_ROUND_OBSERVATIONS.replace('EXPECTED_WIN_SIDE','-1' if profile=='bismarck' else '0').replace('ENTRY_FIELD','char_index' if profile=='bismarck' else 'charaindex')
    if native.count(previous)!=1 or previous.count(ANCHOR)!=1:
        raise ValueError('accepted lethal observation restoration drift')
    native=native.replace(previous,previous.replace(ANCHOR,exp_observations(profile)+ANCHOR,1),1)
    declarations,bodies=original_exp_parts(profile,battle,root)
    for name,body in bodies.items():
        print(f'EXP_SOURCE|{profile}|{name}|sha256={hashlib.sha256(body.encode()).hexdigest()}',flush=True)
    print(f'EXP_DECLARATIONS|{profile}|sha256={hashlib.sha256(declarations.encode()).hexdigest()}',flush=True)
    entry='int main(int argc,char **argv){'
    if native.count(entry)!=1:raise ValueError('native main drift')
    # Declare every original signature before the unchanged body dependency.
    signatures='\n'.join(b[:b.index('{')].strip()+';' for b in bodies.values())
    native=native.replace(entry,declarations+signatures+'\n'+'\n'.join(bodies.values())+'\n'+entry,1)
    return native,has_lua

def main():
    attack.main(native_builder=exp_native,extra_markers=('REAL_HEADER_EXP_TRANSFER|',))
    for profile in ('gavin','bismarck'):
        # Whole original source bodies and declarations were fingerprinted above.
        print('EXP_BOUNDARY|'+profile+'|direct_original_GetExp;no_LevelUp_or_Finish_dispatch;empty_equipment')
    print('RESOLUTION|ORIGINAL_REAL_HEADER_EXP_TRANSFER_BOUNDED_PASS')

if __name__=='__main__':main()
