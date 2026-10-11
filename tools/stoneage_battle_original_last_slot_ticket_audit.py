"""Original mixed-ticket competition at one free active bag slot or full bag."""
import hashlib
import resource
from tools import stoneage_battle_original_mixed_item_ticket_audit as prior
from tools import stoneage_party_pet_original_reward_item_audit as item

attack=prior.attack
replace_once=prior.replace_once


def last_slot_controls(profile):
    c=prior.mixed_controls(profile).replace('mixed_','lastslot_')
    c=replace_once(c,' for(int kind=0;kind<2;kind++){',' for(int available=0;available<2;available++){\n for(int kind=0;kind<2;kind++){')
    c=replace_once(c,'\n memcpy(reward_items,lastslot_saved_items','\n }\n memcpy(reward_items,lastslot_saved_items')
    c=replace_once(c,'mask|=1<<k;}','mask|=1<<k;}\n  int first_valid=0;while(pattern[first_valid]!=3)first_valid++;awards=available;')
    decl=item.substitutions(profile,'static ITEM_TYPE lastslot_input_items[256];')
    c=replace_once(c,'char lastslot_baseline_rs[1024];', 'char lastslot_baseline_rs[1024];int lastslot_baseline_release=0;'+decl)
    setup=item.substitutions(profile,'''int active_limit=ITEM_LIMIT;
   demand(active_limit==ACTIVE_EXPECTED,"exact native active inventory limit");
   for(int box=CHAR_STARTITEMARRAY;box<active_limit;box++){
    if(available&&box==active_limit-1)continue;
    int filler=80+box;
    demand(filler<249&&!reward_items[filler].use,"explicit unused filler record");
    reward_items[filler].use=1;reward_items[filler].ITEM_FIELD.data[ITEM_ID]=1800+filler;
    reward_items[filler].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]=0;
    reward_items[filler].ITEM_FIELD.workint[ITEM_WORKOBJINDEX]=-1;
    slots[0].indexOfExistItems[box]=filler;ITEM_COUNT++;
   }
   memcpy(lastslot_input_items,reward_items,sizeof lastslot_input_items);int input_count=ITEM_COUNT;
   arena->use=1;''').replace('ACTIVE_EXPECTED','54' if profile=='bismarck' else '24')
    c=replace_once(c,'   arena->use=1;', '   '+setup)
    c=replace_once(c,'demand(first_slot==CHAR_STARTITEMARRAY,"explicit empty bag fixture first slot");',
                   'demand(first_slot==(available?active_limit-1:-1),"exact final active slot or full bag input");')
    c=replace_once(c,'reward_phase=kind?3:2;', 'reward_phase=2;')
    c=replace_once(c,'int cleanup_ret=BATTLE_Loop();',
        'lastslot_release_phase=1;lastslot_release_calls=lastslot_release_item3=lastslot_release_invalid=lastslot_release_empty=0;\n'
        '   int cleanup_ret=BATTLE_Loop();lastslot_release_phase=0;\n'
        '   if(!with_ticket)lastslot_baseline_release=lastslot_release_empty;\n'
        '   demand(lastslot_release_empty==lastslot_baseline_release&&lastslot_release_item3==(with_ticket?kind+1-available:0)&&lastslot_release_invalid==(with_ticket&&bad<3?(kind?1:2):0)&&lastslot_release_calls==lastslot_release_empty+lastslot_release_item3+lastslot_release_invalid,"actual release calls versus original no-ticket empty-slot teardown");')
    c=replace_once(c,'!memcmp(lastslot_saved_items,reward_items,sizeof lastslot_saved_items)&&'+item.substitutions(profile,'ITEM_COUNT')+'==lastslot_saved_count',
                   '!memcmp(lastslot_input_items,reward_items,sizeof lastslot_input_items)&&'+item.substitutions(profile,'ITEM_COUNT')+'==input_count')
    old=item.substitutions(profile,'''    lastslot_expected_items[3].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]=0;
    lastslot_expected_items[3].ITEM_FIELD.workint[ITEM_WORKOBJINDEX]=-1;
    for(int k=0;k<awards;k++)lastslot_expected_actors[0].indexOfExistItems[first_slot+k]=3;''')
    new=item.substitutions(profile,'''    if(available){
     lastslot_expected_items[3].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]=0;
     lastslot_expected_items[3].ITEM_FIELD.workint[ITEM_WORKOBJINDEX]=-1;
     lastslot_expected_actors[0].indexOfExistItems[first_slot]=3;
    }else{
     lastslot_expected_items[3].use=0;
     lastslot_expected_items[3].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]=-1;expected_count--;
    }''')
    c=replace_once(c,old,new)
    c=replace_once(c,'reward_data_count==1&&','reward_data_count==available&&')
    c=replace_once(c,'if(pattern[k]==3)strcat(lastslot_expected_rs,','if(available&&k==first_valid)strcat(lastslot_expected_rs,')
    start=c.index('    printf("REAL_HEADER_MIXED_ITEM_TICKET|')
    end=c.index('   }\n   reward_phase=0;',start)
    printf=item.substitutions(profile,r'''    printf("REAL_HEADER_LAST_SLOT_TICKET|available=%d|kind=%d|bad=%d|position=%d|invalid=%d|pending_mask=%d|accepted_mask=%d|pending_valid=%d|awards=%d|bag_slot=%d|active_limit=%d|named_items=%d|leak=LEAK_EXPECTED|secret_empty=1|item=3|live=%d|owner=%d|pool_size=256|count_delta=%d|references=%d|logs=%d|data=%d|one=%d|release_calls=%d|release_item3=%d|release_invalid=%d|release_empty=%d|baseline_release=%d|rs=1|packet_oracle=1|second_loop=1|arena_released=1|tickets_cleared=1|whole_items=1|whole_fillers=1|whole_actors=1|whole_arena=1|whole_connections=1|original_timer=1\n",
           available,kind,bad,position,invalids[bad],mask,available?1<<first_valid:0,kind+1,awards,first_slot,active_limit,NAMED_COUNT,
           reward_items[3].use,reward_items[3].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX],ITEM_COUNT-input_count,
           references,reward_log_count,reward_data_count,reward_one_count,lastslot_release_calls,lastslot_release_item3,lastslot_release_invalid,lastslot_release_empty,lastslot_baseline_release);
''').replace('LEAK_EXPECTED','0' if profile=='bismarck' else '1').replace('NAMED_COUNT','available' if profile=='bismarck' else '0')
    return c[:start]+printf+c[end:]


