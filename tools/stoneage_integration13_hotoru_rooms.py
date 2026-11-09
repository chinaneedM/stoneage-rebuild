"""Join five original Hotoru room sources to the already rendered MAP07 canvases."""
import argparse
from collections import Counter
import hashlib
import html
import io
import json
import re
from pathlib import Path
import zipfile
import zlib

from tools.stoneage_integration10_dat_recovery import dat_planes
from tools.stoneage_integration11_floor1300 import parse_warps
from tools.stoneage_map06_two_original_scenes import need, placements, sha
from tools.stoneage_server_static_map import parse_ls2map

ROOT = Path(__file__).resolve().parents[1]
FLOORS = range(1301, 1306)
REPORT = 'STONEAGE-INTEGRATION13-HOTORU-FIVE-ROOMS-SOURCE-R1.json'
SOURCES = {
    'char': ('STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json', 'a088b61a3212f7049e7793f587123ffb29bebad7'),
    'i11': ('STONEAGE-INTEGRATION11-FLOOR1300-SOURCE-SCENE-R1.json', '3a3d601d9c40a322871ae4996893012d2f2dd3ef'),
    'map07': ('STONEAGE-MAP07-28-ORIGINAL-DAT-SOURCE-SCENE-RECEIPT-R1.json', 'f2cba278f4b5a15e50e905a1e6591958fd09dba5'),
    'r18': ('STONEAGE-MIXED25-SERVER-FULL-SOURCE-R18.json', 'f4ac9b805724bcd847c9632cad3c35bc4309a526'),
    'map01': ('STONEAGE-MAP-SCENE-MODULE-01-ORIGINAL-SOURCE-MANIFEST-R1.json', '03675ee98d391f9ef0246315b2426f2a8b721fd3'),
}


def pinned_sources():
    data = {}
    for key, (filename, pin) in SOURCES.items():
        raw = (ROOT / 'research/recovered' / filename).read_bytes()
        need(hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest() == pin, filename)
        data[key] = json.loads(raw)
    return data


def identity(raw):
    return dict(bytes=len(raw), sha256=sha(raw), crc32=f'{zlib.crc32(raw):08x}')


def sample(geometry, point):
    width, height, planes = geometry
    x, y = point
    need(0 <= x < width and 0 <= y < height, f'DAT point outside room: {point}')
    return [p[y * width + x] for p in planes]


