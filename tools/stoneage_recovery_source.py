"""Derive WORLD31 from the private mixed25 archive and three extracted members."""

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import struct
import zlib

from tools.stoneage_cooking_source import REPORT as WORLD30, source_rows
from tools.stoneage_recovery_callback_replay import BATTLE, BATTLE_INIT, CODE, DATA, FIELD, X87_RESET_CONTROL, trial
from tools.stoneage_savepoint_item_source import original_image
from tools.stoneage_scene33_source_pair import ARCHIVE_SHA, ROOT, canonical, config_rows, one, sha

REPORT = ROOT / 'research/recovered/STONEAGE-STAGE-A-WORLD31-RECOVERY-SOURCE-R1.json'
SOURCE_SCOPE = 'SAME_PRESERVED_MIXED25_ARCHIVE_X86_CALLBACK_REPLAY_WITH_FIXTURES'
SOURCE_MEMBERS = ('gmsv/gmsv.exe', 'gmsv/setup.cf', 'gmsv/data/itemset.txt')
SYMBOLS = {
    '_ITEM_useRecovery': 0x500590, '_ITEM_useRecovery_Field': 0x4fe4d0,
    '_ITEM_useRecovery_Battle': 0x559140, '_CHAR_ItemUse': 0x4746e0,
    '_BATTLE_MultiRecovery': 0x548eb0, '__CHAR_DelItem': 0x433ab0,
    '__CHAR_setInt': 0x42dcf0, '_CHAR_CanCureFlg': 0x4335f0,
}
SAMPLES = (12530, 12500, 12555, 12780, 12754)
TOKEN = re.compile(r'([體氣])([0-9]+)')
SHAPES = {frozenset('體'): 'HP', frozenset('氣'): 'MP', frozenset('體氣'): 'HP_MP'}
DELETED = [[8, 7, 1, 0]]
RNG_HIGH = 2147483647
BOUNDARY = ('original_client_or_server_started', 'live_battle_outcome_observed',
            'inventory_actually_mutated', 'frontend_scene_or_target_enforcement_verified',
            'official_early_version_equivalence_proven')


def verified_sources(archive_path, extracted):
    raw = archive_path.read_bytes()
    if len(raw) != 361255180 or sha(raw) != ARCHIVE_SHA:
        raise ValueError('Complete parent archive differs')
    parent = json.loads(WORLD30.read_text(encoding='utf-8'))
    witnesses = {entry['target']: entry for entry in parent['archive_witness']['members']}
    result = {}
    selected = []
    for name in SOURCE_MEMBERS:
        member = (extracted / Path(name).name).read_bytes()
        entry = witnesses[name]
        offset = entry['header_offset']
        packed_start = offset + entry['header_bytes']
        packed_end = packed_start + entry['packed_bytes']
        if (len(member) != entry['unpacked_bytes'] or sha(member) != entry['member_sha256']
                or zlib.crc32(member) != entry['member_crc32']
                or sha(raw[offset:packed_start]) != entry['header_sha256']
                or sha(raw[packed_start:packed_end]) != entry['packed_sha256']):
            raise ValueError(f'Original source witness differs: {name}')
        result[name] = member
        selected.append(entry)
    cfg, _ = config_rows(result['gmsv/setup.cf'])
    if one(cfg, 'itemset6file') != 'data/itemset.txt':
        raise ValueError('Configured item table differs')
    return result, selected


def program_evidence(take, literal, found):
    literal(0x55e470, 'ITEM_useRecovery')
    target = struct.unpack('<I', take(0x55e490, 4))[0]
    if target != found['_ITEM_useRecovery']:
        raise ValueError('Original item callback registration differs')
    for address, text in ((0x5a4e98, '體'), (0x5a4e9b, '氣'), (0x5aa896, '體'), (0x5aa89c, '氣')):
        if take(address, 3) != text.encode('cp950') + b'\0':
            raise ValueError('Original recovery token differs')
    edges = []
    for address, opcode, symbol in (
        (0x41324c, 0xe9, '_CHAR_ItemUse'), (0x5296bb, 0xe8, '_CHAR_ItemUse'),
        (0x50060f, 0xe9, '_ITEM_useRecovery_Battle'), (0x500629, 0xe9, '_ITEM_useRecovery_Field'),
        (0x4feb5a, 0xe8, '_CHAR_CanCureFlg'), (0x4fec52, 0xe8, '__CHAR_setInt'),
        (0x55927c, 0xe8, '_BATTLE_MultiRecovery'), (0x5593bb, 0xe8, '__CHAR_DelItem'),
    ):
        instruction = take(address, 5)
        destination = address + 5 + struct.unpack_from('<i', instruction, 1)[0]
        if instruction[0] != opcode or destination != found[symbol]:
            raise ValueError(f'Original relative edge differs at {address:#x}')
        edges.append({'address': address, 'target': symbol, 'instruction_sha256': sha(instruction)})
    return {
        'symbols': found, 'registration_sha256': sha(take(0x55e470, 40)), 'edges': edges,
        'field_current_hp_mp_keys': list(struct.unpack('<2I', take(0x588988, 8))),
        'field_max_hp_mp_work_keys': list(struct.unpack('<2I', take(0x588974, 8))),
        'field_rand_constants': list(struct.unpack('<2df', take(0x5a5488, 20))),
        'emulator_source_windows': [[a, b, sha(take(a, b - a))] for a, b in CODE + DATA],
    }


