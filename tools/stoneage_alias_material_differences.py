"""Replay five fixed alias cases against complete preserved physical tables.

This is a bounded material report, not a new generic resource catalog. Original
RD bytes, pixel semantics and the effective runtime overwrite are not inferred.
"""
import argparse
from collections import Counter
import json
from pathlib import Path

from tools import stoneage_logical_alias_catalog as catalog

ROOT = catalog.ROOT
OUTPUT = Path('research/recovered/STONEAGE-ALIAS-MATERIAL-DIFFERENCES-R1.json')
ALIASES = (26089, 26204, 26040, 26100, 29000)
CATALOG = catalog.DEST
PINS = {
    str(CATALOG/'REFERENCES-R1.tsv.gz'): '3092102e3ee83524ccbf27414ce0cf5bc5579d9a5c8638bfa073f9e62a4db1ea',
    str(CATALOG/'CONTENTS-R1.tsv.gz'): '2e4ac01f97d2e481ca1517c50a5ae6df96097dab72f4453273a761e938c35b89',
    str(CATALOG/'REPORT-R1.json'): 'e5dc7249b20a60b13fc4bf12b299d4a6f386fcb928d5d8843017ded58f9c1951',
    **{p: catalog.PINS[p] for p in [catalog.PATCH, catalog.NATIVE,
        catalog.EARLY['TW10']+'ADRN-R1.tsv.gz', catalog.EARLY['CN50']+'ADRN-R1.tsv.gz']},
}
PHYSICAL = {
    'TW10': (catalog.EARLY['TW10']+'ADRN-R1.tsv.gz', 125996),
    'CN50': (catalog.EARLY['CN50']+'ADRN-R1.tsv.gz', 303197),
    'TW85_NATIVE': (catalog.NATIVE, 416220),
}
HEADER = {'physical_bitmapno': 'bitmapno', 'adrn_offset': 'adder',
          'adrn_size': 'size', **{k: k for k in ['xoff', 'yoff', 'width', 'height']}}


def pin(root, path, expected):
    raw = (root/path).read_bytes()
    catalog.need(catalog.sha(raw) == expected, 'source SHA differs: '+path)
    import hashlib
    return {'bytes': len(raw), 'sha256': expected,
            'git_blob': hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}


def physical(row):
    """Normalize stored metadata; never default an unavailable logical alias to 0."""
    out = {'source_index': int(row['index']),
           **{k: int(row[v]) for k, v in HEADER.items()},
           'attr_sha256': row['attr_sha256'],
           'record_sha256': row.get('record_sha256', ''),
           'rd_sha256': row.get('rd_sha256', row.get('rd_block_sha256')),
           'rd_size_field': int(row['rd_size'] if 'rd_size' in row else row['rd_size_field']),
           **{k: int(row[k]) for k in ['rd_flag', 'rd_width', 'rd_height']},
           'source_rd_status': row.get('rd_status', 'PRIOR_ORIGINAL_BLOCK_METADATA')}
    catalog.need(isinstance(out['rd_sha256'], str) and len(out['rd_sha256']) == 64,
                 'missing original content hash')
    return out


def block(row):
    return row['adrn_size'], row['rd_sha256']


def scan(rows, wanted_blocks, wanted_ids, expected_rows):
    """Inspect zero-alias physical resources too; preserve all matching occurrences."""
    hits, same_id = [], []
    count = 0
    for index, row in enumerate(rows):
        catalog.need(int(row['index']) == index, 'physical source occurrence order/gap differs')
        count += 1
        value = physical(row)
        if block(value) in wanted_blocks:
            hits.append(value)
        if value['physical_bitmapno'] in wanted_ids:
            same_id.append(value)
    catalog.need(count == expected_rows, 'complete physical table count differs')
    return {'rows_scanned': count, 'exact_block_matches': hits,
            'same_physical_id_rows': same_id}


