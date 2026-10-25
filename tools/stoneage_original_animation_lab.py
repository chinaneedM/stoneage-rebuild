"""Source-qualified TW1 SPR timelines and PRIVATE grayscale animation previews.

No historical FPS, palette, transparency, action names or entity identity is
inferred. Metadata is sufficient for a numeric timeline; export additionally
requires four authenticated original files. No original payload is in Git.
"""
from __future__ import annotations

import argparse
import base64
import csv
import gzip
import hashlib
import io
import json
from pathlib import Path
import struct

from tools.stoneage_original_observation_lab import (
    ROOT, PINNED, MODE, SOURCE, check_original, get_record, gray_png,
)
from tools.stoneage_rd_codec import decode_rd_block
from tools.stoneage_tw10_animation_selector_r101 import ticks, first_match

META = ROOT / 'research/recovered/tw10-resource-metadata'
PINS = {
    'SPR-GROUP-R1.tsv.gz': '4db7809de4197eb90cca6dc04bda8550025e022c8232e2ebb902db0e9faf0175',
    'SPR-ANIMATION-R1.tsv.gz': '25f8039e6c6ca47d94289b269d5ff74a67fde999c6b6d4dbb08af297ddcaa567',
    'SPR-FRAME-R1.tsv.gz': '2bbfb2db4a866445085d98934fd475cbd72e034fe1155b2e17ae802ffdc5fe80',
    'ADRN-R1.tsv.gz': 'c8669789de1cc6e3575c2412ed86354a49c2b3e90cd2854c1e7b2fc71b0fe9ea',
}
ORIGINALS = dict(PINNED, **{
    'spr_1.bin': (2889630, '53d5b2d40453a30fd1569637ebf0db7b3010542b00970ec83af0295a3b3ae31a'),
    'spradrn_1.bin': (5568, '275b64ff55667aec633a7e82e09d65c84141380521f0f2e64c9a28e0d3aa6c25'),
})
CASES = ((100000, 0, 0), (100000, 0, 6), (100000, 2, 2))
REPORT = ROOT / 'research/recovered/STONEAGE-TW10-ANIMATION-OBSERVATION-P2A-R1.json'
TEMPLATE = ROOT / 'tools/original-animation-viewer.html'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def rows(name, metadata=META):
    raw = (metadata / name).read_bytes()
    require(digest(raw) == PINS[name], 'source metadata SHA mismatch: ' + name)
    with gzip.open(io.BytesIO(raw), 'rt', encoding='utf-8', newline='') as f:
        yield from csv.DictReader(f, delimiter='\t')


def numeric(row):
    return {k: int(v) if not k.endswith('sha256') else v for k, v in row.items()}


def reconstruct_group(group, animations, frames):
    """Independent re-encoding of ALL group metadata against the old raw SHA."""
    require(len(animations) == group['anim_count'], 'group animation count mismatch')
    output = bytearray()
    cursor = group['offset']
    for ai, animation in enumerate(animations):
        require(animation['anim_index'] == ai and animation['offset'] == cursor,
                'animation order/offset mismatch')
        require((animation['group_index'], animation['spr_no']) == (group['index'], group['spr_no']),
                'animation namespace mismatch')
        ff = frames.get(ai, [])
        require(len(ff) == animation['frame_count'] and 0 < len(ff) <= 112,
                'frame count outside finite original contract')
        output.extend(struct.pack('<HHII', animation['direction'], animation['anim_no'],
                                  animation['duration'], len(ff)))
        cursor += 12
        for fi, frame in enumerate(ff):
            require((frame['group_index'], frame['spr_no'], frame['anim_index'],
                     frame['frame_index'], frame['offset']) ==
                    (group['index'], group['spr_no'], ai, fi, cursor), 'frame order/offset mismatch')
            require(frame['sentinel'] == int(frame['bmp_no'] == 0xffffffff), 'sentinel metadata mismatch')
            output.extend(struct.pack('<IhhH', frame['bmp_no'], frame['pos_x'], frame['pos_y'], frame['sound_no']))
            cursor += 10
        require(cursor == animation['end_offset'], 'animation end mismatch')
    require(cursor == group['end_offset'] == group['next_offset'], 'group extent mismatch')
    require(digest(output) == group['segment_sha256'], 're-encoded original SPR group SHA mismatch')
    return bytes(output)


