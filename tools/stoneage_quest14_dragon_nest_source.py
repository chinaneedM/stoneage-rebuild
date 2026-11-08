"""Source-bounded original Dragon Nest event17 extraction; proprietary bytes stay private.

Run locally only when authorized PRIVATE_SOURCE directory exists (the retained
StoneAge source ZIPs). Public GitHub CI verifies the derived ledger separately.
"""
from __future__ import annotations

import hashlib
import io
import os
import json
import re
import struct
import zipfile
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'research/recovered/STONEAGE-QUEST14-DRAGON-NEST-ORIGINAL-SOURCE-R1.json'
PRIVATE_SOURCE = Path(os.environ.get('STONEAGE_PRIVATE_SOURCE', '/mnt/data/stoneage_sources'))
ORIGINAL_NPC_ZIP = PRIVATE_SOURCE / 'StoneAge-CHAR01-mixed25-all-npc-original-private.zip'
ORIGINAL_ITEM_ZIP = PRIVATE_SOURCE / 'StoneAge-ITEM01-private-two-itemsets-832-original-RD-icon-observer.zip'
ORIGINAL_MAP_ZIP = PRIVATE_SOURCE / 'StoneAge-MAP09-691-source-ready-map-catalog-private.zip'
NPC_MANIFEST = PRIVATE_SOURCE / 'STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json'
QUEST01_MANIFEST = PRIVATE_SOURCE / 'STONEAGE-QUEST01-PUBLIC-INDEX-MINIFIED-R1.json'
ITEM_INDEX = PRIVATE_SOURCE / 'STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-02-R1.json'

QUEST_CREATE = 'jaruga/event/event17.create'
QUEST_SCRIPTS = [f'jaruga/event/event17_{i}' for i in range(1, 5)]
QUEST_TEMPLATE = 'jaruga/event/event.template'
QUEST_FILES = [QUEST_CREATE, *QUEST_SCRIPTS, QUEST_TEMPLATE]
ITEM_IDS = [2457, 2458, 2459, 2460, 2461, 2462, 2505]
FLOORS = [20801, 20807]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob(data: bytes) -> str:
    return hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()


def crc(data: bytes) -> str:
    return f'{zlib.crc32(data) & 0xffffffff:08x}'


def parse_events(raw: bytes) -> list[dict]:
    """Extract ONLY control grammar; do not publish scripted dialogue or full blocks."""
    s = raw.decode('cp950', 'strict').replace('\r\n', '\n')
    matches = list(re.finditer(r'(?m)^EventNo:(-?\d+)\s*$', s))
    output = []
    for n, match in enumerate(matches):
        end_match = re.search(r'(?m)^EventEnd\s*$', s[match.start():])
        if end_match is None:
            raise ValueError(f'Unbounded event block {n}')
        end = match.start() + end_match.end()
        section = s[match.start():end]
        # Original source index includes a trailing normalized newline.
        section_sha = sha((section.rstrip('\n') + '\n').encode())
        typ = re.search(r'(?m)^TYPE:(\w+)\s*$', section)
        pred = re.search(r'(?m)^EVENT:(.*)$', section)
        if not typ or not pred:
            raise ValueError('Unqualified event without TYPE/EVENT')
        actions = {}
        for key in ('GetItem', 'DelItem', 'EndSetFlg'):
            actions[key] = [m.group(1) for m in re.finditer(rf'(?m)^{key}:(.*)$', section)]
        output.append({'ordinal': n, 'event_no': int(match.group(1)),
                       'type': typ.group(1), 'predicate': pred.group(1),
                       'predicate_sha256': sha(pred.group(1).encode()),
                       'section_sha256': section_sha,
                       'actions': actions,
                       'has_eventend': True})
    return output


