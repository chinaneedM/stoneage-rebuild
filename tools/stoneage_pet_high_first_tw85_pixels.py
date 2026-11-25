"""Read pinned, saved TW85 assets and publish only indexed-pixel digests and source links."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import json
import mmap
from pathlib import Path
import struct
import tempfile

from tools.stoneage_cn50_spr_metadata import export_cn50_spr
from tools.stoneage_pet_high_first_cn50_catalog import git_blob
from tools.stoneage_pet_high_first_tw85_material import INPUTS as PET09_INPUTS
from tools.stoneage_rd_codec import RDDecodeError, decode_rd_block
from tools.stoneage_tw85_r30_preview import ADRN_ORIGINAL, REAL_ORIGINAL, original_check
from tools.stoneage_tw85_spr137_material_r28 import ORIGINALS, qualify_pair, source_rows

ROOT = Path(__file__).resolve().parents[1]
PET09 = ROOT / 'research/pets/PET-HIGH-FIRST-TW85-VISUAL-ACTION-REFERENCES-R1.json'
TARGET = ROOT / 'research/pets/PET-HIGH-FIRST-12-TW85-INDEXED-PIXELS-R1.json.gz'
ANIMATION = ROOT / 'research/recovered/tw85-spr137-r28/SPR-ANIMATION-R28.tsv.gz'
PINS = {
    PET09: '3bcfbba98cfb915b14679ba472dbc554db297018',
    ANIMATION: '240a4d034842f7732261d88109e8534cae018822',
    **{ROOT / path: digest for key, (path, digest) in PET09_INPUTS.items()
       if key in ('r28_groups', 'r28_frames', 'native')},
}
SOURCE_FILES = {**ORIGINALS, 'adrn_158.bin': ADRN_ORIGINAL, 'real_158.bin': REAL_ORIGINAL}
COLS = struct.Struct('<IIIiiii48xI')
SCOPE = 'PRESERVED_TW85_CLASSIC_PC_SOURCE_ONLY'


def sha(blob):
    return hashlib.sha256(blob).hexdigest()


def build_plan():
    for path, digest in PINS.items():
        if git_blob(path.read_bytes()) != digest:
            raise ValueError(f'archived input changed: {path.name}')
    atlas = json.loads(PET09.read_bytes())
    known = {}
    aliases = set()
    for row in atlas['records']:
        routes = {exe: candidate for exe, candidate in row['original_native_program_routes'].items()
                  if candidate['status'] == 'SOURCE_LOCAL_NAMED_ROUTE'}
        if not routes:
            continue
        aliases.update(candidate['source_portrait_alias'] for candidate in routes.values())
        for group in row['original_physical_sprite_occurrences']:
            index = group['original_source_group_index']
            if index in known:
                raise ValueError(f'duplicate physical SPR group: {index}')
            known[index] = (row['tw85_original_spr_no_not_official_pet_id'],
                            group['original_full_spr_segment_sha256'])
    if (len(known), len(aliases)) != (518, 207):
        raise ValueError('PET09 named source scope changed')
    sequences = select_sequences(known)
    selected = {sequence['physical_group'] for sequence in sequences}
    return atlas, sorted(aliases), sorted(set(known) - selected), sequences


def select_sequences(known):
    """Choose one bounded original sequence per requested physical SPR group."""
    choices = {}
    for row in source_rows(ANIMATION):
        index = int(row['group_index'])
        count = int(row['frame_count'])
        if index not in known or not 2 <= count <= 32:
            continue
        direction, action, original_index = map(int, (row['direction'], row['anim_no'], row['anim_index']))
        score = (direction != 0, action != 2, original_index)
        if index not in choices or score < choices[index][0]:
            choices[index] = (score, row)
    sequences = {}
    for index, (_, row) in choices.items():
        number, segment_sha = known[index]
        if int(row['spr_no']) != number:
            raise ValueError(f'physical SPR group drift: {index}')
        sequences[index] = {
            'spr': number, 'physical_group': index,
            'spr_segment_sha256': segment_sha,
            'animation_index': int(row['anim_index']), 'direction': int(row['direction']),
            'action': int(row['anim_no']), 'duration_word': int(row['duration']), 'frames': [],
        }
    for row in source_rows(ROOT / PET09_INPUTS['r28_frames'][0]):
        index = int(row['group_index'])
        sequence = sequences.get(index)
        if sequence is None or int(row['anim_index']) != sequence['animation_index']:
            continue
        if int(row['frame_index']) != len(sequence['frames']):
            raise ValueError(f'original SPR frame sequence reordered: {index}')
        number = None if row['sentinel'] == '1' else int(row['bmp_no'])
        sequence['frames'].append([number, int(row['pos_x']), int(row['pos_y']), int(row['sound_no'])])
    for index, sequence in sequences.items():
        if len(sequence['frames']) != int(choices[index][1]['frame_count']):
            raise ValueError(f'original header/frame mismatch: {index}')
    return [sequences[i] for i in sorted(sequences)]


def native_candidates(wanted, frames):
    refs = defaultdict(list)
    for row in source_rows(ROOT / PET09_INPUTS['native'][0]):
        index, bitmap = int(row['index']), int(row['bitmapno'])
        if index in wanted or bitmap in frames:
            refs[bitmap].append(row)
    for bitmap in frames:
        if len(refs[bitmap]) != 1:
            raise ValueError(f'ambiguous or absent original frame block {bitmap}')
    return refs


def inspect(directory, plan):
    from tools.stoneage_scene07_independent_pixels import independent_rd

    atlas, aliases, no_sequence, sequences = plan
    qualify_pair(directory)
    for filename in ('adrn_158.bin', 'real_158.bin'):
        original_check(directory / filename, SOURCE_FILES[filename])
    with tempfile.TemporaryDirectory() as temporary:
        paths = [Path(temporary) / key for key in ('group', 'animation', 'frame')]
        export_cn50_spr(directory / 'spradrn_137.bin', directory / 'spr_137.bin', *paths)
        for path, source in zip(paths, (ROOT / PET09_INPUTS['r28_groups'][0], ANIMATION,
                                        ROOT / PET09_INPUTS['r28_frames'][0]), strict=True):
            if path.read_bytes() != source.read_bytes():
                raise ValueError(f'full original SPR export differs: {path.name}')
    adrn = (directory / 'adrn_158.bin').read_bytes()
    portraits = {alias: [] for alias in aliases}
    for index, (bitmap, *_, alias) in enumerate(COLS.iter_unpack(adrn)):
        if alias in portraits:
            portraits[alias].append([index, bitmap])
    frames = {frame[0] for sequence in sequences for frame in sequence['frames'] if frame[0] is not None}
    portrait_indices = {i for pairs in portraits.values() for i, _ in pairs}
    refs = native_candidates(portrait_indices, frames)
    bitmap_rows = {int(row['index']): row for rows in refs.values() for row in rows}
    for alias, candidates in atlas['portrait_alias_to_saved_tw85_native_rd_candidates'].items():
        for candidate in candidates:
            for row in candidate['native_exact_candidates']:
                index, number = row['original_native_index'], row['bitmapno']
                if [index, number] not in portraits[int(alias)]:
                    raise ValueError(f'patch portrait does not agree with original alias: {alias}')
    selected = portrait_indices | {int(refs[b][0]['index']) for b in frames}
    observations = {}
    with (directory / 'real_158.bin').open('rb') as stream, mmap.mmap(stream.fileno(), 0, access=mmap.ACCESS_READ) as real:
        for index in sorted(selected):
            raw = adrn[index * 80:(index + 1) * 80]
            number, offset, size, _, _, width, height, _ = COLS.unpack(raw)
            expected = bitmap_rows[index]
            if sha(raw) != expected['record_sha256'] or not 16 <= size <= len(real) - offset:
                raise ValueError(f'original ADRN row/extent drift: {index}')
            block = real[offset:offset + size]
            digest = sha(block)
            if digest != expected['rd_sha256']:
                raise ValueError(f'original RD bytes drift: {index}')
            pixels_sha = None
            status = 'UNSUPPORTED_INDEX_ENCODING'
            if width > 0 and height > 0 and width * height <= 1_000_000 and block[2] in (0, 1):
                try:
                    header, pixels = decode_rd_block(block, authoritative_block_size=size)
                    peer = independent_rd(block)
                except (RDDecodeError, ValueError):
                    status = 'INDEX_DECODE_REJECTED'
                else:
                    if (header['width_s'], header['height_s'], pixels) != peer or peer[:2] != (width, height):
                        raise ValueError(f'independent pixel decoders disagree: {index}')
                    pixels_sha = sha(pixels)
                    status = 'DUAL_DECODED_INDEX_PIXELS'
            observations[str(index)] = {'bitmap': number, 'adrn_sha256': expected['record_sha256'],
                                        'rd_sha256': digest, 'width': width, 'height': height,
                                        'index_pixels_sha256': pixels_sha, 'status': status}
    return {
        'scope': SCOPE,
        'source_files': {name: {'bytes': size, 'sha256': digest} for name, (size, digest) in SOURCE_FILES.items()},
        'source_git_blobs': {str(path.relative_to(ROOT)): digest for path, digest in PINS.items()},
        'portraits_by_original_alias': {str(alias): candidates for alias, candidates in portraits.items()},
        'sequences': sequences,
        'physical_groups_without_bounded_sequence': no_sequence,
        'frame_bitmap_to_adrn_index': {str(b): int(refs[b][0]['index']) for b in sorted(frames)},
        'observed_blocks': observations,
    }


def verify(report, plan):
    atlas, aliases, no_sequence, sequences = plan
    portraits = report['portraits_by_original_alias']
    if (report['scope'] != SCOPE or report['sequences'] != sequences or
            report['physical_groups_without_bounded_sequence'] != no_sequence or
            set(portraits) != {str(x) for x in aliases} or
            report['source_files'] != {p: {'bytes': n, 'sha256': h} for p, (n, h) in SOURCE_FILES.items()} or
            report['source_git_blobs'] != {str(p.relative_to(ROOT)): h for p, h in PINS.items()}):
        raise ValueError('source attribution or sequence plan drift')
    frames = {frame[0] for s in sequences for frame in s['frames'] if frame[0] is not None}
    frame_ref = report['frame_bitmap_to_adrn_index']
    if set(frame_ref) != {str(b) for b in frames}:
        raise ValueError('frame reference coverage drift')
    portrait_indices = set()
    for alias, candidates in portraits.items():
        order = [row[0] for row in candidates]
        if order != sorted(set(order)) or portrait_indices.intersection(order):
            raise ValueError(f'duplicate ADRN portrait row or order change: {alias}')
        portrait_indices.update(order)
        for large in atlas['portrait_alias_to_saved_tw85_native_rd_candidates'].get(alias, ()):
            for row in large['native_exact_candidates']:
                if [row['original_native_index'], row['bitmapno']] not in candidates:
                    raise ValueError(f'missing existing exact patch portrait {alias}')
    refs = native_candidates(portrait_indices, frames)
    expected = {str(row['index']): row for rows in refs.values() for row in rows
                if int(row['index']) in portrait_indices or int(row['bitmapno']) in frames}
    observations = report['observed_blocks']
    if expected.keys() != observations.keys():
        raise ValueError('physical observed blocks missing or added')
    for key, row in observations.items():
        reference = expected[key]
        if (row['rd_sha256'], row['adrn_sha256'], row['bitmap'], row['width'], row['height']) != (
            reference['rd_sha256'], reference['record_sha256'], *(int(reference[k]) for k in ('bitmapno', 'width', 'height'))):
            raise ValueError(f'physical observed block drift: {key}')
        digest = row['index_pixels_sha256']
        if row['status'] == 'DUAL_DECODED_INDEX_PIXELS':
            if not isinstance(digest, str) or len(bytes.fromhex(digest)) != 32:
                raise ValueError(f'invalid index pixel digest: {key}')
        elif digest is not None or row['status'] not in ('UNSUPPORTED_INDEX_ENCODING', 'INDEX_DECODE_REJECTED'):
            raise ValueError(f'unsupported status or unverified pixel digest: {key}')
    for b, index in frame_ref.items():
        if observations[str(index)]['bitmap'] != int(b):
            raise ValueError(f'physical reference changed: {b}')
    for candidates in portraits.values():
        if any(observations[str(index)]['bitmap'] != number for index, number in candidates):
            raise ValueError('portrait bitmap identity changed')
    decoded = {int(i) for i, row in observations.items() if row['status'] == 'DUAL_DECODED_INDEX_PIXELS'}
    complete = [s for s in sequences if any(f[0] is not None for f in s['frames']) and
                all(f[0] is None or frame_ref[str(f[0])] in decoded for f in s['frames'])]
    return {'portrait_aliases_with_records': sum(bool(v) for v in portraits.values()),
            'portrait_aliases_outside_patch_with_records': sum(bool(v) and not atlas['portrait_alias_to_saved_tw85_native_rd_candidates'].get(alias)
                for alias, v in portraits.items()),
            'portrait_records': len(portrait_indices), 'portrait_records_decoded': len(decoded & portrait_indices),
            'sampled_groups': len(sequences), 'sampled_groups_fully_decoded': len(complete),
            'sampled_positions': sum(len(s['frames']) for s in sequences),
            'sampled_physical_frame_blocks': len(frame_ref),
            'block_status': dict(Counter(row['status'] for row in observations.values()))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir', type=Path)
    parser.add_argument('--receipt', type=Path, default=TARGET)
    args = parser.parse_args()
    plan = build_plan()
    report = inspect(args.source_dir, plan) if args.source_dir else json.loads(gzip.decompress(args.receipt.read_bytes()))
    print(json.dumps(verify(report, plan), ensure_ascii=False, sort_keys=True))
    if args.source_dir:
        payload = (json.dumps(report, sort_keys=True, separators=(',', ':')) + '\n').encode()
        args.receipt.write_bytes(gzip.compress(payload, mtime=0))


if __name__ == '__main__':
    main()