OBSERVER=r'''
static void demand(int truth,const char *name);
static int lastslot_release_phase,lastslot_release_calls,lastslot_release_item3,lastslot_release_invalid,lastslot_release_empty;
static void lastslot_release_observer(int index,char *file,int line){
 if(lastslot_release_phase){lastslot_release_calls++;if(index==3)lastslot_release_item3++;else if(index==-1)lastslot_release_empty++;else {demand(index==249||index==256||index==2147483647,"only explicit nonnegative invalid release indices");lastslot_release_invalid++;}}
 _ITEM_endExistItemsOne(index,file,line);
}
#pragma push_macro("ITEM_endExistItemsOne")
#undef ITEM_endExistItemsOne
#define ITEM_endExistItemsOne(index) lastslot_release_observer(index,__FILE__,__LINE__)
'''


def last_slot_native(profile,source,battle,event,root):
    native,has_lua=prior.mixed_native(profile,source,battle,event,root)
    old=prior.mixed_controls(profile)
    native=replace_once(native,old,old+'\n'+last_slot_controls(profile))
    native=replace_once(native,'static Char slots[7];','static Char slots[7];\n'+OBSERVER)
    for path,names in {'item/item.c':('_ITEM_endExistItemsOne',),
                       'char/char_item.c':('CHAR_findEmptyItemBox','CHAR_addItemSpecificItemIndex')}.items():
        original=attack.pp_file(profile,root,attack.LAYOUTS[profile]/path)
        for name in names:
            body=attack.definition(native,name)
            if body!=attack.definition(original,name):raise ValueError('original last-slot body drift '+name)
            print(f'LAST_SLOT_SOURCE|{profile}|{name}|sha256={hashlib.sha256(body.encode()).hexdigest()}',flush=True)
    return native,has_lua


