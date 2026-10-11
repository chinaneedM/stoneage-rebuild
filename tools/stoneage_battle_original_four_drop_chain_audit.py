"""One unchanged enemy creation and one uninterrupted four-drop assignment."""
import hashlib
import resource
from tools import stoneage_battle_original_overflow_ticket_audit as prior
attack=prior.attack
item=prior.item
replace_once=prior.replace_once
PATTERNS=((8,9,10),(11,9,10),(8,11,10),(8,9,11))

RNG=r'''
static int chain_rng_phase,chain_rng_branch,chain_rng_at;
static int chain_rand(void){
 if(!chain_rng_phase)return overflow_rand();
 int at=chain_rng_at++;rng_count++;
 demand(at<6,"bounded uninterrupted four-drop assignment draw count");
 if(at<4)return 0;
 if(at==4)return chain_rng_branch?2147483647:0;
 int values[3]={0,1073741824,2147483647};return values[chain_rng_branch-1];
}
#undef rand
#define rand chain_rand
'''

OBSERVER=r'''
static int chain_release_phase,chain_release_calls,chain_release_empty,chain_release_hits[4],chain_winner;
static void chain_release_observer(int index,char *file,int line){
 if(chain_release_phase){chain_release_calls++;if(index==-1)chain_release_empty++;else {demand(index>=8&&index<=11,"only four original chain-created items released");chain_release_hits[index-8]++;}}
 distinct_release_observer(index,file,line);
}
#undef ITEM_endExistItemsOne
#define ITEM_endExistItemsOne(index) chain_release_observer(index,__FILE__,__LINE__)
'''

