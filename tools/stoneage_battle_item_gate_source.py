"""Replay bounded item selection and command intake from the preserved mixed25 pair."""

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import struct
import zlib

from tools.stoneage_recovery_source import REPORT as WORLD31, catalog, verified_sources
from tools.stoneage_savepoint_item_source import original_image
from tools.stoneage_scene33_source_pair import ARCHIVE_SHA, PINS, REPORT as SCENE33, ROOT, canonical, sha
from tools.stoneage_wayi_pe_static_inventory import inventory_pe

REPORT = ROOT / 'research/recovered/STONEAGE-STAGE-A-WORLD33-BATTLE-ITEM-GATE-SOURCE-R1.json'
SCOPE = 'PRESERVED_MIXED25_CLIENT_ITEM_SELECTION_AND_SERVER_B_COMMAND_INTAKE'
CLIENT = 'stoneage2.5/sa_2903.exe'
SERVER_SYMBOLS = {
    '_lssproto_B_recv': 0x414f30,
    '__CHAR_CHECKINDEX': 0x42d960,
    '_CHAR_getInt': 0x42db90,
    '__CHAR_getWorkInt': 0x42ddc0,
    '__CHAR_setWorkInt': 0x42de30,
    '__CHAR_getItemIndex': 0x42e2e0,
    '__ITEM_CHECKINDEX': 0x4f71b0,
    '_ITEM_isTargetValid': 0x4fc070,
    '_checkErrorStatus': 0x5455a0,
    '_BattleCommandDispach': 0x5456a0,
    '_ITEM_itemconfentries': 0x587e60,
}
SERVER_CODE = ((0x414f30, 0x414ff0), (0x42d960, 0x42d998), (0x42db90, 0x42dbac),
               (0x42ddc0, 0x42ded9 + 1), (0x42e2e0, 0x42e3b0), (0x4f71b0, 0x4f7220),
               (0x4fc070, 0x4fc170), (0x5455a0, 0x5469c0))
SERVER_DATA = ((0x593225, 0x59323a), (0x5a49c5, 0x5a4a11), (0x5a8588, 0x5a85cb),
               (0x5a9614, 0x5a9670))
CLIENT_CODE = ((0x404a10, 0x404a38), (0x405d12, 0x405d83),
               (0x433997, 0x4339ce))
CLIENT_DATA = ((0x404dc9, 0x404de9), (0x465514, 0x46551c))
CLIENT_FIELD = 0x2b24ec0
CLIENT_ITEM_STRIDE = 0x9c
ITEM_TABLE = 0x700000
CHAR_TABLE = 0x710000
BATTLE_TABLE = 0x740000
TEXT = 0x730000
STOP = 0x731000
STACK = 0x800000
ACTOR = 8
COMMAND_KEYS = (3, 4, 5, 0)
SERVER_STUBS = {
    0x409800: 'connection_to_character', 0x40a010: 'set_receive_time', 0x40ae20: 'is_client_connection',
    0x40b000: 'is_logged_in', 0x543e80: 'notify_action_setting',
    0x55ad30: 'libc_diagnostic_stream', 0x55af50: 'libc_diagnostic',
    0x55af60: 'memset', 0x55afd0: 'sscanf_ordinary_item_command',
}


def client_image(raw):
    if (len(raw), sha(raw)) != PINS[CLIENT]:
        raise ValueError('Complete preserved client differs')
    sections = inventory_pe(raw)['sections']
    pe = struct.unpack_from('<I', raw, 0x3c)[0]
    base = struct.unpack_from('<I', raw, pe + 24 + 28)[0]

    def take(va, size):
        for section in sections:
            delta = va - base - section['rva']
            if 0 <= delta and delta + size <= section['raw_size']:
                start = section['raw_offset'] + delta
                return raw[start:start + size]
        raise ValueError('Client window outside original raw sections')

    return take


def map_windows(cpu, take, windows, stubs=()):
    from unicorn import UC_PROT_READ, UC_PROT_EXEC

    mapped = set()
    for start, payload in [(a, take(a, b - a)) for a, b in windows] + [(a, b'\xc3') for a in stubs]:
        for page in range(start & ~0xfff, (start + len(payload) + 0xfff) & ~0xfff, 0x1000):
            if page not in mapped:
                cpu.mem_map(page, 0x1000, UC_PROT_READ | UC_PROT_EXEC)
                mapped.add(page)
        cpu.mem_write(start, payload)


