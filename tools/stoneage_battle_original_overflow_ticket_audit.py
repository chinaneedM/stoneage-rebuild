"""Bounded original fourth factory object: rejection and three replacement slots."""
import hashlib
import resource
from tools import stoneage_battle_original_distinct_item_ticket_audit as prior
attack=prior.attack
item=prior.item
replace_once=prior.replace_once
PATTERNS=((4,5,6),(7,5,6),(4,7,6),(4,5,7))

RNG=r'''
static void demand(int truth,const char *name);
static int overflow_rng_phase,overflow_rng_case,overflow_rng_at;
static int overflow_rand(void){
 if(!overflow_rng_phase)return audit_rand();
 int at=overflow_rng_at++;rng_count++;
 demand(at<3,"bounded fourth ticket random draw count");
 if(at==0)return 0;
 if(at==1)return overflow_rng_case?2147483647:0;
 int values[3]={0,1073741824,2147483647};return values[overflow_rng_case-1];
}
#undef rand
#define rand overflow_rand
'''

CONTROL=r'''
 {
 static ITEM_TYPE overflow_input[256],overflow_expected[256],overflow_control[256];
 static Char overflow_actors[7],overflow_actor_control[7],overflow_actor_expected[7];
 BATTLE overflow_arena=*arena,overflow_arena_control,overflow_arena_expected;
 int overflow_count=ITEM_COUNT,overflow_rng_saved=rng_count,overflow_mode_saved=rng_mode;
 memcpy(overflow_input,reward_items,sizeof overflow_input);
 memcpy(overflow_actors,slots,sizeof overflow_actors);
 rng_count=0;rng_mode=0;
 int fourth=ITEM_makeItemAndRegist(2);
 demand(fourth==7&&rng_count==66,"fourth distinct original factory object and unchanged allocator cursor");
 ITEM_Item overflow_template=distinct_template;overflow_template.data[ITEM_LEAKLEVEL]=LEAK_EXPECTED;
 overflow_input[7].use=1;overflow_input[7].ITEM_FIELD=overflow_template;
 demand(!memcmp(overflow_input,reward_items,sizeof overflow_input)&&ITEM_COUNT==overflow_count+1,"fourth factory complete pool/count oracle");
 demand(!memcmp(overflow_actors,slots,sizeof overflow_actors)&&!memcmp(&overflow_arena,arena,sizeof overflow_arena),"fourth factory preserves complete actors/arena");
 demand(!memcmp(distinct_index_snapshot,allocator_table,sizeof distinct_index_snapshot),"fourth factory preserves complete index table");
 INDIRECT_ORACLE
 /* Explicit ownership binding to the preceding original-created enemy, not a new natural master claim. */
 reward_items[7].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]=distinct_actor;
 memcpy(overflow_input,reward_items,sizeof overflow_input);
 int overflow_after_factory=ITEM_COUNT;
 for(int branch=0;branch<4;branch++){
  int victim=branch?3+branch:7;
  int pending[3]={4,5,6};if(branch)pending[branch-1]=7;
  for(int with_item=0;with_item<2;with_item++){
   memcpy(reward_items,overflow_input,sizeof overflow_input);memcpy(slots,overflow_actors,sizeof overflow_actors);
   *arena=overflow_arena;ITEM_COUNT=overflow_after_factory;
   CHAR_setFlg(distinct_actor,CHAR_ISDIE,FALSE);slots[distinct_actor].data[CHAR_HP]=0;
   slots[distinct_actor].indexOfExistItems[CHAR_STARTITEMARRAY]=with_item?7:-1;
   overflow_rng_phase=1;overflow_rng_case=branch;overflow_rng_at=0;rng_count=0;
   distinct_release_phase=1;distinct_release_calls=distinct_release_empty=0;memset(distinct_release_hits,0,sizeof distinct_release_hits);
   demand(BATTLE_AddExpItem(battle_at,distinct_list)==0,"unchanged original fourth ticket assignment");
   distinct_release_phase=0;overflow_rng_phase=0;
   demand(rng_count==(with_item?(branch?3:2):0)&&overflow_rng_at==rng_count,"exact recipient/coin/replacement original RNG draws");
   demand(distinct_release_calls==with_item&&distinct_release_empty==0,"exact single overflow release versus no-item control");
   for(int k=0;k<4;k++)demand(distinct_release_hits[k]==(with_item&&k+4==victim),"exact overflow victim release");
   if(!with_item){
    memcpy(overflow_control,reward_items,sizeof overflow_control);memcpy(overflow_actor_control,slots,sizeof overflow_actor_control);
    overflow_arena_control=*arena;
    demand(!memcmp(overflow_input,reward_items,sizeof overflow_input)&&ITEM_COUNT==overflow_after_factory,"no-item assignment control pool/count immutable");
   }else{
    memcpy(overflow_expected,overflow_control,sizeof overflow_expected);
    overflow_expected[victim].use=0;overflow_expected[victim].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]=-1;
    memcpy(overflow_actor_expected,overflow_actor_control,sizeof overflow_actor_expected);
    overflow_arena_expected=overflow_arena_control;
    for(int k=0;k<3;k++)overflow_arena_expected.Side[0].Entry[0].getitem[k]=pending[k];
    demand(!memcmp(overflow_expected,reward_items,sizeof overflow_expected)&&ITEM_COUNT==overflow_after_factory-1,"complete overflow 256 item/count oracle");
    demand(!memcmp(overflow_actor_expected,slots,sizeof overflow_actor_expected),"all seven complete overflow actors versus original no-item death/EXP control");
    demand(!memcmp(&overflow_arena_expected,arena,sizeof overflow_arena_expected),"entire overflow arena versus no-item control");
    for(int a=0;a<7;a++)for(int box=0;box<CHAR_MAXITEMHAVE;box++)demand(slots[a].indexOfExistItems[box]!=victim&&slots[a].indexOfExistItems[box]!=7,"overflow carried slots cleared and released victim unreferenced");
    printf("REAL_HEADER_OVERFLOW_ASSIGN|branch=%d|factory=7|factory_id=2|factory_draws=66|binding=explicit|victim=%d|pending=%d,%d,%d|rng=%d|release_calls=1|count_delta=-1|whole_items=1|whole_actors=1|whole_arena=1|tables_immutable=1|carried_cleared=1|original_factory=1|original_assignment=1|no_item_control=1\n",branch,victim,pending[0],pending[1],pending[2],rng_count);
    PAYOUT
   }
  }
 }
 memcpy(reward_items,distinct_created_items,sizeof distinct_created_items);
 memcpy(slots,distinct_created_actors,sizeof distinct_created_actors);*arena=overflow_arena;
 ITEM_COUNT=overflow_count;rng_count=overflow_rng_saved;rng_mode=overflow_mode_saved;
 }
'''


