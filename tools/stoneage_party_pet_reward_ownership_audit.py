"""Original terminal reward shared references, duplicates and serialization.

Unchanged pinned gameplay functions; full real-header item/actor/arena oracles.
Warning/log/transport collectors are explicit presentation adapters only.
"""
from __future__ import annotations
from tools import stoneage_party_pet_original_reward_item_audit as item
from tools import stoneage_party_pet_original_attack_audit as attack
replace_once=item.replace_once
NAME='R,|\\\n'
ESCAPED='R\\c\\z\\y\\n'

def escape_oracle(name):
    mapping={'\n':'\\n',',':'\\c','|':'\\z','\\':'\\y'}
    return ''.join(mapping.get(c,c) for c in name)

PREP=r'''
  for(int a=0;a<2;a++){
    for(int j=0;j<CHAR_MAXITEMHAVE;j++)slots[a].indexOfExistItems[j]=-1;
    for(int j=0;j<CHAR_MAXPOOLITEMHAVE;j++)slots[a].indexOfExistPoolItems[j]=-1;
  }
  memset(reward_items,0,sizeof reward_items);ITEM_ARRAY=reward_items;ITEM_SIZE=256;ITEM_COUNT=1+(mode==3);
  for(int id=250;id<=250+(mode==3);id++){
    reward_items[id].use=1;reward_items[id].ITEM_FIELD.data[ITEM_ID]=731+(id-250);
    reward_items[id].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]=-1;
    reward_items[id].ITEM_FIELD.workint[ITEM_WORKOBJINDEX]=19;
    reward_items[id].ITEM_FIELD.workint[ITEM_WORKTIMELIMIT]=0;
    strcpy(reward_items[id].ITEM_FIELD.string[ITEM_UNIQUECODE].string,"bounded");
    strcpy(reward_items[id].ITEM_FIELD.string[ITEM_NAME].string,id==251?"Second":"Reward");
  }
  if(mode==3)strcpy(reward_items[250].ITEM_FIELD.string[ITEM_NAME].string,"R,|\\\n");
  int reward_actor=0,reward_slot=CHAR_STARTITEMARRAY,reward_limit=ITEM_LIMIT;
  if(mode<=1){
    for(int j=CHAR_STARTITEMARRAY;j<reward_limit;j++){
      slots[0].indexOfExistItems[j]=j;reward_items[j].use=1;
      reward_items[j].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]=0;ITEM_COUNT++;
    }
    reward_items[250].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]=1;
    reward_items[250].ITEM_FIELD.workint[ITEM_WORKOBJINDEX]=-1;
    if(mode==0){slots[1].indexOfExistItems[CHAR_STARTITEMARRAY]=250;slots[1].indexOfExistItems[CHAR_STARTITEMARRAY+1]=250;}
    else slots[1].indexOfExistPoolItems[0]=250;
  }
  battle->Side[0].Entry[0].getitem[0]=250;
  if(mode>=2)battle->Side[0].Entry[0].getitem[1]=mode==2?250:251;
  ITEM_TYPE expected_items[256];memcpy(expected_items,reward_items,sizeof expected_items);
  int expected_item_count=ITEM_COUNT-(mode==1);
  if(mode==1){expected_items[250].use=0;expected_items[250].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]=-1;}
  if(mode>=2)for(int id=250;id<=250+(mode==3);id++){
    expected_items[id].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]=0;
    expected_items[id].ITEM_FIELD.workint[ITEM_WORKOBJINDEX]=-1;
  }
  reward_log_count=reward_data_count=reward_one_count=0;reward_phase=1;
  reward_expected_actor=0;reward_expected_slot=CHAR_STARTITEMARRAY;
  reward_case=mode;reward_warning_count=reward_duplicate_warning_count=0;
'''
EXPECTED=r'''
  if(mode>=2){
    expected_finish[0].indexOfExistItems[CHAR_STARTITEMARRAY]=250;
    expected_finish[0].indexOfExistItems[CHAR_STARTITEMARRAY+1]=mode==2?250:251;
  }
'''
OBSERVE=r'''
  demand(!memcmp(expected_items,reward_items,sizeof expected_items),"whole original shared item array oracle");
  demand(ITEM_COUNT==expected_item_count,"original shared reward live item count oracle");
  demand(reward_log_count==(mode>=2?2:0)&&reward_data_count==(mode>=2?1:0)&&reward_one_count==OWNERSHIP_SEND_COUNT,"typed multiple reward log and transport counts");
  demand(reward_warning_count==(mode==0?2:0)&&reward_duplicate_warning_count==(mode==0?1:0),"exact original carried reference diagnostics");
  demand(slots[1].indexOfExistPoolItems[0]==(mode==1?250:-1),"pool reference retained independently of item lifetime");
  printf("REAL_HEADER_REWARD_OWNERSHIP|mode=%d|battle=%d|shared_carried=%d|pool_ref=%d|duplicate_award=%d|distinct_escaped_awards=%d|item250_use=%d|item250_owner=%d|item250_object=%d|item251_use=%d|item251_owner=%d|carried_warnings=%d|duplicate_warnings=%d|item_logs=%d|item_data=%d|item_one=%d|whole_item_oracle=1|whole_actor_oracle=1|whole_arena_oracle=1|released=1\n",mode,battle_at,mode==0,mode==1,mode==2,mode==3,reward_items[250].use,reward_items[250].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX],reward_items[250].ITEM_FIELD.workint[ITEM_WORKOBJINDEX],reward_items[251].use,reward_items[251].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX],reward_warning_count,reward_duplicate_warning_count,reward_log_count,reward_data_count,reward_one_count);
  reward_phase=0;
'''

