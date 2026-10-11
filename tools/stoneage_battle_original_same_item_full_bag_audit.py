"""Original second Loop/Finish capacity matrix, with synthetic bag fillers.

Retains the accepted predecessor unchanged. No natural item-master or early
server provenance claim follows from these controlled late-source executions.
"""
from tools import stoneage_battle_original_same_item_finish_audit as prior
from tools import stoneage_party_pet_original_attack_audit as attack


def matrix_controls(profile):
    c = prior.second_controls(profile)
    c = prior.replace_once(c, "  for(int with_item=0;with_item<2;with_item++){", """
  for(int capacity_case=0;capacity_case<3;capacity_case++){
  for(int with_item=0;with_item<2;with_item++){""")
    c = prior.replace_once(c, "   arena->use=1;arena->mode=BATTLE_MODE_FINISH;", """
   if(capacity_case){
     ITEM_SIZE=256;
     int filler=20;
     int capacity_limit=ITEM_LIMIT;
     demand(capacity_limit>CHAR_STARTITEMARRAY&&capacity_limit<=CHAR_MAXITEMHAVE,
            "original profile active capacity lies in native Char array");
     for(int box=CHAR_STARTITEMARRAY;box<capacity_limit;box++){
       if(capacity_case==2 && box==capacity_limit-1){
         demand(slots[0].indexOfExistItems[box]<0,"fixture final bag slot initially empty");
         continue;
       }
       if(ITEM_CHECKINDEX(slots[0].indexOfExistItems[box]))continue;
       demand(filler<256 && !reward_items[filler].use,"fixture filler valid unused item record");
       slots[0].indexOfExistItems[box]=filler;
       reward_items[filler].use=1;
       reward_items[filler].ITEM_FIELD.data[ITEM_ID]=1800+filler;
       reward_items[filler].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]=0;
       reward_items[filler].ITEM_FIELD.workint[ITEM_WORKOBJINDEX]=-1;
       ITEM_COUNT++;filler++;
     }
   }
   arena->use=1;arena->mode=BATTLE_MODE_FINISH;""")
    c = prior.replace_once(c, '''   demand(first_empty>=CHAR_STARTITEMARRAY&&first_empty<CHAR_MAXITEMHAVE,
          "same-item second Finish first genuine bag slot");''', '''   printf("CAPACITY_INPUT|case=%d|with_item=%d|slot=%d|active_limit=%d|array_limit=%d|live=%d\\n",
          capacity_case,with_item,first_empty,ITEM_LIMIT,CHAR_MAXITEMHAVE,ITEM_COUNT);fflush(stdout);
   demand(capacity_case==1 ? first_empty==-1 :
          first_empty>=CHAR_STARTITEMARRAY&&first_empty<CHAR_MAXITEMHAVE,
          "original bag capacity independently verified before second Finish");
   if(capacity_case==2)demand(first_empty==ITEM_LIMIT-1,
          "original scan reaches last remaining bag slot");
   if(!with_item)memcpy(baseline_items,reward_items,sizeof baseline_items);
   int capacity_input_count=ITEM_COUNT;''')
    c = prior.replace_once(c, '      memcpy(baseline_items,reward_items,sizeof baseline_items);', '')
    c = prior.replace_once(c, '      demand(reward_items[3].', '''      demand(!memcmp(baseline_items,reward_items,sizeof baseline_items)&&ITEM_COUNT==capacity_input_count,
             "no-loot original second Finish preserves entire registered item and filler pool");
      demand(reward_items[3].''')
    c = prior.replace_once(c, '''      baseline_actors[0].indexOfExistItems[first_empty]=3;
      baseline_items[3].''', '''      if(capacity_case==1){
        baseline_items[3].use=0;
        baseline_items[3].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]=-1;
        baseline_count--;
      }else{
      baseline_actors[0].indexOfExistItems[first_empty]=3;
      baseline_items[3].''')
    pool_check = next(line for line in prior.second_controls(profile).splitlines()
                      if line.startswith('      demand(!memcmp(baseline_items'))
    c = prior.replace_once(c, pool_check, '      }\n' + pool_check)
    c = prior.replace_once(c, '''      demand(reward_log_count==1&&settle_log_count==1,
             "same-item original second Finish issues original pickup log");''', '''      demand(reward_log_count==(capacity_case!=1)&&settle_log_count==(capacity_case!=1)&&
             reward_data_count==(capacity_case!=1)&&
             reward_one_count==((capacity_case!=1)&&ONE_EXPECTED),
             "original pickup and presentation counts match actual bag acceptance");
      for(int actor=0;actor<7;actor++)for(int box=0;box<CHAR_MAXITEMHAVE;box++)
        if(capacity_case==1)demand(slots[actor].indexOfExistItems[box]!=3,
             "released full-bag item has no remaining carried reference");
      demand(reward_items[3].use==(capacity_case!=1)&&
             reward_items[3].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]==(capacity_case==1?-1:0),
             "actual registered item final liveness and owner");''')
    start = c.index('      printf("REAL_HEADER_SAME_ITEM_FINISH|')
    end = c.index('   }\n   reward_phase=0;', start)
    c = c[:start] + r'''      printf("REAL_HEADER_SAME_ITEM_CAPACITY|case=%d|actor=%d|registered_item=3|recipient=0|bag_slot=%d|owner=%d|item_live=%d|released=%d|second_loop=1|original_finish=1|profit=1|exp_gold=1|whole_items=1|whole_actors=1|whole_arena=1|arena_released=1|logs=%d|data=%d|one=%d\n",
             capacity_case,positive_actor,first_empty,
             reward_items[3].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX],reward_items[3].use,
             capacity_case==1,reward_log_count,reward_data_count,reward_one_count);
''' + c[end:]
    c = prior.replace_once(c, '\n  memcpy(reward_items,loop_saved_items', '\n  }\n  memcpy(reward_items,loop_saved_items')
    c = prior.payout.ticket.drop.factory.allocator.item.substitutions(profile, c)
    # Audit snapshots only: keep expanded, complete-layout fixture copies off
    # the native stack. Each is overwritten before use, never a game variable.
    for declaration in ('Char loop_saved_actors[7];', 'Char baseline_actors[7];',
                        'BATTLE baseline_arena;',
                        'ITEM_Exists loop_saved_items[256];', 'ITEM_Exists baseline_items[256];',
                        'ITEM_exists loop_saved_items[256];', 'ITEM_exists baseline_items[256];'):
        if declaration in c:
            c = prior.replace_once(c, declaration, 'static ' + declaration)
    return c.replace('ONE_EXPECTED', '1' if profile == 'bismarck' else '0')


