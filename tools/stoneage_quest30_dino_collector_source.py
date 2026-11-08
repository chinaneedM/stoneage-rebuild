"""Bounded original dinosaur-collector source dossier; commercial bytes remain private.

This tool reads only explicitly supplied, already preserved private NPC/item ZIPs.
It never runs original predicates, pet removal, rewards, client, or server.
"""
from __future__ import annotations
import argparse
import hashlib
import html
import json
from pathlib import Path
import re
import zipfile
from collections import Counter

from tools.stoneage_quest29_spirit_king_source import (
    NPC_SHA, ITEM_SHA, Q_SHA, CH_SHA, Q_BLOB, CH_BLOB,
    sha, info, gitblob, index_pin, sections,
)

ROOT=Path(__file__).resolve().parents[1]
REC=ROOT/'research/recovered'
OUTPUT=REC/'STONEAGE-QUEST30-DINOSAUR-COLLECTOR-EVENT35-SOURCE-R1.json'
CREATE='seimu/event/event02_n.create'
SCRIPT='seimu/event/event02_1'
TEMPLATE='jaruga/event/event.template'
ITEM=2607
QUEST09_SCRIPTS=('seimu/event/event01_1','seimu/event/event01_2')
WORLD21_GIT_BLOB='f8614b9e90e548efb6d61e269d725d17ea173a74'
Q05_GIT_BLOB='b004e488e1d0a93ca7c14eb90abb584b23f341fe'
CURRENT_GIT_BLOB='c89e0e33537990aa2132b47c40fef49a985a935c'
WORLD21_EXPECTED={93:(171,100319),341:(274,100362)}


