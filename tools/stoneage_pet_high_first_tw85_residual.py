"""PET13: complete bounded TW85 long/failed samples, retaining original pixel failures."""
from __future__ import annotations

import argparse
import gzip
import json
import mmap
from pathlib import Path

from tools import stoneage_pet_high_first_tw85_pixels as base
from tools.stoneage_rd_codec import decode_rd_block, parse_rd_header, RDDecodeError

TARGET = base.ROOT / 'research/pets/PET-HIGH-FIRST-13-TW85-LONG-AND-SPECIAL-R1.json.gz'
PRIOR_SHA256 = 'e5da62e07eba449ba83bf238e70979e29aa69bad7f931241968dea282d9f3382'
SCOPE = 'PRESERVED_TW85_CLASSIC_PC_LONG_AND_SPECIAL_SOURCE_ONLY'


def old_receipt():
    raw = base.TARGET.read_bytes()
    if base.sha(raw) != PRIOR_SHA256:
        raise ValueError('PET12 receipt changed')
    return json.loads(gzip.decompress(raw))


def complete(seq, receipt):
    return any(f[0] is not None for f in seq['frames']) and all(
        f[0] is None or receipt['observed_blocks'][
            str(receipt['frame_bitmap_to_adrn_index'][str(f[0])])]['status']
        == 'DUAL_DECODED_INDEX_PIXELS' for f in seq['frames'])


def build_plan():
    prior = old_receipt()
    original = base.build_plan()
    base.verify(prior, original)
    atlas, aliases, long_groups, old_sequences = original
    failed = {s['physical_group']: s for s in old_sequences if not complete(s, prior)}
    bad = {o['bitmap'] for o in prior['observed_blocks'].values()
           if o['status'] != 'DUAL_DECODED_INDEX_PIXELS'}
    if (len(long_groups), len(failed), len(bad)) != (12, 8, 7):
        raise ValueError('PET12 residual scope drift')
    wanted = set(long_groups) | set(failed)
    groups = {}
    for row in atlas['records']:
        for group in row['original_physical_sprite_occurrences']:
            index = group['original_source_group_index']
            if index in wanted:
                groups[index] = (row['tw85_original_spr_no_not_official_pet_id'],
                                 group['original_full_spr_segment_sha256'])
    if set(groups) != wanted:
        raise ValueError('residual group identity')
    candidates = {}
    for row in base.source_rows(base.ANIMATION):
        index = int(row['group_index'])
        count = int(row['frame_count'])
        if index not in wanted or not 2 <= count <= 41:
            continue
        spr, segment = groups[index]
        if int(row['spr_no']) != spr:
            raise ValueError('SPR group drift')
        anim = int(row['anim_index'])
        key = (index, anim)
        if key in candidates:
            raise ValueError('duplicate candidate animation')
        candidates[key] = {'spr': spr, 'physical_group': index, 'spr_segment_sha256': segment,
                           'animation_index': anim, 'direction': int(row['direction']),
                           'action': int(row['anim_no']), 'duration_word': int(row['duration']),
                           'frames': [], '_count': count}
    for row in base.source_rows(base.ROOT / base.PET09_INPUTS['r28_frames'][0]):
        key = int(row['group_index']), int(row['anim_index'])
        seq = candidates.get(key)
        if seq is None:
            continue
        if int(row['frame_index']) != len(seq['frames']):
            raise ValueError('residual frame order')
        bmp = None if row['sentinel'] == '1' else int(row['bmp_no'])
        seq['frames'].append([bmp, int(row['pos_x']), int(row['pos_y']), int(row['sound_no'])])
    by_group = {i: [] for i in wanted}
    for key, seq in candidates.items():
        if len(seq['frames']) != seq.pop('_count'):
            raise ValueError('residual sequence count')
        by_group[key[0]].append(seq)
    selected = []
    reasons = {}
    for index in sorted(wanted):
        options = by_group[index]
        if index in long_groups:
            if len(options) != 1 or len(options[0]['frames']) not in (37, 41):
                raise ValueError('long sequence scope drift')
            choice = options[0]
            reasons[str(index)] = 'ORIGINAL_LONG_SEQUENCE'
        else:
            eligible = [s for s in options if any(f[0] is not None for f in s['frames'])
                        and not any(f[0] in bad for f in s['frames'])]
            if eligible:
                choice = min(eligible, key=lambda s: (s['direction'] != 0, s['action'] != 2,
                                                       s['animation_index']))
                reasons[str(index)] = 'ALTERNATE_AVOIDS_PREVIOUS_BAD_BLOCKS'
            else:
                choice = failed[index]
                reasons[str(index)] = 'NO_ALTERNATE_WITHOUT_KNOWN_BAD_BLOCKS'
        selected.append(choice)
    if len(selected) != 20 or sum(len(s['frames']) for s in selected
                                  if s['physical_group'] in long_groups) != 468:
        raise ValueError('residual target conservation')
    return (atlas, aliases, [], selected), prior, reasons


