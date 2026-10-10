"""Original positive reward-item transfer in bounded terminal Finish fixtures.

Whole original item/Char/BATTLE layouts; gameplay bodies extracted transiently.
Presentation is collected, not a live transport. Item creation/drop allocation
and pre-existing ownership rejection remain independent open gates.
"""
from __future__ import annotations
import hashlib,json,re
from pathlib import Path
from tools import stoneage_party_pet_original_pet_growth_audit as pet
from tools import stoneage_party_pet_original_attack_audit as attack
replace_once=pet.replace_once
GROUPS={
 'char/char_item.c':('CHAR_findEmptyItemBoxFromChar','CHAR_findEmptyItemBox','CHAR_addItemSpecificItemIndex'),
 'char/char_base.c':('_CHAR_setItemIndex','_CHAR_CHECKITEMINDEX','_CHAR_getItemIndex','CHAR_getPlayerMaxNum','ITEM_setItemUniCode'),
 'item/item.c':('ITEM_CHECKARRAYINDEX','_ITEM_CHECKINDEX','ITEM_CHECKINTDATAINDEX','ITEM_CHECKCHARDATAINDEX','_ITEM_endExistItemsOne','_ITEM_getInt','ITEM_getChar','ITEM_getWorkInt','ITEM_setWorkInt','ITEM_getAppropriateName'),
}
def original_parts(profile,root):
    bodies={}
    for path,names in GROUPS.items():
        text=attack.pp_file(profile,root,attack.LAYOUTS[profile]/path)
        bodies.update({n:attack.definition(text,n) for n in names})
    util=attack.pp_file(profile,root,attack.LAYOUTS[profile]/'util.c' if profile=='gavin' else attack.LAYOUTS[profile].parent/'common/utils/util_string.c')
    bodies['makeEscapeString']=attack.definition(util,'makeEscapeString')
    bodies['escape_table']=re.search(r'typedef struct tagEscapeChar\s*\{[^{}]+\}\s*EscapeChar;\s*static EscapeChar \w+\[\]\s*=\s*\{.*?\};',util,re.S)[0]
    return bodies

