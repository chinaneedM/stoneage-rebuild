"""Original four-drop assignment to two PLAYER entries and independent payout."""
import hashlib
import resource
from tools import stoneage_battle_original_four_drop_chain_audit as prior
attack=prior.attack
item=prior.item
replace_once=prior.replace_once
MASKS=tuple(range(1,15))

RNG=r'''
static int split_rng_phase,split_rng_mask,split_rng_at;
static int split_rand(void){
 if(!split_rng_phase)return chain_rand();
 int at=split_rng_at++;rng_count++;
 demand(at<4,"two eligible recipients consume exactly four original draws");
 return (split_rng_mask&(1<<at))?2147483647:0;
}
#undef rand
#define rand split_rand
'''

OBSERVE=r'''
static int split_release_phase,split_release_calls,split_release_empty,split_release_hits[4];
static int split_winners[2],split_slots[2],split_logs[2],split_data[2],split_one[2];
static void split_release_observer(int index,char *file,int line){
 if(split_release_phase){split_release_calls++;if(index==-1)split_release_empty++;else {demand(index>=8&&index<=11,"only four original split objects released");split_release_hits[index-8]++;}}
 chain_release_observer(index,file,line);
}
#undef ITEM_endExistItemsOne
#define ITEM_endExistItemsOne(index) split_release_observer(index,__FILE__,__LINE__)
'''