def config_rows(originals, sources, geometry, retained):
    from tools.stoneage_scene14_independent_replay import source_blocks

    files = {r[0]: r[1:4] for r in sources['char']['source_files']}
    inventory = {r['path']: r for r in sources['r18']['all_server_occurrences']}
    templates = {(r[0], r[1]): r for r in sources['char']['template_rows']}

    def read_npc(path):
        key = 'npc/' + path
        if key not in retained:
            raw = (originals / key).read_bytes()
            meta = identity(raw)
            need(list(meta.values()) == files[path], f'CHAR01 file {path}')
            prior = inventory[key]
            need((meta['bytes'], meta['sha256']) == (prior['size'], prior['sha256']), f'R18 file {path}')
            retained[key] = raw
        return retained[key]

    selected = [r for r in sources['char']['create_rows'] if r[5] in FLOORS]
    parsed = {}
    for row in selected:
        for path in [row[0], *(r[0] for r in row[13])]:
            if path not in parsed:
                parsed[path] = source_blocks(read_npc(path))

    rooms = {floor: [] for floor in FLOORS}
    for row in selected:
        path, ordinal, start, stop, digest, floor, graphic, corner = row[:8]
        raw = read_npc(path)
        block = parsed[path][ordinal]
        need(block['start'] == start and raw[block['end']:stop] in (b'\n', b'\r\n')
             and sha(raw[start:stop]) == digest, f'CREATE block {path}:{ordinal}')
        fields = block['fields']
        xy = list(map(int, fields[b'borncorner'].split(b',')))
        need(xy == corner and xy[:2] == xy[2:] and int(fields[b'floorid']) == floor, 'CREATE room and point')
        need(int(fields[b'graphicname']) == graphic if graphic is not None else b'graphicname' not in fields,
             'CREATE graphic field')
        enemy = fields[b'enemy'].decode('ascii').split('|')
        need(enemy[0] == row[11] and len(row[13]) == 1, 'exact CREATE template token')
        template_path, template_ordinal = row[13][0]
        template = templates[template_path, template_ordinal]
        tb = parsed[template_path][template_ordinal]
        traw = read_npc(template_path)
        span = traw[tb['start']:tb['end']]
        terminator = b'\r\n' if traw[tb['end']:].startswith(b'\r\n') else b'\n'
        need(sha(span + terminator) == template[2], 'original template block SHA')
        tf = tb['fields']
        need(tf[b'templatename'].decode('ascii') == enemy[0] == template[3], 'template name')
        function = tf.get(b'functionset', b'').decode('ascii')
        need(function == template[4], 'template function')
        parameters = []
        for p, qualification, digest_p in row[15]:
            need(qualification == 'EXACT_SAME_NPC_SUBTREE_PATH' and 'file:' + p in enemy[1:],
                 'exact CREATE parameter reference')
            need(sha(read_npc(p)) == digest_p, 'original parameter SHA')
            parameters.append(dict(path=p, sha256=digest_p))
        target = list(map(int, enemy[1:])) if function == 'Warp' else None
        literals = []
        if target is not None:
            need(len(target) == 3, 'Warp target grammar')
        else:
            literals = [value for value in enemy[1:] if not value.startswith('file:')]
            need(len(enemy) == 1 + len(parameters) + len(literals)
                 and all(re.fullmatch(r'-?\d+(?:\.\d+)?', value) for value in literals),
                 'CREATE literal or exact file argument')
        rooms[floor].append(dict(path=path, ordinal=ordinal, block_sha256=digest, xy=xy[:2],
                                graphic_alias=graphic, enemy_template=enemy[0], functionset=function or None,
                                template=[template_path, template_ordinal, template[2]], parameters=parameters,
                                target=target, argument_literals=literals, dat_u16=sample(geometry[floor], xy[:2])))
    return rooms