def check_reference(ref, source):
    for k in ['source_index', *HEADER, 'attr_sha256', 'rd_sha256',
              'rd_flag', 'rd_width', 'rd_height', 'rd_size_field']:
        catalog.need(ref[k] == source[k], 'catalog/source projection mismatch: '+k)
    if ref['record_sha256']:
        catalog.need(ref['record_sha256'] == source['record_sha256'], 'record hash differs')


def relation(left, right):
    if left == right:
        return 'SAME_BLOCK_CANDIDATE_SET'
    if left < right:
        return 'LEFT_STRICT_SUBSET_OF_RIGHT'
    if right < left:
        return 'RIGHT_STRICT_SUBSET_OF_LEFT'
    return 'OVERLAPPING_BLOCK_CANDIDATE_SETS' if left & right else 'DISJOINT_BLOCK_CANDIDATE_SETS'


def summarize(alias, references, searches):
    refs = [r for r in references if r['logical_alias'] == alias]
    catalog.need(bool(refs), 'fixed review alias missing')
    keys = {block(r) for r in refs}
    ids = {r['physical_bitmapno'] for r in refs}
    sets = {p: {block(r) for r in refs if r['profile'] == p}
            for p in ['TW10', 'CN50', 'PATCH129']}
    profiles = {}
    for profile, search in searches.items():
        profiles[profile] = {
            'rows_scanned': search['rows_scanned'],
            'exact_block_matches': [r for r in search['exact_block_matches'] if block(r) in keys],
            'same_physical_id_rows': [r for r in search['same_physical_id_rows'] if r['physical_bitmapno'] in ids],
        }
    if alias in ALIASES[:2]:
        absent = not any(profiles[p]['exact_block_matches'] for p in ['TW10', 'TW85_NATIVE'])
        conclusion = ('CN50_ONLY_BLOCK_IN_PINNED_PHYSICAL_SAMPLES' if absent
                      else 'EXACT_BLOCK_COUNTERPART_REQUIRES_ALIAS_ATTRIBUTION')
    else:
        conclusion = 'MULTIPLE_BLOCKS_UNDER_SAME_ALIAS_NO_RUNTIME_WINNER'
    return {'logical_alias': alias, 'references': refs, 'distinct_byte_blocks': len(keys),
            'occurrences_by_profile': dict(sorted(Counter(r['profile'] for r in refs).items())),
            'distinct_attributes': len({r['attr_sha256'] for r in refs}),
            'block_candidate_set_relations': [
                {'left': a, 'right': b, 'relation': relation(sets[a], sets[b])}
                for a, b in [('TW10', 'CN50'), ('TW10', 'PATCH129'), ('CN50', 'PATCH129')]],
            'complete_physical_search': profiles, 'classification': conclusion,
            'effective_runtime_reference': None, 'exact_renumbering_established': False,
            'official_content_deletion_established': False, 'game_role': 'UNKNOWN_RESOURCE_ALIAS'}