def validate_report(report):
    prior.validate_report(report)
    rows={}
    for line in report.splitlines():
        if not line.startswith('ACTUAL|') or '|REAL_HEADER_LAST_SLOT_TICKET|' not in line:continue
        parts=line.split('|');profile=parts[1]
        try:
            f=dict(p.split('=',1) for p in parts[3:]);a=int(f['available']);k=int(f['kind']);b=int(f['bad']);p=int(f['position']);key=profile,a,k,b,p
            if profile not in ('gavin','bismarck') or a not in (0,1) or k not in (0,1) or b not in range(5 if k else 6) or p not in range(3) or key in rows:raise ValueError('unknown/duplicate last-slot witness')
            mask=7-(1<<p) if k else 1<<p;first=next(i for i in range(3) if mask&(1<<i));ri=(1 if k else 2) if b<3 else 0;r3=k+1-a
            expected=dict(invalid=prior.INVALID[b],pending_mask=mask,accepted_mask=(1<<first) if a else 0,pending_valid=k+1,awards=a,
                          bag_slot=(53 if profile=='bismarck' else 23) if a else -1,active_limit=54 if profile=='bismarck' else 24,
                          named_items=a if profile=='bismarck' else 0,leak=0 if profile=='bismarck' else 1,secret_empty=1,item=3,live=a,owner=0 if a else -1,
                          pool_size=256,count_delta=0 if a else -1,references=a,logs=a,data=a,one=a if profile=='bismarck' else 0,
                          release_calls=(84 if profile=='bismarck' else 54)+r3+ri,release_item3=r3,release_invalid=ri,release_empty=84 if profile=='bismarck' else 54,baseline_release=84 if profile=='bismarck' else 54,rs=1)
            for n in ('packet_oracle','second_loop','arena_released','tickets_cleared','whole_items','whole_fillers','whole_actors','whole_arena','whole_connections','original_timer'):expected[n]=1
            if any(int(f[n])!=v for n,v in expected.items()):raise ValueError('last-slot witness disagrees with ordered retention/release oracle')
            rows[key]=f
        except (KeyError,TypeError) as exc:raise ValueError('incomplete last-slot witness') from exc
    if set(rows)!={(p,a,k,b,s) for p in ('gavin','bismarck') for a in (0,1) for k in (0,1) for b in range(5 if k else 6) for s in range(3)}:raise ValueError('missing last-slot profile/capacity/pattern')
    if 'RESOLUTION|ORIGINAL_REAL_HEADER_LAST_SLOT_TICKET_BOUNDED_PASS' not in report.splitlines():raise ValueError('missing last-slot resolution')
    return rows


def main():
    soft,hard=resource.getrlimit(resource.RLIMIT_STACK)
    if soft!=resource.RLIM_INFINITY and soft<64*1024*1024:resource.setrlimit(resource.RLIMIT_STACK,(64*1024*1024,hard))
    attack.main(native_builder=last_slot_native,extra_markers=('REAL_HEADER_FINISH_DISPATCH|','REAL_HEADER_SAME_ITEM_CAPACITY|','REAL_HEADER_TICKET_CLEANUP|','REAL_HEADER_RECIPIENT_SIDE|','REAL_HEADER_INVALID_ITEM_TICKET|','REAL_HEADER_MIXED_ITEM_TICKET|','REAL_HEADER_LAST_SLOT_TICKET|'))
    print('BOUNDARY|explicit synthetic bag fillers and logical256 pool; original release observer forwards unchanged arguments; late-source original functions; no natural invalid/duplicate generation, early server identity, real transport or modern ownership DESIGN')
    for gate in ('SAME_ITEM_CAPACITY','TICKET_CLEANUP','RECIPIENT_SIDE','INVALID_ITEM_TICKET','MIXED_ITEM_TICKET','LAST_SLOT_TICKET'):print('RESOLUTION|ORIGINAL_REAL_HEADER_'+gate+'_BOUNDED_PASS')


if __name__=='__main__':main()
