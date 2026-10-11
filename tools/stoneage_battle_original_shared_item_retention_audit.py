'Original replacement guard with a synthetic carried old-item alias.'
import hashlib
import resource
from tools import stoneage_battle_original_two_player_concentrated_audit as prior
attack=prior.attack
item=prior.item
replace_once=prior.replace_once


def controls(profile):
    c=prior.controls(profile)
    c=replace_once(c,' for(int branch=0;branch<4;branch++){',' for(int branch=1;branch<4;branch++){\n for(int alias=-1;alias<2;alias++){\n  int retained=alias>=0;')
    c=replace_once(c,' {\n',item.substitutions(profile,' {\n static ITEM_TYPE no_alias_items[256];static Char no_alias_actors[7];static BATTLE no_alias_arena;\n'))
    c=replace_once(c,'   CHAR_setFlg(chain_actor,CHAR_ISDIE,FALSE);',r'''   demand(getFdnum()==2,"synthetic original guard partition includes both actual players");
   for(int a=0;a<2;a++)slots[a].indexOfExistItems[CHAR_STARTITEMARRAY+1]=-1;
   if(retained){demand(slots[alias].indexOfExistItems[CHAR_STARTITEMARRAY+1]==-1,"explicit alias input uses empty second nonequipment bag slot");slots[alias].indexOfExistItems[CHAR_STARTITEMARRAY+1]=victim;}
   CHAR_setFlg(chain_actor,CHAR_ISDIE,FALSE);''')
    c=replace_once(c,'\n   split_release_phase=1;split_release_calls=split_release_empty=0;', '\n   shared_guard_warnings=0;split_release_phase=1;split_release_calls=split_release_empty=0;')
    c=replace_once(c,'   demand(rng_count==', '   demand(shared_guard_warnings==with_item*retained,"one original guard diagnostic only for explicit carried alias");\n   demand(rng_count==')
    c=replace_once(c,'split_release_calls==with_item','split_release_calls==with_item*(1-retained)')
    c=replace_once(c,'(with_item&&8+k==victim)','(with_item&&!retained&&8+k==victim)')
    c=replace_once(c,'if(with_item){split_expected_items[victim].use=0;','if(with_item&&!retained){split_expected_items[victim].use=0;')
    count='ITEM_sUseItemNum' if profile=='bismarck' else 'ITEM_UseItemnum'
    c=replace_once(c,count+'==chain_after_create-with_item',count+'==chain_after_create-with_item*(1-retained)')
    c=replace_once(c,'demand(slots[a].indexOfExistItems[box]<8||slots[a].indexOfExistItems[box]>11,"no original-created object remains carried after assignment");',r'''demand(slots[a].indexOfExistItems[box]==((retained&&a==alias&&box==CHAR_STARTITEMARRAY+1)?victim:slots[a].indexOfExistItems[box])&&((retained&&a==alias&&box==CHAR_STARTITEMARRAY+1)||slots[a].indexOfExistItems[box]<8||slots[a].indexOfExistItems[box]>11),"only explicit carried old-item alias remains after original assignment");
    if(!retained){memcpy(no_alias_items,reward_items,sizeof no_alias_items);memcpy(no_alias_actors,slots,sizeof no_alias_actors);no_alias_arena=*arena;}
    else{
     no_alias_items[victim]=chain_created_items[victim];
     no_alias_actors[alias].indexOfExistItems[CHAR_STARTITEMARRAY+1]=victim;
     demand(!memcmp(no_alias_items,reward_items,sizeof no_alias_items)&&!memcmp(no_alias_actors,slots,sizeof no_alias_actors)&&!memcmp(&no_alias_arena,arena,sizeof no_alias_arena),"exact no-alias original control differs only retained victim and explicit carried alias");
     no_alias_actors[alias].indexOfExistItems[CHAR_STARTITEMARRAY+1]=-1;
    }''')
    a=c.index('    printf("REAL_HEADER_TWO_PLAYER_CONCENTRATED_ASSIGN|');z=c.index('    memcpy(split_assigned_items',a)
    c=c[:a]+r'''    printf("REAL_HEADER_SHARED_ITEM_ASSIGN|recipient=%d|branch=%d|alias=%d|victim=%d|eligible=0,1,-1|pending0=%d,%d,%d|pending1=%d,%d,%d|rng=%d|calls=1|guard_warnings=%d|release_calls=%d|count_delta=%d|victim_live=%d|victim_owner=%d|victim_refs=%d|initial_pending=empty|other_pending_empty=1|whole_items=1|whole_actors=1|whole_arena=1|enemy_carried_cleared=1|no_item_control=1|no_alias_control=1|original_assignment=1|owner_unmodified=1|synthetic_alias=1\n",recipient,branch,alias,victim,pending_two[0][0],pending_two[0][1],pending_two[0][2],pending_two[1][0],pending_two[1][1],pending_two[1][2],rng_count,shared_guard_warnings,1-retained,retained-1,retained,retained?6:-1,retained);
'''+c[z:]
    c=replace_once(c,count+'=chain_after_create-1;',count+'=chain_after_create-1+retained;')
    c=replace_once(c,'       for(int box=CHAR_STARTITEMARRAY;box<CHAR_MAXITEMHAVE;box++)slots[a].indexOfExistItems[box]=-1;',r'''       for(int box=CHAR_STARTITEMARRAY;box<CHAR_MAXITEMHAVE;box++){
        if(retained&&a==alias&&box==CHAR_STARTITEMARRAY+1){demand(slots[a].indexOfExistItems[box]==victim,"prepared payout preserves explicit carried alias");continue;}
        slots[a].indexOfExistItems[box]=-1;
       }''')
    c=replace_once(c,'        if(available[a]&&box==active_limit-1)continue;','        if((retained&&a==alias&&box==CHAR_STARTITEMARRAY+1)||(available[a]&&box==active_limit-1))continue;')
    c=replace_once(c,'references[k]==(8+k==split_winners[0]||8+k==split_winners[1])','references[k]==((retained&&8+k==victim)||8+k==split_winners[0]||8+k==split_winners[1])')
    c=replace_once(c,'REAL_HEADER_TWO_PLAYER_CONCENTRATED_PAYOUT|recipient=%d|branch=%d|victim=%d|','REAL_HEADER_SHARED_ITEM_PAYOUT|recipient=%d|branch=%d|alias=%d|victim=%d|alias_preserved=1|no_double_release=1|synthetic_alias=1|')
    c=replace_once(c,'",recipient,branch,victim,capacity,','",recipient,branch,alias,victim,capacity,')
    c=replace_once(c,' }\n }\n memcpy(reward_items,split_saved_items',' }\n }\n }\n memcpy(reward_items,split_saved_items')
    return c