def payout_controls(profile):
    c=prior.competition_controls(profile)
    a=c.index(' int permutations[6][3]');z=c.index('  int recipient=0;',a)
    c=c[:a]+" for(int available=0;available<2;available++){\n  int *pattern=pending,first_valid=0,awards=available;distinct_winner=available?pending[0]:-1;\n"+c[z:]
    c=replace_once(c,'\n }\n }\n memcpy(reward_items,distinct_saved_items','\n }\n memcpy(reward_items,distinct_saved_items')
    c=replace_once(c,'for(int k=0;k<3;k++)demand(distinct_release_hits[k]==(with_ticket&&(!available||k+4!=distinct_winner)?1:0)', 'for(int k=0;k<4;k++)demand(distinct_release_hits[k]==(with_ticket&&k+4!=victim&&(!available||k+4!=distinct_winner)?1:0)')
    c=replace_once(c,'    for(int k=0;k<3;k++){\n     int index=4+k;','    for(int k=0;k<4;k++){\n     int index=4+k;if(index==victim)continue;')
    c=replace_once(c,'int references[3]={0,0,0};','int references[4]={0,0,0,0};')
    c=replace_once(c,'if(index>=4&&index<=6)references[index-4]++;','if(index>=4&&index<=7)references[index-4]++;')
    c=replace_once(c,'for(int k=0;k<3;k++)demand(references[k]','for(int k=0;k<4;k++)demand(references[k]')
    c=c.replace('distinct_winner==5?', '(distinct_winner==5||distinct_winner==7)?')
    a=c.index('    printf("REAL_HEADER_DISTINCT_ITEM_TICKET|');z=c.index('   }\n   reward_phase=0;',a)
    c=c[:a]+item.substitutions(profile,r'''    printf("REAL_HEADER_OVERFLOW_PAYOUT|branch=%d|available=%d|pending=%d,%d,%d|victim=%d|winner=%d|count_delta=%d|logs=%d|data=%d|one=%d|release_calls=%d|baseline_release=%d|rs=1|packet_oracle=1|second_loop=1|arena_released=1|tickets_cleared=1|whole_items=1|whole_fillers=1|whole_actors=1|whole_arena=1|whole_connections=1|original_timer=1",
     branch,available,pending[0],pending[1],pending[2],victim,distinct_winner,ITEM_COUNT-input_count,reward_log_count,reward_data_count,reward_one_count,distinct_release_calls,distinct_baseline_release);
    for(int k=0;k<4;k++)printf("|live%d=%d|owner%d=%d|ref%d=%d|release%d=%d",k+4,reward_items[k+4].use,k+4,reward_items[k+4].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX],k+4,references[k],k+4,distinct_release_hits[k]);
    printf("\n");
''')+c[z:]
    return '{\n'+c+'\n}'


