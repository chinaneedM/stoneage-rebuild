"""Replay ordinary single-target recovery from the verified mixed25 GMSV image."""

import argparse
from hashlib import file_digest
import json
from pathlib import Path
import struct
from zlib import crc32

from tools.stoneage_recovery_callback_replay import BATTLE, X87_RESET_CONTROL, trial
from tools.stoneage_recovery_source import REPORT as WORLD31, sha
from tools.stoneage_savepoint_item_source import EXE_SHA, original_image
from tools.stoneage_scene33_source_pair import ARCHIVE_SHA, ROOT

REPORT = ROOT / 'research/recovered/STONEAGE-STAGE-A-WORLD32-BATTLE-RECOVERY-SOURCE-R1.json'
SCOPE = 'PRESERVED_MIXED25_ORDINARY_SINGLE_TARGET_NO_MOUNT_X86_REPLAY'
SYMBOLS = {
    '_BATTLE_No2Index': 0x517760, '_BATTLE_TargetCheck': 0x518440,
    '_BATTLE_MultiList': 0x5185e0, '_BATTLE_getRidePet': 0x5300e0,
    '_BATTLE_MagicEffect': 0x548360, '_BATTLE_MultiRecovery': 0x548eb0,
}
CODE = ((0x517760, 0x517810), (0x518440, 0x518b20), (0x5300e0, 0x530158),
        (0x548360, 0x54855a), (0x548eb0, 0x54981e))
DATA = ((0x5a7008, 0x5a70e9), (0x5a9b48, 0x5a9c54))
MAX_RAND = 2**31 - 1
GLOBALS = 0x2030000
BATTLE_TABLE = 0x700000
LOG = 0x701000
STOP = 0x702000
STACK = 0x800000
FORMATS = {
    0x5a9b57: b'BJ|a%X|m%X|e%X|e%X|',
    0x5a9b6b: b'r%X|',
    0x5a9c1a: b'BD|r%X|%X|%X|d%X|p%X|',
}
POISON_LIST = (0x12345678, 0x23456789)
STUBS = {
    0x42d960: 'character_index_check', 0x42db90: 'read_attribute',
    0x42dcf0: 'write_attribute', 0x42ddc0: 'read_work_attribute',
    0x42e190: 'read_flag', 0x4335f0: 'can_cure', 0x55ad30: 'getreent',
    0x55ae00: 'fwrite', 0x55ae20: 'snprintf', 0x55af60: 'memset',
    0x55b030: 'rand', 0x55b150: 'memcpy',
}