PREP=r'''
  for(int a=0;a<2;a++)for(int j=0;j<CHAR_MAXITEMHAVE;j++)slots[a].indexOfExistItems[j]=-1;
  memset(reward_items,0,sizeof reward_items);ITEM_ARRAY=reward_items;ITEM_SIZE=256;ITEM_COUNT=1;
  reward_items[250].use=1;
  reward_items[250].ITEM_FIELD.data[ITEM_ID]=731;
  reward_items[250].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]=-1;
  reward_items[250].ITEM_FIELD.workint[ITEM_WORKOBJINDEX]=19;
  reward_items[250].ITEM_FIELD.workint[ITEM_WORKTIMELIMIT]=0;
  strcpy(reward_items[250].ITEM_FIELD.string[ITEM_NAME].string,"Reward");
  strcpy(reward_items[250].ITEM_FIELD.string[ITEM_UNIQUECODE].string,"bounded");
  int reward_actor=mode==2?1:0;
  int reward_slot=CHAR_STARTITEMARRAY;
  int reward_limit=ITEM_LIMIT;
  if(mode==1)for(int j=CHAR_STARTITEMARRAY;j<reward_limit;j++){
    slots[0].indexOfExistItems[j]=j;reward_items[j].use=1;
    reward_items[j].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]=0;ITEM_COUNT++;
  }
  if(mode==3){slots[0].indexOfExistItems[CHAR_STARTITEMARRAY]=249;STALE_SLOT}
  battle->Side[0].Entry[reward_actor].getitem[0]=250;
  ITEM_TYPE expected_items[256];memcpy(expected_items,reward_items,sizeof expected_items);
  int invalid_item_count=ITEM_COUNT;
  Char invalid_recipient_before[7];memcpy(invalid_recipient_before,slots,sizeof slots);
  demand(CHAR_addItemSpecificItemIndex(-1,250)==-1&&CHAR_addItemSpecificItemIndex(reward_actor,249)==-1,"invalid owner and inactive item rejected by original add");
  demand(ITEM_COUNT==invalid_item_count&&!memcmp(invalid_recipient_before,slots,sizeof slots)&&!memcmp(expected_items,reward_items,sizeof expected_items),"invalid recipient/item full state unchanged");
  int expected_item_count=ITEM_COUNT-(mode==1);
  if(mode==1){expected_items[250].use=0;expected_items[250].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]=-1;}
  else{expected_items[250].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]=reward_actor;expected_items[250].ITEM_FIELD.workint[ITEM_WORKOBJINDEX]=-1;}
  reward_log_count=reward_data_count=reward_one_count=0;reward_phase=1;reward_expected_actor=reward_actor;reward_expected_slot=reward_slot;
'''
OBSERVE=r'''
  demand(!memcmp(expected_items,reward_items,sizeof expected_items),"whole original item array oracle");
  demand(ITEM_COUNT==expected_item_count,"original live item count oracle");
  demand(reward_log_count==(mode!=1)&&reward_data_count==(mode!=1)&&reward_one_count==ONE_COUNT,"typed item log and transport counts");
  printf("REAL_HEADER_REWARD_ITEM|mode=%d|battle=%d|actor=%d|item=250|slot=%d|acquired=%d|use=%d|owner=%d|object=%d|item_logs=%d|item_data=%d|item_one=%d|whole_item_oracle=1|whole_actor_oracle=1|whole_arena_oracle=1|released=1\n",mode,battle_at,reward_actor,reward_slot,mode!=1,reward_items[250].use,reward_items[250].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX],reward_items[250].ITEM_FIELD.workint[ITEM_WORKOBJINDEX],reward_log_count,reward_data_count,reward_one_count);
  reward_phase=0;
'''
COLLECT=r'''
static int reward_phase,reward_expected_actor,reward_expected_slot,reward_log_count,reward_data_count,reward_one_count;
BOOL CHAR_sendItemData(int actor,int *indices,int count){
 if(!reward_phase||actor!=reward_expected_actor||count!=1||indices[0]!=reward_expected_slot)abort();reward_data_count++;return TRUE;
}
BOOL CHAR_sendItemDataOne(int actor,int slot){
 if(!reward_phase||actor!=reward_expected_actor||slot!=reward_expected_slot)abort();reward_one_count++;return TRUE;
}
void LogItem(char *name,char *key,int item,char *cause,int floor,int x,int y,char *code,char *itemname,int id){
 if(!reward_phase||item!=250||strcmp(code,"bounded")||strcmp(itemname,"Reward")||id!=731||!name||!key||floor!=slots[reward_expected_actor].data[CHAR_FLOOR]||x!=slots[reward_expected_actor].data[CHAR_X]||y!=slots[reward_expected_actor].data[CHAR_Y])abort();
 if(strcmp(cause,LOG_CAUSE))abort();reward_log_count++;
}
'''
def substitutions(profile,text):
    return (text.replace('ITEM_ARRAY','ITEM_gExists' if profile=='bismarck' else 'ITEM_item')
        .replace('ITEM_SIZE','ITEM_sItemNum' if profile=='bismarck' else 'ITEM_itemnum')
        .replace('ITEM_COUNT','ITEM_sUseItemNum' if profile=='bismarck' else 'ITEM_UseItemnum')
        .replace('ITEM_TYPE','ITEM_Exists' if profile=='bismarck' else 'ITEM_exists')
        .replace('ITEM_FIELD','item' if profile=='bismarck' else 'itm')
        .replace('ITEM_LIMIT','CheckCharMaxItem(0)' if profile=='bismarck' else 'CHAR_MAXITEMHAVE')
        .replace('STALE_SLOT','' if profile=='bismarck' else 'reward_slot++;')
        .replace('ONE_COUNT','(mode!=1)' if profile=='bismarck' else '0'))

