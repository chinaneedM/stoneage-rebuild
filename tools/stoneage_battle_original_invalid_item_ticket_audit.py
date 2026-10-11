"""Bounded invalid item tickets through unchanged original second Finish."""
import hashlib
import resource
from tools import stoneage_battle_original_recipient_side_audit as prior
attack = prior.attack
replace_once = prior.replace_once
CASES = (249, 3, 256, 2147483647, -2, -2147483648)


def invalid_controls(profile):
    c = prior.prior.NEGATIVE.replace('negative_', 'invalid_')
    c = replace_once(c, 'invalid_case<4', 'invalid_case<6')
    c = replace_once(c, 'int recipient=invalid_case==1?2:invalid_case==2?-1:0;',
                     'int recipient=0;int indices[6]={249,3,256,2147483647,-2,(-2147483647-1)};int ticket=indices[invalid_case];')
    c = replace_once(c, 'static ITEM_TYPE invalid_saved_items[256],invalid_expected_items[256];',
                     'static ITEM_TYPE invalid_saved_items[256],invalid_expected_items[256],invalid_input_items[256];')
    c = replace_once(c, 'arena->use=1;',
                     'ITEM_SIZE=256;demand(ITEM_SIZE==256,"explicit complete pool boundary fixture");\n'
                     '   if(invalid_case==1){_ITEM_endExistItemsOne(3,"invalid-ticket-input",1);\n'
                     '    demand(reward_items[3].use==0&&reward_items[3].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]==-1&&ITEM_COUNT==invalid_saved_count-1,"original release creates inactive stale ticket input");}\n'
                     '   demand(invalid_case>1||!ITEM_CHECKINDEX(ticket),"inactive ticket input verified by original check");\n'
                     '   memcpy(invalid_input_items,reward_items,sizeof invalid_input_items);int input_count=ITEM_COUNT;\n'
                     '   arena->use=1;')
    c = replace_once(c, 'arena->Side[0].Entry[0].getitem[0]=3;', 'arena->Side[0].Entry[0].getitem[0]=ticket;')
    c = replace_once(c, '    if(invalid_case==3)arena->Side[0].Entry[0].getitem[1]=3;', '')
    c = replace_once(c, 'CHAR_setFlg(0,CHAR_ISDIE,invalid_case==0);', 'CHAR_setFlg(0,CHAR_ISDIE,FALSE);')
    c = c.replace('invalid_case==0||invalid_case==3', '1')
    c = replace_once(c, 'reward_phase=invalid_case==3?3:2;', 'reward_phase=2;')
    c = replace_once(c, '!memcmp(invalid_saved_items,reward_items,sizeof invalid_saved_items)&&ITEM_COUNT==invalid_saved_count',
                     '!memcmp(invalid_input_items,reward_items,sizeof invalid_input_items)&&ITEM_COUNT==input_count')
    start=c.index('    if(invalid_case==3){')
    end=c.index('    demand(!memcmp(invalid_expected_items',start)
    c=c[:start]+c[end:]
    c=replace_once(c, 'if(slots[actor].indexOfExistItems[box]==3)', 'if(slots[actor].indexOfExistItems[box]==ticket)')
    c=c.replace('(invalid_case==3?2:0)', '0').replace('(invalid_case==3?1:0)', '0')
    start=c.index('    printf("REAL_HEADER_TICKET_CLEANUP|')
    end=c.index('   }\n   reward_phase=0;',start)
    c=c[:start]+r'''    printf("REAL_HEADER_INVALID_ITEM_TICKET|case=%d|ticket=%d|recipient=0|pool_size=256|pool_unchanged=1|count_unchanged=1|references=0|logs=%d|data=%d|one=%d|second_loop=1|arena_released=1|tickets_cleared=1|whole_items=1|whole_actors=1|whole_arena=1|whole_connections=1|original_timer=1\n",
           invalid_case,ticket,reward_log_count,reward_data_count,reward_one_count);
'''+c[end:]
    c=prior.prior.capacity.prior.payout.ticket.drop.factory.allocator.item.substitutions(profile,c)
    return (c.replace('ENTRY_FIELD','char_index' if profile=='bismarck' else 'charaindex')
            .replace('WIN_SIDE','-1' if profile=='bismarck' else '0')
            .replace('ONE_EXPECTED','0')
            .replace('CONNECTION_TYPE','GmsvSession' if profile=='bismarck' else 'CONNECT')
            .replace('TIMER_EXPECTED','1005' if profile=='bismarck' else '1000')
            .replace('TIMER_DRAWS','1').replace('TIMER_SENDS','1' if profile=='bismarck' else '0'))


