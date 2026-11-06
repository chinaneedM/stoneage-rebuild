"""Replay original mixed25 capture item effects and their capture-score consumer."""

import argparse
import json
from pathlib import Path
import re
import struct

from tools.stoneage_battle_item_gate_source import map_windows
from tools.stoneage_battle_recovery_source import CODE as BATTLE_CODE, DATA as BATTLE_DATA, FORMATS
from tools.stoneage_cooking_source import source_rows
from tools.stoneage_recovery_callback_replay import X87_RESET_CONTROL
from tools.stoneage_recovery_source import RNG_HIGH, verified_sources
from tools.stoneage_savepoint_item_source import original_image
from tools.stoneage_scene33_source_pair import ARCHIVE_SHA, ROOT, sha
from tools.stoneage_world34_field_item_replay import (
    CHAR_STRIDE, ITEMS_OFFSET, WORK_OFFSET, REPORT as WORLD34, replay as replay_field,
)

REPORT = ROOT / 'research/recovered/STONEAGE-STAGE-A-WORLD35-CAPTURE-ITEM-SOURCE-R1.json'
WORLD19 = ROOT / 'research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-19-ITEM-USE-HANDLERS-R1.json'
SYMBOLS = {
    '_ITEM_useCaptureUp': 0x5011b0, '_ITEM_useCaptureUp_Battle': 0x559df0,
    '_BATTLE_MultiCaptureUp': 0x54cc30, '_BATTLE_Capture': 0x5380e0,
    '_BATTLE_ItemUseDelete': 0x558450, '_BATTLE_Index2No': 0x5178c0,
    '__CHAR_getWorkInt': 0x42ddc0, '__CHAR_setWorkInt': 0x42de30,
    '_ITEM_itemconfentries': 0x587e60,
}
CODE = (
    (0x5011b0, 0x501234), (0x559df0, 0x559f06), (0x54cc30, 0x54ce8d),
    (0x5389ca, 0x538a9e), (0x5381b9, 0x5381ef), (0x558450, 0x558605),
    (0x5178c0, 0x517970), BATTLE_CODE[0], BATTLE_CODE[1], BATTLE_CODE[3],
    (0x42d960, 0x42d998), (0x42db90, 0x42dbac), (0x42dc30, 0x42dcf0),
    (0x42ddc0, 0x42deda), (0x42e190, 0x42e208), (0x42e2e0, 0x42e3b0),
    (0x42e670, 0x42e67a), (0x433ab0, 0x433c40), (0x4f71b0, 0x4f7220),
    (0x4f72a0, 0x4f7460), (0x4f7500, 0x4f7640), (0x4f76e0, 0x4f7777),
)
DATA = (*BATTLE_DATA, (0x569b24, 0x569b2c), (0x5a4a6b, 0x5a4a6c),
        (0x5a8004, 0x5a8018), (0x5a9e72, 0x5a9e94), (0x5aa899, 0x5aa89c))
STUBS = {
    0x417f40: 'item_log', 0x43f040: 'display_name', 0x473740: 'inventory_notice',
    0x55ad30: 'diagnostic_context', 0x55ae00: 'diagnostic_write', 0x55ae20: 'snprintf',
    0x55af50: 'diagnostic_log', 0x55af60: 'memset', 0x55afd0: 'sscanf',
    0x55b030: 'rand', 0x55b150: 'memcpy',
}
ACTOR, TEAMMATE, WILD = 8, 9, 10
ACTOR_SLOT, TEAMMATE_SLOT, WILD_SLOT, ITEM_SLOT = 2, 7, 17, 7
ITEM_TABLE, BATTLE_TABLE, CHAR_TABLE = 0x700000, 0x702000, 0x710000
LOG, STACK, STOP = 0x703000, 0x800000, 0x805000
WORK_KEY = 32
OPTIONS_OFFSET = 0x10c + 3 * 64
CAPTURE_FORMATS = {**FORMATS, 0x5a9e72: b'B%%|%X|%X|'}


