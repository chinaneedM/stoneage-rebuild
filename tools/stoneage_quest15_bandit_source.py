"""QUEST15: source-bounded extraction of retained mixed25 event20 controls.

The private source ZIP is never added to the public repository. Public tests
validate only the derived numeric/source-hash ledger. This is NOT game runtime.
"""
from __future__ import annotations

import hashlib
import json
import re
import zipfile
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'research/recovered/STONEAGE-QUEST15-BANDIT-EVENT20-ORIGINAL-SOURCE-R1.json'
NPC_ZIP_SHA = 'c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f'
ITEM_ZIP_SHA = 'cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa'
CREATE_PATH = 'jaruga/event/event20.create'
SCRIPTS = [f'jaruga/event/event20_{n}' for n in range(1, 7)]
TEMPLATE = 'jaruga/event/event.template'
ITEM_IDS = list(range(2486, 2495))
LATER_BRANCH_IDS = [2744, 2745]
# Exact qualified source DAT hashes from existing public MAP09 (not reread this unit).
PRIOR_MAP09 = {
    3406: ('8e643f9c8c37040af1e753dc8ec4a52d72a3994af215b24ef53236188c35e802', [40,30]),
    20607: ('61030ae7ad974ec396074f3bb7a44c3741694be093fb91abec145392a8a67845', [80,60]),
    20608: ('c557d48683e1b2ee361a6d35bf2f67ff28f2b016e1e90062567ead1514653612', [15,15]),
}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f'{zlib.crc32(raw) & 0xffffffff:08x}'


def parse_events(raw: bytes) -> list[dict]:
    """Keep original control grammar, omit copyrighted narrative/dialogue."""
    source = raw.decode('cp950', 'strict').replace('\r\n', '\n')
    starts = list(re.finditer(r'(?m)^EventNo:(-?\d+)\s*$', source))
    out = []
    keys = ('GetItem', 'DelItem', 'GetRandItem', 'EndSetFlg', 'GetPet', 'DelPet', 'DelStone')
    for ordinal, match in enumerate(starts):
        end = re.search(r'(?m)^EventEnd\s*$', source[match.start():])
        if end is None:
            raise ValueError('unbounded event block')
        section = source[match.start():match.start()+end.end()]
        typ = re.search(r'(?m)^TYPE:(\w+)\s*$', section)
        pred = re.search(r'(?m)^EVENT:(.*)$', section)
        if not typ or not pred:
            raise ValueError('event without TYPE/EVENT')
        controls = {k:[m.group(1) for m in re.finditer(rf'(?m)^{k}:(.*)$', section)] for k in keys}
        out.append({
            'ordinal': ordinal, 'event_no': int(match.group(1)),
            'type': typ.group(1), 'predicate': pred.group(1),
            'predicate_sha256': sha(pred.group(1).encode('utf-8')),
            'section_sha256': sha((section.rstrip('\n') + '\n').encode('utf-8')),
            'actions': {k:v for k,v in controls.items() if v},
            'explicit_end_present': True,
        })
    return out


def parse_creates(raw: bytes) -> list[dict]:
    content = raw.decode('cp950','strict')
    result=[]
    for ordinal, m in enumerate(re.finditer(rb'\{[^{}]*\}', raw)):
        block=m.group().decode('cp950','strict')
        fields=dict(re.findall(r'(?m)^([A-Za-z]+)\s*=\s*(.+?)\s*$',block))
        floor=int(fields['floorid'])
        xy=[int(x) for x in fields['borncorner'].split(',')]
        ref=fields['enemy'].split('file:',1)[1]
        result.append({
            'ordinal': ordinal, 'source_offset_start': m.start(),
            'source_offset_end_exclusive': m.end()+1,
            'source_block_sha256': sha(raw[m.start():m.end()+1]),
            'source_floor':floor, 'source_borncorner':xy,
            'graphic_alias_not_image_identity':int(fields['graphicname']),
            'direction':int(fields['dir']), 'script_ref':ref,
            'function':'changeevent',
        })
    if [x['script_ref'] for x in result]!=SCRIPTS:
        raise AssertionError('unexpected original create/script order')
    return result


