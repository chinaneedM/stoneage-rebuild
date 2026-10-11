"""Bounded original second Finish exceptional recipient/ticket cleanup.

Retains capacity predecessors. No game function body is edited: all scenario
changes below are explicit original-layout fixture inputs and typed collectors.
"""
import hashlib
import resource
import re
from tools import stoneage_battle_original_same_item_full_bag_audit as capacity
from tools import stoneage_party_pet_original_attack_audit as attack

NEGATIVE = r'''
 static ITEM_TYPE negative_saved_items[256],negative_expected_items[256];
 static Char negative_saved_actors[7],negative_expected_actors[7];
 static BATTLE negative_saved_arena,negative_expected_arena;
 memcpy(negative_saved_items,reward_items,sizeof negative_saved_items);
 memcpy(negative_saved_actors,slots,sizeof negative_saved_actors);
 negative_saved_arena=*arena;
 int negative_saved_count=ITEM_COUNT,negative_saved_size=ITEM_SIZE;
 int negative_saved_total=Total_BattleNum,negative_saved_phase=reward_phase;
 int negative_saved_transport=finish_transport_phase;
 int negative_saved_log=reward_log_count,negative_saved_data=reward_data_count;
 int negative_saved_one=reward_one_count,negative_saved_settle=settle_log_count;
 int negative_saved_actor=reward_expected_actor,negative_saved_slot=reward_expected_slot;
 for(int negative_case=0;negative_case<4;negative_case++){
  int recipient=negative_case==1?2:negative_case==2?-1:0;
  int expected_count=0,first_slot=-1;
  for(int with_ticket=0;with_ticket<2;with_ticket++){
   memcpy(reward_items,negative_saved_items,sizeof negative_saved_items);
   memcpy(slots,negative_saved_actors,sizeof negative_saved_actors);
   *arena=negative_saved_arena;ITEM_COUNT=negative_saved_count;ITEM_SIZE=negative_saved_size;
   for(int box=CHAR_STARTITEMARRAY;box<CHAR_MAXITEMHAVE;box++)slots[0].indexOfExistItems[box]=-1;
   arena->use=1;arena->mode=BATTLE_MODE_FINISH;arena->type=BATTLE_TYPE_P_vs_E;
   arena->winside=WIN_SIDE;arena->Side[0].type=BATTLE_S_TYPE_PLAYER;
   arena->Side[1].type=BATTLE_S_TYPE_ENEMY;
   for(int side=0;side<2;side++)for(int e=0;e<BATTLE_ENTRY_MAX;e++){
    arena->Side[side].Entry[e].ENTRY_FIELD=-1;
    for(int k=0;k<GETITEM_MAX;k++)arena->Side[side].Entry[e].getitem[k]=-1;
   }
   arena->Side[0].Entry[0].ENTRY_FIELD=recipient;
   arena->Side[1].Entry[0].ENTRY_FIELD=positive_actor;
   if(with_ticket){
    arena->Side[0].Entry[0].getitem[0]=3;
    if(negative_case==3)arena->Side[0].Entry[0].getitem[1]=3;
   }
   slots[0].workint[CHAR_WORKGETEXP]=slots[2].workint[CHAR_WORKGETEXP]=0;
   CHAR_setFlg(0,CHAR_ISDIE,negative_case==0);
   if(recipient>=0){
    slots[recipient].workint[CHAR_WORKBATTLEINDEX]=battle_at;
    slots[recipient].workint[CHAR_WORKBATTLEMODE]=BATTLE_CHARMODE_C_WAIT;
   }
   slots[positive_actor].workint[CHAR_WORKBATTLEINDEX]=battle_at;
   slots[positive_actor].workint[CHAR_WORKBATTLEMODE]=BATTLE_CHARMODE_C_WAIT;
   arena->CreateTime=900;arena->flgTime=0;
   memset(cleanup_connections,0,sizeof cleanup_connections);
   cleanup_timer_calls=cleanup_timer_draws=cleanup_nu_sends=0;cleanup_timer_phase=1;
   demand(CHAR_getInt(2,CHAR_WHICHTYPE)==CHAR_TYPEPET,"actual selected owned pet recipient input");
   first_slot=CHAR_findEmptyItemBox(0);
   demand(first_slot==CHAR_STARTITEMARRAY,"explicit empty bag fixture first slot");
   Total_BattleNum=1;reward_phase=negative_case==3?3:2;
   reward_expected_actor=0;reward_expected_slot=first_slot;
   reward_log_count=reward_data_count=reward_one_count=settle_log_count=0;
   finish_rs_count=finish_status_count=0;finish_transport_phase=1;
   int cleanup_ret=BATTLE_Loop();
   demand(cleanup_ret==1&&arena->use==0&&arena->mode==BATTLE_MODE_NONE&&Total_BattleNum==0,
          "actual exceptional second Loop Finish and DeleteBattle release");
   CONNECTION_TYPE expected_connections[8];memset(expected_connections,0,sizeof expected_connections);
   if(negative_case==0||negative_case==3)expected_connections[7].BDTime=TIMER_EXPECTED;
   demand(!memcmp(expected_connections,cleanup_connections,sizeof expected_connections)&&
          cleanup_timer_draws==TIMER_DRAWS&&cleanup_nu_sends==TIMER_SENDS&&
          cleanup_timer_calls==(negative_case==0||negative_case==3),
          "whole original native connection and original death timer oracle");
   for(int side=0;side<2;side++)for(int e=0;e<BATTLE_ENTRY_MAX;e++)for(int k=0;k<GETITEM_MAX;k++)
    demand(arena->Side[side].Entry[e].getitem[k]==-1,"original EntryInit clears all pending ticket slots");
   if(!with_ticket){
    memcpy(negative_expected_items,reward_items,sizeof negative_expected_items);
    memcpy(negative_expected_actors,slots,sizeof negative_expected_actors);
    negative_expected_arena=*arena;expected_count=ITEM_COUNT;
    demand(!memcmp(negative_saved_items,reward_items,sizeof negative_saved_items)&&ITEM_COUNT==negative_saved_count,
           "no-ticket control preserves whole actual registered item pool");
   }else{
    if(negative_case==3){
     negative_expected_items[3].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]=0;
     negative_expected_items[3].ITEM_FIELD.workint[ITEM_WORKOBJINDEX]=-1;
     negative_expected_actors[0].indexOfExistItems[first_slot]=3;
     negative_expected_actors[0].indexOfExistItems[first_slot+1]=3;
    }else{
     negative_expected_items[3].use=0;
     negative_expected_items[3].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]=-1;
     expected_count--;
    }
    demand(!memcmp(negative_expected_items,reward_items,sizeof negative_expected_items)&&ITEM_COUNT==expected_count,
           "whole registered item pool and live count exceptional ticket oracle");
    demand(!memcmp(negative_expected_actors,slots,sizeof negative_expected_actors),
           "all seven original Char differential cleanup oracle");
    demand(!memcmp(&negative_expected_arena,arena,sizeof negative_expected_arena),
           "complete original BATTLE differential cleanup oracle");
    demand(reward_log_count==(negative_case==3?2:0)&&settle_log_count==reward_log_count&&
           reward_data_count==(negative_case==3?1:0)&&reward_one_count==ONE_EXPECTED,
           "exact rejected or duplicate original reward presentation counts");
    int references=0;
    for(int actor=0;actor<7;actor++)for(int box=0;box<CHAR_MAXITEMHAVE;box++)
     if(slots[actor].indexOfExistItems[box]==3)references++;
    demand(references==(negative_case==3?2:0),"whole actor carried-reference multiplicity oracle");
    printf("REAL_HEADER_TICKET_CLEANUP|case=%d|recipient=%d|item=3|live=%d|owner=%d|references=%d|logs=%d|data=%d|one=%d|second_loop=1|arena_released=1|tickets_cleared=1|whole_items=1|whole_actors=1|whole_arena=1|whole_connections=1|original_timer=ORIGINAL_TIMER\n",
           negative_case,recipient,reward_items[3].use,
           reward_items[3].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX],references,
           reward_log_count,reward_data_count,reward_one_count);
   }
   reward_phase=0;finish_transport_phase=0;cleanup_timer_phase=0;
  }
 }
 memcpy(reward_items,negative_saved_items,sizeof negative_saved_items);
 memcpy(slots,negative_saved_actors,sizeof negative_saved_actors);
 *arena=negative_saved_arena;ITEM_COUNT=negative_saved_count;ITEM_SIZE=negative_saved_size;
 Total_BattleNum=negative_saved_total;reward_phase=negative_saved_phase;
 finish_transport_phase=negative_saved_transport;
 reward_log_count=negative_saved_log;reward_data_count=negative_saved_data;
 reward_one_count=negative_saved_one;settle_log_count=negative_saved_settle;
 reward_expected_actor=negative_saved_actor;reward_expected_slot=negative_saved_slot;
'''


