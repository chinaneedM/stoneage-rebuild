"""Replay preserved mixed25 field item intake and recovery against offline fixture memory."""

import argparse
import json
from pathlib import Path
import re
import struct
import zlib

from tools.stoneage_battle_item_gate_source import (
    CLIENT, CLIENT_CODE, CLIENT_DATA, SCENE33, client_image, client_selection, map_windows,
)
from tools.stoneage_cooking_source import source_rows
from tools.stoneage_recovery_callback_replay import CODE as RECOVERY_CODE, DATA as RECOVERY_DATA, X87_RESET_CONTROL
from tools.stoneage_recovery_source import RNG_HIGH, verified_sources
from tools.stoneage_savepoint_item_source import original_image
from tools.stoneage_scene33_source_pair import ARCHIVE_SHA, ROOT, sha
from tools.stoneage_world34_mapped_pe_source import REPORT as WORLD34_R2

REPORT = ROOT / 'research/recovered/STONEAGE-STAGE-A-WORLD34-R3-FIELD-ITEM-REPLAY-R1.json'
ITEM_IDS = (1232, 12530, 12555)
SYMBOLS = {
    '_lssproto_ID_recv': 0x413130, '_CHAR_ItemUse': 0x4746e0,
    '_CHAR_getCharPet': 0x42ea10, '_CHAR_getPartyIndex': 0x42b560,
    '_ITEM_getFunctionPointer': 0x4f7fb0, '_ITEM_useRecovery': 0x500590,
    '_ITEM_useRecovery_Field': 0x4fe4d0, '__CHAR_setInt': 0x42dcf0,
    '__CHAR_DelItem': 0x433ab0, '__ITEM_endExistItemsOne': 0x4f72a0,
}
CODE = (
    (0x413130, 0x4132a0), (0x4746e0, 0x474aae),
    (0x42b560, 0x42b636), (0x42d960, 0x42da60), (0x42db90, 0x42dbac),
    (0x42dc30, 0x42dcf0), (0x42dcf0, 0x42ddc0), (0x42ddc0, 0x42de30),
    (0x42e190, 0x42e208), (0x42e2e0, 0x42e3b0), (0x42e670, 0x42e67a),
    (0x42ea10, 0x42eaa5), (0x433ab0, 0x433c40), (0x4f71b0, 0x4f7220),
    (0x4f72a0, 0x4f7460), (0x4f7500, 0x4f7640), (0x4f76e0, 0x4f7777),
    (0x4f7fb0, 0x4f8070), RECOVERY_CODE[0],
)
DATA = (*RECOVERY_DATA, (0x569b24, 0x569b2c), (0x5a4a6b, 0x5a4a6c))
STUBS = {
    0x409800: 'connection_actor', 0x40ae20: 'client_connection', 0x40b000: 'logged_in',
    0x442340: 'position_update', 0x417f40: 'item_log', 0x43c660: 'action_notice',
    0x4335f0: 'can_cure', 0x438840: 'parameter_recalculation',
    0x43af80: 'nearby_status_notice', 0x43d9d0: 'player_status_notice',
    0x43eaa0: 'pet_status_notice', 0x43e2a0: 'party_update',
    0x43f040: 'display_name', 0x471f90: 'client_text', 0x473740: 'inventory_notice',
    0x55ad30: 'diagnostic_context', 0x55af50: 'diagnostic_log', 0x55ae20: 'diagnostic_output',
    0x55b000: 'message_format', 0x55b030: 'rand', 0x55b130: 'strstr', 0x55afd0: 'scan_int',
}
CHAR_TABLE, ITEM_TABLE, STACK, STOP = 0x710000, 0x700000, 0x800000, 0x731000
ACTOR, PET, PARTY, SLOT = 8, 10, 9, 7
CHAR_STRIDE, WORK_OFFSET, ITEMS_OFFSET = 0x24a4, 0x1f74, 0x4c0


