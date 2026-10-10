"""Bounded original pending-reward -> BATTLE_GetExpGold -> real inventory bridge.

The item is actually ENEMY_createEnemy -> ITEM_makeItemAndRegist ID1 -> enemy6 ->
BATTLE_AddExpItem player0 ticket -> BATTLE_GetExpGold. Native source bodies,
headers and item/actor arrays are unchanged. THIS GATE does not yet execute a
second BATTLE_Loop/FInish on this particular item and cannot be cited as such.
"""
from __future__ import annotations
import hashlib,json
from tools import stoneage_battle_original_drop_ticket_audit as ticket
from tools import stoneage_party_pet_original_attack_audit as attack

replace_once=ticket.replace_once

PAYOUT=r"""
 /* Original registered enemy item3 currently appears in actual player0
    original AddExpItem getitem[0], with source enemy owner6. */
 ITEM_TYPE payout_base_pool[256];memcpy(payout_base_pool,reward_items,sizeof payout_base_pool);
 Char payout_base_actors[7];memcpy(payout_base_actors,slots,sizeof payout_base_actors);
 BATTLE payout_base_arena=*arena;
 int payout_base_count=ITEM_COUNT,payout_base_size=ITEM_SIZE;
 int payout_old_log=reward_log_count,payout_old_data=reward_data_count,payout_old_one=reward_one_count;
 int payout_old_phase=reward_phase,payout_old_recipient=reward_expected_actor,payout_old_slot=reward_expected_slot;
 int payout_old_transport=finish_transport_phase;
 for(int payout_scenario=0;payout_scenario<2;payout_scenario++){
   memcpy(reward_items,payout_base_pool,sizeof payout_base_pool);
   memcpy(slots,payout_base_actors,sizeof payout_base_actors);
   *arena=payout_base_arena;ITEM_COUNT=payout_base_count;ITEM_SIZE=payout_scenario?256:payout_base_size;
   /* Zero EXP to isolate inventory transfer, not redefine historical XP. */
   slots[0].workint[CHAR_WORKGETEXP]=0;slots[2].workint[CHAR_WORKGETEXP]=0;
   CHAR_setFlg(0,CHAR_ISDIE,FALSE);
   int empty=CHAR_findEmptyItemBox(0);
   demand(empty>=CHAR_STARTITEMARRAY && empty<CHAR_MAXITEMHAVE,
          "original player has first genuine empty persistent item box");
   if(payout_scenario){
     int next_id=20;
     for(int box=CHAR_STARTITEMARRAY;box<CHAR_MAXITEMHAVE;box++)if(slots[0].indexOfExistItems[box]<0){
        demand(next_id<256 && !reward_items[next_id].use,"valid unoccupied synthetic filler item pool slot");
        slots[0].indexOfExistItems[box]=next_id;
        reward_items[next_id].use=1;
        reward_items[next_id].ITEM_FIELD.data[ITEM_ID]=1800+next_id;
        reward_items[next_id].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]=0;
        reward_items[next_id].ITEM_FIELD.workint[ITEM_WORKOBJINDEX]=-1;
        ITEM_COUNT++;next_id++;
     }
     demand(CHAR_findEmptyItemBox(0)==-1,"original player persistent bag verified full");
   }
   ITEM_TYPE expected_items[256];memcpy(expected_items,reward_items,sizeof expected_items);
   Char expected_actors[7];memcpy(expected_actors,slots,sizeof expected_actors);
   BATTLE expected_arena=*arena;
   expected_arena.Side[0].Entry[0].getitem[0]=-1;
   if(!payout_scenario){
     expected_items[3].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]=0;
     expected_items[3].ITEM_FIELD.workint[ITEM_WORKOBJINDEX]=-1;
     expected_actors[0].indexOfExistItems[empty]=3;
   }else{
     expected_items[3].use=0;
     expected_items[3].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]=-1;
   }
   int expected_live=ITEM_COUNT-payout_scenario;
   reward_phase=2;reward_expected_actor=0;reward_expected_slot=empty;
   reward_log_count=reward_data_count=reward_one_count=0;
   settle_log_count=0;finish_rs_count=finish_status_count=0;finish_transport_phase=1;
   int payout_ret=BATTLE_GetExpGold(battle_at,0,0);
   demand(payout_ret==0,"actual original BATTLE_GetExpGold executed");
   demand(!memcmp(expected_items,reward_items,sizeof expected_items),
          "complete 256 native item records as original source payout or full-bag release");
   demand(ITEM_COUNT==expected_live,"exact native live item count after original source payout");
   demand(!memcmp(&expected_arena,arena,sizeof expected_arena),
          "whole native BATTLE arena and all three tickets exact after GetExpGold");
   if(memcmp(expected_actors,slots,sizeof expected_actors)){
      for(int actor=0;actor<7;actor++)for(int j=0;j<CHAR_WORKDATAINTNUM;j++)
       if(expected_actors[actor].workint[j]!=slots[actor].workint[j])
        printf("PAYOUT_ACTOR_WORK_DIFF|mode=%d|actor=%d|field=%d|old=%d|new=%d\n",
           payout_scenario,actor,j,expected_actors[actor].workint[j],slots[actor].workint[j]);
      for(int actor=0;actor<7;actor++)for(int j=0;j<CHAR_DATAINTNUM;j++)
       if(expected_actors[actor].data[j]!=slots[actor].data[j])
        printf("PAYOUT_ACTOR_DATA_DIFF|mode=%d|actor=%d|field=%d|old=%d|new=%d\n",
           payout_scenario,actor,j,expected_actors[actor].data[j],slots[actor].data[j]);
      fflush(stdout);
   }
   demand(!memcmp(expected_actors,slots,sizeof expected_actors),
          "all seven entire native Char records after reward settle");
   demand(reward_log_count==!payout_scenario&&
          reward_data_count==!payout_scenario&&
          reward_one_count==(!payout_scenario && ONE_EXPECTED)&&
          settle_log_count==!payout_scenario,
          "native reward item log and exact source profile item data presentation");
   demand(finish_rs_count==1&&finish_status_count<=1,
          "exact one original RS reward packet on standalone GetExpGold");
   printf("REAL_HEADER_DROP_PAYOUT|case=%d|recipient=0|item=3|empty_slot=%d|bag_full=%d|player_has=%d|item_live=%d|owner=%d|count=%d|logs=%d|data=%d|one=%d|rs=%d|whole_pool=1|whole_actors=1|whole_arena=1\n",
          payout_scenario,empty,payout_scenario,
          !payout_scenario,reward_items[3].use,reward_items[3].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX],
          ITEM_COUNT,reward_log_count,reward_data_count,reward_one_count,finish_rs_count);
   reward_phase=0;finish_transport_phase=0;
 }
 memcpy(reward_items,payout_base_pool,sizeof payout_base_pool);
 memcpy(slots,payout_base_actors,sizeof payout_base_actors);
 *arena=payout_base_arena;ITEM_COUNT=payout_base_count;ITEM_SIZE=payout_base_size;
 reward_phase=payout_old_phase;reward_log_count=payout_old_log;reward_data_count=payout_old_data;
 reward_one_count=payout_old_one;reward_expected_actor=payout_old_recipient;reward_expected_slot=payout_old_slot;
 finish_transport_phase=payout_old_transport;finish_rs_count=finish_status_count=0;
"""

