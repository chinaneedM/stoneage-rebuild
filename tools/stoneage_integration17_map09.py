"""Recover INTEGRATION17 map canvases and corroborate both ends of the original doors."""
import base64
import io
import json
import zipfile

from tools.stoneage_integration10_dat_recovery import dat_planes
from tools.stoneage_integration11_floor1300 import point
from tools.stoneage_integration13_hotoru_rooms import identity, sample
from tools.stoneage_map06_two_original_scenes import need, placements, sha

FLOORS17 = (1403, 3103, 3203)
MAP09_PINS = {
    'map09_custody': ('STONEAGE-MAP09-PRIVATE-CUSTODY-R1.json', '5d6b591c659563aef24d93a30d314dd1d13b8d2c'),
    'map04': ('STONEAGE-MAP-SCENE-MODULE-04-955-ORIGINAL-DAT-4166-RD-PIXEL-INDEX-R1.json', '1ef8c004179128ea44ffa4fb4259748bc8c83911'),
}


def catalog_rooms(catalog, source, warps, retained, *, floors=FLOORS17):
    import numpy as np
    from PIL import Image

    from tools.stoneage_map09_batch_scenes import verified_frames
    from tools.stoneage_scene21_town1000 import render

    public = source['map09']
    model = catalog.read('dataset.js')
    prefix = b'window.MAP09_DATA='
    need(model.startswith(prefix) and model.endswith(b';\n'), 'MAP09 private dataset envelope')
    model = json.loads(model[len(prefix):-2])
    pixel_index = catalog.read('private-image-source-records.json')
    need(sha(pixel_index) == public['private_image_source_records_sha256'], 'MAP09 private tile metadata')
    pixel_index = json.loads(pixel_index)
    dat_archive = catalog.read('source-all-955-original-DAT.zip')
    dat_pin = public['original_DAT_archive']
    need((len(dat_archive), sha(dat_archive)) == (dat_pin['bytes'], dat_pin['sha256']), 'MAP09 inner DAT archive')
    names = {r[0]: r for r in source['map04']['per_floor_source_rows']}
    endpoint_floors = sorted(set(floors) | {p[0] for _, start, end, _ in warps for p in (start, end)})
    originals = {}
    with zipfile.ZipFile(io.BytesIO(dat_archive)) as dats:
        need(len(set(dats.namelist())) == len(dats.namelist()) == dat_pin['members']
             and dats.testzip() is None, 'MAP09 inner DAT CRC')
        for floor in endpoint_floors:
            name = f'{floor}.dat'
            dat = dats.read(name)
            need([len(dat), sha(dat)] == names[name][1:3], 'MAP04 original DAT: ' + name)
            originals[floor] = dat
            if floor not in floors:
                retained[f'maps/{floor}.dat'] = dat
    frames, room_replay = {}, {}
    images, records, arrays = {}, {}, {}
    for floor in floors:
        key = str(floor)
        dat = originals[floor]
        row = public['maps'][key]
        model_row = model['maps'][key]
        need(base64.b64decode(model_row['dat_base64'], validate=True) == dat
             and all(model_row[k] == v for k, v in row.items())
             and sha(dat) == row['source_sha256'], 'MAP09 original DAT and model: ' + key)
        info, selected = placements(dat)
        wanted = {p['image_key'] for p in selected}
        for tile in sorted(wanted - images.keys()):
            alias = str(tile)
            pin = pixel_index[alias]
            layout = model['records'][alias]
            need(all(layout[k] == pin[k] for k in ('width', 'height', 'xoff', 'yoff')),
                 'MAP09 source tile layout: ' + alias)
            raw = catalog.read(f'tiles/{alias}.png')
            with Image.open(io.BytesIO(raw)) as png:
                rgba = png.convert('RGBA')
            array = np.array(rgba)
            need(sha(raw) == pin['candidate_PNG_sha256'] and sha(rgba.tobytes()) == pin['candidate_RGBA_sha256']
                 and list(rgba.size) == [pin['width'], pin['height']]
                 and set(np.unique(array[:, :, 3])) <= {0, 255}, 'MAP09 original tile pixels: ' + alias)
            images[tile], records[tile], arrays[tile] = rgba, layout, array
        size, origin, hashes, _ = verified_frames(dat, info, selected, images, records, arrays)
        need((size, origin, hashes, len(selected), len(wanted)) ==
             (row['canvas_size'], row['origin'], row['frame_RGBA_sha256'], row['draw_positions'],
              row['unique_draw_aliases']), 'MAP09 all three original frame states: ' + key)
        png = render(images, records, selected, False, True, False, origin, size)
        need(sha(png.tobytes()) == hashes['combined'], 'private combined frame pixels: ' + key)
        stream = io.BytesIO()
        png.save(stream, 'PNG')
        frames[floor] = (dat, stream.getvalue())
        room_replay[floor] = dict(draw_positions=len(selected), image_aliases=sorted(wanted), frame_RGBA_sha256=hashes)
    return frames, originals, room_replay


