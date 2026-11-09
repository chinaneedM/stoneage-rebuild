"""Build a private three-room observer from verified StoneAge source files."""
import argparse
import base64
import hashlib
from html import escape
import io
import json
from pathlib import Path
import struct
import zipfile

from tools.stoneage_integration10_dat_recovery import dat_planes
from tools.stoneage_integration11_floor1300 import parse_warps, point
from tools.stoneage_integration13_hotoru_rooms import identity, sample
from tools.stoneage_item06_mixed25_item_pixels import render_bitmap, resolve_aliases, source_pin
from tools.stoneage_map06_two_original_scenes import need, sha
from tools.stoneage_pet11_tw10_capture_sprite_source import file_sha, records
from tools.stoneage_server_static_map import parse_ls2map
from tools.stoneage_tw10_palette import initial_rgb

ROOT = Path(__file__).resolve().parents[1]
FLOORS = (1103, 1203, 2003)
REPORT = 'STONEAGE-INTEGRATION16-THREE-PET-ROOMS-SOURCE-R1.json'
PINS = {
    'char': ('STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json', 'a088b61a3212f7049e7793f587123ffb29bebad7'),
    'skills': ('STONEAGE-GAMEPLAY03-ORIGINAL-21-PET-SKILL-SHOP-SOURCE-R1.json', '5735ddc1117a8a6fb2f9417327ec242e4fd06192'),
    'shops': ('STONEAGE-GAMEPLAY05-ORIGINAL-PETSHOP-SAVEPOINT-HEAL-SOURCE-R1.json', '878be2f05a4dc17f51d21ed2401fd7a7f3d73563'),
    'map01': ('STONEAGE-MAP-SCENE-MODULE-01-ORIGINAL-SOURCE-MANIFEST-R1.json', '03675ee98d391f9ef0246315b2426f2a8b721fd3'),
    'map07': ('STONEAGE-MAP07-28-ORIGINAL-DAT-SOURCE-SCENE-RECEIPT-R1.json', 'f2cba278f4b5a15e50e905a1e6591958fd09dba5'),
    'map09': ('STONEAGE-MAP09-691-SOURCE-READY-SCENES-R1.json', '137580e7c25aadf3d679b6ebfb5080b79912cc4f'),
    'world11': ('STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-11-NPC-STATIC-APPEARANCE-R1.json', 'f79d7355a4e82c2bd8c0a771b898690cc4a3e680'),
}
LIMITS = dict(official_same_deployment=False, original_client_or_server_executed=False,
              native_renderer_or_collision_verified=False, native_storage_or_training_verified=False,
              proprietary_sources_published=False, overall_percent=None)


def upstream():
    result = {}
    for key, (name, pin) in PINS.items():
        raw = (ROOT / 'research/recovered' / name).read_bytes()
        need(hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest() == pin, name)
        result[key] = json.loads(raw)
    return result


def service_candidates(sources, floor):
    shops = sources['shops']['original_CREATE_refs_and_derived_numeric_fields']
    skills = sources['skills']['original_skillshop_CREATE_to_parameter_rows']
    for r in shops:
        if r['floorid'] == floor and r['source_function'] == 'npcgen_petshop':
            yield (r['create_path'], r['create_ordinal'], r['source_parameter_path'],
                   'PetShop', r['source_parameter_sha256'], r['create_block_sha256'], r['graphicname'])
    for r in skills:
        if r['source_floorid'] == floor:
            yield (r['create_file'], r['create_ordinal'], r['parameter_path'],
                   'PetSkillShop', r['source_original_sha256'], r['create_block_sha256'], r['source_graphicnum'])


