"""Lossless complete-file catalog for four acquired client specimens.

Replay pinned derived inventories; never acquire, deploy, delete or publish assets.
Exact digest equality links content, not official build or entity identity.
"""
import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import json
from pathlib import Path, PurePosixPath
import re

from tools.stoneage_crossversion_audio_content import bridge_files, fields
from tools.stoneage_battle_sab_crossversion_r17 import build as battle_build

ROOT = Path(__file__).resolve().parents[1]
BASE = 'research/recovered/'
TW = BASE+'STONEAGE-TW10-CLIENT-INVENTORY-R1.txt'
MIXED = BASE+'STONEAGE-25-PRESERVED-BUNDLE-STATIC-INVENTORY-R1.txt'
CN5 = BASE+'STONEAGE-STONEAGE5-REAL-CAB-MSI-PATH-JOIN-R1.json'
LATE = BASE+'STONEAGE-WAYI85-MSI-CLIENT-PAYLOAD-R1.json'
OUTPUT = ROOT/BASE/'STONEAGE-FOUR-CLIENT-CONTENT-CATALOG-R24.json.gz'
SUMMARY = ROOT/BASE/'STONEAGE-FOUR-CLIENT-CONTENT-SUMMARY-R24.json'
PINS = {
    CN5: '69b19fc3ea988a6e3ed3047291082096a2d955f8ca24423d4280a37487fc8a92',
    TW: '413d197d19ea405490bfffc2bdbf021089177671445ca567533b2eb2576dae7b',
    MIXED: '48feb98aa977c88dcc236b530e0428ab665032ec923787eac0c293d5960159b0',
    LATE: '4ea7b43a7e3427ab4443afe801ae7d3e156e6193e1d42ce1b261f733e07de1d8',
}
PROFILES = {
    'CN5': {'source': CN5, 'expected_files': 413,
            'qualification': 'PRESERVED_CN5_DISC_CAB_FILES_JOINED_TO_MSI_PATHS_NOT_CLEAN_OFFICIAL_AUTHENTICATION',
            'official_clean_client_authenticated': False},
    'TW10': {'source': TW, 'expected_files': 383,
             'qualification': 'ACCEPTED_TW10_RETAIL_CORE_INCLUDES_8_INSTALLER_SUPPORT_FILES',
             'official_clean_client_authenticated': True},
    'MIXED25': {'source': MIXED, 'expected_files': 2302,
                'qualification': 'MIXED_COMMUNITY_CLIENT_SUBTREE_NOT_OFFICIAL_CLEAN_BUILD',
                'official_clean_client_authenticated': False},
    'CLAIMED_TW85': {'source': LATE, 'expected_files': 557,
                     'qualification': 'PROVENANCE_SUPPORTED_CANDIDATE_COMMUNITY_PRESERVED_CLAIMED_WAYI85',
                     'official_clean_client_authenticated': False},
}
LATE_PREFIX = 'Program Files/WAYI/石器時代 魔域大冒險/'
MIXED_PREFIX = '/SA2.5主程式/stoneage2.5/'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def fingerprint(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
            'git_blob': hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}


def safe_relative(path):
    need(isinstance(path, str) and path and '\\' not in path, 'invalid relative path')
    parts = path.split('/')
    need(not PurePosixPath(path).is_absolute() and all(p not in ('', '.', '..') for p in parts),
         'noncanonical relative path')
    return path  # Preserve case, Unicode and every occurrence; no casefold merging.


