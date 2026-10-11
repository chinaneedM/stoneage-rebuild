"""Original three-object, two-template enemy drops and ordered last-slot payout."""
import hashlib
import itertools
import resource
from tools import stoneage_battle_original_last_slot_ticket_audit as prior

attack=prior.attack
item=prior.item
replace_once=prior.replace_once
PERMUTATIONS=tuple(itertools.permutations((4,5,6)))

CREATE=r'''
 static ITEM_TYPE distinct_original_items[256],distinct_created_items[256];
 static Char distinct_original_actors[7],distinct_created_actors[7];
 BATTLE distinct_original_arena=*arena;
 memcpy(distinct_original_items,reward_items,sizeof distinct_original_items);
 memcpy(distinct_original_actors,slots,sizeof distinct_original_actors);
 int distinct_original_count=ITEM_COUNT,distinct_original_size=ITEM_SIZE;
 int distinct_original_rng=rng_count,distinct_original_rng_mode=rng_mode;
 TABLE_TYPE distinct_old_index=allocator_table[2];
 INDIRECT_SAVE
 int distinct_master_items[10],distinct_master_probs[10];
 for(int i=0;i<10;i++){
  distinct_master_items[i]=master[ENEMY_ITEM1+i];distinct_master_probs[i]=master[ENEMY_ITEMPROB1+i];
  master[ENEMY_ITEM1+i]=0;master[ENEMY_ITEMPROB1+i]=0;
 }
 for(int box=0;box<CHAR_MAXITEMHAVE;box++)demand(slots[positive_actor].indexOfExistItems[box]==-1,"preceding restored enemy has no carried items before original disposal");
 CHAR_endCharOneArray(positive_actor);
 demand(!CHAR_CHECKINDEX(positive_actor)&&!memcmp(distinct_original_items,reward_items,sizeof distinct_original_items)&&ITEM_COUNT==distinct_original_count,"original empty-enemy disposal preserves complete pool/count");
 ITEM_Item distinct_template=specimen;distinct_template.data[ITEM_ID]=2;
 strcpy(distinct_template.string[ITEM_NAME].string,"FactoryTwo");
 strcpy(distinct_template.string[ITEM_UNIQUECODE].string,"factory-two");
 DISTINCT_TABLE_SETUP
 TABLE_TYPE distinct_index_snapshot[3];memcpy(distinct_index_snapshot,allocator_table,sizeof distinct_index_snapshot);
 INDIRECT_SNAPSHOT
 master[ENEMY_ITEM1]=1;master[ENEMY_ITEM1+1]=2;master[ENEMY_ITEM1+2]=1;
 for(int i=0;i<3;i++)master[ENEMY_ITEMPROB1+i]=1000;
 Char distinct_before_create[7];memcpy(distinct_before_create,slots,sizeof distinct_before_create);
 memcpy(distinct_created_items,reward_items,sizeof distinct_created_items);
 rng_mode=0;rng_count=0;
 int distinct_actor=ENEMY_createEnemy(0,2);
 demand(distinct_actor==4,"original character cursor wraps to actual free enemy four without rewind");
 demand(rng_count==zero_draws+3*(1+DATA_FIELDS),"three probability draws plus every field of three original factory objects");
 for(int k=0;k<3;k++){
  int index=4+k;
  ITEM_Item expected=k==1?distinct_template:specimen;
  expected.data[ITEM_LEAKLEVEL]=LEAK_EXPECTED;
  expected.workint[ITEM_WORKCHARAINDEX]=distinct_actor;expected.workint[ITEM_WORKOBJINDEX]=-1;
  distinct_created_items[index].use=1;distinct_created_items[index].ITEM_FIELD=expected;
  demand(slots[distinct_actor].indexOfExistItems[CHAR_STARTITEMARRAY+k]==index,"three original allocated drops carried in exact master order");
 }
 for(int k=3;k<10;k++)demand(slots[distinct_actor].indexOfExistItems[CHAR_STARTITEMARRAY+k]==-1,"other seven drop slots remain empty");
 demand(!memcmp(distinct_created_items,reward_items,sizeof distinct_created_items)&&ITEM_COUNT==distinct_original_count+3,"complete three-object original creation pool/count oracle");
 for(int a=0;a<7;a++)if(a!=distinct_actor)demand(!memcmp(&distinct_before_create[a],&slots[a],sizeof(Char)),"creation preserves six other full Char records");
 demand(!memcmp(&distinct_original_arena,arena,sizeof distinct_original_arena),"creation preserves full arena");
 demand(!memcmp(distinct_index_snapshot,allocator_table,sizeof distinct_index_snapshot),"complete three-entry index/master immutable during creation");
 INDIRECT_ORACLE
 arena->use=1;arena->Side[0].type=BATTLE_S_TYPE_PLAYER;arena->Side[1].type=BATTLE_S_TYPE_ENEMY;
 for(int s=0;s<2;s++)for(int e=0;e<BATTLE_ENTRY_MAX;e++){
  arena->Side[s].Entry[e].ENTRY_FIELD=-1;
  for(int k=0;k<GETITEM_MAX;k++)arena->Side[s].Entry[e].getitem[k]=-1;
 }
 arena->Side[0].Entry[0].ENTRY_FIELD=0;arena->Side[1].Entry[0].ENTRY_FIELD=distinct_actor;
 slots[distinct_actor].data[CHAR_HP]=0;CHAR_setFlg(distinct_actor,CHAR_ISDIE,FALSE);
 BATTLE distinct_ticket_expected=*arena;
 for(int k=0;k<3;k++)distinct_ticket_expected.Side[0].Entry[0].getitem[k]=4+k;
 Char distinct_before_ticket[7];memcpy(distinct_before_ticket,slots,sizeof distinct_before_ticket);
 int distinct_list[2]={0,-1};rng_count=0;
 demand(BATTLE_AddExpItem(battle_at,distinct_list)==0&&rng_count==3,"actual original AddExpItem assigns all three objects with three recipient draws");
 demand(!memcmp(&distinct_ticket_expected,arena,sizeof distinct_ticket_expected),"full arena exact three original pending ticket oracle");
 demand(!memcmp(distinct_created_items,reward_items,sizeof distinct_created_items)&&ITEM_COUNT==distinct_original_count+3,"assignment preserves full pool and original carried owners");
 for(int k=0;k<3;k++)demand(slots[distinct_actor].indexOfExistItems[CHAR_STARTITEMARRAY+k]==-1,"all three original carried slots clear on assignment");
 demand(CHAR_getFlg(distinct_actor,CHAR_ISDIE)&&slots[distinct_actor].data[CHAR_DEADCOUNT]==distinct_before_ticket[distinct_actor].data[CHAR_DEADCOUNT]+1&&slots[0].data[CHAR_KILLPETCOUNT]==distinct_before_ticket[0].data[CHAR_KILLPETCOUNT]+1,"original enemy death and direct-player kill count exactly once");
 for(int a=1;a<7;a++)if(a!=distinct_actor)demand(!memcmp(&distinct_before_ticket[a],&slots[a],sizeof(Char)),"ticket assignment preserves all five nonrecipient full records");
 memcpy(distinct_created_actors,slots,sizeof distinct_created_actors);
 printf("REAL_HEADER_DISTINCT_DROP_CREATE|mode=%d|actor=4|indices=4,5,6|ids=1,2,1|prob=1000|objects=3|templates=2|count_delta=3|factory_draws=%d|spawn_draws=%d|ticket_draws=3|pending=4,5,6|owner=4|whole_items=1|whole_other_actors=1|whole_arena=1|tables_immutable=1|carried_cleared=1|original_disposal=1|original_allocator=1\n",mode,DATA_FIELDS,zero_draws+3*(1+DATA_FIELDS));
'''

