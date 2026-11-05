#!/usr/bin/env python3
"""Bounded Raceman source/compiled mismatch; never runs the original server."""
import argparse
import hashlib
import json
from pathlib import Path
import struct

from tools.stoneage_quest_currency_source import MANIFEST, RECO, read_json, sha, verified_members
from tools.stoneage_savepoint_item_source import original_image

W23 = 'STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-23-NPC-ITEM-TRANSFERS-R1.json'
O88 = 'STONEAGE-O88-FAMILY-PET-HUNT-DATED-EVENT-R1.json'
SYMBOLS = {'_NPC_searchFunctionSet': 0x48aa20,
           '_NPC_copyFunctionSetToChar': 0x48aa70, '_functionSet': 0x579a40}


def ascii_function_names(take, table, count, stride):
    """Read exactly the statically evidenced lookup domain, not a string search."""
    rows = []
    for i in range(count):
        record = take(table + i * stride, stride)
        va, = struct.unpack_from('<I', record)
        raw = bytearray()
        for j in range(128):
            c = take(va + j, 1)[0]
            if c == 0:
                break
            if not 32 <= c < 127:
                raise ValueError('non-ASCII function name')
            raw.append(c)
        else:
            raise ValueError('unterminated function name')
        if not raw:
            raise ValueError('empty function name')
        rows.append([i, va, raw.decode('ascii'), sha(record), sha(bytes(raw) + b'\0')])
    return rows


def compiled_lookup(data):
    base, take, imm, _, symbols = original_image(data, SYMBOLS)
    table_immediate = imm(0x48aa2b, 0xbb, 0x579a40)
    # Stride 0x44; inclusive indices 0..0x3b; unsigned exit; failed return -1.
    checks = [(0x48aa35, bytes.fromhex('46 83 c3 44 83 fe 3b 77 1c')),
              (0x48aa4c, bytes.fromhex('85 c0 75 e5')),
              (0x48aa5d, bytes.fromhex('b8 ff ff ff ff')),
              (0x48aa80, bytes.fromhex('83 fa 3b 76 0b'))]
    for va, expected in checks:
        if take(va, len(expected)) != expected:
            raise ValueError('compiled function lookup bound or branch differs')
    call = take(0x48aa47, 5)
    target = 0x48aa4c + struct.unpack_from('<i', call, 1)[0]
    if call[0] != 0xe8 or target != 0x55b040:
        raise ValueError('case-insensitive comparison call differs')
    rows = ascii_function_names(take, 0x579a40, 60, 68)
    return {'bytes': len(data), 'sha256': sha(data), 'base': base,
            'COFF_symbols': symbols, 'table_immediate': table_immediate,
            'lookup_count': 60, 'record_stride': 68, 'last_inclusive_index': 59,
            'comparison_call': {'va': 0x48aa47, 'target_va': target,
                                'instruction_sha256': sha(call), 'nm_target': '_strcasecmp'},
            'lookup_code_window': {'first_VA': 0x48aa20, 'end_VA_exclusive': 0x48aa67,
                                   'sha256': sha(take(0x48aa20, 0x47))},
            'lookup_names': rows,
            'Raceman_case_insensitive_table_matches': [r[0] for r in rows if r[2].lower() == 'raceman'],
            'Raceman_case_insensitive_whole_image_substring_count': data.lower().count(b'raceman'),
            'static_failed_lookup_return': -1,
            'original_program_executed': False}


def git_blob(path):
    b = path.read_bytes()
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()


def derive(exe, npc_zip):
    compiled = compiled_lookup(exe.read_bytes())
    _, members = verified_members(npc_zip, read_json(MANIFEST))
    old, prior = read_json(W23), read_json(O88)
    source, = [f for f in old['files'] if any('Raceman' in ref[8] for ref in f[4])]
    fields = []
    for n, line in enumerate(members[source[0]].splitlines(), 1):
        if line.startswith((b'GetItem:', b'CheckItem:')):
            key, value = line.decode('ascii').split(':', 1)
            fields.append({'line': n, 'key': key, 'raw_literal': value, 'line_sha256': sha(line)})
    op, = source[6]
    if not any((f['line'], f['key'], f['raw_literal'], f['line_sha256']) == tuple(op[:4]) for f in fields):
        raise ValueError('WORLD23 physical field differs')
    selected = []
    for row in prior['source']['members']:
        prefix = 'gmsv/data/npc/'
        if not row['path'].startswith(prefix):
            continue
        path = row['path'][len(prefix):]
        data = members[path]
        if sha(data) != row['sha256'] or len(data) != row['bytes']:
            raise ValueError('original O88 source identity differs')
        selected.append({'path': path, 'bytes': len(data), 'sha256': sha(data),
                         'crc32': row['extracted_crc32']})
    shards = sorted((RECO / 'item-module-01').glob('*.json'))
    index = {r[0]: r for p in shards for r in json.loads(p.read_text())['rows']}
    item = index[20760]
    if item[1] is not None or item[2] is None:
        raise ValueError('itemset A/B source presence differs')
    return {'schema': 'stoneage.world26.raceman_source_boundary.r1',
            'source_scope': 'PRESERVED_COMMUNITY_MIXED25_NOT_AUTHENTICATED_OFFICIAL_OR_MATCHING_DEPLOYMENT',
            'compiled_server': compiled,
            'input_git_blobs': {p.name: git_blob(p) for p in [RECO / MANIFEST, RECO / W23, RECO / O88, *shards]},
            'all_2205_NPC_members_SHA_size_CRC_reverified': True,
            'parent_RAR_reread': False,
            'original_three_source_files': selected,
            'exact_original_CREATE_refs': source[4], 'source_parameter_path': source[0],
            'source_item_fields': fields, 'item01_source_join': item,
            'conclusion': 'RACEMAN_HANDLER_NOT_IN_THIS_COMPILED_NAME_LOOKUP_GETITEM_ROLE_OPEN',
            'different_registered_functions_not_substitutes': ['PetRaceMaster', 'PetRacePet'],
            'event_classification': 'DATED_EVENT_CONFIG_ALREADY_RECORDED_BY_O88_AND_QUEST04_NOT_NEW_EVENT_DISCOVERY',
            'WORLD23_raw_numeric_index_preserved': True,
            'limits': {'GetItem_grant_or_consumption_proven': False, 'event_live_deployment_proven': False,
                       'all_versions_missing_20760': False, 'matching_handler_source_acquired': False,
                       'official_TW1_JSS1999_CN182_rule_proven': False, 'overall_percent': None},
            'reopen_only_with': 'Provenance-qualified matching Raceman handler/build or native trace for these exact parameters',
            'next': 'WORLD27: source-batch pet-handover quest branches, conditions and rewards; leave compiled item-field helper chain'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--exe', type=Path, required=True)
    p.add_argument('--npc-zip', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    report = derive(a.exe, a.npc_zip)
    a.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(report['conclusion'])


if __name__ == '__main__':
    main()
