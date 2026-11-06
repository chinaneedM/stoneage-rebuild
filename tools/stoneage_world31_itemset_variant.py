"""Source-qualified WORLD31 itemset variant comparison from the existing private ITEM01 catalog.

This is a metadata observer, not historical client/server execution. The private
original-derived catalog remains private; only hashes, counts and identifiers
are suitable for publication. The configured itemset selection comes from the
separately qualified WORLD31 same-archive setup.cf finding.
"""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import re
import zipfile

A = 'itemset.txt'
B = 'itemset0710.txt'
REPORT_SCHEMA = 'stoneage.world31.itemset_variant.r1'
EXPECTED_ZIP_SHA = 'cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa'
EXPECTED_CATALOG_SHA = '0438c4fc9bf945223d46c24e9d374de436f2ac981c23fa282776281c2e772e60'
EXPECTED_ARCHIVE_SHA = 'd71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5'
EXPECTED_SOURCES = {
    A: ('a415e78f9aab2e5ea5ca92ecb7430253f7be1ba7c876d6b0bb6d067b1b466688', 3392473),
    B: ('6d6d63fda59c6bda2f239fe18c9361b5c9da18c84f678b7cc95bde24544292fb', 3668487),
}


def sha(data):
    return sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode('utf-8')


def class_of(option):
    pairs = re.findall(r'([體氣])([0-9]+)', option)
    if not pairs or len(pairs) != len(dict(pairs)) or ''.join(x + y for x, y in pairs) != option:
        return 'OTHER'
    s = set(key for key, _ in pairs)
    return {frozenset('體'): 'HP', frozenset('氣'): 'MP', frozenset('體氣'): 'HP_MP'}.get(frozenset(s), 'OTHER')


def qualified_catalog(path):
    path = Path(path)
    if sha(path.read_bytes()) != EXPECTED_ZIP_SHA:
        raise ValueError('Private ITEM01 source ZIP SHA mismatch')
    with zipfile.ZipFile(path) as archive:
        if archive.testzip() is not None:
            raise ValueError('Private ZIP member CRC mismatch')
        original = archive.read('private-full-catalog.json')
        if sha(original) != EXPECTED_CATALOG_SHA:
            raise ValueError('Private original-derived catalog SHA mismatch')
        catalog = json.loads(original)
    prov = catalog['origin_community_mixed25_source_tables_provenance']
    if prov['mixed25_community_RAR_sha256'] != EXPECTED_ARCHIVE_SHA:
        raise ValueError('Parent original source archive mismatch')
    for name, tag in ((A, 'itemset_a'), (B, 'itemset_b')):
        item = prov[tag]
        if (item['sha256'], item['source_size_bytes']) != EXPECTED_SOURCES[name]:
            raise ValueError('Original itemset source witness mismatch: ' + name)
    if prov['community_archive_certified_official_clean_build'] or prov['same_original_official_deployment_of_itemsets_and_retail_art_proven']:
        raise ValueError('Source boundary differs')
    return catalog


def callback_rows(catalog, table):
    found = {}
    for row in catalog['items']:
        source = row.get(table)
        if source is None:
            continue
        values = source['original_94_columns']
        if len(values) != 94 or int(values[16]) != row['id']:
            raise ValueError('Incorrect source ID or field count')
        if values[10] != 'ITEM_useRecovery':
            continue
        if row['id'] in found:
            raise ValueError('Duplicate recovery callback item ID')
        found[row['id']] = source
    return found


def generate(private_zip):
    catalog = qualified_catalog(private_zip)
    a, b = (callback_rows(catalog, name) for name in (A, B))
    shared, add, deleted = sorted(a.keys() & b.keys()), sorted(b.keys() - a.keys()), sorted(a.keys() - b.keys())
    # Compare all 94 fields, not just callback name or options.
    changed = [ident for ident in shared if a[ident]['original_94_columns'] != b[ident]['original_94_columns']]
    if len(a) != 644 or len(b) != 663 or len(shared) != 644 or len(add) != 19 or deleted or changed:
        raise ValueError('Expected source bounded table relationship changed')
    def shape_counts(rows):
        return dict(sorted(Counter(class_of(x['original_94_columns'][3]) for x in rows.values()).items()))
    if shape_counts(a) != {'HP':389, 'HP_MP':48, 'MP':147, 'OTHER':60}:
        raise ValueError('Configured WORLD31 source scope differs')
    if shape_counts(b) != {'HP':395, 'HP_MP':48, 'MP':149, 'OTHER':71}:
        raise ValueError('Alternate source scope differs')
    return {
        'schema': REPORT_SCHEMA,
        'scope': 'PRIVATE_ITEM01_ORIGINAL_DERIVED_CATALOG_CROSS_TABLE_STATIC_REPLAY',
        'source_private_zip_sha256': EXPECTED_ZIP_SHA,
        'source_private_catalog_member_sha256': EXPECTED_CATALOG_SHA,
        'parent_original_mixed25_archive_sha256': EXPECTED_ARCHIVE_SHA,
        'source_itemsets': {k: {'original_member_sha256': v[0], 'original_member_size': v[1]} for k, v in EXPECTED_SOURCES.items()},
        'configured_itemset_from_world31_setup_cf': A,
        'callback_function_column_zero_based': 10,
        'callback_option_column_zero_based': 3,
        'item_id_column_zero_based': 16,
        'source_field_count': 94,
        'tables': {
            A: {'callback_rows': len(a), 'shape_counts': shape_counts(a), 'ids_sha256': sha(canonical(sorted(a)))},
            B: {'callback_rows': len(b), 'shape_counts': shape_counts(b), 'ids_sha256': sha(canonical(sorted(b)))},
        },
        'shared_callback_ids': len(shared),
        'shared_changed_94_field_rows': len(changed),
        'configured_only_callback_ids': deleted,
        'alternate_only_callback_rows': [
            {
                'id': ident,
                'source_row_1based': b[ident]['source_row_1based'],
                'source_row_sha256_from_item01_catalog': b[ident]['original_row_sha256'],
                'raw_option_sha256_cp950': sha(b[ident]['original_94_columns'][3].encode('cp950')),
                'option_shape': class_of(b[ident]['original_94_columns'][3]),
                'scene_raw': b[ident]['original_94_columns'][20],
                'target_raw': b[ident]['original_94_columns'][21],
            }
            for ident in add
        ],
        'interpretation': '19 additional static callback rows in a nonconfigured candidate itemset, not 19 additional deployed usable items',
        'source_original_executable_replayed_in_this_package': False,
        'world32_combat_settlement_verified': False,
        'source_same_deployment_or_official_version_proven': False,
        'original_server_started': False,
        'original_items_used_in_game': False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('private_item01_zip', type=Path)
    args = parser.parse_args()
    print(json.dumps(generate(args.private_item01_zip), ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
