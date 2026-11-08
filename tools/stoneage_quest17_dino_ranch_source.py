"""Source-bounded historical StoneAge dinosaur-ranch quest evidence.

Replays separately retained ORIGINAL ZIP files privately.  The checked-in output
contains only numerical command literals and source hashes; it contains NO
original commercial NPC dialogue, bitmap, DAT, or extracted original file.

The community mixed25 archive is NOT a verified JSS1999/TW1/CN1.82 build.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
import zlib
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_PATH = ROOT / 'research/recovered/STONEAGE-QUEST17-DINO-RANCH-SOURCE-R1.json'
SOURCE_CREATE = 'jaruga/event/bait01.create'
SOURCE_SCRIPTS = ['jaruga/event/'+x for x in ('bait_01','bait_02','bait_03a2','bait_03b2','bait_03c2','bait_04')]
UNREFERENCED_ALTERNATES = ['jaruga/event/'+x for x in ('bait_03a','bait_03b','bait_03c')]
SOURCE_TEMPLATE = 'jaruga/event/event.template'
SOURCE_FILES = [SOURCE_CREATE,*SOURCE_SCRIPTS,*UNREFERENCED_ALTERNATES,SOURCE_TEMPLATE]
ITEM_IDS = tuple(range(2589,2597))
PET_GROUPS = {
    'jaruga/event/bait_03a2': (2594,560,'jaruga/event/bait_03a'),
    'jaruga/event/bait_03b2': (2595,559,'jaruga/event/bait_03b'),
    'jaruga/event/bait_03c2': (2596,558,'jaruga/event/bait_03c'),
}
MAP09_FLOORS = {
    201: ('ddc811bd4483403ae49ea7882650e3047a9abb29e67cbb0bd6e43377873314d1',[30,40]),
    20901: ('71dd85505dabe06de069741fbc38b89d634cdfb956b880d21d09f6d1558e738b',[70,70]),
}
NPC_ZIP_NAME='StoneAge-CHAR01-mixed25-all-npc-original-private.zip'
ITEM_ZIP_NAME='StoneAge-ITEM01-private-two-itemsets-832-original-RD-icon-observer.zip'
QUEST01_INDEX_NAME='STONEAGE-QUEST01-PUBLIC-INDEX-MINIFIED-R1.json'
ITEM_INDEX_NAME='STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-02-R1.json'
NPC_ZIP_SHA='c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f'
ITEM_ZIP_SHA='cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa'
PARENT_RAR_SHA='d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5'
QUEST01_GIT_BLOB='52db8b4b6cd43cd2afa4a8d2e8460f214933f5e2'
MAP09_GIT_BLOB='137580e7c25aadf3d679b6ebfb5080b79912cc4f'
CURRENT_GIT_BLOB='c89e0e33537990aa2132b47c40fef49a985a935c'


def sha(raw:bytes)->str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw:bytes)->str:
    return f'{zlib.crc32(raw)&0xffffffff:08x}'


def parse_creates(raw:bytes)->list[dict]:
    out=[]
    decoded=raw.decode('cp950','strict')
    # CP950 multibyte second bytes can equal ASCII '}' (0x7d). Never parse braces
    # from the encoded bytes: that would truncate two real NPC CREATE blocks.
    for ordinal,m in enumerate(re.finditer(r'\{[^{}]*\}',decoded)):
        chunk=m.group(0).encode('cp950','strict')
        fields=dict(re.findall(r'(?m)^\s*([A-Za-z_]+)\s*=\s*(.+?)\s*$',m.group(0)))
        ref=fields['enemy'].split('file:',1)[1]
        if not fields['enemy'].startswith('changeevent|file:'):
            raise AssertionError('unknown function binding')
        out.append(dict(ordinal=ordinal,source_block_sha256=sha(chunk),
                        floor=int(fields['floorid']),borncorner=[int(v) for v in fields['borncorner'].split(',')],
                        original_name=fields['name'],graphic_alias=int(fields['graphicname']),
                        script_ref=ref))
    return out


def parse_events(raw:bytes)->list[dict]:
    """Read actual source EventNo/TYPE/EVENT and numeric operations only."""
    data=raw.decode('cp950','strict').replace('\r\n','\n')
    headers=list(re.finditer(r'(?m)^EventNo:(-?\d+)\s*$',data))
    out=[]
    for ordinal,m in enumerate(headers):
        ending=re.search(r'(?m)^EventEnd\s*$',data[m.start():])
        if ending is None:
            raise AssertionError('missing EventEnd')
        section=data[m.start():m.start()+ending.end()]
        ty=re.search(r'(?m)^TYPE:(\w+)\s*$',section)
        pred=re.search(r'(?m)^EVENT:(.*)$',section)
        if ty is None or pred is None:
            raise AssertionError('incomplete original event section')
        commands={key:[x.group(1).strip() for x in re.finditer(rf'(?m)^\s*{key}:([^\r\n]*)',section)]
                  for key in ('GetItem','DelItem','GetStone','DelStone','GetRandItem',
                              'EndSetFlg','GetPet','DelPet','NotDel')}
        section_normalized=section.rstrip('\n')+('\n' if section.endswith('\n') else '')
        out.append(dict(ordinal=ordinal,event_no=int(m.group(1)),type=ty.group(1),
                        condition_literal=pred.group(1),condition_sha256=sha(pred.group(1).encode()),
                        section_sha256=sha(section_normalized.encode()),
                        commands={key:values for key,values in commands.items() if values}))
    return out


def source_info(path:str,raw:bytes)->dict:
    return dict(path=path,bytes=len(raw),sha256=sha(raw),crc32=crc(raw))


def validate_report(report:dict,quest01:dict|None=None,maps:dict|None=None,items_shard:dict|None=None)->None:
    assert report['schema']=='stoneage.quest17.dino_ranch_pet_certificate_original_source.r1'
    assert report['source_scope']=='MIXED25_COMMUNITY_PRESERVED_NOT_OFFICIAL_EARLY_BUILD'
    assert report['source_parent_RAR_sha256']==PARENT_RAR_SHA
    assert report['original_npc_archive_sha256']==NPC_ZIP_SHA
    assert report['original_item_archive_sha256']==ITEM_ZIP_SHA
    assert [x['script_ref'] for x in report['source_creates']]==SOURCE_SCRIPTS
    assert len(report['source_creates'])==6
    assert sorted(set(x['floor'] for x in report['source_creates']))==[201,20901]
    assert len(report['source_scripts'])==6
    assert [len(x['events']) for x in report['source_scripts']]==[25,4,10,10,10,2]
    assert report['source_event_total']==61
    assert report['source_event_type_totals']=={'ACCEPT':51,'MESSAGE':9,'REQUEST':1}
    assert len(report['source_unreferenced_variants'])==3
    assert [x['event_count'] for x in report['source_unreferenced_variants']]==[18,18,18]
    assert all(x['create_file_reference_count_within_2205_retained_NPC_members']==0
               for x in report['source_unreferenced_variants'])
    assert len(report['source_items'])==8
    assert [x['item_id'] for x in report['source_items']]==list(ITEM_IDS)
    assert sum(len(x['source_rows']) for x in report['source_items'])==16
    assert len(report['original_tw1_cross_carrier_candidate_images'])==4
    assert len(report['pet_certificate_branches'])==3
    assert [(x['script'],x['wristband_id'],x['pet_predicate_numeric'])
            for x in report['pet_certificate_branches']]==[(k,*v[:2]) for k,v in PET_GROUPS.items()]
    assert all(x['original_events']==10 and x['unreferenced_variant_events']==18
               for x in report['pet_certificate_branches'])
    assert len(report['source_21_payment_literals'])==21
    assert sorted(Counter(x['wristband_id'] for x in report['source_21_payment_literals']).values())==[7,7,7]
    amounts=[x['source_getstone_literal'] for x in report['source_21_payment_literals']]
    assert all(isinstance(v,int) and v>0 for v in amounts)
    assert report['source_command_totals']['GetStone']==21
    assert report['source_command_totals']['NotDel']==6
    assert report['source_command_totals']['DelPet']==18
    assert report['source_command_totals']['GetItem']==31
    assert report['unverified']['native_pet_capture_exchange_executed'] is False
    assert report['unverified']['official_original_version_deployment'] is False
    assert report['overall_percent'] is None
    if quest01 is not None:
        old={x['path']:x for x in quest01['source_scripts']}
        controls={(x['script_path'],x['script_block_ordinal']):x for x in quest01['source_event_blocks']}
        refs=[x for x in quest01['source_creation_references'] if x['create_source_path']==SOURCE_CREATE]
        assert len(refs)==6
        for x in report['source_scripts']:
            assert old[x['path']]['original_sha256']==x['sha256']
            assert old[x['path']]['original_crc32']==x['crc32']
            for e in x['events']:
                t=controls[x['path'],e['ordinal']]
                assert (e['type'],e['event_no'],e['condition_sha256'],e['section_sha256'])==(
                    t['raw_type'],t['event_number'],t['condition_expression_decoded_cp950_UTF8_sha256'],
                    t['source_section_decoded_cp950_normalized_UTF8_sha256'])
        for c in report['source_creates']:
            y=next(x for x in refs if x['create_brace_ordinal']==c['ordinal'])
            assert (y['floorid'],y['graphic_alias_numeric'],y['original_script_path'])==(
                c['floor'],c['graphic_alias'],c['script_ref'])
    if maps is not None:
        for entry in report['source_map_qualification']['previously_verified_map09_DAT']:
            obj=maps['maps'][str(entry['floor'])]
            assert (obj['source_sha256'],obj['geometry'])==(
                entry['sha256'],entry['geometry'])
    if items_shard is not None:
        original={x[0]:x for x in items_shard['rows']}
        for item in report['source_items']:
            x=original[item['item_id']]
            assert item['source_rows'][0]['sha256']==x[1]
            assert item['source_rows'][1]['sha256']==x[2]


def derive(private_dir:Path)->tuple[dict,dict[str,bytes]]:
    npc_path=private_dir/NPC_ZIP_NAME
    item_path=private_dir/ITEM_ZIP_NAME
    q01=json.loads((private_dir/QUEST01_INDEX_NAME).read_text('utf-8'))
    item_shard=json.loads((private_dir/ITEM_INDEX_NAME).read_text('utf-8'))
    assert sha(npc_path.read_bytes())==NPC_ZIP_SHA
    assert sha(item_path.read_bytes())==ITEM_ZIP_SHA
    original_script_index={x['path']:x for x in q01['source_scripts']}
    original_block_index={(x['script_path'],x['script_block_ordinal']):x for x in q01['source_event_blocks']}
    original_create_refs=[x for x in q01['source_creation_references'] if x['create_source_path']==SOURCE_CREATE]
    assert len(original_create_refs)==6
    private={}
    with zipfile.ZipFile(npc_path) as z:
        assert len(z.namelist())==2205
        assert z.testzip() is None
        source={p:z.read('npc/'+p) for p in SOURCE_FILES}
        private.update({'original-npc/'+p:b for p,b in source.items()})
        create=parse_creates(source[SOURCE_CREATE])
        assert len(create)==6
        for c in create:
            r=next(x for x in original_create_refs if x['create_brace_ordinal']==c['ordinal'])
            assert (r['floorid'],r['original_script_path'],r['graphic_alias_numeric'])==(
                c['floor'],c['script_ref'],c['graphic_alias'])
        scripts=[]
        for path in SOURCE_SCRIPTS:
            raw=source[path]
            original=original_script_index[path]
            assert (sha(raw),crc(raw),len(raw))==(
                original['original_sha256'],original['original_crc32'],original['original_size'])
            events=parse_events(raw)
            for e in events:
                old=original_block_index[(path,e['ordinal'])]
                assert (e['event_no'],e['type'],e['condition_sha256'],e['section_sha256'])==(
                    old['event_number'],old['raw_type'],old['condition_expression_decoded_cp950_UTF8_sha256'],
                    old['source_section_decoded_cp950_normalized_UTF8_sha256'])
            scripts.append(dict(**source_info(path,raw),events=events))
        assert [len(x['events']) for x in scripts]==[25,4,10,10,10,2]
        all_create_bytes=[(n,z.read(n)) for n in z.namelist() if n.endswith(('.create','.bak'))]
        variants=[]
        for path in UNREFERENCED_ALTERNATES:
            raw=source[path];ev=parse_events(raw)
            # Count exact old target, rejecting suffix2 and substring matches.
            exact=path.encode('ascii')
            pat=rb'file:'+re.escape(exact)+rb'(?![A-Za-z0-9_])'
            count=sum(len(re.findall(pat,b)) for _,b in all_create_bytes)
            assert count==0
            assert len(ev)==18
            variants.append(dict(**source_info(path,raw),event_count=len(ev),
                        create_file_reference_count_within_2205_retained_NPC_members=count,
                        source_command_counts=dict(sorted(Counter(k for e in ev for k,v in e['commands'].items() for _ in v).items())),
                        note='ARCHIVED_ALTERNATE_NOT_REFERENCED_BY_THIS_PRESERVED_CREATE_CORPUS'))
    with zipfile.ZipFile(item_path) as z:
        assert z.testzip() is None
        catalog=json.loads(z.read('private-full-catalog.json'))
        records={x['id']:x for x in catalog['items'] if x['id'] in ITEM_IDS}
        assert sorted(records)==list(ITEM_IDS)
        public_rows={x[0]:x for x in item_shard['rows']}
        images_by_alias={x['source_itemset_image_number_alias']:x for x in catalog['image_source_receipts']}
        item_rows=[];images={}
        for item_id in ITEM_IDS:
            item=records[item_id];old=public_rows[item_id];replayed=[]
            for col,src in ((1,'itemset.txt'),(2,'itemset0710.txt')):
                record=item[src];columns=record['original_94_columns']
                assert len(columns)==94 and int(columns[16])==item_id
                raw=','.join(columns).encode('cp950','strict')
                assert sha(raw)==record['original_row_sha256']==old[col]
                name=f'original-itemrows/{src}/{item_id}-{record["source_row_1based"]}.txt'
                private[name]=raw+b'\n'
                replayed.append(dict(table=src,row=record['source_row_1based'],sha256=sha(raw),
                                     original_column_count=94,graphic_alias=int(columns[17])))
            assert replayed[0]['graphic_alias']==replayed[1]['graphic_alias']
            alias=replayed[0]['graphic_alias']
            receipt=images_by_alias[alias]
            assert receipt['tw1_original_RD_status']=='VERIFIED_ORIGINAL_RD_INDEXED_PIXELS'
            png_name=f'source-TW1-original-RD-candidates/alias-{alias}.png'
            png=z.read(png_name)
            assert sha(png)==receipt['candidate_PNG_SHA256']
            private[f'cross-carrier-TW1-original-RD/alias-{alias}.png']=png
            images[alias]=dict(alias=alias,private_png_sha256=sha(png),bytes=len(png),
                original_RD_sha256=receipt['original_RD_SHA256'],
                candidate_only_other_TW1_original_source=True)
            item_rows.append(dict(item_id=item_id,source_rows=replayed,source_image_alias=alias,
                                  cross_carrier_TW1_candidate_PNG_SHA256=sha(png)))
        assert len(images)==4
    # Payout grid comes from 21 actual source sections, not from an invented price formula.
    payments=[]
    for e in scripts[0]['events']:
        if 'GetStone' not in e['commands']:
            continue
        pred=e['condition_literal']
        x=re.fullmatch(r'ITEM=(2589|2590|2591|2592)(?:\*(\d+))?&ITEM=(2594|2595|2596)',pred)
        if x is None:raise AssertionError('payout condition changed')
        assert e['commands'].get('DelItem')==[f'{x.group(1)}*{x.group(2) or "1"}']
        payment=int(e['commands']['GetStone'][0]);assert payment>0
        payments.append(dict(event_ordinal=e['ordinal'],voucher_id=int(x.group(1)),
                   voucher_quantity=int(x.group(2) or '1'),wristband_id=int(x.group(3)),
                   source_getstone_literal=payment,
                   original_delitem_literal=e['commands']['DelItem'][0]))
    assert len(payments)==21
    assert sorted(Counter(x['wristband_id'] for x in payments).values())==[7,7,7]
    branches=[]
    for s in SOURCE_SCRIPTS:
        if s not in PET_GROUPS:continue
        band,pet,legacy=PET_GROUPS[s]
        es=next(x['events'] for x in scripts if x['path']==s)
        assert all((f'PET>0-{pet}' in e['condition_literal']) for e in es[:6])
        assert all((f'ITEM={band}' in e['condition_literal']) for e in es[:6])
        assert [e['commands'].get('DelPet') for e in es[:6]]==[
            ['EVDEL'],['EVDEL'],*[ [f'PET>0-{pet}*{n}'] for n in (4,3,2,1)]]
        assert [e['commands'].get('NotDel') for e in es[:6]]==[[str(band)],[str(band)],None,None,None,None]
        assert [e['commands'].get('GetItem') for e in es[:6]]==[["2591*1"],["2590*1"],*[ [f'2589*{n}'] for n in (4,3,2,1)]]
        legacy_record=next(x for x in variants if x['path']==legacy)
        branches.append(dict(script=s,wristband_id=band,pet_predicate_numeric=pet,
            original_events=10,unreferenced_variant_source=legacy,
            unreferenced_variant_events=legacy_record['event_count'],
            first_two_sections_use_EVDEL=True,
            first_two_sections_use_NotDel_wristband=True,
            four_following_sections_use_explicit_DelPet=True))
    assert len(branches)==3
    counts=Counter(k for script in scripts for e in script['events'] for k,x in e['commands'].items() for _ in x)
    type_counts=Counter(e['type'] for script in scripts for e in script['events'])
    report=dict(
        schema='stoneage.quest17.dino_ranch_pet_certificate_original_source.r1',
        source_scope='MIXED25_COMMUNITY_PRESERVED_NOT_OFFICIAL_EARLY_BUILD',
        source_parent_RAR_sha256=PARENT_RAR_SHA,
        original_npc_archive_sha256=NPC_ZIP_SHA,
        original_npc_verified_member_count=2205,
        original_item_archive_sha256=ITEM_ZIP_SHA,
        source_quest01_catalog_git_blob=QUEST01_GIT_BLOB,
        source_map09_ledger_git_blob=MAP09_GIT_BLOB,
        historical_current_git_blob_unmodified=CURRENT_GIT_BLOB,
        source_manifest=[source_info(p,source[p]) for p in SOURCE_FILES],
        source_creates=create,source_scripts=scripts,
        source_event_total=sum(len(x['events']) for x in scripts),
        source_event_type_totals=dict(sorted(type_counts.items())),
        source_command_totals=dict(sorted(counts.items())),
        source_unreferenced_variants=variants,
        source_items=item_rows,
        original_tw1_cross_carrier_candidate_images=[images[k] for k in sorted(images)],
        pet_certificate_branches=branches,
        source_21_payment_literals=payments,
        source_map_qualification=dict(previously_verified_map09_DAT=[
            dict(floor=f,sha256=record[0],geometry=record[1],source_DAT_bytes_replayed_this_round=False)
            for f,record in sorted(MAP09_FLOORS.items())],
            original_DAT_cells_replayed_this_round=0),
        source_work_scope=dict(quest01_old_source_script_records=6,quest01_old_event_records=61,
            original_npc_create_count=6,
            same_archive_alt_scripts_not_in_current_create=3,
            new_original_commercial_game_execution=0,
            newly_found_original_source_bytes_outside_existing_private_archives=0,
            special_subsystem='ITEM_PET_PREDICATES_AND_CERTIFICATE_EXCHANGE_STATIC_SOURCE_ONLY'),
        unverified=dict(native_pet_capture_exchange_executed=False,
            official_original_version_deployment=False,
            script_selection_priority_and_EVDEL_semantics=False,
            real_item_reward_or_currency_changes=False,
            pet_species_identity_from_numeric_PET_predicate=False,
            original_DAT_cells_at_created_NPC_coordinates=False,
            actual_same_build_TW1_image_and_community_item=False),
        next='QUEST18-DEDUP-AND-NEXT_SOURCE_READY_ORIGINAL_FAMILY',
        stage_A={'PARTIAL':7,'OPEN':2},stage_B='GATED',wiki='GATED',
        R79='PAUSED_NON_BLOCKING',overall_percent=None,
    )
    validate_report(report,quest01=q01,items_shard=item_shard)
    private['source-summary-derived-no-commercial-text.json']=json.dumps(report,ensure_ascii=False,indent=2).encode()+b'\n'
    return report,private


def public_validate(root:Path=ROOT)->dict:
    r=json.loads((root/'research/recovered/STONEAGE-QUEST17-DINO-RANCH-SOURCE-R1.json').read_text('utf-8'))
    q=json.loads((root/'research/recovered/STONEAGE-QUEST-STORY-MODULE-01-ORIGINAL-EXCHANGEMAN-QUEST-SOURCE-BLOCK-CATALOG-R1.json').read_text('utf-8'))
    maps=json.loads((root/'research/recovered/STONEAGE-MAP09-691-SOURCE-READY-SCENES-R1.json').read_text('utf-8'))
    shard=json.loads((root/'research/recovered/item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-02-R1.json').read_text('utf-8'))
    validate_report(r,quest01=q,maps=maps,items_shard=shard)
    return r


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--private-dir',type=Path)
    parser.add_argument('--output',type=Path,default=PUBLIC_PATH)
    parser.add_argument('--private-zip',type=Path)
    parser.add_argument('--public-only',action='store_true')
    args=parser.parse_args()
    if args.public_only:
        r=public_validate(ROOT)
    else:
        if args.private_dir is None: parser.error('--private-dir required unless --public-only')
        r,private=derive(args.private_dir)
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        if args.private_zip:
            args.private_zip.parent.mkdir(parents=True,exist_ok=True)
            with zipfile.ZipFile(args.private_zip,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8) as z:
                for name,raw in sorted(private.items()): z.writestr(name,raw)
    print('CREATES',len(r['source_creates']),'EVENT',r['source_event_total'],
          'ITEM',len(r['source_items']),'PNG',len(r['original_tw1_cross_carrier_candidate_images']))