def negative_controls(profile):
    c = capacity.prior.payout.ticket.drop.factory.allocator.item.substitutions(profile, NEGATIVE)
    return c.replace('ENTRY_FIELD', 'char_index' if profile == 'bismarck' else 'charaindex').replace(
        'WIN_SIDE', '-1' if profile == 'bismarck' else '0').replace(
        'ONE_EXPECTED', '(negative_case==3?2:0)' if profile == 'bismarck' else '0').replace(
        'CONNECTION_TYPE', 'GmsvSession' if profile == 'bismarck' else 'CONNECT').replace(
        'TIMER_EXPECTED', '0' if profile == 'bismarck' else '(negative_case==0?1010:1000)').replace(
        'TIMER_DRAWS', '0' if profile == 'bismarck' else '(negative_case==0||negative_case==3)').replace(
        'TIMER_SENDS', '0').replace('ORIGINAL_TIMER', '0' if profile == 'bismarck' else '1')


def cleanup_native(profile, source, battle, event, root):
    native, has_lua = capacity.capacity_native(profile, source, battle, event, root)
    path = attack.LAYOUTS[profile] / ('net/net.c' if profile == 'bismarck' else 'net.c')
    net_source = attack.pp_file(profile, root, path)
    typename = 'GmsvSession' if profile == 'bismarck' else 'CONNECT'
    match = re.search(r'typedef\s+struct\s+tag' + typename + r'\s*\{.*?\}\s*' + typename + r'\s*;', net_source, re.S)
    if not match:
        raise ValueError('original native connection type missing')
    timer = attack.definition(net_source, 'CheckDefBTime')
    extra = '#pragma push_macro("CheckDefBTime")\n#undef CheckDefBTime\n#include <sys/socket.h>\n#include <netinet/in.h>\n#include <sys/time.h>\n'
    if profile == 'bismarck':
        extra += '#include "tcp_buffer.h"\n'
    extra += match[0] + '\n'
    extra += f'static {typename} cleanup_connections[8];{typename} *Connect=cleanup_connections;\n'
    extra += 'static int cleanup_timer_calls,cleanup_timer_draws,cleanup_nu_sends,cleanup_timer_phase;\n'
    extra += 'static time_t cleanup_fixed_time(time_t *out){if(out)abort();return 1000;}\n'
    extra += 'static int cleanup_fixed_rand(void){cleanup_timer_draws++;return 0;}\n'
    if profile != 'bismarck':
        extra += 'void lssproto_NU_send(int fd,int value){if(fd!=7||value!=-12)abort();cleanup_nu_sends++;}\n'
        extra += '#pragma push_macro("time")\n#pragma push_macro("rand")\n#undef time\n#undef rand\n#define time cleanup_fixed_time\n#define rand cleanup_fixed_rand\n' + timer + '\n#undef rand\n#undef time\n#pragma pop_macro("rand")\n#pragma pop_macro("time")\n'
    else:
        # The pinned default-preprocessed body references undeclared delayTime.
        # Do not invent a value or enable another feature profile to hide it.
        if 'delayTime' not in timer or re.search(r'\b(?:int|unsigned)\s+delayTime\b', timer):
            raise ValueError('recorded Bismarck original timer compile boundary drift')
        extra += 'BOOL CheckDefBTime(int actor,int fd,unsigned int low,unsigned int duration,unsigned int add){if(actor!=0||fd!=7||low!=900||duration!=0||add!=(CHAR_getFlg(actor,CHAR_ISDIE)?10:0))abort();return TRUE;}\n'
        print('OPEN|bismarck|original_default_CheckDefBTime_undeclared_delayTime|typed_timer_fixture_only=1', flush=True)
    print(f'CLEANUP_SOURCE|{profile}|CheckDefBTime|sha256={hashlib.sha256(timer.encode()).hexdigest()}|connection_type_sha256={hashlib.sha256(match[0].encode()).hexdigest()}', flush=True)
    for helper in ('getCharloops', 'GmsvServer_NU_send', 'lssproto_NU_send'):
        try:
            old_helper = attack.definition(native, helper)
        except ValueError:
            continue
        native = capacity.prior.replace_once(native, old_helper, '')
    old_timer = attack.definition(native, 'CheckDefBTime')
    extra += old_timer.replace('CheckDefBTime(', 'cleanup_inherited_timer(', 1) + '\n'
    extra += 'BOOL cleanup_dispatch(int actor,int fd,unsigned int low,unsigned int duration,unsigned int add){if(cleanup_timer_phase){cleanup_timer_calls++;return CheckDefBTime(actor,fd,low,duration,add);}return cleanup_inherited_timer(actor,fd,low,duration,add);}\n#pragma pop_macro("CheckDefBTime")\n'
    native = capacity.prior.replace_once(native, old_timer, extra)
    native = '#define CheckDefBTime cleanup_dispatch\n' + native
    old = capacity.matrix_controls(profile)
    native = capacity.prior.replace_once(native, old, old + '\n' + negative_controls(profile))
    # A new audit-only transport/log phase observes two real bag aliases without
    # weakening the existing one-item collector or replacing game logic.
    for name, injected in {
        'CHAR_sendItemData': '''if(reward_phase==3){
 if(actor!=0||count!=2||indices[0]!=reward_expected_slot||indices[1]!=reward_expected_slot+1||
    slots[0].indexOfExistItems[indices[0]]!=3||slots[0].indexOfExistItems[indices[1]]!=3)abort();
 reward_data_count++;return TRUE;}''',
        'CHAR_sendItemDataOne': '''if(reward_phase==3){
 if(actor!=0||reward_one_count>=2||slot!=reward_expected_slot+reward_one_count||
    slots[0].indexOfExistItems[slot]!=3)abort();reward_one_count++;return TRUE;}''',
        'LogItem': '''if(reward_phase==3){
 if(item!=3||id!=1||strcmp(code,"factory-bounded")||strcmp(itemname,"Factory")||!name||!key||
    strcmp(cause,"BattleGet(战斗後所得的道具)")||floor!=slots[0].data[CHAR_FLOOR]||
    x!=slots[0].data[CHAR_X]||y!=slots[0].data[CHAR_Y])abort();
 settle_log_count++;reward_log_count++;return;}''',
    }.items():
        old_body = attack.definition(native, name)
        new_body = old_body.replace('{', '{\n' + injected, 1)
        native = capacity.prior.replace_once(native, old_body, new_body)
    for name in ('BATTLE_DeleteItem', 'BATTLE_DeleteBattle'):
        body = attack.definition(native, name)
        original = attack.definition(battle, name)
        if body != original:
            raise ValueError('original cleanup body drift ' + name)
        # The inherited body uses its original raw/preprocessed profile form.
        print(f'CLEANUP_SOURCE|{profile}|{name}|native_sha256={hashlib.sha256(body.encode()).hexdigest()}|preprocessed_sha256={hashlib.sha256(original.encode()).hexdigest()}', flush=True)
    return native, has_lua


