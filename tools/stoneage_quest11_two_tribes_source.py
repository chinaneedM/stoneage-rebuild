"""Two-tribe source dossier: preserve malformed headers and ordered item operands.

No condition interpreter, source typo correction, or runtime behavior is added.
"""
import argparse
import html
import io
import json
from pathlib import Path
import re
import struct
import zipfile
import zlib
from tools.stoneage_quest08_mining_source import ROOT,SOURCE,load_private_source,sha,blob,numeric_item
from tools.stoneage_quest10_quarry_spirits_source import ITEM_ARCHIVE_SHA,MAP_ARCHIVE_SHA

REPORT=ROOT/'research/recovered/STONEAGE-QUEST11-TWO-TRIBES-ORIGINAL-SOURCE-R1.json'
PARAMETERS=[f'giiru/event/garunaev{n}' for n in range(1,9)]
CREATE='giiru/event/garunaev1.create'
CATALOG=ROOT/'research/recovered/STONEAGE-QUEST-STORY-MODULE-01-ORIGINAL-EXCHANGEMAN-QUEST-SOURCE-BLOCK-CATALOG-R1.json'


def source_events(raw):
    """Capture every bounded TYPE block, including literal EvebtNo header.

    Unknown/missing headers fail closed. A typo is recorded, never canonicalized.
    Item comma operands are preserved in order, not executed as an expression.
    """
    rows=[];current=None;offset=0
    for line_no,line in enumerate(raw.splitlines(keepends=True),1):
        value=line.strip()
        if value.startswith((b'EventNo:',b'EvebtNo:')):
            if current is not None:raise ValueError('Unclosed source event')
            key,number=value.split(b':',1)
            current={'ordinal':len(rows),'start_byte':offset,'start_line':line_no,
                'header_key':key.decode(),'header_numeric_literal':int(number),
                'event_number':int(number) if key==b'EventNo' else None,
                'commands':[],'other_numeric_controls':[],'message_keys':[]}
        if current is not None and b':' in value:
            key,v=value.split(b':',1)
            if key in (b'TYPE',b'EVENT'):
                field='type' if key==b'TYPE' else 'event'
                if field in current:raise ValueError('Duplicate source control')
                current[field]=v.decode('ascii')
                if key==b'TYPE':current['type_line']=line_no
            elif key in (b'DelItem',b'GetItem'):
                literal=v.decode('ascii')
                current['commands'].append({'name':key.decode(),'raw_operand':literal,
                    'operands':[numeric_item(x) for x in literal.split(',')]})
            elif key in (b'EndSetFlg',b'DelStone'):
                current['other_numeric_controls'].append({'name':key.decode(),'value':int(v)})
            elif b'Msg' in key:current['message_keys'].append(key.decode('ascii'))
        if value==b'EventEnd':
            if current is None or 'type' not in current or 'event' not in current:raise ValueError('Unbounded source event')
            current.update(end_byte=offset+len(line),end_line=line_no,
                block_sha256=sha(raw[current['start_byte']:offset+len(line)]))
            rows.append(current);current=None
        elif value.startswith(b'TYPE:') and current is None:raise ValueError('TYPE lacks preserved source header')
        offset+=len(line)
    if current is not None:raise ValueError('Unclosed source event')
    return rows