def capacity_native(profile, source, battle, event, root):
    native, has_lua = prior.same_item_native(profile, source, battle, event, root)
    native = prior.replace_once(native, prior.second_controls(profile), matrix_controls(profile))
    return native, has_lua


def validate_report(report):
    """Reject incomplete or inconsistent derived capacity witnesses."""
    rows = {}
    for line in report.splitlines():
        if not line.startswith('ACTUAL|') or '|REAL_HEADER_SAME_ITEM_CAPACITY|' not in line:
            continue
        parts = line.split('|')
        profile = parts[1]
        try:
            fields = dict(part.split('=', 1) for part in parts[3:])
            case = int(fields['case'])
            key = (profile, case)
            if key in rows or profile not in ('gavin', 'bismarck') or case not in (0, 1, 2):
                raise ValueError('duplicate or unknown capacity witness')
            expected = {
                'actor': 6, 'registered_item': 3, 'recipient': 0,
                'owner': -1 if case == 1 else 0,
                'item_live': int(case != 1), 'released': int(case == 1),
                'logs': int(case != 1), 'data': int(case != 1),
                'one': int(case != 1 and profile == 'bismarck'),
            }
            for name in ('second_loop', 'original_finish', 'profit', 'exp_gold',
                         'whole_items', 'whole_actors', 'whole_arena', 'arena_released'):
                expected[name] = 1
            if any(int(fields[name]) != value for name, value in expected.items()):
                raise ValueError('capacity result disagrees with original-source oracle')
            slot = int(fields['bag_slot'])
            if case == 1 and slot != -1 or case != 1 and slot < 0:
                raise ValueError('capacity slot disagrees with acceptance')
            rows[key] = fields
        except (KeyError, TypeError) as exc:
            raise ValueError('incomplete capacity witness') from exc
    if set(rows) != {(p, c) for p in ('gavin', 'bismarck') for c in range(3)}:
        raise ValueError('missing profile or capacity case')
    for profile in ('gavin', 'bismarck'):
        if int(rows[profile, 2]['bag_slot']) <= int(rows[profile, 0]['bag_slot']):
            raise ValueError('last-slot case did not reach a later slot')
        headers = [line for line in report.splitlines() if line.startswith('PROFILE|' + profile + '|')]
        if len(headers) != 1 or '|optimizations=O0,O2|' not in headers[0]:
            raise ValueError('missing paired optimization witness')
    if 'RESOLUTION|ORIGINAL_REAL_HEADER_SAME_ITEM_CAPACITY_BOUNDED_PASS' not in report.splitlines():
        raise ValueError('missing capacity resolution')
    return rows


def main():
    # Full original-header differential snapshots exceed the usual 8 MiB
    # stack on Bismarck at O0. This changes only the audit execution budget.
    import resource
    soft, hard = resource.getrlimit(resource.RLIMIT_STACK)
    required = 64 * 1024 * 1024
    if soft != resource.RLIM_INFINITY and soft < required:
        if hard != resource.RLIM_INFINITY and hard < required:
            raise RuntimeError('capacity audit requires a 64 MiB stack budget')
        resource.setrlimit(resource.RLIMIT_STACK, (required, hard))
    attack.main(native_builder=capacity_native, extra_markers=(
        'REAL_HEADER_FINISH_DISPATCH|', 'REAL_HEADER_DROP_TICKET|',
        'REAL_HEADER_DROP_PAYOUT|', 'REAL_HEADER_SAME_ITEM_CAPACITY|'))
    print('BOUNDARY|synthetic filler and drop master; late descendants; differential EXP/Exit oracle; no early server, real transport or modern engine claim')
    print('RESOLUTION|ORIGINAL_REAL_HEADER_SAME_ITEM_CAPACITY_BOUNDED_PASS')


if __name__ == '__main__':
    main()