def overflow_controls(profile):
    c=item.substitutions(profile,CONTROL)
    c=c.replace('LEAK_EXPECTED','0' if profile=='bismarck' else '1').replace('INDIRECT_ORACLE','demand(!memcmp(distinct_table_snapshot,factory_table,sizeof distinct_table_snapshot),"fourth factory indirect table immutable");' if profile=='bismarck' else '')
    return c.replace('PAYOUT',payout_controls(profile))


def overflow_native(profile,source,battle,event,root):
    n,lua=prior.distinct_native(profile,source,battle,event,root)
    observer=prior.OBSERVER.replace('distinct_release_hits[3]','distinct_release_hits[4]').replace('index<=6','index<=7')
    n=replace_once(n,prior.OBSERVER,observer)
    anchor='#define rand audit_rand\n'
    n=replace_once(n,anchor,anchor+RNG)
    for name in ('CHAR_sendItemData','CHAR_sendItemDataOne','LogItem'):
        body=attack.definition(n,name)
        n=replace_once(n,body,body.replace('distinct_winner==5?', '(distinct_winner==5||distinct_winner==7)?'))
    create,restore=prior.create_controls(profile)
    n=replace_once(n,create+'\n'+prior.competition_controls(profile)+'\n'+restore,create+'\n'+prior.competition_controls(profile)+'\n'+overflow_controls(profile)+'\n'+restore)
    original=attack.pp_file(profile,root,attack.LAYOUTS[profile]/'battle/battle.c')
    for name in ('BATTLE_AddExpItem','BATTLE_ItemDelCheck'):
        body=attack.definition(n,name)
        if body!=attack.definition(original,name):raise ValueError('overflow original body drift '+name)
        print(f'OVERFLOW_SOURCE|{profile}|{name}|sha256={hashlib.sha256(body.encode()).hexdigest()}',flush=True)
    return n,lua


