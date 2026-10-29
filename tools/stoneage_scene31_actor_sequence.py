"""One authentic TW1 actor resource, action=2, eight full ordered sequences.

Private source rendering never executes the game. Public CI uses pinned derived
tables and a frozen pixel receipt only, never source sprites or original programs.
"""
import argparse
import base64
import csv
import functools
import gzip
import hashlib
import io
import json
from pathlib import Path
import struct
import zipfile

from tools.stoneage_scene23_body_visuals import PINS, BODY_SHA, WINDOW_SHA
from tools.stoneage_private_scene_actor_r7 import select_animations, resolve_bitmaps
from tools.stoneage_rd_codec import decode_rd_block
from tools.stoneage_scene29_tw10_battle_pet import alternate_rle
from tools.stoneage_tw10_palette import initial_rgb
from tools.stoneage_private_scene_palette_r3 import candidate_rgba

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'research/recovered/STONEAGE-SCENE31-ORIGINAL-ACTOR-SEQUENCE-R1.json'
META = ROOT / 'research/recovered/tw10-resource-metadata'
ZIP_SHA = '3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24'
DATASET_PINS = {
 'SPR-GROUP-R1.tsv.gz': '4db7809de4197eb90cca6dc04bda8550025e022c8232e2ebb902db0e9faf0175',
 'SPR-ANIMATION-R1.tsv.gz': '25f8039e6c6ca47d94289b269d5ff74a67fde999c6b6d4dbb08af297ddcaa567',
 'SPR-FRAME-R1.tsv.gz': '2bbfb2db4a866445085d98934fd475cbd72e034fe1155b2e17ae802ffdc5fe80',
 'ADRN-R1.tsv.gz': 'c8669789de1cc6e3575c2412ed86354a49c2b3e90cd2854c1e7b2fc71b0fe9ea',
}
PIXEL_RECEIPT_SHA = 'a8fd5030382f821875fa0f4ff40ead4a5e7303b716f090535c7388033bfd8a0f'
FALSE = ('original_world_entered', 'original_executable_executed', 'native_action_name_known',
 'native_fps_verified', 'native_palette_selection_verified', 'official_character_name_known',
 'original_character_selector_authenticated', 'source_action_run_executed', 'proprietary_pixels_in_git')

def need(ok, text):
    if not ok:
        raise ValueError(text)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()

@functools.lru_cache(maxsize=1)
def expected_sequences():
    tables = {}
    for name, expected in DATASET_PINS.items():
        data = (META / name).read_bytes()
        need(sha(data) == expected, 'pinned original-derived table changed: ' + name)
        with gzip.open(META / name, 'rt') as f:
            tables[name] = list(csv.DictReader(f, delimiter='\t'))
    groups = [r for r in tables['SPR-GROUP-R1.tsv.gz'] if int(r['spr_no']) == 100000]
    need(len(groups) == 1, 'unique actor resource')
    animations = [r for r in tables['SPR-ANIMATION-R1.tsv.gz']
                  if int(r['spr_no']) == 100000 and int(r['anim_no']) == 2]
    need(len(animations) == 8, 'eight unique directional animations')
    sequences = []
    for a in sorted(animations, key=lambda x: int(x['direction'])):
        fs = [f for f in tables['SPR-FRAME-R1.tsv.gz']
              if int(f['spr_no']) == 100000 and f['anim_index'] == a['anim_index']]
        fs.sort(key=lambda x: int(x['frame_index']))
        need([int(f['frame_index']) for f in fs] == list(range(6)), 'six ordered frame positions')
        frames = [[int(f[k]) for k in ('bmp_no', 'pos_x', 'pos_y', 'sound_no')] for f in fs]
        span = struct.pack('<HHII', int(a['direction']), 2, int(a['duration']), len(frames))
        span += b''.join(struct.pack('<IhhH', *f) for f in frames)
        sequences.append(dict(direction=int(a['direction']), action=2,
            source_animation_index=int(a['anim_index']), header_offset=int(a['offset']),
            end_offset=int(a['end_offset']), duration_word=int(a['duration']), frames=frames,
            source_animation_span_sha256=sha(span)))
    wanted = {f[0] for a in sequences for f in a['frames']}
    adr = {int(r['bitmapno']): r for r in tables['ADRN-R1.tsv.gz'] if int(r['bitmapno']) in wanted}
    need(len(adr) == len(wanted) == 48, 'all frame source bitmap records')
    return sequences, adr, groups[0]