def server_command(take, field, target, side, command, *, item_present=True, logged_in=True):
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
    from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_EIP, UC_X86_REG_ESP

    cpu = Uc(UC_ARCH_X86, UC_MODE_32)
    map_windows(cpu, take, SERVER_CODE + SERVER_DATA, (*SERVER_STUBS, STOP))
    for start, size in ((0x5ab000, 0x1000), (0x61b000, 0x1000), (0x6c6000, 0x1000),
                        (ITEM_TABLE, 0x1000), (CHAR_TABLE, 0x15000), (BATTLE_TABLE, 0x1000),
                        (TEXT, 0x1000), (STACK, 0x4000), (0x2030000, 0x2000)):
        cpu.mem_map(start, size)

    def put(addr, *values):
        cpu.mem_write(addr, struct.pack('<' + 'i' * len(values), *values))

    def args(count):
        sp = cpu.reg_read(UC_X86_REG_ESP) + 4
        return struct.unpack('<' + 'i' * count, cpu.mem_read(sp, count * 4))

    actor = CHAR_TABLE + ACTOR * 0x24a4
    work = actor + 0x1f74
    put(0x5ab500, ACTOR + 1)
    put(0x6c63f0, CHAR_TABLE)
    put(actor, 1)
    put(actor + 4 + 0x36 * 4, 1)
    for key, value in {0: 2, 1: 0, 2: side, 3: -1, 4: -1, 5: -1}.items():
        put(work + key * 4, value)
    put(actor + 0x4c0 + 7 * 4, 0 if item_present else -1)
    put(0x61b640, ITEM_TABLE)
    put(0x61b650, 1)
    put(ITEM_TABLE, 1)
    put(ITEM_TABLE + 0x14, field, target)
    put(0x2030410, 1)
    put(0x2031a90, BATTLE_TABLE)
    put(BATTLE_TABLE + 0x0c, 2)
    cpu.mem_write(TEXT, command.encode('ascii') + b'\0')
    put(STACK + 0x3f00, STOP, 4, TEXT)
    cpu.reg_write(UC_X86_REG_ESP, STACK + 0x3f00)
    parsed, item_reads, writes, notices = [], [], [], []

    def scan():
        text, fmt, slot_out, target_out = args(4)
        if cpu.mem_read(fmt, 6) != b'%X|%X\0' or text != TEXT + 2:
            raise ValueError('Unexpected command parser call')
        body = command[2:]
        match = re.fullmatch(r'([0-9A-F]+)\|([0-9A-F]+)', body)
        if match:
            slot, requested = (int(part, 16) for part in match.groups())
            put(slot_out, slot)
            put(target_out, requested)
            parsed.extend((slot, requested))
            return 2
        if body == 'GG|7':
            return 0
        raise ValueError('Command is outside the bounded scanf fixtures')

    def fill():
        ptr, value, size = args(3)
        if size != 255 or value != 0:
            raise ValueError('Unexpected command buffer initialization')
        cpu.mem_write(ptr, bytes(size))
        return ptr

    def notice():
        notices.append(args(1)[0])
        return 0

    callbacks = {
        0x409800: lambda: ACTOR, 0x40a010: lambda: 0, 0x40ae20: lambda: 1, 0x40b000: lambda: int(logged_in),
        0x543e80: notice, 0x55ad30: lambda: BATTLE_TABLE + 0x500, 0x55af50: lambda: 0,
        0x55af60: fill, 0x55afd0: scan,
    }

    def code(machine, address, _size, _context):
        if address in callbacks:
            machine.reg_write(UC_X86_REG_EAX, callbacks[address]())
        elif not any(a <= address < b for a, b in SERVER_CODE):
            raise ValueError(f'Command left approved source windows at {address:#x}')

    def read(_cpu, _access, address, size, _value, _context):
        item_reads.append([address - ITEM_TABLE, size])

    def write(_cpu, _access, address, size, value, _context):
        if size != 4:
            raise ValueError('Unexpected battle work write size')
        writes.append([(address - work) // 4, value])

    cpu.hook_add(UC_HOOK_CODE, code)
    cpu.hook_add(UC_HOOK_MEM_READ, read, begin=ITEM_TABLE, end=ITEM_TABLE + 0x783)
    cpu.hook_add(UC_HOOK_MEM_WRITE, write, begin=work, end=work + 0x1f)
    cpu.emu_start(SERVER_SYMBOLS['_lssproto_B_recv'], STOP, count=4000)
    if cpu.reg_read(UC_X86_REG_EIP) != STOP:
        raise ValueError('Battle command did not return within the bound')
    return {'parsed_slot_target': parsed, 'item_instance_reads': item_reads,
            'battle_work_writes': writes, 'action_setting_calls': notices}


def client_selection(take, field, target, actor_slot, selected_slot, *, occupied=True, required_level=0):
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE
    from unicorn.x86_const import (
        UC_X86_REG_EAX, UC_X86_REG_EBP, UC_X86_REG_EBX, UC_X86_REG_EIP,
        UC_X86_REG_ESI, UC_X86_REG_ESP,
    )

    cpu = Uc(UC_ARCH_X86, UC_MODE_32)
    map_windows(cpu, take, CLIENT_CODE + CLIENT_DATA)
    for page in (0x490000, 0x491000, 0x2b24000, 0x2b25000, STACK):
        cpu.mem_map(page, 0x1000)

    def put(addr, value, size=4):
        cpu.mem_write(addr, value.to_bytes(size, 'little', signed=True))

    slot = 7
    row_field = CLIENT_FIELD + slot * CLIENT_ITEM_STRIDE
    row_name = row_field - 0x92
    put(row_name - 2, int(occupied), 2)
    put(row_field - 4, required_level)
    put(row_field, field, 2)
    put(row_field + 2, target, 2)
    put(0x490d08, slot)
    put(0x491d58, actor_slot)
    cpu.reg_write(UC_X86_REG_ESI, row_name)
    cpu.reg_write(UC_X86_REG_EAX, slot * CLIENT_ITEM_STRIDE)
    cpu.reg_write(UC_X86_REG_EBX, 0)
    cpu.reg_write(UC_X86_REG_EBP, STACK + 0xc00)
    cpu.reg_write(UC_X86_REG_ESP, STACK + 0xc00)
    battle_endpoints = (0x404a38, 0x404a6f, 0x404a8d)
    field_endpoints = (0x4339ce, 0x433ae4)
    gates = battle_endpoints + field_endpoints + (0x405e50, 0x405ecb)

    def stop(machine, address, _size, _context):
        if address in gates:
            machine.emu_stop()
        elif not any(a <= address < b for a, b in CLIENT_CODE):
            raise ValueError(f'Client left approved source windows at {address:#x}')

    cpu.hook_add(UC_HOOK_CODE, stop)
    cpu.emu_start(0x404a10, 0, count=100)
    battle = cpu.reg_read(UC_X86_REG_EIP)
    cpu.reg_write(UC_X86_REG_EAX, slot * CLIENT_ITEM_STRIDE)
    cpu.emu_start(0x433997, 0, count=100)
    field_use = cpu.reg_read(UC_X86_REG_EIP)
    if battle not in battle_endpoints or field_use not in field_endpoints:
        raise ValueError('Client selector did not reach its original branch endpoint')
    result = {'battle_slot_selectable': battle == 0x404a8d, 'field_use_gate_passed': field_use == 0x4339ce,
              'selector_endpoints': [battle, field_use]}
    if result['battle_slot_selectable']:
        cpu.reg_write(UC_X86_REG_EAX, selected_slot)
        cpu.emu_start(0x405d12, 0, count=100)
        endpoint = cpu.reg_read(UC_X86_REG_EIP)
        if endpoint != 0x405e50:
            raise ValueError('Client command formatter was not reached')
        fmt, item, requested = struct.unpack('<3I', cpu.mem_read(cpu.reg_read(UC_X86_REG_ESP), 12))
        if cpu.mem_read(fmt, 8) != b'I|%X|%X\0':
            raise ValueError('Unexpected original client command format')
        result['client_format_args'] = [item, requested]
    return result


def source_evidence(server, client):
    fields = []
    for column, name, key in ((20, 'fieldtype', 4), (21, 'target', 5)):
        entry = server(SERVER_SYMBOLS['_ITEM_itemconfentries'] + column * 16, 16)
        ptr, kind, int_key, _ = struct.unpack('<4I', entry)
        if (kind, int_key, server(ptr, len(name) + 1)) != (0, key, name.encode() + b'\0'):
            raise ValueError('Original item column descriptor differs')
        fields.append({'column_zero_based': column, 'field': name, 'runtime_int_key': key,
                       'item_record_offset': 4 + 4 * key, 'descriptor_sha256': sha(entry)})
    edges = []
    for address, target in ((0x414f82, 0x5456a0), (0x546115, 0x42e2e0),
                            (0x546130, 0x4f71b0), (0x54649c, 0x4fc070)):
        call = server(address, 5)
        if call[0] != 0xe8 or address + 5 + struct.unpack_from('<i', call, 1)[0] != target:
            raise ValueError('Original command call differs')
        edges.append([address, target, sha(call)])
    # GMSV status record formatter and same-pair client record parser. The
    # public receipt keeps source offsets and hashes, not original text.
    self_target_path, = struct.unpack('<I', client(0x404dc9, 4))
    if self_target_path != 0x404ab3:
        raise ValueError('Original client target type 0 picker differs')
    bridge = [('server', 0x4fa43b, 0x4fa4a7, server), ('server', 0x4fa5a1, 0x4fa5e7, server),
              ('client', 0x43de9f, 0x43ded0, client)]
    return {
        'client_target_type_0_picker': {'entry': self_target_path,
                                        'source_sha256': sha(client(self_target_path, 0x404acb - self_target_path))},
        'item_columns': fields, 'server_symbols': SERVER_SYMBOLS, 'server_call_edges': edges,
        'status_record_bridge_windows': [[side, a, b, sha(read(a, b-a))] for side, a, b, read in bridge],
        'server_windows': [[a, b, sha(server(a, b-a))] for a, b in SERVER_CODE + SERVER_DATA],
        'client_windows': [[a, b, sha(client(a, b-a))] for a, b in CLIENT_CODE + CLIENT_DATA],
    }


def derive(archive, extracted):
    import unicorn

    members, receipts = verified_sources(archive, extracted)
    client_raw = (extracted / Path(CLIENT).name).read_bytes()
    client = client_image(client_raw)
    scene33 = json.loads(SCENE33.read_bytes())
    member, = [row for row in scene33['original_RAR_witness']['members'] if row['target'] == CLIENT]
    with archive.open('rb') as stream:
        stream.seek(member['header_offset'])
        if (sha(stream.read(member['header_bytes'])) != member['header_sha256']
                or sha(stream.read(member['packed_bytes'])) != member['packed_sha256']
                or zlib.crc32(client_raw) != member['member_crc32']):
            raise ValueError('Preserved client archive member differs')
    _, server, _, _, _ = original_image(members['gmsv/gmsv.exe'], SERVER_SYMBOLS)
    rows = catalog(members['gmsv/data/itemset.txt'])
    previous = json.loads(WORLD31.read_bytes())
    if sha(canonical(rows)) != previous['catalog']['all_derived_callback_rows_sha256']:
        raise ValueError('Configured recovery row inventory differs from WORLD31')
    counts = Counter((row['scene'], row['target']) for row in rows)
    by_id = {row['id']: row for row in rows}
    exemplars = {}
    for row in rows:
        fields = row['scene'], row['target']
        if fields not in exemplars or exemplars[fields]['raw_hash_prefix']:
            exemplars[fields] = row
    for item_id in (12530, 12555, 12780):
        row = by_id[item_id]
        exemplars[row['scene'], row['target']] = row

    witnesses = []
    for fields, row in sorted(exemplars.items()):
        field, target = fields
        c = client_selection(client, field, target, 2, 2 if target == 0 else 7)
        native = {str(slot): server_command(server, field, target, 0, f'I|7|{slot:X}')
                  for slot in (7, 17, 20, 21, 22, 23)}
        client_command = None
        if c['battle_slot_selectable']:
            slot, requested = c['client_format_args']
            client_command = server_command(server, field, target, 0, f'I|{slot:X}|{requested:X}')
        witnesses.append({'source_rows': counts[fields], 'row': {k: row[k] for k in
                          ('id', 'line', 'row_sha256', 'scene', 'target', 'shape', 'raw_hash_prefix')},
                          'client': c, 'server': native, 'client_command_server_replay': client_command})
    sides = []
    for target in (2, 3, 4):
        for side in (0, 1):
            c = client_selection(client, 0, target, 2 + 10 * side, 7)
            sides.append({'target_type': target, 'caster_side': side, 'client': c,
                          'server': {str(slot): server_command(server, 0, target, side, f'I|7|{slot:X}')
                                     for slot in (20, 21, 22)}})
    negative = {
        'missing_inventory_item': server_command(server, 0, 1, 0, 'I|7|7', item_present=False),
        'malformed_command': server_command(server, 0, 1, 0, 'I|GG|7'),
        'not_logged_in': server_command(server, 0, 1, 0, 'I|7|7', logged_in=False),
    }
    return {'schema': 'stoneage.world33.battle_item_gate_source.r1', 'scope': SCOPE,
            'archive_sha256': ARCHIVE_SHA, 'member_witnesses': receipts + [member],
            'world31_receipt_sha256': sha(WORLD31.read_bytes()), 'configured_recovery_rows': len(rows),
            'program': source_evidence(server, client),
            'fixture': {'engine': f'Unicorn {unicorn.__version__} x86-32', 'item_slot': 7,
                        'client_single_target_slot': 7, 'server_stubbed_functions': SERVER_STUBS,
                        'battle_work_keys': COMMAND_KEYS},
            'source_class_witnesses': witnesses, 'group_target_controls': sides, 'negative_controls': negative,
            'client_selection_controls': {
                'unoccupied_slot': client_selection(client, 0, 1, 2, 7, occupied=False),
                'level_requirement_unmet': client_selection(client, 0, 1, 2, 7, required_level=1),
            },
            'client_or_server_started': False, 'network_packets_sent': False,
            'live_battle_effect_or_inventory_change_observed': False, 'official_same_deployment_proven': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('private_extracted_members', type=Path)
    args = parser.parse_args()
    print(json.dumps(derive(args.archive, args.private_extracted_members), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