def shared_native(profile,source,battle,event,root):
    n,lua=prior.concentrated_native(profile,source,battle,event,root)
    old=prior.controls(profile);n=replace_once(n,old,old+'\n'+controls(profile))
    body=attack.definition(n,'BATTLE_ItemDelCheck')
    n='static int shared_guard_warnings;\n'+replace_once(n,body,'#undef fprintf\n#define fprintf(...) (++shared_guard_warnings,++diagnostics,0)\n'+body+'\n#undef fprintf\n#define fprintf(...) (++diagnostics,0)\n')
    original=attack.pp_file(profile,root,attack.LAYOUTS[profile]/'battle/battle.c')
    for name in ('BATTLE_AddExpItem','BATTLE_ItemDelCheck','BATTLE_GetProfit','BATTLE_GetExpGold','BATTLE_Finish','BATTLE_DeleteBattle'):
        body=attack.definition(n,name)
        if body!=attack.definition(original,name):raise ValueError('shared retention original body drift '+name)
        print(f'SHARED_SOURCE|{profile}|{name}|sha256={hashlib.sha256(body.encode()).hexdigest()}',flush=True)
    return n,lua


def validate_report(report):
    prior.validate_report(report);assignment={};payout={}
    for line in report.splitlines():
        if not line.startswith('ACTUAL|'):continue
        parts=line.split('|');profile=parts[1];marker=parts[2]
        if marker not in ('REAL_HEADER_SHARED_ITEM_ASSIGN','REAL_HEADER_SHARED_ITEM_PAYOUT'):continue
        try:
            f=dict(p.split('=',1) for p in parts[3:]);r=int(f['recipient']);b=int(f['branch']);alias=int(f['alias']);retained=alias>=0
            if profile not in ('gavin','bismarck') or r not in (0,1) or b not in (1,2,3) or alias not in (-1,0,1):raise ValueError('unknown shared retention identity')
            victim=7+b;pending=prior.PATTERNS[b]
            if marker.endswith('ASSIGN'):
                rows=assignment;key=profile,r,b,alias
                expected=dict(victim=victim,rng=6,calls=1,guard_warnings=int(retained),release_calls=1-int(retained),count_delta=int(retained)-1,victim_live=int(retained),victim_owner=6 if retained else -1,victim_refs=int(retained))
                for a in (0,1):
                    if f[f'pending{a}']!=','.join(map(str,pending if a==r else (-1,-1,-1))):raise ValueError('incorrect shared pending order')
                if f['eligible']!='0,1,-1' or f['initial_pending']!='empty':raise ValueError('incorrect shared initial state')
                ones=('other_pending_empty','whole_items','whole_actors','whole_arena','enemy_carried_cleared','no_item_control','no_alias_control','original_assignment','owner_unmodified','synthetic_alias')
            else:
                cap=int(f['capacity']);rows=payout;key=profile,r,b,alias,cap
                if cap not in range(4):raise ValueError('unknown shared capacity')
                available=[(cap>>a)&1 for a in (0,1)];received=[available[a] if a==r else 0 for a in (0,1)];winners=[pending[0] if received[a] else -1 for a in (0,1)];awards=sum(received);bis=profile=='bismarck';limit=54 if bis else 24;baseline=84 if bis else 54
                expected=dict(victim=victim,active_limit=limit,awards=awards,count_delta=awards-3,release_calls=baseline+3-awards,baseline_release=baseline,rs_count=2,timer_calls=2,timer_draws=2,nu=2 if bis else 0,timer_value=1005 if bis else 1000)
                for a in (0,1):expected.update({f'winner{a}':winners[a],f'bag{a}':limit-1 if available[a] else -1,f'logs{a}':received[a],f'data{a}':received[a],f'one{a}':received[a] if bis else 0})
                for i in range(8,12):
                    owner=6 if i==victim and retained else (winners.index(i) if i in winners else -1)
                    expected.update({f'live{i}':int(owner>=0),f'owner{i}':owner,f'ref{i}':int(owner>=0),f'release{i}':int(owner<0 and i!=victim)})
                if f['fd_order']!='7,6':raise ValueError('incorrect shared descriptor routing/order')
                ones=('alias_preserved','no_double_release','synthetic_alias','other_bag_unchanged','whole_items','whole_fillers','whole_actors','whole_arena','whole_connections','packet_oracle','tickets_cleared','arena_released','no_ticket_control','original_payout')
            expected.update({x:1 for x in ones})
            if key in rows or any(int(f[k])!=v for k,v in expected.items()):raise ValueError('shared exact retention/count/owner/reference/release/presentation mismatch or duplicate')
            rows[key]=f
        except (KeyError,TypeError) as exc:raise ValueError('incomplete shared witness') from exc
    matrix={(p,r,b,a) for p in ('gavin','bismarck') for r in (0,1) for b in (1,2,3) for a in (-1,0,1)}
    if set(assignment)!=matrix or set(payout)!={k+(c,) for k in matrix for c in range(4)}:raise ValueError('missing shared recipient/replacement/alias/capacity combination')
    if 'RESOLUTION|ORIGINAL_REAL_HEADER_SHARED_ITEM_RETENTION_BOUNDED_PASS' not in report.splitlines():raise ValueError('missing shared retention resolution')
    return assignment,payout


