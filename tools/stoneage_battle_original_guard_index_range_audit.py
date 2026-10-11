"""Original ItemDelCheck index range crossed with type, use flag and alias.

Only the isolated configuration adapter and explicitly snapshotted inputs vary.
No original game body is edited; all preceding creation and payout gates remain.
"""
import hashlib
import resource
from tools import stoneage_battle_original_player_pet_partition_audit as prior

attack=prior.attack
item=prior.item
replace_once=prior.replace_once

CONTROL=r'''
 {
 static ITEM_TYPE range_saved_items[256],range_input_items[256];
 static Char range_saved_actors[7],range_input_actors[7];
 BATTLE range_saved_arena=*arena,range_input_arena;
 CONNECTION_TYPE range_saved_connections[8],range_input_connections[8];
 TABLE_TYPE range_saved_tables[3];memcpy(range_saved_tables,allocator_table,sizeof range_saved_tables);
 INDIRECT_SNAPSHOT
 memcpy(range_saved_items,reward_items,sizeof range_saved_items);memcpy(range_saved_actors,slots,sizeof range_saved_actors);
 memcpy(range_saved_connections,cleanup_connections,sizeof range_saved_connections);
 int range_saved_count=ITEM_COUNT,range_saved_size=ITEM_SIZE,range_saved_rng=rng_count,range_saved_mode=rng_mode;
 int range_saved_warnings=shared_guard_warnings,range_saved_diagnostics=diagnostics,range_saved_fd=range_fdnum;
 int range_saved_release_phase=split_release_phase,range_saved_release_calls=split_release_calls,range_saved_release_empty=split_release_empty,range_saved_hits[4];
 memcpy(range_saved_hits,split_release_hits,sizeof range_saved_hits);
 for(int fdnum=2;fdnum<=3;fdnum++)for(int index=0;index<3;index++)for(int kind=0;kind<2;kind++)for(int active=0;active<2;active++)for(int alias=0;alias<2;alias++){
  memcpy(reward_items,chain_created_items,sizeof range_saved_items);memcpy(slots,chain_created_actors,sizeof range_saved_actors);
  *arena=range_saved_arena;ITEM_COUNT=chain_after_create;ITEM_SIZE=256;
  demand(CHAR_getInt(2,CHAR_WHICHTYPE)==CHAR_TYPEPET&&slots[0].unionTable.indexOfPet[0]==2,"retained initial owned PET2 before explicit type/use crossing");
  for(int a=0;a<3;a++)for(int box=0;box<CHAR_MAXITEMHAVE;box++)if(slots[a].indexOfExistItems[box]==8)slots[a].indexOfExistItems[box]=-1;
  int box=CHAR_STARTITEMARRAY+1;
  slots[index].data[CHAR_WHICHTYPE]=kind?CHAR_TYPEPET:CHAR_TYPEPLAYER;
  slots[index].use=active;
  slots[index].indexOfExistItems[box]=alias?8:-1;
  range_fdnum=fdnum;
  int blocked=active&&alias&&index<fdnum;
  demand(reward_items[8].use&&reward_items[8].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]==6,"original-created query8 retains live owner6 before direct guard");
  memcpy(range_input_items,reward_items,sizeof range_input_items);memcpy(range_input_actors,slots,sizeof range_input_actors);range_input_arena=*arena;
  memcpy(range_input_connections,cleanup_connections,sizeof range_input_connections);
  int before_count=ITEM_COUNT,before_size=ITEM_SIZE,before_rng=rng_count,before_mode=rng_mode,before_lookup=lookup_count,before_total=Total_BattleNum;
  int before_diagnostics=diagnostics;
  shared_guard_warnings=0;split_release_phase=1;split_release_calls=split_release_empty=0;memset(split_release_hits,0,sizeof split_release_hits);
  int result=BATTLE_ItemDelCheck(8);
  demand(result==1-blocked&&shared_guard_warnings==blocked&&diagnostics==before_diagnostics+blocked,"original guard exact return and diagnostic crossed with index/type/use/alias");
  demand(!memcmp(range_input_items,reward_items,sizeof range_input_items)&&ITEM_COUNT==before_count&&ITEM_SIZE==before_size,"direct original guard leaves whole256 pool/count/size unchanged");
  demand(!memcmp(range_input_actors,slots,sizeof range_input_actors)&&!memcmp(&range_input_arena,arena,sizeof range_input_arena),"direct original guard leaves all seven complete actors and arena unchanged");
  demand(!memcmp(range_input_connections,cleanup_connections,sizeof range_input_connections)&&rng_count==before_rng&&rng_mode==before_mode&&lookup_count==before_lookup&&Total_BattleNum==before_total,"whole eight connections and RNG/lookup/battle count unchanged");
  demand(!memcmp(range_saved_tables,allocator_table,sizeof range_saved_tables),"all three direct/index factory records unchanged");
  INDIRECT_ORACLE
  demand(!split_release_calls&&!split_release_empty&&!split_release_hits[0]&&!split_release_hits[1]&&!split_release_hits[2]&&!split_release_hits[3],"guard decision alone never releases any object");
  printf("REAL_HEADER_GUARD_INDEX_RANGE|fdnum=%d|index=%d|type=%s|active=%d|alias=%d|query=8|box=%d|scan_limit=%d|calls=1|result=%d|guard_warnings=%d|diagnostic_delta=%d|release_calls=0|count_delta=0|victim_live=%d|victim_owner=%d|whole_items=1|whole_actors=1|whole_arena=1|whole_connections=1|tables_immutable=1|rng_unchanged=1|lookups_unchanged=1|battle_count_unchanged=1|original_guard=1|synthetic_config=1|synthetic_type_use_alias=1\n",fdnum,index,kind?"PET":"PLAYER",active,alias,box,SCAN_LIMIT,result,shared_guard_warnings,diagnostics-before_diagnostics,reward_items[8].use,reward_items[8].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]);
 }
 memcpy(reward_items,range_saved_items,sizeof range_saved_items);memcpy(slots,range_saved_actors,sizeof range_saved_actors);*arena=range_saved_arena;
 memcpy(cleanup_connections,range_saved_connections,sizeof range_saved_connections);
 ITEM_COUNT=range_saved_count;ITEM_SIZE=range_saved_size;rng_count=range_saved_rng;rng_mode=range_saved_mode;
 shared_guard_warnings=range_saved_warnings;diagnostics=range_saved_diagnostics;range_fdnum=range_saved_fd;
 split_release_phase=range_saved_release_phase;split_release_calls=range_saved_release_calls;split_release_empty=range_saved_release_empty;memcpy(split_release_hits,range_saved_hits,sizeof range_saved_hits);
 demand(range_fdnum==2,"configuration adapter restored for retained witnesses");
 }
'''


