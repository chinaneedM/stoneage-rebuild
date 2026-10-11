"""Hash-pinned, non-executing I22/S46-I/SI24 inventory layout analysis.

Produces derived operand/control metadata only. It neither runs original code
nor treats client display slots as physical server item IDs or persistent owners.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct

from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_OP_REG
from tools.stoneage_jss_launcher_deep_probe import parse_pe_layout
from tools.stoneage_wayi_pet_sender_probe import EXPECTED_BYTES, EXPECTED_SHA256
from tools.stoneage_wayi_pet_state_probe import (
    probe as pet_probe, resolve_indexed_switch, loop_values,
)
from tools.stoneage_wayi_pet_transport_probe import summarize_window
from tools.stoneage_wayi_saupdate_route_probe import decode_window, raw_window

FIELDS = ['name', 'name2', 'color', 'memo', 'graNo', 'field', 'target',
          'level', 'sendFlag', 'damage', 'pile', 'alch', 'type', 'jigsaw']
OFFSETS = [230, 259, 0, 276, 4, 222, 224, 8, 228, 361, 12, 16, 377, 378]
WIDTHS = [None, None, 4, None, 4, 2, 2, 4, 2, None, 4, None, 1, None]


def slot_scale(instructions, initial):
    """Restricted linear slot multipliers; unknown/partial operations fail."""
    regs = dict(initial)
    def value(reg):
        if reg not in regs:
            raise ValueError('Unknown multiplier register: ' + reg)
        return regs[reg]
    for ins in instructions:
        ops = ins.operands
        if not ins.id or len(ops) != 2 or ops[0].type != X86_OP_REG or ops[0].size != 4:
            raise ValueError('Unsupported multiplier destination')
        dst = ins.reg_name(ops[0].reg)
        if ins.mnemonic == 'lea' and ops[1].type == X86_OP_MEM:
            m = ops[1].mem
            if m.disp or m.scale not in (1, 2, 4, 8):
                raise ValueError('Nonlinear/displaced multiplier')
            regs[dst] = ((value(ins.reg_name(m.base)) if m.base else 0) +
                         (value(ins.reg_name(m.index)) * m.scale if m.index else 0))
        elif ins.mnemonic == 'shl' and ops[1].type == X86_OP_IMM and 0 <= ops[1].imm <= 31:
            regs[dst] = value(dst) * (1 << ops[1].imm)
        elif ins.mnemonic == 'add' and ops[1].type == X86_OP_REG and ops[1].size == 4:
            regs[dst] = value(dst) + value(ins.reg_name(ops[1].reg))
        else:
            raise ValueError('Unsupported multiplier instruction')
    return regs


def row_positions(row, item_fields=14):
    """Bounded hypothetical field indices, not a native packet parser."""
    if type(row) is not int or not 0 <= row <= 65535 or type(item_fields) is not int or not 1 <= item_fields <= 32:
        raise ValueError('Row/field bounds')
    start = row * (item_fields + 1)
    return {'slot': start + 1, 'name': start + 2, 'last_item_field': start + item_fields + 1}


def layout_signature(rows):
    if len(rows) != 14:
        raise ValueError('Missing inventory fields')
    signature = []
    for row in sorted(rows, key=lambda x: x['item_field']):
        i = row['item_field']
        if type(i) is not int or not 1 <= i <= 14 or row['label'] != FIELDS[i - 1]:
            raise ValueError('Wrong field identity')
        offset = row['offset']
        kind, width = row['kind'], row['width_bytes']
        if type(offset) is not int or not 0 <= offset < 388:
            raise ValueError('Record offset outside observed stride')
        if kind == 'numeric':
            if width not in (1, 2, 4) or offset + width > 388:
                raise ValueError('Numeric field width')
        elif kind != 'string' or width is not None:
            raise ValueError('String capacity inferred without evidence')
        signature.append((i, row['label'], offset, kind, width))
    if [x[0] for x in signature] != list(range(1, 15)):
        raise ValueError('Duplicate field identity')
    return signature


def same_layout(*layouts):
    signatures = [layout_signature(rows) for rows in layouts]
    return bool(signatures) and all(s == signatures[0] for s in signatures[1:])


def probe(payload):
    if len(payload) != EXPECTED_BYTES or hashlib.sha256(payload).hexdigest() != EXPECTED_SHA256:
        raise ValueError('Expected exact accepted decompressed game specimen')
    layout = parse_pe_layout(payload)
    base = struct.unpack_from('<I', payload, layout['pe_off'] + 52)[0]
    def window(a, b):
        return decode_window(raw_window(payload, layout, a, b), base + a)
    dispatch = window(0x90c3f, 0x90c82)
    delta = window(0x646b0, 0x64afe)
    full = window(0x61697, 0x619db)
    swap = window(0x7c8b0, 0x7ca49)
    d = {i.address - base: i for i in delta}
    f = {i.address - base: i for i in full}
    def immediate(by, rva, mnemonic, index=1):
        ins = by[rva]
        if ins.mnemonic != mnemonic or ins.operands[index].type != X86_OP_IMM:
            raise ValueError('Changed immediate structure')
        return ins.operands[index].imm
    if dispatch[0].operands[1].imm != 22 or d[0x646b0].mnemonic != 'mov':
        raise ValueError('Changed I22 route')
    dispatcher = {i.address - base: i for i in dispatch}
    if dispatcher[0x90c67].mnemonic != 'jne' or dispatcher[0x90c67].operands[0].imm - base != 0x92484:
        raise ValueError('Changed string-checksum callback gate')
    callback = next(i for i in dispatch if i.address - base == 0x90c7a)
    if callback.mnemonic != 'call' or callback.operands[0].imm - base != 0x646b0:
        raise ValueError('Changed I22 callback')
    step = immediate(d, 0x64ab6, 'add')
    if step != 15 or d[0x64aed].mnemonic != 'jne' or d[0x64aed].operands[0].imm - base != 0x6470d:
        raise ValueError('Changed incremental record loop')
    if immediate(d, 0x64aea, 'cmp') != 1:
        raise ValueError('Changed name-token termination condition')
    origin = d[0x6481b].operands[0].mem.disp - base
    # ECX is repurposed for strlen between the two EBX address operations.
    multipliers = slot_scale(window(0x64757, 0x6475f), {'ebx': 1, 'ecx': 1})
    scale = slot_scale(window(0x64762, 0x64765), multipliers)['ebx']
    if scale != 388:
        raise ValueError('Changed incremental item stride')
    numeric = [(3, 0x6481b), (5, 0x648a9), (6, 0x648b8), (7, 0x648d2),
               (8, 0x6490d), (9, 0x64933), (11, 0x649d8), (13, 0x64a56)]
    strings = [(1, 0x64785), (2, 0x647f0), (4, 0x6487e),
               (10, 0x64975), (12, 0x649fc), (14, 0x64a7d)]
    delta_fields = []
    for i, rva in numeric:
        op = d[rva].operands[0]
        delta_fields.append({'item_field': i, 'wire_token_within_record': i + 1,
            'label': FIELDS[i - 1], 'offset': op.mem.disp - base - origin,
            'kind': 'numeric', 'width_bytes': op.size, 'write_rva': rva})
    for i, rva in strings:
        op = d[rva].operands[1]
        delta_fields.append({'item_field': i, 'wire_token_within_record': i + 1,
            'label': FIELDS[i - 1], 'offset': op.mem.disp - base - origin,
            'kind': 'string', 'width_bytes': None, 'destination_rva': rva})
    delta_fields.sort(key=lambda x: x['item_field'])
    # Full S46/I uses an EBP pointer to useFlag, not to record origin.
    flag_origin = immediate(f, 0x616a1, 'mov') - base
    flag_offset = d[0x6476a].operands[0].mem.disp - base - origin
    full_fields = []
    for i, rva in [(3, 0x61789), (5, 0x61808), (6, 0x61817), (7, 0x6182e),
                   (8, 0x6185d), (9, 0x61880), (11, 0x6190d), (13, 0x61963)]:
        op = f[rva].operands[0]
        full_fields.append({'item_field': i, 'label': FIELDS[i - 1],
            'offset': op.mem.disp + flag_offset, 'kind': 'numeric',
            'width_bytes': op.size, 'write_rva': rva})
    for i, rva in [(1, 0x61708), (2, 0x61761), (4, 0x617e0),
                   (10, 0x618b6), (12, 0x6192b), (14, 0x6199b)]:
        full_fields.append({'item_field': i, 'label': FIELDS[i - 1],
            'offset': f[rva].operands[1].mem.disp + flag_offset,
            'kind': 'string', 'width_bytes': None, 'destination_rva': rva})
    full_fields.sort(key=lambda x: x['item_field'])
    old = pet_probe(payload)
    pet_fields = [{'item_field': x['token_within_slot'],
                   'label': x['semantic_label_from_source'], 'offset': x['offset_in_record'],
                   'kind': 'numeric', 'width_bytes': x['width_bytes']}
                  for x in old['numeric_field_writes']]
    pet_fields += [{'item_field': x['token_within_slot'],
                    'label': x['semantic_label_from_source'], 'offset': x['offset_in_record'],
                    'kind': 'string', 'width_bytes': None} for x in old['string_destinations']]
    if flag_origin - flag_offset != origin or not same_layout(delta_fields, full_fields, pet_fields):
        raise ValueError('Incremental/full/PET item layout differs')
    switch = resolve_indexed_switch(payload, layout, 0x42, 23, 0x620d0, 0x62094, 15, base)
    category = next(x for x in switch if x['input_byte'] == ord('I'))
    if category['target_rva'] != 0x61697:
        raise ValueError('Changed S46/I category')
    start = immediate(f, 0x61697, 'mov')
    full_step = immediate(f, 0x619b7, 'add')
    full_limit = immediate(f, 0x619c0, 'cmp')
    if (full_step, immediate(f, 0x619ba, 'add')) != (14, scale):
        raise ValueError('Changed full item stride')
    if f[0x619ca].mnemonic != 'jl' or f[0x619ca].operands[0].imm - base != 0x616a6:
        raise ValueError('Changed full signed exclusive backedge')
    swap_scale = slot_scale(window(0x7c8ca, 0x7c8e0), {'eax': 1, 'ecx': 1})
    if swap_scale['esi'] != scale or swap_scale['edi'] != scale:
        raise ValueError('Changed swap address stride')
    swap_numeric = sorted({(i.operands[0].mem.disp - base - origin, i.operands[0].size)
        for i in swap if i.mnemonic == 'mov' and i.operands[0].type == X86_OP_MEM})
    swap_strings = sorted({i.operands[1].mem.disp - base - origin
        for i in swap if i.mnemonic == 'lea' and i.operands[1].mem.disp >= base + origin})
    if 16 in swap_strings or swap_strings != [230, 259, 276, 361, 378]:
        raise ValueError('Changed selective string swap')
    s = {i.address - base: i for i in swap}
    if any(s[rva].mnemonic != 'jl' or s[rva].operands[0].imm - base != 0x7ca48
           for rva in (0x7c8b6, 0x7c8c2)):
        raise ValueError('Changed negative swap-index guards')
    si = {i.address - base: i for i in window(0x90c96, 0x90ce9)}
    si_fields = [immediate(si, rva, 'push', 0) for rva in (0x90ca0, 0x90cae, 0x90cbc)]
    if si_fields != [2, 3, 4] or si[0x90ccc].mnemonic != 'jne' or si[0x90ccc].operands[0].imm - base != 0x92484:
        raise ValueError('Changed SI24 integer/checksum route')
    windows = []
    for label, a, b in [('I22-dispatch', 0x90c3f, 0x90c82),
            ('I22-incremental', 0x646b0, 0x64afe), ('S46-I-full', 0x61697, 0x619db),
            ('SI24-dispatch', 0x90c96, 0x90ce9), ('SI24-callback', 0x64690, 0x646ac),
            ('selective-item-swap', 0x7c8b0, 0x7ca49)]:
        windows.append({'label': label, 'start_rva': a, 'end_rva_exclusive': b,
                        **summarize_window(window(a, b), base, {})})
    return {'schema': 'STONEAGE-WAYI-INVENTORY-STATE-PROBE-R1',
        'input_bytes': len(payload), 'decompressed_input_sha256': EXPECTED_SHA256,
        'evidence_status': 'STATIC_COMPILED_CLIENT_DISPLAY_STATE_NOT_NATIVE_RUNTIME',
        'record_origin_rva': origin, 'record_stride_bytes': scale,
        'use_flag_offset': flag_offset, 'incremental_fields': delta_fields,
        'full_fields': full_fields, 'three_paths_share_field_layout': True,
        'incremental': {'logical_id': 22, 'callback_rva': 0x646b0,
            'tokens_per_record': step, 'slot_token': 1, 'first_name_token': 2,
            'item_fields_per_record': step - 1, 'name_missing_return_code': 1,
            'empty_clear_width_bytes': d[0x6473a].operands[0].size,
            'empty_clear_offset': d[0x6473a].operands[0].mem.disp - base - origin,
            'jigsaw_helper_limit_argument': immediate(d, 0x64a50, 'push', 0),
            'observed_upper_slot_guard': False},
        'full': {'logical_id': 46, 'category': 'I', 'branch_rva': category['target_rva'],
            'loop_start': start, 'loop_step': full_step, 'exclusive_limit': full_limit,
            'loop_values': loop_values(start, full_step, full_limit),
            'slots_iterated': len(loop_values(start, full_step, full_limit)),
            'empty_clear_width_bytes': f[0x616d9].operands[0].size,
            'empty_clear_offset': flag_offset,
            'jigsaw_copy_length_guard': immediate(f, 0x61989, 'cmp')},
        'swap': {'logical_id': 24, 'callback_rva': 0x64690, 'helper_rva': 0x7c8b0,
            'integer_fields_then_checksum': si_fields,
            'numeric_offsets_and_widths': [list(x) for x in swap_numeric],
            'string_offsets': swap_strings, 'alch_offset16_exchanged': False,
            'negative_index_guards': True, 'observed_upper_slot_guard': False},
        'pet_empty_clear_bytes': old['empty_record_clear_bytes'],
        'windows': windows, 'original_program_executed': False,
        'wire_packet_captured': False, 'matching_server_verified': False,
        'native_owner_lifecycle_verified': False, 'early_version_promoted': False}


def validate(report):
    expected = {'schema': 'STONEAGE-WAYI-INVENTORY-STATE-PROBE-R1',
        'input_bytes': EXPECTED_BYTES, 'decompressed_input_sha256': EXPECTED_SHA256,
        'evidence_status': 'STATIC_COMPILED_CLIENT_DISPLAY_STATE_NOT_NATIVE_RUNTIME',
        'record_origin_rva': 0x431296c, 'record_stride_bytes': 388,
        'use_flag_offset': 220, 'three_paths_share_field_layout': True,
        'pet_empty_clear_bytes': 388}
    if any(report.get(k) != v for k, v in expected.items()):
        raise ValueError('Changed specimen/evidence identity')
    if not same_layout(report['incremental_fields'], report['full_fields']):
        raise ValueError('Layout comparison changed')
    signature = [(i + 1, FIELDS[i], OFFSETS[i],
                  'string' if WIDTHS[i] is None else 'numeric', WIDTHS[i]) for i in range(14)]
    if layout_signature(report['incremental_fields']) != signature:
        raise ValueError('Changed pinned storage profile')
    wanted = {'incremental': {'logical_id': 22, 'tokens_per_record': 15,
                             'slot_token': 1, 'first_name_token': 2,
                             'item_fields_per_record': 14, 'empty_clear_width_bytes': 2,
                             'empty_clear_offset': 220, 'observed_upper_slot_guard': False,
                             'name_missing_return_code': 1, 'jigsaw_helper_limit_argument': 9},
              'full': {'logical_id': 46, 'category': 'I', 'slots_iterated': 24,
                       'loop_values': loop_values(2, 14, 338), 'empty_clear_width_bytes': 2,
                       'empty_clear_offset': 220, 'jigsaw_copy_length_guard': 10},
              'swap': {'logical_id': 24, 'alch_offset16_exchanged': False,
                       'string_offsets': [230, 259, 276, 361, 378],
                       'numeric_offsets_and_widths': [[0,4],[4,4],[8,4],[12,4],[220,2],
                                                     [222,2],[224,2],[226,2],[228,2],[377,1]],
                       'integer_fields_then_checksum': [2, 3, 4],
                       'negative_index_guards': True, 'observed_upper_slot_guard': False}}
    for name, fields in wanted.items():
        if any(report[name].get(k) != v for k, v in fields.items()):
            raise ValueError('Changed update/clear/swap boundary')
    for key in ('original_program_executed', 'wire_packet_captured', 'matching_server_verified',
                'native_owner_lifecycle_verified', 'early_version_promoted'):
        if report.get(key) is not False:
            raise ValueError('Unsupported native/server/early claim')
    if 'source_comparison' in report and report['source_comparison'].get('source_native_layout_equivalence') is not False:
        raise ValueError('Source layout identity promoted')
    if 'server_comparison' in report and report['server_comparison'].get('profiles_admitted_as_matching_server') is not False:
        raise ValueError('Server compatibility promoted')
    return report


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('local_decompressed_client', type=Path)
    args = ap.parse_args()
    with args.local_decompressed_client.open('rb') as f:
        payload = f.read(EXPECTED_BYTES + 1)
    print(json.dumps(validate(probe(payload)), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
