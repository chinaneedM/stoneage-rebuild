"""QUEST12: qualified mixed25 mining competition source, not an event interpreter.

Only private inputs are read; public report contains numeric controls, hashes,
original source positions and explicit unknowns, never original dialogue/bitmaps.
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

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'research/recovered/STONEAGE-QUEST12-MINING-COMPETITION-ORIGINAL-SOURCE-R1.json'
SOURCE = ROOT / 'research/recovered/STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json'
NPC_ZIP_SHA = 'c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f'
ITEM_ZIP_SHA = 'cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa'
MAP_ZIP_SHA = 'd84d0800dd600798769dfb7251a1d7816588ac061ccc27812ac64a37922d4a8a'
SCRIPTS = ['giiru/event/giruev2_1', 'giiru/event/giruev2_2']
CREATE_PATHS = ['giiru/event/giruev2.create', '300/sb_bac.create', 'genout/giruev2.create']
EXTRA = ['300/sb_bac.arg', '300/sb_bac.template', 'jaruga/event/event.template',
         'genout/wpm_31805_22_4']
ITEM_IDS = (2391, 2393, 2394, 2527, 2533, 2534, 2535, 2536)


def sha(b): return hashlib.sha256(b).hexdigest()


def git_blob(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()


def parse_operand(s):
    m=re.fullmatch(r'(\d+)(?:\*(\d+))?',s)
    if not m: raise ValueError('Unknown original item operand')
    return {'item_id':int(m[1]), 'explicit_quantity':None if m[2] is None else int(m[2])}


def parse_events(raw):
    """Accept only bounded original EventNo/TYPE/EVENT/EventEnd, no execution."""
    rows=[];cur=None;offset=0
    for line_no,line in enumerate(raw.splitlines(keepends=True),1):
        t=line.strip()
        if t.startswith(b'EventNo:'):
            if cur is not None: raise ValueError('Unclosed source header')
            cur={'ordinal':len(rows),'source_start_line':line_no,'source_start_byte':offset,
                 'event_number':int(t.split(b':',1)[1]),'commands':[], 'messages_seen':[]}
        if cur is not None and b':' in t:
            k,v=t.split(b':',1)
            if k in (b'TYPE',b'EVENT'):
                key='type' if k==b'TYPE' else 'raw_condition'
                if key in cur: raise ValueError('Repeated control '+key)
                cur[key]=v.decode('ascii')
            elif k in (b'GetItem',b'DelItem'):
                literal=v.decode('ascii')
                cur['commands'].append({'key':k.decode(),'raw_operand':literal,
                                        'operands':[parse_operand(x) for x in literal.split(',')]})
            elif k in (b'EndSetFlg',b'DelStone'):
                cur['commands'].append({'key':k.decode(),'raw_operand':v.decode('ascii'),
                                        'value':int(v)})
            elif b'Msg' in k: cur['messages_seen'].append(k.decode('ascii'))
        if t==b'EventEnd':
            if cur is None or not all(k in cur for k in ('type','raw_condition')):
                raise ValueError('Unbounded/incomplete event')
            cur.update(source_end_line=line_no,source_end_byte=offset+len(line),
                       source_block_sha256=sha(raw[cur['source_start_byte']:offset+len(line)]))
            rows.append(cur);cur=None
        elif t.startswith(b'TYPE:') and cur is None: raise ValueError('Unbound TYPE')
        offset+=len(line)
    if cur is not None: raise ValueError('Unclosed event')
    return rows


def read_source(npc_path):
    raw=npc_path.read_bytes()
    if len(raw)!=995176 or sha(raw)!=NPC_ZIP_SHA:raise ValueError('NPC archive mismatch')
    manifest=json.loads(SOURCE.read_text())
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        expected={'npc/'+x[0]:x for x in manifest['source_files']}
        if len(expected)!=2205 or len(z.infolist())!=2205 or set(z.namelist())!=set(expected):
            raise ValueError('NPC inventory mismatch')
        source={}
        for name,row in expected.items():
            b=z.read(name)
            if [len(b),sha(b),f'{zlib.crc32(b):08x}']!=row[1:4]:
                raise ValueError('NPC member hash/CRC mismatch: '+name)
            source[row[0]]=b
    return source,manifest


def original_create_rows(source,manifest):
    rows=[]
    for path in CREATE_PATHS:
        matches=[r for r in manifest['create_rows'] if r[0]==path]
        for r in matches:
            if sha(source[path][r[2]:r[3]])!=r[4]:raise ValueError('Original CREATE block SHA mismatch')
            rows.append({'path':path,'ordinal':r[1],'block_sha256':r[4], 'start_byte':r[2],
                         'end_byte':r[3],'floor':r[5],'graphic_alias':r[6],
                         'borncorner':r[7], 'borncenter':r[8], 'direction':r[10],
                         'template_token':r[11],'template_bindings':r[13],
                         'parameter_references':r[15]})
    if [sum(r['path']==p for r in rows) for p in CREATE_PATHS]!=[2,1,21]:
        raise ValueError('Original CREATE population changed')
    return rows


def numeric_control(raw,keys):
    controls=[]
    for i,line in enumerate(raw.splitlines(),1):
        if b':' not in line:continue
        k,v=line.strip().split(b':',1)
        if k.decode('ascii',errors='ignore') in keys:
            controls.append({'line':i,'key':k.decode('ascii'),'raw_value':v.decode('ascii')})
    return controls


def extract(npc_path,item_path,map_path,private_dir=None):
    from PIL import Image,ImageDraw
    source,manifest=read_source(npc_path)
    for p in set(SCRIPTS+CREATE_PATHS+EXTRA):
        if source[p].decode('cp950').encode('cp950')!=source[p]:
            raise ValueError('Nonroundtrip CP950: '+p)
    creates=original_create_rows(source,manifest)
    events=[{'path':p,'sha256':sha(source[p]),'events':parse_events(source[p])} for p in SCRIPTS]
    if [len(x['events']) for x in events]!=[7,6]:
        raise ValueError('Unexpected event population')
    controls={p:numeric_control(source[p], {'WARP','FREE','MONEY','DelItem','item','enemyno','steal','time','entype'})
              for p in ['300/sb_bac.arg','genout/wpm_31805_22_4']}
    # Preserve absence across every original NPC file, including non-selected files.
    all_gets={item:[] for item in ITEM_IDS}
    for path,b in source.items():
        for i,line in enumerate(b.splitlines(),1):
            if line.strip().startswith(b'GetItem:'):
                for item in ITEM_IDS:
                    if re.search(rb'(?<!\d)'+str(item).encode()+rb'(?:\*\d+)?(?!\d)',line):
                        all_gets[item].append({'path':path,'source_line':i})
    if sha(item_path.read_bytes())!=ITEM_ZIP_SHA:raise ValueError('ITEM01 source archive mismatch')
    items=[];icons={}
    with zipfile.ZipFile(item_path) as z:
        if len(z.infolist())!=838 or z.testzip() is not None:raise ValueError('ITEM source ZIP damaged')
        catalog=json.loads(z.read('private-full-catalog.json'))
        pixels={r['source_itemset_image_number_alias']:r for r in json.loads(z.read('private-RD-source-receipts.json'))['source_image_rows']}
        for item in catalog['items']:
            if item['id'] not in ITEM_IDS:continue
            rows=[];image_aliases=[]
            for table in ['itemset.txt','itemset0710.txt']:
                if table not in item:continue
                src=item[table]
                b=','.join(src['original_94_columns']).encode('cp950')
                if len(src['original_94_columns'])!=94 or sha(b)!=src['original_row_sha256']:
                    raise ValueError('Original item row mismatch')
                rows.append({'table':table,'source_row_1based':src['source_row_1based'],
                             'raw_line_without_newline_sha256':sha(b),'source_name_cp950_sha256':sha(src['source_name'].encode('cp950'))})
                image_aliases.append(src['source_image_number'])
                if private_dir:
                    d=private_dir/'original-item-rows';d.mkdir(parents=True,exist_ok=True)
                    (d/f'{table}-{item["id"]}.row').write_bytes(b)
            if len(set(image_aliases))!=1:raise ValueError('Image alias differs by source table')
            alias=image_aliases[0];p=pixels.get(alias,{});icon_available=False
            if 'private_PNG' in p:
                png=z.read('source-TW1-original-RD-candidates/'+p['private_PNG'])
                rgba=Image.open(io.BytesIO(png)).convert('RGBA').tobytes()
                if sha(png)!=p['candidate_PNG_SHA256'] or sha(rgba)!=p['candidate_RGBA_SHA256']:
                    raise ValueError('Previously recorded original RD candidate mismatch')
                if private_dir:
                    folder=private_dir/'icons';folder.mkdir(exist_ok=True)
                    (folder/p['private_PNG']).write_bytes(png)
                icon_available=True
                icons[alias]=p['private_PNG']
            items.append({'item_id':item['id'],'original_rows':rows,'image_alias':alias,
                          'tw1_original_RD_candidate_available':icon_available,
                          'image_source_status':p.get('tw1_original_RD_status','MISSING_IN_THIS_ARCHIVE'),
                          'image_PNG_SHA256':p.get('candidate_PNG_SHA256')})
    if set(x['item_id'] for x in items)!=set(ITEM_IDS):raise ValueError('Missing selected item')
    if sha(map_path.read_bytes())!=MAP_ZIP_SHA:raise ValueError('MAP09 source archive mismatch')
    floor_targets={31805:[('tenim',19,21),('babaro',33,23),('miner_center',26,23),('permit_gate',22,4)],
                   31806:[('permit_dest',34,6)]}
    maps=[]
    with zipfile.ZipFile(map_path) as z:
        if len(z.infolist())!=4195 or z.testzip() is not None:raise ValueError('MAP09 CRC/inventory mismatch')
        m=json.loads(z.read('scene-source-receipt.json'))
        dz=zipfile.ZipFile(io.BytesIO(z.read('source-all-955-original-DAT.zip')))
        for floor,targets in floor_targets.items():
            raw=dz.read(f'{floor}.dat');old=m['maps'][str(floor)]
            if sha(raw)!=old['source_sha256']:raise ValueError('Original DAT vs prior MAP09 receipt')
            width,height=struct.unpack_from('<II',raw);n=width*height
            if len(raw)!=8+n*6:raise ValueError('Original DAT size mismatch')
            thumb_b=z.read(f'thumbnails/{floor}.jpg');im=Image.open(io.BytesIO(thumb_b)).convert('RGB')
            draw=ImageDraw.Draw(im);sx=im.width/old['canvas_size'][0];sy=im.height/old['canvas_size'][1]
            originx,originy=old['origin'];points=[]
            for label,x,y in targets:
                if not (0<=x<width and 0<=y<height):raise ValueError('Position out of range')
                vals=[struct.unpack_from('<H',raw,8+2*(q*n+y*width+x))[0] for q in range(3)]
                points.append({'label':label,'xy':[x,y],'source_three_u16_values':vals})
                px=(originx+(x+y)*32)*sx;py=(originy+(y-x)*24)*sy
                draw.ellipse([px-4,py-4,px+4,py+4],outline='yellow',width=2);draw.text((px+4,py-9),label,fill='yellow')
            maps.append({'floor':floor,'original_DAT_sha256':sha(raw),'original_DAT_bytes':len(raw),
                         'geometry':[width,height],'original_thumbnail_sha256':sha(thumb_b),'source_points':points})
            if private_dir:
                (private_dir/'maps').mkdir(exist_ok=True)
                (private_dir/'original-DAT').mkdir(exist_ok=True)
                (private_dir/'original-DAT'/f'{floor}.dat').write_bytes(raw)
                im.save(private_dir/'maps'/f'{floor}-marked.jpg',quality=95)
    selected={p:source[p] for p in SCRIPTS+CREATE_PATHS+EXTRA}
    if private_dir:
        for path,b in selected.items():
            d=private_dir/'original'/path;d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes(b)
        lines=[]
        for i in sorted(items,key=lambda i:i['item_id']):
            pic=icons.get(i['image_alias']);image='<img src="icons/'+pic+'" style="image-rendering:pixelated;max-width:100px">' if pic else '该源未取到原图'
            lines.append('<article><b>道具 '+str(i['item_id'])+'</b> '+image+'</article>')
        source_html=''.join('<details><summary>'+html.escape(p)+'</summary><pre>'+html.escape(b.decode('cp950'))+'</pre></details>' for p,b in sorted(selected.items()))
        content='<!doctype html><html lang="zh-Hans"><meta charset="utf-8"><title>QUEST12 原矿山比赛资料</title><style>body{font:16px system-ui;max-width:1100px;margin:auto;background:#f8f6ee;color:#26372d}pre{white-space:pre-wrap;padding:16px;background:white}article,figure{display:inline-block;margin:12px;padding:12px;background:white}img{max-width:100%}</style><h1>矿山比赛：来源限定原文与地图</h1><p>后期 mixed25 社区保存资料。原文本繁体及疑似异常字保持不修；这里只查阅原文件，不模拟事件条件、掉落或原版执行。</p><h2>原地图缩图</h2><figure><img src="maps/31805-marked.jpg"></figure><figure><img src="maps/31806-marked.jpg"></figure><h2>候选道具像素</h2>'+''.join(lines)+'<h2>原始配置全文（仅私人文件）</h2>'+source_html+'</html>'
        (private_dir/'index.html').write_text(content,encoding='utf-8')
    report={'schema':'stoneage.quest12.mining_competition_original_source.r1','date':'2026-11-08',
            'origin_class':'ORIGIN_UNRESOLVED','carrier':'LATER_COMMUNITY_MIXED25_NOT_OFFICIAL_DEPLOYMENT',
            'verified_original_NPC_members':2205,'source_archive_sha256':NPC_ZIP_SHA,
            'private_item_archive_sha256':ITEM_ZIP_SHA,'private_map_archive_sha256':MAP_ZIP_SHA,
            'parent_RAR_sha256':manifest['original_rar_sha256'],
            'prior_manifest_git_blob_sha1':git_blob(SOURCE.read_bytes()),
            'source_files':[{'path':p,'bytes':len(b),'sha256':sha(b),'crc32':f'{zlib.crc32(b):08x}'} for p,b in sorted(selected.items())],
            'principal_creates':[r for r in creates if r['path']==CREATE_PATHS[0]],
            'miner_create':[r for r in creates if r['path']==CREATE_PATHS[1]],
            'generated_support_creates':[r for r in creates if r['path']==CREATE_PATHS[2]],
            'scripts':events,'other_original_controls':controls,
            'item_evidence':sorted(items,key=lambda i:i['item_id']),
            'get_item_source_occurrences_across_all_2205_files':{str(k):v for k,v in all_gets.items()},
            'map_source_observations':maps,
            'boundaries':{k:False for k in ['original_game_runtime_executed','event_branch_order_verified',
                'source_misspellings_corrected','implicit_quantity_assumed','item_2533_acquisition_proven',
                'item_2534_acquisition_proven','item_2535_enemy_drops_verified','mining_rights_reward_runtime_verified',
                'warp_runtime_verified','character_movement_or_collision_verified','original_NPC_pixels_rendered',
                'original_2d_map_full_scene_redrawn','all_version_quest_completion_verified',
                'same_official_deployment_verified','official_version_or_permanent_event_origin_verified']},
            'status':{'stage_A':'7_PARTIAL_2_OPEN','stage_B_wiki':'GATED','R79':'PAUSED_NON_BLOCKING','overall_percent':None}}
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if private_dir:(private_dir/'source-evidence.json').write_bytes(REPORT.read_bytes())
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for key in ['npc_zip','item_zip','map_zip']:p.add_argument(key,type=Path)
    p.add_argument('--private-dir',type=Path)
    a=p.parse_args();r=extract(a.npc_zip,a.item_zip,a.map_zip,a.private_dir)
    print(json.dumps({'source_files':len(r['source_files']),'event_blocks':sum(len(s['events']) for s in r['scripts']),
        'principal_creates':len(r['principal_creates']),'generated_support_creates':len(r['generated_support_creates']),
        'selected_item_rows':sum(len(x['original_rows']) for x in r['item_evidence'])},sort_keys=True))

if __name__=='__main__':main()
