"""QUEST13 source-bounded Goa mountain Uli letters and flower chain.

Read the already qualified private archives. Preserve source script byte positions,
CP950, punctuation and literal quantities. This does not execute game conditions.
Public JSON has numeric controls and digests; proprietary dialogue/tiles stay private.
"""
import argparse
import hashlib
import html
import io
import json
from pathlib import Path
import re
import struct
import zipfile
import zlib

from tools.stoneage_quest12_mining_competition_source import (
    ROOT, SOURCE, NPC_ZIP_SHA, ITEM_ZIP_SHA, MAP_ZIP_SHA,
    read_source, parse_events, sha, git_blob,
)

REPORT = ROOT/'research/recovered/STONEAGE-QUEST13-GOA-ULI-LETTERS-ORIGINAL-SOURCE-R1.json'
CATALOG = ROOT/'research/recovered/STONEAGE-QUEST-STORY-MODULE-01-ORIGINAL-EXCHANGEMAN-QUEST-SOURCE-BLOCK-CATALOG-R1.json'
ITEM_SHARDS = [ROOT/f'research/recovered/item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-0{i}-R1.json' for i in (1,2)]
MAP_RECEIPT = ROOT/'research/recovered/STONEAGE-MAP09-691-SOURCE-READY-SCENES-R1.json'
CREATE = 'jaruga/event/event07n.create'
SCRIPTS = [f'jaruga/event/event07_{i}' for i in range(1,11)]
ITEM_IDS = (1206,2414,2424,2425,2426)


def verified_create_rows(source, manifest):
    rows=[]
    for r in manifest['create_rows']:
        if r[0]!=CREATE: continue
        if sha(source[CREATE][r[2]:r[3]])!=r[4]:raise ValueError('CREATE original-byte SHA mismatch')
        refs=r[15]
        if len(refs)!=1 or refs[0][0] not in SCRIPTS or refs[0][2]!=sha(source[refs[0][0]]):
            raise ValueError('CREATE script foreign key mismatch')
        x,y=r[7][:2]
        rows.append({'path':CREATE,'ordinal':r[1], 'start_byte':r[2], 'end_byte':r[3],
                     'original_block_sha256':r[4], 'floor':r[5], 'xy':[x,y],
                     'original_borncorner':r[7], 'graphic_alias':r[6],
                     'original_direction':r[10], 'template_token':r[11],
                     'original_template_bindings':r[13], 'source_script':refs[0][0],
                     'source_script_sha256':refs[0][2]})
    if len(rows)!=10 or len({x['source_script'] for x in rows})!=10:raise ValueError('Unexpected original CREATE count')
    return rows


def audited_scripts(source):
    old=json.loads(CATALOG.read_text())
    scripts=[];n=0
    for p in SCRIPTS:
        raw=source[p]
        if raw.decode('cp950').encode('cp950')!=raw:raise ValueError('CP950 round-trip changed original')
        ev=parse_events(raw)
        independent=[x for x in old['source_event_blocks'] if x['script_path']==p]
        if len(ev)!=len(independent):raise ValueError('Prior QUEST01 TYPE population mismatch')
        for x,y in zip(ev,independent):
            if (x['ordinal'],x['type'])!=(y['script_block_ordinal'],y['raw_type']):
                raise ValueError('QUEST01 original TYPE identity mismatch')
            if hashlib.sha256(x['raw_condition'].encode('utf-8')).hexdigest()!=y['condition_expression_decoded_cp950_UTF8_sha256']:
                raise ValueError('Original condition independent SHA mismatch')
            # Keep source header and event number, not merely guessed type counts.
            if x['event_number']!=y['event_number']:
                raise ValueError('Original EventNo mismatch')
        scripts.append({'path':p,'bytes':len(raw),'sha256':sha(raw),
                        'crc32':f'{zlib.crc32(raw):08x}', 'events':ev})
        n+=len(ev)
    if n!=16:raise ValueError('Unexpected source event count')
    return scripts,n