CONTROL=r'''
 {
 static ITEM_TYPE chain_saved_items[256],chain_created_items[256],chain_input_items[256],chain_expected_items[256],chain_control_items[256];
 static Char chain_before_create[7],chain_saved_actors[7],chain_created_actors[7],chain_control_actors[7],chain_expected_actors[7];
 BATTLE chain_saved_arena=*arena,chain_input_arena,chain_control_arena,chain_expected_arena;
 memcpy(chain_saved_items,reward_items,sizeof chain_saved_items);memcpy(chain_saved_actors,slots,sizeof chain_saved_actors);
 int chain_saved_count=ITEM_COUNT,chain_saved_size=ITEM_SIZE,chain_saved_rng=rng_count,chain_saved_mode=rng_mode;
 int chain_saved_ids[10],chain_saved_probs[10];
 for(int i=0;i<10;i++){
  chain_saved_ids[i]=master[ENEMY_ITEM1+i];chain_saved_probs[i]=master[ENEMY_ITEMPROB1+i];
  master[ENEMY_ITEM1+i]=0;master[ENEMY_ITEMPROB1+i]=0;
 }
 int chain_blockers=0,chain_blockmask=0,chain_stale_refs=0;ITEM_SIZE=256;
 for(int i=0;i<8;i++)if(!reward_items[i].use){
  /* Explicit allocator occupancy inputs; never overwrite an original live object. */
  reward_items[i].use=1;memset(&reward_items[i].ITEM_FIELD,0,sizeof(ITEM_Item));reward_items[i].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]=-1;
  reward_items[i].ITEM_FIELD.workint[ITEM_WORKOBJINDEX]=-1;ITEM_COUNT++;chain_blockers++;chain_blockmask|=1<<i;
 }
 /* Remove only pre-existing dangling references to records that were inactive before occupancy inputs. */
 for(int a=0;a<7;a++)if(slots[a].use)for(int box=0;box<CHAR_MAXITEMHAVE;box++){
  int index=slots[a].indexOfExistItems[box];
  if(index>=0&&index<8&&(chain_blockmask&(1<<index))){slots[a].indexOfExistItems[box]=-1;chain_stale_refs++;}
 }
 memcpy(chain_before_create,slots,sizeof chain_before_create);
 memcpy(chain_created_items,reward_items,sizeof chain_created_items);int chain_before_count=ITEM_COUNT;
 for(int k=0;k<4;k++){master[ENEMY_ITEM1+k]=k%2?2:1;master[ENEMY_ITEMPROB1+k]=1000;}
 TABLE_TYPE chain_index_snapshot[3];memcpy(chain_index_snapshot,allocator_table,sizeof chain_index_snapshot);
 INDIRECT_SNAPSHOT
 rng_mode=0;rng_count=0;int chain_actor=ENEMY_createEnemy(0,2);
 demand(chain_actor==6&&CHAR_CHECKINDEX(chain_actor),"unchanged original character cursor finds free enemy six");
 demand(rng_count==zero_draws+4*(1+66),"four original probability draws and four complete native factories");
 for(int k=0;k<4;k++){
  int index=8+k;demand(!chain_created_items[index].use,"new chain object was previously inactive");
  ITEM_Item expected=k%2?distinct_template:specimen;expected.data[ITEM_LEAKLEVEL]=LEAK_EXPECTED;
  expected.workint[ITEM_WORKCHARAINDEX]=chain_actor;expected.workint[ITEM_WORKOBJINDEX]=-1;
  chain_created_items[index].use=1;chain_created_items[index].ITEM_FIELD=expected;
  demand(slots[chain_actor].indexOfExistItems[CHAR_STARTITEMARRAY+k]==index,"original four carried objects in master order without ownership rebinding");
 }
 for(int k=4;k<10;k++)demand(slots[chain_actor].indexOfExistItems[CHAR_STARTITEMARRAY+k]==-1,"other six master drop slots remain empty");
 demand(!memcmp(chain_created_items,reward_items,sizeof chain_created_items)&&ITEM_COUNT==chain_before_count+4,"complete original four-drop pool/count creation oracle");
 for(int a=0;a<7;a++)if(a!=chain_actor)demand(!memcmp(&chain_before_create[a],&slots[a],sizeof(Char)),"creation preserves six other complete actors");
 demand(!memcmp(&chain_saved_arena,arena,sizeof chain_saved_arena),"creation preserves whole original arena");
 demand(!memcmp(chain_index_snapshot,allocator_table,sizeof chain_index_snapshot),"complete index table immutable during four factories");
 INDIRECT_ORACLE
 fflush(stdout);printf("REAL_HEADER_FOUR_DROP_CREATE|actor=6|indices=8,9,10,11|ids=1,2,1,2|objects=4|templates=2|prob=1000|factory_draws=66|spawn_draws=%d|count_delta=4|blockers=%d|cleared_inactive_refs=%d|pool_size=256|owner=6|object=-1|whole_items=1|whole_other_actors=1|whole_arena=1|tables_immutable=1|original_creation=1|no_rebinding=1|no_cursor_rewind=1\n",rng_count,chain_blockers,chain_stale_refs);fflush(stdout);
 memcpy(chain_created_actors,slots,sizeof chain_created_actors);
 chain_input_arena=*arena;chain_input_arena.use=1;chain_input_arena.Side[0].type=BATTLE_S_TYPE_PLAYER;chain_input_arena.Side[1].type=BATTLE_S_TYPE_ENEMY;
 for(int s=0;s<2;s++)for(int e=0;e<BATTLE_ENTRY_MAX;e++){
  chain_input_arena.Side[s].Entry[e].ENTRY_FIELD=-1;
  for(int k=0;k<GETITEM_MAX;k++)chain_input_arena.Side[s].Entry[e].getitem[k]=-1;
 }
 chain_input_arena.Side[0].Entry[0].ENTRY_FIELD=0;chain_input_arena.Side[1].Entry[0].ENTRY_FIELD=chain_actor;
 int chain_after_create=ITEM_COUNT,chain_list[2]={0,-1};
 for(int branch=0;branch<4;branch++){
  int victim=branch?7+branch:11;
  int pending[3]={8,9,10};if(branch)pending[branch-1]=11;
  for(int with_item=0;with_item<2;with_item++){
   memcpy(reward_items,chain_created_items,sizeof chain_created_items);memcpy(slots,chain_created_actors,sizeof chain_created_actors);
   *arena=chain_input_arena;ITEM_COUNT=chain_after_create;
   CHAR_setFlg(chain_actor,CHAR_ISDIE,FALSE);slots[chain_actor].data[CHAR_HP]=0;
   if(!with_item)for(int k=0;k<4;k++)slots[chain_actor].indexOfExistItems[CHAR_STARTITEMARRAY+k]=-1;
   chain_rng_phase=1;chain_rng_branch=branch;chain_rng_at=0;rng_count=0;
   chain_release_phase=1;chain_release_calls=chain_release_empty=0;memset(chain_release_hits,0,sizeof chain_release_hits);
   demand(BATTLE_AddExpItem(battle_at,chain_list)==0,"one unchanged uninterrupted AddExpItem call handles all four original-created drops");
   chain_release_phase=0;chain_rng_phase=0;
   demand(rng_count==(with_item?(branch?6:5):0)&&chain_rng_at==rng_count,"exact four recipient draws then coin and optional replacement draw");
   demand(chain_release_calls==with_item&&chain_release_empty==0,"exact single overflow release and no-item baseline");
   for(int k=0;k<4;k++)demand(chain_release_hits[k]==(with_item&&k+8==victim),"exact chain overflow victim");
   for(int k=0;k<10;k++)demand(slots[chain_actor].indexOfExistItems[CHAR_STARTITEMARRAY+k]==-1,"all original carried drop slots clear");
   if(!with_item){
    memcpy(chain_control_items,reward_items,sizeof chain_control_items);memcpy(chain_control_actors,slots,sizeof chain_control_actors);chain_control_arena=*arena;
    demand(!memcmp(chain_created_items,reward_items,sizeof chain_created_items)&&ITEM_COUNT==chain_after_create,"no-item original assignment preserves complete creation pool/count");
   }else{
    memcpy(chain_expected_items,chain_control_items,sizeof chain_expected_items);
    chain_expected_items[victim].use=0;chain_expected_items[victim].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]=-1;
    memcpy(chain_expected_actors,chain_control_actors,sizeof chain_expected_actors);chain_expected_arena=chain_control_arena;
    for(int k=0;k<3;k++)chain_expected_arena.Side[0].Entry[0].getitem[k]=pending[k];
    demand(!memcmp(chain_expected_items,reward_items,sizeof chain_expected_items)&&ITEM_COUNT==chain_after_create-1,"complete uninterrupted assignment 256 pool/count oracle");
    demand(!memcmp(chain_expected_actors,slots,sizeof chain_expected_actors),"all seven complete actors versus no-item original death/EXP control");
    demand(!memcmp(&chain_expected_arena,arena,sizeof chain_expected_arena),"full arena exact pending order versus original no-item control");
    for(int a=0;a<7;a++)for(int box=0;box<CHAR_MAXITEMHAVE;box++)demand(slots[a].indexOfExistItems[box]<8||slots[a].indexOfExistItems[box]>11,"all four created objects have no carried references after assignment");
    printf("REAL_HEADER_FOUR_DROP_ASSIGN|branch=%d|actor=6|indices=8,9,10,11|victim=%d|pending=%d,%d,%d|rng=%d|release_calls=1|count_delta=-1|recipient_draws=4|initial_pending=empty|calls=1|whole_items=1|whole_actors=1|whole_arena=1|carried_cleared=1|original_assignment=1|no_item_control=1|no_rebinding=1\n",branch,victim,pending[0],pending[1],pending[2],rng_count);
    PAYOUT
   }
  }
 }
 memcpy(reward_items,chain_saved_items,sizeof chain_saved_items);memcpy(slots,chain_saved_actors,sizeof chain_saved_actors);*arena=chain_saved_arena;
 ITEM_COUNT=chain_saved_count;ITEM_SIZE=chain_saved_size;rng_count=chain_saved_rng;rng_mode=chain_saved_mode;
 for(int i=0;i<10;i++){master[ENEMY_ITEM1+i]=chain_saved_ids[i];master[ENEMY_ITEMPROB1+i]=chain_saved_probs[i];}
 }
'''