def services(npc, sources, geometries, retained):
    from tools.stoneage_scene14_independent_replay import source_blocks

    char = sources['char']
    members = {r[0]: r[1:4] for r in char['source_files']}
    creates = {(r[0], r[1]): r for r in char['create_rows']}
    templates = {(r[0], r[1]): r for r in char['template_rows']}
    parsed = {}

    def original(path):
        key = 'npc/' + path
        if key not in retained:
            raw = npc.read(key)
            need(list(identity(raw).values()) == members[path], 'original NPC member ' + path)
            need(raw.decode('cp950').encode('cp950') == raw, 'source CP950 round trip')
            retained[key] = raw
        return retained[key]

    def block(path, ordinal):
        if path not in parsed:
            parsed[path] = source_blocks(original(path))
        return parsed[path][ordinal]

    output = []
    for floor, geometry in geometries.items():
        candidates = list(service_candidates(sources, floor))
        need([c[3] for c in candidates] == ['PetShop', 'PetSkillShop'], 'expected one of each role')
        for path, ordinal, parameter, role, parameter_sha, create_sha, alias in candidates:
            row = creates[path, ordinal]
            create = block(path, ordinal)
            raw = original(path)
            fields = create['fields']
            need(create['start'] == row[2] and raw[create['end']:row[3]] in (b'\n', b'\r\n')
                 and sha(raw[row[2]:row[3]]) == row[4] == create_sha, 'CREATE byte span')
            actual_floor, x, y = point(fields)
            need(actual_floor == row[5] == floor and int(fields[b'graphicname']) == row[6] == alias
                 and row[7] == [x, y, x, y], 'CREATE position and graphic')
            need(fields[b'enemy'] == f'{row[11]}|file:{parameter}'.encode()
                 and row[15] == [[parameter, 'EXACT_SAME_NPC_SUBTREE_PATH', parameter_sha]]
                 and sha(original(parameter)) == parameter_sha, 'exact parameter path and SHA')
            ((template_path, template_ordinal),) = row[13]
            template = block(template_path, template_ordinal)
            traw = original(template_path)
            end = template['end']
            terminator = b'\r\n' if traw[end:].startswith(b'\r\n') else b'\n'
            template_sha = templates[template_path, template_ordinal][2]
            need(traw[end:].startswith(terminator) and sha(traw[template['start']:end] + terminator) == template_sha
                 and template['fields'][b'templatename'] == row[11].encode()
                 and template['fields'][b'functionset'] == role.encode(), 'exact template and function')
            output.append(dict(floor=floor, xy=[x, y], graphic=alias, role=role, create=[path, ordinal, create_sha],
                               template=[template_path, template_ordinal, template_sha],
                               parameter=[parameter, parameter_sha], dat_u16=sample(geometry, (x, y))))
    return output


def png_identity(png):
    from PIL import Image

    with Image.open(io.BytesIO(png)) as image:
        return dict(dimensions=list(image.size), png_sha256=sha(png), rgba_sha256=sha(image.convert('RGBA').tobytes()))


