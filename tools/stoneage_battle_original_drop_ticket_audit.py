"""Run unchanged original BATTLE_AddExpItem on actual registered enemy drop.

This extends the accepted exact-header ENEMY_createEnemy + ITEM_makeItemAndRegist
probe, rather than inventing a parallel reward model. Synthetic drop master and
attack list remain explicitly bounded.
"""
from __future__ import annotations
import hashlib,json,re
from pathlib import Path
from tools import stoneage_enemy_original_drop_audit as drop
from tools import stoneage_party_pet_original_attack_audit as attack

replace_once=drop.replace_once
SOURCE=Path(__file__).resolve().parents[1]/"research/recovered/STONEAGE-BATTLE-ORIGINAL-DROP-TICKET-SOURCE-R1.json"

TICKET=r"""
 /* Independent original AddExpItem after actual ENEMY_createEnemy item index3. */
 ITEM_TYPE ticket_saved_items[256];memcpy(ticket_saved_items,reward_items,sizeof ticket_saved_items);
 Char ticket_saved_actors[7];memcpy(ticket_saved_actors,slots,sizeof ticket_saved_actors);
 BATTLE ticket_saved_arena=*arena;
 int ticket_saved_use=ITEM_COUNT, ticket_saved_rng=rng_count,ticket_saved_mode=rng_mode;
 int ticket_list[2]={0,-1};
 arena->use=1;arena->Side[0].type=BATTLE_S_TYPE_PLAYER;
 arena->Side[1].type=BATTLE_S_TYPE_ENEMY;
 for(int j=0;j<BATTLE_ENTRY_MAX;j++)arena->Side[1].Entry[j].ENTRY_FIELD=-1;
 arena->Side[1].Entry[0].ENTRY_FIELD=positive_actor;
 arena->Side[0].Entry[0].ENTRY_FIELD=0;
 for(int j=0;j<GETITEM_MAX;j++)arena->Side[0].Entry[0].getitem[j]=-1;
 slots[positive_actor].data[CHAR_HP]=0;
 CHAR_setFlg(positive_actor,CHAR_ISDIE,FALSE);
 demand(BATTLE_CHECKINDEX(battle_at),"source arena passes original index guard");
 demand(BATTLE_No2Index(battle_at,0)==0,
        "original battle attacker ticket maps valid active player");
 BATTLE ticket_expected=*arena;
 ticket_expected.Side[0].Entry[0].getitem[0]=3;
 Char ticket_before[7];memcpy(ticket_before,slots,sizeof ticket_before);
 int owner_before=reward_items[3].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX];
 rng_mode=0;rng_count=0;
 int ticket_result=BATTLE_AddExpItem(battle_at,ticket_list);
 demand(ticket_result==0,"original AddExpItem player ticket success");
 demand(rng_count==1,"exact one original RAND for one eligible attacker");
 demand(!memcmp(&ticket_expected,arena,sizeof ticket_expected),
        "complete original battle arena only mutates player pending reward slot");
 demand(!memcmp(ticket_saved_items,reward_items,sizeof ticket_saved_items)&&ITEM_COUNT==ticket_saved_use,
        "entire 256-item pool and count preserved by pending ticket");
 demand(slots[positive_actor].indexOfExistItems[CHAR_STARTITEMARRAY]==-1,
        "enemy original carried slot cleared at reward assignment");
 demand(CHAR_getFlg(positive_actor,CHAR_ISDIE)==TRUE,
        "enemy original death flag set during reward assignment");
 demand(slots[positive_actor].data[CHAR_DEADCOUNT]==ticket_before[positive_actor].data[CHAR_DEADCOUNT]+1,
        "enemy native death count increments once");
 demand(reward_items[3].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]==owner_before,
        "pre-Finish pending reward retains original carried owner until payout");
 demand(slots[0].data[CHAR_KILLPETCOUNT]==ticket_before[0].data[CHAR_KILLPETCOUNT]+1,
        "only direct player attack recipient obtains original kill count");
 for(int i=1;i<7;i++)if(i!=positive_actor)
  demand(!memcmp(&ticket_before[i],&slots[i],sizeof(Char)),
         "all five nonrecipient original actors unchanged at ticket assignment");
 printf("REAL_HEADER_DROP_TICKET|mode=%d|actor=%d|item=3|recipient=0|ticket=0|draws=%d|pending=3|enemy_carried_cleared=1|original_item_owner=%d|arena_oracle=1|item_pool_oracle=1|other_actor_oracle=1\n",
        mode,positive_actor,rng_count,owner_before);
 memcpy(reward_items,ticket_saved_items,sizeof ticket_saved_items);
 memcpy(slots,ticket_saved_actors,sizeof ticket_saved_actors);
 *arena=ticket_saved_arena;ITEM_COUNT=ticket_saved_use;
 rng_count=ticket_saved_rng;rng_mode=ticket_saved_mode;
"""

