"""Static dream-cave source extraction; never interpret flags as executed rules."""
import argparse
from collections import Counter
import html
import json
from pathlib import Path
import re
import zlib
from tools.stoneage_quest08_mining_source import load_private_source, sha, blob, events, ROOT, SOURCE

REPORT = ROOT/'research/recovered/STONEAGE-QUEST09-DREAM-CAVE-ORIGINAL-CONTROLS-R1.json'
GUIDE = ROOT/'research/recovered/STONEAGE-CN2003-DREAM-CAVE-SOURCE-R1.json'
ENEMIES = ROOT/'research/recovered/STONEAGE-CHARACTER-NPC-MODULE-09-ORIGINAL-NPCENEMY-ROSTER-BRIDGE-R1.json'
MAPS = ROOT/'research/recovered/STONEAGE-QUEST05-598-ORIGINAL-CREATE-FLOOR-MAP-AND-WARP-CROSSWALK-R1.json'
CREATE_FILES = ['seimu/event/event01.create','400/sb_mugen.create',
                'genout/mugendungeon.create','genout/mugendungeon2.create']
SCRIPTS = ['seimu/event/event01_1','seimu/event/event01_2']


def event_controls(raw):
    rows = events(raw)
    for row in rows:
        segment = raw[row['start_byte']:row['end_byte']]
        row['extra_controls'] = []
        for key, value in re.findall(rb'(?m)^(GetRandItem|EndSetFlg):([^\r\n]*)', segment):
            values = [int(v) for v in value.split(b',')]
            row['extra_controls'].append({'name':key.decode(), 'values_in_source_order':values})
    return rows


def create_controls(raw):
    """Only numeric configuration and template tokens leave the private source."""
    fields = dict(re.findall(rb'(?m)^([A-Za-z]+)=([^\r\n]*)', raw))
    out = {'time_raw':int(fields[b'time'])}
    enemy = fields[b'enemy'].decode('ascii')
    parts = enemy.split('|')
    if parts[0]=='npcgen_warp':
        if len(parts) not in (4,5):
            raise ValueError('Unexpected original warp operand count')
        out['target_floor_x_y'] = [int(x) for x in parts[1:4]]
        out['trailing_token'] = parts[4] if len(parts)==5 else None
    return out


