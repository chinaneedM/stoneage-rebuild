"""Original ordinary-NPC versus player recipient crossed with battle-side type.

Only explicit native fixture inputs are changed; original game bodies and
accepted capacity/exceptional-ticket controls remain intact.
"""
import hashlib
import resource
from tools import stoneage_battle_original_ticket_cleanup_audit as prior

attack = prior.attack
replace_once = prior.capacity.prior.replace_once


def guard_controls(profile):
    c = prior.NEGATIVE.replace('negative_', 'guard_')
    c = replace_once(c, ' for(int guard_case=0;', ' for(int guard_side=0;guard_side<2;guard_side++){\n for(int guard_case=0;')
    c = replace_once(c, '\n memcpy(reward_items,guard_saved_items', '\n }\n memcpy(reward_items,guard_saved_items')
    c = replace_once(c, 'int recipient=guard_case==1?2:guard_case==2?-1:0;',
                     'int recipient=0;int accepted=GUARD_ACCEPT;')
    c = replace_once(c, 'arena->Side[0].type=BATTLE_S_TYPE_PLAYER;',
                     'arena->Side[guard_side].type=guard_case>=2?BATTLE_S_TYPE_ENEMY:BATTLE_S_TYPE_PLAYER;\n'
                     '   slots[0].data[CHAR_WHICHTYPE]=guard_case%2?CHAR_TYPEOTHERNPC:CHAR_TYPEPLAYER;')
    c = replace_once(c, 'arena->Side[1].type=BATTLE_S_TYPE_ENEMY;', 'arena->Side[1-guard_side].type=BATTLE_S_TYPE_ENEMY;')
    c = c.replace('arena->Side[0].Entry[0]', 'arena->Side[guard_side].Entry[0]')
    c = c.replace('arena->Side[1].Entry[0]', 'arena->Side[1-guard_side].Entry[0]')
    c = replace_once(c, '    if(guard_case==3)arena->Side[guard_side].Entry[0].getitem[1]=3;', '')
    c = replace_once(c, 'CHAR_setFlg(0,CHAR_ISDIE,guard_case==0);', 'CHAR_setFlg(0,CHAR_ISDIE,FALSE);')
    c = replace_once(c, 'reward_phase=guard_case==3?3:2;', 'reward_phase=2;')
    c = c.replace('guard_case==0||guard_case==3', 'guard_case%2==0')
    c = replace_once(c, 'if(guard_case==3){', 'if(accepted){')
    c = replace_once(c, '     guard_expected_actors[0].indexOfExistItems[first_slot+1]=3;', '')
    c = c.replace('(guard_case==3?2:0)', 'accepted').replace('(guard_case==3?1:0)', 'accepted')
    start = c.index('    printf("REAL_HEADER_TICKET_CLEANUP|')
    end = c.index('   }\n   reward_phase=0;', start)
    c = c[:start] + r'''    printf("REAL_HEADER_RECIPIENT_SIDE|side=%d|case=%d|recipient=0|npc=%d|non_player_side=%d|acquired=%d|bag_slot=%d|item=3|live=%d|owner=%d|references=%d|logs=%d|data=%d|one=%d|second_loop=1|arena_released=1|tickets_cleared=1|whole_items=1|whole_actors=1|whole_arena=1|whole_connections=1|original_timer=1\n",
           guard_side,guard_case,guard_case%2,guard_case>=2,accepted,accepted?first_slot:-1,
           reward_items[3].use,reward_items[3].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX],
           references,reward_log_count,reward_data_count,reward_one_count);
''' + c[end:]
    c = prior.capacity.prior.payout.ticket.drop.factory.allocator.item.substitutions(profile, c)
    return (c.replace('GUARD_ACCEPT', '!(guard_case%2)' if profile == 'bismarck' else 'guard_case<2')
            .replace('ENTRY_FIELD', 'char_index' if profile == 'bismarck' else 'charaindex')
            .replace('WIN_SIDE', '-1' if profile == 'bismarck' else '0')
            .replace('CONNECTION_TYPE', 'GmsvSession' if profile == 'bismarck' else 'CONNECT')
            .replace('TIMER_EXPECTED', '1005' if profile == 'bismarck' else '1000')
            .replace('TIMER_DRAWS', '(guard_case%2==0)')
            .replace('TIMER_SENDS', '(guard_case%2==0)' if profile == 'bismarck' else '0')
            .replace('ONE_EXPECTED', 'accepted' if profile == 'bismarck' else '0'))