def extract(npc_zip,item_zip,map_zip,out):
    from PIL import Image,ImageDraw
    archive,source,data=load_private_source(npc_zip)
    selected={p:data[p] for p in PARAMETERS+[CREATE]};creates=[]
    for r in source['create_rows']:
        if r[0]!=CREATE:continue
        if sha(data[CREATE][r[2]:r[3]])!=r[4]:raise ValueError('Original CREATE slice mismatch')
        for path,_ in r[13]:selected[path]=data[path]
        creates.append({'file':r[0],'ordinal':r[1],'start_byte':r[2],'end_byte':r[3],
            'block_sha256':r[4],'floor':r[5],'graphic_alias':r[6],'borncorner_raw':r[7],
            'direction_raw':r[10],'template_token':r[11],'template_bindings':r[13],'parameter_references':r[15]})
    scripts=[{'path':p,'sha256':sha(data[p]),'events':source_events(data[p])} for p in PARAMETERS]
    prior_catalog=json.loads(CATALOG.read_text());prior_blocks=[]
    for s in scripts:
        old=[r for r in prior_catalog['source_event_blocks'] if r['script_path']==s['path']]
        if len(old)!=len(s['events']):raise ValueError('Prior TYPE population mismatch')
        for e,p in zip(s['events'],old):
            if (e['ordinal'],e['type_line'],e['type'])!=(p['script_block_ordinal'],p['source_type_line'],p['raw_type']):raise ValueError('Prior TYPE identity mismatch')
        prior_blocks.extend(old)
    ids=set()
    for s in scripts:
        for e in s['events']:
            ids.update(int(x) for x in re.findall(r'ITEM[!=<>]+(\d+)',e['event']))
            ids.update(o['item_id'] for c in e['commands'] for o in c['operands'])
    public_items={};pins={}
    for p in sorted((ROOT/'research/recovered/item-module-01').glob('*DERIVED-INDEX-*-R1.json')):
        matching=[r for r in json.loads(p.read_text())['rows'] if r[0] in ids]
        if matching:pins[p.relative_to(ROOT).as_posix()]=blob(p.read_bytes());public_items.update({r[0]:r for r in matching})
    if set(public_items)!=ids:raise ValueError('Unresolved selected item ID')
    out.mkdir(parents=True,exist_ok=True)
    for p,raw in selected.items():
        if raw.decode('cp950').encode('cp950')!=raw:raise ValueError('Source encoding mismatch')
        dest=out/'original'/p;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
    if sha(item_zip.read_bytes())!=ITEM_ARCHIVE_SHA:raise ValueError('ITEM01 archive mismatch')
    item_evidence=[];cards=[]
    with zipfile.ZipFile(item_zip) as z:
        if len(z.infolist())!=838 or z.testzip() is not None:raise ValueError('ITEM01 ZIP CRC/population')
        catalog=json.loads(z.read('private-full-catalog.json'))
        pixels={r['source_itemset_image_number_alias']:r for r in json.loads(z.read('private-RD-source-receipts.json'))['source_image_rows']}
        subset=[r for r in catalog['items'] if r['id'] in ids]
        (out/'private-item-catalog.json').write_text(json.dumps(subset,ensure_ascii=False,indent=2)+'\n')
        for item in subset:
            row=public_items[item['id']];evidence={'item_id':item['id'],'source_row_reconstructions':[]}
            for table,index in [('itemset.txt',1),('itemset0710.txt',2)]:
                if table not in item:
                    if row[index] is not None:raise ValueError('Missing catalog table row')
                    continue
                r=item[table];raw=','.join(r['original_94_columns']).encode('cp950')
                if sha(raw)!=r['original_row_sha256'] or sha(raw)!=row[index]:raise ValueError('Recovered complete original row mismatch')
                dest=out/'original-item-rows'/f'{table}-{item["id"]}.row';dest.parent.mkdir(exist_ok=True);dest.write_bytes(raw)
                evidence['source_row_reconstructions'].append({'table':table,'bytes':len(raw),'sha256':sha(raw)})
            r=item.get('itemset.txt',item.get('itemset0710.txt'));image_no=r['source_image_number']
            evidence.update(source_name_sha256=sha(r['source_name'].encode()),source_image_alias=image_no,
                            source_item01_numeric_row=row)
            icon=None
            if image_no in pixels and 'private_PNG' in pixels[image_no]:
                p=pixels[image_no];png=z.read('source-TW1-original-RD-candidates/'+p['private_PNG'])
                image=Image.open(io.BytesIO(png)).convert('RGBA')
                if sha(png)!=p['candidate_PNG_SHA256'] or sha(image.tobytes())!=p['candidate_RGBA_SHA256']:raise ValueError('Original item image mismatch')
                icon='icons/'+p['private_PNG'];target=out/icon;target.parent.mkdir(exist_ok=True);target.write_bytes(png)
                evidence['source_icon_receipt']=p
            else:
                evidence['source_icon_status']=pixels.get(image_no,{}).get('tw1_original_RD_status','NO_QUALIFIED_PIXEL_IN_THIS_ARCHIVE')
            evidence['qualified_icon_present']=icon is not None;item_evidence.append(evidence)
            cards.append('<article><h3>'+str(item['id'])+' '+html.escape(r['source_name'])+'</h3>'+
                         ('<img style="image-rendering:pixelated;max-width:180px" src="'+icon+'">' if icon else '<p>本來源原圖未取得</p>')+
                         '<p>'+html.escape(r['source_description'])+'</p></article>')
    prior_map=ROOT/'research/recovered/STONEAGE-MAP09-691-SOURCE-READY-SCENES-R1.json'
    if sha(map_zip.read_bytes())!=MAP_ARCHIVE_SHA:raise ValueError('MAP09 archive mismatch')
    map_evidence=[];panels=[]
    with zipfile.ZipFile(map_zip) as z:
        if z.testzip() is not None or len(z.infolist())!=4195:raise ValueError('MAP09 ZIP CRC/population')
        prior=json.loads(prior_map.read_text())
        if json.loads(z.read('scene-source-receipt.json'))!=prior:raise ValueError('MAP09 receipt mismatch')
        raw_zip=z.read('source-all-955-original-DAT.zip')
        if sha(raw_zip)!=prior['original_DAT_archive']['sha256']:raise ValueError('DAT archive mismatch')
        dz=zipfile.ZipFile(io.BytesIO(raw_zip))
        for floor in sorted({r['floor'] for r in creates}):
            raw=dz.read(str(floor)+'.dat');old=prior['maps'][str(floor)]
            if sha(raw)!=old['source_sha256']:raise ValueError('Original DAT mismatch')
            w,h=struct.unpack_from('<II',raw);n=w*h
            positions=[(r['ordinal'],r['borncorner_raw'][:2]) for r in creates if r['floor']==floor]
            points=[]
            thumb_bytes=z.read(f'thumbnails/{floor}.jpg');thumb=Image.open(io.BytesIO(thumb_bytes)).convert('RGB');draw=ImageDraw.Draw(thumb)
            sx,sy=thumb.width/old['canvas_size'][0],thumb.height/old['canvas_size'][1];ox,oy=old['origin']
            for label,(x,y) in positions:
                if not(0<=x<w and 0<=y<h):raise ValueError('Source point outside original DAT')
                values=[int.from_bytes(raw[8+2*(plane*n+y*w+x):10+2*(plane*n+y*w+x)],'little') for plane in range(3)]
                px,py=(ox+(x+y)*32)*sx,(oy+(y-x)*24)*sy
                draw.ellipse((px-4,py-4,px+4,py+4),outline='yellow',width=2)
                draw.text((px+6,py-8),str(label),fill='yellow')
                points.append({'source_create_ordinal_or_target':label,'xy':[x,y],'original_three_u16_values':values})
            (out/'original-DAT').mkdir(exist_ok=True);(out/'maps').mkdir(exist_ok=True)
            (out/'original-DAT'/f'{floor}.dat').write_bytes(raw);target=out/'maps'/f'{floor}-marked.jpg';thumb.save(target,quality=95)
            map_evidence.append({'floor':floor,'source_DAT_sha256':sha(raw),'source_DAT_bytes':len(raw),'geometry':[w,h],
                'prior_MAP09_thumbnail_sha256':sha(thumb_bytes),'marked_thumbnail_sha256':sha(target.read_bytes()),'source_points':points})
            panels.append('<figure><img src="maps/'+str(floor)+'-marked.jpg"><figcaption>來源floor '+str(floor)+'；圈標為現代原CREATE/目標點</figcaption></figure>')
    report={'schema':'stoneage.quest11.two_tribes_literal_source.r1','date':'2026-11-08',
        'origin_class':'ORIGIN_UNRESOLVED','source_scope':'LATER_COMMUNITY_MIXED25_NOT_AUTHENTICATED_OFFICIAL_DEPLOYMENT',
        'baseline':{'head':'492a80bbe435752a9c6a8dbc38d7ebcbce1d1c1b','tree':'f90d7221542124ff184b4946d135bd928b43973d',
                    'preserved_current_blob':'c89e0e33537990aa2132b47c40fef49a985a935c'},
        'private_source_zip_sha256':sha(archive),'verified_original_NPC_members':len(data),
        'source_files':[{'path':p,'bytes':len(b),'sha256':sha(b),'crc32':f'{zlib.crc32(b):08x}'} for p,b in sorted(selected.items())],
        'source_creates':creates,'source_event_scripts':scripts,
        'prior_QUEST01_TYPE_blocks_verified':len(prior_blocks),
        'source_item_evidence':item_evidence,'source_map_observations':map_evidence,
        'private_item_archive_sha256':ITEM_ARCHIVE_SHA,'private_map_archive_sha256':MAP_ARCHIVE_SHA,
        'derived_input_blobs':{**{p.relative_to(ROOT).as_posix():blob(p.read_bytes()) for p in [SOURCE,CATALOG,prior_map]},**pins},
        'boundaries':{k:False for k in ['native_execution_verified','complete_deployed_quest_chain_verified',
            'official_origin_verified','source_typos_repaired','condition_punctuation_interpreted',
            'implicit_item_quantity_assumed','source_order_claimed_runtime_priority','ore_sellers_claimed_warps',
            'new_original_RD_decodes','new_full_map_canvas_rendered','original_NPC_sprites_drawn','same_official_deployment_verified']},
        'status':{'stage_A':'7_PARTIAL_2_OPEN','stage_B_wiki':'GATED','R79':'PAUSED_NON_BLOCKING','overall_percent':None}}
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');(out/'source-evidence.json').write_bytes(REPORT.read_bytes())
    originals=''.join('<details><summary>'+html.escape(p)+'</summary><pre>'+html.escape(b.decode('cp950'))+'</pre></details>' for p,b in sorted(selected.items()))
    (out/'index.html').write_text('<!doctype html><html lang="zh-Hans"><meta charset="utf-8"><title>两族误会原文资料</title>'
        '<style>body{max-width:1100px;margin:30px auto;background:#f4f0e5;color:#24362d;font:17px system-ui}pre{white-space:pre-wrap;background:white;padding:18px}summary{padding:12px;cursor:pointer}article,figure{display:inline-block;vertical-align:top;margin:12px;padding:12px;max-width:480px;background:white}img{max-width:100%}</style>'
        '<h1>两族误会：原文、道具与位置</h1><p>后期社群 mixed25 保存材料。8份事件参数、8个CREATE点。garunaev7/8为矿石商人，非入口传送配置。原文仍保留繁体及异常字。这里只整理来源，未执行原游戏。</p>'
        '<h2>任务阅读顺序</h2><ol><li>garunaev2/5：翻译海螺与23/24入口分支。</li><li>garunaev3/6：两只乌力的关系与沟通。</li><li>garunaev1/4：25/26书信交接与两方矿石。</li><li>garunaev7/8：完成标志后的矿石购买参数。</li><li>garunaev3/6：两种矿石合成；garunaev6另有手环对话。</li><li>族长的2391/2393/2395后续协议段，保持跨任务候选。</li></ol>'
        '<p>原字段 EvebtNo、NomalWinodowMsg、NOEEV=24、ITEM=1 及重复条件均未修正。裸ID不补数量。源文件次序不等于已验证运行优先级。道具名沿用各候选表，不按对话改名。</p>'
        '<h2>原来源位置缩图</h2>'+''.join(panels)+'<h2>完整原道具行与既存TW1像素候选</h2>'+''.join(cards)+'<h2>原文件全文</h2>'+originals+'</html>',encoding='utf-8')
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ['npc_zip','item_zip','map_zip','private_output']:p.add_argument(name,type=Path)
    a=p.parse_args();r=extract(a.npc_zip,a.item_zip,a.map_zip,a.private_output)
    print(json.dumps({'source_files':len(r['source_files']),'event_blocks':sum(len(s['events']) for s in r['source_event_scripts']),
        'creates':len(r['source_creates']),'items':len(r['source_item_evidence']),'maps':len(r['source_map_observations'])}))