def replay(take, item, option, request, *, rand=0, hp=100, mp=10, item_present=True,
           pet_present=True, party_present=True, work64=0, battle_mode=0, can_cure=True, useaction=0):
    from unicorn import (
        Uc, UcError, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE, UC_HOOK_MEM_INVALID,
        UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE, UC_PROT_READ, UC_PROT_WRITE,
    )
    from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_EIP, UC_X86_REG_ESP, UC_X86_REG_FPCW

    cpu = Uc(UC_ARCH_X86, UC_MODE_32)
    map_windows(cpu, take, CODE + DATA, (*STUBS, STOP))
    for address, size in ((0x5ab000, 0x1000), (0x61b000, 0x1000), (0x6c6000, 0x1000),
                          (CHAR_TABLE, 0x1a000), (ITEM_TABLE, 0x1000), (STACK, 0x4000)):
        cpu.mem_map(address, size, UC_PROT_READ | UC_PROT_WRITE)

    def put(address, *values):
        cpu.mem_write(address, struct.pack(f'<{len(values)}i', *values))

    def read(address):
        return struct.unpack('<i', cpu.mem_read(address, 4))[0]

    def args(count):
        address = cpu.reg_read(UC_X86_REG_ESP) + 4
        return list(struct.unpack(f'<{count}i', cpu.mem_read(address, count * 4)))

    def cstring(address):
        result = bytearray()
        for offset in range(256):
            byte = cpu.mem_read(address + offset, 1)
            if byte == b'\0':
                return bytes(result)
            result.extend(byte)
        raise ValueError('Unterminated string in field item replay')

    def strstr():
        text, needle = args(2)
        offset = cstring(text).find(cstring(needle))
        return 0 if offset < 0 else text + offset

    def scan_int():
        text, fmt, output = args(3)
        if cstring(fmt) != b'%d':
            raise ValueError('Unexpected recovery scan format')
        match = re.match(rb'\s*[+-]?\d+', cstring(text))
        if not match:
            return 0
        put(output, int(match[0]))
        return 1

    put(0x5ab500, PET + 1)
    put(0x5ab510, PARTY + 1)
    put(0x6c63f0, CHAR_TABLE)
    watched = {}
    for who, kind in ((ACTOR, 1), (PET, 3), (PARTY, 1)):
        character = CHAR_TABLE + who * CHAR_STRIDE
        put(character, 1)
        put(character + 4 + 0x36 * 4, kind)
        put(character + 4 + 10 * 4, hp, mp)
        put(character + WORK_OFFSET + 13 * 4, 1000, 100)
        put(character + ITEMS_OFFSET, *([-1] * 20))
        put(character + 0x1cbc, *([-1] * 5))
        for field in (10, 11):
            watched[character + 4 + field * 4] = [who, field]
    actor = CHAR_TABLE + ACTOR * CHAR_STRIDE
    slot_address = actor + ITEMS_OFFSET + SLOT * 4
    put(actor + 0x1cbc, PET if pet_present else -1)
    put(actor + WORK_OFFSET, battle_mode)
    put(actor + WORK_OFFSET + 63 * 4, 1, work64, PARTY if party_present else -1)
    put(slot_address, 0 if item_present else -1)

    put(0x61b630, int(item_present))
    put(0x61b640, ITEM_TABLE)
    put(0x61b650, 1)
    put(ITEM_TABLE, int(item_present))
    for key, value in item['ints'].items():
        put(ITEM_TABLE + 4 + 4 * key, value)
    put(ITEM_TABLE + 4 + 46 * 4, useaction)
    put(ITEM_TABLE + 0x720 + 19 * 4, SYMBOLS['_ITEM_useRecovery'])
    cpu.mem_write(ITEM_TABLE + 0x10c + 3 * 64, option + b'\0')

    initial_stack = STACK + 0x3f00
    put(initial_stack, STOP, 4, 0, 0, SLOT, request)
    cpu.reg_write(UC_X86_REG_ESP, initial_stack)
    cpu.reg_write(UC_X86_REG_FPCW, X87_RESET_CONTROL)

    trace = {key: [] for key in ('item_use_args', 'callback_args', 'int_keys', 'work_keys',
                                 'stat_writes', 'delete_args', 'inventory_writes', 'fixture_calls')}
    trace.update(callback_returned=False, field_callback_entered=False)
    stub_values = {
        0x409800: lambda: ACTOR, 0x40ae20: lambda: 1, 0x40b000: lambda: 1,
        0x4335f0: lambda: int(can_cure), 0x43f040: lambda: ITEM_TABLE + 0x10c,
        0x55ad30: lambda: ITEM_TABLE + 0xc00, 0x55b030: lambda: rand,
        0x55b130: strstr, 0x55afd0: scan_int,
    }

    def instruction(machine, address, size, _context):
        if address in STUBS:
            trace['fixture_calls'].append(STUBS[address])
            handler = stub_values.get(address)
            machine.reg_write(UC_X86_REG_EAX, handler() if handler else 0)
            return
        if not any(first <= address and address + size <= end for first, end in CODE):
            raise ValueError(f'Field item replay left approved code at {address:#x}')
        if address == 0x4746e0:
            trace['item_use_args'] = args(3)
        elif address == 0x500590:
            trace['callback_args'] = args(3)
        elif address == 0x474a06:
            trace['callback_returned'] = True
        elif address == 0x4fe4d0:
            trace['field_callback_entered'] = True
        elif address == 0x4f7500:
            trace['int_keys'].append(args(4)[3])
        elif address == 0x42ddc0:
            trace['work_keys'].append(args(4)[2:4])
        elif address == 0x433ab0:
            trace['delete_args'].append(args(6)[2:6])

    def write(_cpu, _access, address, size, value, _context):
        signed_value = struct.unpack('<i', struct.pack('<I', value & 0xffffffff))[0]
        if address in watched and size == 4:
            trace['stat_writes'].append([*watched[address], signed_value])
        if address == slot_address and size == 4:
            trace['inventory_writes'].append(signed_value)

    item_reads = set()

    def item_read(_cpu, _access, address, size, _value, _context):
        item_reads.add((address - ITEM_TABLE, size))

    faults = []

    def invalid(machine, _access, address, _size, _value, _context):
        faults.append([machine.reg_read(UC_X86_REG_EIP), address])
        return False

    cpu.hook_add(UC_HOOK_MEM_INVALID, invalid)
    cpu.hook_add(UC_HOOK_CODE, instruction)
    cpu.hook_add(UC_HOOK_MEM_READ, item_read, begin=ITEM_TABLE, end=ITEM_TABLE + 0x783)
    cpu.hook_add(UC_HOOK_MEM_WRITE, write, begin=CHAR_TABLE, end=CHAR_TABLE + 0x19fff)
    try:
        cpu.emu_start(SYMBOLS['_lssproto_ID_recv'], STOP, count=30000)
    except UcError as error:
        # Invalid target -1 is passed to the unchecked character integer accessor.
        # Guard the preceding record instead of supplying made-up out-of-table memory.
        if (faults == [[0x42dba8, CHAR_TABLE - CHAR_STRIDE + 4 + 0x36 * 4]]
                and trace['item_use_args'] == [ACTOR, -1, SLOT]
                and not trace['callback_args'] and not trace['stat_writes'] and not trace['inventory_writes']):
            trace['guarded_target_read'] = faults[0]
        else:
            raise ValueError(f'Field item {item["id"]}, target {request}, fault {faults}, trace {trace}') from error
    returned = cpu.reg_read(UC_X86_REG_EIP) == STOP and cpu.reg_read(UC_X86_REG_ESP) == initial_stack + 4
    if not returned and 'guarded_target_read' not in trace:
        raise ValueError('Field item intake did not return to its caller')
    trace.update(intake_returned=returned, item_reads=sorted(item_reads), slot_before=0 if item_present else -1, slot_after=read(slot_address),
                 item_live_after=read(ITEM_TABLE), active_item_count_after=read(0x61b630))
    return trace


