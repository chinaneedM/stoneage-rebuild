"""Original released-slot reuse following unchanged battle drop assignment.

Source-free wrapper. This does not alter any original function bodies, touch a
production pool or claim historical natural reachability. Three controlled
cases cross no alias, an owned PET2 alias and a PLAYER0 alias of old item8.
"""
from __future__ import annotations

import hashlib
import resource
from tools import stoneage_battle_original_guard_index_range_audit as prior

attack = prior.attack
item = prior.item
replace_once = prior.replace_once

CONTROL = r'''
 {
 static ITEM_TYPE reuse_saved_items[256],reuse_before_factory[256];
 static Char reuse_saved_actors[7],reuse_before_factory_actors[7];
 BATTLE reuse_saved_arena=*arena,reuse_before_factory_arena;
 CONNECTION_TYPE reuse_saved_connections[8],reuse_before_factory_connections[8];
 TABLE_TYPE reuse_saved_tables[3];memcpy(reuse_saved_tables,allocator_table,sizeof reuse_saved_tables);
 INDIRECT_SNAPSHOT
 memcpy(reuse_saved_items,reward_items,sizeof reuse_saved_items);
 memcpy(reuse_saved_actors,slots,sizeof reuse_saved_actors);
 memcpy(reuse_saved_connections,cleanup_connections,sizeof reuse_saved_connections);
 int reuse_saved_count=ITEM_COUNT,reuse_saved_size=ITEM_SIZE;
 int reuse_saved_rng=rng_count,reuse_saved_mode=rng_mode;
 int reuse_saved_lookup=lookup_count,reuse_saved_total=Total_BattleNum;
 int reuse_saved_warnings=shared_guard_warnings,reuse_saved_diagnostics=diagnostics;
 int reuse_saved_release_phase=split_release_phase,reuse_saved_release_calls=split_release_calls,reuse_saved_release_empty=split_release_empty;
 int reuse_saved_release_hits[4];memcpy(reuse_saved_release_hits,split_release_hits,sizeof reuse_saved_release_hits);
 int reuse_list[3]={0,1,-1};
 for(int alias_case=0;alias_case<3;alias_case++){
  /* All four drops and enemy6 come from the accepted original creation. */
  memcpy(reward_items,chain_created_items,sizeof reuse_saved_items);
  memcpy(slots,chain_created_actors,sizeof reuse_saved_actors);
  *arena=chain_input_arena;arena->Side[0].Entry[1].ENTRY_FIELD=1;
  ITEM_COUNT=chain_after_create;ITEM_SIZE=256;range_fdnum=2;
  demand(CHAR_playernum==2&&CHAR_getInt(2,CHAR_WHICHTYPE)==CHAR_TYPEPET&&slots[0].unionTable.indexOfPet[0]==2,"unaltered two-PLAYER/owned PET2 fixture");
  for(int a=0;a<3;a++)slots[a].indexOfExistItems[CHAR_STARTITEMARRAY+1]=-1;
  int alias_index=alias_case==1?2:(alias_case==2?0:-1);
  if(alias_index>=0)slots[alias_index].indexOfExistItems[CHAR_STARTITEMARRAY+1]=8;
  CHAR_setFlg(chain_actor,CHAR_ISDIE,FALSE);slots[chain_actor].data[CHAR_HP]=0;
  concentrated_rng_phase=1;concentrated_rng_recipient=0;concentrated_rng_branch=1;
  concentrated_rng_at=0;rng_count=0;
  split_release_phase=1;split_release_calls=split_release_empty=0;
  memset(split_release_hits,0,sizeof split_release_hits);shared_guard_warnings=0;
  int before_assignment=ITEM_COUNT;
  demand(BATTLE_AddExpItem(battle_at,reuse_list)==0,"unchanged original concentrated four-drop assignment with two actual PLAYER recipients");
  split_release_phase=0;concentrated_rng_phase=0;
  int protected=alias_case==2;
  demand(rng_count==6&&concentrated_rng_at==6,"four original recipient draws and two replacement draws");
  demand(split_release_calls==!protected&&!split_release_empty&&split_release_hits[0]==!protected,"original victim8 release only when PLAYER0 not carrying alias");
  for(int k=1;k<4;k++)demand(!split_release_hits[k],"no other original-created item released on replacement");
  demand(shared_guard_warnings==protected&&ITEM_COUNT==before_assignment-!protected,"original guard and live count partition");
  demand(reward_items[8].use==protected&&reward_items[8].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]==(protected?6:-1),"original released/retained old item8 state");
  demand(arena->Side[0].Entry[0].getitem[0]==11&&arena->Side[0].Entry[0].getitem[1]==9&&arena->Side[0].Entry[0].getitem[2]==10,"original replacement pending order 11,9,10");
  for(int k=0;k<10;k++)demand(slots[6].indexOfExistItems[CHAR_STARTITEMARRAY+k]==-1,"original ten enemy carried slots cleared");
  demand(slots[2].indexOfExistItems[CHAR_STARTITEMARRAY+1]==(alias_case==1?8:-1),"PET2 stale reference only in synthetic PET case");
  demand(slots[0].indexOfExistItems[CHAR_STARTITEMARRAY+1]==(protected?8:-1),"PLAYER0 alias only in synthetic protected case");
  /* Do not rewind the original function-static allocator cursor. Only force
     other inactive slots occupied to make old index8 the sole free candidate.
     Count and item bytes of these blockers are explicit synthetic inputs. */
  int synthetic_blockers=0;
  for(int i=0;i<256;i++)if(i!=8&&!reward_items[i].use){
   reward_items[i].use=1;ITEM_COUNT++;synthetic_blockers++;
  }
  memcpy(reuse_before_factory,reward_items,sizeof reuse_before_factory);
  memcpy(reuse_before_factory_actors,slots,sizeof reuse_before_factory_actors);
  reuse_before_factory_arena=*arena;
  memcpy(reuse_before_factory_connections,cleanup_connections,sizeof reuse_before_factory_connections);
  int before_factory=ITEM_COUNT,lookup_before=lookup_count,warnings_before=shared_guard_warnings,diagnostics_before=diagnostics;
  int before_total=Total_BattleNum,release_before=split_release_calls;
  demand(reuse_before_factory[8].ITEM_FIELD.data[ITEM_ID]==1,"released original victim carries historical template ID1 bytes before attempted reuse");
  rng_mode=0;rng_count=0;
  int created=ITEM_makeItemAndRegist(2);
  int success=!protected;
  demand(created==(success?8:-1),"original factory allocator reuses only free victim8, or fails when guard retained it");
  demand(rng_count==66,"unchanged original factory draws exactly 66 times");
  demand(ITEM_COUNT==before_factory+success,"original allocator increments item live count only on successful reuse");
  demand(reward_items[8].use==1&&reward_items[8].ITEM_FIELD.data[ITEM_ID]==(success?2:1),"new ID2 overwrites original ID1 only on permitted reused index");
  demand(reward_items[8].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]==(success?-1:6),"factory owner differs from original enemy owner, or guard preserves enemy owner");
  int others_unchanged=1;
  for(int i=0;i<256;i++)if(i!=8&&memcmp(&reward_items[i],&reuse_before_factory[i],sizeof reward_items[i]))others_unchanged=0;
  demand(others_unchanged,"all 255 noncandidate object records unchanged by factory");
  if(!success)demand(!memcmp(reuse_before_factory,reward_items,sizeof reuse_before_factory),"protected full pool failed without any item mutation");
  else demand(memcmp(&reuse_before_factory[8],&reward_items[8],sizeof reward_items[8])!=0,"original factory changes old item bytes at reused index");
  demand(!memcmp(reuse_before_factory_actors,slots,sizeof reuse_before_factory_actors)&&!memcmp(&reuse_before_factory_arena,arena,sizeof reuse_before_factory_arena),"factory never fixes dangling PET2/PLAYER0 carried indices or mutates arena");
  demand(!memcmp(reuse_before_factory_connections,cleanup_connections,sizeof reuse_before_factory_connections)&&lookup_count>=lookup_before&&Total_BattleNum==before_total,"native connection/total battle state preserved");
  demand(!memcmp(reuse_saved_tables,allocator_table,sizeof reuse_saved_tables),"entire original item ID table preserved");
  INDIRECT_ORACLE
  demand(shared_guard_warnings==warnings_before&&diagnostics==diagnostics_before+protected&&split_release_calls==release_before,"factory yields exact full-pool diagnostic only on protected retained object, with no new guard warning or release");
  printf("REAL_HEADER_RELEASED_SLOT_REUSE|alias=%d|victim=8|old_id=1|created=%d|new_id=%d|old_owner=%d|new_owner=%d|released=%d|guard_warnings=%d|factory_diagnostics=%d|release_calls=%d|assignment_draws=6|factory_draws=%d|blockers=%d|count_delta=%d|pet_ref=%d|player_ref=%d|others_unchanged=1|whole_actors=1|whole_arena=1|whole_connections=1|tables_immutable=1|no_cursor_rewind=1|original_creation=1|original_assignment=1|original_factory=1|synthetic_alias=1|synthetic_blockers=1\n",alias_index,created,reward_items[8].ITEM_FIELD.data[ITEM_ID],protected?6:-1,reward_items[8].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX],!protected,protected,diagnostics-diagnostics_before,!protected,rng_count,synthetic_blockers,ITEM_COUNT-before_factory,slots[2].indexOfExistItems[CHAR_STARTITEMARRAY+1],slots[0].indexOfExistItems[CHAR_STARTITEMARRAY+1]);
 }
 memcpy(reward_items,reuse_saved_items,sizeof reuse_saved_items);
 memcpy(slots,reuse_saved_actors,sizeof reuse_saved_actors);*arena=reuse_saved_arena;
 memcpy(cleanup_connections,reuse_saved_connections,sizeof reuse_saved_connections);
 ITEM_COUNT=reuse_saved_count;ITEM_SIZE=reuse_saved_size;rng_count=reuse_saved_rng;rng_mode=reuse_saved_mode;
 shared_guard_warnings=reuse_saved_warnings;diagnostics=reuse_saved_diagnostics;
 split_release_phase=reuse_saved_release_phase;split_release_calls=reuse_saved_release_calls;split_release_empty=reuse_saved_release_empty;
 memcpy(split_release_hits,reuse_saved_release_hits,sizeof reuse_saved_release_hits);
 demand(lookup_count>=reuse_saved_lookup&&Total_BattleNum==reuse_saved_total&&range_fdnum==2,"full isolated fixture restored apart from original factory cursor/lookup totals");
 }
'''


