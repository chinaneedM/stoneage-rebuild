"""Replay original mixed25 capture comparison, pet allocation and owner binding."""

import argparse
from collections import Counter
import json
from pathlib import Path
import struct

from tools.stoneage_battle_item_gate_source import map_windows
from tools.stoneage_battle_recovery_source import verify_archive
from tools.stoneage_capture_item_source import REPORT as WORLD35
from tools.stoneage_recovery_callback_replay import X87_RESET_CONTROL
from tools.stoneage_savepoint_item_source import EXE_SHA, original_image
from tools.stoneage_scene33_source_pair import ARCHIVE_SHA, ROOT, sha
from tools.stoneage_world34_field_item_replay import CHAR_STRIDE, WORK_OFFSET

REPORT = ROOT / 'research/recovered/STONEAGE-STAGE-A-WORLD36-CAPTURE-ROSTER-SOURCE-R1.json'
SYMBOLS = {
    '_BATTLE_Capture': 0x5380e0, '_PET_createPetFromCharaIndex': 0x468de0,
    '_CHAR_getDefaultChar': 0x448df0, '_CHAR_getCharPetElement': 0x42ec10,
    '_CHAR_initCharOneArray': 0x42f630, '_CHAR_setMaxExpFromLevel': 0x433750,
    '_CHAR_setPetUniCode': 0x431fa0, '_CHAR_setCharPet': 0x432230,
    '__CHAR_setChar': 0x42df10, '__CHAR_setWorkInt': 0x42de30,
    '__CHAR_complianceParameter': 0x438840,
}
CODE = (
    (0x5389ca, 0x538a9e), (0x5381b9, 0x5381fc), (0x5383c3, 0x538443),
    (0x468de0, 0x4693f6), (0x55ad60, 0x55ad8d), (0x448df0, 0x448f8d),
    (0x42ec10, 0x42ed00), (0x42db90, 0x42dbac), (0x42dc30, 0x42deda),
    (0x42df10, 0x42dfbf), (0x42f0a0, 0x42f189), (0x42f630, 0x42f8f6),
    (0x431fa0, 0x43222b), (0x432230, 0x4322fb), (0x433750, 0x4337c9),
    (0x438840, 0x4398e0), (0x4fa990, 0x4fb940), (0x42d960, 0x42d998),
    (0x449030, 0x449080), (0x42ea10, 0x42eaa5), (0x42e190, 0x42e208), (0x42e2e0, 0x42e3b0), (0x4f71b0, 0x4f7220),
)
ACTOR, WILD = 1, 12
PET_START, PET_END = 3, 12
CHAR_TABLE, STACK = 0x710000, 0x800000
ROSTER_OFFSET, STRINGS_OFFSET = 0x1cbc, 0x1fc
SUCCESS_END, FAILURE_END = 0x538443, 0x5381fc
TEMPLATE_TABLE, TEMPLATE_COUNT, TEMPLATE_ID = 0x570a60, 53, 31010
FALLBACK = 0x570dc0
NAMES_TABLE = 0x574620
ALLOCATOR = 0x569b00
WRITABLE_SOURCE = ((ALLOCATOR, ALLOCATOR + 44), (0x569be0, 0x569c50), (0x5885e8, 0x5887f8), (0x569000, 0x5698c0))
FIELDS = (1, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
          33, 34, 35, 36, 37, 38, 53, 61, 65)
CALLBACK_REGISTRATIONS = (0x55ed58, 0x55edf8)
STUBS = {
    0x4177f0: 'callback_resolution_from_original_registry',
    0x4387d0: 'status_notice',
    0x404e80: 'server_number', 0x4062a0: 'bounded_string_copy',
    0x55ad30: 'diagnostic_context', 0x55af50: 'diagnostic_log',
    0x55ae10: 'time', 0x55ae20: 'snprintf', 0x55b000: 'sprintf',
    0x55af60: 'memset', 0x55af70: 'strchr', 0x55b030: 'rand', 0x55b150: 'memcpy',
}


