"""Frozen repository-material audit; no original source acquisition or public export."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
from .stoneage_jp2003_character_visual import build_catalog

ROOT = Path(__file__).resolve().parents[1]
PREFIX = 'research/recovered/'
MANIFEST = PREFIX + 'STONEAGE-MATERIAL-REVIEW-INPUTS-R102.json'
REVIEW = PREFIX + 'STONEAGE-MATERIAL-PORTFOLIO-REVIEW-R102.json'
REPORT = PREFIX + 'STONEAGE-MATERIAL-RECORD-AUDIT-R102.json'
MANIFEST_SHA = '8f236ee26c119121469d45c8bb5b2e793d14d74da380c1357bd7c04f6d8998fa'
REVIEW_SHA = 'e555451cf5f214547a44413ac66645cfd1130913d70e3df7c11755eb481017fe'
FIELDS = frozenset(('record_id', 'entity_type', 'version_profile', 'source_refs',
                    'verification_status', 'rights_status', 'record_revision'))
JP_SOURCE = PREFIX + 'STONEAGE-JP2003-CHARACTER-VISUAL-SOURCE-R1.json'
JP_CATALOG = PREFIX + 'STONEAGE-JP2003-CHARACTER-VISUAL-CATALOG-R1.json'
CN_FIRST = PREFIX + 'STONEAGE-WAEI-CN20-NEW-PET-CATALOG-FIRST-PAGE-R1.json'
CN_FINITE = PREFIX + 'STONEAGE-WAEI-CN20-NEW-PET-FINITE-CATALOG-R1.json'
JP_PETS = PREFIX + 'STONEAGE-JP-OFFICIAL-PET-CATALOG-R1.json'
BASE = PREFIX + 'STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json'

def require(ok, message):
    if not ok:
        raise ValueError(message)

def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':'))

def identity(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
            'git_blob': hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}

def walk(obj, pointer=''):
    """All nested dictionaries, including a full record containing another record."""
    if isinstance(obj, dict):
        yield pointer, obj
        for key, value in obj.items():
            escaped = key.replace('~', '~0').replace('/', '~1')
            yield from walk(value, pointer+'/'+escaped)
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            yield from walk(value, pointer+'/'+str(i))

def collect(objects):
    groups = defaultdict(list)
    near = []
    matched = set()
    for path, obj in sorted(objects.items()):
        for pointer, row in walk(obj):
            keys = row.keys()
            if FIELDS <= keys:
                require(isinstance(row['record_id'], str), 'Non-string record identity')
                groups[row['record_id']].append((path, pointer, row))
                matched.add(path)
            elif {'record_id', 'entity_type'} <= keys:
                near.append({'path': path, 'pointer': pointer,
                             'missing': sorted(FIELDS-keys)})
    return groups, matched, near

def check_projections(objects, payload):
    expected = build_catalog(objects[JP_SOURCE], payload)
    require(expected == objects[JP_CATALOG], 'JP catalog is not exact documented enrichment')
    old, new, jp = (objects[p]['records'] for p in (CN_FIRST, CN_FINITE, JP_PETS))
    require(len(old) == 40 and len(new) == 104 and old == new[:40],
            'CN first-page inclusion changed')
    ids = [row['record_id'] for row in new+jp]
    require(len(jp) == 124 and len(ids) == len(set(ids)) == 228,
            'Versioned web-position union changed')
    return {r['record_id'] for r in expected['records']}

def summarize(objects, payload, manifest):
    allowed = check_projections(objects, payload)
    groups, matched, near = collect(objects)
    variants, unrouted = [], []
    bodies = 0
    counts = Counter()
    occurrences = sum(map(len, groups.values()))
    for rid, entries in sorted(groups.items()):
        distinct = {canonical(e[2]) for e in entries}
        bodies += len(distinct)
        # Collection is optional in the original seven-field schema. Never infer it.
        collections = {e[2].get('collection') for e in entries}
        require(len(collections) == 1, 'Conflicting collection for one research ID')
        collection = collections.pop()
        counts[collection or 'UNROUTED'] += 1
        if collection is None:
            unrouted.append({'record_id': rid, 'occurrences': [
                {'path': p, 'pointer': q} for p, q, _ in entries]})
        if len(distinct) > 1:
            require(rid in allowed and len(entries) == 2 and
                    {e[0] for e in entries} == {JP_SOURCE, JP_CATALOG},
                    'Unexplained distinct-body duplicate: '+rid)
            variants.append({'record_id': rid, 'classification':
                             'DOCUMENTED_PROVENANCE_ENRICHMENT_NOT_HISTORICAL_CONFLICT',
                             'occurrences': [{'path': p, 'pointer': q} for p, q, _ in entries]})
    require({v['record_id'] for v in variants} == allowed, 'Missing documented JP projections')
    return {'schema': 'stoneage.material_record_audit.r102',
            'baseline_commit': manifest['baseline_commit'],
            'scope': manifest['scope'], 'input_manifest': MANIFEST,
            'input_manifest_sha256': MANIFEST_SHA,
            'counts': {'json_files_scanned': len(objects), 'files_with_full_records': len(matched),
                       'full_record_occurrences': occurrences, 'unique_research_record_ids': len(groups),
                       'distinct_record_bodies': bodies, 'identical_body_repeat_occurrences': occurrences-bodies,
                       'ids_with_distinct_bodies': len(variants), 'unrouted_unique_ids': len(unrouted),
                       'near_records_missing_required_fields': len(near)},
            'unique_ids_by_collection': dict(sorted(counts.items())),
            'distinct_body_ids': variants, 'unrouted_records': unrouted, 'near_records': near,
            'pet_catalog_overlap': {'first_page_occurrences': 40, 'finite_cn_positions': 104,
                                    'jp_positions': 124, 'file_occurrences': 268,
                                    'unique_versioned_web_position_ids': 228,
                                    'same_build_or_cross_region_species_count': None},
            'interpretation': {'counts_are_species_or_restoration_progress': False,
                               'full_record_schema_does_not_cover_all_legacy_evidence': True,
                               'no_record_automatically_selected_or_rewritten': True,
                               'original_server_or_full_client_execution_proven': False,
                               'new_historical_source_acquired': False,
                               'public_export_approved': False}}

def validate_review(review, objects):
    base = objects[BASE]['domains']
    require(len(review['domains']) == len(base) == 22, '22-domain review required')
    for old, new in zip(base, review['domains']):
        require((new['id'], new['order'], new['label'], new['baseline_status']) ==
                (old['id'], old['order'], old['label'], old['status']), 'Baseline status changed')
        require(new['anchor'] in objects and new['complete'] is False and
                bool(new['available']) and bool(new['remaining_gap']), 'Missing scoped evidence/gap')
    require(review['boundaries'] == {'baseline_domain_statuses_preserved': True,
        'original_full_payload_recovered': False, 'new_historical_source_acquired': False,
        'new_game_or_wiki_production_started': False, 'public_export_approved': False,
        'stage_a': '7_PARTIAL_2_OPEN', 'stage_b_and_wiki': 'GATED',
        'savedata_r79': 'PAUSED_NON_BLOCKING', 'overall_completion_percentage': None,
        'counts_are_restoration_progress': False}, 'Evidence boundary changed')

def audit(root=ROOT):
    raw = (root/MANIFEST).read_bytes()
    require(hashlib.sha256(raw).hexdigest() == MANIFEST_SHA, 'Frozen manifest changed')
    manifest = json.loads(raw)
    paths = [p['path'] for p in manifest['files']]
    require(paths == sorted(set(paths)) and len(paths) == 880, 'Frozen scope changed')
    objects, payload = {}, None
    for pin in manifest['files']:
        path = pin['path']
        require(Path(path).parent.as_posix() == PREFIX.rstrip('/') and path.endswith('.json'),
                'Input outside frozen top-level scope')
        source = (root/path).read_bytes()
        require(identity(source) == {k: pin[k] for k in ('bytes','sha256','git_blob')},
                'Frozen evidence changed: '+path)
        objects[path] = json.loads(source.decode('utf-8', errors='strict'))
        if path == JP_SOURCE:
            payload = source.decode('utf-8')
    review_raw = (root/REVIEW).read_bytes()
    require(hashlib.sha256(review_raw).hexdigest() == REVIEW_SHA, 'Reviewed portfolio changed')
    validate_review(json.loads(review_raw), objects)
    return summarize(objects, payload, manifest)

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--write-report', action='store_true')
    args = p.parse_args()
    result = audit()
    if args.write_report:
        (ROOT/REPORT).write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    require(json.loads((ROOT/REPORT).read_text()) == result, 'Committed audit does not replay')
    print(json.dumps(result['counts'], sort_keys=True))

if __name__ == '__main__':
    main()
