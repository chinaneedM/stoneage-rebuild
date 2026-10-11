"""Original four drops all assigned to one of two eligible PLAYER recipients."""
import hashlib
import resource
from tools import stoneage_battle_original_two_player_split_audit as prior
attack=prior.attack
item=prior.item
replace_once=prior.replace_once
PATTERNS=prior.prior.PATTERNS

RNG=r'''
static int concentrated_rng_phase,concentrated_rng_recipient,concentrated_rng_branch,concentrated_rng_at;
static int concentrated_rand(void){
 if(!concentrated_rng_phase)return split_rand();
 int at=concentrated_rng_at++;rng_count++;
 demand(at<6,"bounded concentrated recipient/overflow original RNG stream");
 if(at<4)return concentrated_rng_recipient?2147483647:0;
 if(at==4)return concentrated_rng_branch?2147483647:0;
 int raw[3]={0,1073741824,2147483647};return raw[concentrated_rng_branch-1];
}
#undef rand
#define rand concentrated_rand
'''


def controls(profile):
    c=prior.controls(profile)
    a=c.index(' for(int mask=1;mask<15;mask++){');z=c.index('  for(int with_item=',a)
    c=c[:a]+r''' for(int recipient=0;recipient<2;recipient++){
 for(int branch=0;branch<4;branch++){
  int mask=recipient?15:0,victim=branch?7+branch:11;
  int pending_two[2][3]={{-1,-1,-1},{-1,-1,-1}};
  for(int k=0;k<3;k++)pending_two[recipient][k]=8+k;
  if(branch)pending_two[recipient][branch-1]=11;
'''+c[z:]
    c=replace_once(c,'   split_rng_phase=1;split_rng_mask=mask;split_rng_at=0;rng_count=0;',
                   '   concentrated_rng_phase=1;concentrated_rng_recipient=recipient;concentrated_rng_branch=branch;concentrated_rng_at=0;rng_count=0;')
    c=replace_once(c,'   split_release_phase=0;split_rng_phase=0;','   split_release_phase=0;concentrated_rng_phase=0;')
    c=replace_once(c,'demand(rng_count==(with_item?4:0)&&split_rng_at==rng_count,"exact distributed recipient RNG stream without overflow draws");',
                   'demand(rng_count==(with_item?(branch?6:5):0)&&concentrated_rng_at==rng_count,"four recipient draws and exact coin/optional replacement draw");')
    c=replace_once(c,'demand(!split_release_calls&&!split_release_empty,"distributed original assignment releases no object");',
                   'demand(split_release_calls==with_item&&!split_release_empty,"one exact overflow release versus zero no-item releases");\n   for(int k=0;k<4;k++)demand(split_release_hits[k]==(with_item&&8+k==victim),"exact concentrated assignment victim release");')
    original='   demand(!memcmp(chain_created_items,reward_items,sizeof chain_created_items)&&ITEM_COUNT==chain_after_create,"assignment preserves all256 original records/count and original enemy ownership");'
    expected=item.substitutions(profile,r'''   memcpy(split_expected_items,chain_created_items,sizeof split_expected_items);
   if(with_item){split_expected_items[victim].use=0;split_expected_items[victim].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]=-1;}
   demand(!memcmp(split_expected_items,reward_items,sizeof split_expected_items)&&ITEM_COUNT==chain_after_create-with_item,"all256 items/count match exact original overflow victim change");''')
    original=item.substitutions(profile,original);c=replace_once(c,original,expected)
    a=c.index('    printf("REAL_HEADER_TWO_PLAYER_ASSIGN|');z=c.index('    memcpy(split_assigned_items',a)
    c=c[:a]+r'''    printf("REAL_HEADER_TWO_PLAYER_CONCENTRATED_ASSIGN|recipient=%d|branch=%d|victim=%d|eligible=0,1,-1|pending0=%d,%d,%d|pending1=%d,%d,%d|rng=%d|calls=1|release_calls=1|count_delta=-1|initial_pending=empty|other_pending_empty=1|whole_items=1|whole_actors=1|whole_arena=1|carried_cleared=1|no_item_control=1|original_assignment=1|no_rebinding=1\n",recipient,branch,victim,pending_two[0][0],pending_two[0][1],pending_two[0][2],pending_two[1][0],pending_two[1][1],pending_two[1][2],rng_count);
'''+c[z:]
    c=replace_once(c,'int available[2]={capacity&1,(capacity>>1)&1},awards=available[0]+available[1];',
                   'int available[2]={capacity&1,(capacity>>1)&1},received[2]={0,0};received[recipient]=available[recipient];int awards=received[recipient];')
    c=replace_once(c,'split_winners[a]=available[a]?pending_two[a][0]:-1;', 'split_winners[a]=received[a]?pending_two[a][0]:-1;')
    count='ITEM_sUseItemNum' if profile=='bismarck' else 'ITEM_UseItemnum'
    c=replace_once(c,'*arena=split_assigned_arena;'+count+'=chain_after_create;', '*arena=split_assigned_arena;'+count+'=chain_after_create-1;')
    c=replace_once(c,'(with_ticket?4-awards:0)','(with_ticket?3-awards:0)')
    c=replace_once(c,'(with_ticket&&8+k!=split_winners[0]&&8+k!=split_winners[1])','(with_ticket&&8+k!=victim&&8+k!=split_winners[0]&&8+k!=split_winners[1])')
    c=replace_once(c,'int index=8+k,owner=', 'int index=8+k;if(index==victim)continue;int owner=')
    c=replace_once(c,'split_logs[a]==available[a]&&split_data[a]==available[a]&&split_one[a]=='+('available[a]' if profile=='bismarck' else '0'),
                   'split_logs[a]==received[a]&&split_data[a]==received[a]&&split_one[a]=='+('received[a]' if profile=='bismarck' else '0'))
    c=replace_once(c,'if(available[a]&&k==0)','if(received[a]&&k==0)')
    c=replace_once(c,'       printf("REAL_HEADER_TWO_PLAYER_PAYOUT|mask=%d|capacity=%d|',
                   '       demand(CHAR_findEmptyItemBox(1-recipient)==split_slots[1-recipient],"other eligible player bag capacity remains unconsumed");\n       printf("REAL_HEADER_TWO_PLAYER_CONCENTRATED_PAYOUT|recipient=%d|branch=%d|victim=%d|other_bag_unchanged=1|capacity=%d|')
    c=replace_once(c,'",mask,capacity,split_winners[0]', '",recipient,branch,victim,capacity,split_winners[0]')
    c=replace_once(c,' }\n memcpy(reward_items,split_saved_items',' }\n }\n memcpy(reward_items,split_saved_items')
    return c