RESTORE=r'''
 memcpy(reward_items,distinct_original_items,sizeof distinct_original_items);
 memcpy(slots,distinct_original_actors,sizeof distinct_original_actors);*arena=distinct_original_arena;
 ITEM_COUNT=distinct_original_count;ITEM_SIZE=distinct_original_size;
 rng_count=distinct_original_rng;rng_mode=distinct_original_rng_mode;
 allocator_table[2]=distinct_old_index;
 INDIRECT_RESTORE
 for(int i=0;i<10;i++){master[ENEMY_ITEM1+i]=distinct_master_items[i];master[ENEMY_ITEMPROB1+i]=distinct_master_probs[i];}
'''


def create_controls(profile):
    c=item.substitutions(profile,CREATE);restore=item.substitutions(profile,RESTORE)
    b=profile=='bismarck';t='ITEM_Index' if b else 'ITEM_table'
    setup=('allocator_table[2].use=1;allocator_table[2].index=2;ITEM_sTableLen=3;factory_table[2]=factory_table[1];factory_table[2].item=distinct_template;' if b else
           'allocator_table[2]=allocator_table[1];allocator_table[2].use=1;allocator_table[2].itm=distinct_template;')
    subs={'TABLE_TYPE':t,'INDIRECT_SAVE':'ITEM_Table distinct_old_table=factory_table[2];int distinct_old_len=ITEM_sTableLen;' if b else '',
          'DISTINCT_TABLE_SETUP':setup,'INDIRECT_SNAPSHOT':'ITEM_Table distinct_table_snapshot[3];memcpy(distinct_table_snapshot,factory_table,sizeof distinct_table_snapshot);' if b else '',
          'INDIRECT_ORACLE':'demand(!memcmp(distinct_table_snapshot,factory_table,sizeof distinct_table_snapshot),"complete indirect factory table immutable");' if b else '',
          'INDIRECT_RESTORE':'factory_table[2]=distinct_old_table;ITEM_sTableLen=distinct_old_len;' if b else '',
          'DATA_FIELDS':'ITEM_DATA_ENUM_MAX' if b else 'ITEM_DATAINTNUM','LEAK_EXPECTED':'0' if b else '1',
          'ENTRY_FIELD':'char_index' if b else 'charaindex'}
    for k,v in subs.items():c=c.replace(k,v);restore=restore.replace(k,v)
    return c,restore


