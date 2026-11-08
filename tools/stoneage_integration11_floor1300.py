"""Join floor 1300 originals and render a private TW1 pixel candidate."""
import argparse
from collections import Counter
import csv
import gzip
import hashlib
import io
import json
from pathlib import Path
import re
import struct
import zipfile
import zlib

from tools.stoneage_integration10_dat_recovery import dat_planes
from tools.stoneage_map06_two_original_scenes import ADRN, META, need, placements, sha, source_images

ROOT = Path(__file__).resolve().parents[1]
REC = ROOT / 'research/recovered'
REPORT = REC / 'STONEAGE-INTEGRATION11-FLOOR1300-SOURCE-SCENE-R1.json'
PINS = {
    'i06': ('STONEAGE-INTEGRATION06-MAP1300-MAP-DAT-SIX-CREATE-SOURCE-R1.json', '5e1f49922731e55070cc6e43fbadf29a3609adeb'),
    'i10': ('STONEAGE-INTEGRATION10-TWELVE-RECOVERED-DAT-SEVEN-CHECKPOINT-SCENES-R1.json', '4b91fd0f0115bc58fed182b2f36468d5e3b117b2'),
    'char': ('STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json', 'a088b61a3212f7049e7793f587123ffb29bebad7'),
    'map': ('STONEAGE-MAP-SCENE-MODULE-01-ORIGINAL-SOURCE-MANIFEST-R1.json', '03675ee98d391f9ef0246315b2426f2a8b721fd3'),
}
FLOOR = 1300
WARP_FILES = ('genout/100warp.create', 'genout/warp_y.create')


def sources():
    result = {}
    for key, (filename, pin) in PINS.items():
        raw = (REC / filename).read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        need(blob == pin, f'changed source blob: {filename}')
        result[key] = json.loads(raw)
    return result


def point(fields):
    x, y, x2, y2 = map(int, fields[b'borncorner'].split(b','))
    need((x, y) == (x2, y2), 'expected point CREATE bounds')
    return int(fields[b'floorid']), x, y


def parse_warps(raw):
    rows = []
    for line, text in enumerate(raw.splitlines(), 1):
        if not text.strip() or text.lstrip().startswith(b'#'):
            continue
        fields = text.split(b':')
        need(len(fields) == 5 and all(re.fullmatch(rb'-?\d+,-?\d+,-?\d+', s)
                                      for s in fields[2:4]), 'unexpected mapwarp row grammar')
        source, target = (tuple(map(int, s.split(b','))) for s in fields[2:4])
        rows.append((line, source, target, sha(text)))
    return rows


