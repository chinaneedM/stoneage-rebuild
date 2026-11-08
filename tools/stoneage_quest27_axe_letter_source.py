"""Original event-3/5 axe-letter source chain; original assets stay private."""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
import zipfile

from tools.stoneage_quest08_mining_source import load_private_source
from tools.stoneage_quest17_dino_ranch_source import NPC_ZIP_SHA, ITEM_ZIP_SHA, source_info, sha
from tools.stoneage_quest21_liuli_source import ROOT, REC, QUEST01, CHAR01, load, pin
from tools.stoneage_quest23_poru_source import catalog_sections
from tools.stoneage_quest25_island_tour_source import Q05
from tools.stoneage_quest26_shell_flower_source import read_source_items
from tools.stoneage_itemset_schema_probe import SCHEMA

OUTPUT=REC/'STONEAGE-QUEST27-AXE-LETTER-EVENT3-5-SOURCE-R1.json'
CREATE='sainasu/event/event03.create'
SCRIPTS=('sainasu/event/event03_1','sainasu/event/event03_2')
WORLD23='STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-23-NPC-ITEM-TRANSFERS-R1.json'
Q16='STONEAGE-QUEST16-AXE-WOOD-SOURCE-R1.json'


def derive(npc_path,item_path):
    _,ch,data=load_private_source(npc_path);q=load(QUEST01)
    rows=[r for r in ch['create_rows'] if r[0]==CREATE];assert len(rows)==2
    templates={(r[0],r[1]):r for r in ch['template_rows']};files={CREATE,*SCRIPTS};creates=[]
    for r in rows:
        assert sha(data[CREATE][r[2]:r[3]])==r[4]
        p,_,digest=r[15][0];assert sha(data[p])==digest
        tp,n=r[13][0];assert templates[tp,n][4]=='ExChangeMan';files.add(tp)
        creates.append(dict(create_ordinal=r[1],block_sha256=r[4],floor=r[5],borncorner=r[7],
            borncenter=r[8],graphic_alias=r[6],direction=r[10],script_path=p,template_path=tp,
            template_ordinal=n,functionset=templates[tp,n][4]))
    scripts=[dict(**source_info(p,data[p]),events=catalog_sections(data[p],
        [b for b in q['source_event_blocks'] if b['script_path']==p])) for p in SCRIPTS]
    private={'original-npc/'+p:data[p] for p in sorted(files)}
    items,labels=read_source_items(item_path,(2416,2423,2448),private)
    assert SCHEMA[78]==('dropatlogout','bool') and SCHEMA[79]==('vanishatdrop','bool')
    fields=[]
    for item in items:
        for row in item['source_rows']:
            raw=private[f'original-itemrows/{row["table"]}/{item["item_ID"]}.txt'].removesuffix(b'\n')
            columns=raw.decode('cp950').split(',');assert len(columns)==94 and sha(raw)==row['sha256']
            fields.append(dict(item_ID=item['item_ID'],table=row['table'],row_sha256=row['sha256'],
                column78_dropatlogout=int(columns[78]),column79_vanishatdrop=int(columns[79]),
                named_by_existing_descendant94_schema=True,original_loader_or_drop_executed=False))
    steps=[]
    for path,ordinal in [(SCRIPTS[1],1),(SCRIPTS[0],0),(SCRIPTS[0],1),(SCRIPTS[1],0)]:
        s=next(s for s in scripts if s['path']==path);e=s['events'][ordinal]
        c=next(c for c in creates if c['script_path']==path)
        steps.append(dict(script_path=path,event_ordinal=ordinal,event_no=e['event_no'],type=e['type'],
            condition_literal=e['condition_literal'],commands=e['commands'],section_sha256=e['section_sha256'],
            source_create_ordinal=c['create_ordinal'],source_floor=c['floor']))
    old=load(WORLD23)
    report=dict(schema='stoneage.quest27.axe_letter_event3_and5_source.r1',date='2026-11-08',
        initial_remote=dict(head='7af65dbda8bdb6f2d1c2c02098283f187e817adb',tree='d17d9dcaf27d22f80bcf4b3796a6921b1b11ffd7',
                            preserved_CURRENT_blob='c89e0e33537990aa2132b47c40fef49a985a935c'),
        source_scope='MIXED25_COMMUNITY_PRESERVED_NOT_AUTHENTICATED_OFFICIAL_EARLY_BUILD',
        verified_private_carriers=dict(NPC_ZIP_sha256=NPC_ZIP_SHA,NPC_members_SHA_CRC=2205,
            ITEM_ZIP_sha256=ITEM_ZIP_SHA,ITEM_members_CRC=838,parent_RAR_reread=False),
        old_evidence_inputs=[pin(p) for p in (QUEST01,CHAR01,Q05,Q16,WORLD23)],
        existing_WORLD23_mentions_in_serialized_report={p:json.dumps(old).count(p) for p in SCRIPTS},
        existing_QUEST01_TYPE_sections=5,new_original_script_discoveries=0,
        source_manifest=[source_info(p,data[p]) for p in sorted(files)],source_creates=creates,source_scripts=scripts,
        source_item_and_flag_link_order=steps,source_items=items,source_drop_field_values=fields,
        source_map_metadata_reused=[r for r in load(Q05)['floors'] if r['source_floor_id'] in (1300,1400)],
        boundaries=dict(source_link_order_executed_as_native_route=False,actual_handoff_or_reward_executed=False,
            omitted_quantity_replaced_with_one=False,comma_condition_interpreted=False,
            source_dialogue_claim_treated_as_actual_drop_observation=False,
            descendant94_field_names_prove_original_loader=False,original_DAT_or_NPC_sprite_replayed=False,
            official_early_same_deployment_authenticated=False,original_assets_or_dialogue_published=False,
            quest_origin='UNRESOLVED'),stage_A={'PARTIAL':7,'OPEN':2},stage_B='GATED',wiki='GATED',
        R79='PAUSED_NON_BLOCKING',overall_percent=None,next='QUEST28_MODULE_REVIEW_AFTER_TWO_COURIER_FAMILIES_SOURCE_STOP')
    private['source-summary-derived.json']=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode()
    page='<!doctype html><meta charset="utf-8"><title>QUEST27 斧头与感谢函原资料</title><style>body{font:16px sans-serif;max-width:1050px;margin:30px auto;background:#14272c;color:#eee}pre{white-space:pre-wrap;background:#29434c;padding:15px}td,th{border:1px solid #52717b;padding:10px}table{border-collapse:collapse;width:100%}summary{padding:10px;cursor:pointer}img{image-rendering:pixelated;max-width:160px}</style><h1>斧头交付与感谢函往返：事件3／5</h1><p>后期社区保存来源关系。按物品与旗标整理原字段，未执行任务或丢弃。原对白对两斧头的消失描述与物品表数值并列，不能当成实际原服观察。</p><table><tr><th>原出处</th><th>条件</th><th>命令</th></tr>'
    for e in steps:page+='<tr><td>'+e['script_path']+' #'+str(e['event_ordinal'])+'</td><td>'+html.escape(e['condition_literal'])+'</td><td>'+html.escape(json.dumps(e['commands']))+'</td></tr>'
    page+='</table><h2>原物品与跨来源候选图</h2>'
    for item in items:
        i=item['item_ID'];name,desc=labels[i]
        page+=f'<h3>{i} {html.escape(name)}</h3><img src="cross-carrier-TW1-item-candidates/{item["cross_carrier_candidate_alias"]}.png"><p>{html.escape(desc)}</p>'
    page+='<h2>两原表字段78／79（既有后代94栏命名）</h2><pre>'+html.escape(json.dumps(fields,indent=2))+'</pre><h2>完整原文，保留物理顺序</h2>'
    for p in sorted(files):page+='<details><summary>'+p+'</summary><pre>'+html.escape(data[p].decode('cp950'))+'</pre></details>'
    private['index.html']=page.encode();return report,private


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for key in ('npc-zip','item-zip','private-zip'):p.add_argument('--'+key,type=Path,required=True)
    p.add_argument('--output',type=Path,default=OUTPUT);a=p.parse_args();assert ROOT not in a.private_zip.resolve().parents
    r,private=derive(a.npc_zip,a.item_zip);a.output.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with zipfile.ZipFile(a.private_zip,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8) as z:
        for n,b in sorted(private.items()):z.writestr(n,b)
    print(json.dumps(dict(files=len(r['source_manifest']),events=5,private_members=len(private))))


if __name__=='__main__':main()
