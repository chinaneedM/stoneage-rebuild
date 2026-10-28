"""Private same-carrier SPR/RD observer. No original game process or server runs.

Only metadata and hashes may be published. Original sources/PNGs/HTML must stay
outside this repository. Animation placement/timing is explicitly experimental.
"""
from __future__ import annotations
import argparse
import base64
import hashlib
import io
import json
from pathlib import Path
import struct
import zipfile

from tools.stoneage_rd_codec import decode_rd_block
from tools.stoneage_private_scene_graphic_join_r1 import ADRN_SIZE, ADRN_SHA, REAL_SIZE, REAL_SHA
from tools.stoneage_private_scene_palette_r3 import candidate_rgba, PALETTE1_SHA
from tools.stoneage_tw10_palette import initial_rgb

ROOT = Path(__file__).resolve().parents[1]
R6_SHA = 'e21c913af9cf80fc7d717fef67f6528f018bd8e57bb1629e1d1510ee184832f7'
PINS = {
    'adrn_15.bin': (ADRN_SIZE, ADRN_SHA),
    'real_15.bin': (REAL_SIZE, REAL_SHA),
    'spr_4.bin': (5588120, '865b58860c7fe025850bf942f6ce6a5deb4464993ceeecbc20a034c99e159749'),
    'spradrn_5.bin': (10164, '5f13c956cf013e073298ab91667d3aaa17767b26ba94d696514726950ce94de6'),
    'Palet_1.sap': (708, PALETTE1_SHA),
}
GROUPS = (100000, 100700)
ACTIONS = (2, 6)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def need(ok, message):
    if not ok:
        raise ValueError(message)

def authenticate(path, pin):
    need(path.is_file() and not path.is_symlink() and path.stat().st_size == pin[0],
         'original full-file extent mismatch: '+path.name)
    with path.open('rb') as f:
        need(hashlib.file_digest(f, 'sha256').hexdigest() == pin[1],
             'original full-file SHA mismatch: '+path.name)

def select_animations(index, spr, selected=GROUPS):
    """Retain duplicate source selector occurrences; never silently use last-wins."""
    need(len(index) % 12 == 0 and 0 < len(index) <= 120000, 'index extent')
    rows = [struct.unpack_from('<IIHH', index, p) for p in range(0, len(index), 12)]
    offsets = sorted({r[1] for r in rows})
    need(all(0 <= n < len(spr) for n in offsets), 'index source range')
    ends = {p: offsets[i+1] if i+1 < len(offsets) else len(spr) for i,p in enumerate(offsets)}
    groups = []
    for key in selected:
        matches = [(i,r) for i,r in enumerate(rows) if r[0] == key]
        need(len(matches) == 1, 'missing/ambiguous original SPR group')
        gi, (no, start, count, reserved) = matches[0]
        need(0 < count <= 128, 'group animation bound')
        cursor = start
        animations = []
        for ai in range(count):
            need(cursor+12 <= ends[start], 'short animation header')
            header_offset = cursor
            direction, action, duration, n = struct.unpack_from('<HHII', spr, cursor)
            cursor += 12
            need(0 < n <= 112 and cursor+n*10 <= ends[start], 'frame source range')
            frames = [list(struct.unpack_from('<IhhH', spr, cursor+j*10)) for j in range(n)]
            cursor += n*10
            if direction in range(8) and action in ACTIONS:
                need(all(f[0] != 0xffffffff for f in frames), 'sentinel needs separate semantics')
                animations.append({'source_animation_index': ai, 'header_offset': header_offset,
                    'direction': direction, 'action': action, 'duration_word': duration,
                    'frames': frames, 'end_offset': cursor,
                    'source_animation_span_sha256': sha(spr[header_offset:cursor])})
        need(cursor == ends[start], 'whole original group boundary mismatch')
        need(len(animations) == 16 and
             {(a['direction'], a['action']) for a in animations} ==
             {(d,a) for d in range(8) for a in ACTIONS}, 'missing/ambiguous selected animation')
        groups.append({'spr_no': no, 'source_group_index': gi, 'offset': start,
            'end_offset': cursor, 'source_animation_count': count, 'reserved_word': reserved,
            'index_record_sha256': sha(index[gi*12:gi*12+12]),
            'whole_group_segment_sha256': sha(spr[start:cursor]), 'animations': animations})
    return groups

