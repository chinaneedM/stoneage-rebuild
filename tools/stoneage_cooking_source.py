"""Rebuild the WORLD30 report from private mixed25 files without running GMSV."""

import argparse
import json
from pathlib import Path
import struct

from tools.stoneage_savepoint_item_source import original_image
from tools.stoneage_scene33_source_pair import PINS, ROOT, config_rows, one, rar_receipt, sha

RECOVERED = ROOT / 'research/recovered'
REPORT = RECOVERED / 'STONEAGE-STAGE-A-WORLD30-COOKING-SOURCE-R1.json'
O75 = RECOVERED / 'STONEAGE-O75-ORIGINAL-COOKING-CRAFTING-NPC-SOURCE-R1.json'
SOURCE_SCOPE = 'SAME_PRESERVED_MIXED25_ARCHIVE_STATIC_ONLY'
SYMBOLS = {
    '_ITEM_readItemConfFile': 0x4f9110, '_PETSKILL_initPetskill': 0x550ab0,
    '_ITEM_initItemAtom': 0x50e450, '_ITEM_initItemIngCache': 0x50db10,
    '_ITEM_initRandTable': 0x50da20, '_PETSKILL_functbl': 0x58f900,
    '_PETSKILL_Merge': 0x553b50, '_ITEM_mergeItem_merge': 0x511c50,
    '_ITEM_getmergeItemFromFromITEMtabl': 0x4fbf00, '_ITEM_mergeItem': 0x50f5c0,
    '_ITEM_merge_getPetFix': 0x50e860, '_getStringFromIndexWithDelim_body': 0x407090,
    '_CHAR_findEmptyItemBox': 0x473bc0, '__CHAR_setItemIndex': 0x4323e0,
    '__ITEM_endExistItemsOne': 0x4f72a0, '_ITEM_makeItemAndRegist': 0x4fa7d0,
    '_CHAR_addItemSpecificItemIndex': 0x475d50, '_random': 0x55b020,
}
CALLS = {
    0x401fa4: '_ITEM_readItemConfFile', 0x402593: '_PETSKILL_initPetskill',
    0x4025fc: '_ITEM_initItemAtom', 0x40265d: '_ITEM_initItemIngCache',
    0x4026be: '_ITEM_initRandTable', 0x50e650: '_getStringFromIndexWithDelim_body',
    0x50e6df: '_getStringFromIndexWithDelim_body',
    0x553c15: '_ITEM_mergeItem_merge', 0x511c8e: '_CHAR_findEmptyItemBox',
    0x511cf5: '_getStringFromIndexWithDelim_body',
    0x511dbb: '_ITEM_getmergeItemFromFromITEMtabl', 0x511e8f: '_ITEM_mergeItem',
    0x50fbaf: '_ITEM_merge_getPetFix', 0x5107dd: '_random',
    0x511f2e: '__CHAR_setItemIndex', 0x5120bc: '__ITEM_endExistItemsOne',
    0x51210f: '_ITEM_makeItemAndRegist', 0x51218c: '_CHAR_addItemSpecificItemIndex',
}
CONFIG_KEYS = {
    'itemset6file': (0x55c5a0, 0x404fd0, 0x61cb6c),
    'petskillfile2': (0x55c7b0, 0x405090, 0x61cccc),
    'itematomfile': (0x55c7e0, 0x4050b0, 0x61ccec),
}
WITNESSES = {
    'first_argument_scan_index_5': (0x511ca0, 5),
    'last_argument_scan_index_19': (0x511cb1, 3),
    'require_more_than_one_accepted_item': (0x511e31, 13),
    'first_accepted_type_20_sets_mode_1': (0x511e40, 19),
    'atom_name_index_equality': (0x510694, 6),
    'candidate_cache_and_output_flag_gates': (0x5105f8, 23),
    'candidate_hit_and_size_equality': (0x51099d, 14),
    'adjusted_atom_value_upper_and_lower_checks': (0x510919, 32),
    'candidate_random_remainder': (0x5107e3, 6),
    'bounded_outer_retry_branch': (0x510804, 13),
    'mixed_type_rejection_bypasses_consumption': (0x511e9a, 9),
}
FALSE = ('original_program_executed', 'native_result_observed', 'fixed_recipe_or_success_rate_proven',
         'historical_deployment_authenticated', 'official_early_version_equivalence_proven')


def compiled(data):
    _, take, _, literal, found = original_image(data, SYMBOLS)
    calls = []
    for address, symbol in CALLS.items():
        raw = take(address, 5)
        target = address + 5 + struct.unpack_from('<i', raw, 1)[0]
        if raw[0] != 0xe8 or target != found[symbol]:
            raise ValueError(f'Unexpected compiled call at {address:#x}')
        calls.append({'address': address, 'symbol': symbol, 'instruction_sha256': sha(raw)})
    slot = 0x58f9e0
    name, target = struct.unpack('<II', take(slot, 8))
    if target != found['_PETSKILL_Merge']:
        raise ValueError('Incorrect pet skill registration')
    literal(name, 'PETSKILL_Merge')
    literal(0x5a68a7, '|')
    config_bindings = {}
    for key, (entry, getter, destination) in CONFIG_KEYS.items():
        literal(entry, key)
        expected = struct.pack('<I', destination)
        if take(entry + 32, 4) != expected or take(getter + 1, 5) != b'\xb8' + expected:
            raise ValueError(f'Compiled config destination differs: {key}')
        config_bindings[key] = {'entry': entry, 'getter': getter, 'destination': destination,
                                'entry_sha256': sha(take(entry, 48))}
    raw_search_table = take(0x58bda0, 32)
    return {
        'symbols': found, 'calls': calls, 'config_bindings': config_bindings,
        'registration': {'slot': slot, 'name_address': name, 'callback': target,
                         'slot_sha256': sha(take(slot, 8))},
        'search_table_min_max': [list(pair) for pair in struct.iter_unpack('<dd', raw_search_table)],
        'search_table_sha256': sha(raw_search_table),
        'instruction_windows': {key: {'address': va, 'bytes': size, 'sha256': sha(take(va, size))}
                                for key, (va, size) in WITNESSES.items()},
    }