def controls(profile: str) -> str:
    c = item.substitutions(profile, CONTROL)
    return (c.replace("CONNECTION_TYPE", "GmsvSession" if profile == "bismarck" else "CONNECT")
             .replace("TABLE_TYPE", "ITEM_Index" if profile == "bismarck" else "ITEM_table")
             .replace("INDIRECT_SNAPSHOT", "ITEM_Table reuse_indirect_snapshot[3];memcpy(reuse_indirect_snapshot,factory_table,sizeof reuse_indirect_snapshot);" if profile == "bismarck" else "")
             .replace("INDIRECT_ORACLE", 'demand(!memcmp(reuse_indirect_snapshot,factory_table,sizeof reuse_indirect_snapshot),"whole indirect factory table unchanged");' if profile == "bismarck" else "")
             .replace("ENTRY_FIELD", "char_index" if profile == "bismarck" else "charaindex"))


def reuse_native(profile, source, battle, event, root):
    native, lua = prior.range_native(profile, source, battle, event, root)
    anchor = prior.controls(profile)
    native = replace_once(native, anchor, anchor + "\n" + controls(profile))
    original_battle = attack.pp_file(profile, root, attack.LAYOUTS[profile] / "battle/battle.c")
    original_item = attack.pp_file(profile, root, attack.LAYOUTS[profile] / "item/item.c")
    for name in ("BATTLE_AddExpItem", "BATTLE_ItemDelCheck"):
        body = attack.definition(native, name)
        if body != attack.definition(original_battle, name):
            raise ValueError("released-slot reuse original battle body changed: " + name)
        print(f"REUSE_ORIGINAL_BATTLE|{profile}|{name}|sha256={hashlib.sha256(body.encode()).hexdigest()}", flush=True)
    for name in ("ITEM_makeItem", "ITEM_makeItemAndRegist", "_ITEM_initExistItemsOne", "_ITEM_endExistItemsOne"):
        body = attack.definition(native, name)
        if body != attack.definition(original_item, name):
            raise ValueError("released-slot reuse original allocator body changed: " + name)
        print(f"REUSE_ORIGINAL_ITEM|{profile}|{name}|sha256={hashlib.sha256(body.encode()).hexdigest()}", flush=True)
    return native, lua


