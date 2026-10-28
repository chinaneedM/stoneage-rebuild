"""One source-qualified room shop linkage, not original server interaction.
Private export reads exact original members and one candidate NPC bitmap.
Public replay checks derived metadata only; original scripts and pixels stay private.
"""
from __future__ import annotations
import argparse,base64,hashlib,io,json,re,struct,zlib
from pathlib import Path
from tools.stoneage_private_scene_actor_r7 import PINS,authenticate,need,sha
from tools.stoneage_private_scene_graphic_join_r1 import resolve_ids
from tools.stoneage_private_scene_palette_r3 import candidate_rgba
from tools.stoneage_tw10_palette import initial_rgb
from tools.stoneage_preserved_item_shop_r44 import parse_items,arg_fields,inventory_tokens,INDEX
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'research/recovered/STONEAGE-SCENE14-ROOM-SHOP-SOURCE-R1.json'
MEMBERS={
 'npc/genout/shop_m.create':(20491,'d540e9a1354a0f82839cd30ab315a6dee4a3b0299744a0f63ae5ee461c5b587b'),
 'npc/genout/npcgen.template':(4950,'0c5a58d5e31cafd3b58ccc1fa88fee7d1f95d12c0b87b04db9f06fea3b2a4df3'),
 'npc/genout/ss_1001_17_13':(543,'f907e77774bc66151465f47e000852a598b935890f2b3334b6a8552f189b279a'),
 'itemset.txt':(3392473,'a415e78f9aab2e5ea5ca92ecb7430253f7be1ba7c876d6b0bb6d067b1b466688'),
 'client-map/1001.dat':(5408,'62dbef1614ede0ba032ca9c69cbfdc3d43938e45baba78701885790937b86b90')}
SOURCE_DERIVED_SHA='2cea071e768a77c10278182743f839329ecc8c82841523b911cadc3c5447cb99'
PRIOR_HTML_SHA='ae82aa61120b08a14c9e1b3f3b939a36a9649dba97af555ed1a0ed274f36d99f'
IDS=[0,4,10,20,40,100,110,130,200,210,220,240,300,310,330,600,620]
FALSE=('same_deployed_build_authenticated','official_tw10_npc_authenticated','original_server_executed',
 'original_world_entered','original_transaction_verified','original_native_occlusion_verified',
 'script_dialogue_published','original_frame_or_camera_verified')

def blocks(raw,magic):
    need(raw.splitlines()[0]==magic,'original config magic')
    result=[]
    for m in re.finditer(rb'(?ms)^\{\r?\n.*?^\}',raw):
        fields={};rows=[]
        for line in m.group().splitlines()[1:-1]:
            if not line.strip() or line.lstrip().startswith(b'#'):continue
            need(b'=' in line,'unsupported config assignment')
            k,v=line.split(b'=',1);k=k.strip().decode('ascii');v=v.strip()
            need(k not in fields,'duplicate config field requires separate semantics');fields[k]=v
            rows.append({'key':k,'value_bytes':len(v),'value_sha256':sha(v)})
        result.append({'ordinal':len(result),'byte_start':m.start(),'byte_end':m.end(),
          'block_sha256':sha(m.group()),'fields':fields,'field_fingerprints':rows})
    need(len(result)>0 and len(re.findall(rb'(?m)^\{\r?$',raw))==len(result)==len(re.findall(rb'(?m)^\}\r?$',raw)),'incomplete or unmatched source blocks');return result

def public_block(b):return {k:v for k,v in b.items() if k!='fields'}

