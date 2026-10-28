"""Private pet-template numeric links and actual same-carrier sprite pixels.

Common archive membership and equal integers never establish a deployed build
or an official early species identity. Original payloads stay outside Git.
"""
from __future__ import annotations
import argparse,base64,copy,io,json,struct,zipfile
from pathlib import Path
from tools.stoneage_private_scene_actor_r7 import (
    ROOT,PINS,authenticate,select_animations,resolve_bitmaps,sha,need)
from tools.stoneage_rd_codec import decode_rd_block
from tools.stoneage_private_scene_palette_r3 import candidate_rgba
from tools.stoneage_tw10_palette import initial_rgb

PET_KEYS=(100250,100251,100252)
R7_HTML_SHA='ca449e14b2cbbea8fd48eb4f8acb27c00dcd0c9ae6d35c0152f5431b67e4842f'
R7_SOURCE_SHA='d2b38cba3b4722308ceaf3f39a6208b7b6f2298385e23b8eb4113fec53d8533b'
R7_RD_ZIP_SHA='68ebc210af090fcdef84a21153f7fbced981aed6206fc1f2a15ab55c3cd8c18d'
LINK_KIND='SAME_CARRIER_EQUAL_NUMERIC_KEY_ONLY_NOT_DEPLOYMENT_PROOF'
EVIDENCE={
 'STONEAGE-PRESERVED-PET-SPR-MATERIAL-R40.json':'a147e7fffdf6faac40ea947cd2e519518ff3342de905f985e624ff7cd98bcf06',
 'STONEAGE-PRESERVED-PET-SPR-SOURCE-R40.json':'076eeab6710d9a88bf36081da4ca0718c7cbb13d99aaf6f19dd9cb9c4baf75ea',
 'STONEAGE-PRESERVED-PET-TEMPLATE-SOURCE-R39.json':'09dc73e801f5020059812acb71b1db6d41e8987a3730ee2126348ee349a24d3b'}

def qualified_links():
    evidence={}
    for name,digest in EVIDENCE.items():
        raw=(ROOT/'research/recovered'/name).read_bytes()
        need(sha(raw)==digest,'immutable original-derived evidence: '+name)
        evidence[name]=json.loads(raw)
    material=evidence['STONEAGE-PRESERVED-PET-SPR-MATERIAL-R40.json']
    need(material['source_report_sha256']==EVIDENCE['STONEAGE-PRESERVED-PET-SPR-SOURCE-R40.json'] and
         material['server_source_sha256']==EVIDENCE['STONEAGE-PRESERVED-PET-TEMPLATE-SOURCE-R39.json'],
         'original server/client evidence chain')
    links=copy.deepcopy(material['server_occurrence_links'])
    need(len(links)==7 and {r['server_graphic_column_37'] for r in links}==set(PET_KEYS),
         'retain all seven original template occurrences')
    need(all(r['join_kind']==LINK_KIND for r in links),'numeric key link is not deployed-build proof')
    return links,evidence['STONEAGE-PRESERVED-PET-SPR-SOURCE-R40.json']['material']['selected_groups']

def pet_groups(index,spr):
    links,prior=qualified_links()
    groups=select_animations(index,spr,PET_KEYS,actions=(2,))
    for g in groups:
        old=[v for v in prior if v['spr_no']==g['spr_no']]
        need(len(old)==1,'unique original R40 group witness');old=old[0]
        need((g['source_group_index'],g['offset'],g['end_offset'],g['source_animation_count'],g['reserved_word'],g['whole_group_segment_sha256'])==
             (old['group_index'],old['offset'],old['end_offset'],old['anim_count'],old['reserved'],old['segment_sha256']),
             'actual original group versus complete R40 witness')
        # Re-encode every animation, including unselected actions and repeats.
        encoded=b''.join(struct.pack('<HHII',a['direction'],a['anim_no'],a['duration'],len(a['frames']))+
                          b''.join(struct.pack('<IhhH',*f) for f in a['frames']) for a in old['animations'])
        need(encoded==spr[g['offset']:g['end_offset']],'complete prior metadata versus actual original SPR')
        for a in g['animations']:
            b=old['animations'][a['source_animation_index']]
            need((a['direction'],a['action'],a['duration_word'],a['frames'])==
                 (b['direction'],b['anim_no'],b['duration'],b['frames']), 'exact selected source frame occurrences')
        g['available_source_action_codes']=sorted({a['anim_no'] for a in old['animations']})
        g['absent_source_action_codes']=[6]
        need(6 not in g['available_source_action_codes'],'no silent human-action fallback')
        g['template_links']=[r for r in links if r['server_graphic_column_37']==g['spr_no']]
        names={r['server_name'] for r in g['template_links']}
        need(len(names)==1,'ambiguous original template name')
        g['preserved_template_name']=next(iter(names))
    return groups,links

