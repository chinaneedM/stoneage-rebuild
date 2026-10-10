"""Bounded original pet EXP/level/growth in actual second Loop Finish.

Only extraction, controlled fixture inputs, strict presentation/RNG collection
and independent whole-state oracles are committed; original bodies stay transient.
"""
from __future__ import annotations
import hashlib,json
from pathlib import Path
from tools import stoneage_party_pet_original_player_level_audit as player
from tools import stoneage_party_pet_original_attack_audit as attack

replace_once=player.replace_once
GROWTH=((103,148,189,234),(138,198,252,312),(206,296,378,468),(0,0,0,0))
DERIVED=((101,126,127,102,709),(101,127,128,103,713),(102,128,129,104,719),(100,125,125,100,700))
VARIABLE_SEEDS=(9800,1000,9500,1000)
VARIABLE_FINAL=(10000,1500,10000,1000)

PET_PREP=r'''
  static const int pet_exp_seed[4]={PET_SEEDS};
  static const int pet_var_seed[4]={9800,1000,9500,1000};
  static const int pet_var_final[4]={10000,1500,10000,1000};
  static const int pet_growth[4][4]={{103,148,189,234},{138,198,252,312},{206,296,378,468},{0,0,0,0}};
  static const int pet_derived[4][5]={{101,126,127,102,709},{101,127,128,103,713},{102,128,129,104,719},{100,125,125,100,700}};
  slots[2].data[CHAR_EXP]=pet_exp_seed[mode];slots[2].workint[CHAR_WORKGETEXP]=1;
  slots[2].data[CHAR_PETID]=1;slots[2].data[CHAR_LIMITLEVEL]=0;
  slots[2].data[CHAR_ALLOCPOINT]=(20<<24)+(30<<16)+(40<<8)+50;
  slots[2].data[CHAR_PETRANK]=(mode==1)?5:((mode==2)?6:0);
  slots[2].data[CHAR_VARIABLEAI]=pet_var_seed[mode];
  slots[2].data[CHAR_VITAL]=slots[2].data[CHAR_STR]=slots[2].data[CHAR_TOUGH]=slots[2].data[CHAR_DEX]=10000;
  slots[0].data[CHAR_FMLEADERFLAG]=0;slots[0].data[CHAR_TRANSMIGRATION]=0;
  slots[0].data[CHAR_FAME]=7;slots[2].data[CHAR_FAME]=11;
  GAVIN_MOMENTUM
  CHAR_complianceParameter(2);
  demand(slots[2].workint[CHAR_WORKFIXAI]==100,"pet fixed AI100 fixture");
  pet_rng_count=pet_loop_rng=0;pet_rng_expected=11*up;pet_rng_rank_max=(mode==1);
'''

PET_EXPECTED=r'''
  expected_finish[2].data[CHAR_EXP]=expected_residual[mode];
  expected_finish[2].workint[CHAR_WORKGETEXP]=payout;
  expected_finish[2].data[CHAR_LV]=100+up;
  expected_finish[2].data[CHAR_VARIABLEAI]=pet_var_final[mode];
  expected_finish[2].data[CHAR_VITAL]=10000+pet_growth[mode][0];
  expected_finish[2].data[CHAR_STR]=10000+pet_growth[mode][1];
  expected_finish[2].data[CHAR_TOUGH]=10000+pet_growth[mode][2];
  expected_finish[2].data[CHAR_DEX]=10000+pet_growth[mode][3];
  expected_finish[2].workint[CHAR_WORKFIXVITAL]=pet_derived[mode][0];
  expected_finish[2].workint[CHAR_WORKFIXSTR]=expected_finish[2].workint[CHAR_WORKATTACKPOWER]=pet_derived[mode][1];
  expected_finish[2].workint[CHAR_WORKFIXTOUGH]=expected_finish[2].workint[CHAR_WORKDEFENCEPOWER]=pet_derived[mode][2];
  expected_finish[2].workint[CHAR_WORKFIXDEX]=expected_finish[2].workint[CHAR_WORKQUICK]=pet_derived[mode][3];
  expected_finish[2].workint[CHAR_WORKMAXHP]=pet_derived[mode][4];
  PET_FAME_EXPECTED
'''

PET_OBSERVE=r'''
  demand(pet_rng_count==11*up,"exact original pet growth11 draws per level and0 negative control");
  demand(pet_loop_rng==1,"original Loop unconditional rand distinct from growth");
  printf("REAL_HEADER_PET_GROWTH|mode=%d|battle=%d|levels=%d|pet_lv=%d|pet_exp=%d|pet_raw=%d|pet_payout=%d|vital=%d|str=%d|tough=%d|dex=%d|variable_ai=%d|fixed_ai=%d|attack=%d|defense=%d|quick=%d|maxhp=%d|rng=%d|loop_rng=1|owner_fame=%d|pet_fame=%d|whole_actor_oracle=1|whole_arena_oracle=1|released=1\n",
   mode,battle_at,up,slots[2].data[CHAR_LV],slots[2].data[CHAR_EXP],1,payout,
   slots[2].data[CHAR_VITAL],slots[2].data[CHAR_STR],slots[2].data[CHAR_TOUGH],slots[2].data[CHAR_DEX],
   slots[2].data[CHAR_VARIABLEAI],slots[2].workint[CHAR_WORKFIXAI],slots[2].workint[CHAR_WORKATTACKPOWER],slots[2].workint[CHAR_WORKDEFENCEPOWER],slots[2].workint[CHAR_WORKQUICK],slots[2].workint[CHAR_WORKMAXHP],pet_rng_count,slots[0].data[CHAR_FAME],slots[2].data[CHAR_FAME]);
  pet_rng_phase=0;
'''

