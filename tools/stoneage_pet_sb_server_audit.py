"""Compare two pinned late server source profiles to the accepted S46/B client.

GCC preprocessing only: no original client/server program is built or executed.
The report contains derived metadata, never original source or disassembly.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

from tools.stoneage_enemy_creation_audit import definition

COMMITS = {
    'previous': '999ffdf1d220ec6666eb65339180689c9caf1876',
    'current': '2f736808ff4361f5429ee919b718c88fabb60346',
}
COMMON = {
    'server/gmsv/char/char_item.c': '970b7b3f975965c6c5e77352a2e0382adf943753',
    'server/gmsv/item/item.c': '94b00b11d02cc775bab6fe72c9c2ba77d9618712',
    'server/gmsv/include/item.h': '1823db6f6965063fdc740ac8b6709d679ba27c18',
    'server/gmsv/autil.c': 'c1f4886c879d6d847017cc53373e9e6ead28ae28',
    'server/gmsv/char/pet.c': '5f18dbc539b2177e80c9616f772e0f58be5b8bdf',
}
VARIABLE = {
    'previous': {
        'server/gmsv/include/char_base.h': 'c3a47a05d077604db86101f8ad715f8fa1247ff4',
        'server/gmsv/include/version.h': 'b3fc0c80705973bc8d088287c98a5d66171bb6c2',
        'server/common/gmsv_server_send.c': '84dd1b2d9fbac10fe39983e6b8984aaebf1b3075',
        'server/common/gmsv_server.h': '708fe1b9f73be4952677fda474f10e86d9a56306',
    },
    'current': {
        'server/gmsv/include/char_base.h': '6240ed65076a7b6658bd9cc0e036f079a6c03fc3',
        'server/gmsv/include/version.h': 'cd68519a68a90b1123f298e16afa00d5798cd844',
        'server/common/gmsv_server_send.c': '099efdea50f6dcb4c7fc3a4831d612ea7a2f1b08',
        'server/common/gmsv_server.h': 'da501b1870da38b5628c0ef160d43c8502b35f20',
    },
}
FIELDS = ['name', 'name2', 'color', 'memo', 'graNo', 'field', 'target',
          'level', 'sendFlag', 'damage', 'pile', 'alch', 'type']
CLIENT_FIELDS = FIELDS + ['jigsaw']


def demand(value, message):
    if not value:
        raise ValueError(message)


def format_fields(fmt):
    """Count a restricted delimiter-separated C conversion format, not a C VM."""
    parts = fmt.split('|')
    demand(1 <= len(parts) <= 64, 'format field count out of bounds')
    demand(all(re.fullmatch(r'%[sd]', p) for p in parts), 'unsupported format')
    return [p[1] for p in parts]


def empty_fields(value):
    demand(len(value) <= 63 and set(value) <= {'|'}, 'not a bounded empty row')
    return len(value) + 1


def alignment(sender_width, receiver_width, slots):
    """ASCII delimiter-free synthetic rows only; no wire codec/native parser."""
    demand(all(type(x) is int and 1 <= x <= 64
               for x in (sender_width, receiver_width, slots)), 'alignment bounds')
    result = []
    for slot in range(slots):
        first = slot * receiver_width
        result.append({'client_slot': slot, 'client_first_flat_token': first + 1,
                       'sender_slot_at_client_start': first // sender_width,
                       'sender_field_at_client_start': first % sender_width + 1,
                       'extends_past_sender_payload':
                           first + receiver_width > sender_width * slots})
    return result


def enum_index(text, target):
    """Read a simple preprocessed enum; reject expressions rather than guess."""
    blocks = re.findall(r'\benum\s*(?:\w+\s*)?\{([^{}]*)\}', text, re.S)
    matches = [b for b in blocks if re.search(r'\b' + re.escape(target) + r'\b', b)]
    demand(len(matches) == 1, 'missing or duplicate enum')
    value = -1
    for member in matches[0].split(','):
        member = member.strip()
        if not member:
            continue
        m = re.fullmatch(r'(\w+)(?:\s*=\s*(0x[0-9a-fA-F]+|\d+))?', member)
        demand(m is not None, 'unsupported enum expression')
        value = int(m[2], 0) if m[2] else value + 1
        if m[1] == target:
            return value
    raise ValueError('missing enum member')


def ordered(text, tokens):
    position = -1
    for token in tokens:
        position = text.find(token, position + 1)
        demand(position >= 0, 'missing/reordered statement: ' + token)


def run(args, stdin=None):
    p = subprocess.run(args, input=stdin, text=True, capture_output=True, timeout=60)
    demand(p.returncode == 0, 'preprocess/read failed: ' + p.stderr[-600:])
    return p.stdout


def inspect(profile, root):
    root = root.resolve()
    def git(*args):
        return run(['git', '-C', str(root), *args]).strip()
    demand(git('rev-parse', 'HEAD') == COMMITS[profile], 'checkout commit drift')
    pin = COMMON | VARIABLE[profile]
    raw = {}
    for path, sha in pin.items():
        demand(git('hash-object', path) == sha, 'source blob drift: ' + path)
        raw[path] = (root / path).read_text(encoding='utf-8-sig')
    inc = [root / p for p in ('server/gmsv/include', 'server/gmsv',
           'server/common', 'server/common/utils', 'shared/lua51')]
    flags = ['-I' + str(p) for p in inc]
    dependency_blobs = {}
    def pp(path, enabled=False):
        cmd = ['gcc', '-std=gnu99', *flags, *(['-D_PET_ITEM'] if enabled else [])]
        dependencies = run([*cmd, '-MM', str(root / path)])
        for name in dependencies.replace('\\\n', ' ').split()[1:]:
            p = Path(name)
            if p.is_file():
                rel = p.relative_to(root).as_posix()
                sha = git('rev-parse', 'HEAD:' + rel)
                demand(git('hash-object', rel) == sha, 'dependency drift: ' + rel)
                dependency_blobs[rel] = sha
        return run([*cmd, '-E', '-P', str(root / path)])
    macros = run(['gcc', '-dM', '-E', '-x', 'c', *flags,
                  '-include', 'version.h', '-'], '')
    macro_names = set(re.findall(r'^#define\s+(\w+)', macros, re.M))
    demand('_PET_ITEM' not in macro_names, 'default PET gate changed')
    demand(all(m in macro_names for m in ('_ADD_SHOW_ITEMDAMAGE', '_ITEM_PILENUMS',
                                         '_ALCHEMIST')), 'item field flags changed')
    item = pp('server/gmsv/item/item.c')
    default = pp('server/gmsv/char/char_item.c')
    enabled = pp('server/gmsv/char/char_item.c', True)
    active = definition(item, 'ITEM_makeItemStatusString')
    formats = re.findall(r'"((?:%[sd]\|)+%[sd])"', active)
    widths = [len(format_fields(f)) for f in formats]
    demand(widths == [13, 13], 'active item field profile changed')
    forced_item = definition(pp('server/gmsv/item/item.c', True), 'ITEM_makeItemStatusString')
    demand([len(format_fields(f)) for f in re.findall(r'"((?:%[sd]\|)+%[sd])"', forced_item)]
           == [13, 13], 'forced PET item field profile changed')
    ordered(active[active.index('if (haveitem_index == -1)'):],
            ['escapename, paramshow, itemcolor, escapeeffectstring',
             'ITEM_BASEIMAGENUMBER', 'ITEM_ABLEUSEFIELD', 'ITEM_TARGET',
             'ITEM_LEVEL', 'flg, buff1', 'ITEM_USEPILENUMS', 'INGNAME0', 'ITEM_TYPE'])
    false = definition(item, 'ITEM_makeItemFalseString')
    literals = re.findall(r'"(\|+)"', false)
    demand(len(literals) == 1, 'ambiguous empty item record')
    demand(empty_fields(literals[0]) == 13, 'empty item profile changed')
    demand(not re.search(r'void\s+CHAR_sendPetItemData\s*\([^;{}]*\)\s*\{', default),
           'default PET sender unexpectedly active')
    definition(enabled, 'CHAR_sendPetItemData')
    definition(enabled, 'CHAR_movePetItem')
    pet_slots = enum_index(enabled, 'CHAR_PETITEMNUM')
    equip_slots = enum_index(enabled, 'CHAR_EQUIPPLACENUM')
    demand((pet_slots, equip_slots) == (7, 9), 'slot limits changed')
    data = raw['server/gmsv/char/char_item.c']
    send = definition(data, 'CHAR_sendPetItemData')
    move = definition(data, 'CHAR_movePetItem')
    ordered(send, ['"B%d"', 'i < CHAR_MAXPETITEMHAVE',
                   'ITEM_makeItemStatusString(-1, item_index)',
                   'ITEM_makeItemFalseString()', 'dchop(', 'GmsvServer_S_send('])
    for direction in [('fromindex', 'toindex'), ('toindex', 'fromindex')]:
        a, b = direction
        ordered(move, [f'CHAR_setItemIndex(char_index, {a}, petitem_index)',
                       f'CHAR_setItemIndex(petindex, {b}, charitem_index)',
                       f'CHAR_sendItemDataOne(char_index, {a})',
                       'CHAR_sendPetItemData(char_index, petid)'])
    ordered(move, ['CHAR_complianceParameter(petindex)', '"K%d"',
                   'CHAR_sendStatusString(char_index, token)'])
    # Preserve the surprising occupied-backpack branch comparison, without
    # projecting a descendant source defect into the captured original binary.
    remove = move[move.index('    } else {'):]
    demand('if (ITEM_CHECKINDEX(charitem_index))' in remove and
           '(type - ITEM_PET_HEAD) != toindex' in remove,
           'occupied removal source comparison changed')
    one = definition(data, 'CHAR_sendItemDataOne')
    demand('CHAR_sendItemData(char_index, itemgrp, 1)' in one, 'I update wrapper')
    demand('GmsvServer_I_send' in definition(data, 'CHAR_sendItemData'), 'I handoff')
    ssend = definition(raw['server/common/gmsv_server_send.c'], 'GmsvServer_S_send')
    fd_name = 'fd' if profile == 'previous' else 'client_fd'
    ordered(ssend, ['util_mkstring(buffer, data)', 'util_mkint(buffer, check_sum_calc)',
                    f'util_SendMesg({fd_name}, LSSPROTO_S_SEND, buffer)'])
    header = raw['server/common/gmsv_server.h']
    demand(re.search(r'#define\s+LSSPROTO_S_SEND\s+46\b', header) and
           re.search(r'#define\s+LSSPROTO_I_SEND\s+22\b', header), 'logical IDs')
    autil = raw['server/gmsv/autil.c']
    demand('func + 23' in definition(autil, '_util_SendMesg') and
           'return strlen(value)' in definition(autil, 'util_mkstring'), 'transport')
    return {'commit': COMMITS[profile], 'source_blobs': pin,
            'dependency_blobs': dict(sorted(dependency_blobs.items())),
            'default_pet_item_enabled': False, 'forced_pet_sender_present': True,
            'item_feature_macros': ['_ADD_SHOW_ITEMDAMAGE', '_ITEM_PILENUMS', '_ALCHEMIST'],
            'active_item_field_counts': widths, 'empty_item_fields': 13,
            'pet_slots': pet_slots, 'player_equipment_slots': equip_slots,
            'jigsaw_field_emitted': False, 'sender_client_field_width_matches': False,
            'move_update_order': ['player_item_I22', 'pet_item_S46_B',
                                  'pet_parameter_recalculation', 'pet_status_K'],
            'occupied_remove_compares_item_type_to_backpack_destination': True,
            'occupied_remove_backpack_min': 9, 'pet_type_slot_max': 6,
            's_sender_string_then_checksum': True, 'string_checksum_is_byte_length': True,
            'source_send_offset_if_new_or_80': 23,
            'bounded_sender_body_sha256': hashlib.sha256(send.encode()).hexdigest(),
            'bounded_move_body_sha256': hashlib.sha256(move.encode()).hexdigest()}


def validate(report):
    demand(report.get('schema') == 'STONEAGE-PET-SB-SERVER-COMPARISON-R1', 'schema')
    demand(report.get('client_fields') == CLIENT_FIELDS and
           report.get('server_fields') == FIELDS, 'field mapping')
    demand(set(report.get('profiles', {})) == set(COMMITS), 'profile set')
    for profile, row in report['profiles'].items():
        demand(row.get('commit') == COMMITS[profile] and
               row.get('source_blobs') == COMMON | VARIABLE[profile], 'source identity')
        for key, value in {'default_pet_item_enabled': False,
                           'forced_pet_sender_present': True,
                           'active_item_field_counts': [13, 13], 'empty_item_fields': 13,
                           'pet_slots': 7, 'player_equipment_slots': 9,
                           'jigsaw_field_emitted': False,
                           'sender_client_field_width_matches': False,
                           'move_update_order': ['player_item_I22', 'pet_item_S46_B',
                              'pet_parameter_recalculation', 'pet_status_K'],
                           'occupied_remove_compares_item_type_to_backpack_destination': True,
                           'occupied_remove_backpack_min': 9, 'pet_type_slot_max': 6,
                           's_sender_string_then_checksum': True,
                           'string_checksum_is_byte_length': True,
                           'source_send_offset_if_new_or_80': 23}.items():
            demand(row.get(key) == value, 'unsupported comparison: ' + key)
    demand(report.get('synthetic_alignment') == alignment(13, 14, 7), 'alignment')
    for key in ('original_program_executed', 'wire_packet_captured',
                'matching_server_verified', 'native_owner_lifecycle_verified',
                'exact_2005_release_verified', 'early_version_promoted'):
        demand(report.get(key) is False, 'false runtime/provenance claim: ' + key)
    return report


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for p in COMMITS:
        ap.add_argument('--' + p, type=Path, required=True)
    args = ap.parse_args()
    report = {'schema': 'STONEAGE-PET-SB-SERVER-COMPARISON-R1',
              'profiles': {p: inspect(p, getattr(args, p)) for p in COMMITS},
              'client_fields': CLIENT_FIELDS, 'server_fields': FIELDS,
              'synthetic_alignment': alignment(13, 14, 7),
              'evidence_status': 'SOURCE_PREPROCESSING_COMPARED_TO_COMPILED_CLIENT_NOT_PAIRED_RUNTIME',
              **{k: False for k in ('original_program_executed', 'wire_packet_captured',
                 'matching_server_verified', 'native_owner_lifecycle_verified',
                 'exact_2005_release_verified', 'early_version_promoted')}}
    print(json.dumps(validate(report), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