def controls(profile):
    c=item.substitutions(profile,CONTROL)
    return (c.replace('CONNECTION_TYPE','GmsvSession' if profile=='bismarck' else 'CONNECT')
            .replace('TABLE_TYPE','ITEM_Index' if profile=='bismarck' else 'ITEM_table')
            .replace('INDIRECT_SNAPSHOT','ITEM_Table range_saved_indirect[3];memcpy(range_saved_indirect,factory_table,sizeof range_saved_indirect);' if profile=='bismarck' else '')
            .replace('INDIRECT_ORACLE','demand(!memcmp(range_saved_indirect,factory_table,sizeof range_saved_indirect),"all three indirect factory records unchanged");' if profile=='bismarck' else '')
            .replace('SCAN_LIMIT','CheckCharMaxItem(index)' if profile=='bismarck' else 'CHAR_MAXITEMHAVE'))


def range_native(profile,source,battle,event,root):
    n,lua=prior.partition_native(profile,source,battle,event,root)
    n='static unsigned int range_fdnum=2;\n'+replace_once(n,'unsigned int getFdnum(void){if(CHAR_playernum!=2)abort();return 2;}',
                   'unsigned int getFdnum(void){if(CHAR_playernum!=2)abort();return range_fdnum;}')
    old=prior.controls(profile)
    n=replace_once(n,old,old+'\n'+controls(profile))
    original=attack.pp_file(profile,root,attack.LAYOUTS[profile]/'battle/battle.c')
    for name in ('BATTLE_AddExpItem','BATTLE_ItemDelCheck','BATTLE_GetProfit','BATTLE_GetExpGold','BATTLE_Finish','BATTLE_DeleteBattle'):
        body=attack.definition(n,name)
        if body!=attack.definition(original,name):raise ValueError('guard range original battle body drift '+name)
        print(f'RANGE_SOURCE|{profile}|{name}|sha256={hashlib.sha256(body.encode()).hexdigest()}',flush=True)
    reward_helpers=item.original_parts(profile,root)
    for name in ('_CHAR_CHECKINDEX','_CHAR_CHECKITEMINDEX','_CHAR_getItemIndex')+(('CheckCharMaxItem',) if profile=='bismarck' else ()):
        body=attack.definition(n,name)
        expected=reward_helpers.get(name,attack.definition(source,name))
        if body!=expected:raise ValueError('guard range accepted original helper drift '+name)
        print(f'RANGE_HELPER|{profile}|{name}|inherited_sha256={hashlib.sha256(body.encode()).hexdigest()}',flush=True)
    return n,lua


