"""QUEST16 source-bound axe, water-carrier and wood-trading contracts.

Private source inputs are separately custody-qualified.  Only publish numeric
control fields, original-source SHA/CRC and cross-source qualification limits.
Do not check in original Chinese dialogue, DAT, proprietary PNG or ZIP bytes.
"""
from __future__ import annotations

import hashlib
import json
import re
import struct
import zipfile
import zlib
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'research/recovered/STONEAGE-QUEST16-AXE-WOOD-SOURCE-R1.json'
CREATE = 'jaruga/event/20501ev.create'
SCRIPTS = [f'jaruga/event/20501ev{i}' for i in range(1, 6)]
TEMPLATE = 'jaruga/event/event.template'
FILES = [CREATE, *SCRIPTS, TEMPLATE]
ITEM_IDS = (1837, 1838, 2463, 2464, 2465, 2466, 2467, 2468, 2478, 2481, 2484, 2485)
SOURCE_MAPS = {
    20507: ('6a505b453c2ec229f9f15030971bb59e62a1eca1ba5334d84d531ce7f6fc85ec', [60,60]),
    20508: ('8f31c2a188b47fa5f0470f2cb357c0edc3dffefc5ba7ed2f3a8dd9f539e56a2e', [25,25]),
    3300: ('7f47b7ff641e2eb58d8d944741cd1fb6227f21bdd96a2d9fa7b8cc9d91a381e8', [120,120]),
}
MAP09_PUBLIC_BLOB = '137580e7c25aadf3d679b6ebfb5080b79912cc4f'
QUEST01_PUBLIC_BLOB = '52db8b4b6cd43cd2afa4a8d2e8460f214933f5e2'
NPC_ORIGINAL_ARCHIVE_SHA = 'c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f'
ITEM_ORIGINAL_ARCHIVE_SHA = 'cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa'
ORIGINAL_PARENT_RAR_SHA = 'd71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5'


def sha(data:bytes)->str:
    return hashlib.sha256(data).hexdigest()


def git_blob(data:bytes)->str:
    return hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()


def crc(data:bytes)->str:
    return f'{zlib.crc32(data)&0xffffffff:08x}'


def parse_events(raw:bytes)->list[dict]:
    """Only semantic command grammar, not copyrighted dialogue paragraphs."""
    source=raw.decode('cp950','strict').replace('\r\n','\n')
    out=[]
    for n,m in enumerate(re.finditer(r'(?m)^EventNo:(-?\d+)\s*$',source)):
        end=re.search(r'(?m)^EventEnd\s*$',source[m.start():])
        if end is None:raise ValueError('source event missing EventEnd')
        section=source[m.start():m.start()+end.end()]
        ty=re.search(r'(?m)^TYPE:(\w+)\s*$',section)
        pred=re.search(r'(?m)^EVENT:(.*)$',section)
        if ty is None or pred is None:raise ValueError('source event incomplete')
        actions={k:[x.group(1).strip() for x in re.finditer(rf'(?m)^\s*{k}:([^\r\n]*)',section)]
                 for k in ('GetItem','DelItem','GetStone','DelStone','GetRandItem','EndSetFlg','GetPet','DelPet')}
        out.append(dict(ordinal=n,event_no=int(m.group(1)),type=ty.group(1),
          predicate=pred.group(1),predicate_sha256=sha(pred.group(1).encode()),
          section_sha256=sha((section.rstrip('\n')+('\n' if section.endswith('\n') else '')).encode()),
          controls={k:v for k,v in actions.items() if v},
          literal_EventEnd_present=True))
    return out


def parse_creates(raw:bytes)->list[dict]:
    out=[]
    for i,m in enumerate(re.finditer(rb'\{[^{}]*\}',raw)):
        b=raw[m.start():m.end()]
        d=b.decode('cp950','strict')
        keys=dict(re.findall(r'(?m)^\s*([A-Za-z_]+)\s*=\s*(.+?)\s*$',d))
        x=[int(v) for v in keys['borncorner'].split(',')]
        ref=keys['enemy'].split('file:',1)[1]
        out.append(dict(ordinal=i,source_offset_start=m.start(),source_offset_end_exclusive=m.end(),
            original_block_sha256=sha(b),name_original=keys['name'],floor=int(keys['floorid']),
            borncorner=x,graphic_alias=int(keys['graphicname']),direction=int(keys['dir']),
            function='changeevent',script_ref=ref))
    return out


def read_map_cell(original_dat:bytes,x:int,y:int)->list[int]:
    """Safe parser only. Not used to claim QUEST16 original DAT cells were re-read."""
    w,h=struct.unpack_from('<II',original_dat,0)
    if w<=0 or h<=0 or len(original_dat)!=8+6*w*h:raise AssertionError('DAT geometry')
    if not(0<=x<w and 0<=y<h):raise AssertionError('DAT point outside grid')
    idx=x+y*w
    return [struct.unpack_from('<H',original_dat,8+2*(idx+p*w*h))[0] for p in range(3)]