def program_data(take):
    data = [(0x5a8004, 0x5a8018), (TEMPLATE_TABLE, TEMPLATE_TABLE + TEMPLATE_COUNT * 16),
            (FALLBACK, FALLBACK + 0x4bf), (0x597b8a, 0x597b8e), (0x597c32, 0x597c50),
            (0x594be5, 0x594bf1), (NAMES_TABLE, NAMES_TABLE + 19 * 4),
            (0x595060, 0x595084), (0x5a4e0c, 0x5a4e18), (0x56efc0, 0x56f500), (0x568640, 0x569000)]
    names = struct.unpack('<19I', take(NAMES_TABLE, 19 * 4))
    for pointer in sorted(set(names)):
        size = take(pointer, 32).index(b'\0') + 1
        data.append((pointer, pointer + size))
    registry = {}
    for start in CALLBACK_REGISTRATIONS:
        entry = take(start, 40)
        name = entry[:32].split(b'\0')[0]
        registry[name] = struct.unpack_from('<I', entry, 32)[0]
    if set(registry) != {b'core_PetWatch', b'core_PetTalk'}:
        raise ValueError('Original pet callback registry differs')
    expected = [registry.get(take(p, 32).split(b'\0')[0], 0) for p in names]
    if sum(bool(pointer) for pointer in expected) != 2:
        raise ValueError('Original pet callback slots differ')
    return tuple(data), registry, expected