def observations(profile):
    return ticket.drop.factory.allocator.item.substitutions(profile,PAYOUT).replace(
        "ONE_EXPECTED","1" if profile=="bismarck" else "0")

def payout_native(profile,source,battle,event,root):
    native,has_lua=ticket.ticket_native(profile,source,battle,event,root)
    old_log=attack.definition(native,"LogItem")
    if old_log.count('if(!reward_phase||item!=250')!=1:
        raise ValueError("inherited LogItem collector shape drift")
    injected="""if(reward_phase==2){
      if(item!=3||strcmp(code,"factory-bounded")||strcmp(itemname,"Factory")||id!=1||
         !name||!key||strcmp(cause,"BattleGet(战斗後所得的道具)")||
         floor!=slots[0].data[CHAR_FLOOR]||x!=slots[0].data[CHAR_X]||y!=slots[0].data[CHAR_Y])abort();
      settle_log_count++;reward_log_count++;return;
     }
     """
    newer=old_log.replace('if(!reward_phase||item!=250',injected+'if(!reward_phase||item!=250',1)
    native=replace_once(native,old_log,newer)
    native=replace_once(native,'static int reward_phase,reward_expected_actor',
         'static int settle_log_count;\nstatic int reward_phase,reward_expected_actor')
    old=ticket.ticket_controls(profile)
    restore=' memcpy(reward_items,ticket_saved_items,sizeof ticket_saved_items);'
    if old.count(restore)!=1:raise ValueError("original ticket restoration anchor drift")
    updated=old.replace(restore,observations(profile)+"\n"+restore,1)
    native=replace_once(native,old,updated)
    return native,has_lua

def main():
    attack.main(native_builder=payout_native,extra_markers=(
       "REAL_HEADER_FINISH_DISPATCH|","REAL_HEADER_ITEM_FACTORY|",
       "REAL_HEADER_ENEMY_POSITIVE_DROP|","REAL_HEADER_DROP_TICKET|",
       "REAL_HEADER_DROP_PAYOUT|"))
    print("BOUNDARY|actual enemy-created item through original GetExpGold separately invoked after an accepted earlier original Finish; this registered item has NOT traversed same-instance second BATTLE_Loop/Finish; synthetic item master and partial/full bag only")
    print("RESOLUTION|ORIGINAL_REAL_HEADER_DROP_PAYOUT_DIRECT_BOUNDED_PASS")

if __name__=="__main__":main()