def derive(private_source_dir:Path)->tuple[dict,dict[str,bytes]]:
    npc_path=private_source_dir/'StoneAge-CHAR01-mixed25-all-npc-original-private.zip'
    item_path=private_source_dir/'StoneAge-ITEM01-private-two-itemsets-832-original-RD-icon-observer.zip'
    quest01_path=private_source_dir/'STONEAGE-QUEST01-PUBLIC-INDEX-MINIFIED-R1.json'
    # These two item shards may also be obtained from public main at their exact paths.
    item_index_paths={i:private_source_dir/f'STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-0{i}-R1.json' for i in (1,2)}
    assert sha(npc_path.read_bytes())==NPC_ORIGINAL_ARCHIVE_SHA
    assert sha(item_path.read_bytes())==ITEM_ORIGINAL_ARCHIVE_SHA
    q=json.loads(quest01_path.read_text())
    prior={x['path']:x for x in q['source_scripts']}
    legacy_refs=[x for x in q['source_creation_references'] if x['create_source_path']==CREATE]
    assert len(legacy_refs)==5
    refs={x['original_script_path']:x for x in legacy_refs}
    prior_controls={(x['script_path'],x['script_block_ordinal']):x for x in q['source_event_blocks']
                    if x['script_path'] in SCRIPTS}
    assert len(prior_controls)==36
    private={}
    with zipfile.ZipFile(npc_path) as z:
        assert z.testzip() is None
        names=z.namelist()
        assert len(names)==2205
        selected={f:z.read('npc/'+f) for f in FILES}
        for p,data in selected.items():private['original/npc/'+p]=data
        creates=parse_creates(selected[CREATE]); assert len(creates)==5
        for create in creates:
            r=refs[create['script_ref']]
            assert (r['create_brace_ordinal'],r['floorid'],r['graphic_alias_numeric'])==(create['ordinal'],create['floor'],create['graphic_alias'])
        scripts=[]
        for path in SCRIPTS:
            raw=selected[path]
            assert sha(raw)==prior[path]['original_sha256']
            assert crc(raw)==prior[path]['original_crc32']
            events=parse_events(raw)
            for e in events:
                old=prior_controls[path,e['ordinal']]
                assert (e['type'],e['event_no'],e['predicate_sha256'],e['section_sha256'])==(old['raw_type'],old['event_number'],old['condition_expression_decoded_cp950_UTF8_sha256'],old['source_section_decoded_cp950_normalized_UTF8_sha256'])
            scripts.append(dict(path=path,bytes=len(raw),sha256=sha(raw),crc32=crc(raw),events=events))
        assert sum(len(v['events']) for v in scripts)==36
    with zipfile.ZipFile(item_path) as z:
        assert z.testzip() is None
        catalog=json.loads(z.read('private-full-catalog.json'))
        item_entries={v['id']:v for v in catalog['items'] if v['id'] in ITEM_IDS}
        assert set(item_entries)==set(ITEM_IDS)
        image_index={i['source_itemset_image_number_alias']:i for i in catalog['image_source_receipts']}
        shards={i:{x[0]:x for x in json.loads(path.read_text())['rows']} for i,path in item_index_paths.items()}
        items=[];image_paths={}
        for item_id in ITEM_IDS:
            x=item_entries[item_id]
            public=shards[1 if item_id<2004 else 2][item_id]
            sources=[]
            for table,shapos in [('itemset.txt',1),('itemset0710.txt',2)]:
                v=x[table]; cols=v['original_94_columns']
                assert len(cols)==94 and int(cols[16])==item_id
                raw=','.join(cols).encode('cp950','strict')
                assert sha(raw)==v['original_row_sha256']==public[shapos]
                name=f'original/itemrows/{table}/{item_id}-row{v["source_row_1based"]}.txt'
                private[name]=raw+b'\n'
                sources.append(dict(table=table,row=v['source_row_1based'],sha256=sha(raw),columns=94,
                    graphic_alias=int(cols[17])))
            assert sources[0]['graphic_alias']==sources[1]['graphic_alias']
            alias=sources[0]['graphic_alias']
            img=image_index.get(alias)
            if not img or img.get('tw1_original_RD_status')!='VERIFIED_ORIGINAL_RD_INDEXED_PIXELS':
                raise AssertionError(f'Missing qualified cross-carrier original bitmap for alias {alias}')
            pixname=f'source-TW1-original-RD-candidates/alias-{alias}.png'
            pic=z.read(pixname)
            image_paths[alias]=dict(alias=alias,sha256=sha(pic),bytes=len(pic))
            private['cross-carrier-TW1-original-RD-candidates/'+f'alias-{alias}.png']=pic
            items.append(dict(item_id=item_id,source_original_name= x['itemset.txt']['original_94_columns'][0],
                source_rows=sources,graphic_alias=alias,cross_carrier_TW1_candidate_image_sha256=sha(pic),
                official_same_deployment_unproven=True))
    # All 14 source GetStone amounts remain static strings. Do not assign runtime pricing formula.
    merchant=[x for x in scripts if x['path'].endswith('20501ev5')][0]['events']
    tiers=[]
    for ev in merchant:
        if 'GetStone' not in ev['controls']:continue
        pred=re.search(r'(?<!\w)ITEM=2468\*(\d+)(?!\d)',ev['predicate'])
        assert pred is not None
        tiers.append(dict(quantity_literal=int(pred.group(1)),
            source_getstone_literal=ev['controls']['GetStone'][0],
            original_delitem_literals=ev['controls'].get('DelItem',[]),
            event_ordinal=ev['ordinal']))
    assert sorted(x['quantity_literal'] for x in tiers)==list(range(1,15))
    # Source 12-wood tier omits item 2467, unlike most neighboring tiers. Preserve.
    assert next(x for x in tiers if x['quantity_literal']==12)['original_delitem_literals']==['2468,2478']
    preexisting_ids=set(ITEM_IDS)
    report=dict(schema='stoneage.quest16.axe_wood_lumber_original_source_bound.r1',
        source_scope='MIXED25_COMMUNITY_COMBINED_PRESERVATION_NOT_OFFICIAL_EARLY_VERSION',
        original_RAR_sha256=ORIGINAL_PARENT_RAR_SHA,
        original_NPC_archive_sha256=NPC_ORIGINAL_ARCHIVE_SHA,
        original_NPC_zip_member_count=2205,
        original_ITEM01_archive_sha256=ITEM_ORIGINAL_ARCHIVE_SHA,
        original_source_QUEST01_public_blob=QUEST01_PUBLIC_BLOB,
        historical_current_state_blob='c89e0e33537990aa2132b47c40fef49a985a935c',
        source_files=[dict(path=f,bytes=len(private['original/npc/'+f]),sha256=sha(private['original/npc/'+f]),crc32=crc(private['original/npc/'+f])) for f in FILES],
        source_creates=creates,
        source_event_blocks=scripts,
        source_event_total=sum(len(x['events']) for x in scripts),
        item_count=len(items),items=items,source_item_rows=len(items)*2,
        original_TW1_cross_carrier_images=[image_paths[k] for k in sorted(image_paths)],
        original_TW1_cross_carrier_unique_image_count=len(image_paths),
        original_getstone_wood_tiers=sorted(tiers,key=lambda x:x['quantity_literal']),
        source_map_qualification=dict(map09_public_git_blob=MAP09_PUBLIC_BLOB,
          source_qualified_floors=[dict(floor=f,source_dat_sha256=SOURCE_MAPS[f][0],geometry=SOURCE_MAPS[f][1],
             original_DAT_bytes_not_read_this_work_unit=True) for f in SOURCE_MAPS],
          not_observed_floor=3000,
          not_observed_floor_reason='NOT_IN_THE_691_MAP09_SOURCE_READY_LEDGER_OR_60_MAP10_ADDITIONS',
          actual_three_plane_values_measured_this_work_unit=0),
        source_work_scope=dict(actual_source_scripts_read=7,create_points=5,event_blocks=36,
          stage='SOURCE_BOUNDED_STATIC_NOT_RUNTIME',quest_origin='UNRESOLVED',
          merchant_amounts_are_script_literals_not_proven_runtime_prices=True,
          original_game_started=False,official_same_deployment_confirmed=False,
          original_DAT_bytes_newly_recovered=0),
        remaining_open=['original_3000_DAT_payload','actual_20507_20508_3300_DAT_cells_not_replayed_this_round',
                        'native_predicate_order_branch_selection','quantity_semantics_of_bare_DelItem',
                        'actual_wood_payment_tiers_and_currency','historical_early_official_origin'],
        stage_A={'PARTIAL':7,'OPEN':2},stage_B='GATED',wiki='GATED',R79='PAUSED_NON_BLOCKING',overall_percent=None)
    # The private source custody summary is the same public JSON; original text remains sealed.
    private['source-summary.json']=json.dumps(report,ensure_ascii=False,indent=2).encode('utf-8')+b'\n'
    return report,private


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument('--private-dir',type=Path,required=True)
    p.add_argument('--output',type=Path,default=SOURCE)
    p.add_argument('--private-zip',type=Path)
    a=p.parse_args()
    r,private=derive(a.private_dir)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
    if a.private_zip:
        a.private_zip.parent.mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(a.private_zip,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8) as z:
            for name in sorted(private):z.writestr(name,private[name])
    print('create',len(r['source_creates']),'events',r['source_event_total'],'items',r['item_count'],'png',r['original_TW1_cross_carrier_unique_image_count'])