def replay(take, row, option, *, rand=0, actor_mode=2, target_slot=ACTOR_SLOT,
           recipient_kind=1, target_hp=100, existing=0, occupied=True,
           score_base=10.0, score_rand=0, sleep=0, score_actor=ACTOR):
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE, UC_PROT_READ, UC_PROT_WRITE
    from unicorn.x86_const import (
        UC_X86_REG_EAX, UC_X86_REG_EBP, UC_X86_REG_EIP, UC_X86_REG_ESP, UC_X86_REG_FPCW,
    )

    cpu = Uc(UC_ARCH_X86, UC_MODE_32)
    map_windows(cpu, take, CODE + DATA, (*STUBS, STOP))
    for address, size in ((0x5ab000, 0x1000), (0x61b000, 0x1000), (0x6c6000, 0x1000),
                          (0x2030000, 0x2000), (ITEM_TABLE, 0x1000), (BATTLE_TABLE, 0x2000),
                          (CHAR_TABLE, 0x1a000), (STACK, 0x4000)):
        cpu.mem_map(address, size, UC_PROT_READ | UC_PROT_WRITE)

    def put(address, *values):
        cpu.mem_write(address, struct.pack(f'<{len(values)}i', *values))

    def get(address, count=1):
        return struct.unpack(f'<{count}i', cpu.mem_read(address, count * 4))

    def args(count):
        return get(cpu.reg_read(UC_X86_REG_ESP) + 4, count)

    def character(who):
        return CHAR_TABLE + who * CHAR_STRIDE

    def work(who, key):
        return character(who) + WORK_OFFSET + key * 4

    put(0x5ab500, WILD + 1)
    put(0x5ab510, TEAMMATE + 1)
    put(0x6c63f0, CHAR_TABLE)
    put(0x61b630, int(occupied))
    put(0x61b640, ITEM_TABLE)
    put(0x61b650, 1)
    put(ITEM_TABLE, int(occupied), row['id'])
    for key, field in ((3, 'type'), (4, 'fieldtype'), (5, 'target'), (46, 'useaction')):
        put(ITEM_TABLE + 4 + key * 4, row[field])
    cpu.mem_write(ITEM_TABLE + OPTIONS_OFFSET, option + b'\0')
    put(0x2030410, 1)
    put(0x2030860, LOG)
    put(0x2031a80, LOG + 0x800)
    put(0x2031a90, BATTLE_TABLE)
    for slot in range(20):
        base = 0xac if slot < 10 else 0x220
        who = {ACTOR_SLOT: ACTOR, TEAMMATE_SLOT: TEAMMATE, WILD_SLOT: WILD}.get(slot, -1)
        put(BATTLE_TABLE + base + (slot % 10) * 36, who)
    recipient = {ACTOR_SLOT: ACTOR, TEAMMATE_SLOT: TEAMMATE, WILD_SLOT: WILD}[target_slot]
    for who, kind in ((ACTOR, 1), (TEAMMATE, 1), (WILD, 2)):
        base = character(who)
        put(base, 1)
        put(base + 4 + 10 * 4, target_hp if who == recipient else 100)
        put(base + 4 + 0x36 * 4, recipient_kind if who == recipient else kind)
        cpu.mem_write(base + 0x4bc, b'\x02')
        put(base + ITEMS_OFFSET, *([-1] * 20))
        put(work(who, 0), actor_mode if who == ACTOR else 2)
        put(work(who, WORK_KEY), existing if who == recipient else 0)
    inventory = character(ACTOR) + ITEMS_OFFSET + ITEM_SLOT * 4
    put(inventory, 0 if occupied else -1)

    rolls, requests, selection, deletion, writes = [], [], [], [], []
    phase = 'item'

    def scan():
        source, fmt, dest = args(3)
        if source != ITEM_TABLE + OPTIONS_OFFSET or cpu.mem_read(fmt, 3) != b'%d\0':
            raise ValueError('Unexpected capture item scan')
        actual = bytes(cpu.mem_read(source, len(option) + 1))
        match = re.match(rb'\s*[+-]?\d+', actual)
        if not match:
            return 0
        put(dest, int(match[0]))
        return 1

    def format_message():
        dest, capacity, fmt = args(3)
        template = CAPTURE_FORMATS[fmt]
        if bytes(cpu.mem_read(fmt, len(template) + 1)) != template + b'\0':
            raise ValueError('Original capture format differs')
        values = tuple(value & 0xffffffff for value in args(3 + template.count(b'%X'))[3:])
        payload = template % values
        cpu.mem_write(dest, payload[:capacity - 1] + b'\0')
        return len(payload)

    def fill():
        dest, value, size = args(3)
        cpu.mem_write(dest, bytes((value & 0xff,)) * size)
        return dest

    def copy():
        dest, source, size = args(3)
        cpu.mem_write(dest, bytes(cpu.mem_read(source, size)))
        return dest

    def random():
        value = rand if phase == 'item' else score_rand
        rolls.append(value)
        return value

    handlers = {
        0x43f040: lambda: ITEM_TABLE + 0x10c, 0x55ad30: lambda: BATTLE_TABLE + 0x500,
        0x55ae20: format_message, 0x55af60: fill, 0x55afd0: scan,
        0x55b030: random, 0x55b150: copy,
    }

    def hook(machine, address, size, _context):
        if address in STUBS:
            handler = handlers.get(address)
            machine.reg_write(UC_X86_REG_EAX, handler() if handler else 0)
            return
        if not any(first <= address and address + size <= end for first, end in CODE):
            raise ValueError(f'Capture replay left approved source windows at {address:#x}')
        if address == 0x54cc30:
            requests.append(list(args(6)))
        elif address == 0x54cc57:
            if machine.reg_read(UC_X86_REG_EAX) == 0xffffffff:
                raise ValueError('Original target list returned without a bounded candidate')
            first, terminator = get(machine.reg_read(UC_X86_REG_EBP) - 0x78, 2)
            if first not in (ACTOR_SLOT, TEAMMATE_SLOT, WILD_SLOT) or terminator != -1:
                raise ValueError('Expected original terminated single-target list')
            selection.append(first)
        elif address == 0x42de30:
            _, _, who, key, value = args(5)
            writes.append([who, key, get(work(who, key))[0], value])
        elif address == 0x433ab0:
            deletion.append(list(args(6)[2:]))

    cpu.hook_add(UC_HOOK_CODE, hook)
    sp = STACK + 0x3f00
    put(sp, STOP, ACTOR, target_slot, ITEM_SLOT)
    cpu.reg_write(UC_X86_REG_ESP, sp)
    cpu.reg_write(UC_X86_REG_FPCW, X87_RESET_CONTROL)
    cpu.emu_start(SYMBOLS['_ITEM_useCaptureUp'], STOP, count=30000)
    if cpu.reg_read(UC_X86_REG_EIP) != STOP or cpu.reg_read(UC_X86_REG_ESP) != sp + 4:
        raise ValueError('Capture item callback did not return')
    end, = get(0x2030860)
    result = {
        'settlement_args': requests, 'selected_slots': selection, 'item_rand': rolls.copy(),
        'item_work_writes': writes.copy(), 'delete_args': deletion,
        'slot_after': get(inventory)[0], 'item_live_after': get(ITEM_TABLE)[0],
        'active_item_count_after': get(0x61b630)[0],
        'post_item_modifiers': [get(work(who, WORK_KEY))[0] for who in (ACTOR, TEAMMATE, WILD)],
        'battle_buffer': bytes(cpu.mem_read(LOG, end - LOG)).decode('ascii') if end > LOG else '',
    }

    if score_base is not None:
        # Continue in the same fixture memory, supplying only the earlier base-score result.
        # Enter on the original getter call with its stack arguments already present.
        phase = 'score'
        rolls.clear()
        writes.clear()
        bp = STACK + 0x3000
        sp = STACK + 0x2000
        cpu.reg_write(UC_X86_REG_EBP, bp)
        cpu.reg_write(UC_X86_REG_ESP, sp)
        put(work(WILD, 43), sleep)
        put(bp - 0x628, score_actor)
        put(bp - 0x62c, WILD)
        put(bp - 0x630, 1)
        cpu.mem_write(bp - 0x688, struct.pack('<f', score_base))
        put(sp, 0, 0, score_actor, WORK_KEY)
        modifier_before, = get(work(score_actor, WORK_KEY))
        cpu.emu_start(0x5389ca, 0x5381ef, count=1000)
        if cpu.reg_read(UC_X86_REG_EIP) != 0x5381ef:
            raise ValueError('Capture score replay did not reach the post-reset boundary')
        score, = struct.unpack('<f', cpu.mem_read(bp - 0x688, 4))
        result['score'] = {
            'character': score_actor, 'modifier_before': modifier_before, 'points': score,
            'integer_roll': get(bp - 0x624)[0] + 1,
            'comparison_flag': get(bp - 0x630)[0], 'random_input': rolls,
            'work_writes': writes, 'modifier_after': get(work(score_actor, WORK_KEY))[0],
        }
    return result