def derive(members):
    for n,p in MEMBERS.items():need((len(members[n]),sha(members[n]))==p,'original whole member '+n)
    create=blocks(members['npc/genout/shop_m.create'],b'NPCCREATE')
    selected=[b for b in create if b['fields'].get('floorid')==b'1001' and b['fields'].get('borncorner')==b'17,13,17,13']
    need(len(selected)==1,'unique room1001 weapon shop source block');c=selected[0];f=c['fields']
    need(f['enemy']==b'npcgen_shop|file:genout/ss_1001_17_13','exact parameter dependency, not filename inference')
    templates=blocks(members['npc/genout/npcgen.template'],b'NPCTEMPLATE')
    selected=[b for b in templates if b['fields'].get('templatename')==b'npcgen_shop']
    need(len(selected)==1,'unique original named template');t=selected[0]
    need(t['fields']['functionset']==b'ItemShop','source template functionset')
    fields=arg_fields(members['npc/genout/ss_1001_17_13']);tokens=inventory_tokens(fields['itemlist'])
    need(tokens==[[n,n] for n in IDS],'all17 original stock positions')
    rows,count=parse_items(members['itemset.txt']);need(count==13252 and set(IDS)<=set(rows),'configured table actual IDs')
    items=[]
    for id in IDS[:3]:
        line,offset,body,columns=rows[id];name=columns[INDEX['name']]
        need(name.decode('cp950')==name.decode('big5'),'original name codec consensus')
        items.append({'id':id,'physical_line':line,'byte_offset':offset,'row_sha256':sha(body),
          'name_original':name.decode('cp950'),'name_raw_sha256':sha(name),
          'numeric_fields':{k:int(columns[INDEX[k]]) for k in ['imagenumber','cost','level','type']}})
    dat=members['client-map/1001.dat'];w,h=struct.unpack_from('<II',dat);need((w,h)==(30,30) and len(dat)==8+w*h*6,'room DAT identity')
    cells=[struct.unpack_from('<H',dat,8+2*(plane*w*h+13*w+17))[0] for plane in range(3)]
    name=f['name'];need(name.decode('cp950')==name.decode('big5'),'NPC original name codec consensus')
    return {'schema':'stoneage.scene14.room_shop_actual_source.r1',
      'scope':'PRESERVED_MIXED25_SAME_CARRIER_STATIC_LINKS_NOT_AUTHENTICATED_OFFICIAL_DEPLOYMENT',
      'source_members':{n:{'bytes':len(b),'sha256':sha(b),'crc32':zlib.crc32(b)&0xffffffff} for n,b in members.items()},
      'create_blocks_in_original_file':len(create),'template_blocks_in_original_file':len(templates),
      'selected_create':public_block(c),'selected_template':public_block(t),
      'npc':{'original_name':name.decode('cp950'),'name_raw_sha256':sha(name),'floor':int(f['floorid']),
        'borncorner':[int(n) for n in f['borncorner'].split(b',')],'direction':int(f['dir']),
        'graphicname':int(f['graphicname']),'createnum':int(f['createnum']),'time':int(f['time']),
        'template':'npcgen_shop','functionset':'ItemShop','argument_file':'genout/ss_1001_17_13'},
      'arg_field_fingerprints':{k:{'bytes':len(v),'sha256':sha(v)} for k,v in fields.items()},
      'listed_item_ids':IDS,'listed_defined_count':17,'item_table_rows':count,
      'first_three_selection':'ORIGINAL_ARGUMENT_ORDER_BEFORE_NAME_DECODING','selected_items':items,
      'rates_raw':{k:fields[k].decode('ascii') for k in ['buy_rate','sell_rate','special_rate']},
      'limit_item_type_raw':fields['limititemtype'].decode('ascii'),'limit_item_no_empty':fields['limititemno']==b'',
      'map':{'width':w,'height':h,'npc_cell_xy':[17,13],'original_three_u16_at_cell':cells,'third_plane_semantics':'NOT_ASSUMED_WALKABILITY_OR_SHOP_TRIGGER'},
      'computed_runtime_prices':None,'original_welcome_or_dialogue_published':False,
      **{k:False for k in FALSE},'overall_completion_percent':None}