def audited_items(item_path, private):
    from PIL import Image
    b=item_path.read_bytes()
    if sha(b)!=ITEM_ZIP_SHA:raise ValueError('Original ITEM01 private archive identity mismatch')
    indexes={}
    for path in ITEM_SHARDS:
        if not path.is_file():raise ValueError('Original source index shard missing')
        for r in json.loads(path.read_text())['rows']:
            if r[0] in ITEM_IDS:indexes[r[0]]=r
    if set(indexes)!=set(ITEM_IDS):raise ValueError('Missing source item index')
    out=[];icons={}
    with zipfile.ZipFile(io.BytesIO(b)) as z:
        if len(z.infolist())!=838 or z.testzip() is not None:raise ValueError('ITEM01 ZIP inventory/CRC')
        catalog=json.loads(z.read('private-full-catalog.json'))
        pixels={r['source_itemset_image_number_alias']:r for r in json.loads(z.read('private-RD-source-receipts.json'))['source_image_rows']}
        for item in catalog['items']:
            id=item['id']
            if id not in ITEM_IDS:continue
            rows=[];aliases=[]
            for table,idx in [('itemset.txt',1),('itemset0710.txt',2)]:
                if table not in item:
                    if indexes[id][idx] is not None:raise ValueError('Missing physical item row')
                    continue
                old=item[table]
                cols=old['original_94_columns']
                raw=','.join(cols).encode('cp950')
                if len(cols)!=94 or int(cols[16])!=id or sha(raw)!=old['original_row_sha256'] or sha(raw)!=indexes[id][idx]:
                    raise ValueError('Original 94-field item or public index disagrees')
                rows.append({'source_table':table,'source_row_1based':old['source_row_1based'],
                             'original_line_without_newline_sha256':sha(raw), 'bytes':len(raw),
                             'name_cp950_sha256':sha(old['source_name'].encode('cp950'))})
                aliases.append(old['source_image_number'])
                if private:
                    q=private/'original-item-rows';q.mkdir(parents=True,exist_ok=True)
                    (q/f'{table}-{id}.row').write_bytes(raw)
            if len(set(aliases))!=1:raise ValueError('Different aliases in two same-ID source tables')
            alias=aliases[0]; px=pixels.get(alias,{})
            have='private_PNG' in px
            if have:
                png=z.read('source-TW1-original-RD-candidates/'+px['private_PNG'])
                rgba=Image.open(io.BytesIO(png)).convert('RGBA').tobytes()
                if sha(png)!=px['candidate_PNG_SHA256'] or sha(rgba)!=px['candidate_RGBA_SHA256']:
                    raise ValueError('Previously accepted TW1 source RD candidate changed')
                icons[alias]=px['private_PNG']
                if private:
                    q=private/'icons';q.mkdir(parents=True,exist_ok=True)
                    (q/px['private_PNG']).write_bytes(png)
            out.append({'item_id':id,'original_rows':rows,'original_image_alias':alias,
                        'tw1_original_RD_candidate_available':have,
                        'tw1_original_RD_status':px.get('tw1_original_RD_status','NOT_IN_SAVED_ITEM01_IMAGE_SET'),
                        'candidate_PNG_sha256':px.get('candidate_PNG_SHA256')})
    if len(out)!=len(ITEM_IDS):raise ValueError('Missing private source item')
    return sorted(out,key=lambda r:r['item_id']),icons