def validate_report(report):
    prior.validate_report(report)
    rows={}
    for line in report.splitlines():
        if not line.startswith('ACTUAL|'):continue
        p=line.split('|')
        if p[2]!='REAL_HEADER_GUARD_INDEX_RANGE':continue
        try:
            pairs=[v.split('=',1) for v in p[3:]]
            f=dict(pairs)
            if len(f)!=len(pairs):raise ValueError('duplicate guard field')
            profile=p[1];fd=int(f['fdnum']);index=int(f['index']);kind=f['type'];active=int(f['active']);alias=int(f['alias'])
            key=profile,fd,index,kind,active,alias
            if profile not in ('gavin','bismarck') or fd not in (2,3) or index not in (0,1,2) or kind not in ('PLAYER','PET') or active not in (0,1) or alias not in (0,1):raise ValueError('unknown guard range identity')
            blocked=int(bool(active and alias and index<fd))
            expected=dict(query=8,box=10,scan_limit=54 if profile=='bismarck' else 24,calls=1,result=1-blocked,guard_warnings=blocked,diagnostic_delta=blocked,release_calls=0,count_delta=0,victim_live=1,victim_owner=6)
            ones=('whole_items','whole_actors','whole_arena','whole_connections','tables_immutable','rng_unchanged','lookups_unchanged','battle_count_unchanged','original_guard','synthetic_config','synthetic_type_use_alias')
            expected.update({k:1 for k in ones})
            if set(f)!=set(expected)|{'fdnum','index','type','active','alias'}:raise ValueError('incomplete/unknown guard range fields')
            if key in rows or any(int(f[k])!=v for k,v in expected.items()):raise ValueError('incorrect original guard return or no-state-mutation evidence')
            rows[key]=f
        except (KeyError,TypeError,IndexError) as exc:raise ValueError('incomplete guard range witness') from exc
    matrix={(p,fd,i,t,u,a) for p in ('gavin','bismarck') for fd in (2,3) for i in range(3) for t in ('PLAYER','PET') for u in (0,1) for a in (0,1)}
    if set(rows)!=matrix:raise ValueError('missing original guard index/type/use/alias matrix')
    if 'RESOLUTION|ORIGINAL_REAL_HEADER_GUARD_INDEX_RANGE_BOUNDED_PASS' not in report.splitlines():raise ValueError('missing guard range resolution')
    return rows


def main():
    soft,hard=resource.getrlimit(resource.RLIMIT_STACK)
    if soft!=resource.RLIM_INFINITY and soft<64*1024*1024:resource.setrlimit(resource.RLIMIT_STACK,(64*1024*1024,hard))
    markers=tuple('REAL_HEADER_'+s+'|' for s in ('FINISH_DISPATCH','SAME_ITEM_CAPACITY','TICKET_CLEANUP','RECIPIENT_SIDE','INVALID_ITEM_TICKET','MIXED_ITEM_TICKET','LAST_SLOT_TICKET','DISTINCT_DROP_CREATE','DISTINCT_ITEM_TICKET','OVERFLOW_ASSIGN','OVERFLOW_PAYOUT','FOUR_DROP_CREATE','FOUR_DROP_ASSIGN','FOUR_DROP_PAYOUT','TWO_PLAYER_ASSIGN','TWO_PLAYER_PAYOUT','TWO_PLAYER_CONCENTRATED_ASSIGN','TWO_PLAYER_CONCENTRATED_PAYOUT','SHARED_ITEM_ASSIGN','SHARED_ITEM_PAYOUT','PLAYER_PET_PARTITION_ASSIGN','PLAYER_PET_PARTITION_PAYOUT','GUARD_INDEX_RANGE'))
    attack.main(native_builder=range_native,extra_markers=markers)
    print('BOUNDARY|direct unchanged original guard; explicit configuration adapter2/3; index0/1/2 crossed with PLAYER/PET type, use flag and synthetic alias; complete native snapshots; retained predecessor factory/assignment/payout; no original configuration getter execution, natural reachability, released-slot reuse, early identity, real client/network or modern DESIGN')
    for s in ('SAME_ITEM_CAPACITY','TICKET_CLEANUP','RECIPIENT_SIDE','INVALID_ITEM_TICKET','MIXED_ITEM_TICKET','LAST_SLOT_TICKET','DISTINCT_ITEM_TICKET','OVERFLOW_TICKET','FOUR_DROP_CHAIN','TWO_PLAYER_SPLIT','TWO_PLAYER_CONCENTRATED','SHARED_ITEM_RETENTION','PLAYER_PET_PARTITION','GUARD_INDEX_RANGE'):print('RESOLUTION|ORIGINAL_REAL_HEADER_'+s+'_BOUNDED_PASS')


if __name__=='__main__':main()