def derive(npc_zip: Path, item_zip: Path, quest01_index: Path, item_index: Path) -> tuple[dict,dict[str,bytes]]:
    if sha(npc_zip.read_bytes())!=NPC_ZIP_SHA or sha(item_zip.read_bytes())!=ITEM_ZIP_SHA:
        raise ValueError('private source ZIP identity mismatch')
    quest01=json.loads(quest01_index.read_text(encoding='utf-8'))
    item_public=json.loads(item_index.read_text(encoding='utf-8'))
    public_item={int(row[0]):row for row in item_public['rows']}
    prior={}
    for entry in quest01['source_event_blocks']:
        if entry['script_path'] in SCRIPTS:
            prior[(entry['script_path'],entry['script_block_ordinal'])]=entry
    outputs={}
    with zipfile.ZipFile(npc_zip) as z:
        assert len(z.namelist())==2205 and z.testzip() is None
        source_files=[]
        for filename in [CREATE_PATH,*SCRIPTS,TEMPLATE]:
            raw=z.read('npc/'+filename)
            source_files.append({'path':filename,'bytes':len(raw),'sha256':sha(raw),'crc32':crc(raw)})
            outputs['original/npc/'+filename]=raw
        creates=parse_creates(z.read('npc/'+CREATE_PATH))
        scripts=[]
        for path in SCRIPTS:
            events=parse_events(z.read('npc/'+path))
            for e in events:
                old=prior.get((path,e['ordinal']))
                if old is None or (old['event_number'],old['raw_type'],old['condition_expression_decoded_cp950_UTF8_sha256'],old['source_section_decoded_cp950_normalized_UTF8_sha256'])!=(e['event_no'],e['type'],e['predicate_sha256'],e['section_sha256']):
                    raise AssertionError('prior QUEST01 original block hash mismatch '+path)
            scripts.append({'path':path,'source_sha256':sha(z.read('npc/'+path)),'event_count':len(events),'events':events})
        assert [x['event_count'] for x in scripts]==[5,6,3,6,3,5] and len(prior)==28
        # The bounded search does not cover drops, crafting, shops, or absent scripts.
        all_give={str(i):[] for i in ITEM_IDS+LATER_BRANCH_IDS}
        for name in z.namelist():
            raw=z.read(name)
            txt=raw.decode('cp950', errors='replace')
            for line_no,line in enumerate(txt.splitlines(),1):
                if re.match(r'^\s*GetItem\s*:', line,re.I):
                    for id in ITEM_IDS+LATER_BRANCH_IDS:
                        if re.search(r'(?<!\d)'+str(id)+r'(?!\d)',line):
                            all_give[str(id)].append({'file_path':name[4:],'line_1based':line_no,'source_sha256':sha(raw)})
    with zipfile.ZipFile(item_zip) as z:
        assert z.testzip() is None
        c=json.loads(z.read('private-full-catalog.json'))
        rows={int(x['id']):x for x in c['items']}
        receipts={int(x['source_itemset_image_number_alias']):x for x in c['image_source_receipts']}
        items=[]
        for id in ITEM_IDS:
            item=rows[id]
            lines=[]
            for table in ('itemset.txt','itemset0710.txt'):
                entry=item[table]
                original=entry['original_94_columns']
                assert len(original)==94 and int(original[16])==id
                raw=','.join(original).encode('cp950','strict')
                assert sha(raw)==entry['original_row_sha256']
                assert sha(raw) in (public_item[id][1],public_item[id][2])
                lines.append({'table':table,'physical_row_1based':entry['source_row_1based'],'sha256':sha(raw),'original_columns':94})
                outputs[f'original/itemrows/{table}/{id}-row{entry["source_row_1based"]}.txt']=raw+b'\n'
            assert lines[0]['sha256']==lines[1]['sha256']==public_item[id][1]==public_item[id][2]
            alias=int(item['itemset.txt']['original_94_columns'][17])
            assert public_item[id][3]==alias
            source_img=receipts[alias]
            assert source_img['tw1_original_RD_status']=='VERIFIED_ORIGINAL_RD_INDEXED_PIXELS'
            png_path=f'source-TW1-original-RD-candidates/alias-{alias}.png'
            png=z.read(png_path)
            outputs[f'cross-carrier-TW1-original-RD-candidates/alias-{alias}.png']=png
            items.append({'item_id':id,'source_itemset_image_alias':alias,
                          'two_original_94_column_rows':lines,
                          'cross_carrier_TW1_verified_RD_candidate_png_sha256':sha(png),
                          'cross_carrier_not_official_same_deployment':True})
        # 2744/2745 are absent from this retained 13,915-ID itemset catalog.
        # They cannot be promoted to never-existing in all official versions.
        assert len(rows)==13915 and not any(i in rows for i in LATER_BRANCH_IDS)
    assert len(creates)==6
    result={
        'schema':'stoneage.quest15.bandit_event20.source_bound.r1',
        'source_scope':'MIXED25_COMMUNITY_PRESERVATION_NOT_CONFIRMED_OFFICIAL_EARLY_OR_RUNNING_DEPLOYMENT',
        'original_carrier_NPC_zip_sha256':NPC_ZIP_SHA,
        'original_carrier_ITEM01_zip_sha256':ITEM_ZIP_SHA,
        'original_NPC_members_source_verified':2205,
        'old_QUEST01_blocks_sha_and_condition_independently_matched':28,
        'original_files':source_files,
        'original_creates':creates,
        'original_scripts':scripts,
        'original_event_total':sum(s['event_count'] for s in scripts),
        'original_source_floor_ids_sorted':sorted({c['source_floor'] for c in creates}),
        'original_items_with_two_original_rows_and_source_RD_candidates':items,
        'item_2744_2745_scope':{
            'reference_origin':'event20_2 original conditional branch LV>79 NOWEV=161',
            'not_found_in_private_ITEM01_13915_id_catalog':LATER_BRANCH_IDS,
            'not_found_is_not_global_nonexistence':True,
        },
        'literal_GetItem_occurrences_in_exact_2205_NPC_file_scope':all_give,
        'source_map_observation':{
            'source_floor_ids':sorted({c['source_floor'] for c in creates}),
            'source_DAT_raw_cells_reverified_this_unit':0,
            'source_map_graphics_observed_this_unit':0,
            'status':'EXISTING_MAP09_METADATA_JOIN_ONLY_NO_NEW_ORIGINAL_DAT_REPLAY',
            'previously_qualified_MAP09_sources':[
                {'floor':floor,'source_DAT_sha256_in_existing_MAP09':val[0],
                 'original_grid_in_existing_MAP09':val[1],
                 'this_unit_raw_DAT_sha_rechecked':False}
                for floor,val in sorted(PRIOR_MAP09.items())
            ],
            'source_floor_3400':'NOT_IN_PRIOR_MAP09_691_OR_MAP10_60_REQUIRES_PRIVATE_ORIGINAL_DAT',
        },
        'catalog_relationships':[
            {'kind':'source_NPC_create_to_original_script','create_ordinal':c['ordinal'],'script_ref':c['script_ref'],'source_floor':c['source_floor']}
            for c in creates
        ],
        'stage_A':{'PARTIAL':7,'OPEN':2},'stage_B':'GATED','wiki':'GATED','R79':'PAUSED_NON_BLOCKING','overall_percent':None,
        'unknowns':{'original_game_execution':'UNPROVEN', 'same_official_early_deployment':'UNPROVEN',
                    'reward_selection_probability':'UNPROVEN','actual_item_state_mutation':'UNPROVEN',
                    'map_visual_runtime':'UNPROVEN'},
    }
    return result,outputs


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument('--npc-zip',type=Path,required=True)
    p.add_argument('--item-zip',type=Path,required=True)
    p.add_argument('--quest01-index',type=Path,required=True)
    p.add_argument('--item-index',type=Path,required=True)
    p.add_argument('--derived-out',type=Path,required=True)
    p.add_argument('--private-out',type=Path)
    args=p.parse_args()
    result,private=derive(args.npc_zip,args.item_zip,args.quest01_index,args.item_index)
    args.derived_out.parent.mkdir(parents=True,exist_ok=True)
    args.derived_out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if args.private_out:
        with zipfile.ZipFile(args.private_out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8) as z:
            for path in sorted(private):z.writestr(path,private[path])
            z.writestr('source-summary.json',json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('create',len(result['original_creates']),'events',result['original_event_total'],'items',len(result['original_items_with_two_original_rows_and_source_RD_candidates']))