def payout_controls(profile):
    c=prior.payout_controls(profile).replace('distinct_','chain_')
    c=c.replace('int index=4+k','int index=8+k').replace('k+4','k+8').replace('index>=4&&index<=7','index>=8&&index<=11').replace('references[index-4]','references[index-8]')
    c=c.replace('chain_winner==5','chain_winner==9').replace('chain_winner==7','chain_winner==11')
    c=c.replace('REAL_HEADER_OVERFLOW_PAYOUT','REAL_HEADER_FOUR_DROP_PAYOUT')
    return c


def controls(profile):
    c=item.substitutions(profile,CONTROL)
    c=c.replace('LEAK_EXPECTED','0' if profile=='bismarck' else '1').replace('ENTRY_FIELD','char_index' if profile=='bismarck' else 'charaindex').replace('TABLE_TYPE','ITEM_Index' if profile=='bismarck' else 'ITEM_table')
    c=c.replace('INDIRECT_SNAPSHOT','ITEM_Table chain_table_snapshot[3];memcpy(chain_table_snapshot,factory_table,sizeof chain_table_snapshot);' if profile=='bismarck' else '')
    c=c.replace('INDIRECT_ORACLE','demand(!memcmp(chain_table_snapshot,factory_table,sizeof chain_table_snapshot),"complete indirect factory table immutable");' if profile=='bismarck' else '')
    return c.replace('PAYOUT',payout_controls(profile))