def audited_maps(map_path,creates,private):
    from PIL import Image,ImageDraw
    raw_zip=map_path.read_bytes()
    if sha(raw_zip)!=MAP_ZIP_SHA:raise ValueError('Original MAP09 private archive identity mismatch')
    maps=[]
    with zipfile.ZipFile(io.BytesIO(raw_zip)) as z:
        if len(z.infolist())!=4195 or z.testzip() is not None:raise ValueError('MAP09 inventory/CRC mismatch')
        old=z.read('scene-source-receipt.json')
        if git_blob(old)!= '137580e7c25aadf3d679b6ebfb5080b79912cc4f':
            raise ValueError('Original map source receipt differs from verified Git source')
        receipt=json.loads(old)
        original_dats=z.read('source-all-955-original-DAT.zip')
        if sha(original_dats)!=receipt['original_DAT_archive']['sha256']:
            raise ValueError('Original DAT archive mismatch')
        with zipfile.ZipFile(io.BytesIO(original_dats)) as dz:
            for floor in sorted({r['floor'] for r in creates}):
                original=dz.read(str(floor)+'.dat'); rec=receipt['maps'][str(floor)]
                if sha(original)!=rec['source_sha256']:raise ValueError('Original DAT SHA mismatch')
                w,h=struct.unpack_from('<II',original);cells=w*h
                if len(original)!=8+cells*6:raise ValueError('Unexpected DAT three-plane structure')
                thumb_bytes=z.read(f'thumbnails/{floor}.jpg');im=Image.open(io.BytesIO(thumb_bytes)).convert('RGB')
                sx=im.width/rec['canvas_size'][0];sy=im.height/rec['canvas_size'][1]
                ox,oy=rec['origin'];draw=ImageDraw.Draw(im);points=[]
                for r in [t for t in creates if t['floor']==floor]:
                    x,y=r['xy']
                    if not (0<=x<w and 0<=y<h):raise ValueError('CREATE point outside actual DAT')
                    vals=[struct.unpack_from('<H',original,8+2*(plane*cells+y*w+x))[0] for plane in range(3)]
                    points.append({'create_ordinal':r['ordinal'],'xy':[x,y],
                                   'source_three_u16_values':vals})
                    xx=(ox+(x+y)*32)*sx;yy=(oy+(y-x)*24)*sy
                    draw.ellipse((xx-4,yy-4,xx+4,yy+4),outline='yellow',width=2)
                    draw.text((xx+6,yy-8),str(r['ordinal']),fill='yellow')
                if private:
                    (private/'maps').mkdir(parents=True,exist_ok=True)
                    (private/'original-DAT').mkdir(parents=True,exist_ok=True)
                    (private/'original-DAT'/f'{floor}.dat').write_bytes(original)
                    im.save(private/'maps'/f'{floor}-marked.jpg',quality=94)
                maps.append({'floor':floor,'source_DAT_SHA256':sha(original),'original_DAT_bytes':len(original),
                             'geometry':[w,h],'prior_source_thumbnail_SHA256':sha(thumb_bytes),
                             'source_points':points})
    if len(maps)!=6 or sum(len(x['source_points']) for x in maps)!=10:
        raise ValueError('Original source map or CREATE position coverage incomplete')
    return maps


