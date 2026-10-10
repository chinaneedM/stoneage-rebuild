"""Experimental same-registered-item second original Loop -> Finish -> GetProfit.

Strict candidate gate. Never merge or claim an accepted second-Finish witness until
both source profiles pass native O0/O2 UBSan and complete differential oracles.
"""
from __future__ import annotations
from tools import stoneage_battle_original_drop_payout_audit as payout
from tools import stoneage_party_pet_original_attack_audit as attack
replace_once=payout.replace_once

SECOND=r"""
  /* Only after the accepted independent real BATTLE_GetExpGold oracle has
     restored this item's exact earlier pending-battle state. */
  ITEM_TYPE loop_saved_items[256];memcpy(loop_saved_items,reward_items,sizeof loop_saved_items);
  Char loop_saved_actors[7];memcpy(loop_saved_actors,slots,sizeof loop_saved_actors);
  BATTLE loop_saved_arena=*arena;
  int loop_saved_count=ITEM_COUNT,loop_saved_size=ITEM_SIZE;
  int loop_saved_total=Total_BattleNum;
  int loop_saved_rng_mode=rng_mode,loop_saved_rng_count=rng_count;
  int loop_saved_phase=reward_phase,loop_saved_transport=finish_transport_phase;
  int loop_saved_log=reward_log_count,loop_saved_data=reward_data_count;
  int loop_saved_one=reward_one_count,loop_saved_actor=reward_expected_actor,loop_saved_slot=reward_expected_slot;
  Char baseline_actors[7];BATTLE baseline_arena;ITEM_TYPE baseline_items[256];
  int baseline_count=-1,baseline_total=-1;
  int first_empty=-1;
  for(int with_item=0;with_item<2;with_item++){
   memcpy(reward_items,loop_saved_items,sizeof loop_saved_items);
   memcpy(slots,loop_saved_actors,sizeof loop_saved_actors);
   *arena=loop_saved_arena;ITEM_COUNT=loop_saved_count;ITEM_SIZE=loop_saved_size;
   arena->use=1;arena->mode=BATTLE_MODE_FINISH;
   arena->type=BATTLE_TYPE_P_vs_E;arena->winside=WIN_SIDE;
   arena->Side[0].type=BATTLE_S_TYPE_PLAYER;
   arena->Side[1].type=BATTLE_S_TYPE_ENEMY;
   for(int e=0;e<BATTLE_ENTRY_MAX;e++){
     arena->Side[0].Entry[e].ENTRY_FIELD=-1;
     arena->Side[1].Entry[e].ENTRY_FIELD=-1;
   }
   arena->Side[0].Entry[0].ENTRY_FIELD=0;
   arena->Side[1].Entry[0].ENTRY_FIELD=positive_actor;
   for(int e=0;e<GETITEM_MAX;e++)arena->Side[0].Entry[0].getitem[e]=-1;
   if(with_item)arena->Side[0].Entry[0].getitem[0]=3;
   slots[0].workint[CHAR_WORKBATTLEINDEX]=battle_at;
   slots[0].workint[CHAR_WORKBATTLEMODE]=BATTLE_CHARMODE_C_WAIT;
   slots[positive_actor].workint[CHAR_WORKBATTLEINDEX]=battle_at;
   slots[positive_actor].workint[CHAR_WORKBATTLEMODE]=BATTLE_CHARMODE_C_WAIT;
   slots[0].workint[CHAR_WORKGETEXP]=0;
   slots[2].workint[CHAR_WORKGETEXP]=0;
   CHAR_setFlg(0,CHAR_ISDIE,FALSE);
   Total_BattleNum=1;
   first_empty=CHAR_findEmptyItemBox(0);
   demand(first_empty>=CHAR_STARTITEMARRAY&&first_empty<CHAR_MAXITEMHAVE,
          "same-item second Finish first genuine bag slot");
   reward_phase=2;reward_expected_actor=0;reward_expected_slot=first_empty;
   reward_log_count=reward_data_count=reward_one_count=settle_log_count=0;
   finish_rs_count=finish_status_count=0;finish_transport_phase=1;
   int loop_ret=BATTLE_Loop();
   demand(loop_ret==1,"same item exact original second BATTLE_Loop completed");
   demand(arena->use==0&&arena->mode==BATTLE_MODE_NONE&&Total_BattleNum==0,
          "actual original second BATTLE_Finish and BATTLE_DeleteBattle complete");
   if(!with_item){
      memcpy(baseline_actors,slots,sizeof baseline_actors);
      memcpy(&baseline_arena,arena,sizeof baseline_arena);
      memcpy(baseline_items,reward_items,sizeof baseline_items);
      baseline_count=ITEM_COUNT;baseline_total=Total_BattleNum;
      demand(reward_items[3].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]==positive_actor,
             "no-item second Finish preserves unclaimed synthetic item3 original owner");
   }else{
      baseline_actors[0].indexOfExistItems[first_empty]=3;
      baseline_items[3].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]=0;
      baseline_items[3].ITEM_FIELD.workint[ITEM_WORKOBJINDEX]=-1;
      demand(!memcmp(baseline_items,reward_items,sizeof baseline_items)&&ITEM_COUNT==baseline_count,
             "entire same-item original second Finish item pool owner oracle");
      demand(!memcmp(baseline_actors,slots,sizeof baseline_actors),
             "all seven same-item original second Finish actors differential oracle");
      demand(!memcmp(&baseline_arena,arena,sizeof baseline_arena)&&Total_BattleNum==baseline_total,
             "entire source battle arena and release differential oracle");
      demand(reward_log_count==1&&settle_log_count==1,
             "same-item original second Finish issues original pickup log");
      printf("REAL_HEADER_SAME_ITEM_FINISH|actor=%d|registered_item=3|recipient=0|bag_slot=%d|owner=0|item_live=1|second_loop=1|original_finish=1|profit=1|exp_gold=1|whole_items=1|whole_actors=1|whole_arena=1\n",
             positive_actor,first_empty);
   }
   reward_phase=0;finish_transport_phase=0;
  }
  memcpy(reward_items,loop_saved_items,sizeof loop_saved_items);
  memcpy(slots,loop_saved_actors,sizeof loop_saved_actors);
  *arena=loop_saved_arena;ITEM_COUNT=loop_saved_count;ITEM_SIZE=loop_saved_size;Total_BattleNum=loop_saved_total;
  rng_mode=loop_saved_rng_mode;rng_count=loop_saved_rng_count;
  reward_phase=loop_saved_phase;finish_transport_phase=loop_saved_transport;
  reward_log_count=loop_saved_log;reward_data_count=loop_saved_data;reward_one_count=loop_saved_one;
  reward_expected_actor=loop_saved_actor;reward_expected_slot=loop_saved_slot;
"""

def second_controls(profile):
    return payout.ticket.drop.factory.allocator.item.substitutions(profile,SECOND).replace(
        "ENTRY_FIELD","char_index" if profile=="bismarck" else "charaindex").replace(
        "WIN_SIDE","-1" if profile=="bismarck" else "0")

def same_item_native(profile,source,battle,event,root):
    native,has_lua=payout.payout_native(profile,source,battle,event,root)
    previous=payout.observations(profile)
    # Add AFTER full direct-payout exact oracle has restored pending arena state.
    native=replace_once(native,previous,previous+"\n"+second_controls(profile))
    return native,has_lua

def main():
    attack.main(native_builder=same_item_native,extra_markers=(
        "REAL_HEADER_FINISH_DISPATCH|","REAL_HEADER_DROP_TICKET|",
        "REAL_HEADER_DROP_PAYOUT|","REAL_HEADER_SAME_ITEM_FINISH|"))
    print("BOUNDARY|synthetic drop master, source late descendants, no new engine and no early server history promotion")
    print("RESOLUTION|ORIGINAL_REAL_HEADER_SAME_ITEM_FINISH_BOUNDED_PASS")

if __name__=="__main__":main()
