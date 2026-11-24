"""Audit indexed pet pixels from preserved CN5.0; emit only derived metadata."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import gzip
import hashlib
import json
import mmap
from pathlib import Path
import struct

from tools.stoneage_pet_high_first_cn50_catalog import git_blob
from tools.stoneage_pet_high_first_cn50_native import verify_originals
from tools.stoneage_rd_codec import decode_rd_block
from tools.stoneage_tw10_cn50_resource_acquisition import validate_pinned_target

ROOT = Path(__file__).resolve().parents[1]
PETS = Path('research/pets')
RECOVERED = Path('research/recovered')
CN = RECOVERED / 'cn50-resource-metadata'
TARGET = ROOT / PETS / 'PET-HIGH-FIRST-11-PC-INDEXED-PIXEL-RECEIPTS-R1.json.gz'
INPUTS = {
    'cn50_album': (PETS / 'PET-HIGH-FIRST-CN50-NATIVE-SPR-ALBUM-R1.json', '98fea71c051dfa887b91154a8a72d17c67b57744'),
    'cn50_tw85_retention': (PETS / 'PET-HIGH-FIRST-CN50-TW85-ART-RETENTION-R1.json', 'afb666ecb451aa1cd43fb8a903403419f6b31cff'),
    'tw85_visual': (PETS / 'PET-HIGH-FIRST-TW85-VISUAL-ACTION-REFERENCES-R1.json', '3bcfbba98cfb915b14679ba472dbc554db297018'),
    'cab': (RECOVERED / 'STONEAGE-STONEAGE5-REAL-CAB-PAYLOAD-R1.json', '1edbd31872386753bf9fc62a2260db316ccf84ed'),
    'adrn': (CN / 'ADRN-R1.tsv.gz', '127670eaf2bc19ba9d15776d090a8307058f729d'),
    'group': (CN / 'SPR-GROUP-R1.tsv.gz', 'f4a41ba999167185b55a42c89ece9e24d456e637'),
    'animation': (CN / 'SPR-ANIMATION-R1.tsv.gz', '0da62abce6aecd476ca95f6fc2a8679105d0b09d'),
    'frame': (CN / 'SPR-FRAME-R1.tsv.gz', '6e98e5fea26a69aa5c7042bab1707c7a330c6bf7'),
}
UNLINKED = 'EARLY_TW10_NOT_LINKED'
CONTAINERS = ('sa_5000.exe', 'adrn_31.bin', 'real_31.bin', 'spradrn_17.bin', 'spr_17.bin')


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def load_pinned():
    for path, digest in INPUTS.values():
        if git_blob((ROOT / path).read_bytes()) != digest:
            raise ValueError(f'pinned source changed: {path}')
    return {key: json.loads((ROOT / path).read_bytes())
            for key, (path, _) in INPUTS.items() if path.suffix == '.json'}


def rows(key):
    with gzip.open(ROOT / INPUTS[key][0], 'rt', encoding='utf-8', newline='') as stream:
        yield from csv.DictReader(stream, delimiter='\t')


def expected_files(cab):
    return {row['name']: (row['size'], row['sha256'])
            for row in cab['files']['inventory'] if row['name'] in CONTAINERS}


def make_plan(data):
    album = data['cn50_album']['records']
    retained = {row['cn50_album_ordinal']: row for row in data['cn50_tw85_retention']['records']}
    tw85 = data['tw85_visual']
    unlinked = [row for row in album if row['earlier_tw10_relation'] == UNLINKED]
    eligible_groups = {row['spr_group'] for pet in unlinked for row in pet['spr_groups']
                       if row['held_pet_path_also_maps_to_slot']}
    animations = defaultdict(list)
    for row in rows('animation'):
        group = int(row['spr_no'])
        if group in eligible_groups and row['direction'] == '0' and row['anim_no'] == '2':
            if 3 <= int(row['frame_count']) <= 16:
                animations[group].append(row)
    candidate_keys = {(row['group_index'], row['anim_index'])
                      for group in animations.values() for row in group}
    frames = defaultdict(list)
    for row in rows('frame'):
        key = row['group_index'], row['anim_index']
        if key in candidate_keys:
            frames[key].append(row)

    portraits = {num for row in album for num in row['portrait_bitmap_numbers_in_file_order']}
    wanted = portraits | {int(row['bmp_no']) for sequence in frames.values()
                          for row in sequence if row['sentinel'] == '0'}
    blocks = defaultdict(list)
    for row in rows('adrn'):
        bitmap = int(row['bitmapno'])
        if bitmap in wanted:
            blocks[bitmap].append(row)
    if set(blocks) != wanted or any(len(records) != 1 for records in blocks.values()):
        raise ValueError('missing or ambiguous physical bitmap in CN50 reference')
    blocks = {number: records[0] for number, records in blocks.items()}

    groups = {int(row['spr_no']): row for row in rows('group')}
    pets = []
    for row in album:
        ordinal = row['ordinal']
        old_relation = row['earlier_tw10_relation']
        alias = row['portrait_alias']
        bitmap = row['portrait_lookup_after_ordered_load']
        inherited = retained[ordinal]
        if ((alias, bitmap, row['portrait_lookup_rd_sha256']) !=
                (inherited['cn50_portrait_alias'], inherited['cn50_selected_physical_bitmap'], blocks[bitmap]['rd_block_sha256'])):
            raise ValueError(f'portrait reference disagreement: {ordinal}')
        pet = {'ordinal': ordinal, 'source_id': row['source_record_id'], 'name': row['compiled_name'],
               'cn50_name_row_sha256': row['exe_row_sha256'], 'early_tw10_relation': old_relation,
               'portrait_alias': alias, 'portrait_bitmaps_in_file_order': row['portrait_bitmap_numbers_in_file_order'],
               'portrait_selected_bitmap': bitmap, 'sample': None}
        if old_relation == UNLINKED:
            # Pick the highest held-pet SPR number with a bounded sequence. The
            # numeric action/direction have no inferred gameplay names here.
            for group in sorted(row['spr_groups'], key=lambda item: item['spr_group'], reverse=True):
                number = group['spr_group']
                if not group['held_pet_path_also_maps_to_slot']:
                    continue
                for animation in animations[number]:
                    sequence = frames[animation['group_index'], animation['anim_index']]
                    if len(sequence) != int(animation['frame_count']):
                        raise ValueError('frame count disagrees with header')
                    if any(frame['sentinel'] != '0' for frame in sequence):
                        continue
                    if (groups[number]['segment_sha256'] != group['sha256'] or
                            groups[number]['index'] != animation['group_index'] or
                            [int(frame['frame_index']) for frame in sequence] != list(range(len(sequence)))):
                        raise ValueError('original animation ordering or group binding changed')
                    pet['sample'] = {
                        'spr': number, 'group_index': int(animation['group_index']),
                        'group_sha256': group['sha256'], 'animation_index': int(animation['anim_index']),
                        'direction': 0, 'action': 2, 'duration_word': int(animation['duration']),
                        'frames': [[int(frame[key]) for key in ('bmp_no', 'pos_x', 'pos_y', 'sound_no')]
                                   for frame in sequence],
                    }
                    break
                if pet['sample'] is not None:
                    break
        pets.append(pet)

    linked_tw85 = []
    album_by_bitmap = {pet['portrait_selected_bitmap']: pet for pet in pets}
    for entry in tw85['records']:
        for exe, route in entry['original_native_program_routes'].items():
            if route['status'] != 'SOURCE_LOCAL_NAMED_ROUTE':
                continue
            alias = route['source_portrait_alias']
            for portrait in tw85['portrait_alias_to_saved_tw85_native_rd_candidates'].get(str(alias), ()):
                bitmap = portrait['physical_bitmapno']
                if bitmap not in album_by_bitmap:
                    continue
                cn50 = album_by_bitmap[bitmap]
                inherited = retained[cn50['ordinal']]
                digest = portrait['saved_tw85_real_rd_sha256']
                if (alias != cn50['portrait_alias'] or digest != blocks[bitmap]['rd_block_sha256'] or
                        digest != inherited['tw85_same_physical_portrait_rd_sha256'] or
                        not any(x['physical_bitmap'] == bitmap and x['same_cn50_selected_rd'] and
                                x['original_patch_full_adrn_record_sha256'] == portrait['full_patch_adrn_record_sha256']
                                for x in inherited['official_patch_alias_matches'])):
                    continue
                linked_tw85.append({'spr': entry['tw85_original_spr_no_not_official_pet_id'],
                                   'exe': exe, 'tw85_name': route['original_name_cp950'],
                                   'tw85_name_row_sha256': route['original_28b_record_sha256'],
                                   'tw85_slot': route['local_album_slot'], 'alias': alias,
                                   'bitmap': bitmap, 'cn50_source_id': cn50['source_id'],
                                   'full_adrn_record_sha256': portrait['full_patch_adrn_record_sha256']})
    return pets, blocks, linked_tw85


def extract_pixels(real, adrn, row):
    from tools.stoneage_scene07_independent_pixels import independent_rd

    index, bitmap, offset, size, width, height = (int(row[key]) for key in
        ('index', 'bitmapno', 'adder', 'size', 'width', 'height'))
    raw_record = adrn[index*80:(index+1)*80]
    if (struct.unpack_from('<IIIiiii', raw_record) !=
            (bitmap, offset, size, int(row['xoff']), int(row['yoff']), width, height) or
            sha256(raw_record[28:]) != row['attr_sha256']):
        raise ValueError(f'original ADRN row differs from archived source: {bitmap}')
    if not (16 <= size and offset + size <= len(real) and width > 0 and height > 0 and
            width * height <= 1_000_000):
        raise ValueError(f'invalid original block bounds: {bitmap}')
    rd = real[offset:offset+size]
    if sha256(rd) != row['rd_block_sha256']:
        raise ValueError(f'original RD block differs from archived source: {bitmap}')
    header, indices = decode_rd_block(rd, authoritative_block_size=size)
    if ((header['width_s'], header['height_s'], header['flag']) != (width, height, int(row['rd_flag'])) or
            independent_rd(rd) != (width, height, indices)):
        raise ValueError(f'original indexed pixels disagree between decoders: {bitmap}')
    return {'adrn_index': index, 'adrn_sha256': sha256(raw_record), 'rd_offset': offset, 'rd_bytes': size,
            'rd_sha256': row['rd_block_sha256'], 'width': width, 'height': height,
            'index_pixels_sha256': sha256(indices)}


def selected_bitmaps(pets):
    portraits = {bitmap for pet in pets for bitmap in pet['portrait_bitmaps_in_file_order']}
    motion = {frame[0] for pet in pets if pet['sample'] for frame in pet['sample']['frames']}
    return portraits, motion


def replay(source_dir, data, pets, blocks):
    source = expected_files(data['cab'])
    for filename in CONTAINERS:
        validate_pinned_target(source_dir / filename, filename, source)
    verify_originals(source_dir, data['cn50_album'])
    adrn = (source_dir / 'adrn_31.bin').read_bytes()
    portraits, motion = selected_bitmaps(pets)
    with (source_dir / 'real_31.bin').open('rb') as stream, mmap.mmap(stream.fileno(), 0, access=mmap.ACCESS_READ) as real:
        return {str(bitmap): extract_pixels(real, adrn, blocks[bitmap]) for bitmap in sorted(portraits | motion)}


def validate(receipt, data, pets, blocks, tw85):
    if receipt['scope'] != 'PRESERVED_CLASSIC_PC_ASSET_EVIDENCE_ONLY':
        raise ValueError('receipt scope changed')
    pins = {str(path): digest for path, digest in INPUTS.values()}
    source = {name: {'bytes': size, 'sha256': digest} for name, (size, digest) in expected_files(data['cab']).items()}
    if receipt['source_git_blobs'] != pins or receipt['cn50_complete_files_verified'] != source:
        raise ValueError('receipt provenance changed')
    if receipt['cn50_album'] != pets or receipt['tw85_exact_portrait_routes'] != tw85:
        raise ValueError('receipt native name, portrait or animation linkage changed')
    portraits, motion = selected_bitmaps(pets)
    observed = receipt['cn50_observed_blocks']
    if set(observed) != {str(bitmap) for bitmap in portraits | motion}:
        raise ValueError('receipt missing or extraneous original blocks')
    for number, row in observed.items():
        reference = blocks[int(number)]
        if (row['rd_sha256'] != reference['rd_block_sha256'] or
                any(row[observed_key] != int(reference[source_key]) for observed_key, source_key in
                    (('adrn_index', 'index'), ('rd_offset', 'adder'), ('rd_bytes', 'size'),
                     ('width', 'width'), ('height', 'height')))):
            raise ValueError(f'receipt physical block differs: {number}')
        for key in ('adrn_sha256', 'index_pixels_sha256'):
            if len(bytes.fromhex(row[key])) != 32:
                raise ValueError(f'invalid {key}: {number}')
    for route in tw85:
        if observed[str(route['bitmap'])]['adrn_sha256'] != route['full_adrn_record_sha256']:
            raise ValueError('observed CN50 ADRN row differs from TW85 patch-backed row')
    return {'cn50_named_slots': len(pets), 'cn50_portrait_blocks': len(portraits),
            'cn50_earlier_relations': dict(Counter(pet['early_tw10_relation'] for pet in pets)),
            'cn50_sampled_sequences': sum(pet['sample'] is not None for pet in pets),
            'cn50_sampled_frame_positions': sum(len(pet['sample']['frames']) for pet in pets if pet['sample']),
            'cn50_sampled_frame_blocks': len(motion), 'cn50_distinct_observed_blocks': len(observed),
            'tw85_exact_portrait_bitmaps_read_from_cn50': len({route['bitmap'] for route in tw85}),
            'tw85_original_name_routes_linked_to_observed_portraits': len(tw85)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir', type=Path, help='directory with the four privately extracted CN50 containers')
    args = parser.parse_args()
    data = load_pinned()
    pets, blocks, tw85 = make_plan(data)
    if args.source_dir is not None:
        observed = replay(args.source_dir, data, pets, blocks)
        receipt = {'scope': 'PRESERVED_CLASSIC_PC_ASSET_EVIDENCE_ONLY',
                   'source_git_blobs': {str(path): digest for path, digest in INPUTS.values()},
                   'cn50_complete_files_verified': {name: {'bytes': size, 'sha256': digest}
                                                    for name, (size, digest) in expected_files(data['cab']).items()},
                   'cn50_album': pets, 'cn50_observed_blocks': observed, 'tw85_exact_portrait_routes': tw85}
        summary = validate(receipt, data, pets, blocks, tw85)
        encoded = (json.dumps(receipt, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n').encode()
        TARGET.write_bytes(gzip.compress(encoded, mtime=0))
    else:
        receipt = json.loads(gzip.decompress(TARGET.read_bytes()))
        summary = validate(receipt, data, pets, blocks, tw85)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))


if __name__ == '__main__':
    main()