def competition_controls(profile):
    c=prior.last_slot_controls(profile).replace('lastslot_','distinct_').replace('positive_actor','distinct_actor')
    start=c.index(' for(int available=0;');end=c.index('\n  int recipient=0;',start)
    c=c[:start]+''' int permutations[6][3]={{4,5,6},{4,6,5},{5,4,6},{5,6,4},{6,4,5},{6,5,4}};
 for(int available=0;available<2;available++){
 for(int order=0;order<6;order++){
  int *pattern=permutations[order],first_valid=0,awards=available;
  distinct_winner=available?pattern[0]:-1;
'''+c[end:]
    c=replace_once(c,'\n }\n }\n }\n }\n memcpy(reward_items,distinct_saved_items','\n }\n }\n memcpy(reward_items,distinct_saved_items')
    c=replace_once(c,'reward_phase=2;','reward_phase=4;')
    a=c.index('   distinct_release_phase=1;');z=c.index('   demand(cleanup_ret',a)
    c=c[:a]+'''   distinct_release_phase=1;distinct_release_calls=distinct_release_empty=0;memset(distinct_release_hits,0,sizeof distinct_release_hits);
   int cleanup_ret=BATTLE_Loop();distinct_release_phase=0;
   if(!with_ticket)distinct_baseline_release=distinct_release_empty;
   demand(distinct_release_empty==distinct_baseline_release&&distinct_release_calls==distinct_release_empty+(with_ticket?3-available:0),"full original release counts versus no-ticket teardown");
   for(int k=0;k<3;k++)demand(distinct_release_hits[k]==(with_ticket&&(!available||k+4!=distinct_winner)?1:0),"each unawarded distinct object released exactly once");
'''+c[z:]
    a=c.index('    if(available){');z=c.index('    demand(!memcmp(distinct_expected_items',a)
    c=c[:a]+item.substitutions(profile,'''    for(int k=0;k<3;k++){
     int index=4+k;
     if(index==distinct_winner){
      distinct_expected_items[index].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]=0;
      distinct_expected_items[index].ITEM_FIELD.workint[ITEM_WORKOBJINDEX]=-1;
      distinct_expected_actors[0].indexOfExistItems[first_slot]=index;
     }else{
      distinct_expected_items[index].use=0;
      distinct_expected_items[index].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]=-1;expected_count--;
     }
    }
''')+c[z:]
    a=c.index('    int references=0;');z=c.index('    char distinct_expected_rs',a)
    c=c[:a]+'''    int references[3]={0,0,0};
    for(int actor=0;actor<7;actor++)for(int box=0;box<CHAR_MAXITEMHAVE;box++){
     int index=slots[actor].indexOfExistItems[box];if(index>=4&&index<=6)references[index-4]++;
    }
    for(int k=0;k<3;k++)demand(references[k]==(k+4==distinct_winner),"complete distinct object reference oracle");
'''+c[z:]
    c=replace_once(c,'strcat(distinct_expected_rs,"Factory")' if profile=='bismarck' else 'strcat(distinct_expected_rs,"")',
                   'strcat(distinct_expected_rs,distinct_winner==5?"FactoryTwo":"Factory")' if profile=='bismarck' else 'strcat(distinct_expected_rs,"")')
    a=c.index('    for(int actor=0;actor<7;actor++)for(int box=0;box<CHAR_MAXITEMHAVE;box++)\n     demand(slots[actor].indexOfExistItems[box]!=invalids');z=c.index('   }\n   reward_phase=0;',a)
    out=item.substitutions(profile,r'''    printf("REAL_HEADER_DISTINCT_ITEM_TICKET|available=%d|order=%d|pattern=%d,%d,%d|winner=%d|winner_id=%d|accepted_mask=%d|awards=%d|bag_slot=%d|active_limit=%d|named_items=NAMED|pool_size=256|count_delta=%d|live4=%d|live5=%d|live6=%d|owner4=%d|owner5=%d|owner6=%d|ref4=%d|ref5=%d|ref6=%d|release4=%d|release5=%d|release6=%d|release_empty=%d|baseline_release=%d|release_calls=%d|logs=%d|data=%d|one=%d|rs=1|packet_oracle=1|second_loop=1|arena_released=1|tickets_cleared=1|whole_items=1|whole_fillers=1|whole_actors=1|whole_arena=1|whole_connections=1|original_timer=1|original_creation=1|original_ticket_assignment=1\n",
     available,order,pattern[0],pattern[1],pattern[2],distinct_winner,available?(distinct_winner==5?2:1):-1,available,awards,first_slot,active_limit,
     ITEM_COUNT-input_count,reward_items[4].use,reward_items[5].use,reward_items[6].use,
     reward_items[4].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX],reward_items[5].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX],reward_items[6].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX],
     references[0],references[1],references[2],distinct_release_hits[0],distinct_release_hits[1],distinct_release_hits[2],distinct_release_empty,distinct_baseline_release,distinct_release_calls,reward_log_count,reward_data_count,reward_one_count);
''').replace('NAMED','%d').replace('active_limit,\n','active_limit,'+('available' if profile=='bismarck' else '0')+',\n')
    return c[:a]+out+c[z:]