def main():
    soft,hard=resource.getrlimit(resource.RLIMIT_STACK)
    if soft!=resource.RLIM_INFINITY and soft<64*1024*1024:resource.setrlimit(resource.RLIMIT_STACK,(64*1024*1024,hard))
    markers=tuple('REAL_HEADER_'+s+'|' for s in ('FINISH_DISPATCH','SAME_ITEM_CAPACITY','TICKET_CLEANUP','RECIPIENT_SIDE','INVALID_ITEM_TICKET','MIXED_ITEM_TICKET','LAST_SLOT_TICKET','DISTINCT_DROP_CREATE','DISTINCT_ITEM_TICKET','OVERFLOW_ASSIGN','OVERFLOW_PAYOUT','FOUR_DROP_CREATE','FOUR_DROP_ASSIGN','FOUR_DROP_PAYOUT','TWO_PLAYER_ASSIGN','TWO_PLAYER_PAYOUT','TWO_PLAYER_CONCENTRATED_ASSIGN','TWO_PLAYER_CONCENTRATED_PAYOUT','SHARED_ITEM_ASSIGN','SHARED_ITEM_PAYOUT'))
    attack.main(native_builder=shared_native,extra_markers=markers)
    print('BOUNDARY|explicit synthetic preexisting player0/1 carried alias to original-created victim while original owner6 remains; no-alias controls; unchanged replacement guard and payout; retained LV100/EXP0, guaranteed master/RNG/occupancy/bag/descriptor inputs; no natural alias reachability, early identity, real client/network or modern DESIGN')
    for s in ('SAME_ITEM_CAPACITY','TICKET_CLEANUP','RECIPIENT_SIDE','INVALID_ITEM_TICKET','MIXED_ITEM_TICKET','LAST_SLOT_TICKET','DISTINCT_ITEM_TICKET','OVERFLOW_TICKET','FOUR_DROP_CHAIN','TWO_PLAYER_SPLIT','TWO_PLAYER_CONCENTRATED','SHARED_ITEM_RETENTION'):print('RESOLUTION|ORIGINAL_REAL_HEADER_'+s+'_BOUNDED_PASS')

if __name__=='__main__':main()