def validate_report(report):
    """Require every profile/case and exact alias/release evidence."""
    capacity.validate_report(report)
    rows = {}
    for line in report.splitlines():
        if not line.startswith('ACTUAL|') or '|REAL_HEADER_TICKET_CLEANUP|' not in line:
            continue
        parts = line.split('|')
        profile = parts[1]
        try:
            fields = dict(part.split('=', 1) for part in parts[3:])
            case = int(fields['case'])
            key = profile, case
            if profile not in ('gavin', 'bismarck') or case not in range(4) or key in rows:
                raise ValueError('unknown or duplicate cleanup witness')
            duplicate = case == 3
            expected = dict(recipient=2 if case == 1 else -1 if case == 2 else 0,
                            item=3, live=int(duplicate), owner=0 if duplicate else -1,
                            references=2 if duplicate else 0, logs=2 if duplicate else 0,
                            data=int(duplicate), one=2 if duplicate and profile == 'bismarck' else 0,
                            original_timer=int(profile == 'gavin'))
            for name in ('second_loop', 'arena_released', 'tickets_cleared',
                         'whole_items', 'whole_actors', 'whole_arena', 'whole_connections'):
                expected[name] = 1
            if any(int(fields[name]) != value for name, value in expected.items()):
                raise ValueError('cleanup witness disagrees with complete state oracle')
            rows[key] = fields
        except (KeyError, TypeError) as exc:
            raise ValueError('incomplete cleanup witness') from exc
    if set(rows) != {(p, c) for p in ('gavin', 'bismarck') for c in range(4)}:
        raise ValueError('missing cleanup profile or case')
    if 'RESOLUTION|ORIGINAL_REAL_HEADER_TICKET_CLEANUP_BOUNDED_PASS' not in report.splitlines():
        raise ValueError('missing cleanup resolution')
    return rows


def main():
    soft, hard = resource.getrlimit(resource.RLIMIT_STACK)
    if soft != resource.RLIM_INFINITY and soft < 64 * 1024 * 1024:
        resource.setrlimit(resource.RLIMIT_STACK, (64 * 1024 * 1024, hard))
    attack.main(native_builder=cleanup_native, extra_markers=(
        'REAL_HEADER_FINISH_DISPATCH|', 'REAL_HEADER_SAME_ITEM_CAPACITY|',
        'REAL_HEADER_TICKET_CLEANUP|'))
    print('BOUNDARY|synthetic recipient/ticket and empty bag fixtures; Bismarck typed timer fixture default source compile fault; late descendants; no natural duplicate/invalid ticket reachability or early server identity')
    print('RESOLUTION|ORIGINAL_REAL_HEADER_SAME_ITEM_CAPACITY_BOUNDED_PASS')
    print('RESOLUTION|ORIGINAL_REAL_HEADER_TICKET_CLEANUP_BOUNDED_PASS')


if __name__ == '__main__':
    main()