CONTROL=r'''
 {
 static ITEM_TYPE split_saved_items[256],split_assigned_items[256],split_expected_items[256],split_bag_items[256];
 static Char split_saved_actors[7],split_assigned_actors[7],split_expected_actors[7];
 BATTLE split_saved_arena=*arena,split_assignment_input=chain_input_arena,split_assigned_arena,split_expected_arena;
 int split_saved_count=ITEM_COUNT,split_saved_rng=rng_count,split_saved_mode=rng_mode;
 int split_saved_total=Total_BattleNum,split_saved_reward=reward_phase,split_saved_transport=finish_transport_phase;
 int split_saved_log=reward_log_count,split_saved_data=reward_data_count,split_saved_one=reward_one_count,split_saved_settle=settle_log_count;
 memcpy(split_saved_items,reward_items,sizeof split_saved_items);memcpy(split_saved_actors,slots,sizeof split_saved_actors);
 split_assignment_input.Side[0].Entry[1].ENTRY_FIELD=1;
 int split_list[3]={0,1,-1};
 for(int mask=1;mask<15;mask++){
  int pending_two[2][3]={{-1,-1,-1},{-1,-1,-1}},sizes[2]={0,0};
  for(int k=0;k<4;k++){int recipient=(mask>>k)&1;pending_two[recipient][sizes[recipient]++]=8+k;}
  demand(sizes[0]>=1&&sizes[0]<=3&&sizes[1]>=1&&sizes[1]<=3,"all fourteen distributed four-drop orders avoid per-recipient overflow");
  for(int with_item=0;with_item<2;with_item++){
   memcpy(reward_items,chain_created_items,sizeof chain_created_items);memcpy(slots,chain_created_actors,sizeof chain_created_actors);
   *arena=split_assignment_input;ITEM_COUNT=chain_after_create;
   CHAR_setFlg(chain_actor,CHAR_ISDIE,FALSE);slots[chain_actor].data[CHAR_HP]=0;
   if(!with_item)for(int k=0;k<4;k++)slots[chain_actor].indexOfExistItems[CHAR_STARTITEMARRAY+k]=-1;
   split_rng_phase=1;split_rng_mask=mask;split_rng_at=0;rng_count=0;
   split_release_phase=1;split_release_calls=split_release_empty=0;memset(split_release_hits,0,sizeof split_release_hits);
   demand(BATTLE_AddExpItem(battle_at,split_list)==0,"one original AddExpItem uses actual eligible PLAYER entries zero and one");
   split_release_phase=0;split_rng_phase=0;
   demand(rng_count==(with_item?4:0)&&split_rng_at==rng_count,"exact distributed recipient RNG stream without overflow draws");
   demand(!split_release_calls&&!split_release_empty,"distributed original assignment releases no object");
   demand(!memcmp(chain_created_items,reward_items,sizeof chain_created_items)&&ITEM_COUNT==chain_after_create,"assignment preserves all256 original records/count and original enemy ownership");
   for(int k=0;k<10;k++)demand(slots[chain_actor].indexOfExistItems[CHAR_STARTITEMARRAY+k]==-1,"all ten original carried master slots clear");
   if(!with_item){
    memcpy(split_expected_actors,slots,sizeof split_expected_actors);split_expected_arena=*arena;
   }else{
    for(int a=0;a<2;a++)for(int k=0;k<3;k++)split_expected_arena.Side[0].Entry[a].getitem[k]=pending_two[a][k];
    demand(!memcmp(split_expected_actors,slots,sizeof split_expected_actors),"all seven original actors match no-item death/EXP control");
    demand(!memcmp(&split_expected_arena,arena,sizeof split_expected_arena),"whole arena matches exact independent recipient pending order");
    for(int a=0;a<7;a++)for(int box=0;box<CHAR_MAXITEMHAVE;box++)demand(slots[a].indexOfExistItems[box]<8||slots[a].indexOfExistItems[box]>11,"no original-created object remains carried after assignment");
    printf("REAL_HEADER_TWO_PLAYER_ASSIGN|mask=%d|eligible=0,1,-1|pending0=%d,%d,%d|pending1=%d,%d,%d|size0=%d|size1=%d|rng=4|calls=1|release_calls=0|count_delta=0|initial_pending=empty|whole_items=1|whole_actors=1|whole_arena=1|carried_cleared=1|no_item_control=1|original_assignment=1|no_rebinding=1\n",mask,pending_two[0][0],pending_two[0][1],pending_two[0][2],pending_two[1][0],pending_two[1][1],pending_two[1][2],sizes[0],sizes[1]);
    memcpy(split_assigned_items,reward_items,sizeof split_assigned_items);memcpy(split_assigned_actors,slots,sizeof split_assigned_actors);split_assigned_arena=*arena;
    for(int capacity=0;capacity<4;capacity++){
     int available[2]={capacity&1,(capacity>>1)&1},awards=available[0]+available[1];
     int input_count=0,expected_count=0,baseline_release=0;char baseline_rs[2][1024];
     for(int a=0;a<2;a++)split_winners[a]=available[a]?pending_two[a][0]:-1;
     for(int with_ticket=0;with_ticket<2;with_ticket++){
      memcpy(reward_items,split_assigned_items,sizeof split_assigned_items);memcpy(slots,split_assigned_actors,sizeof split_assigned_actors);*arena=split_assigned_arena;ITEM_COUNT=chain_after_create;
      int active_limit=ACTIVE_LIMIT;
      for(int a=0;a<2;a++){
       demand(CHAR_getInt(a,CHAR_WHICHTYPE)==CHAR_TYPEPLAYER,"two actual eligible original PLAYER actors");
       for(int box=CHAR_STARTITEMARRAY;box<CHAR_MAXITEMHAVE;box++)slots[a].indexOfExistItems[box]=-1;
       for(int box=CHAR_STARTITEMARRAY;box<active_limit;box++){
        if(available[a]&&box==active_limit-1)continue;
        int filler=80+a*60+box;demand(filler<249&&!reward_items[filler].use,"distinct synthetic filler for each player bag");
        reward_items[filler].use=1;reward_items[filler].ITEM_FIELD.data[ITEM_ID]=1800+filler;
        reward_items[filler].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]=a;reward_items[filler].ITEM_FIELD.workint[ITEM_WORKOBJINDEX]=-1;
        slots[a].indexOfExistItems[box]=filler;ITEM_COUNT++;
       }
       split_slots[a]=CHAR_findEmptyItemBox(a);demand(split_slots[a]==(available[a]?active_limit-1:-1),"independent exact full/last-slot bag capacity");
       slots[a].data[CHAR_LV]=100;slots[a].data[CHAR_EXP]=0;
       slots[a].workint[CHAR_WORKGETEXP]=0;CHAR_setFlg(a,CHAR_ISDIE,FALSE);
       slots[a].workint[CHAR_WORKFD]=7-a;
       slots[a].workint[CHAR_WORKBATTLEINDEX]=battle_at;slots[a].workint[CHAR_WORKBATTLEMODE]=BATTLE_CHARMODE_C_WAIT;
       if(!with_ticket)for(int k=0;k<3;k++)arena->Side[0].Entry[a].getitem[k]=-1;
      }
      slots[2].workint[CHAR_WORKGETEXP]=0;
      slots[chain_actor].workint[CHAR_WORKBATTLEINDEX]=battle_at;slots[chain_actor].workint[CHAR_WORKBATTLEMODE]=BATTLE_CHARMODE_C_WAIT;
      arena->use=1;arena->mode=BATTLE_MODE_FINISH;arena->type=BATTLE_TYPE_P_vs_E;arena->winside=0;arena->CreateTime=900;arena->flgTime=0;
      memcpy(split_bag_items,reward_items,sizeof split_bag_items);input_count=ITEM_COUNT;
      memset(cleanup_connections,0,sizeof cleanup_connections);cleanup_timer_calls=cleanup_timer_draws=cleanup_nu_sends=0;cleanup_timer_phase=1;
      Total_BattleNum=1;reward_phase=6;split_transport_phase=1;finish_transport_phase=1;
      reward_log_count=reward_data_count=reward_one_count=settle_log_count=0;
      memset(split_logs,0,sizeof split_logs);memset(split_data,0,sizeof split_data);memset(split_one,0,sizeof split_one);
      finish_rs_count=finish_status_count=0;
      split_release_phase=1;split_release_calls=split_release_empty=0;memset(split_release_hits,0,sizeof split_release_hits);
      int ret=BATTLE_Loop();split_release_phase=0;
      demand(ret==1&&!arena->use&&arena->mode==BATTLE_MODE_NONE&&Total_BattleNum==0,"unchanged original Finish/Exit/DeleteBattle completes both player recipients");
      if(!with_ticket)baseline_release=split_release_empty;
      demand(split_release_empty==baseline_release&&split_release_calls==baseline_release+(with_ticket?4-awards:0),"exact original release total versus no-ticket teardown");
      for(int k=0;k<4;k++)demand(split_release_hits[k]==(with_ticket&&8+k!=split_winners[0]&&8+k!=split_winners[1]),"each split object awarded or released exactly once");
      CONNECTION_TYPE expected_connections[8];memset(expected_connections,0,sizeof expected_connections);
      expected_connections[6].BDTime=expected_connections[7].BDTime=TIMER_VALUE;
      demand(!memcmp(expected_connections,cleanup_connections,sizeof expected_connections)&&cleanup_timer_calls==2&&cleanup_timer_draws==2&&cleanup_nu_sends==NU_COUNT,"whole eight native connections and two exact original timer calls");
      for(int s=0;s<2;s++)for(int e=0;e<BATTLE_ENTRY_MAX;e++)for(int k=0;k<3;k++)demand(arena->Side[s].Entry[e].getitem[k]==-1,"whole original arena pending tickets cleared");
      demand(finish_rs_count==2&&finish_rs_fd[0]==7&&finish_rs_fd[1]==6,"original active-profile ascending entry payout order with explicit separate descriptor collectors");
      if(!with_ticket){
       memcpy(split_expected_items,reward_items,sizeof split_expected_items);memcpy(split_expected_actors,slots,sizeof split_expected_actors);split_expected_arena=*arena;expected_count=ITEM_COUNT;
       demand(!memcmp(split_bag_items,reward_items,sizeof split_bag_items)&&ITEM_COUNT==input_count,"no-ticket whole pool/count unchanged");
       for(int a=0;a<2;a++){
        const char *packet=finish_rs_text[a];int len=strlen(packet);demand(len>=3&&!strcmp(packet+len-3,"|||"),"each original no-ticket RS has exact empty suffix");strcpy(baseline_rs[a],packet);baseline_rs[a][len-3]=0;
       }
      }else{
       for(int k=0;k<4;k++){
        int index=8+k,owner=index==split_winners[0]?0:(index==split_winners[1]?1:-1);
        if(owner>=0){split_expected_items[index].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]=owner;split_expected_items[index].ITEM_FIELD.workint[ITEM_WORKOBJINDEX]=-1;split_expected_actors[owner].indexOfExistItems[split_slots[owner]]=index;}
        else{split_expected_items[index].use=0;split_expected_items[index].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]=-1;expected_count--;}
       }
       demand(!memcmp(split_expected_items,reward_items,sizeof split_expected_items)&&ITEM_COUNT==expected_count,"all256 original items and both filler bags exact payout/count oracle");
       demand(!memcmp(split_expected_actors,slots,sizeof split_expected_actors)&&!memcmp(&split_expected_arena,arena,sizeof split_expected_arena),"all seven original actors/full arena exact no-ticket differential payout oracle");
       if(reward_log_count!=awards||settle_log_count!=awards||reward_data_count!=awards||reward_one_count!=SPLIT_TOTAL_SINGLE_SEND)fprintf(stderr,"TRACE|SPLIT_COUNTS|mask=%d|cap=%d|awards=%d|log=%d|settle=%d|data=%d|one=%d\n",mask,capacity,awards,reward_log_count,settle_log_count,reward_data_count,reward_one_count);
       demand(reward_log_count==awards&&settle_log_count==awards&&reward_data_count==awards&&reward_one_count==SPLIT_TOTAL_SINGLE_SEND,"exact combined typed original logs/item sends");
       for(int a=0;a<2;a++){
        demand(split_logs[a]==available[a]&&split_data[a]==available[a]&&split_one[a]==ONE_PER_PLAYER,"exact separate player typed log and inventory counts");
        char packet[1024];strcpy(packet,baseline_rs[a]);
        for(int k=0;k<3;k++){if(available[a]&&k==0)strcat(packet,DISPLAY_NAME);strcat(packet,"|");}
        demand(!strcmp(packet,finish_rs_text[a]),"each original RS complete control prefix and exact assigned-order suffix");
       }
       int references[4]={0,0,0,0};
       for(int a=0;a<7;a++)for(int box=0;box<CHAR_MAXITEMHAVE;box++){int index=slots[a].indexOfExistItems[box];if(index>=8&&index<=11)references[index-8]++;}
       for(int k=0;k<4;k++)demand(references[k]==(8+k==split_winners[0]||8+k==split_winners[1]),"all split item references counted across seven complete bags");
       printf("REAL_HEADER_TWO_PLAYER_PAYOUT|mask=%d|capacity=%d|winner0=%d|winner1=%d|bag0=%d|bag1=%d|active_limit=%d|awards=%d|count_delta=%d|logs0=%d|logs1=%d|data0=%d|data1=%d|one0=%d|one1=%d|release_calls=%d|baseline_release=%d|rs_count=2|fd_order=7,6|timer_calls=2|timer_draws=2|nu=%d|timer_value=%d|whole_items=1|whole_fillers=1|whole_actors=1|whole_arena=1|whole_connections=1|packet_oracle=1|tickets_cleared=1|arena_released=1|no_ticket_control=1|original_payout=1",mask,capacity,split_winners[0],split_winners[1],split_slots[0],split_slots[1],active_limit,awards,ITEM_COUNT-input_count,split_logs[0],split_logs[1],split_data[0],split_data[1],split_one[0],split_one[1],split_release_calls,baseline_release,cleanup_nu_sends,TIMER_VALUE);
       for(int k=0;k<4;k++)printf("|live%d=%d|owner%d=%d|ref%d=%d|release%d=%d",8+k,reward_items[8+k].use,8+k,reward_items[8+k].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX],8+k,references[k],8+k,split_release_hits[k]);
       printf("\n");
      }
      reward_phase=0;split_transport_phase=0;finish_transport_phase=0;cleanup_timer_phase=0;
     }
    }
   }
  }
 }
 memcpy(reward_items,split_saved_items,sizeof split_saved_items);memcpy(slots,split_saved_actors,sizeof split_saved_actors);*arena=split_saved_arena;
 ITEM_COUNT=split_saved_count;rng_count=split_saved_rng;rng_mode=split_saved_mode;Total_BattleNum=split_saved_total;
 reward_phase=split_saved_reward;finish_transport_phase=split_saved_transport;reward_log_count=split_saved_log;reward_data_count=split_saved_data;reward_one_count=split_saved_one;settle_log_count=split_saved_settle;
 }
'''