def resolve_bitmaps(adrn, needed, real_size):
    need(len(adrn) % 80 == 0 and 0 < len(needed) <= 256, 'bounded bitmap source set')
    matches = {n: [] for n in needed}
    for p in range(0, len(adrn), 80):
        no = struct.unpack_from('<I', adrn, p)[0]
        if no in matches:
            values = struct.unpack_from('<7i', adrn, p)
            matches[no].append((p//80, values, sha(adrn[p:p+80])))
    need(all(len(v) == 1 for v in matches.values()), 'missing/ambiguous physical bitmap')
    out = {}
    for no, values in matches.items():
        idx, (number, offset, size, x, y, w, h), digest = values[0]
        need(number == no and 16 <= size <= 1000000 and 0 <= offset <= real_size-size,
             'original RD range')
        need(0 < w <= 1024 and 0 < h <= 1024 and w*h <= 1000000, 'original pixel budget')
        out[no] = {'bitmapno': no, 'source_adrn_index': idx, 'record_sha256': digest,
            'offset': offset, 'size': size, 'xoff': x, 'yoff': y, 'width': w, 'height': h}
    return out

def export(source, room_file, target):
    from PIL import Image
    target = target.resolve()
    need(target != ROOT and ROOT not in target.parents and not target.exists(),
         'new private output outside public Git required')
    room_bytes = room_file.read_bytes()
    need(sha(room_bytes) == R6_SHA, 'immutable private R6 identity')
    marker = '<script id="evidence" type="application/json">'
    room = json.loads(room_bytes.decode().split(marker)[1].split('</script>')[0])
    need(len(room['placements']) == 30 and len(room['sprites']) == 10 and
         room['source_sap_sha256'] == PALETTE1_SHA, 'same-carrier room/palette identity')
    for key, encoded in room['sprites'].items():
        png = base64.b64decode(encoded, validate=True)
        need(sha(png) == room['sprite_sha256'][key], 'immutable room PNG identity')
        with Image.open(io.BytesIO(png)) as im:
            im.load()
    paths = {name:source/name for name in PINS}
    for name,pin in PINS.items():
        authenticate(paths[name], pin)
    groups = select_animations(paths['spradrn_5.bin'].read_bytes(), paths['spr_4.bin'].read_bytes())
    needed = {f[0] for g in groups for a in g['animations'] for f in a['frames']}
    bitmaps = resolve_bitmaps(paths['adrn_15.bin'].read_bytes(), needed, REAL_SIZE)
    rgb = initial_rgb(paths['Palet_1.sap'].read_bytes())
    images = {}
    private_rd = {}
    with paths['real_15.bin'].open('rb') as real:
        for no,row in bitmaps.items():
            real.seek(row['offset'])
            rd = real.read(row['size'])
            need(len(rd) == row['size'], 'short private original RD read')
            private_rd[f'{no}.rd'] = rd
            header, pixels = decode_rd_block(rd, authoritative_block_size=row['size'])
            need((header['width_s'],header['height_s']) == (row['width'],row['height']),
                 'same-source ADRN/RD geometry mismatch')
            rgba = candidate_rgba(pixels,row['width'],row['height'],rgb)
            im = Image.frombytes('RGBA',(row['width'],row['height']),rgba)
            buf=io.BytesIO();im.save(buf,format='PNG');png=buf.getvalue()
            images[str(no)] = base64.b64encode(png).decode()
            row.update(RD_sha256=sha(rd), index_pixels_sha256=sha(pixels),
                       candidate_RGBA_sha256=sha(rgba), PNG_sha256=sha(png), RD_flag=header['flag'])
    report = {'schema':'stoneage.same_carrier_actor_observation.r7',
        'source_scope':'PRESERVED_MIXED25_NOT_OFFICIAL_TW1',
        'source_files':{k:{'bytes':v[0],'sha256':v[1]} for k,v in PINS.items()},
        'room_r6_sha256': R6_SHA, 'groups':groups, 'bitmaps':list(bitmaps.values()),
        'selected_animation_count':sum(len(g['animations']) for g in groups),
        'frame_occurrences':sum(len(a['frames']) for g in groups for a in g['animations']),
        'distinct_source_bitmaps':len(bitmaps), 'original_world_entered':False,
        'original_client_launched_in_this_observation':False, 'official_build_authenticated':False,
        'entity_names_verified':False, 'live_palette_verified':False, 'native_actor_occlusion_verified':False,
        'native_fps_verified':False, 'audio_events_played':False,
        'actor_placement':'MODERN_MANUAL_OVERLAY_AFTER_ALL_MAP_PARTS',
        'preview_frame_ms':180, 'source_duration_word_is_not_milliseconds':True,
        'stage_a':'7_PARTIAL_2_OPEN','stage_b':'GATED','r79':'PAUSED_NON_BLOCKING',
        'overall_completion_percent':None}
    pack={'room':room,'actors':report,'actor_images':images}
    template=(ROOT/'tools/scene-room-actor-viewer-r7.html').read_text()
    encoded=json.dumps(pack,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
    html=template.replace('"PRIVATE_PACK_PLACEHOLDER"',encoded)
    need(html != template, 'private template marker missing')
    target.mkdir(mode=0o700,parents=True)
    with zipfile.ZipFile(target/'private-source-rd-subset.zip','w',zipfile.ZIP_DEFLATED) as archive:
        for name,raw in private_rd.items():
            archive.writestr(name,raw)
    (target/'stoneage-room-r7-actor-observer.html').write_text(html)
    (target/'source-derived-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-dir',type=Path,required=True)
    p.add_argument('--room-r6',type=Path,required=True)
    p.add_argument('--output-dir',type=Path,required=True)
    args=p.parse_args()
    r=export(args.source_dir,args.room_r6,args.output_dir)
    print(json.dumps({k:r[k] for k in ('schema','selected_animation_count','frame_occurrences',
                                      'distinct_source_bitmaps','original_world_entered')}))

if __name__=='__main__':
    main()