def timeline(spr_no, direction, action, metadata=META):
    require(type(spr_no) is int and type(direction) is int and type(action) is int,
            'integer selectors required')
    require(0 <= direction <= 65535 and 0 <= action <= 65535, 'selector outside uint16')
    gg = [numeric(r) for r in rows('SPR-GROUP-R1.tsv.gz', metadata) if int(r['spr_no']) == spr_no]
    require(len(gg) == 1, 'original SPR group missing or ambiguous')
    group = gg[0]
    aa = [numeric(r) for r in rows('SPR-ANIMATION-R1.tsv.gz', metadata) if int(r['group_index']) == group['index']]
    ff = {}
    for r in rows('SPR-FRAME-R1.tsv.gz', metadata):
        if int(r['group_index']) == group['index']:
            frame = numeric(r)
            ff.setdefault(frame['anim_index'], []).append(frame)
    reconstruct_group(group, aa, ff)
    selected = first_match([(a['direction'], a['anim_no']) for a in aa], direction, action)
    require(selected is not None, 'empty animation group')
    animation = aa[selected]
    frames = ff[selected]
    needed = {f['bmp_no'] for f in frames}
    require(0xffffffff not in needed, 'sentinel frame requires separate source semantics; preview refused')
    bitmaps = {}
    for r in rows('ADRN-R1.tsv.gz', metadata):
        if int(r['bitmapno']) in needed:
            b = numeric(r)
            require(b['bitmapno'] not in bitmaps, 'ambiguous original bitmap identity')
            require(b['width'] > 0 and b['height'] > 0 and b['width'] * b['height'] <= 8_000_000,
                    'special or oversized bitmap cannot be previewed')
            bitmaps[b['bitmapno']] = b
    require(set(bitmaps) == needed, 'SPR frame has no same-source ADRN record')
    step = ticks(animation['duration'], animation['frame_count'])
    output = []
    for frame in frames:
        bitmap = bitmaps[frame['bmp_no']]
        output.append(dict(frame, bitmap=bitmap,
                           composed_x=frame['pos_x'] + bitmap['xoff'],
                           composed_y=frame['pos_y'] + bitmap['yoff'],
                           start_tick=frame['frame_index'] * step,
                           hold_ticks=step))
    return {
        'schema': 'stoneage.original_animation_timeline.p2a_v1', 'sample': SOURCE,
        'source_metadata_sha256': PINS,
        'group': group, 'requested': {'spr_no': spr_no, 'direction': direction, 'action': action},
        'animation': animation, 'fallback_to_first':
            (animation['direction'], animation['anim_no']) != (direction, action),
        'cycle_ticks': len(frames) * step, 'distinct_bitmaps': len(needed), 'frames': output,
        'preview_mode': MODE, 'timing_mode': 'SOURCE_COUNTDOWN_TICKS_AT_USER_CHOSEN_PREVIEW_RATE',
        'source_tick_rate_hz': None, 'original_palette_verified': False,
        'original_colors_reproduced': False, 'transparency_verified': False,
        'row_orientation_verified': False, 'original_client_executed': False,
        'historical_gameplay_screenshot': False, 'sound_events_played': False,
        'action_name': None, 'entity_identity': None, 'overall_percent': None,
    }


def sample_report():
    return {'schema': 'stoneage.original_animation_observation.p2a_v1',
            'work_package': 'ORIGINAL-GAME-OBSERVATION-P2A',
            'evidence': 'ARCHIVED_SAME_SOURCE_METADATA_REENCODED_AND_JOINED_NOT_NEW_ORIGINAL_BYTES',
            'cases': [timeline(*case) for case in CASES],
            'palette_gap': '16 original SAP hashes exist; original RGB/BGR order, index placement, '
                           'reserved colors and actual scene selection remain unverified',
            'next': 'ORIGINAL-GAME-OBSERVATION-P2B-PALETTE-SOURCE'}