def pet_observations(profile):
    text=player.level_observations(profile)
    prep=PET_PREP.replace('PET_SEEDS',','.join(str(c[0]) for c in player.fixture_cases(profile)))
    prep=prep.replace('GAVIN_MOMENTUM','slots[0].data[CHAR_MOMENTUM]=9;slots[2].data[CHAR_MOMENTUM]=13;' if profile=='gavin' else '')
    text=replace_once(text,'  Char expected_finish[7];',prep+'  Char expected_finish[7];')
    expected=PET_EXPECTED.replace('PET_FAME_EXPECTED','expected_finish[0].data[CHAR_FAME]+=(mode==2?134:(up?62:0));expected_finish[2].data[CHAR_FAME]=11+(mode==1?67:(mode==2?139:0));' if profile=='bismarck' else '')
    text=replace_once(text,'  expected_finish[2].workint[CHAR_WORKBATTLEMODE]',expected+'  expected_finish[2].workint[CHAR_WORKBATTLEMODE]')
    text=replace_once(text,'finish_transport_phase=1;','finish_transport_phase=1;pet_rng_phase=1;')
    text=replace_once(text,'finish_rs_count==2&&finish_status_count==1','finish_rs_count==2&&finish_status_count==(up?1:0)')
    payout='4c92' if profile=='bismarck' else '1'
    original=f'(up?"-2|1|{payout},,,,,|||":"-2|0|{payout},,,,,|||")'
    pet_packet=f'(up?"-2|1|{payout},0|1|{payout},,,,|||":"-2|0|{payout},0|0|{payout},,,,|||")'
    text=replace_once(text,original,pet_packet)
    text=replace_once(text,'  finish_transport_phase=0;',PET_OBSERVE+'  finish_transport_phase=0;')
    return text

def original_parts(profile,root):
    data=attack.pp_file(profile,root,attack.LAYOUTS[profile]/'char/char_data.c')
    char=attack.pp_file(profile,root,attack.LAYOUTS[profile]/'char/char.c')
    base=attack.pp_file(profile,root,attack.LAYOUTS[profile]/'char/char_base.c')
    return {'CHAR_PetLevelUp':attack.definition(data,'CHAR_PetLevelUp'),
            'CHAR_CheckPetDoLimitlevel':attack.definition(data,'CHAR_CheckPetDoLimitlevel'),
            'CHAR_PetAddVariableAi':attack.definition(char,'CHAR_PetAddVariableAi'),
            'CHAR_earnFame':attack.definition(base,'CHAR_earnFame')}

def pet_native(profile,source,battle,event,root):
    native,has_lua=player.level_native(profile,source,battle,event,root)
    field='char_index' if profile=='bismarck' else 'charaindex'
    native=replace_once(native,player.level_observations(profile).replace('ENTRY_FIELD',field),pet_observations(profile).replace('ENTRY_FIELD',field))
    rng=attack.definition(native,'audit_rand')
    stream=r'''if(pet_rng_phase){
 /* Original Loop starts with one discarded rand, before any pet growth. */
 if(!pet_loop_rng){pet_loop_rng=1;int vals[]={0,1073741824,2147483647,536870912};rng_count++;return vals[rng_mode];}
 if(pet_rng_count>=pet_rng_expected){fputs("PET_RNG_OVERFLOW",stderr);abort();}
 int at=pet_rng_count++%11;
 if(at==10)return pet_rng_rank_max?2147483647:0;
 int draws[]={0,536870912,1073741824,1610612736};return draws[at%4];
 }'''
    native=replace_once(native,rng,rng.replace('{','{'+stream,1))
    native='static int pet_rng_phase,pet_rng_count,pet_rng_expected,pet_rng_rank_max,pet_loop_rng;\n'+native
    bodies=original_parts(profile,root)
    frozen=Path(__file__).resolve().parents[1]/'research/recovered/STONEAGE-PARTY-PET-ORIGINAL-PET-GROWTH-SOURCE-R1.json'
    player.validate_bodies(bodies,json.loads(frozen.read_text())[profile])
    for name,body in bodies.items():
        try:previous=attack.definition(native,name)
        except ValueError:pass
        else:native=replace_once(native,previous,'')
        print(f'PET_GROWTH_SOURCE|{profile}|{name}|sha256={hashlib.sha256(body.encode()).hexdigest()}',flush=True)
    entry='int main(int argc,char **argv){'
    # Empty family membership makes account/clan branch unreachable. Preserve
    # complete original family structure, with zeroed transient fixture storage.
    declarations='int acfd;\n'
    if profile=='gavin':
        native='#include "family.h"\n#include "saacproto_cli.h"\n'+native
        declarations+='struct FM_POINTLIST fmpointlist;\n'
    else:
        native='#include "family.h"\n#include "saac_client.h"\n'+native
    signatures='\n'.join(b[:b.index('{')].strip()+';' for b in bodies.values())
    native=signatures+'\n'+native
    native=replace_once(native,entry,declarations+'\n'+'\n'.join(bodies.values())+'\n'+entry)
    return native,has_lua

def main():
    attack.main(native_builder=pet_native,extra_markers=('REAL_HEADER_LETHAL_LOOP|','REAL_HEADER_FINISH_DISPATCH|','FINISH_RS_OBS|','REAL_HEADER_PLAYER_LEVEL|','REAL_HEADER_PET_GROWTH|'))
    print('BOUNDARY|pet_raw_EXP1_fixture;seeded_EXP;explicit_alloc_points_rank_rand_stream;empty_equipment_items_family;no_special_petIDs_or_natural_RNG_historical_promotion')
    print('RESOLUTION|ORIGINAL_REAL_HEADER_PET_GROWTH_BOUNDED_PASS')

if __name__=='__main__':main()