def replay(take, request, *, hp=100, mp=10, max_hp=1000, max_mp=100,
           rand=(0,), target_hp=None, mode=2, flag1=1, flag8=0,
           can_cure=1, no_candidate=False):
    from unicorn import Uc, UC_ARCH_X86, UC_HOOK_CODE, UC_MODE_32, UC_PROT_ALL, UC_PROT_READ, UC_PROT_EXEC
    from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_EBP, UC_X86_REG_EIP, UC_X86_REG_ESP, UC_X86_REG_FPCW

    battle, caster_slot, target_slot, kind, _, percent, _, _ = request
    if battle != 0 or percent != 0 or kind not in (0, 1) or not 0 <= target_slot < 20:
        raise ValueError('Request is outside the ordinary single-target fixture')
    uc = Uc(UC_ARCH_X86, UC_MODE_32)
    uc.reg_write(UC_X86_REG_FPCW, X87_RESET_CONTROL)
    pages = set()

    def image(address, payload):
        for page in range(address & ~0xfff, (address + len(payload) + 0xfff) & ~0xfff, 0x1000):
            if page not in pages:
                uc.mem_map(page, 0x1000, UC_PROT_READ | UC_PROT_EXEC)
                pages.add(page)
        uc.mem_write(address, payload)

    def integers(address, *values):
        uc.mem_write(address, struct.pack('<' + 'i' * len(values), *values))

    def read_ints(address, count):
        return struct.unpack('<' + 'i' * count, uc.mem_read(address, count * 4))

    def args(count):
        return read_ints(uc.reg_read(UC_X86_REG_ESP) + 4, count)

    for start, end in CODE + DATA:
        image(start, take(start, end - start))
    for address in STUBS:
        image(address, b'\xc3')
    image(STOP, b'\xcc')
    uc.mem_map(STACK, 0x4000, UC_PROT_ALL & ~UC_PROT_EXEC)
    uc.mem_map(GLOBALS, 0x2000, UC_PROT_ALL & ~UC_PROT_EXEC)
    uc.mem_map(BATTLE_TABLE, 0x2000, UC_PROT_ALL & ~UC_PROT_EXEC)
    integers(0x2030410, 1)
    integers(0x2030860, LOG)
    integers(0x2031a80, LOG + 0x800)
    integers(0x2031a90, BATTLE_TABLE)

    slots = dict.fromkeys(range(20), -1)
    slots[caster_slot] = 8
    slots[target_slot] = 9
    if target_hp is not None and not no_candidate:
        fallback_slot = 0 if target_slot < 10 else 10
        slots[fallback_slot] = 10
    for slot, index in slots.items():
        offset = 0xac if slot < 10 else 0x220
        integers(BATTLE_TABLE + offset + (slot % 10) * 36, index)

    stats = {who: {10: hp, 11: mp, 0x36: 1, 0x57: -1} for who in (8, 9, 10)}
    work = {who: {0: 2, 13: max_hp, 14: max_mp} for who in stats}
    flags = {who: {1: 1, 8: 0} for who in stats}
    stats[9][10] = hp if target_hp is None else target_hp
    work[9][0] = mode
    flags[9] = {1: flag1, 8: flag8}
    start = STACK + 0x3f00
    integers(start, STOP, *request)
    uc.reg_write(UC_X86_REG_ESP, start)
    rolls, writes, cure_checks, selected, diagnostics = [], [], [], [], []
    incomplete_list = {}

    def format_message():
        dest, size, fmt = args(3)
        template = FORMATS[fmt]
        if uc.mem_read(fmt, len(template) + 1) != template + b'\0':
            raise ValueError('Source format differs')
        values = tuple(value & 0xffffffff for value in args(3 + template.count(b'%X'))[3:])
        payload = template % values
        uc.mem_write(dest, payload[:size - 1] + b'\0')
        return len(payload)

    def set_attr():
        _, _, who, key, value = args(5)
        writes.append([who, key, stats[who][key], value])
        stats[who][key] = value
        return 1

    def read_work():
        _, _, who, key = args(4)
        return work[who][key]

    def read_flag():
        _, _, who, flag = args(4)
        return flags[who][flag]

    def check_cure():
        who, marker = args(2)
        if uc.mem_read(marker, 3) != b'HP\0':
            raise ValueError('Unexpected cure marker')
        cure_checks.append(who)
        return can_cure

    def fill():
        dest, value, count = args(3)
        uc.mem_write(dest, bytes((value & 0xff,)) * count)
        return dest

    def copy():
        dest, src, count = args(3)
        uc.mem_write(dest, bytes(uc.mem_read(src, count)))
        return dest

    def rng():
        value = rand[len(rolls)]
        rolls.append(value)
        return value

    def diagnostic():
        _, size, count, _ = args(4)
        diagnostics.append([size, count])
        return count

    callbacks = {
        0x42d960: lambda: args(3)[2] in stats,
        0x42db90: lambda: stats[args(2)[0]][args(2)[1]],
        0x42dcf0: set_attr, 0x42ddc0: read_work, 0x42e190: read_flag,
        0x4335f0: check_cure, 0x55ad30: lambda: BATTLE_TABLE + 0x500,
        0x55ae00: diagnostic, 0x55ae20: format_message, 0x55af60: fill,
        0x55b030: rng, 0x55b150: copy,
    }
    if set(callbacks) != set(STUBS):
        raise ValueError('Fixture callback addresses differ')

    def hook(cpu, address, _size, _context):
        if address in callbacks:
            cpu.reg_write(UC_X86_REG_EAX, callbacks[address]())
        elif address == 0x548ee0 and no_candidate:
            # Distinguish an untouched output list from a written terminator.
            integers(cpu.reg_read(UC_X86_REG_EBP) - 0x78, *POISON_LIST)
        elif address == 0x548ee5 and no_candidate:
            value = cpu.reg_read(UC_X86_REG_EAX)
            incomplete_list.update({
                'return_value': struct.unpack('<i', struct.pack('<I', value))[0],
                'stack_words_after_call': read_ints(cpu.reg_read(UC_X86_REG_EBP) - 0x78, 2),
                'stack_words_before_call': POISON_LIST,
            })
            cpu.emu_stop()
        elif address == 0x548f04:
            slot, end = read_ints(cpu.reg_read(UC_X86_REG_EBP) - 0x78, 2)
            if slot not in range(20) or end != -1:
                raise ValueError('Expected a terminated single-target list')
            selected.append(slot)
        elif not any(lo <= address < hi for lo, hi in CODE):
            raise ValueError(f'Execution left approved source windows at {address:#x}')

    uc.hook_add(UC_HOOK_CODE, hook)
    uc.emu_start(SYMBOLS['_BATTLE_MultiRecovery'], STOP, count=8000)
    expected_end = 0x548ee5 if no_candidate else STOP
    if uc.reg_read(UC_X86_REG_EIP) != expected_end:
        raise ValueError('Recovery did not reach the expected endpoint')
    end, = read_ints(0x2030860, 1)
    log = bytes(uc.mem_read(LOG, end - LOG)).decode('ascii') if end != LOG else ''
    return {'selected_slots': selected, 'writes': writes, 'cure_checks': cure_checks,
            'rand': rolls, 'battle_buffer': log, 'diagnostics': diagnostics,
            'settlement_returned': not no_candidate,
            **({'incomplete_list': incomplete_list} if no_candidate else {})}