def parse_sources(raw):
    """Return exactly one complete-file size/digest for every source occurrence."""
    rows = []
    for line in raw[TW].decode('utf-8').splitlines():
        if not line.startswith('CORE_FILE|'):
            continue
        _, x = fields(line)
        need(x['path'].startswith('StoneAge/'), 'TW root changed')
        rows.append({'sample': 'TW10', 'original_path': x['path'],
                     'relative_path': safe_relative(x['path'][len('StoneAge/'):]),
                     'bytes': int(x['size']), 'sha256': x['sha256']})
    text = raw[MIXED].decode('utf-8')
    paths = {}
    after = False
    for line in text.splitlines():
        if line == 'ALL-FILE SHA256':
            after = True
        m = re.fullmatch(r'([0-9a-f]{64})  (.+)', line) if after else None
        if m and MIXED_PREFIX in m[2]:
            relative = m[2].split(MIXED_PREFIX, 1)[1]
            need(relative not in paths, 'repeated original mixed path')
            paths[relative] = m[2]
    for x in bridge_files(text).values():
        rows.append({'sample': 'MIXED25', 'original_path': paths[x['path']],
                     'relative_path': safe_relative(x['path']),
                     'bytes': x['bytes'], 'sha256': x['sha256']})
    late = json.loads(raw[LATE])
    need(late['official_clean_client_authenticated'] is False, 'candidate promoted to official')
    samples = late['inspection']['inventory']['samples']
    need(len(samples) == 1 and samples[0]['sample_id'] == 'TW85-INSTALLER-MSI-CLIENT',
         'late client sample changed')
    for x in samples[0]['files']:
        need(x['path'].startswith(LATE_PREFIX), 'late installation root changed')
        rows.append({'sample': 'CLAIMED_TW85', 'original_path': x['path'],
                     'relative_path': safe_relative(x['path'][len(LATE_PREFIX):]),
                     'bytes': x['size'], 'sha256': x['sha256']})
    cn = json.loads(raw[CN5])
    need(cn['status'] == '413_REAL_FILE_SHA_JOINED_TO_413_MSI_DESTINATION_PATHS', 'CN5 join status changed')
    need(cn['scope']['official_clean_client_authenticated'] is False, 'CN5 official promotion')
    for x in cn['installed_files']:
        rows.append({'sample': 'CN5', 'original_path': x['installed_path'],
                     'relative_path': safe_relative(x['installed_path']),
                     'bytes': x['size'], 'sha256': x['sha256'],
                     'cab_file_key': x['cab_file_key'], 'cab_index': x['cab_index'],
                     'msi_sequence': x['msi_sequence']})
    for sample, profile in PROFILES.items():
        subset = [x for x in rows if x['sample'] == sample]
        need(len(subset) == profile['expected_files'], 'incomplete sample '+sample)
        need(len({x['original_path'] for x in subset}) == len(subset), 'duplicate source path')
        need(len({x['relative_path'] for x in subset}) == len(subset), 'relative path collision')
    for x in rows:
        need(type(x['bytes']) is int and x['bytes'] >= 0, 'invalid file size')
        need(re.fullmatch('[0-9a-f]{64}', x['sha256']) is not None, 'invalid complete digest')
    return sorted(rows, key=lambda x: (x['sample'], x['original_path']))


def group_rows(rows):
    groups = defaultdict(list)
    for x in rows:
        groups[x['sha256']].append(x)
    contents = []
    for digest, refs in sorted(groups.items()):
        sizes = {x['bytes'] for x in refs}
        need(len(sizes) == 1, 'same digest with inconsistent byte extent')
        contents.append({'content_id': 'sha256:'+digest, 'bytes': sizes.pop(),
                         'references': [x['reference_id'] for x in refs]})
    return contents