def parse_create(raw: bytes, manifest_rows: list[list]) -> list[dict]:
    output = []
    found = list(re.finditer(rb'\{[^{}]*\}', raw))
    if len(found) != 4 or len(manifest_rows) != 4:
        raise AssertionError('Four actual create blocks required')
    for i, m in enumerate(found):
        row = manifest_rows[i]
        # CHAR01's block SHA covers brace through trailing newline, not mere braces.
        src = raw[m.start():m.end() + 1]
        if sha(src) != row[4] or row[1] != i or row[2] != m.start() or row[3] != m.end() + 1:
            raise AssertionError('Original CREATE source-bound row digest mismatch')
        block = src.decode('cp950', 'strict')
        fields = dict(re.findall(r'(?m)^([A-Za-z]+)\s*=\s*(.+?)\s*$', block))
        xyz = [int(x) for x in fields['borncorner'].split(',')]
        floor = int(fields['floorid'])
        if row[5] != floor or row[6] != int(fields['graphicname']) or row[7] != xyz:
            raise AssertionError('CHAR01 floor/graphic/borncorner mismatch')
        ref = fields['enemy'].split('file:',1)[1]
        output.append({'ordinal':i,'original_sha256':row[4],
                       'source_offset_start':m.start(),'source_offset_end_exclusive':m.end()+1,
                       'floor':floor, 'original_borncorner':xyz, 'graphic_alias':int(fields['graphicname']),
                       'direction':int(fields['dir']),'enemy_function':'changeevent',
                       'script_ref':ref,'exact_original_source_row':True})
    return output


def read_map_cell(original_dat: bytes, x: int, y: int) -> list[int]:
    width,height=struct.unpack_from('<II',original_dat,0)
    if len(original_dat)!=8+6*width*height:
        raise AssertionError('DAT three-plane geometry mismatch')
    if not (0<=x<width and 0<=y<height):
        raise AssertionError('source coordinate outside original DAT')
    idx=x+y*width
    return [struct.unpack_from('<H',original_dat,8+2*(idx+plane*width*height))[0] for plane in range(3)]


