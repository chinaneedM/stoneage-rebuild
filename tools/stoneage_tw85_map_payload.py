"""Hash-qualified TW8.5 map-cache structure; export metadata, never map grids.

The three uint16 planes are ordinal here. Compatibility with the historical
tile/parts/event layout does not prove this build's runtime interpretation.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import struct

ROOT = Path(__file__).resolve().parents[1]
REVIEW = 'research/recovered/STONEAGE-WAYI85-MSI-CLIENT-REVIEW-R1.json'
RAW = 'research/recovered/STONEAGE-WAYI85-MSI-CLIENT-PAYLOAD-R1.json'
MAX_CELLS = 4_000_000


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def pin(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': digest(raw),
            'git_blob': hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}


def parse(raw):
    if len(raw) < 8:
        raise ValueError('short map header')
    width, height = struct.unpack_from('<II', raw)
    cells = width * height
    if not width or not height or cells > MAX_CELLS:
        raise ValueError('zero or excessive dimensions')
    if len(raw) != 8+6*cells:
        raise ValueError('not exact three-plane uint16 layout')
    planes = []
    for index in range(3):
        data = raw[8+index*2*cells:8+(index+1)*2*cells]
        counts = Counter(x[0] for x in struct.iter_unpack('<H', data))
        planes.append({'ordinal': index+1, 'bytes': len(data), 'sha256': digest(data),
                       'nonzero_cells': cells-counts.get(0, 0), 'distinct_values': len(counts),
                       'minimum': min(counts), 'maximum': max(counts),
                       'most_frequent': [{'value': value, 'cells': count} for value, count in
                                         sorted(counts.items(), key=lambda x: (-x[1], x[0]))[:10]]})
    return {'width': width, 'height': height, 'cells': cells,
            'layout': 'LE_U32_WIDTH_HEIGHT_THREE_LE_U16_PLANES_EXACT_LENGTH', 'planes': planes}


def analyze(client, expected):
    candidates = {}
    for path in client.rglob('*'):
        if path.is_file():
            rel = path.relative_to(client).as_posix()
            if re.fullmatch(r'map/\d+\.dat', rel, re.I):
                key = rel.casefold()
                if key in candidates:
                    raise ValueError('case-insensitive duplicate map path')
                candidates[key] = path
    wanted = {row['path'].casefold(): row for row in expected}
    if len(wanted) != len(expected) or set(candidates) != set(wanted):
        raise ValueError('map candidate set differs from qualified MSI inventory')
    rows = []
    for key in sorted(wanted):
        source = wanted[key]
        raw = candidates[key].read_bytes()
        if len(raw) != source['bytes'] or digest(raw) != source['sha256']:
            raise ValueError('map payload differs from qualified MSI inventory: '+key)
        row = {'path': source['path'], 'filename_numeric_token': int(Path(key).stem),
               'bytes': len(raw), 'sha256': digest(raw), 'original_place_name': None}
        try:
            row.update(parse(raw))
            row['status'] = 'EXACT_LAYOUT_MATCH'
        except ValueError as exc:
            row.update(status='LAYOUT_UNRESOLVED', reason=str(exc))
        rows.append(row)
    return rows


def report(client):
    review = json.loads((ROOT/REVIEW).read_bytes())
    raw = json.loads((ROOT/RAW).read_bytes())
    # These source identities are fixed in the already accepted payload review.
    from tools.stoneage_wayi85_payload_review import RAW_SHA256
    if digest((ROOT/RAW).read_bytes()) != RAW_SHA256:
        raise ValueError('qualified source report drift')
    from tools.stoneage_wayi85_payload_review import analyze as review_source
    if review_source(raw) != review:
        raise ValueError('MSI inventory review does not replay')
    rows = analyze(client, review['numeric_map_dat_candidates'])
    groups = defaultdict(list)
    for row in rows:
        if row['status'] == 'EXACT_LAYOUT_MATCH':
            groups[(row['width'], row['height'])].append(row['path'])
    return {'schema': 'stoneage.tw85_map_payload_structure.r1',
            'source_pins': {path: pin(ROOT/path) for path in (RAW, REVIEW)},
            'wrapper_sha256': raw['assembled_installer']['sha256'],
            'msi_sha256': raw['inspection']['msi_sha256'],
            'source_scope': 'COMMUNITY_PRESERVED_WAYI_MSI_8.50.0000_PAYLOAD',
            'files': rows, 'numeric_map_files': len(rows),
            'exact_layout_matches': sum(x['status'] == 'EXACT_LAYOUT_MATCH' for x in rows),
            'dimension_groups': [{'width': wh[0], 'height': wh[1], 'paths': paths}
                                 for wh, paths in sorted(groups.items())],
            'same_path_mixed25_byte_comparison': review['numeric_map_same_path_comparison_with_mixed25'],
            'excluded_auxiliary_dat_files': review['map_directory_auxiliary_dat_files'],
            'boundaries': {key: False for key in (
                'runtime_or_installer_executed', 'publisher_clean_disc_authenticated',
                'plane_semantics_proven_for_this_build', 'filename_token_is_authenticated_floor_id',
                'named_place_attribution_proven', 'npc_quest_spawn_tables_recovered',
                'tw10_or_jss1999_map_geometry_proven', 'full_world_coverage_proven',
                'grid_or_proprietary_asset_published', 'walkability_or_teleports_inferred')}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--client', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = report(args.client)
    args.output.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2)+'\n')
    print(json.dumps({key: result[key] for key in ('numeric_map_files', 'exact_layout_matches')}))
