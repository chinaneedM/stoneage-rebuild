"""Original second Loop Finish with bounded positive PLAYER level effects.

Original gameplay bodies remain unchanged and transient. Presentation adapters
collect exact typed calls; full actor/arena oracles are independently specified.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from tools import stoneage_party_pet_original_finish_dispatch_audit as finish
from tools import stoneage_party_pet_original_attack_audit as attack

# Bismarck original cumulative table deltas at levels101/102. Gavin uses the
# accepted explicitly synthetic threshold10000000, not an operator table.
THRESHOLDS={'gavin':(10000000,10000000),'bismarck':(1345723,1442322)}
PAYOUTS={'gavin':1,'bismarck':1000000}

def fixture_cases(profile):
    first,second=THRESHOLDS[profile];payout=PAYOUTS[profile]
    # exact threshold, residual17, two levels/residual23, one-below threshold.
    return [(first-payout,1,0,98),(first-payout+17,1,17,97),
            (first+second-payout+23,2,23,99),(first-payout-1,0,first-1,96)]

def replace_once(text,old,new):
    if text.count(old)!=1:raise ValueError('player level fixture anchor drift: '+old[:70])
    return text.replace(old,new,1)

def validate_bodies(bodies,expected):
    actual={n:hashlib.sha256(b.encode()).hexdigest() for n,b in bodies.items()}
    if actual!=expected:raise ValueError('original player level dependency drift')
    return actual

PREP=r'''
  static const int seed_exp[4]={SEEDS};
  static const int expected_levels[4]={1,1,2,0};
  static const int expected_residual[4]={RESIDUALS};
  static const int seed_charm[4]={98,97,99,96};
  int up=expected_levels[mode],payout=PLAYER_PAYOUT;
  int previous_leader_self=slots[0].workint[CHAR_WORKPARTYINDEX1];
  int previous_member_owner=slots[1].workint[CHAR_WORKPARTYINDEX1];
  /* Explicit post-lethal complete party roster fixture for original update. */
  slots[0].workint[CHAR_WORKPARTYINDEX1]=0;
  slots[1].workint[CHAR_WORKPARTYINDEX1]=0;
  slots[0].data[CHAR_EXP]=seed_exp[mode];
  slots[0].data[CHAR_SKILLUPPOINT]=10;slots[0].data[CHAR_DUELPOINT]=500;
  slots[0].data[CHAR_CHARM]=seed_charm[mode];
  FAME_PREP
  CHAR_complianceParameter(0);CHAR_complianceParameter(2);
  demand(slots[2].workint[CHAR_WORKFIXAI]==100,"owned pet AI capped before player upgrade fixture");
  level_p_count=level_n_count=level_exit_n_count=level_exit_p_count=level_image_p_count=0;
  int previous_world_broadcasts=world_broadcasts;
'''

EXPECTED=r'''
  expected_finish[0].data[CHAR_EXP]=expected_residual[mode];
  expected_finish[0].data[CHAR_LV]=100+up;
  expected_finish[0].data[CHAR_SKILLUPPOINT]=10+up*3;
  expected_finish[0].data[CHAR_DUELPOINT]=500+(up?1010:0)+(up==2?1020:0);
  int expected_charm=seed_charm[mode]+(up?2:0);
  if(expected_charm>100)expected_charm=100;
  expected_finish[0].data[CHAR_CHARM]=expected_charm;
  expected_finish[0].workint[CHAR_WORKFIXCHARM]=expected_charm;
  FAME_EXPECTED
'''

OBSERVED=r'''
  printf("LEVEL_PRESENTATION_COUNTS|mode=%d|upgrade_p=%d|exit_p=%d|image_p=%d|upgrade_n=%d|exit_n=%d|world=%d\n",mode,level_p_count,level_exit_p_count,level_image_p_count,level_n_count,level_exit_n_count,world_broadcasts-previous_world_broadcasts);fflush(stdout);
  demand(level_p_count==(up?1:0),"exact upgrade P status mask/actor count");
  demand(level_n_count==(up?1:0),"original PartyUpdate exact teammate N status count");
  demand(level_exit_n_count==2,"original Exit exact party HP update count");
  demand(level_exit_p_count==2&&level_image_p_count==0,"exact two-player Exit masks and no BecomePig image status");
  demand(world_broadcasts-previous_world_broadcasts==(up?1:0),"exact upgrade broadcast without BecomePig Exit broadcasts");
  demand(slots[0].data[CHAR_EXP]==expected_residual[mode]&&slots[0].data[CHAR_LV]==100+up,"independent positive level and remaining EXP");
  printf("REAL_HEADER_PLAYER_LEVEL|mode=%d|battle=%d|seed_exp=%d|payout=%d|levels=%d|lv=%d|residual=%d|skill=%d|charm=%d|duel=%d|fame=%d|pet_lv=%d|pet_exp=%d|status_calls=%d|party_calls=%d|whole_actor_oracle=1|whole_arena_oracle=1|released=1\n",
    mode,battle_at,seed_exp[mode],payout,up,slots[0].data[CHAR_LV],slots[0].data[CHAR_EXP],
    slots[0].data[CHAR_SKILLUPPOINT],slots[0].data[CHAR_CHARM],slots[0].data[CHAR_DUELPOINT],
    FAME_OBS,slots[2].data[CHAR_LV],slots[2].data[CHAR_EXP],level_p_count,level_n_count);
'''

PARTY_COLLECTOR=r'''
static int level_n_count,level_exit_n_count;
BOOL CHAR_send_N_StatusString(int actor,int party_slot,unsigned int mask){
 if(!finish_transport_phase||CHAR_getWorkInt(0,CHAR_WORKPARTYINDEX1)!=0||CHAR_getWorkInt(0,CHAR_WORKPARTYINDEX2)!=1||CHAR_getWorkInt(1,CHAR_WORKPARTYINDEX1)!=0){fputs("LEVEL_PARTY_STATUS_SCOPE_VIOLATION",stderr);abort();}
 if(mask==CHAR_N_STRING_LV&&actor==1&&party_slot==0)level_n_count++;
 else if(mask==CHAR_N_STRING_HP&&((actor==1&&party_slot==0)||(actor==0&&party_slot==1)))level_exit_n_count++;
 else{fprintf(stderr,"LEVEL_PARTY_MASK_BAD|actor=%d|slot=%d|mask=%u\n",actor,party_slot,mask);abort();}
 return TRUE;
}
'''

def level_observations(profile):
    cases=fixture_cases(profile)
    text=finish.finish_observations(profile)
    prep=PREP.replace('SEEDS',','.join(str(c[0]) for c in cases)).replace('RESIDUALS',','.join(str(c[2]) for c in cases)).replace('PLAYER_PAYOUT',str(PAYOUTS[profile]))
    prep=prep.replace('FAME_PREP','slots[0].data[CHAR_FAME]=7;' if profile=='bismarck' else '')
    text=replace_once(text,'  Char expected_finish[7];',prep+'  Char expected_finish[7];')
    expected=EXPECTED.replace('FAME_EXPECTED','expected_finish[0].data[CHAR_FAME]=7+(mode==1?67:(mode==2?139:0));' if profile=='bismarck' else '')
    text=replace_once(text,'  expected_finish[2].workint[CHAR_WORKBATTLEMODE]',expected+'  expected_finish[2].workint[CHAR_WORKBATTLEMODE]')
    packet='"-2|0|4c92,,,,,|||"' if profile=='bismarck' else '"-2|0|1,,,,,|||"'
    upgrade='"-2|1|4c92,,,,,|||"' if profile=='bismarck' else '"-2|1|1,,,,,|||"'
    text=replace_once(text,'strcmp(finish_rs_text[0],'+packet+')','strcmp(finish_rs_text[0],(up?'+upgrade+':'+packet+'))')
    text=replace_once(text,'  finish_transport_phase=0;',OBSERVED.replace('FAME_OBS','slots[0].data[CHAR_FAME]' if profile=='bismarck' else '-1')+'  finish_transport_phase=0;\n  slots[0].workint[CHAR_WORKPARTYINDEX1]=previous_leader_self;slots[1].workint[CHAR_WORKPARTYINDEX1]=previous_member_owner;')
    return text

def level_native(profile,source,battle,event,root):
    native,has_lua=finish.finish_native(profile,source,battle,event,root)
    recovered=Path(__file__).resolve().parents[1]/'research/recovered'
    prior=json.loads((recovered/'STONEAGE-PARTY-PET-ORIGINAL-FINISH-DISPATCH-ACCEPTANCE-R3.json').read_text())['original_function_sha256'][profile]
    validate_bodies({n:attack.definition(native,n) for n in ('BATTLE_GetExpGold','CHAR_LevelUpCheck','CHAR_HandleExp','CHAR_GetLevelExp')},{n:prior[n] for n in ('BATTLE_GetExpGold','CHAR_LevelUpCheck','CHAR_HandleExp','CHAR_GetLevelExp')})
    field='char_index' if profile=='bismarck' else 'charaindex'
    native=replace_once(native,finish.finish_observations(profile).replace('ENTRY_FIELD',field),level_observations(profile).replace('ENTRY_FIELD',field))
    # Preserve the inherited status collector outside this dedicated Finish
    # phase; upgrade P status is an exact actor/mask typed output collection.
    status=attack.definition(native,'CHAR_send_P_StatusString')
    insert=f'''if(finish_transport_phase){{
 if({field}!=0&&{field}!=1)abort();
 if(indextable==(CHAR_P_STRING_LV|CHAR_P_STRING_NEXTEXP|CHAR_P_STRING_DUELPOINT)){{if({field}!=0)abort();level_p_count++;}}
 else if(indextable==CHAR_P_STRING_BASEBASEIMAGENUMBER)level_image_p_count++;
 else if(indextable==(CHAR_P_STRING_HP|CHAR_P_STRING_EXP|CHAR_P_STRING_MP|CHAR_P_STRING_DUELPOINT|CHAR_P_STRING_CHARM|CHAR_P_STRING_EARTH|CHAR_P_STRING_WATER|CHAR_P_STRING_FIRE|CHAR_P_STRING_WIND|CHAR_P_STRING_RIDEPET))level_exit_p_count++;
 else abort();
 }}'''
    native=replace_once(native,status,status.replace('{','{'+insert,1))
    native='static int level_p_count,level_exit_p_count,level_image_p_count;\n'+native
    bodies={}
    char=attack.pp_file(profile,root,attack.LAYOUTS[profile]/'char/char.c')
    bodies['CHAR_PartyUpdate']=attack.definition(char,'CHAR_PartyUpdate')
    if profile=='bismarck':
        party=attack.pp_file(profile,root,attack.LAYOUTS[profile]/'char/char_party.c')
        bodies['getPartyNum']=attack.definition(party,'getPartyNum')
        base=attack.pp_file(profile,root,attack.LAYOUTS[profile]/'char/char_base.c')
        bodies['CHAR_earnFame']=attack.definition(base,'CHAR_earnFame')
    validate_bodies(bodies,json.loads((recovered/'STONEAGE-PARTY-PET-ORIGINAL-PLAYER-LEVEL-SOURCE-R1.json').read_text())[profile])
    for name,body in bodies.items():
        try:prior=attack.definition(native,name)
        except ValueError:pass
        else:native=replace_once(native,prior,'')
        print(f'LEVEL_SOURCE|{profile}|{name}|sha256={hashlib.sha256(body.encode()).hexdigest()}',flush=True)
    entry='int main(int argc,char **argv){'
    native=replace_once(native,entry,PARTY_COLLECTOR+'\n'+'\n'.join(bodies.values())+'\n'+entry)
    return native,has_lua

def main():
    attack.main(native_builder=level_native,extra_markers=('REAL_HEADER_LETHAL_LOOP|','REAL_HEADER_FINISH_DISPATCH|','FINISH_RS_OBS|','REAL_HEADER_PLAYER_LEVEL|'))
    print('BOUNDARY|positive_player_levels_only;seeded_EXP;synthetic_Gavin_thresholds;original_Bismarck_table;empty_items;typed_presentation_collectors;no_pet_growth_or_historical_promotion')
    print('RESOLUTION|ORIGINAL_REAL_HEADER_PLAYER_LEVEL_BOUNDED_PASS')

if __name__=='__main__':main()