def build():
    raw = {p: (ROOT/p).read_bytes() for p in PINS}
    for p, sha in PINS.items():
        need(hashlib.sha256(raw[p]).hexdigest() == sha, 'source bytes changed '+p)
    rows = parse_sources(raw)
    for n, x in enumerate(rows):
        x['reference_id'] = 'r24:'+str(n).zfill(4)
        x['digest_domain'] = 'COMPLETE_FILE'
    contents = group_rows(rows)
    per_sample = {}
    for sample in PROFILES:
        subset = [x for x in rows if x['sample'] == sample]
        per_sample[sample] = {'file_occurrences': len(subset),
                              'unique_contents': len({x['sha256'] for x in subset}),
                              'logical_bytes': sum(x['bytes'] for x in subset)}
    membership = Counter('+'.join(sorted({rows[int(ref.split(':')[1])]['sample']
                                         for ref in c['references']})) for c in contents)
    logical = sum(x['bytes'] for x in rows)
    unique = sum(x['bytes'] for x in contents)
    battle = battle_build()
    correction = {k: battle[k] for k in ('schema', 'digest_domain', 'supersedes',
                  'original_tw10_file_count', 'mixed25_file_count', 'same_index_sha256_equal_count',
                  'same_index_sha256_diff_count', 'all_occurrence_count', 'all_unique_sha256_count')}
    summary = {
        'schema': 'stoneage.four_client.complete_file_content_summary.r24',
        'source_head': 'f9fae070ca0dcc132f5fcca3e11baf492b1c5dd1',
        'scope': 'Four acquired specimens, not four authenticated official versions or all clients',
        'source_pins': {p: fingerprint(raw[p]) for p in PINS},
        'profiles': PROFILES, 'per_sample': per_sample,
        'occurrences': len(rows), 'unique_complete_file_contents': len(contents),
        'duplicate_reference_occurrences': len(rows)-len(contents),
        'logical_file_bytes': logical, 'unique_content_byte_budget': unique,
        'potential_duplicate_bytes': logical-unique,
        'content_membership': dict(sorted(membership.items())),
        'r17_correction': correction,
        'boundaries': {'original_source_files_deleted': 0, 'actual_bytes_saved': 0,
                       'original_asset_bytes_published': 0, 'new_original_bytes_acquired': False,
                       'all_clients_acquired': False, 'source_payloads_durably_custodied': False,
                       'same_content_proves_official_version': False,
                       'npc_pet_quest_identity_proven': False, 'original_game_world_entered': False,
                       'cn5_complete_file_digest_corpus_included': True,
                       'resource_subfile_aliases_collapsed_into_file_identity': False},
        'omissions': ['Official patch129 is a patch/resource subset, not a fourth full client',
                      'Loose files and packed resource spans are distinct identity domains'],
    }
    return {'schema': 'stoneage.four_client.complete_file_content_catalog.r24',
            'summary': summary, 'occurrences': rows, 'contents': contents}


def validate(doc):
    need(doc == build(), 'catalog differs from complete pinned source replay')
    s = doc['summary']
    need((s['occurrences'], s['unique_complete_file_contents'], s['duplicate_reference_occurrences'])
         == (3655, 2488, 1167), 'lossless complete file partition changed')
    refs = {x['reference_id']: x for x in doc['occurrences']}
    need(len(refs) == 3655, 'missing/repeated reference identifier')
    seen = []
    for c in doc['contents']:
        for ref in c['references']:
            need(ref in refs and c['content_id'] == 'sha256:'+refs[ref]['sha256']
                 and c['bytes'] == refs[ref]['bytes'], 'misbound complete file content')
            seen.append(ref)
    need(len(seen) == len(set(seen)) == len(refs), 'content partition lost/repeated occurrence')
    return s


def encoded(doc):
    return (json.dumps(doc, ensure_ascii=False, sort_keys=True, separators=(',', ':'))+'\n').encode()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    if args.write:
        doc = build()
        validate(doc)
        OUTPUT.write_bytes(gzip.compress(encoded(doc), mtime=0))
        SUMMARY.write_text(json.dumps(doc['summary'], ensure_ascii=False, indent=2)+'\n')
    doc = json.loads(gzip.decompress(OUTPUT.read_bytes()))
    summary = validate(doc)
    need(json.loads(SUMMARY.read_bytes()) == summary, 'summary drift')
    print(json.dumps({'status': 'PASS', 'occurrences': summary['occurrences'],
                      'contents': summary['unique_complete_file_contents'],
                      'r17_corrected_shared_files': summary['r17_correction']['same_index_sha256_equal_count']}))


if __name__ == '__main__':
    main()
