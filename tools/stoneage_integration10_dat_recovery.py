"""Recover twelve previously unread DAT members; privately observe seven source checkpoints.

No original assets are published. Scene rendering reuses the MAP06/SCENE21
research convention and does not certify native movement, palette or deployment.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import zipfile
import zlib

from tools.stoneage_native_album_source_r36 import isolated_rar

ROOT = Path(__file__).resolve().parents[1]
REC = ROOT / 'research/recovered'
REPORT = REC / 'STONEAGE-INTEGRATION10-TWELVE-RECOVERED-DAT-SEVEN-CHECKPOINT-SCENES-R1.json'
RAR_SHA = 'd71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5'
FLOORS = (100, 119, 200, 300, 400, 500, 1100, 1300, 3000, 3400, 6000, 10920)
INPUTS = {
    'map01': ('STONEAGE-MAP-SCENE-MODULE-01-ORIGINAL-SOURCE-MANIFEST-R1.json', '03675ee98d391f9ef0246315b2426f2a8b721fd3'),
    'i07': ('STONEAGE-INTEGRATION07-FOURTEEN-UNMATCHED-DAT-QUALIFICATION-R1.json', 'd756b20c7ee1fe6d10ad2c6800739108daab0520'),
    'q25': ('STONEAGE-QUEST25-FOUR-ISLAND-TOUR-ROUTES-SOURCE-R1.json', 'a52b4e5519912ac7e46e1f892cc01515861cf2e8'),
}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def sources():
    result = {}
    for key, (name, pin) in INPUTS.items():
        raw = (REC / name).read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        if actual != pin:
            raise ValueError('source blob changed: ' + name)
        result[key] = json.loads(raw)
    return result


def dat_planes(raw):
    if len(raw) < 8:
        raise ValueError('truncated DAT header')
    w, h = struct.unpack_from('<II', raw)
    if not (0 < w <= 4096 and 0 < h <= 4096) or len(raw) != 8 + 6*w*h:
        raise ValueError('DAT dimensions/three-plane extent')
    n = w*h
    return w, h, [struct.unpack_from('<' + 'H'*n, raw, 8 + 2*n*i) for i in range(3)]


def checkpoints(q25):
    return [(r['label'], c['number'], c['source']) for r in q25['routes']
            if r['label'] in ('C', 'D') for c in r['checkpoints']
            if c['source']['floor'] in (100, 1100, 1300)]


def acquire(rar, unar, work):
    import rarfile
    if rar.stat().st_size != 361255180 or sha(rar.read_bytes()) != RAR_SHA:
        raise ValueError('original RAR identity')
    src = sources()
    expected = {r['floor_id']: r for r in src['i07']['floors'] if r['floor_id'] in FLOORS}
    work.mkdir(parents=True, exist_ok=False)
    maps, rows = {}, []
    with rarfile.RarFile(rar) as archive, rar.open('rb') as stream:
        entries = archive.infolist()
        if len(entries) != 7952:
            raise ValueError('original archive inventory')
        for entry in entries:
            path = entry.filename.replace('\\', '/')
            leaf = path.rsplit('/', 1)[-1]
            if '/stoneage2.5/map/' not in path or not leaf.lower().endswith('.dat') or not leaf[:-4].isdigit():
                continue
            floor = int(leaf[:-4])
            if floor not in expected:
                continue
            if floor in maps:
                raise ValueError('duplicate selected original floor')
            old = expected[floor]['source_DAT_original_read_errors']
            if len(old) != 1 or (old[0]['original_filename'], old[0]['expected_member_bytes']) != (leaf, entry.file_size):
                raise ValueError('old read-error member mismatch')
            stream.seek(entry.header_offset)
            header = stream.read(entry.data_offset-entry.header_offset)
            stream.seek(entry.data_offset)
            packed = stream.read(entry.compress_size)
            if int.from_bytes(header[:2], 'little') != zlib.crc32(header[2:]) & 0xffff:
                raise ValueError('original RAR file-header CRC')
            carrier = work / (str(floor) + '.rar')
            carrier.write_bytes(isolated_rar(header, packed, entry.flags))
            dest = work / ('extract-' + str(floor))
            proc = subprocess.run([str(unar), '-f', '-D', '-o', str(dest), str(carrier)], capture_output=True, timeout=60)
            files = [p for p in dest.rglob('*') if p.is_file() and p.as_posix().endswith(path)]
            if proc.returncode != 0 or len(files) != 1:
                raise ValueError('unar original member failed: ' + leaf)
            raw = files[0].read_bytes()
            if len(raw) != entry.file_size or zlib.crc32(raw) & 0xffffffff != entry.CRC:
                raise ValueError('original full size/CRC mismatch: ' + leaf)
            w, h, planes = dat_planes(raw)
            n = w*h
            rows.append(dict(floor=floor, original_path=path, bytes=len(raw), crc32=f'{entry.CRC:08x}',
                sha256=sha(raw), width=w, height=h, header_offset=entry.header_offset,
                packed_offset=entry.data_offset, packed_bytes=entry.compress_size,
                original_flags=entry.flags, original_header_sha256=sha(header), packed_sha256=sha(packed),
                unar_exit=proc.returncode, old_read_error=old[0],
                planes=[dict(sha256=sha(raw[8+2*n*i:8+2*n*(i+1)]), nonzero=sum(v != 0 for v in p),
                             distinct_values=len(set(p))) for i, p in enumerate(planes)]))
            maps[floor] = raw
    if set(maps) != set(FLOORS):
        raise ValueError('incomplete selected recovery')
    return maps, sorted(rows, key=lambda r: r['floor'])


def observe(maps, tiles, target):
    from PIL import Image, ImageDraw
    import io
    from tools.stoneage_map06_two_original_scenes import source_images, scene_frames
    data = sources()
    selected, wanted = [], set()
    for route, number, source in checkpoints(data['q25']):
        floor = source['floor']
        w, h, planes = dat_planes(maps[floor])
        x, y, x2, y2 = source['borncorner']
        if (x, y) != (x2, y2) or not (5 <= x < w-5 and 5 <= y < h-5):
            raise ValueError('qualified 11 by 11 source checkpoint window')
        order = sorted(((xx, yy) for yy in range(y-5, y+6) for xx in range(x-5, x+6)), key=lambda p: (p[0]-p[1], -p[0]))
        draw = [dict(layer=label, xy=[xx, yy], image_key=planes[i][yy*w+xx],
                     anchor=[(xx-x+yy-y+10)*32, (yy-y-xx+x)*24])
                for i, label in ((0, 'tile'), (1, 'parts')) for xx, yy in order if planes[i][yy*w+xx] > 99]
        wanted.update(p['image_key'] for p in draw)
        selected.append((route, number, source, w, h, planes, draw))
    images, records, resources = source_images(tiles, wanted)
    windows, thumbs = [], []
    with zipfile.ZipFile(target, 'x', zipfile.ZIP_DEFLATED) as z:
        for floor, raw in sorted(maps.items()):
            z.writestr(f'source/{floor}.dat', raw)
        for route, number, source, w, h, planes, draw in selected:
            x, y = source['borncorner'][:2]
            info = {'width': 11, 'height': 11}
            frame, pngs = scene_frames(info, draw, images, records)
            label = f'{route}{number:02d}-floor{source["floor"]}'
            row = dict(label=label, route=route, checkpoint=number, floor=source['floor'], xy=[x, y],
                source_block_sha256=source['block_sha256'], window=[x-5, y-5, x+5, y+5],
                checkpoint_three_u16=[p[y*w+x] for p in planes], draw_positions=len(draw),
                distinct_image_aliases=len({p['image_key'] for p in draw}), missing_MAP04_pixel_aliases=[], **frame)
            windows.append(row)
            for mode, png in pngs.items():
                z.writestr(f'{label}-{mode}.png', png)
            im = Image.open(io.BytesIO(pngs['combined'])).convert('RGB')
            im.thumbnail((480, 400))
            thumb = Image.new('RGB', (500, 440), '#11232a')
            thumb.paste(im, ((500-im.width)//2, 30))
            ImageDraw.Draw(thumb).text((10, 8), label + ' | source candidate', fill='white')
            thumbs.append(thumb)
        with zipfile.ZipFile(tiles) as original:
            for key in sorted(wanted):
                z.writestr(f'tiles/{key}.png', original.read(f'original-TW1-Palet1-candidate/alias-{key:05d}.png'))
        z.writestr('private-observation.json', json.dumps(dict(windows=windows, resources=resources), sort_keys=True))
        options = ''.join(f'<option>{r["label"]}-{mode}</option>' for r in windows for mode in ('combined', 'plane0', 'plane1'))
        z.writestr('INTEGRATION10.html', '''<!doctype html><meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src 'self'; script-src 'unsafe-inline'; style-src 'unsafe-inline'"><title>原环岛检查站来源场景</title><style>body{background:#11232a;color:#eee;font:16px system-ui;margin:24px}img{max-width:100%;image-rendering:pixelated}</style><h1>七处原检查站场景候选</h1><p>mixed25 原DAT与TW1原图块。现代拼接、配色、层序未认证原客户端；无NPC图、原生路线或任务运行证明。解压全部文件后使用。</p><select id="v">'''+options+'''</select><p id="l"></p><img id="p" alt="来源场景候选"><script>const v=document.getElementById('v');function show(){document.getElementById('p').src=v.value+'.png';document.getElementById('l').textContent=v.value}v.onchange=show;show()</script>''')
    contact = Image.new('RGB', (1500, 1320), '#11232a')
    for i, im in enumerate(thumbs):
        contact.paste(im, ((i % 3)*500, (i//3)*440))
    contact.save(target.with_suffix('.jpg'), quality=90)
    with zipfile.ZipFile(target) as z:
        if z.testzip() is not None:
            raise ValueError('private output CRC')
        count = len(z.namelist())
    return windows, resources, dict(bytes=target.stat().st_size, sha256=sha(target.read_bytes()), members=count)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for key in ('rar', 'unar', 'work', 'tiles', 'private_zip'):
        p.add_argument('--' + key.replace('_', '-'), type=Path, required=True)
    a = p.parse_args()
    if ROOT in a.work.resolve().parents or ROOT in a.private_zip.resolve().parents:
        raise ValueError('original assets must stay outside Git')
    maps, rows = acquire(a.rar, a.unar, a.work)
    windows, resources, private = observe(maps, a.tiles, a.private_zip)
    report = dict(schema='stoneage.integration10.original_DAT_recovery_seven_source_windows.r1', date='2026-11-09',
        initial_remote_head='95b8010f2fabf200229826e2ebbaf24e4182fa85', initial_remote_tree='ee16f47db195ffd96aad30cd96140233485815fa',
        preserved_CURRENT_blob='c89e0e33537990aa2132b47c40fef49a985a935c',
        source_scope='PRESERVED_COMMUNITY_MIXED25_DAT_WITH_SEPARATE_TW10_RD_CANDIDATES_NOT_OFFICIAL_SAME_DEPLOYMENT',
        original_RAR_bytes=361255180, original_RAR_sha256=RAR_SHA, source_ci_run_id=None,
        extractor='unar v1.10.1; isolated unchanged original RAR4 header and packed member; full member CRC verified',
        source_pins={k: dict(path='research/recovered/'+v[0], git_blob=v[1]) for k, v in INPUTS.items()},
        material_impact=dict(recovered_floor_count=12, recovered_bytes=sum(r['bytes'] for r in rows),
            recovered_cells=sum(r['width']*r['height'] for r in rows),
            QUEST05_source_CREATE_refs_newly_joinable=67, still_no_selected_DAT_floor=830,
            still_no_selected_DAT_CREATE_refs=2, C_D_prior_DAT_error_checkpoint_positions=7),
        recovered_DAT=rows, source_windows=windows, source_pixel_resources=resources, private_archive=private,
        boundaries={k: False for k in ('old_failed_attempts_rewritten_as_success', 'all_63_MAP01_errors_resolved',
            'new_original_pixel_blocks_decoded', 'original_client_executed', 'native_route_reachability_verified',
            'native_NPC_spawn_verified', 'native_quest_rewards_verified', 'official_same_deployment_verified',
            'native_palette_layer_order_verified', 'raw_original_assets_in_public_git')},
        stage_A='7_PARTIAL_2_OPEN', stage_B='GATED', wiki='GATED', R79='PAUSED_NON_BLOCKING', overall_percent=None,
        next='USE_NEW_DAT_FOR_SOURCE_BOUNDED_CONTENT_JOINS; QUALIFY_REMAINING_PIXEL_GAPS_WITH_EXACT_SOURCE_BYTES')
    REPORT.write_text(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2)+'\n')
    print(json.dumps(dict(recovered_DAT=len(rows), windows=len(windows), pixel_resources=len(resources), private=private)))


if __name__ == '__main__':
    main()