def diagnose(directory, prior):
    from tools.stoneage_scene07_independent_pixels import independent_rd

    adrn = (directory / 'adrn_158.bin').read_bytes()
    result = {}
    with (directory / 'real_158.bin').open('rb') as f, mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as real:
        for key, old in prior['observed_blocks'].items():
            if old['status'] == 'DUAL_DECODED_INDEX_PIXELS':
                continue
            i = int(key)
            raw = adrn[i * 80:(i + 1) * 80]
            bmp, off, size, _, _, w, h, _ = base.COLS.unpack(raw)
            block = real[off:off + size]
            if (base.sha(raw), base.sha(block), bmp, w, h) != (
                    old['adrn_sha256'], old['rd_sha256'], old['bitmap'], old['width'], old['height']):
                raise ValueError('special RD source mismatch')
            header = parse_rd_header(block)
            primary = peer = None
            try:
                decode_rd_block(block, authoritative_block_size=size)
            except RDDecodeError as exc:
                primary = str(exc)
            try:
                independent_rd(block)
            except ValueError as exc:
                peer = str(exc)
            if primary is None and peer is None:
                raise ValueError('previous rejection not reproduced; requires separate review')
            result[key] = {'bitmap': bmp, 'rd_sha256': old['rd_sha256'],
                           'adrn_sha256': old['adrn_sha256'], 'block_bytes': size,
                           'header': header, 'primary_rejection': primary,
                           'independent_rejection': peer}
    return result


def verify(receipt, plan, prior, reasons):
    if (receipt['scope'], receipt['prior_receipt_sha256'], receipt['selection_reasons']) != (
            SCOPE, PRIOR_SHA256, reasons):
        raise ValueError('PET13 provenance drift')
    result = receipt['observations']
    summary = base.verify(result, plan)
    for i, observation in result['observed_blocks'].items():
        if i in prior['observed_blocks'] and observation != prior['observed_blocks'][i]:
            raise ValueError('previous original pixel observation changed')
    bad = {i: o for i, o in prior['observed_blocks'].items()
           if o['status'] != 'DUAL_DECODED_INDEX_PIXELS'}
    diagnostic = receipt['prior_special_blocks']
    if set(diagnostic) != set(bad):
        raise ValueError('special RD diagnostic coverage')
    for i, row in diagnostic.items():
        if any(row[k] != bad[i][k] for k in ('bitmap', 'rd_sha256', 'adrn_sha256')):
            raise ValueError('special RD provenance')
        if not (row['primary_rejection'] or row['independent_rejection']):
            raise ValueError('unsupported success claim')
    long_complete = sum(complete(s, result) for s in plan[3]
                        if reasons[str(s['physical_group'])] == 'ORIGINAL_LONG_SEQUENCE')
    failed_complete = sum(complete(s, result) for s in plan[3]
                          if reasons[str(s['physical_group'])] != 'ORIGINAL_LONG_SEQUENCE')
    return {**summary, 'long_group_complete': long_complete,
            'previous_incomplete_group_now_has_complete_sample': failed_complete,
            'cumulative_named_physical_groups_with_complete_sample': 498 + long_complete + failed_complete,
            'prior_special_blocks_diagnosed': len(diagnostic)}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-dir', type=Path)
    p.add_argument('--receipt', type=Path, default=TARGET)
    p.add_argument('--plan-only', action='store_true')
    args = p.parse_args()
    plan, prior, reasons = build_plan()
    if args.plan_only:
        print(json.dumps({'groups': len(plan[3]), 'reasons': reasons,
                          'positions': sum(len(s['frames']) for s in plan[3])}, sort_keys=True))
        return
    if args.source_dir:
        receipt = {'scope': SCOPE, 'prior_receipt_sha256': PRIOR_SHA256,
                   'selection_reasons': reasons,
                   'observations': base.inspect(args.source_dir, plan),
                   'prior_special_blocks': diagnose(args.source_dir, prior)}
    else:
        receipt = json.loads(gzip.decompress(args.receipt.read_bytes()))
    print(json.dumps(verify(receipt, plan, prior, reasons), sort_keys=True))
    if args.source_dir:
        args.receipt.write_bytes(gzip.compress(
            (json.dumps(receipt, sort_keys=True, separators=(',', ':')) + '\n').encode(), mtime=0))


if __name__ == '__main__':
    main()