def useaction_column(take):
    """Follow the compiled descriptor loop's extra physical-column increments."""
    descriptors = take(SYMBOLS['_ITEM_itemconfentries'], 79 * 16)
    physical = 0
    paired = []
    paired_first_columns = []
    action = None
    for ordinal, (name, kind, key, parser) in enumerate(struct.iter_unpack('<4I', descriptors)):
        if take(name, 10) == b'useaction\0':
            action = {'descriptor_ordinal': ordinal, 'physical_column': physical, 'runtime_int_key': key}
        if kind == 2 and parser == 0x4f8f70:
            paired.append(ordinal)
            paired_first_columns.append(physical)
            physical += 1
        physical += 1
    if physical != 94 or action != {'descriptor_ordinal': 62, 'physical_column': 77, 'runtime_int_key': 46}:
        raise ValueError('Original descriptor-to-column mapping differs')
    return {
        **action, 'paired_descriptors': paired, 'paired_first_physical_columns': paired_first_columns,
        'descriptors_sha256': sha(descriptors),
        'parser_windows': [[a, b, sha(take(a, b-a))] for a, b in
                           ((0x4f96df, 0x4f97fa), (0x4f986e, 0x4f98b8))],
    }


def field_rechecks(take, physical_rows):
    previous = json.loads(WORLD34.read_bytes())
    by_id = {row['id']: row for row in previous['items']}
    results = []
    for case in previous['cases']:
        if case['scenario'] not in ('self_min', 'self_max', 'pet_min', 'pet_max', 'party_min', 'party_max'):
            continue
        row = by_id[case['item']]
        digest, option, useaction = physical_rows[row['id']]
        if digest != row['row_sha256'] or sha(option) != row['option_sha256']:
            raise ValueError('WORLD34 physical row or option differs')
        row = {**row, 'ints': {int(key): value for key, value in row['ints'].items()}}
        new = replay_field(take, row, option, case['target_input'], useaction=useaction, **case['overrides'])
        old = case['trace']
        keys = ('stat_writes', 'delete_args', 'slot_after', 'item_live_after', 'intake_returned')
        if any(new[key] != old[key] for key in keys):
            raise ValueError('WORLD34 original useaction changed a previously reported material result')
        results.append({'id': row['id'], 'scenario': case['scenario'], 'useaction': useaction,
                        'action_notice_called': 'action_notice' in new['fixture_calls'],
                        **{key: new[key] for key in keys}})
    return results