def derive_original() -> tuple[dict, dict[str, bytes]]:
    manifest=json.loads(NPC_MANIFEST.read_text())
    quest01=json.loads(QUEST01_MANIFEST.read_text())
    item_index=json.loads(ITEM_INDEX.read_text())
    source_index={p[0]:(p[1],p[2],p[3]) for p in manifest['source_files']}
    selected_rows=[row for row in manifest['create_rows'] if row[0]==QUEST_CREATE]
    if len(selected_rows)!=4:raise AssertionError('Original CHAR01 catalog missing four CREATE blocks')
    selected_rows.sort(key=lambda r:r[1])
    controls_by_path={}
    for x in quest01['source_event_blocks']:
        if x['script_path'] in QUEST_SCRIPTS:
            controls_by_path.setdefault(x['script_path'],[]).append(x)
    private={}
    with zipfile.ZipFile(ORIGINAL_NPC_ZIP) as z:
        assert len(z.namelist())==2205 and len(source_index)==2205
        assert sorted(z.namelist())==sorted('npc/'+path for path in source_index)
        total=0
        for name in z.namelist():
            raw=z.read(name)
            record=source_index[name[4:]]
            if (len(raw),sha(raw),crc(raw))!=record:
                raise AssertionError(f'Original NPC source conservation: {name}')
            total+=len(raw)
        assert total==1930332
        for name in QUEST_FILES:
            b=z.read('npc/'+name)
            private['original/npc/'+name]=b
        creates=parse_create(private['original/npc/'+QUEST_CREATE],selected_rows)
        scripts=[]
        for script in QUEST_SCRIPTS:
            data=private['original/npc/'+script]
            blocks=parse_events(data)
            expected=sorted(controls_by_path[script],key=lambda x:x['script_block_ordinal'])
            if len(blocks)!=len(expected):raise AssertionError('Prior QUEST01 block count mismatch')
            for b,ref in zip(blocks,expected):
                if (b['event_no'],b['type'],b['section_sha256'],b['predicate_sha256'])!=(ref['event_number'],ref['raw_type'],ref['source_section_decoded_cp950_normalized_UTF8_sha256'],ref['condition_expression_decoded_cp950_UTF8_sha256']):
                    raise AssertionError(f'Independent QUEST01 original block disagreement: {script} #{b["ordinal"]}')
            scripts.append({'path':script,'bytes':len(data),'original_sha256':sha(data),
                            'event_count':len(blocks),'events':blocks,
                            'independently_existing_QUEST01_index_verified':True})
        # Only bounded absence of literal GetItem references in these 2,205 NPC files.
        target={2457,2458,2459,2460,2461,2462,2505}
        get_hits={str(i):[] for i in target}
        for name in z.namelist():
            data=z.read(name)
            s=data.decode('cp950', errors='replace')
            for line_num,line in enumerate(s.splitlines(),start=1):
                if re.match(r'^\s*GetItem\s*:',line,re.I):
                    for item_id in target:
                        if re.search(r'(?<!\d)'+str(item_id)+r'(?!\d)',line):
                            get_hits[str(item_id)].append({'file':name[4:],'line':line_num,'file_sha256':source_index[name[4:]][1]})
    refs=[x for x in quest01['source_creation_references'] if x['create_source_path']==QUEST_CREATE]
    if len(refs)!=4:
        raise AssertionError("QUEST01 original four independent CREATE references missing")
    for i,x in enumerate(refs):
        if x['original_script_path']!=creates[i]['script_ref'] or x['create_brace_ordinal']!=i:
            raise AssertionError('Original direct event script reference differs')
    if any(i['script_ref'] not in QUEST_SCRIPTS for i in creates):
        raise AssertionError('Create references not exact scripts')
    assert [len(s['events']) for s in scripts]==[2,2,2,4]
    # Read exact private item rows independently of the already-public item index.
    with zipfile.ZipFile(ORIGINAL_ITEM_ZIP) as z:
        catalog=json.loads(z.read('private-full-catalog.json'))
        objects={x['id']:x for x in catalog['items'] if x['id'] in ITEM_IDS}
        assert set(objects)==set(ITEM_IDS)
        public_rows={x[0]:x for x in item_index['rows'] if x[0] in ITEM_IDS}
        if set(public_rows)!=set(ITEM_IDS):raise AssertionError('Item index not complete for QUEST14')
        image_receipts={x['source_itemset_image_number_alias']:x for x in catalog['image_source_receipts']}
        item_records=[]
        for item_id in ITEM_IDS:
            item=objects[item_id]
            row=public_rows[item_id]
            sources=[]
            for table,ix in [('itemset.txt',1),('itemset0710.txt',2)]:
                entry=item[table]
                cols=entry['original_94_columns']
                if len(cols)!=94 or int(cols[16])!=item_id:
                    raise AssertionError('Original 94-column row schema mismatch')
                data=','.join(cols).encode('cp950','strict')
                if sha(data)!=entry['original_row_sha256'] or row[ix]!=sha(data):
                    raise AssertionError('Item literal row or public ITEM01 index SHA mismatch')
                name=f'original/itemrows/{table}/{item_id}-row{entry["source_row_1based"]}.txt'
                private[name]=data+b'\n'
                sources.append({'table':table,'physical_row_1based':entry['source_row_1based'],
                                'source_sha256':sha(data),'original_94_columns':94,
                                'source_graphic_alias':int(cols[17])})
            alias=sources[0]['source_graphic_alias']
            picture=image_receipts.get(alias)
            if picture is None or picture['tw1_original_RD_status']!='VERIFIED_ORIGINAL_RD_INDEXED_PIXELS':
                raise AssertionError('TW1 actual raw RD candidate unsupported')
            icon_path=f'source-TW1-original-RD-candidates/alias-{alias}.png'
            pixel=z.read(icon_path)
            if sha(pixel)!=picture['candidate_PNG_SHA256']:
                raise AssertionError('TW1 actual original RD-derived private PNG changed')
            private[f'icons/alias-{alias}.png']=pixel
            item_records.append({'item_id':item_id, 'name_original':item['itemset.txt']['source_name'],
                                 'row_identity':item['catalog_class'],
                                 'two_source_original_lines':sources,
                                 'separate_TW1_carrying_source_graphic_alias':alias,
                                 'original_TW1_RD_candidate_png_sha256':sha(pixel),
                                 'cross_carrier_not_proof_of_same_official_deployment':True})
    with zipfile.ZipFile(ORIGINAL_MAP_ZIP) as z:
        receipt=json.loads(z.read('scene-source-receipt.json'))
        dat_archive=z.read('source-all-955-original-DAT.zip')
        assert sha(dat_archive)==receipt['original_DAT_archive']['sha256']
        map_records=[]
        with zipfile.ZipFile(io.BytesIO(dat_archive)) as dat:
            assert len(dat.namelist())==955
            for floor in FLOORS:
                name=f'{floor}.dat'
                original=dat.read(name)
                width,height=struct.unpack_from('<II',original,0)
                mr=receipt['maps'][str(floor)]
                if sha(original)!=mr['source_sha256'] or [width,height]!=mr['geometry']:
                    raise AssertionError('MAP09 original map SHA/geometry mismatch')
                private['original/dat/'+name]=original
                coordinates=[]
                for c in creates:
                    if c['floor']==floor:
                        x,y=c['original_borncorner'][:2]
                        coordinates.append({'create_ordinal':c['ordinal'],'at':[x,y],
                                            'actual_three_original_u16':read_map_cell(original,x,y)})
                map_records.append({'floor':floor,'original_bytes':len(original),'original_sha256':sha(original),
                                    'dimensions':[width,height], 'source_positions':coordinates,
                                    'rendered_original_draw_observer_composite_sha256':mr['frame_RGBA_sha256']['combined'],
                                    'scene_thumbnail_is_modern_source_observer_not_original_client':True})
                thumbnail_name=f'thumbnails/{floor}.jpg'
                private[f'maps/{floor}-source-thumb.jpg']=z.read(thumbnail_name)
    source_ledger=[{'path':x,'bytes':len(private['original/npc/'+x]),'original_sha256':sha(private['original/npc/'+x]),
                    'source_crc32':crc(private['original/npc/'+x])} for x in QUEST_FILES]
    doc={
      'schema':'stoneage.quest14.dragon_nest_three_dragons_original_source_bound.r1',
      'source_scope':'MIXED25_COMMUNITY_COMBINED_PRESERVATION_NOT_CONFIRMED_OFFICIAL_EARLY_VERSION_OR_RUNNING_DEPLOYMENT',
      'quest_id':'QUEST14-DRAGON-NEST-EVENT17',
      'source_parent_RAR_sha256':manifest['original_rar_sha256'],
      'source_parent_RAR_original_bytes':manifest['original_rar_bytes'],
      'public_source_NPC_inventory_git_blob':git_blob(NPC_MANIFEST.read_bytes()),
      'public_SOURCE_QUEST01_index_git_blob':git_blob(QUEST01_MANIFEST.read_bytes().rstrip(b'\n')),
      'source_NPC_archive_original_bytes':ORIGINAL_NPC_ZIP.stat().st_size,
      'source_NPC_archive_sha256':sha(ORIGINAL_NPC_ZIP.read_bytes()),
      'source_original_NPC_members_checked':2205,
      'source_original_NPC_member_bytes_checked':total,
      'original_source_files':source_ledger,
      'original_create_rows':creates,
      'scripts':scripts,
      'script_total_events':sum(s['event_count'] for s in scripts),
      'seven_item_IDs':ITEM_IDS,
      'original_item_94_column_rows':item_records,
      'source_item_physical_rows_verified':sum(len(x['two_source_original_lines']) for x in item_records),
      'two_original_dat_maps':map_records,
      'original_DAT_map_count':len(map_records),
      'literal_GetItem_occurrences_all_2205_NPC_files':get_hits,
      'catalog_relationships':[
        {'relation':'guardian_source_instruction_get_item','source_script':'jaruga/event/event17_4','item_id':2505,
         'scope':'original_source_control_only'},
        *[{'relation':'dragon_source_condition_exchange_to_reward','source_script':f'jaruga/event/event17_{i}',
           'required_item_ids_literal':[2457,2458,2459,2505],'reward_item_id':reward,
           'original_end_set_flag_literal':17, 'scope':'original_source_control_only'}
          for i,reward in [(1,2462),(2,2460),(3,2461)]],
      ],
      'unknowns':{'dragon_jade_origin_in_this_original_NPC_inventory':'NO_MATCHING_GetItem_LITERAL_FOUND',
                  'script_operation_runtime':'UNPROVEN','three_rewards_repeatability':'UNPROVEN',
                  'original_early_official_version':'UNPROVEN','native_map_runtime':'UNPROVEN',
                  'native_dragon_encounter_or_battle':'UNPROVEN','cross_carrier_TW1_art_same_deployment':'UNPROVEN'},
      'stage_A':{'PARTIAL':7,'OPEN':2},'stage_B':'GATED','wiki':'GATED','R79':'PAUSED_NON_BLOCKING',
      'overall_percent':None,'next':'QUEST15-DEDUP-AND-SOURCE-READY-UNRESTORED-ORIGINAL-FAMILY'
    }
    return doc,private


def main():
    from argparse import ArgumentParser
    parser=ArgumentParser()
    parser.add_argument('--report',type=Path,default=SOURCE)
    parser.add_argument('--private-root',type=Path,default=ROOT/'private/quest14')
    args=parser.parse_args()
    report,items=derive_original()
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    args.private_root.mkdir(parents=True,exist_ok=True)
    for name,blob in items.items():
        p=args.private_root/name
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_bytes(blob)
    print(json.dumps({'event_blocks':report['script_total_events'],
                      'NPC_CREATE':len(report['original_create_rows']),
                      'original_items':len(report['seven_item_IDs']),
                      'original_item_lines':report['source_item_physical_rows_verified'],
                      'map_floors':report['original_DAT_map_count']},ensure_ascii=False))

if __name__=='__main__':main()
