"""Finite private action0 pixel export and source-safe historical replay.
Original RD/PNG/HTML stay outside Git. Offline CI does not read source pixels.
"""
from __future__ import annotations
import argparse, base64, copy, hashlib, io, json, re, zipfile
from pathlib import Path
from tools.stoneage_private_scene_actor_r7 import (ROOT, PINS, authenticate, select_animations, resolve_bitmaps, need, sha)
from tools.stoneage_private_scene_pet_r8 import qualified_links
from tools.stoneage_rd_codec import decode_rd_block
from tools.stoneage_private_scene_palette_r3 import candidate_rgba
from tools.stoneage_tw10_palette import initial_rgb

KEYS=(100250,100251,100252)
PRIOR_SHA='edf6c438803d1d4a1ab388aebe2ad17df7000b9a80883e9f95d27fea670e9996'
SOURCE='STONEAGE-PRESERVED-PET-SPR-SOURCE-R40.json'
SOURCE_SHA='076eeab6710d9a88bf36081da4ca0718c7cbb13d99aaf6f19dd9cb9c4baf75ea'
PIXEL_METADATA_SHA='b3075c5d553640a4acc810880782f9361353f96d78e8bc539a95f391bfb3706b'
REPORT=ROOT/'research/recovered/STONEAGE-SCENE13-PET-ACTION0-R1.json'
FALSE_FLAGS=('official_species_identity_authenticated','same_deployed_build_proven',
 'original_world_entered','native_frame_rate_verified','native_actor_occlusion_verified',
 'live_palette_verified','original_client_executed','proprietary_pixels_published')

def original():
    raw=(ROOT/'research/recovered'/SOURCE).read_bytes()
    need(sha(raw)==SOURCE_SHA,'immutable R40 complete source metadata')
    return json.loads(raw)['material']['selected_groups']

def public_summary(groups, rows):
    result=[]
    for g in groups:
        anim=g['animations'];ids=[f[0] for a in anim for f in a['frames']]
        result.append({'graphic':g['spr_no'],'group_index':g['source_group_index'],
          'full_segment_sha256':g['whole_group_segment_sha256'],
          'animations':copy.deepcopy(anim),'frame_occurrences':len(ids),
          'distinct_bitmaps':len(set(ids)),'repeated_positions':len(ids)-len(set(ids)),
          'direction_patterns':[[list(dict.fromkeys(f[0] for f in a['frames'])).index(f[0])
                                 for f in a['frames']] for a in anim]})
    return {'schema':'stoneage.scene13.actual_pet_action0.r1',
      'scope':'PRESERVED_MIXED25_NOT_AUTHENTICATED_OFFICIAL_TW1',
      'source_R40_sha256':SOURCE_SHA,'private_prior_html_sha256':PRIOR_SHA,
      'source_files':{k:{'bytes':v[0],'sha256':v[1]} for k,v in PINS.items()},
      'action':0,'animation_count':24,'groups':result,'bitmaps':rows,
      'frame_occurrences':sum(g['frame_occurrences'] for g in result),
      'distinct_pet_bitmaps':len(rows),
      'repeated_positions':sum(g['repeated_positions'] for g in result),
      'timing':'SOURCE_DURATION_WORDS_RETAINED_NOT_MILLISECONDS',
      'draw_order':'MODERN_MANUAL_ACTORS_AFTER_MAP_NO_R9_WITNESS_REUSE',
      **{k:False for k in FALSE_FLAGS},'overall_completion_percent':None}