COLLECT=r'''
static int reward_case,reward_warning_count,reward_duplicate_warning_count;
BOOL CHAR_sendItemData(int actor,int *indices,int count){
 if(!reward_phase||reward_case<2||actor!=0||count!=2||indices[0]!=CHAR_STARTITEMARRAY||indices[1]!=CHAR_STARTITEMARRAY+1)abort();reward_data_count++;return TRUE;
}
BOOL CHAR_sendItemDataOne(int actor,int slot){
 if(!reward_phase||reward_case<2||actor!=0||slot!=CHAR_STARTITEMARRAY+reward_one_count||reward_one_count>=2)abort();reward_one_count++;return TRUE;
}
void LogItem(char *name,char *key,int index,char *cause,int floor,int x,int y,char *code,char *itemname,int id){
 int expected_id=250+(reward_case==3?reward_log_count:0);
 char *expected_name=reward_case==3?(reward_log_count==0?"R,|\\\n":"Second"):"Reward";
 if(!reward_phase||reward_case<2||reward_log_count>=2||index!=expected_id||strcmp(code,"bounded")||strcmp(itemname,expected_name)||id!=731+(expected_id-250)||!name||!key||floor!=slots[0].data[CHAR_FLOOR]||x!=slots[0].data[CHAR_X]||y!=slots[0].data[CHAR_Y]||strcmp(cause,"BattleGet(战斗後所得的道具)"))abort();reward_log_count++;
}
static int reward_diagnostic(FILE *stream,const char *format,...){
 if(!reward_phase||reward_case!=0||stream!=stderr)abort();
 va_list ap;va_start(ap,format);
 int index=va_arg(ap,int);if(index!=250)abort();
 if(!strcmp(format,"warning !! player have this item:%d call from [%s:%d](%s)(%s)\n")){
  char *file=va_arg(ap,char *);int line=va_arg(ap,int);char *name=va_arg(ap,char *);char *itemname=va_arg(ap,char *);
  if(!file||line<=0||!name||strcmp(itemname,"Reward"))abort();reward_warning_count++;
 }else if(!strcmp(format,"ITEM_INDEX(%d) duplicate!!\n"))reward_duplicate_warning_count++;
 else abort();
 va_end(ap);return 0;
}
'''