def graphics(directory, real_path, wanted, world_zip, source, retained):
    paths = {name: directory / name for name in source['original_files']}
    paths['real_15.bin'] = real_path
    for name, path in paths.items():
        pin = source['original_files'][name]
        source_pin(path, (pin['bytes'], pin['sha256'], pin['crc32']))
    adrn = paths['adrn_15.bin'].read_bytes()
    spr = records(paths['spradrn_5.bin'].read_bytes())
    aliases = resolve_aliases(adrn, wanted)
    known = {r['graphic']: r for r in source['decoded_static_graphics']}
    palette_raw = paths['Palet_1.sap'].read_bytes()
    palette = initial_rgb(palette_raw)
    retained['pixels/Palet_1.sap'] = palette_raw
    output = {}
    with real_path.open('rb') as real:
        for alias in sorted(wanted):
            ((index, record),) = aliases[alias]
            bitmap, offset, size, dx, dy, width, height = struct.unpack_from('<IIIiiii', record)
            need(not any(r[0] == alias for r in spr), 'same alias also in SPR index')
            need(16 <= size <= 1_000_000 and 0 < width <= 1024 and 0 < height <= 1024
                 and offset + size <= real_path.stat().st_size, 'original ADRN range')
            real.seek(offset)
            rd = real.read(size)
            meta = dict(bitmap=bitmap, adrn_ordinal=index, adrn_sha256=sha(record), rd_offset=offset,
                        rd_bytes=size, rd_sha256=sha(rd), signed_adrn_offset=[dx, dy])
            if alias in known:
                png = world_zip.read(f'npc/{alias}.png')
                prior = known[alias]
                need(all(prior[k] == v for k, v in meta.items() if k != 'bitmap'), 'WORLD11 original ADRN and RD')
                image = png_identity(png)
                need(all(prior[k] == v for k, v in image.items()), 'WORLD11 exact PNG and RGBA')
                pixel_sha = prior['indexed_sha256']
                mode = 'WORLD11_REUSED_ORIGINAL_PNG'
            else:
                status, _, pixels, png = render_bitmap(rd, width, height, palette)
                need(status == 'strict' and all(i == 0 or 16 <= i < 240 for i in pixels), 'strict original RD/palette')
                pixel_sha = sha(pixels)
                mode = 'TWO_DECODERS_ORIGINAL_RD'
                image = png_identity(png)
            need(image['dimensions'] == [width, height], 'ADRN / PNG dimensions')
            output[alias] = dict(**meta, **image, graphic=alias, mode=mode, indexed_sha256=pixel_sha)
            retained[f'pixels/{alias}.png'] = png
            retained[f'pixels/{alias}.rd'] = rd
            retained[f'pixels/{alias}.adrn'] = record
    return output


def view_box(frame, services):
    from PIL import Image, ImageChops

    with Image.open(io.BytesIO(frame)) as decoded:
        image = decoded.convert('RGB')
    background = Image.new('RGB', image.size, image.getpixel((0, 0)))
    left, top, right, bottom = ImageChops.difference(image, background).getbbox()
    for service in services:
        gx, gy = service['graphic_px']
        mx, my = service['marker_px']
        w, h = service['graphic_dimensions']
        left, top = min(left, gx, mx - 16), min(top, gy, my - 16)
        right, bottom = max(right, gx + w, mx + 16), max(bottom, gy + h, my + 16)
    padding = 36
    left, top = max(0, left - padding), max(0, top - padding)
    right, bottom = min(image.width, right + padding), min(image.height, bottom + padding)
    return [left, top, right - left, bottom - top]