def source_rows(raw, width):
    if raw.decode('cp950').encode('cp950') != raw:
        raise ValueError('Source CP950 round trip failed')
    for line_no, line in enumerate(raw.splitlines(keepends=True), 1):
        fields = line.rstrip(b'\r\n').split(b',')
        if len(fields) != width:
            raise ValueError(f'Unexpected source width on line {line_no}')
        yield line_no, line, fields


def composition(rows, atoms, chef_rows):
    by_id = {int(fields[16]): (number, line, fields) for number, line, fields in rows}
    if len(by_id) != len(rows):
        raise ValueError('Duplicate physical item ID')
    ingredients = {}
    for item_id, (number, line, fields) in by_id.items():
        tags = [field for field in fields[84:94:2] if field]
        if not fields[0].startswith(b'#') and fields[19] == b'20' and fields[82] == b'1' and len(tags) == 1:
            slot = fields[84:94:2].index(tags[0])
            ingredients.setdefault(tags[0], []).append(
                {'id': item_id, 'line': number, 'row_sha256': sha(line), 'value': int(fields[85 + slot * 2])})
    dishes = []
    for old in chef_rows:
        if not old['exact_unique_itemset_name']:
            continue
        item_id = old['item_id']
        number, line, fields = by_id[item_id]
        old_row_sha = sha(line.rstrip(b'\r\n'))
        if (number != old['itemset_zero_based_line'] + 1 or old_row_sha != old['full_source_row_sha256']
                or fields[0].decode('cp950') != old['menu_name']):
            raise ValueError('Chef item row differs from O75')
        slots = []
        for tag, value in zip(fields[84:94:2], fields[85:94:2]):
            if tag:
                slots.append({'atom_dictionary_line': atoms[tag], 'target_value': int(value),
                              'single_atom_input_rows': ingredients[tag]})
        dishes.append({'id': item_id, 'line': number, 'row_sha256': sha(line), 'type': int(fields[19]),
                       'o75_row_sha256_without_line_ending': old_row_sha, 'input_flag': int(fields[82]),
                       'output_flag': int(fields[83]), 'atom_slots': slots})
    return dishes


def derive(archive, extracted):
    prior = json.loads(O75.read_text(encoding='utf-8'))
    pins = {key: PINS[key] for key in ('gmsv/gmsv.exe', 'gmsv/setup.cf')}
    for key in ('itemset.txt', 'itematom.txt', 'npc/jaruga/cook.conf',
                'npc/jaruga/menu01.conf', 'npc/jaruga/menu02.conf'):
        old = prior['actual_extracted_source_files'][key]
        pins['gmsv/data/' + key] = old['bytes'], old['sha256']
    pins['gmsv/data/petskill.txt'] = (
        15112, 'f9cefefda40e3a5de9b8cdcb9f8d5c75cd768257bb9b12f7591e86d61fe2f6d4')
    members = {key: (extracted / Path(key).name).read_bytes() for key in pins}
    for key, data in members.items():
        if (len(data), sha(data)) != pins[key]:
            raise ValueError(f'Original member identity differs: {key}')
    archive_witness = rar_receipt(archive.read_bytes(), members)
    config, _ = config_rows(members['gmsv/setup.cf'])
    paths = {key: one(config, key) for key in CONFIG_KEYS}

    skills = []
    for number, line in enumerate(members['gmsv/data/petskill.txt'].splitlines(keepends=True), 1):
        fields = line.rstrip(b'\r\n').split(b',')
        if len(fields) == 12 and fields[2] == b'PETSKILL_Merge' and not line.startswith(b'#'):
            skills.append({'id': int(fields[6]), 'line': number, 'row_sha256': sha(line),
                           'callback': fields[2].decode('ascii'), 'kind': fields[11].decode('ascii')})

    if [entry['id'] for entry in skills] != [200, 201]:
        raise ValueError('Original crafting and cooking rows differ')

    atom_rows = list(source_rows(members['gmsv/data/itematom.txt'], 3))
    atoms = {fields[0]: number for number, _, fields in atom_rows}
    if len(atoms) != len(atom_rows):
        raise ValueError('Duplicate atom name')
    item_rows = list(source_rows(members['gmsv/data/itemset.txt'], 94))
    return {
        'schema': 'stoneage.world30.cooking_source.r1', 'source_scope': SOURCE_SCOPE,
        'archive_sha256': prior['source_archive']['sha256'], 'archive_witness': archive_witness,
        'configured_paths': paths, 'pet_skill_rows': skills, 'item_physical_rows': len(item_rows),
        'atom_dictionary_rows': len(atom_rows),
        'compiled': compiled(members['gmsv/gmsv.exe']),
        'chef_dishes': composition(item_rows, atoms, prior['chef_menu_to_itemset']),
        **dict.fromkeys(FALSE, False),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('private_extracted_members', type=Path)
    args = parser.parse_args()
    print(json.dumps(derive(args.archive, args.private_extracted_members), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
