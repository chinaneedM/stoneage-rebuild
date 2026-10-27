"""Private actual-source palette/placement candidate, never an original game scene.

Reuses the retained mixed25 carrier and the exact R2 eight-image observation.
No network, original process, animation, NPC or audio is started by this tool.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import struct

from tools.stoneage_private_scene_source_r2 import BUNDLE_SHA, BUNDLE_SIZE, PREFIX
from tools.stoneage_private_scene_graphic_join_r1 import sha_file
from tools.stoneage_tw10_palette import initial_rgb

ROOT = Path(__file__).resolve().parents[1]
EXE_SHA = 'ec678517f76564ebc9ab00cf3f66853ed9975ef6290eb48168b78909a68a5d16'
EXE_BYTES = 561152
R2_SHA = 'da869a0921fe71970d547210f2d110c4fc643a950fb12a27273580660c7895c9'
PALETTE1_SHA = '32870080c47537a59beaf770b6df7bd79820fd52a23825058460900494f0b4b0'
LINEAGE_COMMIT = '999ffdf1d220ec6666eb65339180689c9caf1876'
LINEAGE = {
 'map.cpp': 'bd7ee7f1c60c30e372ad2dd5b0d30d1d0ef392fe',
 'sprmgr.cpp': 'dc0c906f31400fb1e4286acf754323f4ea961ad2',
 'sprmgr.h': 'd7e62956ebbc19d90706cbb8a839aa3a4afba3eb',
 'sprdisp.cpp': '666eb344f5a5c07265f7bfd4f8c8058bac66c157',
 'directdraw.cpp': 'dac379ee4b5c4d09b6249102f5a6fc4b2e28f728',
}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def pin_file(path, size, digest):
    require(path.is_file() and path.stat().st_size == size and sha_file(path) == digest,
            'private original source size/SHA conflict: ' + path.name)

def palette_program_witness(raw):
    require(len(raw) == EXE_BYTES and sha(raw) == EXE_SHA, 'unqualified preserved original program')
    pointers = struct.unpack_from('<16I', raw, 0x68288)
    names = []
    for pointer in pointers:
        offset = pointer - 0x400000
        require(0x65000 <= offset < 0x88000, 'palette pointer outside original data section')
        end = raw.find(b'\0', offset, offset+64)
        require(end >= 0, 'unterminated source palette path')
        names.append(raw[offset:end].decode('ascii'))
    expected = [f'data\\pal\\Palet_{i}.sap' for i in range(1,16)] + ['data\\pal\\Palet_0.sap']
    require(names == expected, 'original palette filename table differs')
    require(raw[0xb309:0xb30f] == bytes.fromhex('ff3588824600'), 'initial table-zero xref differs')
    require(raw[0xb318:0xb31d] == bytes.fromhex('bee19c4f00') and
            raw[0xb341:0xb349] == bytes.fromhex('81fe61a04f007cd4'), '224-entry original loop extent differs')
    return {
        'program_bytes': len(raw), 'program_sha256': sha(raw),
        'table_file_offset': 0x68288, 'table_va': 0x468288,
        'source_palette_filename_order': names,
        'initial_branch_palette_file': names[0], 'initial_selector': 0,
        'initial_branch_guard_required_zero_va': 0x4f9480,
        'blue_green_red_reads_per_entry': 3, 'loaded_slots_inclusive': [16,239],
        'loaded_bytes': (0x4fa061-0x4f9ce1)//4*3,
        'forced_black_slot_if_transmigration_guard_zero': 168,
        'native_static_spans': [
            {'file_start': a, 'file_end_exclusive': e, 'sha256': sha(raw[a:e])}
            for a,e in [(0x68288,0x682c8),(0xb2fc,0xb350),(0xb350,0xb36a),(0xb4cc,0xb4e2)]],
        'original_program_executed': False, 'runtime_branch_observed': False,
        'same_deployed_build_authenticated': False,
    }

def source_lineage(directory):
    report = []
    for name, expected in LINEAGE.items():
        b = (directory/name).read_bytes()
        blob = hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        require(blob == expected, 'lineage source Git blob conflict: '+name)
        report.append({'filename':name,'git_blob':blob,'bytes':len(b),'sha256':sha(b)})
    return report

def sweep(width, height):
    require(type(width) is int and type(height) is int and 1 <= width <= 64 and 1 <= height <= 64,
            'bounded source sweep required')
    ti, tj = height-1, 0
    out = []
    while ti >= 0:
        i, j = ti, tj
        while i >= 0 and j >= 0:
            out.append((j,i))
            i -= 1
            j -= 1
        if tj < width-1:
            tj += 1
        else:
            ti -= 1
    require(len(out) == width*height and len(set(out)) == len(out), 'source traversal coverage conflict')
    return out

def anchor(x, y):
    require(type(x) is int and type(y) is int, 'integer grid coordinates required')
    return (x+y)*32, (y-x)*24

def candidate_rgba(indices, width, height, rgb):
    """Descendant-source bottom-up and key-zero candidate; preserve index identity."""
    require(0 < width <= 8192 and 0 < height <= 8192 and width*height == len(indices) <= 8000000,
            'image extent mismatch')
    require(len(rgb) == 768, '256 RGB slots required')
    # These eight actual inputs do not use the source's 32 reserved RGB slots.
    # Do not inherit TW1 reserved colors silently if a future input uses them.
    require(all(n == 0 or 16 <= n <= 239 for n in indices),
            'reserved source color requires a separate native witness')
    result = bytearray()
    for y in range(height-1,-1,-1):
        for n in indices[y*width:(y+1)*width]:
            result.extend(rgb[n*3:n*3+3])
            result.append(0 if n == 0 else 255)
    return bytes(result)

def extract_palettes_and_program(carrier, output):
    import libarchive
    pin_file(carrier, BUNDLE_SIZE, BUNDLE_SHA)
    output.mkdir(mode=0o700)
    wanted = {PREFIX+'data/pal/Palet_'+str(i)+'.sap' for i in range(16)} | {PREFIX+'sa_2903.exe'}
    source_rows = []
    with libarchive.file_reader(str(carrier)) as archive:
        for e in archive:
            name = e.pathname.replace('\\','/')
            if name not in wanted:
                continue
            require(e.isfile and name not in {x['source_path'] for x in source_rows}, 'duplicate/non-file palette member')
            expected_size = EXE_BYTES if name.endswith('.exe') else 708
            require(e.size == expected_size, 'original member extent conflict')
            chunks, total = [], 0
            for block in e.get_blocks():
                total += len(block)
                require(total <= expected_size, 'original member decompression bound exceeded')
                chunks.append(block)
            raw = b''.join(chunks)
            require(len(raw) == expected_size, 'short original palette/program')
            (output/name.rsplit('/',1)[-1]).write_bytes(raw)
            source_rows.append({'source_path':name,'bytes':len(raw),'sha256':sha(raw)})
    require({x['source_path'] for x in source_rows} == wanted, 'fixed palette/program source members absent')
    # Cross-check every actual palette against the earlier independent carrier pair.
    pairs = json.loads((ROOT/'research/recovered/STONEAGE-TW85-PALETTE-SAME-CARRIER-R33.json').read_text())['original_palette_pairs_exact']
    expected = {x['palette_index']:x['sha256'] for x in pairs}
    for i in range(16):
        pin_file(output/f'Palet_{i}.sap',708,expected[i])
    pin_file(output/'sa_2903.exe',EXE_BYTES,EXE_SHA)
    return source_rows

def render(observation, palette_dir, lineage_dir, target):
    from PIL import Image, ImageDraw, ImageFont
    target = target.resolve()
    require(target != ROOT and ROOT not in target.parents and not target.exists(),
            'new private output outside public repository required')
    target.mkdir(mode=0o700)
    report_bytes = (ROOT/'research/recovered/STONEAGE-SCENE02-SOURCE-REAL-PIXELS-R2.json').read_bytes()
    require(sha(report_bytes) == R2_SHA, 'immutable R2 source report differs')
    source = json.loads(report_bytes)
    manifest = json.loads((observation/'source-manifest.json').read_text())
    require(manifest == source['observation'], 'private R2 manifest/source report differs')
    native = palette_program_witness((palette_dir/'sa_2903.exe').read_bytes())
    lineage = source_lineage(lineage_dir)
    sap = (palette_dir/'Palet_1.sap').read_bytes()
    require(len(sap) == 708 and sha(sap) == PALETTE1_SHA, 'selected source palette differs')
    rgb = initial_rgb(sap)
    adrn = (observation/'source-adrn_15.bin').read_bytes()
    mapraw = (observation/'source-map-1001.dat').read_bytes()
    require(sha(adrn) == manifest['source_adrn_sha256'] and sha(mapraw) == manifest['source_map_payload_sha256'],
            'R2 full source ADRN/DAT differs')
    width,height = struct.unpack_from('<II',mapraw)
    require((width,height) == (30,30) and len(mapraw) == 5408, 'fixed source map extent differs')
    planes = struct.unpack_from('<2700H',mapraw,8)
    sprites = {}; used = set(); witnesses = []
    from tools.stoneage_rd_codec import decode_rd_block
    for resource in manifest['resources']:
        require(resource['rendered_artwork'] and len(resource['occurrences']) == 1, 'unresolved source mapping')
        row = resource['occurrences'][0]
        record = adrn[row['index']*80:(row['index']+1)*80]
        require(sha(record) == row['source_record_sha256'], 'original ADRN record changed')
        block = (observation/(resource['filename']+'.rd')).read_bytes()
        require(sha(block) == resource['rd_block_sha256'], 'original RD differs')
        header,indices = decode_rd_block(block,authoritative_block_size=row['size'])
        require(sha(indices) == resource['decoded_palette_indices_sha256'], 'source index bytes differ')
        w,h = header['width_s'],header['height_s']
        require((w,h) == (row['width'],row['height']), 'source dimensions differ')
        png = Image.open(observation/resource['filename']);png.load()
        require(png.mode == 'L' and png.size == (w,h) and png.tobytes() == indices,
                'independent actual PNG/index comparison differs')
        used.update(indices)
        rgba = candidate_rgba(indices,w,h,rgb)
        sprites[resource['map_id']] = Image.frombytes('RGBA',(w,h),rgba)
        witnesses.append({'map_id':resource['map_id'],'bitmapno':row['bitmapno'],
            'rgba_after_candidate_bottom_up_sha256':sha(rgba),'rgba_size':[w,h]})
    by_id = {r['map_id']:r['occurrences'][0] for r in manifest['resources']}
    positions = []
    for layer in (0,1):
        for x,y in sweep(3,3):
            gx,gy = x+14,y+14
            n = planes[layer*900+gy*30+gx]
            if n <= 99:
                continue
            require(n in sprites, 'viewport references image outside fixed R2 set')
            row = by_id[n];ax,ay = anchor(x,y)
            positions.append({'plane':'tile' if layer == 0 else 'parts','grid':[gx,gy],
                'map_id':n,'bitmapno':row['bitmapno'],'anchor_relative':[ax,ay],
                'signed_ADRN_offset':[row['xoff'],row['yoff']],
                'top_left_relative':[ax+row['xoff'],ay+row['yoff']]})
    xmin = min(p['top_left_relative'][0] for p in positions)
    ymin = min(p['top_left_relative'][1] for p in positions)
    xmax = max(p['top_left_relative'][0]+sprites[p['map_id']].width for p in positions)
    ymax = max(p['top_left_relative'][1]+sprites[p['map_id']].height for p in positions)
    require(0 < xmax-xmin <= 1024 and 0 < ymax-ymin <= 1024, 'bounded candidate canvas exceeded')
    layers = [Image.new('RGBA',(xmax-xmin,ymax-ymin)),Image.new('RGBA',(xmax-xmin,ymax-ymin))]
    for p in positions:
        x,y = p['top_left_relative'];layers[p['plane']=='parts'].alpha_composite(sprites[p['map_id']],(x-xmin,y-ymin))
    result = layers[0].copy();result.alpha_composite(layers[1])
    for name,im in [('candidate-tile-layer.png',layers[0]),('candidate-parts-layer.png',layers[1]),('candidate-composite.png',result)]:
        im.save(target/name)
    sheet = Image.new('RGB',(1000,650),'#172027');draw = ImageDraw.Draw(sheet)
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
    small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',12)
    draw.text((24,18),'StoneAge | Actual source colors + source-lineage layout candidate',font=font,fill='white')
    draw.text((24,46),'Floor 1001 [14,14..16,16] | Native initial selector 0 -> Palet_1.sap | Not game footage',font=small,fill='#e9c483')
    for i,(title,im) in enumerate([('Tile plane: 9 source placements',layers[0]),('Tile + parts: 12 source placements',result)]):
        zoom = min(2,450//im.width,500//im.height)
        view = im.resize((im.width*zoom,im.height*zoom),Image.Resampling.NEAREST)
        x = i*500+(500-view.width)//2;y = 170
        sheet.paste(view,(x,y),view)
        draw.text((i*500+24,104),title,font=font,fill='white')
    draw.text((24,610),'Candidate: bottom-up rows, index-zero transparency, 32/24 projection, ground before parts.',font=small,fill='#b6c8d1')
    draw.text((24,632),'Runtime palette, camera, occlusion, same deployment and original-world entry remain OPEN.',font=small,fill='#e9c483')
    sheet.save(target/'stoneage-scene03-color-layout-candidate.png')
    report = {'schema':'stoneage.private_scene_palette_projection.r3','source_grade':'PRESERVED_MIXED25_NOT_OFFICIAL_TW1',
        'original_R2_source_report_sha256':R2_SHA,'palette_program_static_witness':native,
        'source_lineage_commit':LINEAGE_COMMIT,'source_lineage_files':lineage,
        'source_SAP1_sha256':sha(sap),'candidate_RGB_table_sha256':sha(rgb),
        'used_source_palette_slots':sorted(used),'reserved_slots_used_except_transparent_zero':[],
        'source_image_count':len(sprites),'placements':positions,
        'candidate_canvas_bounds_relative':[xmin,ymin,xmax,ymax],
        'rendering_policy':{'projection':'x=32*(gx+gy), y=24*(gy-gx), relative grid',
            'row_orientation':'BOTTOM_UP_DESCENDANT_SOURCE_CANDIDATE',
            'alpha':'INDEX_0_TRANSPARENT_DESCENDANT_SOURCE_CANDIDATE',
            'layer_order':'GROUND_FIRST_THEN_PARTS_IN_SOURCE_DIAGONAL_SWEEP',
            'palette_state':'INITIAL_BRANCH_CACHE_GUARD_ZERO_TRANSMIGRATION_ZERO_CANDIDATE'},
        'images':witnesses,'private_outputs':[
            {'filename':p.name,'bytes':p.stat().st_size,'sha256':sha_file(p)} for p in sorted(target.glob('*.png'))],
        'original_world_entered':False,'original_program_executed':False,'actual_runtime_palette_observed':False,
        'same_deployed_build_authenticated':False,'authentic_scene_rendered':False,
        'actual_visual_inspection_completed':False,'raw_originals_or_PNG_published_to_git':False}
    (target/'scene03-source-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    return report

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--carrier',type=Path,required=True)
    p.add_argument('--r2-observation-dir',type=Path,required=True)
    p.add_argument('--lineage-dir',type=Path,required=True)
    p.add_argument('--private-work',type=Path,required=True)
    a = p.parse_args();work = a.private_work.resolve()
    require(work != ROOT and ROOT not in work.parents and not work.exists(), 'new private work outside repository required')
    work.mkdir(mode=0o700)
    rows = extract_palettes_and_program(a.carrier,work/'original-palette-program')
    report = render(a.r2_observation_dir,work/'original-palette-program',a.lineage_dir,work/'preview')
    report['reused_carrier_sha256'] = BUNDLE_SHA
    report['acquired_private_members'] = rows
    report['new_original_network_download_bytes'] = 0
    (work/'source-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('PRIVATE_SCENE03_ACTUAL_SOURCE_PALETTE_PROJECTION_CANDIDATE=PASS; ORIGINAL_WORLD_ENTERED=FALSE')

if __name__ == '__main__':
    main()