def validate(r):
    need(sha(json.dumps(r,sort_keys=True,separators=(',',':')).encode())==SOURCE_DERIVED_SHA,'exact authenticated source-derived metadata')
    need(r['schema']=='stoneage.scene14.room_shop_actual_source.r1','schema')
    need(r['scope']=='PRESERVED_MIXED25_SAME_CARRIER_STATIC_LINKS_NOT_AUTHENTICATED_OFFICIAL_DEPLOYMENT','scope')
    need(set(r['source_members'])==set(MEMBERS),'finite source member set')
    for n,p in MEMBERS.items():need((r['source_members'][n]['bytes'],r['source_members'][n]['sha256'])==p,'original member chain')
    n=r['npc'];need(n=={'original_name':'薩姆吉爾的武器店','name_raw_sha256':sha('薩姆吉爾的武器店'.encode('cp950')),'floor':1001,'borncorner':[17,13,17,13],'direction':6,'graphicname':16017,'createnum':1,'time':0,'template':'npcgen_shop','functionset':'ItemShop','argument_file':'genout/ss_1001_17_13'},'exact NPC authored binding')
    need(r['listed_item_ids']==IDS and r['listed_defined_count']==17 and r['item_table_rows']==13252,'all source stock IDs, zero is valid')
    need(r['first_three_selection']=='ORIGINAL_ARGUMENT_ORDER_BEFORE_NAME_DECODING' and [x['id'] for x in r['selected_items']]==IDS[:3],'unbiased finite sample')
    for item in r['selected_items']:
        need(sha(item['name_original'].encode('cp950'))==item['name_raw_sha256'],'original name bytes')
    need(r['rates_raw']=={'buy_rate':'1.0','sell_rate':'0.2','special_rate':'1.5'} and r['limit_item_type_raw']=='OFFENCE' and r['limit_item_no_empty'] is True,'do not invent transaction semantics')
    need(r['map']['npc_cell_xy']==[17,13] and (r['map']['width'],r['map']['height'])==(30,30) and len(r['map']['original_three_u16_at_cell'])==3,'same-carrier map bounds')
    need(r['computed_runtime_prices'] is None and r['original_welcome_or_dialogue_published'] is False and all(r[k] is False for k in FALSE) and r['overall_completion_percent'] is None,'historical boundaries')
    return {'same_carrier_npc_config_links':1,'authored_cell':[17,13],'listed_item_ids':17,'named_item_sample':3,'original_server_execution':False}

def validate_acceptance(a,r):
    need(a['schema']=='stoneage.scene14.local_source_and_browser_acceptance.r1' and a['scope']=='PRIVATE_OFFLINE_SOURCE_OBSERVER_NOT_ORIGINAL_GAME_SERVER','acceptance scope')
    need(a['source_report_sha256']==sha(REPORT.read_bytes()),'source metadata identity')
    need(a['loaded_images']==11 and a['selected_item_rows_visible']==3 and a['source_inspector_opened_by_button_and_image_click'] is True,'actual browser inspection')
    need(a['JS_errors']==[] and a['external_requests']==[],'browser errors or network')
    need(set(a['all_five_original_members_equal'])==set(MEMBERS),'independent five-member extraction')
    for name,row in a['all_five_original_members_equal'].items():
        need((row['bytes'],row['sha256'])==MEMBERS[name] and row['same_bytes_as_unar'] is True,'two decoders original bytes')
    need(a['raw_source_second_derivation_equal'] is True and a['independent_RD_indices_RGBA_PNG_equal'] is True,'independent source/pixel replay')
    need(a['independent_integer_scale_full_RGBA_matches']==4 and a['independent_integer_scale_states']==['default','npc_hidden','anchor_hidden','map_only'],'four exact whole canvas states')
    browser={f['label']:f['canvas_sha256'] for f in a['browser_states']}
    refs={f['label']:f['canvas_sha256'] for f in a['independent_replay']['frames']}
    need(len(browser)==5 and set(browser)=={'default','npc_hidden','anchor_hidden','map_only','zoom_2_5'},'retain every observed browser state')
    for label in a['independent_integer_scale_states']:
        need(browser[label]==refs[label] and re.fullmatch('[0-9a-f]{64}',browser[label]) is not None,'exact canvas '+label)
    need(a['independent_replay']['fractional_scale_full_pixel_match'] is False and browser['zoom_2_5']!=refs['zoom_2_5'],'fractional reference mismatch must remain visible')
    need(a['private_source_ci_run_id'] is None and a['public_CI_reads_private_pixels_or_scripts'] is False and a['original_world_entered'] is False and a['original_transaction_executed'] is False and a['official_same_build_authenticated'] is False and a['overall_completion_percent'] is None,'no source CI/runtime promotion')
    return {'independent_extractors':2,'private_images':11,'exact_integer_scale_full_canvas_matches':4,'fractional_scale_independent_pixel_match':False}