def observer(rooms, retained):
    def data(path):
        return 'data:image/png;base64,' + base64.b64encode(retained[path]).decode()

    sections = []
    for floor, room in rooms.items():
        width, height = room['canvas_size']
        view = ' '.join(map(str, room['observer_view_box']))
        markers, sprites, cards = [], [], []
        for service in room['services']:
            x, y = service['marker_px']
            left, top = service['graphic_px']
            alias = service['graphic']
            w, h = service['graphic_dimensions']
            role = service['role']
            title = '寵物店服務' if role == 'PetShop' else '寵物技能教學'
            anchor = f'card-{floor}-{role}'
            sprites.append(f'<image class="sprite" href="{data(f"pixels/{alias}.png")}" x="{left}" y="{top}" width="{w}" height="{h}"/>')
            markers.append(f'<a href="#{anchor}" aria-label="{title}"><circle cx="{x}" cy="{y}" r="15"/>'
                           f'<text x="{x}" y="{y + 6}">{"店" if role == "PetShop" else "技"}</text></a>')
            parameter = service['parameter'][0]
            original = escape(retained['npc/' + parameter].decode('cp950'))
            cards.append(f'<article id="{anchor}"><h3>{title} <small>{role}</small></h3>'
                         f'<p>原格 {service["xy"]} · 圖號 {alias} · <code>{escape(parameter)}</code></p>'
                         f'<details><summary>原配置參數</summary><pre>{original}</pre></details></article>')
        title = escape(room['original_name'].removesuffix('|0'))
        doors = ''.join(f'<li>{e["source"]} → {e["target"]}</li>' for e in room['warps'])
        sections.append(f'<section id="floor-{floor}"><h2>{floor} · {title}</h2>'
                        f'<label><input type="checkbox" checked> 顯示來源人物圖</label>'
                        f'<svg viewBox="{view}" aria-label="{title}">'
                        f'<image href="{data(f"scenes/{floor}.png")}" width="{width}" height="{height}"/>'
                        f'<g class="sprites">{"".join(sprites)}</g>{"".join(markers)}</svg>'
                        f'{"".join(cards)}<details><summary>原傳送配置</summary><ul>{doors}</ul></details></section>')
    nav = ' · '.join(f'<a href="#floor-{floor}">{floor}</a>' for floor in rooms)
    return ('''<!doctype html><html lang="zh-Hant"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src data:; style-src 'unsafe-inline'">
<title>三間寵物店原配置觀察</title>
<style>
body{background:#11232a;color:#f0f1e9;font:16px system-ui;margin:auto;max-width:1100px;padding:22px}
a{color:#ffda8d}section{margin:36px 0;border-top:1px solid #49626a}svg{display:block;width:100%;max-height:660px;background:#11232a}
section:has(input:not(:checked)) .sprites{display:none}.sprites{pointer-events:none}
circle{fill:#ffda8d;stroke:#11232a;stroke-width:2}text{fill:#11232a;text-anchor:middle;font-size:17px;font-weight:bold;pointer-events:none}
article{margin:12px 0;padding:0 12px 12px;border:1px solid #49626a}article:target{border-color:#ffda8d}
pre{white-space:pre-wrap;overflow-wrap:anywhere}summary{cursor:pointer}code{overflow-wrap:anywhere}
</style>
<h1>三間寵物店原配置觀察</h1>
<p>後期社群保存版的原 NPC 配置與人物圖，疊加於另存臺灣 1.0 圖塊的候選場景。圓點可跳到來源卡，原生繪製、寄放與技能學習待證。</p>
''' + f'<nav>{nav}</nav>' + ''.join(sections) + '</html>\n')