def export(originals, map07_zip, integration11_zip, target):
    from PIL import Image

    sources = pinned_sources()
    target = target.resolve()
    need(ROOT not in target.parents and not target.exists(), 'private output must be new and outside Git')
    parent = sources['map07']['private_deliverable']
    need((map07_zip.stat().st_size, sha(map07_zip.read_bytes())) == (parent['bytes'], parent['sha256']), 'MAP07 ZIP')
    parent11 = sources['i11']['private_archive']
    need((integration11_zip.stat().st_size, sha(integration11_zip.read_bytes()))
         == (parent11['bytes'], parent11['sha256']), 'INTEGRATION11 ZIP')
    rooms, geometry, retained, frames = {}, {}, {}, {}
    map07 = {r['floor']: r for r in sources['map07']['maps']}
    qualified_aliases = {r['alias'] for r in sources['map07']['qualified_image_source_rows']}
    with zipfile.ZipFile(map07_zip) as z, zipfile.ZipFile(integration11_zip) as iz:
        need(len(z.namelist()) == parent['members'] and z.testzip() is None
             and len(iz.namelist()) == parent11['members'] and iz.testzip() is None, 'parent ZIP CRC')
        prior_frames = json.loads(z.read('source-qualified-derived-report.json'))['maps']
        town = iz.read('source/1300.DAT')
        need(sha(town) == sources['i11']['original_DAT']['sha256'], '1300 DAT')
        geometry[1300] = dat_planes(town)
        for floor in FLOORS:
            key = str(floor)
            raw = z.read(f'sources/{key}.dat')
            prior = map07[floor]
            linked = sources['i11']['linked_DAT'][key]
            dat = identity(raw)
            need(raw == iz.read(f'source/linked-dat/{key}.dat') and dat['sha256'] == prior['source_dat_sha256']
                 and all(dat[k] == linked[k] for k in dat), 'DAT from MAP07 and INTEGRATION11')
            geometry[floor] = dat_planes(raw)
            w, h, planes = geometry[floor]
            server = (originals / 'ls2map' / key).read_bytes()
            ls = parse_ls2map(server)
            need((ls.floor_id, ls.width, ls.height) == (floor, w, h), 'embedded LS2MAP floor and size')
            name = server[8:40].split(b'\0', 1)[0]
            decoded = name.decode('cp950')
            need(decoded.encode('cp950') == name and decoded.endswith('|0'), 'original name field')
            comparison = []
            for server_plane, client_plane in zip((ls.tile_ids, ls.object_ids), planes):
                diffs = Counter((a, b) for a, b in zip(server_plane, client_plane) if a != b)
                comparison.append(dict(changed=sum(diffs.values()), differences=[[*p, n] for p, n in sorted(diffs.items())]))
            info, draw = placements(raw)
            meta = prior_frames[key]
            base = z.read(f'scenes/{key}-combined.png')
            frame = meta['frames']['combined']
            with Image.open(io.BytesIO(base)) as image:
                need((len(base), sha(base), sha(image.convert('RGBA').tobytes()), list(image.size))
                     == (frame['bytes'], frame['png_sha256'], frame['rgba_sha256'], prior['modern_candidate_canvas_size']),
                     'exact MAP07 combined canvas')
            need(len(draw) == prior['modern_candidate_draw_positions'] == info['modern_draw_candidate_positions']
                 and {r['image_key'] for r in draw} <= qualified_aliases, 'MAP07 pixel coverage')
            retained[f'dat/{key}.dat'] = raw
            retained[f'ls2map/{key}'] = server
            frames[floor] = base
            rooms[floor] = dict(original_name=decoded, name_sha256=sha(name), dimensions=[w, h], dat=dat,
                               server_map=dict(archive_path=f'gmsv/data/map/sainasu/hotoru/{key}', **identity(server)),
                               layer_comparison=comparison,
                               map07_canvas=dict(**frame, size=meta['canvas_size'], origin=meta['canvas_origin']),
                               map07_draw_references=len(draw))

    configs = config_rows(originals, sources, geometry, retained)
    for floor, room in rooms.items():
        room['source_create'] = configs[floor]

    raw_warps = (originals / 'mapwarp.txt').read_bytes()
    pin = sources['map01']['mapwarp']
    all_warps = parse_warps(raw_warps)
    need((len(raw_warps), sha(raw_warps), len(all_warps)) == (pin['raw_bytes'], pin['source_sha256'], pin['source_rows']),
         'full mapwarp source')
    retained['mapwarp.txt'] = raw_warps
    previous = {r['line']: r for r in sources['i11']['mapwarp_rows']}
    edges = []
    for line, source, destination, digest in all_warps:
        if source[0] not in FLOORS and destination[0] not in FLOORS:
            continue
        old = previous[line]
        points = [sample(geometry[point[0]], point[1:]) for point in (source, destination)]
        need((list(source), list(destination), digest) == (old['source'], old['target'], old['row_sha256']),
             'original warp identity')
        room_first = source[0] in FLOORS
        need(points == ([old['other_floor_tile_u16'], old['floor1300_tile_u16']] if room_first
                        else [old['floor1300_tile_u16'], old['other_floor_tile_u16']]), 'warp DAT values')
        if room_first:
            matching = [r for r in configs[source[0]] if r['xy'] == list(source[1:]) and r['target'] == list(destination)]
            need(len(matching) == 1 and matching[0]['block_sha256'] == old['same_tuple_create'][0]['block_sha256'],
                 'room exit CREATE')
        edges.append(dict(line=line, source=source, target=destination, row_sha256=digest, endpoints_dat_u16=points))
    need(len(edges) == 20, 'room warp count')
    report = dict(schema='stoneage.integration13.hotoru_five_rooms_source.r1',
                  source_scope='MIXED25_PRESERVED_STATIC_SOURCE_AND_SEPARATE_TW10_MAP07_PIXEL_CANDIDATES',
                  source_git_blobs={v[0]: v[1] for v in SOURCES.values()}, rooms=rooms, warp_rows=edges,
                  original_members={path: identity(data) for path, data in sorted(retained.items())},
                  limits=dict(native_game_executed=False, native_npc_appearance_proven=False, native_warp_execution_proven=False,
                              same_official_deployment_proven=False, shop_transaction_proven=False,
                              new_original_rd_decodes=0, new_base_map_renders=0))
    with zipfile.ZipFile(target, 'x', zipfile.ZIP_DEFLATED) as z:
        for path, raw in sorted(retained.items()):
            z.writestr(f'source/{path}', raw)
        for floor, png in frames.items():
            z.writestr(f'frames/{floor}.png', png)
        z.writestr('index.html', observer(rooms, edges))
        z.writestr('source-joins.json', json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + '\n')
    with zipfile.ZipFile(target) as z:
        need(z.testzip() is None, 'private ZIP CRC')
        report['private_package'] = {**identity(target.read_bytes()), 'members': len(z.namelist())}
    return report