def corroborate_warps(npc, source, warps, originals, retained):
    from tools.stoneage_scene14_independent_replay import source_blocks

    char = source['char']
    members = {r[0]: r[1:4] for r in char['source_files']}
    geometries = {f: dat_planes(raw) for f, raw in originals.items()}
    directions = {(start, end) for _, start, end, _ in warps}
    need(len(directions) == len(warps), 'duplicate original mapwarp direction')
    parsed, matched = {}, {}
    for row in char['create_rows']:
        path, ordinal, start_byte, end_byte, digest, floor = row[:6]
        if row[11] != 'npcgen_warp':
            continue
        if path not in parsed:
            raw = npc.read('npc/' + path)
            need(list(identity(raw).values()) == members[path], 'original Warp CREATE file: ' + path)
            parsed[path] = (raw, source_blocks(raw))
        raw, blocks = parsed[path]
        block = blocks[ordinal]
        fields = block['fields']
        args = fields[b'enemy'].split(b'|')
        if floor not in FLOORS17 and int(args[1]) not in FLOORS17:
            continue
        need(len(args) == 4 and args[0] == b'npcgen_warp', 'selected Warp CREATE arguments')
        target = tuple(map(int, args[1:]))
        start = point(fields)
        need(start == (floor, *row[7][:2])
             and block['start'] == start_byte and raw[block['end']:end_byte] in (b'\r\n', b'\n')
             and sha(raw[start_byte:end_byte]) == digest, 'original Warp CREATE byte span')
        edge = (start, target)
        need(edge not in matched, 'duplicate Warp CREATE direction')
        matched[edge] = [path, ordinal, digest]
        retained['npc/' + path] = raw
    need(set(matched) == directions, 'mapwarp and independent NPC CREATE direction sets')
    template_path, ordinal = 'genout/npcgen.template', 21
    key = 'npc/' + template_path
    raw = npc.read(key)
    need(list(identity(raw).values()) == members[template_path], 'original Warp template member')
    block = source_blocks(raw)[ordinal]
    tr = next(r for r in char['template_rows'] if r[:2] == [template_path, ordinal])
    tail = b'\r\n' if raw[block['end']:].startswith(b'\r\n') else b'\n'
    need(sha(raw[block['start']:block['end']] + tail) == tr[2]
         and block['fields'][b'templatename'] == b'npcgen_warp'
         and block['fields'][b'functionset'] == b'Warp', 'original Warp function template')
    retained[key] = raw
    return {
        (start, end): dict(warp_template=[template_path, ordinal, tr[2]], warp_create=matched[start, end],
                           reverse_listed=(end, start) in directions,
                           source_dat_u16=sample(geometries[start[0]], start[1:]),
                           target_dat_u16=sample(geometries[end[0]], end[1:]))
        for start, end in directions
    }