def preview(t, paths, expected=None, *, color_table=None):
    expected = ORIGINALS if expected is None else expected
    require(set(paths) == set(ORIGINALS), 'all four original source inputs required')
    for name, path in paths.items():
        check_original(path, expected[name])
    g = t['group']
    with paths['spradrn_1.bin'].open('rb') as f:
        f.seek(g['index'] * 12)
        raw = f.read(12)
    require(raw == struct.pack('<IIHH', g['spr_no'], g['offset'], g['anim_count'], g['reserved']),
            'actual original SPRADRN group mismatch')
    with paths['spr_1.bin'].open('rb') as f:
        f.seek(g['offset'])
        raw = f.read(g['end_offset'] - g['offset'])
    require(digest(raw) == g['segment_sha256'], 'actual original SPR group mismatch')
    images, witnesses = {}, []
    with paths['real_1.bin'].open('rb') as real:
        for frame in t['frames']:
            b = frame['bitmap']
            key = str(b['bitmapno'])
            if key in images:
                continue
            actual = get_record(paths['adrn_1.bin'], index=b['index'])
            require(all(actual[k] == b[k] for k in ('index','bitmapno','adder','size','xoff','yoff','width','height')),
                    'actual original ADRN geometry mismatch')
            require(b['adder'] + b['size'] <= paths['real_1.bin'].stat().st_size, 'RD extent exceeds REAL')
            real.seek(b['adder']); block = real.read(b['size'])
            require(digest(block) == b['rd_block_sha256'], 'actual original RD block mismatch')
            header, pixels = decode_rd_block(block, authoritative_block_size=b['size'])
            require((header['width_s'],header['height_s']) == (b['width'],b['height']), 'RD geometry mismatch')
            if color_table is None:
                png = gray_png(pixels,b['width'],b['height'])
            else:
                from tools.stoneage_tw10_palette import indexed_png
                png = indexed_png(pixels,b['width'],b['height'],color_table)
            images[key] = 'data:image/png;base64,' + base64.b64encode(png).decode('ascii')
            witnesses.append({'bitmapno':b['bitmapno'], 'adrn_record_sha256':actual['source_adrn_record_sha256'],
                              'rd_block_sha256':digest(block), 'palette_index_sha256':digest(pixels),
                              ('private_grayscale_png_sha256' if color_table is None else 'private_indexed_color_png_sha256'):digest(png)})
    custody = {'schema':'stoneage.original_animation_preview_source.p2a_v1',
               'timeline': t, 'original_files': {n:{'bytes':v[0],'sha256':v[1]} for n,v in expected.items()},
               'source_status':'FOUR_ORIGINAL_FILES_AND_SELECTED_RD_PIXELS_VERIFIED',
               'bitmap_witnesses':witnesses, 'original_assets_committed':False,
               'assistant_viewed_or_heard_original':False}
    if color_table is not None:
        custody['rendered_rgb_table_sha256']=digest(color_table)
    packed = json.dumps({'timeline':t,'images':images},ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
    template = TEMPLATE.read_text(encoding='utf-8')
    require(template.count('__PACK_JSON__') == 1, 'invalid preview template')
    return template.replace('__PACK_JSON__',packed), custody


def write_private(output, html, custody):
    output = output.expanduser().resolve()
    require(output.suffix.lower() == '.html' and ROOT not in output.parents,
            'original animation output must be an external private HTML')
    sidecar = output.with_suffix('.json')
    require(output.parent.is_dir() and not output.exists() and not sidecar.exists(),
            'private directory must exist and outputs must not exist')
    with output.open('x',encoding='utf-8') as f:
        f.write(html)
    try:
        with sidecar.open('x',encoding='utf-8') as f:
            json.dump(custody,f,ensure_ascii=False,indent=2);f.write('\n')
    except Exception:
        output.unlink()
        raise


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check-report',action='store_true')
    ap.add_argument('--write-report',type=Path)
    ap.add_argument('--spr-no',type=int,default=100000)
    ap.add_argument('--direction',type=int,default=0)
    ap.add_argument('--action',type=int,default=6)
    ap.add_argument('--original-dir',type=Path)
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    require(sum((args.check_report,args.write_report is not None,args.output is not None)) == 1,
            'choose exactly one report check/write or private output')
    if args.check_report or args.write_report:
        report=sample_report()
        if args.check_report:
            require(json.loads(REPORT.read_text()) == report,'permanent animation report replay differs')
        else:
            args.write_report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print('TW1_ANIMATION_TIMELINE_EXACT_REPLAY=PASS; ORIGINAL_COLOR_AND_GAME_RUNTIME=OPEN')
    else:
        require(args.original_dir is not None, '--original-dir required for actual preview')
        t=timeline(args.spr_no,args.direction,args.action)
        paths={n:args.original_dir/n for n in ORIGINALS}
        html,custody=preview(t,paths)
        write_private(args.output,html,custody)
        print('PRIVATE_ORIGINAL_GRAYSCALE_ANIMATION_WRITTEN; HISTORICAL_FPS_AND_COLOR=OPEN')


if __name__ == '__main__':
    main()