def static_join(data, dat, src):
    from tools.stoneage_scene14_independent_replay import source_blocks

    width, height, planes = dat_planes(dat)

    def sample(xy):
        x, y = xy
        need(0 <= x < width and 0 <= y < height, 'floor 1300 endpoint outside DAT')
        return [plane[y*width+x] for plane in planes]

    char = src['char']
    manifest = {r[0]: r for r in char['source_files']}
    blocks = {(r[0], r[1]): r for r in char['create_rows']}
    for name, raw in data.items():
        if name.startswith('npc/'):
            row = manifest[name[4:]]
            need((len(raw), sha(raw), f'{zlib.crc32(raw):08x}') == tuple(row[1:4]), f'NPC identity {name}')

    def verified_block(path, ordinal):
        raw = data['npc/' + path]
        block = source_blocks(raw)[ordinal]
        row = blocks[path, ordinal]
        # CHAR01 hashes the closing line terminator as part of the byte span.
        tail = raw[block['end']:row[3]]
        need(block['start'] == row[2] and row[3] >= block['end']
             and tail in (b'', b'\n', b'\r\n'), f'CREATE block extent {path}:{ordinal}')
        digest = sha(raw[row[2]:row[3]])
        need(digest == row[4], f'CREATE block identity {path}:{ordinal}')
        return block['fields'], digest

    creates = []
    for row in src['i06']['floor1300_source_create_records']:
        path, ordinal = row['create_path'], row['create_block_ordinal']
        fields, digest = verified_block(path, ordinal)
        floor, x, y = point(fields)
        parameter = row['parameter_path']
        function = row['source_function']
        need(floor == FLOOR and int(fields[b'graphicname']) == row['graphic_alias'], 'CREATE floor/alias mismatch')
        token = blocks[path, ordinal][11]
        need(fields[b'enemy'] == f'{token}|file:{parameter}'.encode(), 'CREATE parameter link')
        expected_scope = digest if row['create_sha_scope'] == 'ORIGINAL_CREATE_BLOCK' else sha(data['npc/'+path])
        need(expected_scope == row['create_sha256'], 'CREATE SHA scope')
        need(sha(data['npc/'+parameter]) == row['parameter_sha256'], 'CREATE parameter SHA')
        creates.append(dict(path=path, ordinal=ordinal, block_sha256=digest, parameter=parameter,
                            parameter_sha256=row['parameter_sha256'], function=function, enemy_token=token,
                            graphic_alias=row['graphic_alias'],
                            xy=[x, y], source_tile_u16=sample((x, y))))

    map_manifest = src['map']['mapwarp']
    raw = data['map/mapwarp.txt']
    need((len(raw), sha(raw)) == (map_manifest['raw_bytes'], map_manifest['source_sha256']), 'mapwarp identity')
    all_rows = parse_warps(raw)
    need(len(all_rows) == map_manifest['source_rows'], 'mapwarp source row conservation')
    map_rows = [(line, a, b, digest) for line, a, b, digest in all_rows if FLOOR in (a[0], b[0])]
    by_edge = {}
    for path in WARP_FILES:
        for ordinal, block in enumerate(source_blocks(data['npc/'+path])):
            args = block['fields'].get(b'enemy', b'').split(b'|')
            if len(args) != 4 or args[0] != b'npcgen_warp':
                continue
            a, b = point(block['fields']), tuple(map(int, args[1:]))
            if FLOOR in (a[0], b[0]):
                _, digest = verified_block(path, ordinal)
                by_edge.setdefault((a, b), []).append(dict(path=path, ordinal=ordinal, block_sha256=digest))
    map_edges = {(a, b) for _, a, b, _ in map_rows}
    rows = [dict(line=line, row_sha256=digest, source=a, target=b,
                 floor1300_tile_u16=sample((a if a[0] == FLOOR else b)[1:]),
                 exact_reverse=(b, a) in map_edges, same_tuple_create=by_edge.get((a, b), []))
            for line, a, b, digest in map_rows]
    create_only = [dict(source=a, target=b, creates=v) for (a, b), v in sorted(by_edge.items())
                   if (a, b) not in map_edges]
    overlap = []
    for a in sorted({tuple(row['xy']) for row in creates}):
        x, y = a
        same = [r for r in char['create_rows'] if r[5] == FLOOR and r[7] == [x, y, x, y]]
        if len(same) > 1:
            members = []
            for r in same:
                fields, digest = verified_block(r[0], r[1])
                members.append(dict(path=r[0], ordinal=r[1], block_sha256=digest,
                                    enemy_token=fields[b'enemy'].split(b'|')[0].decode('ascii')))
            overlap.append(dict(xy=a, separate_create_blocks=members))
    return creates, rows, create_only, overlap


def join_other_endpoints(originals, warps, src):
    expected = {r[5]: tuple(r[2:5]) for r in src['map']['original_decoded_source_rows']
                if r[0] == 0 and r[1].lower().endswith('.dat') and r[5] is not None}
    recovered = next(r for r in src['i10']['recovered_DAT'] if r['floor'] == 100)
    expected[100] = tuple(recovered[k] for k in ('bytes', 'sha256', 'crc32'))
    floors = {v[0] for r in warps for v in (r['source'], r['target'])} - {FLOOR}
    data, geometry, receipts = {}, {}, {}
    for floor in sorted(floors):
        name = f'linked-dat/{floor}.dat'
        raw = (originals/name).read_bytes()
        identity = (len(raw), sha(raw), f'{zlib.crc32(raw):08x}')
        need(identity == expected[floor], f'linked DAT identity: {floor}')
        w, h, planes = dat_planes(raw)
        data[name] = raw
        geometry[floor] = (w, h, planes)
        receipts[floor] = dict(bytes=identity[0], sha256=identity[1], crc32=identity[2],
                               width=w, height=h)
    for r in warps:
        floor, x, y = r['target'] if r['source'][0] == FLOOR else r['source']
        w, h, planes = geometry[floor]
        need(0 <= x < w and 0 <= y < h, f'linked endpoint outside DAT: {floor}')
        r['other_floor_tile_u16'] = [p[y*w+x] for p in planes]
    return data, receipts