def validate(r):
    need(r['schema'] == 'stoneage.scene31.original_actor_sequence.r1', 'schema')
    need(r['source_scope'] == 'ACCEPTED_TW1_RETAIL_BODY100000_ACTION2_ONLY', 'source scope')
    need(r['source_parent_zip_sha256'] == ZIP_SHA, 'original parent package identity')
    need(all(r[k] is False for k in FALSE), 'native identity/runtime/publishing boundary')
    need(r['source_action_run_id'] is None and r['overall_percent'] is None, 'no invented run or percent')
    need(r['source_files'] == {n: dict(bytes=p[0], sha256=p[1]) for n,p in PINS.items()}, 'same-build source pins')
    expected, adr, group = expected_sequences()
    need(r['sequences'] == expected, 'complete ordered original sequences')
    need(r['group_segment_sha256'] == group['segment_sha256'], 'original group identity')
    need((r['frame_occurrences'],r['distinct_bitmaps'],r['repeated_bitmap_positions']) == (48,48,0),
         'frame-position conservation')
    need(r['previous_scene23_first_frames_reused'] == 8 and r['further_frame_positions_observed'] == 40,
         'first-frame versus full-sequence evidence delta')
    rows = r['bitmaps']
    need(len(rows) == 48 and {b['bitmapno'] for b in rows} == set(adr), 'complete source pixel set')
    need(sha(canonical(rows)) == PIXEL_RECEIPT_SHA, 'immutable actual source pixel receipt')
    for b in rows:
        old = adr[b['bitmapno']]
        need([b[k] for k in ('source_adrn_index','offset','size','xoff','yoff','width','height')] ==
             [int(old[k]) for k in ('index','adder','size','xoff','yoff','width','height')], 'original pixel geometry')
        need(b['RD_sha256'] == old['rd_block_sha256'], 'original RD source identity')
    need(r['render_model'] == 'CANDIDATE_BOTTOM_UP_INDEX0_TRANSPARENT_TWO_SAP_INITIAL_RGB', 'candidate color/alpha scope')
    need(r['preview_frame_ms'] == 180 and r['source_duration_is_not_milliseconds'] is True, 'modern preview timing')
    return dict(directions=8,frame_positions=48,original_bitmaps=48,further_positions=40,original_world_entered=False)