def extract(source_zip):
    archive_raw, source, data = load_private_source(source_zip)
    rows = [r for r in source['create_rows'] if r[0] in CREATE_FILES]
    if len(rows)!=117:
        raise ValueError('Unexpected complete source CREATE population')
    selected = {p:data[p] for p in CREATE_FILES+SCRIPTS}
    creates = []
    for row in rows:
        segment = data[row[0]][row[2]:row[3]]
        if sha(segment)!=row[4]:
            raise ValueError('Original CREATE slice mismatch')
        for path, _ordinal in row[13]:
            selected[path]=data[path]
        for path, _resolution, target_sha in row[15]:
            if sha(data[path])!=target_sha:
                raise ValueError('Original parameter identity mismatch')
            selected[path]=data[path]
        creates.append({'file':row[0], 'ordinal':row[1], 'start_byte':row[2], 'end_byte':row[3],
                        'block_sha256':row[4], 'floor':row[5], 'graphic_alias':row[6],
                        'borncorner_raw':row[7], 'borncenter_raw':row[8], 'direction_raw':row[10],
                        'template_token':row[11], 'parameter_references':row[15],
                        **create_controls(segment)})
    scripts = [{'path':p, 'sha256':sha(data[p]), 'events':event_controls(data[p])} for p in SCRIPTS]
    argument_paths = ['400/sb_muge1.arg','400/sb_muge2.arg']
    arguments = []
    for path in argument_paths:
        fields = dict(re.findall(rb'(?m)^([A-Za-z]+):([^\r\n]*)',data[path]))
        arguments.append({'path':path, 'sha256':sha(data[path]),
                          'entype_raw':int(fields[b'entype']), 'dieact_raw':int(fields[b'dieact']),
                          'warp_floor_x_y':[int(fields[k]) for k in [b'warpfl',b'warpx',b'warpy']],
                          'enemy_instance_ids_in_source_order':[int(x) for x in fields[b'enemyno'].split(b',')]})
    time_params=[]
    for path in sorted(selected):
        if path.startswith('genout/tman_'):
            fields=dict(re.findall(rb'(?m)^(time|change_no):([^\r\n]*)',data[path]))
            time_params.append({'path':path,'sha256':sha(data[path]),'time_raw':fields[b'time'].decode(),
                                'change_graphic_alias_raw':int(fields[b'change_no'])})
    item_ids={19550,2603,2604,2605,2606}
    for script in scripts:
        for event in script['events']:
            item_ids.update(c['item_id'] for c in event['commands'])
            for extra in event['extra_controls']:
                if extra['name']=='GetRandItem':item_ids.update(extra['values_in_source_order'])
    item_rows=[]
    item_pins={}
    for path in sorted((ROOT/'research/recovered/item-module-01').glob('*DERIVED-INDEX-*-R1.json')):
        shard=json.loads(path.read_text());matches=[r for r in shard['rows'] if r[0] in item_ids]
        if matches:
            item_rows.extend(matches);item_pins[path.relative_to(ROOT).as_posix()]=blob(path.read_bytes())
    enemies=json.loads(ENEMIES.read_text())
    enemy_ids={x for a in arguments for x in a['enemy_instance_ids_in_source_order']}
    enemy_rows=[r for r in enemies['source_enemy_number_to_paired_template_and_spr'] if r[0] in enemy_ids]
    guide=json.loads(GUIDE.read_text())['extraction']
    source_files=[]
    for path,raw in sorted(selected.items()):
        if raw.decode('cp950').encode('cp950')!=raw:raise ValueError('Non-reversible source text')
        source_files.append({'path':path,'bytes':len(raw),'sha256':sha(raw),'crc32':f'{zlib.crc32(raw):08x}'})
    warps=[r for r in creates if 'target_floor_x_y' in r]
    duplicates=[{'block_sha256':h,'occurrences':n} for h,n in Counter(r['block_sha256'] for r in warps).items() if n>1]
    report={'schema':'stoneage.quest09.dream_cave_original_static_controls.r1', 'date':'2026-11-08',
            'origin_class':'ORIGIN_UNRESOLVED',
            'source_scope':'LATER_COMMUNITY_MIXED25_NOT_AUTHENTICATED_OFFICIAL_DEPLOYMENT',
            'baseline':{'head':'ac06bc95cc6f572f7c7a866d024ac722dd5e49c1',
                        'tree':'947f5d08f43e5f188e503b373c0ed683f665f0f2',
                        'preserved_current_blob':'c89e0e33537990aa2132b47c40fef49a985a935c'},
            'private_source_zip':{'bytes':len(archive_raw),'sha256':sha(archive_raw),'verified_members':len(data),
                                  'verified_member_bytes':sum(map(len,data.values()))},
            'parent_rar_sha256':source['original_rar_sha256'],
            'derived_input_blobs':{**{p.relative_to(ROOT).as_posix():blob(p.read_bytes()) for p in [SOURCE,GUIDE,ENEMIES,MAPS]},**item_pins},
            'source_files':source_files,'source_event_scripts':scripts,'source_creates':creates,
            'source_guard_arguments':arguments,'source_time_parameters':time_params,
            'repeated_original_warp_blocks':duplicates,
            'prior_item01_numeric_rows':sorted(item_rows,key=lambda x:x[0]),
            'prior_char09_enemy_numeric_rows':enemy_rows,
            'prior_quest05_map_qualification':[r for r in json.loads(MAPS.read_text())['floors'] if r['source_floor_id'] in [41,42,400,6000]],
            'prior_R68_documentary_positions':{'elder':guide['elder_position_as_reported'],
                                                'entrances':guide['entrances_as_reported'],
                                                'exact_same_deployment_verified':False},
            'boundaries':{k:False for k in ['native_execution_verified','branch_priority_verified',
                          'actual_rewards_verified','random_weights_verified','time_tokens_interpreted',
                          'guide_coordinates_corrected','night_guard_warp_corrected','same_official_deployment_verified',
                          'original_pixel_read_in_this_report','maze_walkability_verified','item_namespace_19550_adopted_as_early_fact']},
            'status':{'stage_A':'7_PARTIAL_2_OPEN','stage_B_wiki':'GATED','R79':'PAUSED_NON_BLOCKING','overall_percent':None}}
    return report,selected