PROFILES = ("gavin", "bismarck")
ALIASES = (-1, 2, 0)


def validate_reuse_rows(lines):
    rows = {}
    for line in lines:
        if not line.startswith("ACTUAL|"):
            continue
        parts = line.split("|")
        if len(parts) < 5 or parts[2] != "REAL_HEADER_RELEASED_SLOT_REUSE":
            continue
        profile = parts[1]
        fields = [f.split("=", 1) for f in parts[3:]]
        if any(len(f) != 2 for f in fields):
            raise ValueError("malformed reuse evidence")
        f = dict(fields)
        if len(f) != len(fields):
            raise ValueError("duplicate reuse field")
        try:
            a = int(f["alias"])
            if profile not in PROFILES or a not in ALIASES:
                raise ValueError("unknown reuse profile / alias")
            if (profile, a) in rows:
                raise ValueError("duplicate reuse row")
            protected = a == 0
            expected = dict(victim=8, old_id=1, created=-1 if protected else 8,
                            new_id=1 if protected else 2, old_owner=6 if protected else -1,
                            new_owner=6 if protected else -1, released=0 if protected else 1,
                            guard_warnings=int(protected), factory_diagnostics=int(protected), release_calls=int(not protected),
                            assignment_draws=6, factory_draws=66,
                            count_delta=int(not protected), pet_ref=8 if a == 2 else -1,
                            player_ref=8 if protected else -1)
            for x in ("others_unchanged", "whole_actors", "whole_arena", "whole_connections",
                      "tables_immutable", "no_cursor_rewind", "original_creation",
                      "original_assignment", "original_factory", "synthetic_alias", "synthetic_blockers"):
                expected[x] = 1
            if set(f) != set(expected) | {"alias", "blockers"}:
                raise ValueError("missing/unknown original reuse field")
            if int(f["blockers"]) < 1 or any(int(f[k]) != v for k, v in expected.items()):
                raise ValueError("wrong item identity, owner, stale reference, release, or pool proof")
            rows[profile, a] = f
        except (KeyError, TypeError, IndexError) as exc:
            raise ValueError("incomplete released-slot reuse evidence") from exc
    if set(rows) != {(p, a) for p in PROFILES for a in ALIASES}:
        raise ValueError("missing original released-slot reuse matrix")
    return rows