OBSERVER=r'''
static int distinct_release_phase,distinct_release_calls,distinct_release_empty,distinct_release_hits[3],distinct_winner;
static void distinct_release_observer(int index,char *file,int line){
 if(distinct_release_phase){distinct_release_calls++;if(index==-1)distinct_release_empty++;else {demand(index>=4&&index<=6,"only three distinct created objects released");distinct_release_hits[index-4]++;}}
 lastslot_release_observer(index,file,line);
}
#undef ITEM_endExistItemsOne
#define ITEM_endExistItemsOne(index) distinct_release_observer(index,__FILE__,__LINE__)
'''


def distinct_native(profile,source,battle,event,root):
    n,lua=prior.last_slot_native(profile,source,battle,event,root)
    n=replace_once(n,prior.OBSERVER,prior.OBSERVER+'\n'+OBSERVER)
    if profile=='bismarck':n=replace_once(n,'static ITEM_Table factory_table[2];','static ITEM_Table factory_table[3];')
    for name in ('CHAR_sendItemData','CHAR_sendItemDataOne','LogItem'):
        body=attack.definition(n,name);brace=body.index('{')
        if name=='LogItem':check=r'''
 if(reward_phase==4){
  int expected_id=distinct_winner==5?2:1;
  const char *expected_name=distinct_winner==5?"FactoryTwo":"Factory";
  const char *expected_code=distinct_winner==5?"factory-two":"factory-bounded";
  demand(distinct_winner>=4&&item==distinct_winner&&id==expected_id&&!strcmp(itemname,expected_name)&&!strcmp(code,expected_code)&&name&&key&&!strcmp(cause,"BattleGet(战斗後所得的道具)")&&floor==slots[0].data[CHAR_FLOOR]&&x==slots[0].data[CHAR_X]&&y==slots[0].data[CHAR_Y],"typed distinct pickup log identity");
  settle_log_count++;reward_log_count++;return;
 }
'''
        else:
            condition='count==1&&indices[0]==reward_expected_slot' if name=='CHAR_sendItemData' else 'slot==reward_expected_slot'
            count='reward_data_count' if name=='CHAR_sendItemData' else 'reward_one_count'
            check='\n if(reward_phase==4){demand(actor==0&&distinct_winner>=4&&'+condition+'&&slots[0].indexOfExistItems[reward_expected_slot]==distinct_winner,"typed distinct reward inventory send identity");'+count+'++;return TRUE;}\n'
        n=replace_once(n,body,body[:brace+1]+check+body[brace+1:])
    old=prior.last_slot_controls(profile);create,restore=create_controls(profile)
    n=replace_once(n,old,old+'\n'+create+'\n'+competition_controls(profile)+'\n'+restore)
    for path,names in {'char/char_base.c':('CHAR_initCharOneArray','_CHAR_endCharOneArray' if profile=='bismarck' else 'CHAR_endCharOneArray'),'item/item.c':('ITEM_makeItem','ITEM_makeItemAndRegist','_ITEM_initExistItemsOne'),'battle/battle.c':('BATTLE_AddExpItem',)}.items():
        original=attack.pp_file(profile,root,attack.LAYOUTS[profile]/path)
        for name in names:
            body=attack.definition(n,name)
            expected=attack.definition(source,name) if name=='CHAR_initCharOneArray' else attack.definition(original,name)
            if body!=expected:raise ValueError('distinct original body drift '+name)
            print(f'DISTINCT_ITEM_SOURCE|{profile}|{name}|inherited_sha256={hashlib.sha256(body.encode()).hexdigest()}|preprocessed_sha256={hashlib.sha256(attack.definition(original,name).encode()).hexdigest()}',flush=True)
    return n,lua