def private_export(zip_path, out):
    from PIL import Image, ImageDraw
    out = out.resolve()
    need(out != ROOT and ROOT not in out.parents and not out.exists(), 'new private directory outside Git')
    with zip_path.open('rb') as f:
        need(hashlib.file_digest(f,'sha256').hexdigest() == ZIP_SHA, 'entire retained original package SHA')
    originals = {}
    with zipfile.ZipFile(zip_path) as z:
        for name,pin in PINS.items():
            path = 'source/' + (name if name.endswith('.exe') else 'data/pal/' + name if name.endswith('.sap') else 'data/' + name)
            raw = z.read(path)
            need((len(raw),sha(raw)) == pin, 'entire original source member: ' + name)
            originals[name] = raw
    need(sha(originals['sa_3.exe'][364072:364200]) == WINDOW_SHA, 'same original body candidate window')
    group = select_animations(originals['spradrn_1.bin'], originals['spr_1.bin'], (100000,), (2,))[0]
    sequences = sorted(group['animations'], key=lambda a:a['direction'])
    need(sequences == expected_sequences()[0], 'actual original SPR equals pinned complete sequence metadata')
    wanted = {f[0] for a in sequences for f in a['frames']}
    rows = resolve_bitmaps(originals['adrn_1.bin'], wanted, len(originals['real_1.bin']))
    rgb = {str(p):initial_rgb(originals['Palet_'+str(p)+'.sap']) for p in (0,1)}
    images = {'0':{},'1':{}}
    rd_subset = {}
    out.mkdir(mode=0o700, parents=True)
    for no,b in sorted(rows.items()):
        raw = originals['real_1.bin'][b['offset']:b['offset']+b['size']]
        header,indices = decode_rd_block(raw, authoritative_block_size=b['size'])
        need(indices == alternate_rle(raw,b['width'],b['height']), 'two actual RD decoders differ')
        need((header['width_s'],header['height_s']) == (b['width'],b['height']), 'original RD geometry')
        b.update(RD_sha256=sha(raw), indices_sha256=sha(indices), palette_candidates={})
        rd_subset[str(no)+'.rd'] = raw
        for p,colors in rgb.items():
            rgba = candidate_rgba(indices,b['width'],b['height'],colors)
            im = Image.frombytes('RGBA',(b['width'],b['height']),rgba)
            buf = io.BytesIO(); im.save(buf,format='PNG'); png = buf.getvalue()
            b['palette_candidates'][p] = dict(RGBA_sha256=sha(rgba),PNG_sha256=sha(png))
            images[p][str(no)] = base64.b64encode(png).decode()
    report = dict(schema='stoneage.scene31.original_actor_sequence.r1',
       source_scope='ACCEPTED_TW1_RETAIL_BODY100000_ACTION2_ONLY',source_parent_zip_sha256=ZIP_SHA,
       source_files={n:dict(bytes=p[0],sha256=p[1]) for n,p in PINS.items()},
       group_segment_sha256=group['whole_group_segment_sha256'],sequences=sequences,
       bitmaps=list(rows.values()),frame_occurrences=48,distinct_bitmaps=48,repeated_bitmap_positions=0,
       previous_scene23_first_frames_reused=8,further_frame_positions_observed=40,
       render_model='CANDIDATE_BOTTOM_UP_INDEX0_TRANSPARENT_TWO_SAP_INITIAL_RGB',
       preview_frame_ms=180,source_duration_is_not_milliseconds=True,
       source_action_run_id=None,overall_percent=None,**{k:False for k in FALSE})
    (out/'source-derived-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    with zipfile.ZipFile(out/'private-original-RD-and-palettes.zip','w',zipfile.ZIP_DEFLATED) as z:
        for n,raw in rd_subset.items(): z.writestr(n,raw)
        for p in (0,1): z.writestr('Palet_'+str(p)+'.sap', originals['Palet_'+str(p)+'.sap'])
    canvases=[]
    for palette in ('0','1'):
        sheet=Image.new('RGBA',(720,1080),'#142129')
        draw=ImageDraw.Draw(sheet)
        for a in sequences:
            for fi,(no,x,y,sound) in enumerate(a['frames']):
                b=rows[no];im=Image.open(io.BytesIO(base64.b64decode(images[palette][str(no)]))).convert('RGBA')
                c=Image.new('RGBA',(240,260),'#142129')
                xx,yy=120+2*(b['xoff']+x),200+2*(b['yoff']+y)
                need(0<=xx<=240-2*b['width'] and 0<=yy<=260-2*b['height'],'bounded full-frame placement')
                c.alpha_composite(im.resize((b['width']*2,b['height']*2),Image.Resampling.NEAREST),(xx,yy))
                canvases.append(dict(palette=palette,direction=a['direction'],frame_index=fi,bitmapno=no,RGBA_sha256=sha(c.tobytes())))
                sx,sy=fi*120,a['direction']*135
                sheet.alpha_composite(im,(sx+60+b['xoff']+x,sy+110+b['yoff']+y))
                draw.text((sx+5,sy+115),f"d{a['direction']} f{fi} #{no}",fill='#e6ce9b')
        sheet.save(out/f'SCENE31-48-original-frames-Palet{palette}-candidate.png')
    pack=dict(report=report,images=images,canvas_hashes=canvases)
    template=(ROOT/'tools/scene31-actor-sequence-observer.html').read_text()
    data=json.dumps(pack,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
    (out/'SCENE31-original-TW1-actor-observer.html').write_text(template.replace('PRIVATE_DATA_PLACEHOLDER',data))
    return report

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--original-zip',type=Path)
    ap.add_argument('--private-output',type=Path)
    args=ap.parse_args()
    if args.original_zip:
        need(args.private_output is not None,'private output required')
        r=private_export(args.original_zip,args.private_output)
        print(json.dumps({'private_export':'complete','pixel_receipt_sha256':sha(canonical(r['bitmaps']))}))
    else:
        print(json.dumps(validate(json.loads(REPORT.read_text()))))

if __name__=='__main__':
    main()