def ownership_observations(profile):
    text=item.pet.pet_observations(profile)
    prep=item.substitutions(profile,PREP)
    text=replace_once(text,'  Char expected_finish[7];',prep+'  Char expected_finish[7];')
    text=replace_once(text,'  BATTLE expected_final_arena=*battle;',EXPECTED+'  BATTLE expected_final_arena=*battle;')
    observed=item.substitutions(profile,OBSERVE).replace('OWNERSHIP_SEND_COUNT','(mode>=2?2:0)' if profile=='bismarck' else '0')
    text=replace_once(text,'  finish_transport_phase=0;',observed+'  finish_transport_phase=0;')
    payout='4c92' if profile=='bismarck' else '1'
    member='4c92' if profile=='bismarck' else '0'
    old=f'demand(!strcmp(finish_rs_text[0],(up?"-2|1|{payout},0|1|{payout},,,,|||":"-2|0|{payout},0|0|{payout},,,,|||"))&&!strcmp(finish_rs_text[1],"-2|0|{member},,,,,|||"),"original reward text independent base62 oracle");'
    prefix=f'(up?"-2|1|{payout},0|1|{payout},,,,":"-2|0|{payout},0|0|{payout},,,,")'
    # Literal independent fixture expected text, not an invocation of original
    # makeEscapeString to build the expected result.
    packet=f'char expected_owner_rs[160];const char *expected_items_rs=mode<2?"|||":(mode==2?"Reward|Reward||":"R\\\\c\\\\z\\\\y\\\\n|Second||");snprintf(expected_owner_rs,sizeof expected_owner_rs,"%s%s",{prefix},expected_items_rs);demand(!strcmp(finish_rs_text[0],expected_owner_rs)&&!strcmp(finish_rs_text[1],"-2|0|{member},,,,,|||"),"exact shared duplicate escaped reward packets");'
    return replace_once(text,old,packet)

def ownership_native(profile,source,battle,event,root):
    native,has_lua=item.item_native(profile,source,battle,event,root)
    field='char_index' if profile=='bismarck' else 'charaindex'
    native=replace_once(native,item.item_observations(profile).replace('ENTRY_FIELD',field),ownership_observations(profile).replace('ENTRY_FIELD',field))
    for n in ('CHAR_sendItemData','CHAR_sendItemDataOne','LogItem'):
        native=replace_once(native,attack.definition(native,n),'')
    # The adapter sees only original release diagnostics; no gameplay return,
    # item fields or scan loop is substituted or modified.
    body=attack.definition(native,'_ITEM_endExistItemsOne')
    macro='#define fprintf(...) (++diagnostics,0)'
    if native.count(macro)!=1:raise ValueError('inherited diagnostic macro drift')
    native=replace_once(native,body,'#undef fprintf\n#define fprintf reward_diagnostic\n'+body+'\n#undef fprintf\n'+macro)
    if attack.definition(native,'_ITEM_endExistItemsOne')!=body:raise ValueError('original release body mutated by adapter')
    collectors=COLLECT.replace('char *','const char *') if profile=='bismarck' else COLLECT
    decl='static int reward_phase,reward_expected_actor,reward_expected_slot,reward_log_count,reward_data_count,reward_one_count;'
    native=replace_once(native,decl,decl+'\n'+collectors)
    # Exact signatures are in the original headers; the warning adapter appears
    # before the extracted release body and uses standard va_list.
    native='#include <stdarg.h>\n'+native
    return native,has_lua

def main():
    attack.main(native_builder=ownership_native,extra_markers=('REAL_HEADER_FINISH_DISPATCH|','FINISH_RS_OBS|','REAL_HEADER_PLAYER_LEVEL|','REAL_HEADER_PET_GROWTH|','REAL_HEADER_REWARD_OWNERSHIP|'))
    print('BOUNDARY|prepared_shared_carried_and_pool_refs;duplicate_original_awards;literal_escaped_name;no_new_drop_allocator_or_historical_equivalence')
    print('RESOLUTION|ORIGINAL_REAL_HEADER_REWARD_OWNERSHIP_BOUNDED_PASS')
if __name__=='__main__':main()
