"""Private large-map observation using existing MAP06 source/pixel/render checks."""
import argparse
import io
import json
from pathlib import Path
import zipfile
import zlib

from tools.stoneage_map06_two_original_scenes import (
    META, placements, source_images, scene_frames, sha, need,
)
from tools.stoneage_map08_private_dat_batch import pinned

FLOORS = (1200, 1400, 3100, 3300, 5100, 5500)
REPORT = META.parent / 'STONEAGE-MAP08-SIX-LARGE-SOURCE-SCENES-R1.json'


def export(dat_archive, tiles, target, source_report):
    from PIL import Image, ImageDraw
    need(not target.exists() and META.parents[2] not in target.resolve().parents,
         'new private output must be outside Git')
    pins = pinned()
    maps, wanted = {}, set()
    with zipfile.ZipFile(dat_archive) as z:
        need(z.testzip() is None and set(z.namelist()) == set(pins), '955 DAT archive CRC/members')
        for name, pin in pins.items():
            raw = z.read(name)
            need((len(raw), sha(raw)) == pin, 'DAT source identity: ' + name)
            if int(name[:-4]) in FLOORS:
                info, selected = placements(raw)
                maps[name[:-4]] = (raw, info, selected)
                wanted.update(p['image_key'] for p in selected)
    images, records, resources = source_images(tiles, wanted)
    report = {
        'schema': 'stoneage.map08.six_large_source_scenes.r1',
        'source_scope': 'MIXED25_ORIGINAL_DAT_AND_TW10_ORIGINAL_RD_SEPARATE_SOURCES',
        'all_955_original_DAT_archive': {'bytes': dat_archive.stat().st_size,
            'sha256': sha(dat_archive.read_bytes()), 'members': len(pins),
            'uncompressed_bytes': sum(p[0] for p in pins.values())},
        'source_run_id': 42361185994,
        'source_head': '7c7fbeddf26f4538aea350a7678a2545dd3b24c9',
        'source_artifact_id': 13569996494,
        'source_artifact_zip_sha256': '0e945d09deecac0b3459a674edfb34c3c43e2144fd0700de7cdc521380f3aa09',
        'source_report_sha256': sha(source_report.read_bytes()),
        'resources': resources, 'maps': {},
        'boundaries': {k: False for k in ('original_client_executed',
            'native_scene_rendering_verified', 'official_same_deployment_verified',
            'native_layer_order_verified', 'native_palette_verified',
            'native_collision_verified', 'raw_originals_in_public_git')},
    }
    private, thumbs = {}, []
    with zipfile.ZipFile(target, 'x', zipfile.ZIP_DEFLATED) as out:
        out.write(dat_archive, 'source-all-955-original-DAT.zip')
        out.write(source_report, 'source-acquisition-report.json')
        for floor, (raw, info, selected) in maps.items():
            result, pngs = scene_frames(info, selected, images, records)
            report['maps'][floor] = {
                'source_bytes': len(raw), 'source_sha256': sha(raw),
                'source_crc32': f'{zlib.crc32(raw) & 0xffffffff:08x}',
                'structure': info,
                'distinct_draw_candidate_aliases': len({p['image_key'] for p in selected}),
                **result,
            }
            private[floor] = {'placements': selected, **result}
            out.writestr('source/' + floor + '.dat', raw)
            for mode, png in pngs.items():
                out.writestr(f'{floor}-{mode}.png', png)
            im = Image.open(io.BytesIO(pngs['combined'])).convert('RGB')
            im.thumbnail((720, 540))
            thumb = Image.new('RGB', (740, 580), '#11232a')
            thumb.paste(im, ((740-im.width)//2, 30))
            ImageDraw.Draw(thumb).text((12, 8), f"DAT {floor} | {info['width']} x {info['height']} | source candidate", fill='white')
            thumbs.append(thumb)
            print(json.dumps({'floor': floor, 'canvas': result['canvas_size'],
                              'placements': len(selected)}), flush=True)
        with zipfile.ZipFile(tiles) as original:
            for key in images:
                png = original.read(f'original-TW1-Palet1-candidate/alias-{key:05d}.png')
                need(sha(png) == resources[str(key)]['candidate_PNG_sha256'], 'original PNG identity')
                out.writestr(f'tiles/{key}.png', png)
        out.writestr('private-source-placements.json', json.dumps(private, sort_keys=True))
        out.writestr('scene-source-receipt.json', json.dumps(report, sort_keys=True))
        options = ''.join(f'<option>{f}-{m}</option>' for f in maps for m in ('combined','plane0','plane1'))
        html = '''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src 'self' data:; script-src 'unsafe-inline'; style-src 'unsafe-inline'"><title>MAP08 原地图来源场景</title><style>body{background:#11232a;color:#eee;font:16px system-ui;margin:24px}img{max-width:100%;image-rendering:pixelated}select{font:inherit;padding:8px}</style><h1>MAP08 六张原来源场景</h1><p>混合2.5原DAT + 台湾1.0原RD像素候选。现代分层、次序、调色板、透明语义尚未认证原客户端；不是游戏截图、官方同服或可玩世界。完整955份原DAT保存在附包，可供后续复用。解压全部文件后打开本页；图像按需读取。</p><select id="view">'''+options+'''</select><p id="label"></p><img id="scene" alt="来源限定候选场景"><script>const q=document.getElementById('view');function show(){document.getElementById('scene').src=q.value+'.png';document.getElementById('label').textContent=q.value}q.onchange=show;show();</script></html>'''
        out.writestr('MAP08.html', html)
        out.write(Path(__file__).with_name('stoneage_map08_independent_replay.py'), 'replay-from-private.py')
    contact = Image.new('RGB', (1480, 1740), '#11232a')
    for i, thumb in enumerate(thumbs): contact.paste(thumb, ((i%2)*740, (i//2)*580))
    contact.save(target.with_suffix('.jpg'), quality=90)
    with zipfile.ZipFile(target) as z:
        need(z.testzip() is None, 'private output CRC')
        report['private_zip_members'] = len(z.namelist())
    report['private_zip_bytes'] = target.stat().st_size
    report['private_zip_sha256'] = sha(target.read_bytes())
    return report


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    for name in ('dat_archive', 'tiles', 'private_zip', 'source_report'): p.add_argument(name, type=Path)
    a = p.parse_args()
    r = export(a.dat_archive, a.tiles, a.private_zip, a.source_report)
    REPORT.write_text(json.dumps(r, ensure_ascii=False, sort_keys=True, indent=2)+'\n')
    print(json.dumps({'maps': len(r['maps']), 'resources': len(r['resources']),
                      'private_bytes': r['private_zip_bytes']}))