def validate_report(report):
    prior.validate_report(report);assignment={};payout={}
    for line in report.splitlines():
        if not line.startswith('ACTUAL|'):continue
        parts=line.split('|');profile=parts[1];marker=parts[2]
        if marker not in ('REAL_HEADER_OVERFLOW_ASSIGN','REAL_HEADER_OVERFLOW_PAYOUT'):continue
        try:
            f=dict(p.split('=',1) for p in parts[3:]);b=int(f['branch']);victim=3+b if b else 7
            if profile not in ('gavin','bismarck') or b not in range(4):raise ValueError('unknown overflow profile/branch')
            if f['pending']!=','.join(map(str,PATTERNS[b])):raise ValueError('incorrect overflow pending order')
            if marker.endswith('ASSIGN'):
                key=profile,b;rows=assignment
                expected=dict(factory=7,factory_id=2,factory_draws=66,victim=victim,rng=3 if b else 2,release_calls=1,count_delta=-1,whole_items=1,whole_actors=1,whole_arena=1,tables_immutable=1,carried_cleared=1,original_factory=1,original_assignment=1,no_item_control=1)
                if f['binding']!='explicit':raise ValueError('missing synthetic binding boundary')
            else:
                a=int(f['available']);key=profile,b,a;rows=payout
                if a not in (0,1):raise ValueError('unknown payout capacity')
                w=PATTERNS[b][0] if a else -1;baseline=84 if profile=='bismarck' else 54
                expected=dict(victim=victim,winner=w,count_delta=a-3,logs=a,data=a,one=a if profile=='bismarck' else 0,release_calls=baseline+3-a,baseline_release=baseline)
                for i in range(4,8):expected.update({f'live{i}':int(i==w),f'owner{i}':0 if i==w else -1,f'ref{i}':int(i==w),f'release{i}':int(i!=victim and i!=w)})
                for n in ('rs','packet_oracle','second_loop','arena_released','tickets_cleared','whole_items','whole_fillers','whole_actors','whole_arena','whole_connections','original_timer'):expected[n]=1
            if key in rows or any(int(f[n])!=v for n,v in expected.items()):raise ValueError('overflow state/release/presentation mismatch or duplicate')
            rows[key]=f
        except (KeyError,TypeError) as exc:raise ValueError('incomplete overflow witness') from exc
    if set(assignment)!={(p,b) for p in ('gavin','bismarck') for b in range(4)} or set(payout)!={(p,b,a) for p in ('gavin','bismarck') for b in range(4) for a in (0,1)}:raise ValueError('missing overflow assignment or payout')
    if 'RESOLUTION|ORIGINAL_REAL_HEADER_OVERFLOW_TICKET_BOUNDED_PASS' not in report.splitlines():raise ValueError('missing overflow resolution')
    return assignment,payout


def main():
    soft,hard=resource.getrlimit(resource.RLIMIT_STACK)
    if soft!=resource.RLIM_INFINITY and soft<64*1024*1024:resource.setrlimit(resource.RLIMIT_STACK,(64*1024*1024,hard))
    markers=tuple('REAL_HEADER_'+s+'|' for s in ('FINISH_DISPATCH','SAME_ITEM_CAPACITY','TICKET_CLEANUP','RECIPIENT_SIDE','INVALID_ITEM_TICKET','MIXED_ITEM_TICKET','LAST_SLOT_TICKET','DISTINCT_DROP_CREATE','DISTINCT_ITEM_TICKET','OVERFLOW_ASSIGN','OVERFLOW_PAYOUT'))
    attack.main(native_builder=overflow_native,extra_markers=markers)
    print('BOUNDARY|fourth original factory object with explicit enemy ownership/carried binding, controlled raw RAND branch draws, synthetic full/one-free bags; no natural fourth-drop master, early identity, real-client or modern DESIGN')
    for s in ('SAME_ITEM_CAPACITY','TICKET_CLEANUP','RECIPIENT_SIDE','INVALID_ITEM_TICKET','MIXED_ITEM_TICKET','LAST_SLOT_TICKET','DISTINCT_ITEM_TICKET','OVERFLOW_TICKET'):print('RESOLUTION|ORIGINAL_REAL_HEADER_'+s+'_BOUNDED_PASS')

if __name__=='__main__':main()
