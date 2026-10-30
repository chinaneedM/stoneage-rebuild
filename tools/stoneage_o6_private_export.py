"""Export pinned PRIVATE StoneAge O5 original-resource observer to an engine-neutral pack.

Research only. No original game executable is started. Copyrighted PNG/text/output
MUST remain outside the public repo. No species names or native events inferred.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import struct
import zipfile

SCHEMA = 'stoneage.o6.private_source_bounded_scene_assets.r1'
O5_SHA = 'e2f6beb8789f1d755fe44bf6d3ba70f7bf6baf7cd713eb34cf47d18062aa5bc6'
O5_HTML_SHA = '2637ac0594ab3922b32fe3b6dd8819a173344933981feb7f5ffa6dc0d6816be7'
SOURCE_SCOPE = 'PRESERVED_MIXED25_COMMUNITY_MODIFIED_SOURCE_ONLY'
ROOM_DAT = '62dbef1614ede0ba032ca9c69cbfdc3d43938e45baba78701885790937b86b90'
TOWN_DAT = '94b19cb59d72b7b48da70d2741ba68516caad970297fd48ed11ef720fa3ea97e'
ROOM_KEYS = ('5000','5001','5002','5005','5007','5009','5015')
PNG_SIG = b'\x89PNG\r\n\x1a\n'
EXPECTED_GROUP_COUNTS = {100250: 72, 100251: 72, 100252: 208}
EXPECTED_BOUNDS = {1001: [7,12,13,18], 1000: [60,96,66,106]}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require(pred, msg):
    if not pred:
        raise ValueError(msg)


class EmbeddedJSON(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.current = None
        self.gather = []
        self.raw = {}

    def handle_starttag(self, tag, attrs):
        if tag != 'script': return
        a = dict(attrs)
        if a.get('type') == 'application/json' and a.get('id') in ('source','o5-data'):
            name = a['id']
            require(name not in self.raw and self.current is None, 'duplicate private JSON script')
            self.current = name
            self.gather = []

    def handle_data(self, data):
        if self.current is not None:
            self.gather.append(data)

    def handle_endtag(self, tag):
        if tag == 'script' and self.current is not None:
            self.raw[self.current] = ''.join(self.gather)
            self.current, self.gather = None, []


def parse_pinned_html(data: bytes):
    require(sha(data) == O5_HTML_SHA, 'unrecognized original O5 HTML identity')
    p = EmbeddedJSON()
    p.feed(data.decode('utf-8'))
    require(set(p.raw) == {'source','o5-data'}, 'missing source/pet private JSON payload')
    return json.loads(p.raw['source']), json.loads(p.raw['o5-data'])


def png(raw: bytes):
    require(raw.startswith(PNG_SIG) and raw[12:16] == b'IHDR' and len(raw)>33,
            'not an original PNG payload')
    w,h = struct.unpack('>II', raw[16:24])
    require(0 < w <= 2048 and 0 < h <= 2048, 'out of scope PNG dimensions')
    return [w,h]


def image_from_b64(data, expected=None, size=None):
    require(isinstance(data,str) and len(data)<5_000_000, 'unbounded image source')
    raw = base64.b64decode(data, validate=True)
    dims = png(raw)
    if expected is not None:
        require(sha(raw)==expected, 'original PNG SHA mismatch')
    if size is not None:
        require(dims==size, 'original PNG dimensions mismatch')
    return raw,dims


def validated_model(source, pet):
    a=source['r15']; town=source['r21']; npc=source['r22']; tw1=source['tw1']
    require(pet['provenance']==SOURCE_SCOPE,'preserved source profile mismatch')
    views=a['views'];require([v['floor'] for v in views]==[1001,1000],'unexpected source map floors')
    require(views[0]['source_DAT_sha256']==ROOM_DAT and views[1]['source_DAT_sha256']==TOWN_DAT,
            'original bounded map DAT provenance mismatch')
    require(views[0]['inclusive_viewport']==EXPECTED_BOUNDS[1001] and town['bounds']==EXPECTED_BOUNDS[1000],
            'source viewport/coordinate bounds drift')
    require(len(views[0]['placements'])==27 and len(views[1]['placements'])==54,
            'source placement membership drift')
    require(len(a['resources'])==len(a['images'])==51,'room original resource count mismatch')
    require(set(a['resources'])==set(a['images']),'room image key mismatch')
    require(all(k in a['images'] for k in ROOM_KEYS),'O5 shared original tile keys missing')
    require(len(town['images'])==8 and town['source_map_sha256']==TOWN_DAT,
            'town composite evidence drift')
    require(len(a['doorway_pair'])==2,'source original warp pair absent')
    require([(q['source_floor'],q['source_xy'],q['destination_floor'],q['destination_xy'])
             for q in a['doorway_pair']] == [(1001,[10,15],1000,[63,99]),(1000,[63,99],1001,[10,15])],
            'source-original manual warp tuple mismatch')
    require(npc['position']==[63,103] and npc['graphic_key']==16048
            and len(npc['text_sha256'])==64, 'original NPC documentary link drift')
    require(source['limits']['original_world_entered'] is False
            and source['limits']['official_TW1_map_authenticated'] is False,
            'native world source falsely certified')
    require(tw1['spr_no']==100000 and tw1['frame_count']==len(tw1['frames'])==7,
            'explicitly cross-version actor numeric reference mismatch')
    require(len(pet['groups'])==3 and len(pet['images'])==len(pet['image_png_sha256'])==208,
            'pet numeric source groups and image payload count drift')
    counts={}; all_frames=[]
    for group in pet['groups']:
        no=group['spr_no'];require(no in EXPECTED_GROUP_COUNTS and no not in counts,'pet numeric group identity conflict')
        animations=group['animations'];require(len(animations)==8,'pet original directions count mismatch')
        require([(x['direction'],x['action']) for x in animations]==[(i,0) for i in range(8)],
                'original direction/action code drift')
        seq=[frame[0] for anim in animations for frame in anim['frames']]
        counts[no]=len(seq);all_frames.extend(seq)
    require(counts==EXPECTED_GROUP_COUNTS and len(all_frames)==352 and len(set(all_frames))==208,
            'source frame occurrence/duplicate conservation drift')
    require(set(map(str,all_frames))==set(pet['images'])==set(pet['image_png_sha256']),
            'unreferenced or missing original bitmap payload')
    return a,town,npc,tw1


def export_private(source_zip:Path, dest:Path, public_repo:Path|None=None):
    source_zip=source_zip.expanduser().resolve()
    dest=dest.expanduser().resolve()
    require(source_zip.is_file() and dest.is_dir() and not dest.is_symlink(),
            'existing genuine private source ZIP / empty private output directory required')
    require(not any(dest.iterdir()),'refuse overwrite: output directory is not empty')
    require(source_zip not in dest.parents and dest not in source_zip.parents,'source/output path overlap')
    if public_repo is not None:
        repo=public_repo.expanduser().resolve()
        require(dest!=repo and repo not in dest.parents,'do not export copyrighted assets into public repo')
    require(sha(source_zip.read_bytes())==O5_SHA,'O5 original private archive whole-file SHA mismatch')
    with zipfile.ZipFile(source_zip) as z:
        require(z.testzip() is None,'original package CRC failure')
        require('index.html' in z.namelist(),'private original observer missing')
        source,pet=parse_pinned_html(z.read('index.html'))
    a,town,npc,tw1=validated_model(source,pet)
    plan=[]
    def add(path, data, expected=None, size=None):
        raw,dims=image_from_b64(data, expected=expected, size=size)
        plan.append((path,raw,sha(raw),dims))
        return {'path':path,'sha256':sha(raw),'width':dims[0],'height':dims[1]}
    room={}
    for key in sorted(a['images'],key=int):
        meta=a['resources'][key]
        room[key]=add(f'images/room1001/{key}.png',a['images'][key],
                      expected=meta['PNG_sha256'],size=[meta['width'],meta['height']])
    town_imgs={}
    for key,data in sorted(town['images'].items()):
        require(re.fullmatch(r'(?:expanded|old)_parts[01]_npc[01]',key) is not None,
                'unexpected town composite key')
        town_imgs[key]=add(f'images/town1000/{key}.png',data,size=town['canvas_size'])
    pet_imgs={}
    for key in sorted(pet['images'],key=int):
        pet_imgs[key]=add(f'images/pet_figure/{key}.png',pet['images'][key],pet['image_png_sha256'][key])
    actor_imgs=[add(f'images/tw1_separate_actor/{i:03}.png',s) for i,s in enumerate(tw1['frames'])]
    human=add('images/saved_mixed25_actor_reference.png',a['human_image'])
    require(len(plan)==275,'exported PNG count and category isolation drift')
    scene1001={
       'status':'SOURCE_POSITION_COMPOSITE_VIEW_NOT_ORIGINAL_ENGINE',
       'floor':1001,'version':'PRESERVED_MIXED25_COMMUNITY_MODIFIED',
       'source_DAT_sha256':ROOM_DAT,'bounds':views_bounds(a['views'][0]),
       'placements':a['views'][0]['placements'],'image_resources':room,
       'manual_warp_source_tuples':a['doorway_pair']}
    scene1000={
       'status':'BOUNDED_PRIVATE_SOURCE_COMPOSITES_NOT_FULL_WORLD_TILES',
       'floor':1000,'version':'PRESERVED_MIXED25_COMMUNITY_MODIFIED',
       'source_DAT_sha256':TOWN_DAT,'bounds':town['bounds'],
       'composite_origin':town['origin'],'composite_canvas_size':town['canvas_size'],
       'source_composite_images':town_imgs,'source_original_NPC_cell_u16':town['source_NPC_cell_original_three_u16'],
       'NPC_document':{'position':npc['position'],'graphic_key':npc['graphic_key'],
                       'source_message_sha256':npc['text_sha256'],'native_dialogue_executed':False},
       'manual_warp_source_tuples':a['doorway_pair']}
    pet_manifest={'status':'ORIGINAL_SPR_NUMERIC_TIMELINE_NOT_SPECIES_OR_SPAWN',
                  'version':'PRESERVED_MIXED25_COMMUNITY_MODIFIED',
                  'groups':pet['groups'],'bitmap_images':pet_imgs,'source_frame_occurrences':352,
                  'distinct_images':208,'historical_duration_unit':'UNKNOWN'}
    manifest={'schema':SCHEMA,'input_O5_zip_sha256':O5_SHA,'input_O5_html_sha256':O5_HTML_SHA,
             'source_scope':SOURCE_SCOPE,'phase':'HISTORICAL_SOURCE_ASSET_OBSERVATION_NOT_NEW_GAME',
             'sources':{'scene1001':'scene-1001.json','scene1000':'scene-1000.json',
                        'pet_numeric_timeline':'pet-numeric-timeline.json'},
             'original_PNGs_exported':len(plan),'original_PNGs_by_class':{'room1001':51,'town1000_composites':8,
              'pet_figure':208,'crossversion_TW1_actor_positions':7,'mixed25_actor_reference':1},
             'original_PNGs_sha256':[{'path':p,'sha256':h,'size':dims} for p,_,h,dims in plan],
             'optional_crossversion_actor':{'source':'TW1_RETAIL_NOT_SAME_BUILD_WORLD',
                 'numeric_spr':100000,'direction':tw1['direction'],'action':tw1['action_code'],
                 'frames':actor_imgs},
             'same_saved_version_actor_reference':human,
             'unproven':{'official_TW1_map_deployment':True,'species_names_and_entity_binding':True,
                 'original_client_executable_gameplay':True,'native_collision':True,
                 'native_pet_spawns':True,'native_warp_and_npc_runtime':True,'historical_frame_time':True,
                 'original_palette_and_occlusion':True,'rights_to_redistribute':True},
             'network_access_or_legacy_executable_used':False}
    files={'manifest.json':manifest,'scene-1001.json':scene1001,'scene-1000.json':scene1000,
           'pet-numeric-timeline.json':pet_manifest}
    # All bytes validated before any output. Emit only under pre-existing private folder.
    for p,raw,_,_ in plan:
        target=dest/p;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
    for name,obj in files.items():
        (dest/name).write_text(json.dumps(obj,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    # Verify all files from disk and prove complete timeline without normalization.
    for path,raw,hash_,_ in plan:
        require(sha((dest/path).read_bytes())==hash_,'exported source PNG not reproduced')
    return manifest


def views_bounds(view):
    return view['inclusive_viewport']


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--private-o5-zip',required=True,type=Path)
    p.add_argument('--output-dir',required=True,type=Path)
    p.add_argument('--public-repo-root',type=Path,default=Path(__file__).resolve().parents[1])
    a=p.parse_args()
    m=export_private(a.private_o5_zip,a.output_dir,a.public_repo_root)
    print(json.dumps({'O6_PRIVATE_EXPORT':'PASS','schema':m['schema'],
          'original_pngs':m['original_PNGs_exported'],'source_scope':m['source_scope'],
          'original_game_world_entered':False,'output_dir':str(a.output_dir)},ensure_ascii=False))


if __name__=='__main__':
    main()