def validate_report(report):
    prior.validate_report(report)
    rows = validate_reuse_rows(report.splitlines())
    if "RESOLUTION|ORIGINAL_REAL_HEADER_RELEASED_SLOT_REUSE_BOUNDED_PASS" not in report.splitlines():
        raise ValueError("missing reuse bounded resolution")
    return rows


def main():
    soft, hard = resource.getrlimit(resource.RLIMIT_STACK)
    if soft != resource.RLIM_INFINITY and soft < 64*1024*1024:
        resource.setrlimit(resource.RLIMIT_STACK, (64*1024*1024, hard))
    previous = ("FINISH_DISPATCH", "SAME_ITEM_CAPACITY", "TICKET_CLEANUP", "RECIPIENT_SIDE",
                "INVALID_ITEM_TICKET", "MIXED_ITEM_TICKET", "LAST_SLOT_TICKET", "DISTINCT_DROP_CREATE",
                "DISTINCT_ITEM_TICKET", "OVERFLOW_ASSIGN", "OVERFLOW_PAYOUT", "FOUR_DROP_CREATE",
                "FOUR_DROP_ASSIGN", "FOUR_DROP_PAYOUT", "TWO_PLAYER_ASSIGN", "TWO_PLAYER_PAYOUT",
                "TWO_PLAYER_CONCENTRATED_ASSIGN", "TWO_PLAYER_CONCENTRATED_PAYOUT", "SHARED_ITEM_ASSIGN",
                "SHARED_ITEM_PAYOUT", "PLAYER_PET_PARTITION_ASSIGN", "PLAYER_PET_PARTITION_PAYOUT",
                "GUARD_INDEX_RANGE", "RELEASED_SLOT_REUSE")
    attack.main(native_builder=reuse_native, extra_markers=tuple("REAL_HEADER_" + s + "|" for s in previous))
    print("BOUNDARY|original unchanged battle allocation and factory after original PET2/PLAYER0 carried alias; synthetic forced occupancy and controlled RNG; old physical index is not object identity; no natural master/alias/config/real session/early identity/modern DESIGN claim")
    for s in ("SAME_ITEM_CAPACITY", "TICKET_CLEANUP", "RECIPIENT_SIDE", "INVALID_ITEM_TICKET",
              "MIXED_ITEM_TICKET", "LAST_SLOT_TICKET", "DISTINCT_ITEM_TICKET", "OVERFLOW_TICKET",
              "FOUR_DROP_CHAIN", "TWO_PLAYER_SPLIT", "TWO_PLAYER_CONCENTRATED",
              "SHARED_ITEM_RETENTION", "PLAYER_PET_PARTITION", "GUARD_INDEX_RANGE",
              "RELEASED_SLOT_REUSE"):
        print("RESOLUTION|ORIGINAL_REAL_HEADER_" + s + "_BOUNDED_PASS")


if __name__ == "__main__":
    main()