def validate_report(report):
    prior.validate_report(report);rows={};created={}
    for line in report.splitlines():
        if not line.startswith('ACTUAL|'):continue
        parts=line.split('|');profile=parts[1]
        if parts[2] not in ('REAL_HEADER_DISTINCT_DROP_CREATE','REAL_HEADER_DISTINCT_ITEM_TICKET'):continue
        try:
            f=dict(p.split('=',1) for p in parts[3:])
            if profile not in ('gavin','bismarck'):raise ValueError('unknown distinct profile')
            if parts[2]=='REAL_HEADER_DISTINCT_DROP_CREATE':
                if profile in created:raise ValueError('duplicate creation witness')
                for key,value in dict(mode=3,actor=4,indices='4,5,6',ids='1,2,1',prob=1000,objects=3,templates=2,count_delta=3,ticket_draws=3,pending='4,5,6',owner=4,factory_draws=66,spawn_draws=215).items():
                    if f[key]!=str(value):raise ValueError('distinct creation identity mismatch')
                for key in ('whole_items','whole_other_actors','whole_arena','tables_immutable','carried_cleared','original_disposal','original_allocator'):
                    if f[key]!='1':raise ValueError('incomplete original creation oracle')
                created[profile]=f;continue
            a=int(f['available']);o=int(f['order']);key=profile,a,o
            if a not in (0,1) or o not in range(6) or key in rows:raise ValueError('unknown/duplicate distinct pattern')
            p=PERMUTATIONS[o];w=p[0] if a else -1;baseline=84 if profile=='bismarck' else 54
            expected=dict(winner=w,winner_id=(2 if w==5 else 1) if a else -1,accepted_mask=a,awards=a,bag_slot=(53 if profile=='bismarck' else 23) if a else -1,active_limit=54 if profile=='bismarck' else 24,named_items=a if profile=='bismarck' else 0,pool_size=256,count_delta=a-3,release_empty=baseline,baseline_release=baseline,release_calls=baseline+3-a,logs=a,data=a,one=a if profile=='bismarck' else 0,rs=1)
            for i in (4,5,6):expected.update({f'live{i}':int(w==i),f'owner{i}':0 if w==i else -1,f'ref{i}':int(w==i),f'release{i}':int(w!=i)})
            for field in ('packet_oracle','second_loop','arena_released','tickets_cleared','whole_items','whole_fillers','whole_actors','whole_arena','whole_connections','original_timer','original_creation','original_ticket_assignment'):expected[field]=1
            if f['pattern']!=','.join(map(str,p)) or any(int(f[n])!=v for n,v in expected.items()):raise ValueError('distinct ordered payout oracle mismatch')
            rows[key]=f
        except (KeyError,TypeError) as exc:raise ValueError('incomplete distinct witness') from exc
    if set(created)!={'gavin','bismarck'} or set(rows)!={(p,a,o) for p in ('gavin','bismarck') for a in (0,1) for o in range(6)}:raise ValueError('missing distinct creation/capacity/order')
    if 'RESOLUTION|ORIGINAL_REAL_HEADER_DISTINCT_ITEM_TICKET_BOUNDED_PASS' not in report.splitlines():raise ValueError('missing distinct resolution')
    return rows


