#!/usr/bin/env python3
"""Crosswalk source-qualified mixed25 item aliases against 2006 official patch metadata.

No original proprietary bytes are copied; every matched resource is a static alias
candidate, not an authenticated same-build item picture or runtime selection.
"""
import argparse
import csv
import gzip
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ITEM = ROOT / 'research/recovered/STONEAGE-ITEM06-MIXED25-MISSING-TW1-ITEM-ALIAS-PIXELS-R1.json'
REF = ROOT / 'research/recovered/logical-alias-catalog-r1/REFERENCES-R1.tsv.gz'
CONTENT = ROOT / 'research/recovered/logical-alias-catalog-r1/CONTENTS-R1.tsv.gz'
OUTPUT = ROOT / 'research/recovered/STONEAGE-ITEM07-PATCH129-ITEM-ALIAS-CROSSVERSION-SOURCE-R1.json'
PINS = {
    ITEM: '989361a944b874e49a19c33846c6d49c2f0ca5be',
    REF: '9a97b3c1ec5ba3e5ab9479f2cdb43e2a540445e1',
    CONTENT: 'e08cf16b96d001310b932251e39e3f3609de9b71',
}
EXPECTED_REF_ROWS = 43632


def git_blob_sha(path):
    data = path.read_bytes()
    return hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()


def read_tsv(path):
    with gzip.open(path, 'rt', encoding='utf-8', newline='') as stream:
        yield from csv.DictReader(stream, delimiter='\t')


def crosswalk(item_doc, patch_rows, content_by_id, *, expected_rows=EXPECTED_REF_ROWS):
    assert item_doc['schema'].startswith('stoneage.item06.') or 'ITEM06' in item_doc['schema'].upper(), item_doc['schema']
    aliases = item_doc['aliases']
    by_key = {int(x['alias']): x for x in aliases}
    assert len(by_key) == len(aliases) == 831
    counts = Counter(x['status'] for x in aliases)
    assert counts == Counter({'strict': 415, 'absent': 416}), counts
    assert item_doc['counts'] == {'strict': 415, 'absent': 416}
    patch = defaultdict(list)
    profile_count = Counter()
    row_count = 0
    for row in patch_rows:
        row_count += 1
        profile_count[row['profile']] += 1
        if row['profile'] == 'PATCH129' and int(row['logical_alias']) in by_key:
            cid = row['content_id']
            assert cid in content_by_id, ('unknown content_id', cid)
            content = content_by_id[cid]
            patch[int(row['logical_alias'])].append({
                'original_patch_record_index': int(row['source_index']),
                'original_patch_physical_bitmapno': int(row['physical_bitmapno']),
                'source_original_rd_sha256': content['rd_sha256'],
                'source_original_rd_size': int(content['bytes']),
                'source_width': int(row['width']),
                'source_height': int(row['height']),
                'source_rd_status': row['source_rd_status'],
                'catalog_rd_qualification': row['catalog_rd_qualification'],
                'source_record_sha256': row['record_sha256'],
            })
    assert row_count == expected_rows, ('reference count', row_count)
    assert profile_count['PATCH129'] == 20229, profile_count
    result = []
    status_counts = Counter()
    reference_count = 0
    exact_same_rd_count = 0
    for alias in sorted(by_key):
        source = by_key[alias]
        matches = sorted(patch[alias], key=lambda x:(x['original_patch_record_index'], x['original_patch_physical_bitmapno']))
        reference_count += len(matches)
        unique = {(x['source_original_rd_sha256'], x['source_original_rd_size']) for x in matches}
        matching_original_rd = source.get('rd_sha256')
        exact_same = sum(x['source_original_rd_sha256'] == matching_original_rd for x in matches) if matching_original_rd else 0
        exact_same_rd_count += bool(exact_same)
        status = ('PATCH_NOT_IN_ALIAS_CATALOG' if not matches else
                  'PATCH_SAME_RD_AS_MIXED25' if exact_same else
                  'PATCH_MULTIPLE_RD_CANDIDATES' if len(unique) > 1 else
                  'PATCH_ONE_RD_CANDIDATE')
        status_counts[(source['status'], status)] += 1
        result.append({
            'mixed25_item_image_alias': alias,
            'mixed25_current_status': source['status'],
            'mixed25_original_rd_sha256': matching_original_rd,
            'distinct_patch_rd_candidates': len(unique),
            'patch_original_alias_occurrences': len(matches),
            'result': status,
            'patch_source_occurrences': matches,
        })
    assert sum(status_counts.values()) == 831
    assert reference_count == sum(x['patch_original_alias_occurrences'] for x in result)
    summary = {
        'mixed25_absent_candidate_aliases': 416,
        'mixed25_strict_pixel_aliases': 415,
        'patch129_matched_aliases': sum(bool(x['patch_original_alias_occurrences']) for x in result),
        'patch129_total_matching_occurrences': reference_count,
        'patch129_exact_same_rd_as_mixed25_aliases': exact_same_rd_count,
        'by_status': {f'{a}|{b}': v for (a,b),v in sorted(status_counts.items())},
    }
    return {'schema':'stoneage.item07.patch129_item_alias_crossversion_source.r1',
            'source_scope':'mixed25_community_saved_item_tables_vs_20060911_official_patch_numeric_resource_metadata',
            'source_pins_git_blobs':{str(p.relative_to(ROOT)):sha for p,sha in PINS.items()},
            'source_references_rows':row_count, 'source_patch129_rows':profile_count['PATCH129'],
            'summary':summary, 'aliases':result,
            'caveats':['A patch numeric alias does not establish a game item or same-deployment client selector.',
                       'No original proprietary bitmap bytes were loaded or rendered in this crosswalk.',
                       'Source absent means absent from the two pinned scopes, not absent from historical StoneAge.',
                       'The 2006 patch is not a complete independently certified 8.5 client.']}


def build():
    for p, expected in PINS.items():
        actual = git_blob_sha(p)
        if actual != expected:
            raise ValueError(f'source changed: {p} got {actual}; expected {expected}')
    item = json.loads(ITEM.read_text(encoding='utf-8'))
    contents = {r['content_id']:r for r in read_tsv(CONTENT)}
    assert len(contents) == 19236, len(contents)
    return crosswalk(item, read_tsv(REF), contents)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=OUTPUT)
    args = parser.parse_args()
    r = build()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(r, ensure_ascii=False, indent=2, sort_keys=True)+'\n',encoding='utf-8')
    print('ITEM07_SOURCE_SUMMARY='+json.dumps(r['summary'],sort_keys=True,ensure_ascii=False))
    print('ITEM07_OUTPUT_BYTES='+str(args.output.stat().st_size))
    print('ITEM07_OUTPUT_SHA256='+hashlib.sha256(args.output.read_bytes()).hexdigest())


if __name__ == '__main__':
    main()