def ticket_controls(profile):
    return drop.factory.allocator.item.substitutions(profile,TICKET).replace(
        "ENTRY_FIELD","char_index" if profile=="bismarck" else "charaindex")

def ticket_native(profile,source,battle,event,root):
    native,has_lua=drop.positive_drop_native(profile,source,battle,event,root)
    for name in ("BATTLE_AddExpItem","BATTLE_ItemDelCheck"):
        extracted=attack.definition(battle,name)
        try:
            already=attack.definition(native,name)
        except ValueError:
            if name!="BATTLE_ItemDelCheck":raise
            # This true original helper was not needed by the previous
            # no-overflow source witness. Supply its unchanged C body now.
            native=replace_once(native,"int main(int argc,char **argv){",
                  extracted+"\nint main(int argc,char **argv){")
            already=attack.definition(native,name)
        symbols=("BATTLE_AddExpItem","getitem","ENEMY","ITEM") if name=="BATTLE_AddExpItem" else ("ITEM","CHAR")
        if not all(z in already for z in symbols[1:]):
            raise ValueError("missing original reward function body "+name)
        print("DROP_TICKET_SOURCE|"+profile+"|"+name+
              "|preprocessed_sha256="+hashlib.sha256(extracted.encode()).hexdigest()+
              "|inherited_native_sha256="+hashlib.sha256(already.encode()).hexdigest(),flush=True)
        pins=json.loads(SOURCE.read_text())["inherited_native_sha256"].get(profile,{})
        if name in pins and hashlib.sha256(already.encode()).hexdigest()!=pins[name]:
            raise ValueError("original inherited reward function body drift "+name)
    # Original getFdnum reads configuration fdnum, absent from the isolated
    # simulator. Here the accepted synthetic character partition is exactly 2
    # users; admit a one-function config boundary without game-rule rewrites.
    native=replace_once(native,"int main(int argc,char **argv){",
          "unsigned int getFdnum(void){if(CHAR_playernum!=2)abort();return 2;}\\n"
          "int main(int argc,char **argv){")
    anchor=' demand(!memcmp(&specimen,&table_snapshot,sizeof specimen),\n        "original enemy drop does not mutate factory master template");'
    native=replace_once(native,anchor,anchor+"\n"+ticket_controls(profile))
    return native,has_lua

def main():
    attack.main(native_builder=ticket_native,extra_markers=(
        "REAL_HEADER_FINISH_DISPATCH|","FINISH_RS_OBS|",
        "REAL_HEADER_REWARD_ITEM|","REAL_HEADER_ITEM_ALLOCATOR|",
        "REAL_HEADER_ITEM_FACTORY|","REAL_HEADER_ENEMY_POSITIVE_DROP|",
        "REAL_HEADER_DROP_TICKET|"))
    print("BOUNDARY|natural-master-data-open synthetic guaranteed item ID1; actual original AddExpItem player attack-list ticket and enemy carried item; original second Finish unconnected to this same item")
    print("RESOLUTION|ORIGINAL_REAL_HEADER_DROP_TICKET_BOUNDED_PASS")

if __name__=="__main__":main()