def build(root=ROOT):
    pins = {p: pin(root, p, digest) for p, digest in PINS.items()}
    parent, refs, contents = catalog.load_catalog(root/CATALOG)
    objects = {c['content_id']: c for c in contents}
    selected = []
    for r in refs:
        if r['logical_alias'] in ALIASES:
            c = objects[r['content_id']]
            selected.append({**r, **{k: c[k] for k in [
                'rd_sha256', 'rd_flag', 'rd_width', 'rd_height', 'rd_size_field']}})
    keys = {block(r) for r in selected}
    ids = {r['physical_bitmapno'] for r in selected}
    searches = {p: scan(catalog.tsv(root, path), keys, ids, count)
                for p, (path, count) in PHYSICAL.items()}
    # The patch has no original RD column. Join to an actual native record by
    # its full record hash and verify every header/attribute, not a shared ID.
    patch_rows = []
    patch_count = 0
    native_candidates = {r['source_index']: r for kind in ['same_physical_id_rows', 'exact_block_matches']
                         for r in searches['TW85_NATIVE'][kind]}
    native_by_record = {r['record_sha256']: r for r in native_candidates.values()}
    catalog.need(len(native_by_record) == len(native_candidates),
                 'ambiguous native full-record occurrences; do not choose last')
    for index, h in enumerate(catalog.tsv(root, catalog.PATCH)):
        catalog.need(int(h['index']) == index, 'patch occurrence order/gap differs')
        patch_count += 1
        if (int(h['bitmapno']) in ids or int(h['map_number']) in ALIASES
                or h['record_sha256'] in native_by_record):
            catalog.need(h['record_sha256'] in native_by_record, 'patch/native full record unavailable')
            n = native_by_record[h['record_sha256']]
            for k, v in HEADER.items():
                catalog.need(int(h[v]) == n[k], 'patch/native header differs: '+k)
            catalog.need(h['attr_sha256'] == n['attr_sha256'], 'patch/native attribute differs')
            patch_rows.append({**n, 'native_source_index': n['source_index'],
                               'source_index': index, 'logical_alias': int(h['map_number'])})
    catalog.need(patch_count == 389698, 'complete patch table count differs')
    searches['PATCH129'] = {'rows_scanned': patch_count,
        'exact_block_matches': [r for r in patch_rows if block(r) in keys],
        'same_physical_id_rows': [r for r in patch_rows if r['physical_bitmapno'] in ids]}
    for ref in selected:
        source = [r for r in searches[ref['profile']]['exact_block_matches']
                  if r['source_index'] == ref['source_index']]
        catalog.need(len(source) == 1, 'catalog reference missing or ambiguous in full physical source')
        check_reference(ref, source[0])
        if ref['profile'] == 'PATCH129':
            catalog.need(source[0]['logical_alias'] == ref['logical_alias'], 'original patch alias differs')
    cases = [summarize(a, selected, searches) for a in ALIASES]
    return {'schema': 'stoneage.alias_material_differences.r1',
        'task': 'RESOURCE-LOGICAL-ALIAS-MATERIAL-DIFFERENCES-14',
        'date': '2026-10-25', 'source_pins': pins,
        'prior_catalog_source_chain': parent['source_pins'],
        'selection': {'required_cn50_only_aliases': list(ALIASES[:2]),
            'additional_case_aliases': list(ALIASES[2:]),
            'reason': 'Same-sized CN-only alternative; retained width-changing candidate; three-block layered candidate set. Fixed cases, not a claim about all 171 groups.'},
        'full_physical_rows_scanned': {p: s['rows_scanned'] for p, s in searches.items()},
        'reviewed_reference_occurrences': len(selected), 'reviewed_distinct_blocks': len(keys),
        'cases': cases,
        'boundaries': {'originals_downloaded': False, 'original_pixels_decoded_or_rendered': False,
            'effective_runtime_overwrite_proven': False, 'same_deployed_build_proven': False,
            'rd_byte_difference_is_pixel_difference': False, 'new_named_entities': 0,
            'original_server_master_recovered': False, 'originals_deleted_bytes': 0,
            'stage_a': '7_PARTIAL_2_OPEN', 'stage_b_and_wiki': 'GATED',
            'savedata_r79': 'PAUSED_NON_BLOCKING', 'large_private_custody': 'PAUSED',
            'quest_origin_taxonomy': 'DD-028_FOUR_CLASSES_PRESERVED',
            'overall_restoration_percentage': None},
        'reopen': 'Exact same-build original alias/load-order evidence or retained raw RD/palette for a named behavior. Missing byte hash is bounded to complete indexed blocks in these pinned samples, not every substring, every version, visual equivalence or official deletion.',
        'next': 'CROSSVERSION-AUDIO-ORIGINAL-CONTENT-15'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    report = build()
    if args.verify:
        catalog.need(report == json.loads((ROOT/OUTPUT).read_bytes()), 'material report semantic replay differs')
        print('five fixed alias cases, complete physical searches and all source projections verified')
    else:
        (ROOT/OUTPUT).write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True)+'\n')
        print(json.dumps({'cases': len(report['cases']), 'references': report['reviewed_reference_occurrences'],
                          'blocks': report['reviewed_distinct_blocks']}))


if __name__ == '__main__':
    main()