def export(source,r7_html,r7_rd_zip,target):
    from PIL import Image
    target=target.resolve()
    need(target!=ROOT and ROOT not in target.parents and not target.exists(),'new private output outside public Git required')
    prior_raw=r7_html.read_bytes();need(sha(prior_raw)==R7_HTML_SHA,'private R7 immutable identity')
    prior=json.loads(prior_raw.decode().split('<script id="evidence" type="application/json">')[1].split('</script>')[0])
    r7_source=(ROOT/'research/recovered/STONEAGE-SCENE07-ACTOR-SOURCE-R7.json').read_bytes()
    need(sha(r7_source)==R7_SOURCE_SHA and prior['actors']==json.loads(r7_source),'R7 actor metadata identity')
    for name,pin in PINS.items():authenticate(source/name,pin)
    groups,links=pet_groups((source/'spradrn_5.bin').read_bytes(),(source/'spr_4.bin').read_bytes())
    needed={f[0] for g in groups for a in g['animations'] for f in a['frames']}
    bitmaps=resolve_bitmaps((source/'adrn_15.bin').read_bytes(),needed,PINS['real_15.bin'][0])
    rgb=initial_rgb((source/'Palet_1.sap').read_bytes());images={};blocks={}
    with (source/'real_15.bin').open('rb') as real:
        for no,row in bitmaps.items():
            real.seek(row['offset']);raw=real.read(row['size']);need(len(raw)==row['size'],'short original RD read')
            header,pixels=decode_rd_block(raw,authoritative_block_size=row['size'])
            need((header['width_s'],header['height_s'])==(row['width'],row['height']),'same-carrier original ADRN/RD geometry')
            rgba=candidate_rgba(pixels,row['width'],row['height'],rgb)
            buf=io.BytesIO();Image.frombytes('RGBA',(row['width'],row['height']),rgba).save(buf,format='PNG');png=buf.getvalue()
            blocks[f'{no}.rd']=raw;images[str(no)]=base64.b64encode(png).decode()
            row.update(RD_sha256=sha(raw),RD_flag=header['flag'],index_pixels_sha256=sha(pixels),
                       candidate_RGBA_sha256=sha(rgba),PNG_sha256=sha(png))
    human=copy.deepcopy(prior['actors']['groups'][0]);need(human['spr_no']==100000,'fixed qualified human observer')
    human['animations']=[a for a in human['animations'] if a['action']==2]
    human_ids={f[0] for a in human['animations'] for f in a['frames']}
    human_bitmaps=[copy.deepcopy(r) for r in prior['actors']['bitmaps'] if r['bitmapno'] in human_ids]
    need(len(human_bitmaps)==len(human_ids)==48,'complete reused human source images')
    need(sha(r7_rd_zip.read_bytes())==R7_RD_ZIP_SHA,'private source RD custody from R7')
    with zipfile.ZipFile(r7_rd_zip) as archive:
        for row in human_bitmaps:
            no=row['bitmapno'];png=base64.b64decode(prior['actor_images'][str(no)],validate=True)
            need(sha(png)==row['PNG_sha256'],'reused human original PNG identity')
            raw=archive.read(f'{no}.rd');need(sha(raw)==row['RD_sha256'],'reused human source RD identity')
            images[str(no)]=prior['actor_images'][str(no)];blocks[f'{no}.rd']=raw
    for no,encoded in prior['room']['sprites'].items():
        png=base64.b64decode(encoded,validate=True);need(sha(png)==prior['room']['sprite_sha256'][no],'reused original room PNG identity')
        with Image.open(io.BytesIO(png)) as image:image.load()
    report={'schema':'stoneage.same_carrier_pet_observation.r8',
        'source_scope':'PRESERVED_MIXED25_NOT_OFFICIAL_TW1','source_files':{k:{'bytes':v[0],'sha256':v[1]} for k,v in PINS.items()},
        'prior_R7_html_sha256':R7_HTML_SHA,'prior_R7_source_report_sha256':R7_SOURCE_SHA,'evidence_sha256':EVIDENCE,
        'groups':groups,'template_links':links,'bitmaps':list(bitmaps.values()),
        'selected_animation_count':sum(len(g['animations']) for g in groups),
        'frame_occurrences':sum(len(a['frames']) for g in groups for a in g['animations']),
        'distinct_source_bitmaps':len(bitmaps),'human_reused':{'group':human,'bitmaps':human_bitmaps},
        'same_deployed_build_proven':False,'official_species_identity_authenticated':False,
        'original_world_entered':False,'original_client_launched_in_this_observation':False,
        'live_palette_verified':False,'native_actor_occlusion_verified':False,'native_fps_verified':False,
        'audio_events_played':False,'automatic_action_fallback':False,
        'actor_placement':'MODERN_MANUAL_OVERLAY_AFTER_ALL_MAP_PARTS','preview_frame_ms':180,
        'source_duration_word_is_not_milliseconds':True,'stage_a':'7_PARTIAL_2_OPEN',
        'stage_b':'GATED','r79':'PAUSED_NON_BLOCKING','overall_completion_percent':None}
    pack={'room':prior['room'],'actors':{'source_scope':report['source_scope'],'groups':[human]+groups,
        'bitmaps':human_bitmaps+list(bitmaps.values())},'actor_images':images,'pet_evidence':report}
    template=(ROOT/'tools/scene-room-pet-viewer-r8.html').read_text()
    need(template.count('"PRIVATE_PACK_PLACEHOLDER"')==1,'private template marker')
    html=template.replace('"PRIVATE_PACK_PLACEHOLDER"',json.dumps(pack,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c'))
    target.mkdir(mode=0o700,parents=True)
    (target/'stoneage-room-r8-pet-observer.html').write_text(html)
    (target/'source-derived-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    with zipfile.ZipFile(target/'private-source-rd-subset.zip','w',zipfile.ZIP_DEFLATED) as archive:
        for name,raw in blocks.items():archive.writestr(name,raw)
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source-dir',type=Path,required=True)
    p.add_argument('--r7-html',type=Path,required=True);p.add_argument('--r7-rd-zip',type=Path,required=True)
    p.add_argument('--output-dir',type=Path,required=True);a=p.parse_args();r=export(a.source_dir,a.r7_html,a.r7_rd_zip,a.output_dir)
    print(json.dumps({k:r[k] for k in ['schema','selected_animation_count','frame_occurrences','distinct_source_bitmaps','original_world_entered']}))
if __name__=='__main__':main()