def side_native(profile, source, battle, event, root):
    native, has_lua = prior.cleanup_native(profile, source, battle, event, root)
    old = prior.negative_controls(profile)
    native = replace_once(native, old, old + '\n' + guard_controls(profile))
    for name in ('BATTLE_Finish', 'BATTLE_GetProfit', 'BATTLE_GetExpGold'):
        body = attack.definition(native, name)
        original = attack.definition(battle, name)
        if body != original:
            raise ValueError('original guard/settlement body drift ' + name)
        print(f'RECIPIENT_SIDE_SOURCE|{profile}|{name}|sha256={hashlib.sha256(body.encode()).hexdigest()}', flush=True)
    return native, has_lua


def validate_report(report):
    prior.validate_report(report)
    rows = {}
    for line in report.splitlines():
        if not line.startswith('ACTUAL|') or '|REAL_HEADER_RECIPIENT_SIDE|' not in line:
            continue
        parts = line.split('|')
        profile = parts[1]
        try:
            fields = dict(p.split('=', 1) for p in parts[3:])
            case = int(fields['case'])
            side = int(fields['side'])
            key = profile, side, case
            if profile not in ('gavin', 'bismarck') or case not in range(4) or side not in (0,1) or key in rows:
                raise ValueError('unknown/duplicate recipient-side witness')
            accepted = int(case % 2 == 0 if profile == 'bismarck' else case < 2)
            expected = dict(recipient=0, npc=case%2, non_player_side=int(case>=2),
                            acquired=accepted, item=3, live=accepted,
                            owner=0 if accepted else -1, references=accepted,
                            logs=accepted, data=accepted, one=accepted if profile=='bismarck' else 0)
            for name in ('second_loop', 'arena_released', 'tickets_cleared', 'whole_items',
                         'whole_actors', 'whole_arena', 'whole_connections', 'original_timer'):
                expected[name] = 1
            if any(int(fields[name]) != value for name,value in expected.items()):
                raise ValueError('recipient-side witness disagrees with original profile')
            if int(fields['bag_slot']) != (9 if accepted else -1):
                raise ValueError('recipient-side bag slot disagrees with actual original layout')
            rows[key] = fields
        except (KeyError, TypeError) as exc:
            raise ValueError('incomplete recipient-side witness') from exc
    if set(rows) != {(p,s,c) for p in ('gavin','bismarck') for s in range(2) for c in range(4)}:
        raise ValueError('missing recipient-side profile/case')
    if 'RESOLUTION|ORIGINAL_REAL_HEADER_RECIPIENT_SIDE_BOUNDED_PASS' not in report.splitlines():
        raise ValueError('missing recipient-side resolution')
    return rows


def main():
    soft,hard = resource.getrlimit(resource.RLIMIT_STACK)
    if soft != resource.RLIM_INFINITY and soft < 64*1024*1024:
        resource.setrlimit(resource.RLIMIT_STACK,(64*1024*1024,hard))
    attack.main(native_builder=side_native, extra_markers=(
        'REAL_HEADER_FINISH_DISPATCH|','REAL_HEADER_SAME_ITEM_CAPACITY|',
        'REAL_HEADER_TICKET_CLEANUP|','REAL_HEADER_RECIPIENT_SIDE|'))
    print('BOUNDARY|synthetic actor0 retag to ordinary NPC and side-type input; fixed time/rand; no natural NPC creation, reachable mismatched side, early server identity or real transport claim')
    print('RESOLUTION|ORIGINAL_REAL_HEADER_SAME_ITEM_CAPACITY_BOUNDED_PASS')
    print('RESOLUTION|ORIGINAL_REAL_HEADER_TICKET_CLEANUP_BOUNDED_PASS')
    print('RESOLUTION|ORIGINAL_REAL_HEADER_RECIPIENT_SIDE_BOUNDED_PASS')


if __name__ == '__main__':
    main()
