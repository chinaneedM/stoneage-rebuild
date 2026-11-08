"""QUEST31: bounded source dossier for event 9-12 across four saved NPC positions.

Only PRIVATE zip arguments contain original script dialogue, original item rows and
copyrighted image candidates. Public JSON contains numeric source predicates,
short item names, hashes, evidence boundaries, and cross-module references.
This module does not execute original event, item, charm, or reward semantics.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import html
import json
from pathlib import Path
import re
import zipfile

from tools.stoneage_quest29_spirit_king_source import (
    NPC_SHA, ITEM_SHA, Q_SHA, CH_SHA, Q_BLOB, CH_BLOB,
    sha, info, index_pin, sections,
)

ROOT=Path(__file__).resolve().parents[1]
REC=ROOT/'research/recovered'
OUTPUT=REC/'STONEAGE-QUEST31-FOUR-VILLAGE-EVENT09-12-SOURCE-R1.json'
CREATE='sainasu/event/event09-12.create'
SCRIPTS=tuple(f'sainasu/event/event{n:02}' for n in range(9,13))
TEMPLATE='jaruga/event/event.template'
ITEM_IDS=(1052,1357,2419,2420,2421,2736)
CURRENT_BLOB='c89e0e33537990aa2132b47c40fef49a985a935c'
Q05_BLOB='b004e488e1d0a93ca7c14eb90abb584b23f341fe'
MAP_STATUSES={
    1200:('MAP09_GT99_RD_SOURCE_READY_CANDIDATE','41cae3e9e07ecee4e51c0a8417afef008afedc6e494cd7ba31241662015c5f07'),
    1300:('NO_MATCHING_DAT_IN_955',None),
    1400:('MAP09_GT99_RD_SOURCE_READY_CANDIDATE','a706890eaa46f89e41ca171ce052d34fb1c18e8cc4602ac686fc1d19af54c73f'),
    11107:('MAP09_GT99_RD_SOURCE_READY_CANDIDATE','1adbf43476b9e1745f7b38b7f48a1c0632fb2d2a47952774cae3d025ed9ef3cc'),
}


def derive(npc_path:Path,item_path:Path,quest01:Path,char01:Path,item_dir:Path):
    q_pin=index_pin(quest01,Q_SHA,Q_BLOB)
    ch_pin=index_pin(char01,CH_SHA,CH_BLOB)
    q=json.loads(quest01.read_text(encoding='utf-8'))
    ch=json.loads(char01.read_text(encoding='utf-8'))
    assert sha(npc_path.read_bytes())==NPC_SHA
    assert sha(item_path.read_bytes())==ITEM_SHA
    assert len(q['source_scripts'])==295 and len(q['source_event_blocks'])==1349
    old_file={r[0]:r for r in ch['source_files']}
    old_scripts={r['path']:r for r in q['source_scripts']}
    assert set(SCRIPTS)<=old_scripts.keys()
    private={}
    def get_bytes(z,p):
        b=z.read('npc/'+p)
        r=old_file[p]
        assert (len(b),sha(b),f'{z.getinfo("npc/"+p).CRC:08x}')==tuple(r[1:4])
        private['original-npc/'+p]=b
        return b
    with zipfile.ZipFile(npc_path) as z:
        assert len(z.namelist())==2205 and z.testzip() is None
        for name in z.namelist():
            assert name.startswith('npc/')
            b=z.read(name);r=old_file[name[4:]]
            assert (len(b),sha(b),f'{z.getinfo(name).CRC:08x}')==tuple(r[1:4])
        raw=get_bytes(z,CREATE)
        template=get_bytes(z,TEMPLATE)
        creates=[r for r in ch['create_rows'] if r[0]==CREATE]
        assert len(creates)==4
        template_row=next(t for t in ch['template_rows'] if t[0]==TEMPLATE and t[1]==0)
        assert template_row[4]=='ExChangeMan'
        old_refs={(r['create_source_path'],r['create_brace_ordinal']):r for r in q['source_creation_references']}
        create_rows=[]
        for i,c in enumerate(creates):
            p=SCRIPTS[i]
            assert c[1]==i and sha(raw[c[2]:c[3]])==c[4]
            assert c[13]==[[TEMPLATE,0]]
            assert c[15][0][0]==p and c[15][0][1]=='EXACT_SAME_NPC_SUBTREE_PATH'
            assert c[15][0][2]==old_scripts[p]['original_sha256']
            o=old_refs[(CREATE,i)]
            assert (o['original_script_path'],o['floorid'],o['graphic_alias_numeric'])==(p,c[5],c[6])
            create_rows.append(dict(ordinal=i,create_path=CREATE,source_block_sha256=c[4],
                floor=c[5],borncorner_original_four_numbers=c[7],direction=c[10],
                graphic_alias=c[6],original_template_token=c[11],
                resolved_function=template_row[4],script_path=p,
                map_source_status=MAP_STATUSES[c[5]][0],
                prior_original_DAT_sha256=MAP_STATUSES[c[5]][1],
                actual_original_map_or_NPC_runtime_entered=False))
        assert [c['floor'] for c in create_rows]==[1200,1300,1400,11107]
        scripts=[]
        for p in SCRIPTS:
            b=get_bytes(z,p)
            old=[e for e in q['source_event_blocks'] if e['script_path']==p]
            assert len(old)==old_scripts[p]['source_control_lines']['TYPE']
            parsed=sections(b,old)
            scripts.append(dict(**info(p,b),events=parsed,already_in_QUEST01=True))
        assert [len(s['events']) for s in scripts]==[3,5,5,5]
        all_events=[e for s in scripts for e in s['events']]
        assert Counter(e['type'] for e in all_events)==Counter({'ACCEPT':8,'REQUEST':5,'MESSAGE':5})
        a={s['path']:s['events'] for s in scripts}
        assert a[SCRIPTS[0]][0]['commands']=={'GetItem':['1357'],'EndSetFlg':['9']}
        assert a[SCRIPTS[1]][0]['commands']['EndSetFlg']==['10,12']
        assert a[SCRIPTS[1]][1]['commands']['EndSetFlg']==['10']
        assert a[SCRIPTS[2]][0]['commands']['EndSetFlg']==['11,12']
        assert a[SCRIPTS[2]][1]['commands']['EndSetFlg']==['11']
        assert a[SCRIPTS[2]][0]['commands']['Charm']==['1']
        assert a[SCRIPTS[3]][0]['commands']['GetItem']==['2419,2420']
        assert a[SCRIPTS[3]][2]['commands']['GetItem']==['2736']
        assert a[SCRIPTS[3]][3]['commands']['EndSetFlg']==['41']
        # Event 41/42 conditions are not inferred as successful native execution.
        assert a[SCRIPTS[3]][1]['condition_literal']=='ENDEV=12&ITEM=2736,ENDEV=42&ITEM=2736,ENDEV=41&ITEM=2736'
        assert a[SCRIPTS[3]][2]['condition_literal']=='ENDEV=41&ITEM!=2736&ENDEV=4&NOWEV=42'
        assert a[SCRIPTS[3]][3]['condition_literal']=='LV>0&NOWEV=41&ENDEV=4&NOWEV=42'
        # Old QUEST01 integer-only EndSetFlg projection drops both compound ',12' source values.
        assert not any(12 in e['end_set_flags'] for e in q['source_event_blocks'])
        assert not q['source_event_blocks'][next(i for i,v in enumerate(q['source_event_blocks'])
            if v['script_path']==SCRIPTS[1] and v['script_block_ordinal']==0)]['end_set_flags']
    # Review all 14 prefixes, but don't turn them into claims of specialist coverage.
    directories=Counter('/'.join(s['path'].split('/')[:-1]) for s in q['source_scripts'])
    assert len(directories)==14 and sum(directories.values())==295
    shard_index={}
    for n in range(1,8):
        shard=json.loads((item_dir/f'STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-{n:02d}-R1.json').read_text('utf8'))
        for row in shard['rows']:
            assert row[0] not in shard_index
            shard_index[row[0]]=row
    item_names={};item_records=[];alias_to_png={}
    with zipfile.ZipFile(item_path) as z:
        assert len(z.namelist())==838 and z.testzip() is None
        data=json.loads(z.read('private-full-catalog.json'))
        source={r['id']:r for r in data['items']}
        images={r['source_itemset_image_number_alias']:r for r in data['image_source_receipts']}
        for n in ITEM_IDS:
            row=source[n];two=[];aliases=set()
            for col,table in ((1,'itemset.txt'),(2,'itemset0710.txt')):
                r=row[table];cols=r['original_94_columns']
                assert len(cols)==94 and int(cols[16])==n
                raw=','.join(cols).encode('cp950')
                assert sha(raw)==r['original_row_sha256']==shard_index[n][col]
                private[f'original-itemrows/{table}/{n}.txt']=raw+b'\n'
                aliases.add(int(cols[17]));two.append(dict(table=table,source_row_1based=r['source_row_1based'],
                    source_row_sha256=sha(raw),source_alias=int(cols[17])))
                item_names[n]=cols[0]
            assert len(aliases)==1 and two[0]['source_row_sha256']==two[1]['source_row_sha256']
            alias=next(iter(aliases));im=images[alias]
            assert im['tw1_original_RD_status']=='VERIFIED_ORIGINAL_RD_INDEXED_PIXELS'
            png=z.read(f'source-TW1-original-RD-candidates/alias-{alias}.png')
            assert sha(png)==im['candidate_PNG_SHA256']
            private[f'cross-carrier-TW1-item-candidates/{alias}.png']=png
            alias_to_png[alias]=sha(png)
            item_records.append(dict(item_ID=n,short_original_name=cols[0],source_two_rows=two,
                original_source_itemset_image_alias=alias,cross_carrier_TW1_candidate_PNG_sha256=sha(png),
                same_official_build_or_original_quest_display_proven=False))
    assert set(alias_to_png)=={21025,22024,24057,24058,24071,24213}
    # Extract IDs from only recognized item operands; not from flags/level/stone or other nouns.
    ids=set()
    for s in scripts:
        for e in s['events']:
            ids.update(int(n) for n in re.findall(r'(?<![A-Z_])ITEM(?:!=|=|>=|<=|>|<)(\d+)',e['condition_literal']))
            for key in ('GetItem','DelItem'):
                for literal in e['commands'].get(key,[]):
                    ids.update(int(n) for n in re.findall(r'(?:^|,)\s*(\d+)',literal))
    assert ids==set(ITEM_IDS)
    report=dict(
        schema='stoneage.quest31.four_village_event09_12_original_source.r1',date='2026-11-08',
        initial_remote=dict(head='4751ebe021110e96867d8c4d802669791bfd1ba4',
            tree='06dcb561a86de9187b106a4528d8256c96f1cc4a',preserved_CURRENT_git_blob=CURRENT_BLOB),
        source_scope='COMMUNITY_MIXED25_PRESERVED_NOT_AUTHENTICATED_EARLY_OFFICIAL',
        source_archive_evidence=dict(NPC_private_zip_sha256=NPC_SHA,NPC_members_full_SHA_CRC_verified=2205,
            ITEM_private_zip_sha256=ITEM_SHA,ITEM_members_CRC_verified=838,parent_RAR_reread=False,
            prior_QUEST01=q_pin,prior_CHAR01=ch_pin),
        source_module_census=dict(prior_QUEST01_script_count=295,prior_QUEST01_TYPE_count=1349,
            prior_QUEST01_directories=dict(sorted(directories.items())),
            selected_original_scripts_already_in_QUEST01=4,selected_original_TYPE_already_in_QUEST01=18,
            newly_discovered_original_scripts=0,newly_discovered_original_TYPE=0,
            legacy_QUEST01_integer_EndSetFlg_flag12_matches=0,
            source_compound_EndSetFlg_with_flag12=[
                dict(script=SCRIPTS[1],event_ordinal=0,exact_line='10,12'),
                dict(script=SCRIPTS[2],event_ordinal=0,exact_line='11,12')],
            legacy_flag12_absence_not_source_absence=True),
        original_files=[info(p,private['original-npc/'+p]) for p in (CREATE,*SCRIPTS,TEMPLATE)],
        source_create_records=create_rows,
        source_scripts=scripts,
        source_event_type_totals=dict(Counter(e['type'] for e in all_events)),
        source_story_control_literals=dict(
            event12_issue_tokens=a[SCRIPTS[3]][0]['commands']['GetItem'][0],
            event10_alternative_flag_literals=[a[SCRIPTS[1]][n]['commands']['EndSetFlg'][0] for n in (0,1)],
            event11_alternative_flag_literals=[a[SCRIPTS[2]][n]['commands']['EndSetFlg'][0] for n in (0,1)],
            event09_final_requirement=a[SCRIPTS[0]][0]['condition_literal'],
            event09_reward=a[SCRIPTS[0]][0]['commands']['GetItem'][0],
            event41_42_coupled_conditions=[a[SCRIPTS[3]][n]['condition_literal'] for n in (1,2,3)],
            event12_41_reward_item='2736',
            actual_order_or_multiple_flags_execution_proven=False),
        source_items=item_records,
        source_item_count=6,source_item_rows=12,distinct_cross_carrier_image_aliases=6,
        prior_QUEST05_map_source_git_blob=Q05_BLOB,
        unresolved_map_1300=dict(no_matching_DAT_in_955=True,original_map_proven_absent=False),
        source_constraints=dict(original_script_text_or_dialogue_in_public_repo=False,
            original_source_item_rows_or_image_bytes_in_public_repo=False,
            original_client_or_server_running=False,
            early_official_same_deployment_proven=False,
            cross_carrier_TW1_art_is_original_mixed25_quest_UI=False,
            native_EVENT_conditional_priority_or_comma_semantics_proven=False,
            native_EndSetFlg_multi_value_execution_proven=False,
            source_Charm_1_effect_proven=False,
            same_quest_as_early_version_proven=False,
            geographic_island_or_village_hierarchy_authenticated=False,
            native_NPC_or_scene_rendered=False,task_origin='UNRESOLVED'),
        stage_A={'PARTIAL':7,'OPEN':2},stage_B='GATED',wiki='GATED',R79='PAUSED_NON_BLOCKING',
        overall_percent=None,
        next='QUEST32_MODULE_STOP_OR_ADDITIONAL_CROSS_MODULE_INTEGRATION_REVIEW_AFTER_FOUR_VILLAGE_CHAIN'
    )
    private['source-summary-derived.json']=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    chunks=['<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><title>QUEST31 原四地事件9–12</title><style>body{max-width:1100px;margin:25px auto;background:#172930;color:#eaf4f4;font:16px system-ui}details{margin:12px 0;padding:15px;background:#29424a;border-radius:8px}pre{white-space:pre-wrap;overflow-wrap:anywhere}img{image-rendering:pixelated;max-width:128px;max-height:128px}</style>',
        '<h1>來源限定：事件9–12 四地任务原文與物品</h1><p>後期社群混合2.5資料；非已運行原版、非最早官方部署。floor1300缺本批已驗DAT；跨來源臺灣1.0道具候選圖不證明同服顯示。</p>']
    for p in (CREATE,*SCRIPTS,TEMPLATE):
        chunks.append('<details><summary>'+html.escape(p)+'</summary><pre>'+html.escape(private['original-npc/'+p].decode('cp950'))+'</pre></details>')
    for i in ITEM_IDS:
        alias=next(r['original_source_itemset_image_alias'] for r in item_records if r['item_ID']==i)
        chunks.append('<details><summary>'+str(i)+' '+html.escape(item_names[i])+'</summary><img src="cross-carrier-TW1-item-candidates/'+str(alias)+'.png">')
        for table in ('itemset.txt','itemset0710.txt'):
            chunks.append('<pre>'+html.escape(private[f'original-itemrows/{table}/{i}.txt'].decode('cp950'))+'</pre>')
        chunks.append('</details>')
    chunks.append('</html>');private['index.html']=''.join(chunks).encode('utf8')
    return report,private


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for key in ('npc-zip','item-zip','quest01-index','char01-index','item-dir','private-zip'):
        p.add_argument('--'+key,type=Path,required=True)
    p.add_argument('--output',type=Path,default=OUTPUT)
    a=p.parse_args()
    assert ROOT not in a.private_zip.resolve().parents
    report,private=derive(a.npc_zip,a.item_zip,a.quest01_index,a.char01_index,a.item_dir)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    with zipfile.ZipFile(a.private_zip,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8) as z:
        for n,b in sorted(private.items()):z.writestr(n,b)
    print(json.dumps({'script_count':len(report['source_scripts']),'source_events':sum(len(s['events']) for s in report['source_scripts']),'private_members':len(private)},ensure_ascii=False))

if __name__=='__main__':main()