def extract(npc,item,map_archive,private=None):
    source,manifest=read_source(npc)
    if sha(npc.read_bytes())!=NPC_ZIP_SHA:raise ValueError('NPC archive mismatch')
    rows=verified_create_rows(source,manifest)
    scripts,n=audited_scripts(source)
    items,icons=audited_items(item,private)
    maps=audited_maps(map_archive,rows,private)
    selected={p:source[p] for p in [CREATE]+SCRIPTS}
    if private:
        for path,raw in selected.items():
            dest=private/'original'/path;dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_bytes(raw)
        orig=''.join('<details><summary>'+html.escape(p)+'</summary><pre>'+html.escape(b.decode('cp950'))+'</pre></details>' for p,b in sorted(selected.items()))
        imgtags=''.join('<figure><img src="maps/'+str(x['floor'])+'-marked.jpg"><figcaption>原DAT floor '+str(x['floor'])+'：现代CREATE位置标注</figcaption></figure>' for x in maps)
        card=''.join('<article><strong>'+str(x['item_id'])+'</strong>'+ ('<img src="icons/'+icons[x['original_image_alias']]+'">' if x['original_image_alias'] in icons else '原图未取得') + '</article>' for x in items)
        (private/'index.html').write_text('<!doctype html><html lang="zh-Hans"><meta charset="utf-8"><title>哥亚山乌力送信原件查阅</title><style>body{font:16px system-ui;max-width:1080px;margin:auto;background:#f4f1e9;color:#25332b;padding:20px}pre{white-space:pre-wrap;background:white;padding:16px}article,figure{display:inline-block;vertical-align:top;padding:12px;margin:10px;background:white;max-width:440px}img{display:block;max-width:100%;image-rendering:pixelated}summary{padding:8px}</style><h1>哥亚山乌力送信与鲜花：原档案</h1><p>来源：后期社区mixed25保存原件，未认证官方部署。全部原文保留繁体。原事件条件只读，不模拟游戏执行；标注地图是现代研究图，不是原截图。TW1道具像素是跨保存来源候选。</p><h2>六份原DAT位置</h2>'+imgtags+'<h2>五个原道具ID及跨源图像候选</h2>'+card+'<h2>11份原CREATE／参数文件</h2>'+orig+'</html>',encoding='utf-8')
    report={'schema':'stoneage.quest13.goa_uli_letters_source.r1','date':'2026-11-08',
            'origin_class':'ORIGIN_UNRESOLVED','carrier':'LATER_COMMUNITY_MIXED25_NOT_OFFICIAL_DEPLOYMENT',
            'verified_original_NPC_members':len(source), 'source_archive_sha256':NPC_ZIP_SHA,
            'original_parent_RAR_sha256':manifest['original_rar_sha256'],
            'private_item_archive_sha256':ITEM_ZIP_SHA,'private_map_archive_sha256':MAP_ZIP_SHA,
            'source_manifest_git_blob_sha1':git_blob(SOURCE.read_bytes()),
            'prior_quest01_catalog_git_blob_sha1':git_blob(CATALOG.read_bytes()),
            'source_files':[{'path':p,'original_bytes':len(raw),'sha256':sha(raw),'crc32':f'{zlib.crc32(raw):08x}'} for p,raw in sorted(selected.items())],
            'original_create_rows':rows,'scripts':scripts,'prior_QUEST01_TYPE_blocks_verified':n,
            'item_source_evidence':items,'original_map_source_observations':maps,
            'source_literal_crossfamily_item_2414':{'item_id':2414, 'also_referenced_by_quest11':True,
                  'official_same_deployment_identity_verified':False},
            'source_stage':{'original_event_numbers':[7,8], 'source_item_ids':list(ITEM_IDS),
                            'source_only_not_a_verified_runtime_walkthrough':True},
            'provenance_negative_guards':{k:False for k in [
                'native_game_execution','quest_branch_priority_or_condition_parser_verified',
                'original_script_text_repaired','implicit_item_quantity_assumed',
                'official_initial_or_permanent_quest_origin_verified','same_official_client_server_deployment_verified',
                'tw1_item_pixels_claimed_mixed25_same_release','native_sprite_pixels_observed_this_task',
                'NPC_original_animation_verified','source_map_collider_or_teleporter_verified',
                'historical_official_world_map_rebuilt','early_1_82_content_confirmed',
                'new_original_RD_decode','modern_new_game_feature_implemented']},
            'status':{'stage_A':'7_PARTIAL_2_OPEN','stage_B_wiki':'GATED',
                      'R79':'PAUSED_NON_BLOCKING','overall_percent':None}}
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if private:(private/'source-evidence.json').write_bytes(REPORT.read_bytes())
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for x in ('npc_archive','item_archive','map_archive'):p.add_argument(x,type=Path)
    p.add_argument('--private-dir',type=Path)
    args=p.parse_args()
    r=extract(args.npc_archive,args.item_archive,args.map_archive,args.private_dir)
    print(json.dumps({'source_files':len(r['source_files']),'create_positions':len(r['original_create_rows']),
                      'event_blocks':sum(len(x['events']) for x in r['scripts']),
                      'item_ids':len(r['item_source_evidence']),'original_DAT_floors':len(r['original_map_source_observations'])}))


if __name__=='__main__':main()