def build(parent, directory, real_path, npc_path, map_path, world_path, target):
    source = upstream()
    target = target.resolve()
    need(ROOT not in target.parents and not target.exists(), 'private ZIP must be new and outside Git')
    parent_identity = dict(bytes=parent.stat().st_size, sha256=file_sha(parent))
    need(parent_identity == dict(bytes=source['map01']['original_rar_bytes'],
                                 sha256=source['map01']['original_rar_sha256']), 'original RAR')
    shop_source = source['shops']['source']
    archive_pins = (
        (npc_path, shop_source['original_NPC_ZIP_bytes'], shop_source['original_private_NPC_ZIP_sha256'], 2205),
        (map_path, *(source['map07']['private_deliverable'][k] for k in ('bytes', 'sha256', 'members'))),
        (world_path, *(source['world11']['observer'][k] for k in ('bytes', 'sha256', 'members'))),
    )
    for path, size, digest, _ in archive_pins:
        need(path.stat().st_size == size and file_sha(path) == digest, path.name)
    retained, rooms, geometries = {}, {}, {}
    with zipfile.ZipFile(npc_path) as npc, zipfile.ZipFile(map_path) as maps, zipfile.ZipFile(world_path) as world:
        for z, (_, _, _, members) in zip((npc, maps, world), archive_pins):
            need(len(set(z.namelist())) == len(z.namelist()) == members and z.testzip() is None, 'original ZIP CRC')
        map07 = {r['floor']: r for r in source['map07']['maps']}
        private_maps = json.loads(maps.read('source-qualified-derived-report.json'))['maps']
        warp = (directory / 'mapwarp.txt').read_bytes()
        need(sha(warp) == source['map01']['mapwarp']['source_sha256'], 'original mapwarp whole SHA')
        warps = parse_warps(warp)
        need(len(warps) == source['map01']['mapwarp']['source_rows'], 'original mapwarp row count')
        retained['maps/mapwarp.txt'] = warp
        for floor in FLOORS:
            key = str(floor)
            dat = maps.read(f'sources/{floor}.dat')
            base = maps.read(f'scenes/{floor}-combined.png')
            server = (directory / key).read_bytes()
            width, height, planes = geometry = geometries[floor] = dat_planes(dat)
            ls = parse_ls2map(server)
            dat_hash = sha(dat)
            public = source['map09']['maps'][key]
            prior = private_maps[key]
            image = png_identity(base)
            need(dat_hash == map07[floor]['source_dat_sha256'] == public['source_sha256']
                 and image['png_sha256'] == prior['frames']['combined']['png_sha256']
                 and image['rgba_sha256'] == public['frame_RGBA_sha256']['combined']
                 and image['dimensions'] == public['canvas_size'] and prior['canvas_origin'] == public['origin'],
                 'exact MAP07 and MAP09 DAT / canvas')
            need((ls.floor_id, ls.width, ls.height) == (floor, width, height), 'LS2MAP room extent')
            name = server[8:40].split(b'\0', 1)[0].decode('cp950')
            need(name.endswith('的寵物店|0'), 'original LS2MAP pet shop name')
            edges = []
            for line, start, end, row_sha in warps:
                if floor in (start[0], end[0]):
                    local = start if start[0] == floor else end
                    edges.append(dict(line=line, source=list(start), target=list(end), sha256=row_sha,
                                      room_dat_u16=sample(geometry, local[1:])))
            rooms[floor] = dict(original_name=name, dat=identity(dat), ls2map=identity(server), canvas=image,
                                canvas_size=public['canvas_size'], origin=public['origin'], warps=edges, services=[],
                                server_client_changed_cells=[sum(a != b for a, b in zip(p, q))
                                                             for p, q in zip((ls.tile_ids, ls.object_ids), planes)])
            retained[f'maps/{floor}.dat'] = dat
            retained[f'maps/{floor}.ls2map'] = server
            retained[f'scenes/{floor}.png'] = base
        joins = services(npc, source, geometries, retained)
        images = graphics(directory, real_path, {r['graphic'] for r in joins}, world, source['world11'], retained)
    for row in joins:
        image = images[row['graphic']]
        room = rooms[row['floor']]
        x, y = row['xy']
        ox, oy = room['origin']
        marker = [ox + (x+y)*32, oy + (y-x)*24]
        graphic = [a + b for a, b in zip(marker, image['signed_adrn_offset'])]
        w, h = image['dimensions']
        need(0 <= graphic[0] <= room['canvas_size'][0] - w and 0 <= graphic[1] <= room['canvas_size'][1] - h,
             'candidate graphic lies outside full canvas')
        room['services'].append(dict(**row, marker_px=marker, graphic_px=graphic, graphic_dimensions=[w, h]))
    for floor, room in rooms.items():
        room['observer_view_box'] = view_box(retained[f'scenes/{floor}.png'], room['services'])
    report = dict(schema='stoneage.integration16.three_pet_rooms.r1', parent_rar=parent_identity,
                  upstream_git_blobs={k: v[1] for k, v in PINS.items()}, rooms=rooms, graphics=list(images.values()),
                  original_mapwarp_sha256=sha(warp), bounds=LIMITS)
    retained['index.html'] = observer(rooms, retained).encode()
    retained['source-joins.json'] = (json.dumps(report, ensure_ascii=False, indent=2) + '\n').encode()
    with zipfile.ZipFile(target, 'x') as output:
        for path, raw in sorted(retained.items()):
            info = zipfile.ZipInfo(path)
            output.writestr(info, raw, compress_type=zipfile.ZIP_DEFLATED)
    with zipfile.ZipFile(target) as output:
        need(output.testzip() is None, 'private package ZIP CRC')
        report['private_package'] = dict(filename=target.name, bytes=target.stat().st_size,
                                         sha256=file_sha(target), members=len(output.namelist()))
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('parent', 'directory', 'real', 'npc', 'map07', 'world11', 'private_zip', 'report'):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    receipt = build(args.parent, args.directory, args.real, args.npc, args.map07, args.world11, args.private_zip)
    args.report.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