def catalog(raw):
    rows = []
    for line, physical, fields in source_rows(raw, 94):
        if fields[10] != b'ITEM_useRecovery':
            continue
        option = fields[3].decode('cp950')
        parsed = TOKEN.findall(option)
        simple = len(parsed) in (1, 2) and len(dict(parsed)) == len(parsed)
        simple = simple and ''.join(key + value for key, value in parsed) == option
        values = {key: int(value) for key, value in parsed} if simple else {}
        shape = SHAPES.get(frozenset(values), 'OTHER')
        rows.append({'id': int(fields[16]), 'line': line, 'row_sha256': sha(physical),
                     'scene': int(fields[20]), 'target': int(fields[21]), 'shape': shape,
                     'raw_hash_prefix': fields[0].startswith(b'#'), 'values': values,
                     'option_sha256': sha(fields[3])})
    return rows


def replay_batch(take, rows):
    multiplicity = Counter(tuple(row['values'].items()) for row in rows
                           if row['values'] and not row['raw_hash_prefix'])
    observations = []
    for tokens, count in sorted(multiplicity.items()):
        option = ''.join(f'{key}{value}' for key, value in tokens)
        values = dict(tokens)
        low = trial(take, option, FIELD, max_hp=10000, max_mp=10000)
        high = trial(take, option, FIELD, max_hp=10000, max_mp=10000, rand=RNG_HIGH)
        battle = trial(take, option, BATTLE)
        first = '體' if '體' in values else '氣'
        request, = battle['battle_requests']
        expected_fields = [number for token, number in (('體', 10), ('氣', 11)) if token in values]
        for result in (low, high):
            if (result['battle_requests'] or result['rand_calls'] != len(values)
                    or [field for _, field, _ in result['changes']] != expected_fields
                    or result['deleted'] != DELETED):
                raise ValueError(f'Unexpected field trace for {option}')
        if (request[3:6] != [int(first == '氣'), values[first], 0] or battle['changes']
                or battle['rand_calls'] or battle['deleted'] != DELETED):
            raise ValueError(f'Unexpected battle trace for {option}')
        observations.append({'tokens': [list(t) for t in tokens], 'source_rows': count,
                             'field_rand_0': [value for _, _, value in low['changes']],
                             'field_rand_max': [value for _, _, value in high['changes']],
                             'battle_request_kind_value_percent': request[3:6]})
    return observations


def fixture_probes(take):
    return {
        'initializing_battle': trial(take, '體320', BATTLE_INIT),
        'field_pet_mixed': trial(take, '氣20體185', FIELD, target_kind=3),
        'field_pet_mp_only': trial(take, '氣5', FIELD, target_kind=3),
        'field_full_hp_mp': trial(take, '氣20體185', FIELD, hp=1000, mp=100),
        'field_cure_denied': trial(take, '氣20體185', FIELD, can_cure=0),
        'battle_position_invalid': trial(take, '氣20體185', BATTLE, battle_position=-1),
        'invalid_caster': trial(take, '體320', FIELD, caster_valid=False),
        'invalid_item': trial(take, '體320', BATTLE, item_valid=False),
        'field_self_mp': trial(take, '氣5', FIELD, target=8),
        'field_marker_full': trial(take, '全', FIELD),
        'field_missing_hp_number': trial(take, '體', FIELD),
        'battle_missing_hp_number': trial(take, '體', BATTLE),
    }


def derive(archive, extracted):
    members, inputs = verified_sources(archive, extracted)
    _, take, _, literal, found = original_image(members['gmsv/gmsv.exe'], SYMBOLS)
    rows = catalog(members['gmsv/data/itemset.txt'])
    by_id = {row['id']: row for row in rows}
    if len(by_id) != len(rows):
        raise ValueError('Original recovery item IDs are not unique')
    distribution = Counter((row['shape'], row['scene'], row['target']) for row in rows)
    return {
        'schema': 'stoneage.world31.recovery_source.r1', 'scope': SOURCE_SCOPE,
        'archive_sha256': ARCHIVE_SHA, 'selected_source_members': inputs,
        'configured_item_source': 'itemset6file=data/itemset.txt',
        'program': program_evidence(take, literal, found),
        'catalog': {
            'physical_callback_rows': len(rows),
            'raw_hash_prefix_ids': [row['id'] for row in rows if row['raw_hash_prefix']],
            'shape_scene_target_counts': [[*key, count] for key, count in sorted(distribution.items())],
            'all_derived_callback_rows_sha256': sha(canonical(rows)),
            'sample_rows': [by_id[item_id] for item_id in SAMPLES],
        },
        'emulated': {
            'engine': 'Unicorn x86-32',
            'common_fixture': {'hp': 100, 'mp': 10, 'batch_max_hp_mp': 10000,
                               'caster': 8, 'target': 9, 'inventory_slot': 7,
                               'rand_inputs': [0, RNG_HIGH], 'battle_mode': BATTLE,
                               'x87_control_word': X87_RESET_CONTROL},
            'ordinary_option_replays': replay_batch(take, rows),
            'boundary_fixture_replays': fixture_probes(take),
        },
        **dict.fromkeys(BOUNDARY, False),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('private_extracted_members', type=Path)
    args = parser.parse_args()
    print(json.dumps(derive(args.archive, args.private_extracted_members), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