def replay(take, slots, used_pool, *, modifier=1, base_score=1.0, serial=41, hp_mp=(1010, 1011), level=1008,
           tail=None):
    from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE, UC_PROT_READ, UC_PROT_WRITE
    from unicorn.x86_const import (
        UC_X86_REG_EAX, UC_X86_REG_EBP, UC_X86_REG_EIP, UC_X86_REG_ESP, UC_X86_REG_FPCW, UC_X86_REG_ESI,
    )

    data, registry, expected_callbacks = program_data(take)
    cpu = Uc(UC_ARCH_X86, UC_MODE_32)
    windows = CODE if tail is None else CODE + tail.code
    success_end = SUCCESS_END if tail is None else tail.endpoint
    from_entry = tail is not None and tail.from_entry
    extra_data = () if tail is None else tail.data
    stubs = STUBS if tail is None else {**STUBS, **tail.stubs}
    stops = (success_end,) if from_entry else (FAILURE_END, success_end)
    map_windows(cpu, take, windows + data + extra_data, (*stubs, *stops))
    for address, size in ((0x569000, 0x1000), (0x588000, 0x1000), (0x5ab000, 0x1000), (0x6c6000, 0x1000),
                          (0x61b000, 0x1000), (0x6bf000, 0x1000), (CHAR_TABLE, 0x1e000), (STACK, 0x7000)):
        cpu.mem_map(address, size, UC_PROT_READ | UC_PROT_WRITE)

    def get(address, count=1):
        return struct.unpack(f'<{count}i', cpu.mem_read(address, 4 * count))

    def put(address, *values):
        cpu.mem_write(address, struct.pack(f'<{len(values)}i', *values))

    def args(count):
        return get(cpu.reg_read(UC_X86_REG_ESP) + 4, count)

    def char(index):
        return CHAR_TABLE + index * CHAR_STRIDE

    def cstring(address, limit=64):
        value = bytearray()
        for offset in range(limit):
            byte = bytes(cpu.mem_read(address + offset, 1))
            if byte == b'\0':
                return bytes(value)
            value.extend(byte)
        return bytes(value)

    def snapshot():
        return [sha(bytes(cpu.mem_read(char(index), CHAR_STRIDE))) for index in range(WILD + 1)]

    for start, end in WRITABLE_SOURCE:
        cpu.mem_write(start, take(start, end - start))
    put(0x6c63f0, CHAR_TABLE)
    put(0x6bf390, 123456789)
    put(0x5ab500, WILD + 1)
    put(0x5ab510, PET_START)
    put(0x5ab520, PET_END - PET_START)
    put(0x5ab4e0, serial)
    put(0x5ab4f0, 900)
    for index in (ACTOR, WILD, *used_pool):
        put(char(index), 1)
    put(char(ACTOR) + 4 + 0x36 * 4, 1)
    put(char(ACTOR) + WORK_OFFSET + 32 * 4, modifier)
    put(char(ACTOR) + ROSTER_OFFSET, *slots)
    cpu.mem_write(char(ACTOR) + STRINGS_OFFSET, b'OwnerName\0')
    cpu.mem_write(char(ACTOR) + STRINGS_OFFSET + 2 * 64, b'OwnerAccount\0')
    for key in FIELDS:
        put(char(WILD) + 4 + key * 4, 1000 + key)
    put(char(WILD) + 4 + 8 * 4, level)
    put(char(WILD) + 4 + 10 * 4, *hp_mp)
    put(char(WILD) + 4 + 0x36 * 4, 2)
    put(char(WILD) + 4 + 58 * 4, 98765)
    put(char(WILD) + ROSTER_OFFSET, 101, 102, -1, 104, -1, 106, 107)
    cpu.mem_write(char(WILD) + STRINGS_OFFSET, b'SourcePet\0')
    if tail is not None:
        tail.initialize(cpu)
    before = snapshot()

    calls, events = Counter(), []
    staged = {}

    def fill():
        dest, value, size = args(3)
        cpu.mem_write(dest, bytes([value & 255]) * size)
        return dest

    def copy():
        dest, source, size = args(3)
        cpu.mem_write(dest, bytes(cpu.mem_read(source, size)))
        return dest

    def safe_copy():
        dest, size, source = args(3)
        cpu.mem_write(dest, cstring(source, size - 1) + b'\0')
        return dest

    def search():
        address, character = args(2)
        offset = cstring(address).find(bytes([character]))
        return 0 if offset < 0 else address + offset

    def format_notice():
        dest, capacity, fmt, slot = args(4)
        template = cstring(fmt)
        if template in (b'K%d', b'W%d'):
            payload = template % slot
        elif from_entry and fmt == 0x5a7fdb and template == b'BT|a%X|r%X|f%X|':
            payload = template % tuple(value & 0xffffffff for value in args(6)[3:])
        else:
            raise ValueError('Unexpected pet status format')
        cpu.mem_write(dest, payload[:capacity - 1] + b'\0')
        return len(payload)

    def format_serial():
        dest, fmt, timestamp, separator, server, counter = args(6)
        if cstring(fmt) != b'%ld%s%d%d':
            raise ValueError('Unexpected original pet serial format')
        payload = b'%d%s%d%d' % (timestamp, cstring(separator), server, counter)
        cpu.mem_write(dest, payload + b'\0')
        return len(payload)

    def fixture_time():
        pointer, = args(1)
        if pointer:
            put(pointer, 123456789)
        return 123456789

    def resolve_callback():
        address, = args(1)
        name = cstring(address, 32) if address else b''
        return registry[name] if name else 0

    def notify():
        owner, payload = args(2)
        events.append(['status_request', owner, cstring(payload).decode('ascii')])
        return 0

    handlers = {
        0x4177f0: resolve_callback, 0x4387d0: notify, 0x404e80: lambda: 2,
        0x4062a0: safe_copy, 0x55ad30: lambda: STACK + 0x100,
        0x55ae10: fixture_time, 0x55ae20: format_notice, 0x55b000: format_serial,
        0x55af60: fill, 0x55af70: search, 0x55b150: copy,
    }

    def hook(machine, address, size, _context):
        if address == success_end:
            machine.emu_stop()
            return
        if tail is not None:
            tail.observe(address)
        if address in stubs:
            calls[stubs[address]] += 1
            handler = handlers.get(address)
            machine.reg_write(UC_X86_REG_EAX, handler() if handler else 0)
            return
        if not any(first <= address and address + size <= end for first, end in windows):
            raise ValueError(f'Capture roster replay left approved windows at {address:#x}')
        if address == 0x468de0:
            events.append(['create', *args(2)])
        elif address == 0x42ec10:
            events.append(['find_carried_slot', *args(1)])
        elif address == 0x448df0:
            events.append(['default_template', args(2)[1]])
        elif address == 0x42f630:
            pointer, = args(1)
            bp = machine.reg_read(UC_X86_REG_EBP)
            staged.update(slot=get(bp - 0x25a0)[0], sha256=sha(bytes(cpu.mem_read(pointer, CHAR_STRIDE))),
                          type=get(pointer + 4 + 0x36 * 4)[0], experience_key_58=get(pointer + 4 + 58 * 4)[0])
            events.append(['allocate', staged['slot']])
        elif address == 0x433750:
            events.append(['max_exp_helper', *args(2)])
        elif address == 0x438840:
            who = args(3)[0]
            events.append(['compliance_before', who, *get(char(who) + 4 + 10 * 4, 2)])
        elif address == 0x46925c:
            who = machine.reg_read(UC_X86_REG_ESI)
            events.append(['compliance_after', who, *get(char(who) + 4 + 10 * 4, 2),
                           *get(char(who) + WORK_OFFSET + 13 * 4, 2)])
        elif address == 0x42de30 and args(5)[3] in (32, 83):
            events.append(['work_write', *args(5)[2:]])
        elif address == 0x432230:
            events.append(['attach', *args(3)])
        elif address == 0x42df10:
            _, _, who, key, source = args(5)
            events.append(['owner_string_write', who, key, cstring(source).decode('ascii')])

    cpu.hook_add(UC_HOOK_CODE, hook)
    if tail is not None:
        tail.probe_requirement()
    cpu.reg_write(UC_X86_REG_FPCW, X87_RESET_CONTROL)
    if from_entry:
        bp, sp = STACK + 0x6800, STACK + 0x6804
        entry, end = tail.prepare_entry_frame(sp)
    else:
        bp, sp = STACK + 0x6800, STACK + 0x5000
        entry, end = 0x5389ca, FAILURE_END
        cpu.reg_write(UC_X86_REG_EBP, bp)
        cpu.reg_write(UC_X86_REG_ESP, sp)
        put(bp - 0x628, ACTOR)
        put(bp - 0x62c, WILD)
        put(bp - 0x630, 1)
        put(bp - 0x634, -1)
        cpu.mem_write(bp - 0x688, struct.pack('<f', base_score))
        put(sp, 0, 0, ACTOR, 32)
        if tail is not None:
            tail.prepare_score_frame(bp)
    try:
        cpu.emu_start(entry, end, count=32000 if tail is None else 120000)
    except UcError as error:
        ip = cpu.reg_read(UC_X86_REG_EIP)
        raise ValueError(f'Capture roster fixture fault at {ip:#x}') from error
    endpoint = cpu.reg_read(UC_X86_REG_EIP)
    if endpoint != success_end and (from_entry or endpoint != FAILURE_END):
        raise ValueError(f'Capture did not reach the bounded endpoint at {endpoint:#x}')
    after = snapshot()
    score, = struct.unpack('<f', cpu.mem_read(bp - 0x688, 4))
    flag, pet = get(bp - 0x630)[0], get(bp - 0x634)[0]
    if from_entry:
        if cpu.reg_read(UC_X86_REG_ESP) != sp + 4 or cpu.reg_read(UC_X86_REG_EAX) != int(bool(flag)):
            raise ValueError('Original capture function did not return with the expected frame/result')
        if flag != 1:
            pet = -1
    result = {
        'score': score, 'roll': get(bp - 0x624)[0] + 1, 'modifier_after': get(char(ACTOR) + WORK_OFFSET + 32 * 4)[0],
        'result_flag': flag, 'created_character': pet, 'endpoint': endpoint,
        'roster_before': list(slots), 'roster_after': list(get(char(ACTOR) + ROSTER_OFFSET, 5)),
        'allocator_partition_start_cursor_end': list(get(ALLOCATOR + 12, 3)),
        'allocation_sequence_after': get(0x5ab4f0)[0], 'serial_counter_after': get(0x5ab4e0)[0],
        'changed_character_records': [i for i, (old, new) in enumerate(zip(before, after)) if old != new],
        'wild_record_unchanged': before[WILD] == after[WILD],
        'staged': staged, 'events': events, 'fixture_call_counts': dict(sorted(calls.items())),
    }
    if pet >= 0:
        address = char(pet)
        callbacks = list(get(address + 0x2458, 19))
        if callbacks != expected_callbacks:
            raise ValueError('Original allocator did not store the expected callback pointers')
        result['pet'] = {
            'type': get(address + 4 + 0x36 * 4)[0], 'owner_work_83': get(address + WORK_OFFSET + 83 * 4)[0],
            'owner_name': cstring(address + STRINGS_OFFSET + 4 * 64).decode('ascii'),
            'owner_account': cstring(address + STRINGS_OFFSET + 3 * 64).decode('ascii'),
            'pet_name': cstring(address + STRINGS_OFFSET).decode('ascii'),
            'pet_serial': cstring(address + STRINGS_OFFSET + 6 * 64).decode('ascii'),
            'fields': [[key, get(address + 4 + key * 4)[0]] for key in (*FIELDS, 28, 58)],
            'skill_slots': list(get(address + ROSTER_OFFSET, 7)), 'allocation_sequence': get(address + 0x2454)[0],
            'callback_pointers': [[i, va] for i, va in enumerate(callbacks) if va],
        }
    if tail is not None:
        result['tail'] = tail.result()
    return result