def observer(rooms, edges):
    parts = []
    esc = html.escape
    for floor, room in rooms.items():
        width, height = room['map07_canvas']['size']
        ox, oy = room['map07_canvas']['origin']
        title = esc(room['original_name'].removesuffix('|0'))
        rows, markers, by_point = [], [], {}
        for i, r in enumerate(room['source_create'], 1):
            x, y = r['xy']
            label = esc(r['functionset'] or r['enemy_template'])
            if r['target'] is not None:
                label += ' → ' + ', '.join(map(str, r['target']))
            by_point.setdefault((x, y), []).append(i)
            rows.append(f'<tr><td>{i}</td><td>{x}, {y}</td><td>{label}</td><td>{r["graphic_alias"] or "—"}</td>'
                        f'<td>{esc(r["path"])} #{r["ordinal"]}</td></tr>')
        for (x, y), ids in by_point.items():
            cx, cy = ox + (x + y)*32, oy + (y - x)*24
            label = '/'.join(map(str, ids))
            markers.append(f'<g><circle cx="{cx}" cy="{cy}" r="{15 if len(ids) == 1 else 20}"/>'
                           f'<text x="{cx}" y="{cy+6}">{label}</text></g>')
        inbound = ', '.join(f'{e["source"][1:]}' for e in edges if e['target'][0] == floor)
        parts.append(f'<section id="floor-{floor}"><h2>{floor} · {title}</h2>'
                     f'<p>村內來向格 {esc(inbound)}</p><div class="scene"><img src="frames/{floor}.png" alt="{title}">'
                     f'<svg viewBox="0 0 {width} {height}" aria-label="配置點">{"".join(markers)}</svg></div>'
                     '<table><thead><tr><th>標記</th><th>原格</th><th>功能</th><th>圖號</th><th>來源塊</th></tr></thead>'
                     f'<tbody>{"".join(rows)}</tbody></table></section>')
    return ('<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" '
            'content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" '
            'content="default-src \'none\'; img-src \'self\' file:; style-src \'unsafe-inline\'">'
            '<title>霍特爾五間室內</title><style>body{background:#11232a;color:#f0f1e9;'
            'font:16px system-ui;margin:auto;max-width:1100px;padding:24px}nav{display:flex;gap:18px}a{color:#f0c979}'
            '.scene{position:relative}.scene img{width:100%;display:block}.scene svg{position:absolute;inset:0;width:100%;'
            'height:100%;fill:#eebd69;stroke:#11232a;stroke-width:2}svg text{fill:#11232a;stroke:none;text-anchor:middle;'
            'font-size:17px;font-weight:bold}table{border-collapse:collapse}td,th{text-align:left;border-bottom:1px solid #43616a;'
            'padding:6px}section{margin-top:38px}</style><h1>霍特爾五間室內</h1>'
            '<p>底圖沿用 MAP07 的跨來源候選畫面。圓點標出原配置座標，人物外觀與原生互動仍待驗證。'
            '同格的兩筆配置可分別在表格查閱。</p><nav>'
            + ''.join(f'<a href="#floor-{f}">{f}</a>' for f in rooms) + '</nav>' + ''.join(parts) + '</html>')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    for arg in ('originals', 'map07_zip', 'integration11_zip', 'private_zip', 'report'):
        p.add_argument(arg, type=Path)
    a = p.parse_args()
    report = export(a.originals, a.map07_zip, a.integration11_zip, a.private_zip)
    a.report.write_text(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + '\n', encoding='utf-8')