def atlas(tiles, tw, wanted):
    from PIL import Image
    from tools.stoneage_private_scene_palette_r3 import candidate_rgba
    from tools.stoneage_rd_codec import decode_rd_block
    from tools.stoneage_scene14_independent_replay import decode
    from tools.stoneage_scene21_town1000 import check, package
    from tools.stoneage_tw10_palette import initial_rgb

    available = {row[0] for row in json.loads(META.read_bytes())['source_TW1_real_RD_rows']}
    reused = wanted & available
    missing = wanted - available
    images, records, _ = source_images(tiles, reused)
    with package(tw, 'tw') as z:
        adrn = z.read('source/data/adrn_1.bin')
        real = z.read('source/data/real_1.bin')
        palette = z.read('source/data/pal/Palet_1.sap')
    for raw, pin in ((adrn, 'tw_adrn'), (real, 'tw_real'), (palette, 'pal')):
        check(raw, pin)
    rgb = initial_rgb(palette)
    hits = {key: [] for key in wanted}
    for offset in range(0, len(adrn), 80):
        key = struct.unpack_from('<i', adrn, offset+76)[0]
        if key in hits:
            hits[key].append(offset//80)
    need(all(len(v) == 1 for v in hits.values()), 'TW1 ADRN alias absent or ambiguous')
    indices = {v[0] for v in hits.values()}
    with gzip.open(ADRN, 'rt') as f:
        table = {int(r['index']): r for r in csv.DictReader(f, delimiter='\t') if int(r['index']) in indices}
    new = {}
    rd_bytes = {}
    for key, (index,) in sorted(hits.items()):
        record = adrn[index*80:(index+1)*80]
        _, start, size, xoff, yoff, w, h = struct.unpack_from('<IIIiiii', record)
        need(16 < size <= len(real)-start, 'RD extent')
        rd = real[start:start+size]
        need(sha(rd) == table[index]['rd_block_sha256'], 'published RD hash mismatch')
        header, pixels = decode_rd_block(rd, authoritative_block_size=size)
        need((header['width_s'], header['height_s']) == (w, h), 'ADRN/RD dimensions')
        need(decode(rd) == (w, h, pixels), 'independent indexed RD replay')
        rgba = candidate_rgba(pixels, w, h, rgb)
        geometry = dict(xoff=xoff, yoff=yoff, width=w, height=h)
        if key in reused:
            need(records[key] == geometry and images[key].tobytes() == rgba, 'MAP04 actual pixel mismatch')
        else:
            images[key] = Image.frombytes('RGBA', (w, h), rgba)
            records[key] = geometry
            new[key] = dict(adrn_index=index, adr_sha256=sha(record), rd_sha256=sha(rd),
                            index_sha256=sha(pixels), rgba_sha256=sha(rgba), **geometry)
            rd_bytes[key] = rd
    return images, records, new, rd_bytes


def make_canvas(dat, images, records, draw):
    import numpy as np
    from tools.stoneage_scene21_town1000 import render

    coords = [(x*32+y*32, (y-x)*24) for x, y in ((0, 0), (0, 99), (99, 0), (99, 99))]
    left, right = min(x for x, _ in coords), max(x for x, _ in coords)+1
    top, bottom = min(y for _, y in coords), max(y for _, y in coords)+1
    for row in draw:
        x, y = row['anchor']
        g = records[row['image_key']]
        x, y = x+g['xoff'], y+g['yoff']
        left, top = min(left, x), min(top, y)
        right, bottom = max(right, x+g['width']), max(bottom, y+g['height'])
    origin = (16-left, 16-top)
    size = (right-left+32, bottom-top+32)
    scene = render(images, records, draw, False, True, False, origin, size)

    # Re-read coordinates from the original bytes and replay with NumPy masks.
    raw = np.frombuffer(dat, dtype='<u2', offset=8).reshape(3, 100, 100)
    canvas = np.empty((size[1], size[0], 4), dtype=np.uint8)
    canvas[:] = (17, 35, 42, 255)
    atlas_arrays = {key: np.asarray(image) for key, image in images.items()}
    count = 0
    for plane in raw[:2]:
        for diagonal in range(-99, 100):
            for x in range(min(99, 99+diagonal), max(0, diagonal)-1, -1):
                y = x-diagonal
                key = int(plane[y, x])
                if key <= 99:
                    continue
                g = records[key]
                x0 = origin[0]+(x+y)*32+g['xoff']
                y0 = origin[1]+(y-x)*24+g['yoff']
                tile = atlas_arrays[key]
                area = canvas[y0:y0+g['height'], x0:x0+g['width']]
                mask = tile[:, :, 3] == 255
                area[mask] = tile[mask]
                count += 1
    need(count == len(draw) and np.array_equal(canvas, np.asarray(scene)), 'independent complete canvas mismatch')
    return scene, origin


def export(originals, dat_path, tiles, tw, output):
    from PIL import Image, ImageDraw
    from tools.stoneage_scene14_independent_replay import source_blocks

    output = output.resolve()
    need(output != ROOT and ROOT not in output.parents and not output.exists()
         and not output.with_suffix('.jpg').exists(), 'new private output outside Git')
    src = sources()
    dat = dat_path.read_bytes()
    pin = next(r for r in src['i10']['recovered_DAT'] if r['floor'] == FLOOR)
    need((len(dat), sha(dat), f'{zlib.crc32(dat):08x}') ==
         (pin['bytes'], pin['sha256'], pin['crc32']), 'DAT original identity')
    paths = {'npc/'+r[k] for r in src['i06']['floor1300_source_create_records']
             for k in ('create_path', 'parameter_path')}
    paths |= {'npc/'+p for p in WARP_FILES} | {'map/mapwarp.txt', '1300.MAP'}
    data = {name: (originals/name).read_bytes() for name in sorted(paths)}
    map_raw = data['1300.MAP']
    old_map = src['i06']['original_MAP_rows'][0]
    need((len(map_raw), sha(map_raw)) == (old_map['bytes'], old_map['original_sha256']), 'MAP original identity')
    w, h, planes = dat_planes(dat)
    need((w, h) == (100, 100) and struct.unpack_from('<II', map_raw) == (w, h), 'map extent')
    map_words = struct.unpack_from('<10000H', map_raw, 8)
    creates, warps, create_only, overlap = static_join(data, dat, src)
    linked, linked_receipts = join_other_endpoints(originals, warps, src)
    data.update(linked)
    board, = [r for r in source_blocks(data['npc/genout/1300npc_m.create'])
              if r['fields'][b'enemy'] == b'npcgen_dengon']
    board_name = board['fields'][b'name'].decode('cp950')
    need(board_name == '霍特爾的傳言板', 'source village name witness')
    board_fields = board['fields']
    board_floor, board_x, board_y = point(board_fields)
    need(board_floor == FLOOR, 'village name witness floor')
    village = dict(editorial_category='VILLAGE', source_name='霍特爾',
                   name_witness_path='genout/1300npc_m.create', name_witness_xy=[board_x, board_y],
                   name_witness_text_sha256=sha(board_fields[b'name']), geographic_region=None)

    _, draw = placements(dat)
    counts = Counter(r['image_key'] for r in draw)
    images, records, new, rd_bytes = atlas(tiles, tw, set(counts))
    scene, origin = make_canvas(dat, images, records, draw)
    size = scene.size
    buffer = io.BytesIO()
    scene.save(buffer, format='PNG')
    png = buffer.getvalue()
    rgba_digest = sha(scene.tobytes())
    scene.thumbnail((1920, 1440), Image.Resampling.LANCZOS)
    preview = scene.convert('RGB')
    mark = ImageDraw.Draw(preview)

    def xy(x, y):
        return (round((origin[0]+(x+y)*32)*preview.width/size[0]),
                round((origin[1]+(y-x)*24)*preview.height/size[1]))

    for label, radius, color in (('source', 4, '#5dd9ff'), ('target', 2, '#fc9e61')):
        for point_ in {tuple(edge[label][1:]) for edge in warps if edge[label][0] == FLOOR}:
            x, y = xy(*point_)
            mark.rectangle((x-radius, y-radius, x+radius, y+radius), outline=color, width=2)
    numbered = {}
    for i, row in enumerate(creates, 1):
        numbered.setdefault(tuple(row['xy']), []).append(str(i))
    for point_, labels in numbered.items():
        x, y = xy(*point_)
        mark.ellipse((x-5, y-5, x+5, y+5), fill='#ffe66c', outline='black')
        mark.text((x+7, y-7), '/'.join(labels), fill='#ffe66c', stroke_width=2, stroke_fill='black')
    preview.save(output.with_suffix('.jpg'), quality=93)

    report = dict(
        schema='stoneage.integration11.floor1300.source_scene.r1',
        source_blobs={key: pin for key, (_, pin) in PINS.items()},
        original_DAT={k: pin[k] for k in ('bytes', 'sha256', 'crc32')},
        original_MAP=dict(bytes=len(map_raw), sha256=sha(map_raw),
                          equal_u16_cells_by_DAT_plane=[sum(a == b for a, b in zip(map_words, plane)) for plane in planes]),
        dimensions=[w, h], village=village, creates=creates, colocated_create_blocks=overlap,
        mapwarp_rows=warps, direct_CREATE_only=create_only, linked_DAT=linked_receipts,
        source_members={name: dict(bytes=len(raw), sha256=sha(raw)) for name, raw in data.items()},
        candidate=dict(draw_references=len(draw), distinct_aliases=len(counts), reused_MAP04_aliases=len(counts)-len(new),
                       recovered_aliases=len(new), recovered_references=sum(counts[k] for k in new),
                       uncovered_references=0, dimensions=size, origin=origin, png_sha256=sha(png),
                       rgba_sha256=rgba_digest, independent_canvas_match=True),
        new_aliases={str(k): dict(references=counts[k], **row) for k, row in new.items()},
        limits=dict(native_collision_verified=False, native_NPC_spawn_verified=False,
                    native_warp_execution_verified=False, native_renderer_verified=False,
                    official_same_deployment_verified=False, original_assets_published=False))
    names = ['寄信任务', '斧头与感谢函', '四村事件', '环岛 C9', '时钟配置 4', '时钟配置 6']
    markers = ''.join(f'<li>{i}．{name} {row["xy"]}，原图别名 {row["graphic_alias"]}</li>'
                      for i, (name, row) in enumerate(zip(names, creates), 1))
    directions = Counter((r['source'][0], r['target'][0]) for r in warps)
    links = ''.join(f'<li>{a} → {b}：{n} 条</li>' for (a, b), n in sorted(directions.items()))
    page = ('<!doctype html><meta charset="utf-8"><title>1300 原件场景查阅</title>'
            '<style>body{background:#11232a;color:#eee;font:16px sans-serif;margin:30px}'
            'img{max-width:100%}a{color:#5dd9ff}</style><h1>霍特爾（1300）地图与创建／传送资料</h1>'
            '<p>社区混合 2.5 DAT × 台湾 1.0 RD。候选图以两平面与现代绘制顺序合成。'
            '黄色为创建点，蓝色为传送源，橙色为落点，重合点可查坐标表。</p>'
            '<img src="annotated.jpg" alt="1300 配置位置预览"><p><a href="floor1300.png">查看无标记全图</a></p>'
            f'<h2>创建位置</h2><ol>{markers}</ol><h2>传送表方向计数</h2><ul>{links}</ul>'
            '<p>完整端点、源行号与原格值见 source-derived.json。</p>')
    with zipfile.ZipFile(output, 'x', zipfile.ZIP_DEFLATED) as z:
        z.writestr('index.html', page)
        z.writestr('floor1300.png', png)
        z.write(output.with_suffix('.jpg'), 'annotated.jpg')
        z.writestr('source/1300.DAT', dat)
        z.writestr('source-derived.json', json.dumps(report, ensure_ascii=False, indent=2))
        for name, raw in data.items():
            z.writestr('source/'+name, raw)
        for key, rd in rd_bytes.items():
            z.writestr(f'source/TW1-RD/{key}.rd', rd)
    with zipfile.ZipFile(output) as z:
        need(z.testzip() is None, 'private archive ZIP CRC')
        report['private_archive'] = dict(bytes=output.stat().st_size, sha256=sha(output.read_bytes()),
                                         members=len(z.namelist()))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for arg in ('originals', 'dat', 'tiles', 'tw', 'output'):
        parser.add_argument(arg, type=Path)
    args = parser.parse_args()
    report = export(args.originals, args.dat, args.tiles, args.tw, args.output)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report['candidate']))


if __name__ == '__main__':
    main()