def invalid_native(profile, source, battle, event, root):
    native,has_lua=prior.side_native(profile,source,battle,event,root)
    old=prior.guard_controls(profile)
    native=replace_once(native,old,old+'\n'+invalid_controls(profile))
    item=attack.pp_file(profile,root,attack.LAYOUTS[profile]/'item/item.c')
    for name,original_source in (('_ITEM_CHECKINDEX',item),('_ITEM_endExistItemsOne',item),('BATTLE_DeleteItem',battle)):
        body=attack.definition(native,name)
        original=attack.definition(original_source,name)
        if body!=original:
            raise ValueError('original invalid-ticket body drift '+name)
        print(f'INVALID_TICKET_SOURCE|{profile}|{name}|sha256={hashlib.sha256(body.encode()).hexdigest()}',flush=True)
    return native,has_lua


def validate_report(report):
    prior.validate_report(report)
    rows={}
    for line in report.splitlines():
        if not line.startswith('ACTUAL|') or '|REAL_HEADER_INVALID_ITEM_TICKET|' not in line:
            continue
        parts=line.split('|');profile=parts[1]
        try:
            fields=dict(p.split('=',1) for p in parts[3:]);case=int(fields['case']);key=profile,case
            if profile not in ('gavin','bismarck') or case not in range(len(CASES)) or key in rows:
                raise ValueError('unknown/duplicate invalid-ticket witness')
            expected=dict(ticket=CASES[case],recipient=0,pool_size=256,references=0,logs=0,data=0,one=0)
            for name in ('pool_unchanged','count_unchanged','second_loop','arena_released','tickets_cleared','whole_items','whole_actors','whole_arena','whole_connections','original_timer'):
                expected[name]=1
            if any(int(fields[n])!=v for n,v in expected.items()):
                raise ValueError('invalid-ticket witness disagrees with complete state oracle')
            rows[key]=fields
        except (KeyError,TypeError) as exc:
            raise ValueError('incomplete invalid-ticket witness') from exc
    if set(rows)!={(p,c) for p in ('gavin','bismarck') for c in range(len(CASES))}:
        raise ValueError('missing invalid-ticket profile/case')
    if 'RESOLUTION|ORIGINAL_REAL_HEADER_INVALID_ITEM_TICKET_BOUNDED_PASS' not in report.splitlines():
        raise ValueError('missing invalid-ticket resolution')
    return rows


def main():
    soft,hard=resource.getrlimit(resource.RLIMIT_STACK)
    if soft!=resource.RLIM_INFINITY and soft<64*1024*1024:
        resource.setrlimit(resource.RLIMIT_STACK,(64*1024*1024,hard))
    attack.main(native_builder=invalid_native,extra_markers=('REAL_HEADER_FINISH_DISPATCH|','REAL_HEADER_SAME_ITEM_CAPACITY|','REAL_HEADER_TICKET_CLEANUP|','REAL_HEADER_RECIPIENT_SIDE|','REAL_HEADER_INVALID_ITEM_TICKET|'))
    print('BOUNDARY|explicit inactive249, original release3, pool boundary256, INT_MAX, -2 and INT_MIN tickets; no natural invalid-ticket reachability or early server provenance; typed transport')
    for gate in ('SAME_ITEM_CAPACITY','TICKET_CLEANUP','RECIPIENT_SIDE','INVALID_ITEM_TICKET'):
        print('RESOLUTION|ORIGINAL_REAL_HEADER_'+gate+'_BOUNDED_PASS')


if __name__=='__main__':main()