def four_drop_native(profile,source,battle,event,root):
    n,lua=prior.overflow_native(profile,source,battle,event,root)
    n=replace_once(n,'#define rand overflow_rand\n','#define rand overflow_rand\n'+RNG)
    anchor='#define ITEM_endExistItemsOne(index) distinct_release_observer(index,__FILE__,__LINE__)\n'
    n=replace_once(n,anchor,anchor+OBSERVER)
    for name in ('CHAR_sendItemData','CHAR_sendItemDataOne','LogItem'):
        body=attack.definition(n,name);brace=body.index('{')
        if name=='LogItem':
            check=r'''
 if(reward_phase==5){
  int expected_id=(chain_winner==9||chain_winner==11)?2:1;
  const char *expected_name=expected_id==2?"FactoryTwo":"Factory";
  const char *expected_code=expected_id==2?"factory-two":"factory-bounded";
  demand(chain_winner>=8&&chain_winner<=11&&item==chain_winner&&id==expected_id&&!strcmp(itemname,expected_name)&&!strcmp(code,expected_code)&&name&&key&&!strcmp(cause,"BattleGet(战斗後所得的道具)")&&floor==slots[0].data[CHAR_FLOOR]&&x==slots[0].data[CHAR_X]&&y==slots[0].data[CHAR_Y],"typed four-drop chain pickup log identity");
  settle_log_count++;reward_log_count++;return;
 }
'''
        else:
            condition='count==1&&indices[0]==reward_expected_slot' if name=='CHAR_sendItemData' else 'slot==reward_expected_slot'
            count='reward_data_count' if name=='CHAR_sendItemData' else 'reward_one_count'
            check='\n if(reward_phase==5){demand(actor==0&&chain_winner>=8&&chain_winner<=11&&'+condition+'&&slots[0].indexOfExistItems[reward_expected_slot]==chain_winner,"typed four-drop chain inventory send");'+count+'++;return TRUE;}\n'
        n=replace_once(n,body,body[:brace+1]+check+body[brace+1:])
    old=prior.overflow_controls(profile)
    c=controls(profile).replace('reward_phase=4;','reward_phase=5;')
    n=replace_once(n,old,old+'\n'+c)
    paths={'char/enemy.c':('ENEMY_createEnemy',),'item/item.c':('ITEM_makeItem','ITEM_makeItemAndRegist','_ITEM_initExistItemsOne'),'battle/battle.c':('BATTLE_AddExpItem','BATTLE_ItemDelCheck')}
    for path,names in paths.items():
        original=attack.pp_file(profile,root,attack.LAYOUTS[profile]/path)
        for name in names:
            body=attack.definition(n,name)
            expected=attack.definition(source,name) if name=='ENEMY_createEnemy' else attack.definition(original,name)
            if body!=expected:raise ValueError('four-drop original body drift '+name)
            print(f'FOUR_DROP_SOURCE|{profile}|{name}|inherited_sha256={hashlib.sha256(body.encode()).hexdigest()}|preprocessed_sha256={hashlib.sha256(attack.definition(original,name).encode()).hexdigest()}',flush=True)
    return n,lua