def main():
    soft,hard=resource.getrlimit(resource.RLIMIT_STACK)
    if soft!=resource.RLIM_INFINITY and soft<64*1024*1024:resource.setrlimit(resource.RLIMIT_STACK,(64*1024*1024,hard))
    markers=tuple('REAL_HEADER_'+s+'|' for s in ('FINISH_DISPATCH','SAME_ITEM_CAPACITY','TICKET_CLEANUP','RECIPIENT_SIDE','INVALID_ITEM_TICKET','MIXED_ITEM_TICKET','LAST_SLOT_TICKET','DISTINCT_DROP_CREATE','DISTINCT_ITEM_TICKET'))
    attack.main(native_builder=distinct_native,extra_markers=markers)
    print('BOUNDARY|explicit synthetic two-template/three-drop master, guaranteed draws, full/one-free bag and permutations after original assignment; no natural master/permutation reachability, early identity, real-client or modern DESIGN')
    for s in ('SAME_ITEM_CAPACITY','TICKET_CLEANUP','RECIPIENT_SIDE','INVALID_ITEM_TICKET','MIXED_ITEM_TICKET','LAST_SLOT_TICKET','DISTINCT_ITEM_TICKET'):print('RESOLUTION|ORIGINAL_REAL_HEADER_'+s+'_BOUNDED_PASS')


if __name__=='__main__':main()