def concentrated_native(profile,source,battle,event,root):
    n,lua=prior.split_native(profile,source,battle,event,root)
    n=replace_once(n,'#define rand split_rand\n','#define rand split_rand\n'+RNG)
    old=prior.controls(profile);n=replace_once(n,old,old+'\n'+controls(profile))
    original=attack.pp_file(profile,root,attack.LAYOUTS[profile]/'battle/battle.c')
    for name in ('BATTLE_AddExpItem','BATTLE_ItemDelCheck','BATTLE_GetProfit','BATTLE_GetExpGold','BATTLE_Finish','BATTLE_DeleteBattle'):
        body=attack.definition(n,name)
        if body!=attack.definition(original,name):raise ValueError('concentrated original body drift '+name)
        print(f'CONCENTRATED_SOURCE|{profile}|{name}|sha256={hashlib.sha256(body.encode()).hexdigest()}',flush=True)
    return n,lua


def validate_report(report):
    prior.validate_report(report);assignment={};payout={}
    for line in report.splitlines():
        if not line.startswith('ACTUAL|'):continue
        parts=line.split('|');profile=parts[1];marker=parts[2]
        if marker not in ('REAL_HEADER_TWO_PLAYER_CONCENTRATED_ASSIGN','REAL_HEADER_TWO_PLAYER_CONCENTRATED_PAYOUT'):continue
        try:
            f=dict(p.split('=',1) for p in parts[3:]);recipient=int(f['recipient']);branch=int(f['branch'])
            if profile not in ('gavin','bismarck') or recipient not in (0,1) or branch not in range(4):raise ValueError('unknown concentrated profile/recipient/branch')
            victim=7+branch if branch else 11;pending=PATTERNS[branch]
            if marker.endswith('ASSIGN'):
                rows=assignment;key=profile,recipient,branch
                expected=dict(victim=victim,rng=6 if branch else 5,calls=1,release_calls=1,count_delta=-1)
                for a in (0,1):
                    if f[f'pending{a}']!=','.join(map(str,pending if a==recipient else (-1,-1,-1))):raise ValueError('incorrect concentrated pending order')
                if f['eligible']!='0,1,-1' or f['initial_pending']!='empty':raise ValueError('incorrect eligible/initial state')
                ones=('other_pending_empty','whole_items','whole_actors','whole_arena','carried_cleared','no_item_control','original_assignment','no_rebinding')
            else:
                cap=int(f['capacity']);rows=payout;key=profile,recipient,branch,cap
                if cap not in range(4):raise ValueError('unknown concentrated bag capacity')
                available=[(cap>>a)&1 for a in (0,1)];received=[available[a] if a==recipient else 0 for a in (0,1)];winners=[pending[0] if received[a] else -1 for a in (0,1)];awards=sum(received);b=profile=='bismarck';limit=54 if b else 24;baseline=84 if b else 54
                expected=dict(victim=victim,active_limit=limit,awards=awards,count_delta=awards-3,release_calls=baseline+3-awards,baseline_release=baseline,rs_count=2,timer_calls=2,timer_draws=2,nu=2 if b else 0,timer_value=1005 if b else 1000)
                for a in (0,1):expected.update({f'winner{a}':winners[a],f'bag{a}':limit-1 if available[a] else -1,f'logs{a}':received[a],f'data{a}':received[a],f'one{a}':received[a] if b else 0})
                for i in range(8,12):
                    owner=winners.index(i) if i in winners else -1
                    expected.update({f'live{i}':int(owner>=0),f'owner{i}':owner,f'ref{i}':int(owner>=0),f'release{i}':int(owner<0 and i!=victim)})
                if f['fd_order']!='7,6':raise ValueError('incorrect separate descriptor routing/order')
                ones=('other_bag_unchanged','whole_items','whole_fillers','whole_actors','whole_arena','whole_connections','packet_oracle','tickets_cleared','arena_released','no_ticket_control','original_payout')
            expected.update({x:1 for x in ones})
            if key in rows or any(int(f[k])!=v for k,v in expected.items()):raise ValueError('concentrated exact victim/state/release/presentation mismatch or duplicate')
            rows[key]=f
        except (KeyError,TypeError) as exc:raise ValueError('incomplete concentrated witness') from exc
    if set(assignment)!={(p,r,b) for p in ('gavin','bismarck') for r in (0,1) for b in range(4)} or set(payout)!={(p,r,b,c) for p in ('gavin','bismarck') for r in (0,1) for b in range(4) for c in range(4)}:raise ValueError('missing concentrated recipient/overflow/capacity combination')
    if 'RESOLUTION|ORIGINAL_REAL_HEADER_TWO_PLAYER_CONCENTRATED_BOUNDED_PASS' not in report.splitlines():raise ValueError('missing concentrated resolution')
    return assignment,payout


