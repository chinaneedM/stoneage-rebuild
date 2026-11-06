"""Continue the authenticated WORLD36 score fixture through the original capture tail."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import struct

from tools.stoneage_battle_recovery_source import verify_archive
from tools.stoneage_capture_roster_source import (
    ACTOR, CHAR_TABLE, PET_START, PET_END, STACK, WILD, WORLD35, replay,
)
from tools.stoneage_savepoint_item_source import EXE_SHA, original_image
from tools.stoneage_scene33_source_pair import ARCHIVE_SHA, ROOT, sha
from tools.stoneage_world34_field_item_replay import CHAR_STRIDE, ITEMS_OFFSET, WORK_OFFSET

REPORT = ROOT / 'research/recovered/STONEAGE-STAGE-A-WORLD37-R2C-COMPILED-CAPTURE-TAIL-REPLAY-R1.json'
R2B = ROOT / 'research/recovered/STONEAGE-STAGE-A-WORLD37-R2B-COMPILED-CAPTURE-REQUIRED-ITEMS-R1.json'
TABLE, TABLE_SIZE = 0x58cd60, 128 * 64
ITEMS, BATTLE = 0x700000, 0x705000
ITEM_STRIDE = 0x784
ACTIVE_ITEM_COUNT = 0x61b630
CHECK_RETURN = STACK + 0x4000
CAPTURE_RETURN = STACK + 0x8000
INITIAL_COUNT = 7
SYMBOLS = {
    '_BATTLE_CaptureItemCheck': 0x537d30, '_BATTLE_CaptureItemDelAll': 0x537e50,
    '_BATTLE_Capture': 0x5380e0, '__BATTLE_Exit': 0x518b20,
    '__CHAR_DelItem': 0x433ab0, '_CHAR_endCharOneArray': 0x42fa60,
    '__ITEM_endExistItemsOne': 0x4f72a0,
    '_BATTLE_No2Index': 0x517760,
}


def char(index):
    return CHAR_TABLE + index * CHAR_STRIDE


def int_field(index, key):
    return char(index) + 4 + 4 * key


def seat(index):
    side, slot = divmod(index, 10)
    return BATTLE + 0xac + side * 0x174 + slot * 0x24


def item_address(index):
    return ITEMS + index * ITEM_STRIDE


class Tail:
    """Guest state and an observation-only write trace for the selected original windows."""

    code = (
        (0x537d30, 0x5380e0), (0x538443, 0x5385e8), (0x518b20, 0x51913e),
        (0x42fa60, 0x42fb5b), (0x42e670, 0x42e67a), (0x433ab0, 0x433c40),
        (0x43e2a0, 0x43e2d6), (0x43e3b6, 0x43e3c0), (0x43f040, 0x43f130),
        (0x4f72a0, 0x4f7460), (0x4f7500, 0x4f7640),
        (0x4f76e0, 0x4f7777), (0x4f7fb0, 0x4f8065),
    )
    data = ((TABLE, TABLE + TABLE_SIZE), (0x5945c0, 0x594800), (0x594dd8, 0x594df8), (0x5a49c0, 0x5a4a20),
            (0x5a7008, 0x5a7040), (0x5a7b98, 0x5a8004))
    endpoint = 0x5385e8
    entry_code = ((0x5380e0, 0x5381b9), (0x5381fc, 0x5383c3), (0x5385e8, 0x5389ca),
                  (0x517760, 0x517810))
    entry_data = ((0x5a7ffc, 0x5a8004),)
    stubs = {
        0x417f40: 'item_log_sink', 0x418210: 'pet_log_sink',
        0x473740: 'inventory_update_sink',
    }
    call_sites = {
        0x5383d6: 'create_pet', 0x538579: 'delete_required_items', 0x538099: 'delete_inventory_slot',
        0x53858b: 'read_capture_count', 0x5385b8: 'write_capture_count',
        0x5385e3: 'battle_exit', 0x519134: 'release_wild_record',
    }

    def __init__(self, key, actor_items, *, wild_seated=True, battle_active=True, from_entry=False,
                 actor_work_146=0, target_work_83=1):
        self.key = key
        self.actor_items = actor_items
        self.wild_seated = wild_seated
        self.battle_active = battle_active
        self.from_entry = from_entry
        self.actor_work_146 = actor_work_146
        self.target_work_83 = target_work_83
        if from_entry:
            self.code = self.code + self.entry_code
            self.data = self.data + self.entry_data
            self.endpoint = CAPTURE_RETURN
        # Wild item references include the first and last slots of both original arrays.
        self.wild_items = [(0x4c0, 3, 6001), (0x50c, 4, 6002),
                           (0x510, 5, 6003), (0x584, 6, 6004)]
        self.calls = []
        self.writes = []
        self.entry_milestones = []

    def get(self, address, count=1):
        return list(struct.unpack(f'<{count}i', self.cpu.mem_read(address, 4 * count)))

    def put(self, address, *values):
        self.cpu.mem_write(address, struct.pack(f'<{len(values)}i', *values))

    def initialize(self, cpu):
        from unicorn import UC_HOOK_MEM_WRITE, UC_PROT_READ, UC_PROT_WRITE

        self.cpu = cpu
        for address, size in ((ITEMS, 0x4000), (BATTLE, 0x1000), (0x2030000, 0x2000)):
            cpu.mem_map(address, size, UC_PROT_READ | UC_PROT_WRITE)
        self.put(0x61b640, ITEMS)
        self.put(0x61b650, 7)
        self.put(0x61b630, len(self.actor_items) + len(self.wild_items))
        self.put(0x2030410, 1)
        self.put(0x2031a90, BATTLE)
        self.put(0x2030860, BATTLE + 0x500)
        self.put(0x2031a80, BATTLE + 0x800)
        self.put(BATTLE, int(self.battle_active))
        for i in range(20):
            self.put(seat(i), {2: ACTOR, 17: WILD if self.wild_seated else -1}.get(i, -1))
        self.put(seat(17) + 8, 73)
        self.put(int_field(ACTOR, 44), INITIAL_COUNT)
        self.put(int_field(WILD, 53), self.key)
        if self.from_entry:
            self.put(int_field(ACTOR, 8), 35)
            self.put(char(ACTOR) + WORK_OFFSET + 4 * 34, 100)
            self.put(char(ACTOR) + WORK_OFFSET + 4 * 146, self.actor_work_146)
            self.put(char(WILD) + WORK_OFFSET + 4 * 13, 100)
            self.put(char(WILD) + WORK_OFFSET + 4 * 83, self.target_work_83)
        self.put(char(ACTOR) + ITEMS_OFFSET, *([-1] * 20))
        self.put(char(WILD) + ITEMS_OFFSET, *([-1] * 50))
        for slot, (index, item_id) in self.actor_items.items():
            self.put(char(ACTOR) + ITEMS_OFFSET + 4 * slot, index)
            self.put(item_address(index), 1, item_id)
        for offset, index, item_id in self.wild_items:
            self.put(char(WILD) + offset, index)
            self.put(item_address(index), 1, item_id)
        self.tracked = {
            int_field(ACTOR, 44): 'actor_int_44',
            seat(17): 'wild_seat_17_character',
            seat(17) + 8: 'wild_seat_17_word_8',
            char(WILD): 'wild_record_in_use',
            ACTIVE_ITEM_COUNT: 'active_item_count',
            **{item_address(i): f'item_record_{i}_in_use' for i in range(7)},
            **{char(ACTOR) + ITEMS_OFFSET + 4 * i: f'actor_item_slot_{i}' for i in range(20)},
            **{char(WILD) + ITEMS_OFFSET + 4 * i: f'wild_item_slot_{i}' for i in range(50)},
        }
        self.before = self.snapshot()
        cpu.hook_add(UC_HOOK_MEM_WRITE, self.watch_write)

    def snapshot(self):
        return {
            'actor_int_44': self.get(int_field(ACTOR, 44))[0],
            'battle_character_indices': [self.get(seat(i))[0] for i in range(20)],
            'wild_seat_word_8': self.get(seat(17) + 8)[0],
            'wild_record_in_use': self.get(char(WILD))[0],
            'actor_item_slots': self.get(char(ACTOR) + ITEMS_OFFSET, 20),
            'wild_item_slots': self.get(char(WILD) + ITEMS_OFFSET, 50),
            'live_item_records': [i for i in range(7) if self.get(item_address(i))[0]],
            'active_item_count': self.get(ACTIVE_ITEM_COUNT)[0],
        }

    def watch_write(self, machine, _access, address, size, value, _context):
        from unicorn.x86_const import UC_X86_REG_EIP

        if address in self.tracked:
            if size != 4:
                raise ValueError('unexpected capture fixture write width')
            signed, = struct.unpack('<i', struct.pack('<I', value & 0xffffffff))
            self.writes.append([machine.reg_read(UC_X86_REG_EIP), self.tracked[address],
                                self.get(address)[0], signed])

    def observe(self, address):
        from unicorn.x86_const import UC_X86_REG_ESP

        if address in self.call_sites:
            self.calls.append([address, self.call_sites[address]])
        if address == 0x538099:
            # The call instruction has not yet pushed its return address.
            stack = self.cpu.reg_read(UC_X86_REG_ESP)
            self.calls[-1].append(self.get(stack + 8, 4))
        if self.from_entry and address in (0x5380e0, 0x53829e, 0x53818e, 0x5386d9, 0x5389ca, 0x5381b9,
                                          0x5381fc, 0x5385e8):
            self.entry_milestones.append(address)

    def prepare_score_frame(self, bp):
        self.put(bp + 8, 0)  # Original _BATTLE_Capture battle-index argument.

    def prepare_entry_frame(self, sp):
        from unicorn.x86_const import UC_X86_REG_ESP

        self.put(sp, CAPTURE_RETURN, 0, 2, 17)
        self.cpu.reg_write(UC_X86_REG_ESP, sp)
        return SYMBOLS['_BATTLE_Capture'], CAPTURE_RETURN

    def probe_requirement(self):
        from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_EIP, UC_X86_REG_ESP

        sp = STACK + 0x4700
        self.put(sp, CHECK_RETURN, ACTOR, WILD)
        self.cpu.reg_write(UC_X86_REG_ESP, sp)
        self.cpu.emu_start(SYMBOLS['_BATTLE_CaptureItemCheck'], CHECK_RETURN, count=16000)
        if (self.cpu.reg_read(UC_X86_REG_EIP), self.cpu.reg_read(UC_X86_REG_ESP)) != (CHECK_RETURN, sp + 4):
            raise ValueError('original requirement helper did not return')
        self.requirement_return = self.cpu.reg_read(UC_X86_REG_EAX)
        if self.requirement_return not in (0, 1) or self.snapshot() != self.before or self.writes:
            raise ValueError('original requirement probe changed fixture state or returned unexpected value')

    def result(self):
        end = self.get(0x2030860)[0]
        return {'before': self.before, 'after': self.snapshot(), 'call_sites': self.calls,
                'guest_writes': self.writes, 'standalone_requirement_helper_return': self.requirement_return,
                'entry_milestones': self.entry_milestones,
                'guest_battle_buffer': bytes(self.cpu.mem_read(BATTLE + 0x500, end - BATTLE - 0x500)).decode('ascii')
                if end > BATTLE + 0x500 else ''}


def derive(archive, exe):
    import unicorn

    raw = exe.read_bytes()
    _, take, _, _, found = original_image(raw, SYMBOLS)
    previous = json.loads(WORLD35.read_bytes())
    source, = [row for row in previous['source_members'] if row['target'] == 'gmsv/gmsv.exe']
    if (source['member_sha256'], previous['archive_sha256']) != (EXE_SHA, ARCHIVE_SHA):
        raise ValueError('original capture source pins changed')
    verify_archive(archive, source, raw)
    previous_conditions = json.loads(R2B.read_bytes())
    prior = previous_conditions['original_condition_table']
    table_bytes = take(TABLE, TABLE_SIZE)
    if sha(table_bytes) != prior['raw_table_sha256']:
        raise ValueError('original compiled requirement table differs')
    condition_rows = {}
    for row in prior['rows']:
        index = row['source_record_index']
        record = table_bytes[64 * index:64 * (index + 1)]
        key, *items = struct.unpack('<16i', record)
        required = items[:items.index(-1)] if -1 in items else items
        if (key, required, sha(record)) != (
            row['char_int_key_53_value'], row['required_item_id_candidates'], row['record_sha256'],
        ):
            raise ValueError('compiled requirement row projection differs')
        condition_rows[key] = required
    table_sources = {row['item_id']: row['presence'] for row in previous_conditions['original_item_id_crosswalk']}
    full = [3, 4, 5, 6, 7]
    holes = [3, 4, -1, 6, -1]
    present = [3, 4, 6]
    single = {7: (0, 20219), 11: (1, 20219), 14: (2, 1690)}
    triple = {0: (0, 1692), 7: (1, 1690), 19: (2, 1691)}
    cases = {
        'no_compiled_requirement': (1053, single, holes, present, {}, {}),
        'duplicate_required_item_slots': (961, single, holes, present, {}, {}),
        'three_distinct_required_items': (1105, triple, holes, present, {}, {}),
        'missing_requirement_diagnostic': (1105, {7: (1, 1690)}, holes, present, {}, {}),
        'comparison_equal': (961, single, holes, present, {'modifier': 0}, {}),
        'full_roster': (961, single, full, full, {}, {}),
        'exhausted_pet_partition': (961, single, holes, list(range(PET_START, PET_END)), {}, {}),
        'wild_not_seated': (1053, single, holes, present, {}, {'wild_seated': False}),
        'inactive_battle': (1053, single, holes, present, {}, {'battle_active': False}),
        'entry_no_compiled_requirement': (1053, single, holes, present, {'level': 35, 'hp_mp': (25, 20)},
                                          {'from_entry': True}),
        'entry_three_required_items': (1105, triple, holes, present, {'level': 35, 'hp_mp': (25, 20)},
                                       {'from_entry': True}),
        'entry_missing_required_items': (1105, {7: (1, 1690)}, holes, present,
                                         {'level': 35, 'hp_mp': (25, 20)}, {'from_entry': True}),
        'entry_full_roster': (961, single, full, full, {'level': 35, 'hp_mp': (25, 20)}, {'from_entry': True}),
        'entry_exhausted_pet_partition': (961, single, holes, list(range(PET_START, PET_END)),
                                          {'level': 35, 'hp_mp': (25, 20)}, {'from_entry': True}),
        'entry_target_at_owner_level_plus_five': (1105, triple, holes, present,
                                                 {'level': 40, 'hp_mp': (25, 20)}, {'from_entry': True}),
        'entry_target_above_owner_level_plus_five': (1105, triple, holes, present,
                                                    {'level': 41, 'hp_mp': (25, 20)}, {'from_entry': True}),
        'entry_owner_work_146_bypasses_level_guard': (1105, triple, holes, present,
                                                     {'level': 41, 'hp_mp': (25, 20)},
                                                     {'from_entry': True, 'actor_work_146': 1}),
        'entry_target_work_83_zero': (1105, triple, holes, present, {'level': 35, 'hp_mp': (25, 20)},
                                     {'from_entry': True, 'target_work_83': 0}),
    }
    result = {}

    def run_case(key, inventory, roster, pool, score_options, fixture_options):
        tail = Tail(key, inventory, **fixture_options)
        trace = replay(take, roster, pool, tail=tail, **score_options)
        score_executed = not tail.from_entry or 0x5389ca in trace['tail']['entry_milestones']
        created = trace['created_character']
        return {
            'target_key_53': key, 'compiled_required_item_ids': condition_rows.get(key, []),
            'initial_actor_item_ids_by_slot': [[slot, i, item] for slot, (i, item) in sorted(inventory.items())],
            'initial_wild_seated': tail.wild_seated, 'initial_battle_active': tail.battle_active,
            'started_at_original_function_entry': tail.from_entry,
            'entry_actor_work_146': tail.actor_work_146 if tail.from_entry else None,
            'entry_target_work_83': tail.target_work_83 if tail.from_entry else None,
            'initial_pet_pool_used': pool, 'score_modifier': score_options.get('modifier', 1),
            'modifier_after': trace['modifier_after'],
            'target_level': score_options.get('level', 1008),
            'score': trace['score'] if score_executed else None, 'capture_result_flag': trace['result_flag'],
            'created_character': created,
            'created_record_in_use': tail.get(char(created))[0] if created >= 0 else None,
            'created_record_type': trace['pet']['type'] if created >= 0 else None,
            'created_record_owner': trace['pet']['owner_work_83'] if created >= 0 else None,
            'roster_before': trace['roster_before'],
            'roster_after': trace['roster_after'], 'endpoint': trace['endpoint'],
            'fixture_call_counts': trace['fixture_call_counts'], **trace['tail'],
        }
    for name, options in cases.items():
        result[name] = run_case(*options)
    requirement_replays = []
    for key, required in condition_rows.items():
        inventory = {3 + i * 5: (i, item) for i, item in enumerate(required)}
        settings = (holes, present, {'level': 35, 'hp_mp': (25, 20)}, {'from_entry': True})
        requirement_replays.append({
            'target_key_53': key, 'compiled_item_ids': required,
            'item_table_presence': [table_sources[item] for item in required],
            'complete': run_case(key, inventory, *settings),
            'missing_cases': [
                {'omitted_item_id': omitted,
                 'trace': run_case(key, {s: pair for s, pair in inventory.items() if pair[1] != omitted}, *settings)}
                for omitted in required
            ],
        })
    return {
        'schema': 'stoneage.world37.r2c.compiled_capture_success_tail_replay.r1',
        'source_archive_sha256': ARCHIVE_SHA, 'source_exe_sha256': EXE_SHA, 'source_member': source,
        'emulator_version': unicorn.__version__, 'verified_original_coff_symbols': found,
        'extra_code_windows': [[a, b, sha(take(a, b-a))] for a, b in Tail.code],
        'extra_data_windows': [[a, b, sha(take(a, b-a))] for a, b in Tail.data],
        'function_entry_extra_code_windows': [[a, b, sha(take(a, b-a))] for a, b in Tail.entry_code],
        'function_entry_extra_data_windows': [[a, b, sha(take(a, b-a))] for a, b in Tail.entry_data],
        'new_stub_boundaries': Tail.stubs, 'cases': result, 'compiled_requirement_replays': requirement_replays,
        'fixture_first_instruction': 0x5389ca, 'successful_stop_before_instruction': Tail.endpoint,
        'function_entry_first_instruction': SYMBOLS['_BATTLE_Capture'],
        'function_entry_guest_return_address': CAPTURE_RETURN,
        'entry_fixture': {'battle_index': 0, 'actor_seat': 2, 'target_seat': 17, 'actor_level': 35,
                          'actor_work_34': 100, 'target_work_13': 100, 'target_work_83': 1,
                          'actor_work_146': 0, 'random_fixture_value': 0},
        'requirement_probe_linked_through_original_dispatcher': False,
        'standalone_server_process_started': False, 'network_messages_delivered': False,
        'save_executed': False, 'historical_official_deployment_verified': False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('gmsv', type=Path)
    args = parser.parse_args()
    print(json.dumps(derive(args.archive, args.gmsv), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