def controls(profile):
    c=item.substitutions(profile,CONTROL)
    b=profile=='bismarck'
    replacements={'ENTRY_FIELD':'char_index' if b else 'charaindex','ACTIVE_LIMIT':'54' if b else 'CHAR_MAXITEMHAVE','CONNECTION_TYPE':'GmsvSession' if b else 'CONNECT','TIMER_VALUE':'1005' if b else '1000','NU_COUNT':'2' if b else '0','SPLIT_TOTAL_SINGLE_SEND':'awards' if b else '0','ONE_PER_PLAYER':'available[a]' if b else '0','DISPLAY_NAME':'(split_winners[a]==9||split_winners[a]==11)?"FactoryTwo":"Factory"' if b else '""'}
    for key,value in replacements.items():c=c.replace(key,value)
    return c


def split_native(profile,source,battle,event,root):
    n,lua=prior.four_drop_native(profile,source,battle,event,root)
    n='static int split_transport_phase;\n'+n
    n=replace_once(n,'#define rand chain_rand\n','#define rand chain_rand\n'+RNG)
    anchor='#define ITEM_endExistItemsOne(index) chain_release_observer(index,__FILE__,__LINE__)\n'
    n=replace_once(n,anchor,anchor+OBSERVE)
    for name in ('getfdFromCharaIndex','CONNECT_checkfd','GmsvServer_NU_send','lssproto_NU_send'):
        try:body=attack.definition(n,name)
        except ValueError:continue
        brace=body.index('{')
        if name=='getfdFromCharaIndex':check='if(split_transport_phase){demand(actor==0||actor==1,"explicit split descriptor actor");return 7-actor;}'
        elif name=='CONNECT_checkfd':check='if(split_transport_phase){demand(fd==6||fd==7,"explicit split descriptor validity collector");return 1;}'
        else:check='if(split_transport_phase){demand((fd==6||fd==7)&&value=='+('0' if profile=='bismarck' else '-12')+',"typed split timer notification");cleanup_nu_sends++;return;}'
        n=replace_once(n,body,body[:brace+1]+check+body[brace+1:])
    for name in ('CHAR_sendItemData','CHAR_sendItemDataOne','LogItem'):
        body=attack.definition(n,name);brace=body.index('{')
        if name=='LogItem':check=r'''
 if(reward_phase==6){
  int actor=ITEM_getWorkInt(item,ITEM_WORKCHARAINDEX),expected_id=(item==9||item==11)?2:1;
  demand(actor>=0&&actor<2&&item==split_winners[actor]&&id==expected_id&&!strcmp(itemname,expected_id==2?"FactoryTwo":"Factory")&&!strcmp(code,expected_id==2?"factory-two":"factory-bounded")&&!strcmp(name,CHAR_getChar(actor,CHAR_NAME))&&!strcmp(key,CHAR_getChar(actor,CHAR_CDKEY))&&!strcmp(cause,"BattleGet(战斗後所得的道具)")&&floor==slots[actor].data[CHAR_FLOOR]&&x==slots[actor].data[CHAR_X]&&y==slots[actor].data[CHAR_Y],"typed split pickup log complete identity/recipient");
  split_logs[actor]++;settle_log_count++;reward_log_count++;return;
 }
'''
        else:
            cond='count==1&&indices[0]==split_slots[actor]' if name=='CHAR_sendItemData' else 'slot==split_slots[actor]'
            counter='split_data[actor]++;reward_data_count++' if name=='CHAR_sendItemData' else 'split_one[actor]++;reward_one_count++'
            check='if(reward_phase==6){demand(actor>=0&&actor<2&&split_winners[actor]>=8&&'+cond+'&&slots[actor].indexOfExistItems[split_slots[actor]]==split_winners[actor],"typed split inventory recipient/slot/object");'+counter+';return TRUE;}\n'
        n=replace_once(n,body,body[:brace+1]+check+body[brace+1:])
    old=prior.controls(profile).replace('reward_phase=4;','reward_phase=5;')
    anchor=item.substitutions(profile,' memcpy(reward_items,chain_saved_items,sizeof chain_saved_items);memcpy(slots,chain_saved_actors,sizeof chain_saved_actors);*arena=chain_saved_arena;')
    updated=replace_once(old,anchor,controls(profile)+'\n'+anchor)
    n=replace_once(n,old,updated)
    original=attack.pp_file(profile,root,attack.LAYOUTS[profile]/'battle/battle.c')
    for name in ('BATTLE_AddExpItem','BATTLE_ItemDelCheck','BATTLE_GetProfit','BATTLE_GetExpGold','BATTLE_Finish','BATTLE_DeleteBattle'):
        body=attack.definition(n,name)
        if body!=attack.definition(original,name):raise ValueError('two-player original body drift '+name)
        print(f'TWO_PLAYER_SOURCE|{profile}|{name}|sha256={hashlib.sha256(body.encode()).hexdigest()}',flush=True)
    return n,lua