def main():
    soft,hard=resource.getrlimit(resource.RLIMIT_STACK)
    if soft!=resource.RLIM_INFINITY and soft<64*1024*1024:resource.setrlimit(resource.RLIMIT_STACK,(64*1024*1024,hard))
    markers=tuple('REAL_HEADER_'+s+'|' for s in ('FINISH_DISPATCH','SAME_ITEM_CAPACITY','TICKET_CLEANUP','RECIPIENT_SIDE','INVALID_ITEM_TICKET','MIXED_ITEM_TICKET','LAST_SLOT_TICKET','DISTINCT_DROP_CREATE','DISTINCT_ITEM_TICKET','OVERFLOW_ASSIGN','OVERFLOW_PAYOUT','FOUR_DROP_CREATE','FOUR_DROP_ASSIGN','FOUR_DROP_PAYOUT','TWO_PLAYER_ASSIGN','TWO_PLAYER_PAYOUT','TWO_PLAYER_CONCENTRATED_ASSIGN','TWO_PLAYER_CONCENTRATED_PAYOUT'))
    attack.main(native_builder=concentrated_native,extra_markers=markers)
    print('BOUNDARY|retained synthetic guaranteed ten-pair master/four original-created objects; two eligible PLAYER entries, raw endpoints concentrate all four at one player with reject/each replacement, normalized LV100/EXP0 and full/one-free bags, explicit descriptor collectors; no natural RNG weighting/master, early identity, real client/network or modern DESIGN')
    for s in ('SAME_ITEM_CAPACITY','TICKET_CLEANUP','RECIPIENT_SIDE','INVALID_ITEM_TICKET','MIXED_ITEM_TICKET','LAST_SLOT_TICKET','DISTINCT_ITEM_TICKET','OVERFLOW_TICKET','FOUR_DROP_CHAIN','TWO_PLAYER_SPLIT','TWO_PLAYER_CONCENTRATED'):print('RESOLUTION|ORIGINAL_REAL_HEADER_'+s+'_BOUNDED_PASS')

if __name__=='__main__':main()