def validate_report(report):
    prior.validate_report(report);created={};assignment={};payout={}
    for line in report.splitlines():
        if not line.startswith('ACTUAL|'):continue
        parts=line.split('|');profile=parts[1];marker=parts[2]
        if marker not in ('REAL_HEADER_FOUR_DROP_CREATE','REAL_HEADER_FOUR_DROP_ASSIGN','REAL_HEADER_FOUR_DROP_PAYOUT'):continue
        try:
            f=dict(p.split('=',1) for p in parts[3:])
            if profile not in ('gavin','bismarck'):raise ValueError('unknown four-drop profile')
            if marker.endswith('CREATE'):
                rows=created;key=profile
                expected=dict(actor=6,objects=4,templates=2,prob=1000,factory_draws=66,spawn_draws=282,count_delta=4,blockers=3,cleared_inactive_refs=54 if profile=='bismarck' else 24,pool_size=256,owner=6,object=-1,whole_items=1,whole_other_actors=1,whole_arena=1,tables_immutable=1,original_creation=1,no_rebinding=1,no_cursor_rewind=1)
                if f['indices']!='8,9,10,11' or f['ids']!='1,2,1,2' or int(f['blockers'])<1 or int(f['cleared_inactive_refs'])<1:raise ValueError('missing exact original-created object/template identities or explicit blockers')
            else:
                b=int(f['branch']);victim=7+b if b else 11
                if b not in range(4) or f['pending']!=','.join(map(str,PATTERNS[b])):raise ValueError('unknown four-drop branch or wrong pending order')
                if marker.endswith('ASSIGN'):
                    rows=assignment;key=profile,b
                    expected=dict(actor=6,victim=victim,rng=6 if b else 5,release_calls=1,count_delta=-1,recipient_draws=4,calls=1,whole_items=1,whole_actors=1,whole_arena=1,carried_cleared=1,original_assignment=1,no_item_control=1,no_rebinding=1)
                    if f['indices']!='8,9,10,11' or f['initial_pending']!='empty':raise ValueError('missing original initial assignment identity')
                else:
                    a=int(f['available']);rows=payout;key=profile,b,a
                    if a not in (0,1):raise ValueError('unknown four-drop payout capacity')
                    w=PATTERNS[b][0] if a else -1;baseline=84 if profile=='bismarck' else 54
                    expected=dict(victim=victim,winner=w,count_delta=a-3,logs=a,data=a,one=a if profile=='bismarck' else 0,release_calls=baseline+3-a,baseline_release=baseline)
                    for i in range(8,12):expected.update({f'live{i}':int(i==w),f'owner{i}':0 if i==w else -1,f'ref{i}':int(i==w),f'release{i}':int(i!=victim and i!=w)})
                    for field in ('rs','packet_oracle','second_loop','arena_released','tickets_cleared','whole_items','whole_fillers','whole_actors','whole_arena','whole_connections','original_timer'):expected[field]=1
            if key in rows or any(int(f[k])!=v for k,v in expected.items()):raise ValueError('four-drop state/creation/RNG/release/presentation mismatch or duplicate')
            rows[key]=f
        except (KeyError,TypeError) as exc:raise ValueError('incomplete four-drop witness') from exc
    if set(created)!={'gavin','bismarck'} or set(assignment)!={(p,b) for p in ('gavin','bismarck') for b in range(4)} or set(payout)!={(p,b,a) for p in ('gavin','bismarck') for b in range(4) for a in (0,1)}:raise ValueError('missing creation/assignment/payout branch/capacity')
    if 'RESOLUTION|ORIGINAL_REAL_HEADER_FOUR_DROP_CHAIN_BOUNDED_PASS' not in report.splitlines():raise ValueError('missing four-drop resolution')
    return created,assignment,payout


def main():
    soft,hard=resource.getrlimit(resource.RLIMIT_STACK)
    if soft!=resource.RLIM_INFINITY and soft<64*1024*1024:resource.setrlimit(resource.RLIMIT_STACK,(64*1024*1024,hard))
    markers=tuple('REAL_HEADER_'+s+'|' for s in ('FINISH_DISPATCH','SAME_ITEM_CAPACITY','TICKET_CLEANUP','RECIPIENT_SIDE','INVALID_ITEM_TICKET','MIXED_ITEM_TICKET','LAST_SLOT_TICKET','DISTINCT_DROP_CREATE','DISTINCT_ITEM_TICKET','OVERFLOW_ASSIGN','OVERFLOW_PAYOUT','FOUR_DROP_CREATE','FOUR_DROP_ASSIGN','FOUR_DROP_PAYOUT'))
    attack.main(native_builder=four_drop_native,extra_markers=markers)
    print('BOUNDARY|synthetic ten-pair master with four guaranteed entries, allocator occupancy blockers/logical256 pool, controlled raw assignment draws and bags; all four objects/owners/carried slots created by one original ENEMY_createEnemy, one uninterrupted AddExpItem; no natural recovered probabilities, early identity, real-client or modern DESIGN')
    for s in ('SAME_ITEM_CAPACITY','TICKET_CLEANUP','RECIPIENT_SIDE','INVALID_ITEM_TICKET','MIXED_ITEM_TICKET','LAST_SLOT_TICKET','DISTINCT_ITEM_TICKET','OVERFLOW_TICKET','FOUR_DROP_CHAIN'):print('RESOLUTION|ORIGINAL_REAL_HEADER_'+s+'_BOUNDED_PASS')

if __name__=='__main__':main()