def verify_archive(archive, source, raw):
    with archive.open('rb') as stream:
        if archive.stat().st_size != 361255180 or file_digest(stream, 'sha256').hexdigest() != ARCHIVE_SHA:
            raise ValueError('Complete preserved archive differs')
        stream.seek(source['header_offset'])
        if (sha(stream.read(source['header_bytes'])) != source['header_sha256']
                or sha(stream.read(source['packed_bytes'])) != source['packed_sha256']
                or crc32(raw) != source['member_crc32']):
            raise ValueError('Preserved GMSV member witness differs')


def derive(archive, exe):
    import unicorn

    raw = exe.read_bytes()
    _, take, _, _, found = original_image(raw, SYMBOLS)
    previous = json.loads(WORLD31.read_bytes())
    source, = [member for member in previous['selected_source_members']
               if member['target'] == 'gmsv/gmsv.exe']
    if source['member_sha256'] != EXE_SHA or previous['archive_sha256'] != ARCHIVE_SHA:
        raise ValueError('WORLD31 source provenance differs')
    verify_archive(archive, source, raw)
    requests = {}
    for witness in previous['emulated']['ordinary_option_replays']:
        option = ''.join(f'{token}{amount}' for token, amount in witness['tokens'])
        callback = trial(take, option, BATTLE)
        request, = callback['battle_requests']
        if request[3:6] != witness['battle_request_kind_value_percent']:
            raise ValueError('Original item callback no longer matches WORLD31')
        key = tuple(request[3:5])
        entry = requests.setdefault(key, {
            'world31_request': request, 'ordinary_options': 0, 'source_rows': 0,
        })
        if entry['world31_request'] != request:
            raise ValueError('Same kind and power have different original requests')
        entry['ordinary_options'] += 1
        entry['source_rows'] += witness['source_rows']
    batch = []
    for entry in requests.values():
        request = [0, 2, 7, *entry['world31_request'][3:]]
        outcomes = [replay(take, request, rand=(value,), max_hp=10000, max_mp=10000)
                    for value in (0, MAX_RAND)]
        batch.append({**entry, 'unclamped_writes': [row['writes'] for row in outcomes]})
    cases = (
        ('hp_low', 0, 320, {}),
        ('hp_high', 0, 320, {'rand': (MAX_RAND,)}),
        ('hp_cap', 0, 320, {'hp': 980}),
        ('hp_full', 0, 320, {'hp': 1000}),
        ('hp_cure_denied', 0, 320, {'can_cure': 0}),
        ('mp_low', 1, 25, {}),
        ('mp_high', 1, 25, {'rand': (MAX_RAND,)}),
        ('mp_cap', 1, 25, {'mp': 95}),
        ('mp_full', 1, 25, {'mp': 100}),
        ('mp_cure_denied_fixture', 1, 25, {'can_cure': 0}),
        ('dead_requested_slot', 0, 320, {'target_hp': 0, 'rand': (0, 0)}),
        ('retarget_retry', 0, 320, {'target_hp': 0, 'rand': (9, 10, MAX_RAND)}),
        ('dead_second_side_slot', 1, 25, {'target_slot': 17, 'target_hp': 0, 'rand': (0, 0)}),
        ('inactive_mode', 0, 320, {'mode': 0, 'target_hp': 100, 'rand': (0, 0)}),
        ('excluded_mode_5', 0, 320, {'mode': 5, 'target_hp': 100, 'rand': (0, 0)}),
        ('required_flag_1_clear', 0, 320, {'flag1': 0, 'target_hp': 100, 'rand': (0, 0)}),
        ('excluded_flag_8_set', 0, 320, {'flag8': 1, 'target_hp': 100, 'rand': (0, 0)}),
        ('no_eligible_slot', 0, 320, {'target_slot': 17, 'target_hp': 0, 'no_candidate': True}),
    )
    observations = {}
    for name, kind, amount, fixture in cases:
        fixture = dict(fixture)
        slot = fixture.pop('target_slot', 7)
        request = [0, 2, slot, *requests[kind, amount]['world31_request'][3:]]
        observations[name] = {'request': request, 'fixture_overrides': fixture, **replay(take, request, **fixture)}
    return {
        'schema': 'stoneage.world32.battle_recovery_source.r1',
        'scope': SCOPE,
        'archive_sha256': ARCHIVE_SHA,
        'original_member': source,
        'world31_receipt_sha256': sha(WORLD31.read_bytes()),
        'program': {'symbols': found, 'source_windows': [[a, b, sha(take(a, b-a))] for a, b in CODE + DATA],
                    'rng_constants': struct.unpack('<2df', take(0x5a9c40, 20))},
        'fixture': {'engine': f'Unicorn {unicorn.__version__} x86-32',
                    'x87_control_word': X87_RESET_CONTROL, 'hp_mp': [100, 10], 'max_hp_mp': [1000, 100],
                    'caster_slot_index': [2, 8], 'requested_character_index': 9,
                    'fallback_character_index': 10, 'stubbed_functions': STUBS,
                    'default_work_mode': 2, 'default_flags_1_8': [1, 0],
                    'player_kind': 1, 'mounted_pet_slot': -1},
        'ordinary_request_batch': batch,
        'observations': observations,
        'original_client_or_server_started': False,
        'live_battle_outcome_observed': False,
        'inventory_actually_mutated': False,
        'official_early_version_equivalence_proven': False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('exe', type=Path)
    args = parser.parse_args()
    print(json.dumps(derive(args.archive, args.exe), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