def item_observations(profile):
    text=pet.pet_observations(profile)
    text=replace_once(text,'  Char expected_finish[7];',substitutions(profile,PREP)+'  Char expected_finish[7];')
    text=replace_once(text,'  BATTLE expected_final_arena=*battle;','  if(mode!=1)expected_finish[reward_actor].indexOfExistItems[reward_slot]=250;\n  BATTLE expected_final_arena=*battle;')
    text=replace_once(text,'  finish_transport_phase=0;',substitutions(profile,OBSERVE)+'  finish_transport_phase=0;')
    # Exact literal reward packet suffix; only selected recipient's first item.
    payout='4c92' if profile=='bismarck' else '1'
    old=f'demand(!strcmp(finish_rs_text[0],(up?"-2|1|{payout},0|1|{payout},,,,|||":"-2|0|{payout},0|0|{payout},,,,|||"))&&!strcmp(finish_rs_text[1],"-2|0|'+('4c92' if profile=='bismarck' else '0')+',,,,,|||"),"original reward text independent base62 oracle");'
    leader=f'(up?"-2|1|{payout},0|1|{payout},,,,":"-2|0|{payout},0|0|{payout},,,,")'
    member='"-2|0|'+('4c92' if profile=='bismarck' else '0')+',,,,,"'
    new=f'char expected_rs0[128],expected_rs1[128];snprintf(expected_rs0,sizeof expected_rs0,"%s%s",{leader},mode==0||mode==3?"Reward|||":"|||");snprintf(expected_rs1,sizeof expected_rs1,"%s%s",{member},mode==2?"Reward|||":"|||");printf("REWARD_PACKET_ORACLE|mode=%d|actual0=%s|expected0=%s|actual1=%s|expected1=%s\\n",mode,finish_rs_text[0],expected_rs0,finish_rs_text[1],expected_rs1);fflush(stdout);demand(!strcmp(finish_rs_text[0],expected_rs0)&&!strcmp(finish_rs_text[1],expected_rs1),"exact recipient reward item text");'
    return replace_once(text,old,new)

def item_native(profile,source,battle,event,root):
    native,has_lua=pet.pet_native(profile,source,battle,event,root)
    field='char_index' if profile=='bismarck' else 'charaindex'
    native=replace_once(native,pet.pet_observations(profile).replace('ENTRY_FIELD',field),item_observations(profile).replace('ENTRY_FIELD',field))
    bodies=original_parts(profile,root)
    frozen=Path(__file__).resolve().parents[1]/'research/recovered/STONEAGE-PARTY-PET-ORIGINAL-REWARD-ITEM-SOURCE-R1.json'
    pet.player.validate_bodies(bodies,json.loads(frozen.read_text())[profile])
    for name,body in bodies.items():
        print(f'REWARD_ITEM_SOURCE|{profile}|{name}|sha256={hashlib.sha256(body.encode()).hexdigest()}',flush=True)
        if name=='escape_table':continue
        try:previous=attack.definition(native,name)
        except ValueError:pass
        else:native=replace_once(native,previous,'')
    cause='"BattleGet(战斗後所得的道具)"'
    # Nonempty already assigned unique code and time-limit0 leave creation/time
    # dependencies untaken, with their original bodies and abort traps intact.
    decl=substitutions(profile,'static ITEM_TYPE reward_items[256];static int ITEM_COUNT,unique_i;\n')
    collectors=COLLECT.replace('LOG_CAUSE',cause)
    if profile=='bismarck':collectors=collectors.replace('char *','const char *')
    native=replace_once(native,'int main(int argc,char **argv){',decl+collectors+'\n'+bodies['escape_table']+'\n'+'\n'.join(b for n,b in bodies.items() if n!='escape_table')+'\nint main(int argc,char **argv){')
    signatures='\n'.join(b[:b.index('{')].strip()+';' for n,b in bodies.items() if n!='escape_table')
    native=replace_once(native,'static Char slots[7];',signatures+'\nstatic Char slots[7];')
    return native,has_lua

def main():
    attack.main(native_builder=item_native,extra_markers=('REAL_HEADER_FINISH_DISPATCH|','FINISH_RS_OBS|','REAL_HEADER_PLAYER_LEVEL|','REAL_HEADER_PET_GROWTH|','REAL_HEADER_REWARD_ITEM|'))
    print('BOUNDARY|prepared_unattached_item250;unique_code_preserved;empty_full_member_stale_slots;no_creation_drop_allocation_owned_rejection_network_historical_promotion')
    print('RESOLUTION|ORIGINAL_REAL_HEADER_REWARD_ITEM_BOUNDED_PASS')
if __name__=='__main__':main()
