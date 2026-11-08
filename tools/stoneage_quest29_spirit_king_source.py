"""Bounded native-source catalogue for the preserved mixed25 event69 family.

Raw original NPC text, scripts, item rows, and candidate image bytes are read only
from explicitly supplied PRIVATE archives, and never written to the public report.
This does not execute game predicates, quests, warps, or random rewards.
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

ROOT=Path(__file__).resolve().parents[1]
REC=ROOT/'research/recovered'
OUTPUT=REC/'STONEAGE-QUEST29-SPIRIT-KING-EVENT69-SOURCE-R1.json'
NPC_SHA='c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f'
ITEM_SHA='cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa'
Q_SHA='2995e5825ffd204d5fd31ccffc95f009d8abbcebad829c5824e490b7f20c2b2c'
CH_SHA='f6beb17b76b23211d36113bcf462c16ac38435233b3891bb21765179b84e4566'
Q_BLOB='52db8b4b6cd43cd2afa4a8d2e8460f214933f5e2'
CH_BLOB='a088b61a3212f7049e7793f587123ffb29bebad7'
CREATE='king/event69_alpha.create'
EXTERNAL_CREATE='giiru/event/event30.create'
ITEM_FIELDS=('GetItem','DelItem','GetRandItem','GetPet','DelPet','EndSetFlg','GetStone','DelStone','NpcWarp','NotDel','Charm')


def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def info(p:str,b:bytes)->dict:
    import zlib
    return dict(path=p,bytes=len(b),sha256=sha(b),crc32=f'{zlib.crc32(b)&0xffffffff:08x}')

def gitblob(b:bytes)->str:
    return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\x00'+b).hexdigest()

def index_pin(path:Path,expected_sha:str,expected_blob:str|None=None)->dict:
    b=path.read_bytes()
    assert sha(b)==expected_sha,(path,sha(b))
    if expected_blob:assert gitblob(b)==expected_blob
    return dict(path=str(path.name),bytes=len(b),sha256=sha(b),git_blob=gitblob(b))

def sections(b:bytes,old:list[dict])->list[dict]:
    text=b.decode('cp950','strict').replace('\r\n','\n')
    lines=text.splitlines(keepends=True)
    assert [i for i,l in enumerate(lines,1) if l.startswith('TYPE:')]==[r['source_type_line'] for r in old]
    result=[]
    for j,r in enumerate(old):
        start=(r['source_eventno_line'] or r['source_type_line'])-1
        stop=((old[j+1]['source_eventno_line'] or old[j+1]['source_type_line'])-1) if j+1<len(old) else len(lines)
        end=next((i+1 for i in range(r['source_type_line'],stop) if lines[i].strip()=='EventEnd'),None)
        assert (end is not None)==r['source_End_found']
        sub=''.join(lines[start:end if end is not None else stop])
        assert sha(sub.encode())==r['source_section_decoded_cp950_normalized_UTF8_sha256']
        cond=re.search(r'(?m)^EVENT:([^\r\n]*)',sub)
        assert cond is not None and sha(cond.group(1).encode())==r['condition_expression_decoded_cp950_UTF8_sha256']
        acts={field:re.findall(rf'(?m)^\s*{field}:([^\r\n]*)',sub) for field in ITEM_FIELDS}
        result.append(dict(ordinal=j,type=r['raw_type'],event_no=r['event_number'],
            condition_literal=cond.group(1),condition_sha256=sha(cond.group(1).encode()),
            section_sha256=sha(sub.encode()),source_type_line=r['source_type_line'],
            commands={k:v for k,v in acts.items() if v},
            exact_EventEnd_found=end is not None))
    return result

def derive(npc_zip:Path,item_zip:Path,quest01:Path,char01:Path,item_dir:Path):
    q_pin=index_pin(quest01,Q_SHA,Q_BLOB);ch_pin=index_pin(char01,CH_SHA,CH_BLOB)
    q=json.loads(quest01.read_text('utf8'));ch=json.loads(char01.read_text('utf8'))
    assert sha(npc_zip.read_bytes())==NPC_SHA
    assert sha(item_zip.read_bytes())==ITEM_SHA
    q_scripts={s['path']:s for s in q['source_scripts']}
    paths=sorted(x for x in q_scripts if x.startswith('king/event69_') and q_scripts[x]['source_control_lines'].get('TYPE',0)>0)
    assert len(paths)==13
    old_blocks={p:[b for b in q['source_event_blocks'] if b['script_path']==p] for p in paths}
    old_file={r[0]:r for r in ch['source_files']}
    selected=[r for r in ch['create_rows'] if r[0]==CREATE or (r[0]==EXTERNAL_CREATE and r[15] and r[15][0][0]=='king/event69_1')]
    assert len(selected)==25 and sum(r[0]==CREATE for r in selected)==24
    all_names=[];private={}
    with zipfile.ZipFile(npc_zip) as z:
        assert len(z.namelist())==2205 and z.testzip() is None
        assert all(n.startswith('npc/') for n in z.namelist())
        # Every retained member must match the pre-existing whole-NPC census.
        for n in z.namelist():
            p=n[4:];b=z.read(n);r=old_file[p]
            assert (len(b),sha(b),f'{z.getinfo(n).CRC:08x}')==tuple(r[1:4])
        def get(p):
            b=z.read('npc/'+p)
            assert len(b)==old_file[p][1] and sha(b)==old_file[p][2]
            all_names.append(p);private['original-npc/'+p]=b
            return b
        source_configs=[]
        old_refs={(r['create_source_path'],r['create_brace_ordinal']):r for r in q['source_creation_references']}
        templates={(r[0],r[1]):r for r in ch['template_rows']}
        for r in selected:
            raw=get(r[0]);assert sha(raw[r[2]:r[3]])==r[4]
            p,role,ref_sha=r[15][0];assert role=='EXACT_SAME_NPC_SUBTREE_PATH' and sha(get(p))==ref_sha
            tp,tno=r[13][0];trow=templates[(tp,tno)];assert sha(get(tp))==old_file[tp][2]
            if p in paths:
                o=old_refs[(r[0],r[1])]
                assert (o['original_script_path'],o['original_script_sha'],o['floorid'],o['graphic_alias_numeric'])==(p,ref_sha,r[5],r[6])
                assert trow[4]=='ExChangeMan'
            source_configs.append(dict(create_path=r[0],create_ordinal=r[1],source_block_sha256=r[4],
                source_byte_span=[r[2],r[3]],floor=r[5],borncorner=r[7],direction=r[10],
                graphic_alias=r[6],function_token=r[11],template_path=tp,
                template_ordinal=tno,template_functionset=trow[4],source_parameter_path=p,
                source_parameter_sha256=ref_sha,script_with_TYPE_blocks=p in paths))
        scripts=[]
        for p in paths:
            b=get(p);o=q_scripts[p]
            assert (len(b),sha(b),f'{z.getinfo("npc/"+p).CRC:08x}')==(o['original_size'],o['original_sha256'],o['original_crc32'])
            scripts.append(dict(**info(p,b),events=sections(b,old_blocks[p])))
    assert len([r for r in source_configs if r['script_with_TYPE_blocks']])==13
    assert len({s['path'] for s in scripts})==13
    # Reuse validated item source positions from all seven old public shards.
    shard_index={}
    for n in range(1,8):
        p=item_dir/f'STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-{n:02d}-R1.json'
        if not p.exists():p=item_dir/f'STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-{n:02d}-R1.json'
        d=json.loads(p.read_text('utf8'))
        for r in d['rows']:
            assert r[0] not in shard_index
            shard_index[r[0]]=r
    item_ids=set()
    for s in scripts:
        for e in s['events']:
            item_ids.update(int(n) for n in re.findall(r'(?<![A-Z_])ITEM(?:!=|=|>=|<=|>|<)(\d+)',e['condition_literal']))
            for k in ('GetItem','DelItem','GetRandItem'):
                for v in e['commands'].get(k,[]):
                    item_ids.update(int(n) for n in re.findall(r'(?:^|,)\s*(\d+)',v))
    # Source operation counts include special `GetRandItem` repeated positions.
    q_item_refs={n for p in paths for r in old_blocks[p] for vals in r['item_numeric_refs'].values() for n in vals}
    assert item_ids==q_item_refs, (sorted(item_ids-q_item_refs),sorted(q_item_refs-item_ids))
    items=[]; images=set();missing_images=set();private_names={}
    with zipfile.ZipFile(item_zip) as z:
        assert len(z.namelist())==838 and z.testzip() is None
        cat=json.loads(z.read('private-full-catalog.json'))
        idx={row['id']:row for row in cat['items']}
        img={row['source_itemset_image_number_alias']:row for row in cat['image_source_receipts']}
        for i in sorted(item_ids):
            rows=[];labels=None
            for col,tbl in ((1,'itemset.txt'),(2,'itemset0710.txt')):
                old=idx[i][tbl];columns=old['original_94_columns']
                assert len(columns)==94 and int(columns[16])==i
                raw=','.join(columns).encode('cp950')
                assert sha(raw)==old['original_row_sha256']==shard_index[i][col]
                private[f'original-itemrows/{tbl}/{i}.txt']=raw+b'\n'
                rows.append(dict(table=tbl,source_row_1based=old['source_row_1based'],sha256=sha(raw),
                                source_image_alias=int(columns[17])))
                if labels is None:labels=(columns[0],columns[2])
            private_names[i]=labels
            a=rows[0]['source_image_alias'];images.add(a)
            candidate=img.get(a)
            qualified=bool(candidate and candidate['tw1_original_RD_status']=='VERIFIED_ORIGINAL_RD_INDEXED_PIXELS'
                and ('source-TW1-original-RD-candidates/alias-'+str(a)+'.png') in z.namelist())
            d={'item_ID':i,'source_rows':rows,'original_rows_identical':rows[0]['sha256']==rows[1]['sha256'],
                'cross_carrier_TW1_candidate':qualified,'cross_carrier_alias':a}
            if qualified:
                png=z.read(f'source-TW1-original-RD-candidates/alias-{a}.png')
                assert sha(png)==candidate['candidate_PNG_SHA256']
                private[f'cross-carrier-TW1-item-candidates/{a}.png']=png
                d['candidate_PNG_sha256']=sha(png)
            else:missing_images.add(i)
            items.append(d)
    assert len(items)==48
    events=[e for s in scripts for e in s['events']];assert len(events)==71
    flag_operands=[v for e in events for v in e['commands'].get('EndSetFlg',[])]
    special={
        'first_person_pet_directions':[dict(script=s['path'],event_ordinal=e['ordinal'],GetPet_literal=v)
            for s in scripts for e in s['events'] for v in e['commands'].get('GetPet',[])],
        'long_trailing_comma_delitem':[dict(script=s['path'],event_ordinal=e['ordinal'],DelItem_literal=v)
            for s in scripts for e in s['events'] for v in e['commands'].get('DelItem',[]) if v.endswith(',')],
        'raw_comma_separated_endset':[dict(script=s['path'],event_ordinal=e['ordinal'],EndSetFlg_literal=v)
            for s in scripts for e in s['events'] for v in e['commands'].get('EndSetFlg',[]) if ',' in v],
        'raw_random_lists':[dict(script=s['path'],event_ordinal=e['ordinal'],GetRandItem_literal=v,
            original_order_includes_duplicates=len(v.split(','))>len(set(v.split(','))))
            for s in scripts for e in s['events'] for v in e['commands'].get('GetRandItem',[])]}
    assert sorted(int(x['GetPet_literal']) for x in special['first_person_pet_directions'])==[355,484,1479]
    assert any(x['DelItem_literal'].endswith(',') for x in special['long_trailing_comma_delitem'])
    assert '122,123' in [x['EndSetFlg_literal'] for x in special['raw_comma_separated_endset']]
    namespace_counts=Counter(x.rsplit('/',1)[0] for x in q_scripts)
    namespace_events=Counter()
    for x,entry in q_scripts.items():namespace_events[x.rsplit('/',1)[0]]+=entry['source_control_lines'].get('TYPE',0)
    assert sum(namespace_counts.values())==295 and sum(namespace_events.values())==1349 and len(namespace_counts)==14
    script_mention_dedupe={
        'whole_QUEST01_source_script_paths':295,
        'whole_QUEST01_source_TYPE_blocks':1349,
        'original_directory_groups_not_number_of_distinct_quests':[dict(path=k,source_scripts=namespace_counts[k],TYPE_blocks=namespace_events[k]) for k in sorted(namespace_counts)],
        'existing_QUEST01_295_script_index':len(paths),
        'existing_QUEST01_event_blocks':len(events),
        'new_original_scripts_discovered_this_package':0,
        'new_original_event_sections_discovered_this_package':0,
        'earlier_CN25_R113_story_is_media_narrative_not_original_NPC_source':True}
    report={
        'schema':'stoneage.quest29.spirit_king_event69_original_source_and_module_review.r1',
        'date':'2026-11-08','initial_remote':dict(head='1d92ff6a2b183020e4582c6206ab74b137188be7',
            tree='2ea181f8efcd5f8150d6fb421e3d09936fa65da3',preserved_CURRENT_blob='c89e0e33537990aa2132b47c40fef49a985a935c'),
        'source_scope':'LATER_COMMUNITY_MIXED25_NOT_AUTHENTICATED_OFFICIAL_JSS1999_TW1_CN182',
        'verified_source_bundles':dict(NPC_zip_sha256=NPC_SHA,NPC_total_members_SHA_CRC_verified=2205,
            ITEM_zip_sha256=ITEM_SHA,ITEM_total_members_CRC_verified=838,parent_mixed25_RAR_reread=False),
        'old_index_pins':[q_pin,ch_pin],
        'quest_module_dedupe':script_mention_dedupe,
        'full_original_source_manifest':[info(p,private['original-npc/'+p]) for p in sorted(set(all_names))],
        'source_creates':source_configs,'source_event_scripts':scripts,
        'source_event_totals':dict(TYPE=len(events),types=dict(sorted(Counter(e['type'] for e in events).items())),
            raw_EndSetFlg_literals=flag_operands),
        'source_items':items,'item_source_coverage':dict(referenced_distinct_IDs=len(items),
            original_94column_rows=2*len(items),cross_carrier_TW1_qualified_IDs=len(items)-len(missing_images),
            source_image_aliases=len(images),missing_TW1_candidate_item_IDs=sorted(missing_images)),
        'source_original_control_exceptions':special,
        'source_scene_floors':sorted({r['floor'] for r in source_configs}),
        'boundaries':dict(original_script_dialogue_or_full_item_rows_published=False,original_native_game_executed=False,
            original_event_punctuation_interpreted=False,original_random_probabilities_inferred=False,
            GetPet_original_reward_transaction_executed=False,GETPET_355_484_1479_called_same_as_pets=False,
            official_same_build_with_earliest_client_verified=False,early_game_presence_proven=False,
            original_DAT_or_sprite_newly_decoded=False,original_scene_routes_replayed=False,
            source_family_origin='UNRESOLVED'),
        'stage_A':{'PARTIAL':7,'OPEN':2},'stage_B':'GATED','wiki':'GATED',
        'R79':'PAUSED_NON_BLOCKING','overall_percent':None,
        'next':'QUEST30_NEXT_SOURCE_READY_UNSPECIALIZED_QUEST_FAMILY_OR_BOUNDED_MODULE_STOP_AFTER_KING_EVENT69'}
    private['derived-source-summary.json']=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    page=['<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><title>QUEST29 原來源精靈王事件資料</title><style>body{max-width:1100px;margin:30px auto;background:#14232b;color:#e8f0f5;font:16px system-ui}details{margin:10px 0;padding:10px;background:#223744}pre{white-space:pre-wrap;overflow-wrap:anywhere}img{image-rendering:pixelated;max-width:110px}summary{cursor:pointer}code{color:#f1dc85}</style>',
          '<h1>精靈王事件69：原來源私人查閱</h1><p>後期社群 mixed25 保存包；原腳本資料查閱工具，不是原遊戲執行或官方初代版本認證。原繁體依 CP950 保留；跨來源候選圖不代表同一部署。</p>',
          '<p>13 原事件腳本、71 原 TYPE、25 原 CREATE、48 原物品 ID（含未有原圖候選者），保留數字及全部重複/異常欄位。</p>']
    for s in scripts:
        p=s['path'];page.append('<details><summary>'+html.escape(p)+' — '+str(len(s['events']))+' TYPE</summary><pre>'+html.escape(private['original-npc/'+p].decode('cp950'))+'</pre></details>')
    page.append('<h2>原建立設定、模板和參數</h2>')
    for p in sorted(set(all_names)-set(paths)):
        page.append('<details><summary>'+html.escape(p)+'</summary><pre>'+html.escape(private['original-npc/'+p].decode('cp950'))+'</pre></details>')
    page.append('<h2>原物品資料與跨來源候選</h2>')
    for item in items:
        i=item['item_ID'];name,description=private_names[i];alias=item['cross_carrier_alias']
        page.append('<details><summary>'+str(i)+' '+html.escape(name)+'</summary><p>'+html.escape(description)+'</p>'+(
            f'<img src="cross-carrier-TW1-item-candidates/{alias}.png">' if item['cross_carrier_TW1_candidate'] else '該物品無資格足夠的臺灣1.0候選像素，不以假圖填補')+'</details>')
    page.append('</html>');private['index.html']=''.join(page).encode('utf8')
    return report,private


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for key in ('npc-zip','item-zip','quest01-index','char01-index','item-dir'):
        p.add_argument('--'+key,required=True,type=Path)
    p.add_argument('--output',type=Path,default=OUTPUT)
    p.add_argument('--private-zip',required=True,type=Path)
    a=p.parse_args();assert ROOT not in a.private_zip.resolve().parents
    report,private=derive(a.npc_zip,a.item_zip,a.quest01_index,a.char01_index,a.item_dir)
    a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    with zipfile.ZipFile(a.private_zip,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8) as z:
        for name,b in sorted(private.items()):z.writestr(name,b)
    print(json.dumps(dict(scripts=len(report['source_event_scripts']),events=report['source_event_totals']['TYPE'],
        creates=len(report['source_creates']),items=len(report['source_items']),private_members=len(private)),ensure_ascii=False))

if __name__=='__main__':main()
