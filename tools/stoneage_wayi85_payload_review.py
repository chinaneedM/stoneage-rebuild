"""Replay MSI destination coverage and lossless per-version SHA relationships."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

from tools.stoneage_cross_version_file_inventory import family
from tools.stoneage_tw10_preserved25_file_intersection import ROOT, BRIDGE, BRIDGE_HASH, BRIDGE_ROOT, GIT_BLOBS, git_blob, replay

RAW = 'research/recovered/STONEAGE-WAYI85-MSI-CLIENT-PAYLOAD-R1.json'
REVIEW = 'research/recovered/STONEAGE-WAYI85-MSI-CLIENT-REVIEW-R1.json'
RAW_SHA256 = '4ea7b43a7e3427ab4443afe801ae7d3e156e6193e1d42ce1b261f733e07de1d8'
PREFIX = 'Program Files/WAYI/石器時代 魔域大冒險/'


def table(text):
    lines = text.splitlines()
    fields = lines[0].split('\t')
    rows = []
    seen = set()
    for line in lines[3:]:
        if not line:
            continue
        values = line.split('\t')
        if len(values) != len(fields) or values[0] in seen:
            raise ValueError('malformed or duplicate MSI table row')
        seen.add(values[0])
        rows.append(dict(zip(fields, values)))
    return rows


def analyze(report):
    inspection = report['inspection']
    if report['status'] != 'MSI_CLIENT_PAYLOAD_ACQUISITION_AND_INVENTORY_COMPLETE' or inspection['installed_or_executed'] is not False:
        raise ValueError('not a static MSI client payload report')
    if any(report[k] is not False for k in ('official_clean_client_authenticated', 'server_quest_pet_data_inferred', 'original_payload_published')):
        raise ValueError('unsupported evidence promotion')
    prop = {x['Property']: x['Value'] for x in table(inspection['msi_tables']['Property'])}
    if (prop['ProductName'], prop['ProductVersion'], prop['Manufacturer']) != ('石器時代 魔域大冒險', '8.50.0000', '華義國際'):
        raise ValueError('unexpected MSI product identity')
    dirs = {x['Directory']: x for x in table(inspection['msi_tables']['Directory'])}
    comps = {x['Component']: x for x in table(inspection['msi_tables']['Component'])}
    def folder(key, trail=()):
        if key == 'INSTALLDIR':
            return ''
        if key in trail or key not in dirs:
            raise ValueError('MSI directory cycle or missing ancestor')
        row = dirs[key]
        parent = folder(row['Directory_Parent'], trail+(key,))
        name = row['DefaultDir'].split(':')[0].split('|')[-1]
        return '/'.join(x for x in (parent, '' if name == '.' else name) if x)
    expected = {}
    for row in table(inspection['msi_tables']['File']):
        if row['Component_'] not in comps:
            raise ValueError('MSI file refers to absent component')
        name = row['FileName'].split('|')[-1]
        rel = '/'.join(x for x in (folder(comps[row['Component_']]['Directory_']), name) if x)
        key = rel.casefold()
        if key in expected:
            raise ValueError('duplicate MSI destination')
        expected[key] = int(row['FileSize'])
    files = inspection['inventory']['samples'][0]['files']
    actual = {}
    for row in files:
        if not row['path'].startswith(PREFIX):
            raise ValueError('file outside expected product destination')
        rel = row['path'][len(PREFIX):]
        if rel.casefold() in actual or row['family_hint'] != family(rel):
            raise ValueError('ambiguous path or altered family hint')
        actual[rel.casefold()] = row['size']
    if actual != expected:
        raise ValueError('MSI file table and actual extracted destinations differ')
    if len(files) != 557 or sum(x['size'] for x in files) != 1808555613:
        raise ValueError('incomplete original MSI payload')
    bridge_bytes = (ROOT/BRIDGE).read_bytes()
    if git_blob(bridge_bytes) != GIT_BLOBS[BRIDGE]:
        raise ValueError('bridge source changed')
    bridge = {}
    for line in bridge_bytes.decode().split('ALL-FILE SHA256\n', 1)[1].splitlines():
        m = BRIDGE_HASH.fullmatch(line)
        if m and BRIDGE_ROOT in m[2]:
            bridge[m[2].split(BRIDGE_ROOT, 1)[1]] = m[1]
    byhash = {}
    for name, digest in bridge.items():
        byhash.setdefault(digest, []).append(name)
    matches = []
    maps = []
    auxiliaries = []
    for row in files:
        rel = row['path'][len(PREFIX):]
        if row['sha256'] in byhash:
            matches.append({'tw85_path': rel, 'sha256': row['sha256'], 'bridge_paths': byhash[row['sha256']]})
        if rel.lower().startswith('map/') and rel.lower().endswith('.dat'):
            entry = {'path': rel, 'bytes': row['size'], 'sha256': row['sha256']}
            if re.fullmatch(r'map/\d+\.dat', rel.lower()):
                entry['map_id_filename_token'] = int(Path(rel).stem)
                maps.append(entry)
            else:
                auxiliaries.append(entry)
    old = replay()
    live_hashes = {x['sha256'] for x in files}
    tw_matches = [p for p in old['matched']+old['unmatched'] if p['sha256'] in live_hashes]
    if len(tw_matches) != 361 or len(maps) != 42 or len(auxiliaries) != 3:
        raise ValueError('unexpected source-qualified counts')
    bridge_by_path = {p.casefold(): digest for p, digest in bridge.items()}
    map_comparison = []
    for row in maps:
        old_sha = bridge_by_path.get(row['path'].casefold())
        status = ('ABSENT_FROM_BRIDGE_PATH' if old_sha is None else
                  'EXACT_SAME_PATH_BYTES' if old_sha == row['sha256'] else 'DIFFERENT_SAME_PATH_BYTES')
        map_comparison.append({'tw85_path': row['path'], 'tw85_sha256': row['sha256'],
                               'bridge_sha256_at_same_path': old_sha, 'status': status})
    return {'schema': 'stoneage.wayi85_msi_payload_review_r1', 'file_count': len(files),
            'logical_file_bytes': sum(x['size'] for x in files),
            'msi_table_destination_and_size_join': 'EXACT_557_OF_557',
            'msi_product': {k: prop[k] for k in ('ProductName', 'ProductVersion', 'Manufacturer', 'ProductLanguage')},
            'tw10_core_exact_file_matches': tw_matches,
            'preserved25_exact_file_matches': matches,
            'numeric_map_dat_candidates': maps, 'map_directory_auxiliary_dat_files': auxiliaries,
            'numeric_map_same_path_comparison_with_mixed25': map_comparison,
            'graphics_animation_containers': inspection['graphics_animation_files'],
            'boundaries': {'pe_wrapper_21_sections_count_as_client_files': False,
                           'all_45_dat_files_are_world_maps': False, 'map_ids_identify_named_world_places': False,
                           'resource_bytes_equal_pet_species': False, 'original_server_tables_recovered': False,
                           'same_filename_is_same_build_or_semantics': False,
                           'byte_change_proves_world_geometry_or_patch_change': False,
                           'full_world_map_coverage_proven': False, 'package_filename_is_release_date': False}}


def validate():
    raw = (ROOT/RAW).read_bytes()
    if hashlib.sha256(raw).hexdigest() != RAW_SHA256:
        raise ValueError('source artifact raw bytes changed')
    actual = analyze(json.loads(raw))
    if actual != json.loads((ROOT/REVIEW).read_bytes()):
        raise ValueError('archived payload review drift')
    receipt = json.loads((ROOT/'research/recovered/STONEAGE-WAYI85-MSI-PAYLOAD-CUSTODY-R1.json').read_bytes())
    for section in ('legacy_source_pins', 'current_derived_pins'):
        for path, pin in receipt[section].items():
            data = (ROOT/path).read_bytes()
            if pin != {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'git_blob': git_blob(data)}:
                raise ValueError('custody source pin changed: '+path)
    if set(receipt['historical_prefixes']) != {'docs/CURRENT-STATE.md', 'docs/HISTORICAL-TIMELINE.md',
                                               'docs/SOURCE-REGISTRY.md', 'docs/RESTORATION-ROADMAP-R2.md'}:
        raise ValueError('incomplete historical prefix coverage')
    for path, pin in receipt['historical_prefixes'].items():
        old = subprocess.check_output(['git', 'show', receipt['base_main']+':'+path], cwd=ROOT)
        if len(old) != pin['bytes'] or git_blob(old) != pin['git_blob'] or not (ROOT/path).read_bytes().startswith(old):
            raise ValueError('historical prefix lost: '+path)
    return {'status': 'PASS', 'file_count': actual['file_count'], 'numeric_map_dat_candidates': 42}


if __name__ == '__main__':
    print(json.dumps(validate(), sort_keys=True))