def derive(archive, extracted):
    members, witness = verified_sources(archive, extracted)
    _, take, _, literal, symbols = original_image(members['gmsv/gmsv.exe'], SYMBOLS)
    literal(0x55e650, 'ITEM_useCaptureUp')
    registration = take(0x55e650, 40)
    if struct.unpack_from('<I', registration, 32)[0] != symbols['_ITEM_useCaptureUp']:
        raise ValueError('Original capture item registration differs')

    schema = useaction_column(take)
    alternate = (extracted / 'itemset0710.txt').read_bytes()
    alternate_source = json.loads(WORLD19.read_bytes())['source']['B']
    if (len(alternate), sha(alternate)) != (alternate_source['bytes'], alternate_source['sha256']):
        raise ValueError('Alternate item table identity differs')
    alternate_rows = {int(fields[16]): (line, sha(physical))
                      for line, physical, fields in source_rows(alternate, 94)
                      if fields[10] == b'ITEM_useCaptureUp'}

    rows = []
    options = {}
    field_rows = {}
    for line, physical, fields in source_rows(members['gmsv/data/itemset.txt'], 94):
        is_field_recheck = fields[16] in (b'1232', b'12530', b'12555')
        is_capture_item = fields[10] == b'ITEM_useCaptureUp'
        if not (is_field_recheck or is_capture_item):
            continue
        if any(not fields[column] for column in schema['paired_first_physical_columns']):
            raise ValueError('Empty paired field needs a separate physical-column qualification')
        useaction = int(fields[schema['physical_column']])
        if is_field_recheck:
            field_rows[int(fields[16])] = (sha(physical), fields[3], useaction)
        if not is_capture_item:
            continue
        if fields[0].startswith(b'#') or not re.fullmatch(rb'[0-9]+', fields[3]):
            raise ValueError('Unqualified original capture row')
        item, item_type, field, target = (int(fields[column]) for column in (16, 19, 20, 21))
        if item in options:
            raise ValueError('Duplicate original capture item ID')
        alternate_line, alternate_sha = alternate_rows[item]
        if sha(physical) != alternate_sha:
            raise ValueError('Alternate capture item physical row differs')
        rows.append({'id': item, 'line': line, 'alternate_line': alternate_line, 'row_sha256': alternate_sha,
                     'row_without_line_ending_sha256': sha(physical.rstrip(b'\r\n')),
                     'option_sha256': sha(fields[3]), 'base_option': int(fields[3]),
                     'type': item_type, 'fieldtype': field, 'target': target,
                     'useaction': useaction})
        options[item] = fields[3]
    if len(rows) != 26 or set(alternate_rows) != set(options):
        raise ValueError('Original configured capture rows differ')
    ordinary = [{'id': row['id'], 'random': rand, 'trace': replay(take, row, options[row['id']],
                 rand=rand, target_slot=TEAMMATE_SLOT if row['target'] == 1 else ACTOR_SLOT)}
                for row in rows for rand in (0, RNG_HIGH)]
    by_id = {row['id']: row for row in rows}
    controls = (
        ('field_mode', 12822, {'actor_mode': 0}), ('initializing_battle', 12822, {'actor_mode': 1}),
        ('missing_item', 12822, {'occupied': False}), ('add_existing', 12822, {'existing': 12}),
        ('middle_random', 12819, {'rand': 2**30}),
        ('nonplayer', 2702, {'target_slot': WILD_SLOT, 'recipient_kind': 2}),
        ('dead_target_same_side_fallback', 2702, {'target_slot': TEAMMATE_SLOT, 'target_hp': 0}),
        ('failed_scan_default_5', 12822, {}), ('empty_option_default_5', 12822, {}),
        ('score_equal_rejected', 12822, {'actor_mode': 0, 'score_base': 1.0}),
        ('score_bonus_changes_comparison', 12781, {'rand': RNG_HIGH, 'score_base': 1.0}),
        ('teammate_consumes_own_bonus', 2702, {'target_slot': TEAMMATE_SLOT, 'score_actor': TEAMMATE}),
        ('sleep_bonus', 12822, {'sleep': 1}),
        ('cap_roll_98', 1833, {'score_base': 90.0, 'score_rand': (97 * 2**31) // 100 + 100000}),
        ('cap_roll_99', 1833, {'score_base': 90.0, 'score_rand': (98 * 2**31) // 100 + 100000}),
        ('cap_and_high_random', 1833, {'score_base': 90.0, 'score_rand': RNG_HIGH}),
    )
    probes = {}
    for name, item, kwargs in controls:
        option = {'failed_scan_default_5': b'invalid', 'empty_option_default_5': b''}.get(name, options[item])
        probes[name] = {'id': item, 'overrides': kwargs, 'synthetic_option': option != options[item],
                        'trace': replay(take, by_id[item], option, **kwargs)}

    return {
        'schema': 'stoneage.world35.capture_item_source.r1',
        'scope': 'PRESERVED_MIXED25_X86_ITEM_CALLBACK_AND_CAPTURE_SCORE_TAIL',
        'archive_sha256': ARCHIVE_SHA, 'source_members': witness, 'symbols': symbols,
        'registration_sha256': sha(registration), 'work_key': WORK_KEY,
        'source_windows': [[a, b, sha(take(a, b-a))] for a, b in CODE + DATA],
        'stub_names_by_address': STUBS, 'roll_constants': list(struct.unpack('<ddf', take(0x5a9e80, 20))),
        'fixture': {'actor': ACTOR, 'teammate': TEAMMATE, 'wild': WILD,
                    'actor_slot': ACTOR_SLOT, 'teammate_slot': TEAMMATE_SLOT, 'wild_slot': WILD_SLOT,
                    'inventory_slot': ITEM_SLOT, 'base_score': 10.0, 'score_rand': 0,
                    'x87_control_word': X87_RESET_CONTROL},
        'alternate_item_source': alternate_source,
        'item_rows': rows, 'ordinary_cases': ordinary, 'control_cases': probes,
        'world34_useaction_correction': {'schema_evidence': schema, 'rechecks': field_rechecks(take, field_rows)},
        'original_process_started': False, 'capture_ownership_executed': False, 'network_messages_delivered': False,
        'historical_official_deployment_verified': False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('extracted', type=Path)
    args = parser.parse_args()
    print(json.dumps(derive(args.archive, args.extracted), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