def derive(archive, exe):
    raw = exe.read_bytes()
    _, take, _, _, symbols = original_image(raw, SYMBOLS)
    previous = json.loads(WORLD35.read_bytes())
    source, = [row for row in previous['source_members'] if row['target'] == 'gmsv/gmsv.exe']
    if source['member_sha256'] != EXE_SHA or previous['archive_sha256'] != ARCHIVE_SHA:
        raise ValueError('WORLD35 source provenance differs')
    verify_archive(archive, source, raw)
    data, _, _ = program_data(take)
    table = take(TEMPLATE_TABLE, TEMPLATE_COUNT * 16)
    templates = list(struct.iter_unpack('<4I', table))
    if TEMPLATE_ID in {row[0] for row in templates} or templates[-1][1] != FALLBACK:
        raise ValueError('Original template lookup qualification differs')
    scenarios = {
        'two_roster_holes': ([3, 4, -1, 6, -1], [3, 4, 6], {}),
        'last_roster_slot_and_serial_wrap': ([3, 4, 5, 6, -1], [3, 4, 5, 6], {'serial': 999}),
        'low_hp_mp_retained': ([3, 4, -1, 6, -1], [3, 4, 6], {'hp_mp': [25, 20], 'level': 35}),
        'full_roster': ([3, 4, 5, 6, 7], [3, 4, 5, 6, 7], {}),
        'exhausted_pet_partition': ([3, 4, -1, 6, -1], list(range(PET_START, PET_END)), {}),
        'comparison_equal': ([3, 4, -1, 6, -1], [3, 4, 6], {'modifier': 0}),
    }
    return {
        'schema': 'stoneage.world36.capture_roster_source.r1',
        'scope': 'PRESERVED_MIXED25_CAPTURE_SCORE_TO_PET_ROSTER_X86_FIXTURE',
        'archive_sha256': ARCHIVE_SHA, 'source_member': source, 'symbols': symbols,
        'code_windows': [[a, b, sha(take(a, b-a))] for a, b in CODE],
        'data_windows': [[a, b, sha(take(a, b-a))] for a, b in
                         (*data, *WRITABLE_SOURCE, *((va, va + 40) for va in CALLBACK_REGISTRATIONS))],
        'default_template': {'requested_key': TEMPLATE_ID, 'table_count': TEMPLATE_COUNT,
                             'matching_entries': 0, 'fallback_address': FALLBACK},
        'fixture': {'owner': ACTOR, 'wild': WILD, 'pet_partition': [PET_START, PET_END],
                    'base_score': 1.0, 'default_capture_modifier': 1, 'random': 0,
                    'timestamp': 123456789, 'server_number': 2, 'serial_counter': 41,
                    'source_hp_mp': [1010, 1011], 'source_level': 1008, 'source_int_key_58': 98765},
        'fixtures_by_address': STUBS,
        'cases': {name: {'pool_records_initially_used': pool, 'overrides': kwargs,
                         'trace': replay(take, slots, pool, **kwargs)}
                  for name, (slots, pool, kwargs) in scenarios.items()},
        'original_process_started': False, 'parameter_compliance_executed': True,
        'network_messages_delivered': False, 'battle_removal_or_save_executed': False,
        'historical_official_deployment_verified': False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('gmsv', type=Path)
    args = parser.parse_args()
    print(json.dumps(derive(args.archive, args.gmsv), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