def export(source,art,prior,target):
    from PIL import Image
    target=target.resolve();need(ROOT!=target and ROOT not in target.parents and not target.exists(),'new private output outside Git')
    members={n:(source/n).read_bytes() for n in MEMBERS};report=derive(members)
    prior_raw=prior.read_bytes();need(sha(prior_raw)==PRIOR_HTML_SHA,'private accepted R13 source page')
    pack=json.loads(prior_raw.split(b'<script id="evidence" type="application/json">')[1].split(b'</script>')[0]);room=pack['room']
    need(room['source_dat_sha256']==MEMBERS['client-map/1001.dat'][1] and room['floor']==1001,'actual source room match')
    for name in ['adrn_15.bin','real_15.bin','Palet_1.sap']:authenticate(art/name,PINS[name])
    matches=resolve_ids((art/'adrn_15.bin').read_bytes(),{16017},PINS['real_15.bin'][0])[16017];need(len(matches)==1,'unique numeric alias candidate, no last-wins')
    b=matches[0]
    with (art/'real_15.bin').open('rb') as f:f.seek(b['offset']);rd=f.read(b['size'])
    hdr,px=decode(rd,b);rgba=candidate_rgba(px,b['width'],b['height'],initial_rgb((art/'Palet_1.sap').read_bytes()))
    im=Image.frombytes('RGBA',(b['width'],b['height']),rgba);out=io.BytesIO();im.save(out,format='PNG');png=out.getvalue()
    b.update(RD_sha256=sha(rd),index_pixels_sha256=sha(px),candidate_RGBA_sha256=sha(rgba),PNG_sha256=sha(png),binding='SAME_CARRIER_EQUAL_NUMERIC_GRAPHIC_KEY_NOT_NATIVE_RENDER_PROOF')
    report['candidate_graphic']=b;report['private_prior_html_sha256']=PRIOR_HTML_SHA
    validate(report)
    private={'room':room,'source':report,'npc_image':base64.b64encode(png).decode(),
      'welcome_original_parameter':arg_fields(members['npc/genout/ss_1001_17_13'])['main_msg'].decode('cp950')}
    template=(ROOT/'tools/scene-room-shop-viewer-r14.html').read_text();need(template.count('"PRIVATE_PACK_PLACEHOLDER"')==1,'template marker')
    html=template.replace('"PRIVATE_PACK_PLACEHOLDER"',json.dumps(private,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c'))
    target.mkdir(parents=True,mode=0o700);(target/'stoneage-room-r14-shop-observer.html').write_text(html)
    (target/'source-derived-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    (target/'private-npc-5863.rd').write_bytes(rd);(target/'private-palette.sap').write_bytes((art/'Palet_1.sap').read_bytes());return report

def decode(rd,b):
    from tools.stoneage_rd_codec import decode_rd_block
    need(len(rd)==b['size'],'short original RD');h,px=decode_rd_block(rd,authoritative_block_size=b['size'])
    need((h['width_s'],h['height_s'])==(b['width'],b['height']),'source geometry');return h,px

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source-dir',type=Path);p.add_argument('--art-dir',type=Path);p.add_argument('--prior-html',type=Path);p.add_argument('--output-dir',type=Path);a=p.parse_args()
    if a.source_dir:r=export(a.source_dir,a.art_dir,a.prior_html,a.output_dir)
    else:r=json.loads(REPORT.read_bytes())
    result=validate(r)
    if not a.source_dir:result['archived_acceptance']=validate_acceptance(json.loads((ROOT/'research/recovered/STONEAGE-SCENE14-ACCEPTANCE-R1.json').read_bytes()),r)
    print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