def derive(archive, extracted):
    members, witness = verified_sources(archive, extracted)
    server = members['gmsv/gmsv.exe']
    _, take, _, _, symbols = original_image(server, SYMBOLS)
    r2 = json.loads(WORLD34_R2.read_bytes())
    mapped_hashes = {section['name']: sha(server[section['raw_offset']:section['raw_end']])
                     for section in r2['pe']['sections']}
    if mapped_hashes != {section['name']: section['sha256'] for section in r2['pe']['sections']}:
        raise ValueError('Complete image and R2 mapped sections differ')
    client_raw = (extracted / Path(CLIENT).name).read_bytes()
    client = client_image(client_raw)
    client_witness, = [entry for entry in json.loads(SCENE33.read_bytes())['original_RAR_witness']['members']
                       if entry['target'] == CLIENT]
    with archive.open('rb') as stream:
        stream.seek(client_witness['header_offset'])
        if (sha(stream.read(client_witness['header_bytes'])) != client_witness['header_sha256']
                or sha(stream.read(client_witness['packed_bytes'])) != client_witness['packed_sha256']
                or zlib.crc32(client_raw) != client_witness['member_crc32']):
            raise ValueError('Preserved client archive member differs')
    if struct.unpack('<I', take(0x55e490, 4))[0] != symbols['_ITEM_useRecovery']:
        raise ValueError('Original recovery registration differs')
    source_rows_by_id = {int(row[16]): (line, physical, row)
                         for line, physical, row in source_rows(members['gmsv/data/itemset.txt'], 94)
                         if row[16] in {str(item).encode() for item in ITEM_IDS}}
    items = []
    options = {}
    for expected in r2['item_original_rows']:
        item_id = expected['id']
        line, physical, fields = source_rows_by_id[item_id]
        if sha(physical) != expected['row_sha256'] or sha(fields[3]) != expected['argument_sha256']:
            raise ValueError('Original recovery row differs')
        if fields[10] != b'ITEM_useRecovery' or fields[62]:
            raise ValueError('Unexpected original callback or action field')
        ints = {key: int(fields[column]) for key, column in ((0, 16), (3, 19), (4, 20), (5, 21))}
        items.append({'id': item_id, 'line': line, 'row_sha256': sha(physical),
                      'option_sha256': sha(fields[3]), 'ints': ints, 'raw_useaction_empty': True,
                      'client_field_gate': client_selection(client, ints[4], ints[5], 2, 7)['field_use_gate_passed']})
        options[item_id] = fields[3]
    if [item['id'] for item in items] != list(ITEM_IDS):
        raise ValueError('Original item test set differs')
    scenarios = [(f'{label}_{endpoint}', request, {'rand': random})
                 for label, request in (('self', 0), ('pet', 1), ('party', 6))
                 for endpoint, random in (('min', 0), ('max', RNG_HIGH))]
    scenarios += [
        ('invalid_target', 11, {}), ('empty_pet', 1, {'pet_present': False}),
        ('empty_party', 6, {'party_present': False}), ('empty_slot', 0, {'item_present': False}),
        ('work64_blocked', 0, {'work64': 1}), ('battle_mode_blocked', 0, {'battle_mode': 2}),
        ('cure_denied', 0, {'can_cure': False}), ('near_cap', 0, {'hp': 980, 'mp': 95}),
        ('no_useaction', 0, {'useaction': -1}),
    ]
    cases = [{'item': item['id'], 'scenario': name, 'target_input': request, 'overrides': overrides,
              'trace': replay(take, item, options[item['id']], request, **overrides)}
             for item in items for name, request, overrides in scenarios]
    prefix_bytes = r2['gmsv_decompression']['verified_common_output_prefix_bytes']
    return {
        'schema': 'stoneage.world34.r3.field_item_replay.r1', 'scope': 'PRESERVED_MIXED25_FIELD_INTAKE_FIXTURE',
        'archive_sha256': ARCHIVE_SHA,
        'server_member': next(entry for entry in witness if entry['target'] == 'gmsv/gmsv.exe'),
        'client_member': client_witness, 'r2_mapped_section_sha256': mapped_hashes,
        'original_sha256_at_r2_prefix_length': sha(server[:prefix_bytes]),
        'symbols': symbols, 'stub_names_by_address': STUBS,
        'server_code_windows': [[a, b, sha(take(a, b-a))] for a, b in CODE],
        'server_data_windows': [[a, b, sha(take(a, b-a))] for a, b in DATA],
        'client_windows': [[a, b, sha(client(a, b-a))] for a, b in CLIENT_CODE + CLIENT_DATA],
        'common_fixture': {'actor': ACTOR, 'pet': PET, 'party': PARTY, 'slot': SLOT,
                           'initial_hp_mp': [100, 10], 'max_hp_mp': [1000, 100], 'empty_useaction_value': 0,
                           'random_inputs': [0, RNG_HIGH], 'x87_control_word': X87_RESET_CONTROL},
        'items': items, 'cases': cases,
        'original_process_started': False, 'live_inventory_changed': False, 'network_messages_delivered': False,
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