def validate(r):
    need(r['schema']=='stoneage.scene13.actual_pet_action0.r1','schema')
    need(r['scope']=='PRESERVED_MIXED25_NOT_AUTHENTICATED_OFFICIAL_TW1','scope')
    need(r['source_R40_sha256']==SOURCE_SHA and r['private_prior_html_sha256']==PRIOR_SHA,'source chain')
    need(r['source_files']=={k:{'bytes':v[0],'sha256':v[1]} for k,v in PINS.items()},'same-carrier full file identities')
    need(type(r['action']) is int and r['action']==0 and r['animation_count']==24,'bounded action')
    old={g['spr_no']:g for g in original()};need([g['graphic'] for g in r['groups']]==list(KEYS),'three fixed graphics')
    all_ids=[]
    for g in r['groups']:
        o=old[g['graphic']]; expected=[a for a in o['animations'] if a['anim_no']==0]
        need(g['group_index']==o['group_index'] and g['full_segment_sha256']==o['segment_sha256'],'whole original SPR segment')
        need(len(g['animations'])==8,'eight original direction occurrences')
        ids=[];patterns=[]
        for a,b in zip(g['animations'],expected):
            need(a['direction']==b['direction'] and a['action']==b['anim_no'] and a['duration_word']==b['duration'] and a['frames']==b['frames'],'exact original SPR occurrences, offsets, sound words')
            need(a['source_animation_index']==o['animations'].index(b),'original animation position')
            need(a['header_offset']==o['offset']+sum(12+10*len(v['frames']) for v in o['animations'][:a['source_animation_index']]),'source header offset')
            need(a['end_offset']==a['header_offset']+12+10*len(a['frames']),'source end offset')
            import struct
            raw=struct.pack('<HHII',b['direction'],b['anim_no'],b['duration'],len(b['frames']))+b''.join(struct.pack('<IhhH',*f) for f in b['frames'])
            need(sha(raw)==a['source_animation_span_sha256'],'source span digest')
            keys=[f[0] for f in a['frames']];ids+=keys
            patterns.append([list(dict.fromkeys(keys)).index(n) for n in keys])
        need((g['frame_occurrences'],g['distinct_bitmaps'],g['repeated_positions'])==(len(ids),len(set(ids)),len(ids)-len(set(ids))),'frame multiplicity')
        need(g['direction_patterns']==patterns,'do not collapse repeated frames')
        all_ids+=ids
    rows=r['bitmaps'];need(sha(json.dumps(rows,sort_keys=True,separators=(',',':')).encode())==PIXEL_METADATA_SHA,'immutable private-derived pixel metadata; offline CI does not decode originals')
    need(len(rows)==len({b['bitmapno'] for b in rows})==len(set(all_ids)) and {b['bitmapno'] for b in rows}==set(all_ids),'all and only original action0 pixels')
    for b in rows:
        need(all(type(b[k]) is int for k in ['bitmapno','width','height','offset','size','source_adrn_index','visible_pixels']),'integer fields')
        need(0<b['width']<=1024 and 0<b['height']<=1024 and 0<=b['visible_pixels']<=b['width']*b['height'],'pixel extent')
        need(0<=b['source_adrn_index']<PINS['adrn_15.bin'][0]//80 and 16<=b['size']<=1000000 and 0<=b['offset']<=PINS['real_15.bin'][0]-b['size'],'RD source extent')
        for k in ['record_sha256','RD_sha256','index_pixels_sha256','candidate_RGBA_sha256','PNG_sha256']:
            need(isinstance(b[k],str) and re.fullmatch('[0-9a-f]{64}',b[k]) is not None,'digest '+k)
    need((r['frame_occurrences'],r['distinct_pet_bitmaps'],r['repeated_positions'])==(len(all_ids),len(rows),len(all_ids)-len(rows)),'total conservation')
    need(r['timing']=='SOURCE_DURATION_WORDS_RETAINED_NOT_MILLISECONDS','no invented FPS')
    need(r['draw_order']=='MODERN_MANUAL_ACTORS_AFTER_MAP_NO_R9_WITNESS_REUSE','new action has no controlled order witness')
    need(all(r[k] is False for k in FALSE_FLAGS) and r['overall_completion_percent'] is None,'historical boundaries')
    return {'animations':24,'frame_occurrences':len(all_ids),'distinct_bitmaps':len(rows),'repeated_positions':r['repeated_positions'],'source_pixels_read_in_offline_CI':False}

def validate_acceptance(a,r):
    need(a['schema']=='stoneage.scene13.actual_source_and_browser_acceptance.r1','acceptance schema')
    need(a['private_source_report_sha256']==sha(REPORT.read_bytes()),'source report digest')
    need(a['actual_loaded_images']==266 and a['canvas_width']==960 and a['canvas_height']==720 and a['rgba_pixels_per_frame']==691200,'real browser image and canvas extent')
    need(a['actual_frame_states_checked']==352 and a['independent_RD_index_RGBA_PNG_checks']==208 and a['all_browser_RGBA_canvas_hashes_equal_independent_Pillow'] is True,'independent real pixel checks')
    expected=[(g['graphic'],v['direction'],i,f[0]) for g in r['groups'] for v in g['animations'] for i,f in enumerate(v['frames'])]
    need([(v['pet'],v['direction'],v['frame'],v['bitmap']) for v in a['frame_hashes']]==expected,'complete original frame-state occurrences')
    need(all(re.fullmatch('[0-9a-f]{64}',v['canvas_sha256']) for v in a['frame_hashes']),'canvas hash')
    need(a['js_errors']==a['external_requests']==0,'browser errors or network')
    need(a['original_world_entered'] is False and a['public_CI_reads_private_pixels'] is False and a['source_ci_run_id'] is None and a['overall_completion_percent'] is None,'local source run is not public CI or gameplay')
    return {'actual_source_bitmaps':208,'browser_canvas_states':352,'local_independent_pixel_comparison':True,'public_CI_reads_private_pixels':False}

def export(source, prior, target):
    from PIL import Image
    target=target.resolve();need(target!=ROOT and ROOT not in target.parents and not target.exists(),'new private output outside Git')
    raw=prior.read_bytes();need(len(raw)==1151954 and sha(raw)==PRIOR_SHA,'private R12 identity')
    pack=json.loads(raw.split(b'<script id="evidence" type="application/json">')[1].split(b'</script>')[0])
    for name,pin in PINS.items():authenticate(source/name,pin)
    groups=select_animations((source/'spradrn_5.bin').read_bytes(),(source/'spr_4.bin').read_bytes(),KEYS,(0,))
    ids={f[0] for g in groups for a in g['animations'] for f in a['frames']}
    rows=resolve_bitmaps((source/'adrn_15.bin').read_bytes(),ids,PINS['real_15.bin'][0])
    rgb=initial_rgb((source/'Palet_1.sap').read_bytes());images={};blocks={}
    with (source/'real_15.bin').open('rb') as real:
        for n,b in sorted(rows.items()):
            real.seek(b['offset']);rd=real.read(b['size']);need(len(rd)==b['size'],'short RD')
            h,px=decode_rd_block(rd,authoritative_block_size=b['size'])
            need((h['width_s'],h['height_s'])==(b['width'],b['height']),'RD versus original ADRN geometry')
            rgba=candidate_rgba(px,b['width'],b['height'],rgb)
            im=Image.frombytes('RGBA',(b['width'],b['height']),rgba);buf=io.BytesIO();im.save(buf,format='PNG');png=buf.getvalue()
            b.update(RD_sha256=sha(rd),index_pixels_sha256=sha(px),candidate_RGBA_sha256=sha(rgba),PNG_sha256=sha(png),visible_pixels=sum(v!=0 for v in rgba[3::4]))
            images[str(n)]=base64.b64encode(png).decode();blocks[str(n)+'.rd']=rd
    report=public_summary(groups,[rows[n] for n in sorted(rows)]);validate(report)
    links,_=qualified_links()
    for g in groups:
        g['template_links']=[x for x in links if x['server_graphic_column_37']==g['spr_no']]
        names={x['server_name'] for x in g['template_links']};need(len(names)==1,'template name ambiguity')
        g['preserved_template_name']=next(iter(names));g['available_source_action_codes']=[0];g['absent_source_action_codes']=[6]
    human=copy.deepcopy(pack['actors']['groups'][0]);human['animations']=[a for a in human['animations'] if a['action']==2]
    human_ids={f[0] for a in human['animations'] for f in a['frames']}
    human_rows=[b for b in pack['actors']['bitmaps'] if b['bitmapno'] in human_ids]
    need(len(human_rows)==48,'qualified human reference')
    for b in human_rows:
        png=base64.b64decode(pack['actor_images'][str(b['bitmapno'])],validate=True)
        need(sha(png)==b['PNG_sha256'],'prior human PNG SHA');images[str(b['bitmapno'])]=base64.b64encode(png).decode()
    new={'room':pack['room'],'actors':{'source_scope':report['scope'],'groups':[human]+groups,'bitmaps':human_rows+report['bitmaps']},'actor_images':images}
    template=(ROOT/'tools/scene-room-action0-viewer-r13.html').read_text();need(template.count('"PRIVATE_PACK_PLACEHOLDER"')==1,'template marker')
    html=template.replace('"PRIVATE_PACK_PLACEHOLDER"',json.dumps(new,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c'))
    target.mkdir(parents=True,mode=0o700)
    (target/'stoneage-room-r13-action0-observer.html').write_text(html)
    (target/'source-derived-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    with zipfile.ZipFile(target/'private-original-rd-subset.zip','w',zipfile.ZIP_DEFLATED) as z:
        for name,b in blocks.items():z.writestr(name,b)
    (target/'private-palette.sap').write_bytes((source/'Palet_1.sap').read_bytes())
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source-dir',type=Path);p.add_argument('--prior-html',type=Path);p.add_argument('--output-dir',type=Path);a=p.parse_args()
    if a.source_dir:
        need(a.prior_html and a.output_dir,'private input and output required');r=export(a.source_dir,a.prior_html,a.output_dir)
    else:r=json.loads(REPORT.read_bytes())
    result=validate(r)
    if not a.source_dir:result['archived_acceptance']=validate_acceptance(json.loads((ROOT/'research/recovered/STONEAGE-SCENE13-PIXEL-ACCEPTANCE-R1.json').read_bytes()),r)
    print(json.dumps(result))
if __name__=='__main__':main()