def derive(npc_zip:Path,item_zip:Path,quest01:Path,char01:Path,item_dir:Path):
    q_pin=index_pin(quest01,Q_SHA,Q_BLOB)
    ch_pin=index_pin(char01,CH_SHA,CH_BLOB)
    q=json.loads(quest01.read_text(encoding='utf-8'))
    ch=json.loads(char01.read_text(encoding='utf-8'))
    assert sha(npc_zip.read_bytes())==NPC_SHA
    assert sha(item_zip.read_bytes())==ITEM_SHA
    source_files={r[0]:r for r in ch['source_files']}
    private={}
    with zipfile.ZipFile(npc_zip) as z:
        assert len(z.namelist())==2205 and z.testzip() is None
        for n in z.namelist():
            assert n.startswith('npc/')
            b=z.read(n);r=source_files[n[4:]]
            assert [len(b),sha(b),f'{z.getinfo(n).CRC:08x}']==r[1:4]
        for p in (CREATE,SCRIPT,TEMPLATE):
            private['original-npc/'+p]=z.read('npc/'+p)
        create=next(r for r in ch['create_rows'] if r[0]==CREATE and r[1]==0)
        assert sum(r[0]==CREATE for r in ch['create_rows'])==1
        assert sha(private['original-npc/'+CREATE][create[2]:create[3]])==create[4]
        assert create[15]==[[SCRIPT,'EXACT_SAME_NPC_SUBTREE_PATH',source_files[SCRIPT][2]]]
        assert create[13]==[[TEMPLATE,0]]
        template=next(r for r in ch['template_rows'] if (r[0],r[1])==(TEMPLATE,0))
        assert template[4]=='ExChangeMan'
        old=[e for e in q['source_event_blocks'] if e['script_path']==SCRIPT]
        assert len(old)==8
        events=sections(private['original-npc/'+SCRIPT],old)
        assert [e['type'] for e in events]==['ACCEPT','MESSAGE','ACCEPT','REQUEST','ACCEPT','MESSAGE','ACCEPT','ACCEPT']
        assert [e['event_no'] for e in events]==[35,-1,-1,35,-1,-1,-1,-1]
        assert len(events)==len(old)==q['source_scripts'][next(i for i,x in enumerate(q['source_scripts']) if x['path']==SCRIPT)]['source_control_lines']['TYPE']
        all_getpet=[(e['ordinal'],s) for e in events for s in e['commands'].get('GetPet',[])]
        assert all_getpet==[(0,'93'),(4,'341')]
        assert events[4]['commands']['DelPet']==['EVDEL']
        assert events[0]['commands']['DelPet']==['PET=25-221*1,PET=25-222*1']
        assert events[2]['commands']['DelPet']==['PET=25-223*1,PET=25-224*1']
        assert events[6]['commands']['DelPet']==['PET=25-291*1,PET=25-294*1']
        assert events[4]['condition_literal'].count(',')==1
        assert events[0]['commands']['EndSetFlg']==['35']
        assert not any('EndSetFlg' in events[n]['commands'] for n in (2,4,6,7))
    shard_index={}
    for n in range(1,8):
        shard=json.loads((item_dir/f'STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-{n:02d}-R1.json').read_text(encoding='utf-8'))
        for row in shard['rows']:
            assert row[0] not in shard_index
            shard_index[row[0]]=row
    assert ITEM in shard_index
    with zipfile.ZipFile(item_zip) as z:
        assert len(z.namelist())==838 and z.testzip() is None
        catalogue=json.loads(z.read('private-full-catalog.json'))
        item_row=next(r for r in catalogue['items'] if r['id']==ITEM)
        source_item=[]
        aliases=set()
        for i,(col,table) in enumerate(((1,'itemset.txt'),(2,'itemset0710.txt'))):
            r=item_row[table]
            columns=r['original_94_columns'];assert len(columns)==94 and int(columns[16])==ITEM
            raw=','.join(columns).encode('cp950')
            assert sha(raw)==r['original_row_sha256']==shard_index[ITEM][col]
            private[f'original-itemrows/{table}/{ITEM}.txt']=raw+b'\n'
            alias=int(columns[17]);aliases.add(alias)
            source_item.append(dict(table=table,row_1based=r['source_row_1based'],sha256=sha(raw),image_alias=alias,
                original_name_UTF8_sha256=sha(columns[0].encode('utf-8'))))
            assert '戒指' in columns[0]
        assert len(aliases)==1
        alias=next(iter(aliases))
        image=next(m for m in catalogue['image_source_receipts'] if m['source_itemset_image_number_alias']==alias)
        assert image['tw1_original_RD_status']=='VERIFIED_ORIGINAL_RD_INDEXED_PIXELS'
        png=z.read('source-TW1-original-RD-candidates/alias-'+str(alias)+'.png')
        assert sha(png)==image['candidate_PNG_SHA256']
        private[f'cross-carrier-TW1-item-candidates/{alias}.png']=png
    raw_script=private['original-npc/'+SCRIPT].decode('cp950','strict')
    assert '證明' in raw_script and '戒指' not in raw_script
    assert sum('證明' in line for line in raw_script.splitlines())>=2
    # The old Q09 file is from a different portion of seimu; only the master paths are shared.
    q09_paths={s['path'] for s in q['source_scripts'] if s['path'] in QUEST09_SCRIPTS}
    assert q09_paths==set(QUEST09_SCRIPTS)
    assert set([SCRIPT]).isdisjoint(q09_paths)
    collect=[dict(event_ordinal=e['ordinal'],type=e['type'],event_number=e['event_no'],
                  original_condition_literal=e['condition_literal'],original_DelPet_literals=e['commands'].get('DelPet',[]),
                  original_GetItem_literals=e['commands'].get('GetItem',[]),
                  original_DelItem_literals=e['commands'].get('DelItem',[]),
                  original_GetPet_literals=e['commands'].get('GetPet',[]),
                  original_EndSetFlg_literals=e['commands'].get('EndSetFlg',[]),
                  section_sha256=e['section_sha256']) for e in events if e['commands']]
    assert [e['event_ordinal'] for e in collect]==[0,2,4,6]
    report={
        'schema':'stoneage.quest30.seimu_dinosaur_collector_event35_source.r1',
        'date':'2026-11-08',
        'initial_remote':dict(head='95fc5875143c7635ee1773f4e2204c3116d2675f',
                              tree='8d4dfc86d6bd7f3b920a344073e0905b5de60068',
                              preserved_CURRENT_blob=CURRENT_GIT_BLOB),
        'source_scope':'LATER_COMMUNITY_MIXED25_NOT_VERIFIED_EARLY_OFFICIAL',
        'verified_carriers':dict(npc_zip_sha256=NPC_SHA,npc_zip_all_members_SHA_and_CRC=2205,
                                 item_zip_sha256=ITEM_SHA,item_zip_CRC_members=838,parent_RAR_reread=False),
        'existing_indices':[q_pin,ch_pin],
        'dedupe':dict(QUEST01_indexed_original_scripts=295,QUEST01_indexed_original_TYPE=1349,
            selected_script_previously_in_QUEST01=True,selected_eight_TYPE_previously_in_QUEST01=True,
            QUEST09_existing_seimu_scripts=list(QUEST09_SCRIPTS),new_original_script_files=0,
            new_original_TYPE_sections=0,selected_family_not_QUEST17_bait_ranch=True),
        'source_files':[info(p,private['original-npc/'+p]) for p in (CREATE,SCRIPT,TEMPLATE)],
        'source_NPC_create':dict(file=CREATE,ordinal=0,source_block_sha256=create[4],floor=create[5],
            source_borncorner_four_integers=create[7],range_not_proven_single_spawn_point=True,
            original_graphic_alias=create[6],original_direction=create[10],
            source_script=SCRIPT,original_functionset=template[4],template_path=TEMPLATE,
            template_ordinal=0),
        'source_script':dict(**info(SCRIPT,private['original-npc/'+SCRIPT]),events=events,
                             original_EVENT_section_count=8),
        'recovered_control_groups':collect,
        'source_2607_item_row':dict(item_ID=ITEM,original_two_94_column_rows=source_item,
            source_image_alias=alias,cross_carrier_TW1_candidate_PNG_sha256=sha(png),
            source_record_discrepancy='NPC_SOURCE_CALLS_CAPTURE_PROOF_ITEMSET_NAMES_RING',
            dialogue_name_and_itemset_source_name_assumed_identical=False,
            mismatch_cause_known=False),
        'prior_WORLD21_existing_GetPet_instances':[dict(source_GetPet_operand=i,
            prior_enemy_instance=i,prior_template_id=t,prior_template_graphic_alias=g,
            original_enemy_instance_not_template_id=True,source='WORLD21_EXISTING_SOURCE_LOOKUP')
            for i,(t,g) in WORLD21_EXPECTED.items()],
        'prior_WORLD21_git_blob':WORLD21_GIT_BLOB,
        'prior_QUEST05_map_floor100':dict(source_floor_id=100,
            existing_source_MAP_status='NO_MATCHING_DAT_IN_955',
            no_matching_DAT_in_this_collection_not_proof_original_floor_absent=True,
            prior_QUEST05_git_blob=Q05_GIT_BLOB),
        'original_variants_and_uncertainties':dict(
            first_reward_has_EndSetFlg35=True,second_reward_without_EndSetFlg=True,
            after_first_flag_second_run_native_reachability_proven=False,
            first_pair_original_PET_literals=events[2]['commands']['DelPet'][0],
            second_pair_original_PET_literals=events[0]['commands']['DelPet'][0],
            alternative_second_run_original_condition=events[4]['condition_literal'],
            second_run_original_DelPet_is_EVDEL=True,
            original_DelPet_EVDEL_interpreted_as_specific_pets=False,
            original_PET25_minus_ID_encoding_interpreted_as_verified_level_or_species=False,
            original_comma_condition_executed=False,
            original_npc_dialogue_replayed=False),
        'boundaries':dict(original_game_or_server_executed=False,native_capture_or_handin_or_reward_observed=False,
            original_palette_or_client_scene_rendered=False,source_100_DAT_recovered_in_955=False,
            official_early_same_deployment_confirmed=False,pet_instance_ids_equated_to_template_ids=False,
            original_source_NPC_dialogue_or_item_rows_published=False,original_rarity_or_random_probabilities_proven=False,
            original_task_origin='UNRESOLVED'),
        'stage_A':{'PARTIAL':7,'OPEN':2},'stage_B':'GATED','wiki':'GATED',
        'R79':'PAUSED_NON_BLOCKING','overall_percent':None,
        'next':'QUEST31_MODULE_GAP_REVIEW_THEN_CROSS_MODULE_INTEGRATION_IF_NO_DISTINCT_SOURCE_READY_TASK'
    }
    private['source-summary-derived.json']=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode()
    page=['<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><title>QUEST30 恐龍收集員原來源</title><style>body{max-width:900px;margin:30px auto;background:#14252b;color:#ecf3f7;font:16px system-ui}pre{white-space:pre-wrap;overflow-wrap:anywhere}details{background:#24343b;margin:14px 0;padding:12px}img{image-rendering:pixelated;width:auto;max-width:160px}</style>',
          '<h1>恐龍收集委託：來源限定查閱</h1><p>社群混合2.5保存檔案。完整原文只限私人查閱；未進入原遊戲、未驗證原服交寵或獎勵。</p>',
          '<p>特別注意：原腳本將2607描述成證明道具，現保存的兩份itemset同ID卻命名為戒指；不得自行統一版本來源。原EVDEL、兩階段重複及原逗號照錄，不當成已知執行規則。</p>']
    for p in (CREATE,TEMPLATE,SCRIPT):
        page.append('<details><summary>'+html.escape(p)+'</summary><pre>'+html.escape(private['original-npc/'+p].decode('cp950'))+'</pre></details>')
    page.append('<h2>來源道具2607的兩條完整行（同表位置保留）</h2>')
    for table in ('itemset.txt','itemset0710.txt'):
        page.append('<details><summary>'+table+'</summary><pre>'+html.escape(private[f'original-itemrows/{table}/2607.txt'].decode('cp950'))+'</pre></details>')
    page.append('<p>臺灣1.0另一來源候選圖：不能當成本社群任務當時顯示的同一圖像</p><img src="cross-carrier-TW1-item-candidates/'+str(alias)+'.png" alt="跨來源候選圖">')
    page.append('</html>');private['index.html']=''.join(page).encode('utf-8')
    return report,private


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for k in ('npc-zip','item-zip','quest01-index','char01-index','item-dir','private-zip'):
        p.add_argument('--'+k,type=Path,required=True)
    p.add_argument('--output',type=Path,default=OUTPUT)
    a=p.parse_args()
    assert ROOT not in a.private_zip.resolve().parents
    report,private=derive(a.npc_zip,a.item_zip,a.quest01_index,a.char01_index,a.item_dir)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with zipfile.ZipFile(a.private_zip,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8) as z:
        for name,b in sorted(private.items()):z.writestr(name,b)
    print(json.dumps({'private_files':len(private),'event_sections':len(report['source_script']['events'])},ensure_ascii=False))

if __name__=='__main__':main()