def observe_maps(archive_path, out):
    """Reuse the qualified MAP09 source pixels and both full-canvas renderers."""
    import base64
    import io
    import struct
    import zipfile
    import numpy as np
    from PIL import Image,ImageDraw
    from tools.stoneage_map06_two_original_scenes import placements
    from tools.stoneage_map09_batch_scenes import verified_frames
    from tools.stoneage_scene21_town1000 import render
    raw_archive=archive_path.read_bytes()
    if len(raw_archive)!=46844444 or sha(raw_archive)!='d84d0800dd600798769dfb7251a1d7816588ac061ccc27812ac64a37922d4a8a':
        raise ValueError('Original private MAP09 package identity mismatch')
    prior_path=ROOT/'research/recovered/STONEAGE-MAP09-691-SOURCE-READY-SCENES-R1.json'
    prior=json.loads(prior_path.read_text())
    receipt={'schema':'stoneage.quest09.two_original_cave_maps_private_observation.r1',
             'source_MAP09_zip_sha256':sha(raw_archive),'source_MAP09_zip_bytes':len(raw_archive),
             'prior_MAP09_blob':blob(prior_path.read_bytes()),'maps':{},
             'boundaries':{'original_NPC_sprite_drawn':False,'original_client_executed':False,
                           'native_walkability_verified':False,'native_palette_verified':False,
                           'new_RD_decodes':0}}
    with zipfile.ZipFile(archive_path) as z:
        if len(z.infolist())!=4195 or z.testzip() is not None:raise ValueError('MAP09 ZIP CRC/population mismatch')
        if json.loads(z.read('scene-source-receipt.json'))!=prior:raise ValueError('MAP09 receipt mismatch')
        model=json.loads(z.read('dataset.js').decode()[len('window.MAP09_DATA='):-2])
        sources=json.loads(z.read('private-image-source-records.json'))
        if sha(z.read('private-image-source-records.json'))!=prior['private_image_source_records_sha256']:raise ValueError('Image source table mismatch')
        datzip=z.read('source-all-955-original-DAT.zip')
        if sha(datzip)!=prior['original_DAT_archive']['sha256']:raise ValueError('Original DAT package mismatch')
        original=zipfile.ZipFile(io.BytesIO(datzip))
        if original.testzip() is not None:raise ValueError('Original DAT CRC mismatch')
        overview=[]
        for floor in ('41','42'):
            raw=original.read(floor+'.dat');entry=model['maps'][floor]
            if raw!=base64.b64decode(entry['dat_base64']) or sha(raw)!=prior['maps'][floor]['source_sha256']:raise ValueError('Original DAT identity mismatch')
            info,selected=placements(raw);wanted={p['image_key'] for p in selected}
            images={};records={};arrays={}
            for key in wanted:
                png=z.read(f'tiles/{key}.png');row=sources[str(key)]
                if sha(png)!=row['candidate_PNG_sha256']:raise ValueError('Source PNG mismatch')
                im=Image.open(io.BytesIO(png)).convert('RGBA')
                if sha(im.tobytes())!=row['candidate_RGBA_sha256']:raise ValueError('Source RGBA mismatch')
                images[key]=im;records[key]=model['records'][str(key)];arrays[key]=np.array(im)
                if not set(np.unique(arrays[key][:,:,3]))<={0,255}:raise ValueError('Unexpected alpha semantics')
            size,origin,hashes,_=verified_frames(raw,info,selected,images,records,arrays)
            if hashes!=entry['frame_RGBA_sha256'] or hashes!=prior['maps'][floor]['frame_RGBA_sha256']:raise ValueError('Prior complete-frame identity mismatch')
            scene=render(images,records,selected,False,True,False,origin,size)
            (out/'maps').mkdir(exist_ok=True);(out/'original-DAT').mkdir(exist_ok=True)
            (out/'original-DAT'/f'{floor}.dat').write_bytes(raw)
            plain=out/'maps'/f'{floor}-source-combined.png';scene.save(plain)
            marked=scene.copy();draw=ImageDraw.Draw(marked)
            points=[]
            for label,x,y in [('SAGE',34,25),('GUARD1',34,41),('GUARD2',33,41),('ENTRY',11,8)]:
                px,py=origin[0]+(x+y)*32,origin[1]+(y-x)*24
                draw.ellipse((px-12,py-12,px+12,py+12),outline='#ffdc69',width=4)
                draw.text((px+16,py-14),label+' '+str((x,y)),fill='#ffdc69',stroke_width=2,stroke_fill='#172b34')
                n=info['width']*info['height'];i=y*info['width']+x
                values=[struct.unpack_from('<H',raw,8+2*(plane*n+i))[0] for plane in range(3)]
                points.append({'label':label,'xy':[x,y],'modern_anchor':[px,py],'original_three_u16_values':values})
            marked_path=out/'maps'/f'{floor}-source-marked.png';marked.save(marked_path)
            thumb=marked.convert('RGB');thumb.thumbnail((1000,800));overview.append((floor,thumb))
            receipt['maps'][floor]={'source_DAT_sha256':sha(raw),'source_DAT_bytes':len(raw),
                'geometry':[info['width'],info['height']],'canvas_size':size,'origin':origin,
                'source_draw_positions':len(selected),'source_candidate_PNGs_reread':len(wanted),
                'low_nonzero_values_not_drawn':info['source_low_nonzero_not_rendered'],
                'three_full_frame_RGBA_sha256':hashes,'source_PNG_sha256':sha(plain.read_bytes()),
                'marked_PNG_sha256':sha(marked_path.read_bytes()),'source_points':points,
                'source_candidate_image_receipts':{str(k):sources[str(k)] for k in sorted(wanted)}}
        contact=Image.new('RGB',(1040,1740),'#11232a');draw=ImageDraw.Draw(contact)
        for no,(floor,im) in enumerate(overview):
            y=no*870;draw.text((24,y+14),'SOURCE FLOOR '+floor+' / MODERN MARKERS ONLY',fill='white')
            contact.paste(im,((1040-im.width)//2,y+50))
        contact.save(out/'dream-cave-source-contact.jpg',quality=92)
        receipt['contact_sha256']=sha((out/'dream-cave-source-contact.jpg').read_bytes())
    target=ROOT/'research/recovered/STONEAGE-QUEST09-TWO-ORIGINAL-CAVE-MAPS-OBSERVATION-R1.json'
    target.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    (out/'map-source-evidence.json').write_bytes(target.read_bytes())
    return receipt


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('source_zip',type=Path);p.add_argument('--report',type=Path,default=REPORT)
    p.add_argument('--private-dir',type=Path);p.add_argument('--map09-zip',type=Path);args=p.parse_args()
    if args.map09_zip and not args.private_dir:p.error('--map09-zip requires --private-dir')
    report,selected=extract(args.source_zip)
    args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    if args.private_dir:
        args.private_dir.mkdir(parents=True,exist_ok=True)
        for path,raw in selected.items():
            target=args.private_dir/'original'/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
        content=''.join('<details><summary>'+html.escape(path)+'</summary><pre>'+html.escape(raw.decode('cp950'))+'</pre></details>' for path,raw in sorted(selected.items()))
        (args.private_dir/'index.html').write_text('<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><title>夢幻洞窟原資料</title>'
            '<style>body{max-width:1040px;margin:40px auto;background:#f3efe4;color:#24372f;font:17px system-ui}summary{padding:12px;cursor:pointer}pre{background:#fff;padding:18px;white-space:pre-wrap}</style>'
            '<h1>夢幻洞窟：原委託、獎勵、入口與守門配置</h1><p>後期社群mixed25保存來源；原CP950文字逐字保留。這是靜態來源查閱，沒有執行原遊戲。'
            '2003年攻略與此保存檔未認證同版；原位置差異、夜間守門轉向41及重複出口保留，不作修正。</p>'+content+'</html>',encoding='utf-8')
        (args.private_dir/'source-evidence.json').write_bytes(args.report.read_bytes())
        if args.map09_zip:
            observe_maps(args.map09_zip,args.private_dir)
            page=args.private_dir/'index.html';text=page.read_text();text=text.replace('</html>',
                '<h2>兩份真實來源地圖的現代標記</h2><p>SAGE為仙人、GUARD為守門建立點、ENTRY為來源傳送落點。圈與文字是現代標記；沒有繪出原NPC。'
                'floor42守門參數仍指向41，並未把目標偷偷改成42。</p>'
                '<p><a href="maps/41-source-marked.png">floor41完整標記圖</a> · <a href="maps/42-source-marked.png">floor42完整標記圖</a></p>'
                '<img src="dream-cave-source-contact.jpg" style="max-width:100%" alt="兩份來源地圖與現代標記"></html>');page.write_text(text)
    print(json.dumps({'files':len(selected),'creates':len(report['source_creates']),
                      'event_blocks':sum(len(s['events']) for s in report['source_event_scripts']),
                      'warp_occurrences':sum('target_floor_x_y' in r for r in report['source_creates'])}))


if __name__=='__main__':main()