def validate_report(report):
    prior.validate_report(report);assignment={};payout={}
    for line in report.splitlines():
        if not line.startswith('ACTUAL|'):continue
        parts=line.split('|');profile=parts[1];marker=parts[2]
        if marker not in ('REAL_HEADER_TWO_PLAYER_ASSIGN','REAL_HEADER_TWO_PLAYER_PAYOUT'):continue
        try:
            f=dict(p.split('=',1) for p in parts[3:]);mask=int(f['mask'])
            if profile not in ('gavin','bismarck') or mask not in MASKS:raise ValueError('unknown two-player profile/mask')
            pending=[[8+k for k in range(4) if ((mask>>k)&1)==a] for a in (0,1)]
            if marker.endswith('ASSIGN'):
                rows=assignment;key=profile,mask
                expected=dict(rng=4,calls=1,release_calls=0,count_delta=0,size0=len(pending[0]),size1=len(pending[1]))
                for a in (0,1):
                    if f[f'pending{a}']!=','.join(map(str,pending[a]+[-1]*(3-len(pending[a])))):raise ValueError('incorrect actual recipient order')
                if f['eligible']!='0,1,-1' or f['initial_pending']!='empty':raise ValueError('incorrect eligible/initial input')
                ones=('whole_items','whole_actors','whole_arena','carried_cleared','no_item_control','original_assignment','no_rebinding')
            else:
                cap=int(f['capacity']);rows=payout;key=profile,mask,cap
                if cap not in range(4):raise ValueError('unknown two-player bag capacity')
                available=[(cap>>a)&1 for a in (0,1)];winners=[pending[a][0] if available[a] else -1 for a in (0,1)];awards=sum(available);b=profile=='bismarck';limit=54 if b else 24
                # Original DeleteItem scans both full sides and enemy disposal scans its ten empty carried slots.
                baseline=84 if b else 54
                expected=dict(active_limit=limit,awards=awards,count_delta=awards-4,release_calls=baseline+4-awards,baseline_release=baseline,rs_count=2,timer_calls=2,timer_draws=2,nu=2 if b else 0,timer_value=1005 if b else 1000)
                for a in (0,1):expected.update({f'winner{a}':winners[a],f'bag{a}':limit-1 if available[a] else -1,f'logs{a}':available[a],f'data{a}':available[a],f'one{a}':available[a] if b else 0})
                for i in range(8,12):
                    owner=winners.index(i) if i in winners else -1
                    expected.update({f'live{i}':int(owner>=0),f'owner{i}':owner,f'ref{i}':int(owner>=0),f'release{i}':int(owner<0)})
                if f['fd_order']!='7,6':raise ValueError('incorrect separate descriptor routing/order')
                ones=('whole_items','whole_fillers','whole_actors','whole_arena','whole_connections','packet_oracle','tickets_cleared','arena_released','no_ticket_control','original_payout')
            expected.update({x:1 for x in ones})
            if key in rows or any(int(f[k])!=v for k,v in expected.items()):raise ValueError('two-player exact state/RNG/release/transport/timer mismatch or duplicate')
            rows[key]=f
        except (KeyError,TypeError) as exc:raise ValueError('incomplete two-player witness') from exc
    if set(assignment)!={(p,m) for p in ('gavin','bismarck') for m in MASKS} or set(payout)!={(p,m,c) for p in ('gavin','bismarck') for m in MASKS for c in range(4)}:raise ValueError('missing two-player recipient order/capacity')
    if 'RESOLUTION|ORIGINAL_REAL_HEADER_TWO_PLAYER_SPLIT_BOUNDED_PASS' not in report.splitlines():raise ValueError('missing two-player split resolution')
    return assignment,payout


def main():
    soft,hard=resource.getrlimit(resource.RLIMIT_STACK)
    if soft!=resource.RLIM_INFINITY and soft<64*1024*1024:resource.setrlimit(resource.RLIMIT_STACK,(64*1024*1024,hard))
    markers=tuple('REAL_HEADER_'+s+'|' for s in ('FINISH_DISPATCH','SAME_ITEM_CAPACITY','TICKET_CLEANUP','RECIPIENT_SIDE','INVALID_ITEM_TICKET','MIXED_ITEM_TICKET','LAST_SLOT_TICKET','DISTINCT_DROP_CREATE','DISTINCT_ITEM_TICKET','OVERFLOW_ASSIGN','OVERFLOW_PAYOUT','FOUR_DROP_CREATE','FOUR_DROP_ASSIGN','FOUR_DROP_PAYOUT','TWO_PLAYER_ASSIGN','TWO_PLAYER_PAYOUT'))
    attack.main(native_builder=split_native,extra_markers=markers)
    print('BOUNDARY|four original-created drops from retained synthetic guaranteed ten-pair master; two eligible PLAYER entries, all fourteen distributed raw endpoint draw orders, separate explicit descriptor6/7 collectors and full/one-free bags; no natural master/probability distribution, early identity, real-client/network or modern DESIGN')
    for s in ('SAME_ITEM_CAPACITY','TICKET_CLEANUP','RECIPIENT_SIDE','INVALID_ITEM_TICKET','MIXED_ITEM_TICKET','LAST_SLOT_TICKET','DISTINCT_ITEM_TICKET','OVERFLOW_TICKET','FOUR_DROP_CHAIN','TWO_PLAYER_SPLIT'):print('RESOLUTION|ORIGINAL_REAL_HEADER_'+s+'_BOUNDED_PASS')

if __name__=='__main__':main()
