#!/usr/bin/env python3
"""Source-bound compiled Quiz item roles; no game/quiz execution or simulation."""
import argparse
import hashlib
import html
import json
from pathlib import Path
import re
import struct

from tools.stoneage_quest_currency_source import MANIFEST, RECO, read_json, sha, verified_members
from tools.stoneage_savepoint_item_source import original_image, EXE_SHA

W23='STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-23-NPC-ITEM-TRANSFERS-R1.json'
W24='STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-24-SAVEPOINT-ITEM-ROLE-R1.json'
SYMBOLS={'_NPC_Quiz_selectWindow':0x4ba130,'_NPC_QuizBorderLine':0x4b8390,
         '_NPC_QuizAddItem':0x4b8990,'_NPC_EntryItemCheck':0x4b9860,'_NPC_EntryItemDel':0x4b9ba0,
         '_NPC_Util_GetStrFromStrWithDelim':0x48f3c0,'_ITEM_makeItemAndRegist':0x4fa7d0,
         '_CHAR_addItemSpecificItemIndex':0x475d50,'__ITEM_endExistItemsOne':0x4f72a0,'__CHAR_DelItem':0x433ab0}
CALLS=[(0x4ba9a3,0x48f3c0,'GetItem_field_reader'),(0x4baa07,0x407090,'odd_comma_position_reader'),
       (0x4baf38,0x407090,'following_reward_payload_reader'),(0x4baf4a,0x4b8990,'reward_payload_to_QuizAddItem'),
       (0x4b89e0,0x407090,'count_dot_delimited_reward_candidates'),(0x4b89f3,0x55b030,'multi_candidate_rand_call'),
       (0x4b8a2b,0x407090,'selected_dot_position_reader'),(0x4b8a33,0x55afe0,'selected_candidate_atoi'),
       (0x4b8a3b,0x4fa7d0,'attempt_make_reward_item'),(0x4b8a6a,0x475d50,'attempt_add_reward_to_inventory'),
       (0x4b8add,0x4f72a0,'cleanup_after_bad_inventory_slot'),(0x4ba7ca,0x4b9860,'entry_requirement_check'),
       (0x4bafbe,0x48f3c0,'EntryItem_field_reader'),(0x4bafda,0x4b9ba0,'entry_item_deletion'),
       (0x4b9ece,0x433ab0,'starred_entry_item_inventory_delete'),(0x4ba108,0x433ab0,'bare_entry_item_inventory_delete')]
SPANS=[(0x4b8390,0x4b8405),(0x4ba97e,0x4baa10),(0x4baef1,0x4baf5c),
       (0x4b8990,0x4b8b38),(0x4baf9f,0x4bafe7),(0x4ba7ca,0x4ba7cf),
       (0x4b9ba0,0x4ba130)]


def parse_quiz_reward_field(value):
    """Parse only well-formed source pairs; never coerce malformed tokens to 0."""
    words=value.split(',')
    if not words or len(words)%2:raise ValueError('threshold/payload pairs required')
    pairs=[]
    for i in range(0,len(words),2):
        threshold,payload=words[i:i+2]
        if not re.fullmatch(r'[+-]?\d+',threshold):raise ValueError('unqualified threshold literal')
        tokens=payload.split('.')
        if any(not re.fullmatch(r'\d+',t)for t in tokens):raise ValueError('unqualified reward candidate literal')
        pairs.append({'threshold_comma_position':i+1,'comparison_threshold':int(threshold),
                      'payload_comma_position':i+2,'payload_literal':payload,
                      'ordered_dot_candidate_item_ids':[int(t)for t in tokens]})
    return pairs


def compiled_quiz(data):
    base,take,imm,literal,symbols=original_image(data,SYMBOLS)
    calls=[]
    for va,target,purpose in CALLS:
        b=take(va,5)
        if b[0]!=0xe8 or va+5+struct.unpack_from('<i',b,1)[0]!=target:raise ValueError('compiled Quiz call differs')
        calls.append({'va':va,'target_va':target,'purpose':purpose,'instruction_sha256':sha(b)})
    compare=take(0x4ba9c7,8)
    if compare[:4]!=bytes([0x39,0xc7,0x0f,0x8d])or 0x4ba9cf+struct.unpack_from('<i',compare,4)[0]!=0x4baef1:
        raise ValueError('compiled threshold signed >= branch differs')
    if take(0x4ba9cf,3)!=bytes([0x83,0xc6,2]):raise ValueError('threshold scan stride differs')
    return {'bytes':len(data),'sha256':sha(data),'base':base,'COFF_symbols':symbols,'call_witnesses':calls,
            'literals':[literal(0x59f00b,'GetItem'),literal(0x59ef8c,'EntryItem'),literal(0x59ee62,','),literal(0x59ee64,'.')],
            'immediates':{'GetItem_field_capacity':imm(0x4ba989,0xbb,256),
                          'first_threshold_position':imm(0x4ba9b2,0xbe,1),
                          'threshold_token_capacity':imm(0x4ba9e4,0xb9,32),
                          'reward_payload_capacity':imm(0x4baf04,0xba,256),
                          'candidate_item_token_capacity':imm(0x4b89c3,0xb8,16)},
            'signed_threshold_branch':{'va':0x4ba9c7,'target':0x4baef1,'source_sha256':sha(compare)},
            'code_windows':[{'first_VA':a,'end_VA_exclusive':b,'sha256':sha(take(a,b-a))}for a,b in SPANS],
            'manual_objdump_semantics':{'threshold_scan':'FIRST_MATCHING_ODD_COMMA_POSITION_IN_SOURCE_ORDER',
                'comparison':'SIGNED_SCORE_VALUE_GREATER_OR_EQUAL_THRESHOLD','threshold_position_step':2,
                'payload_position_relative_to_threshold':1,'reward_candidates_delimiter':'.',
                'single_candidate_position':1,'multiple_candidates_selection':'rand()%candidate_count+1',
                'GetItem_role':'SCORE_THRESHOLD_TO_REWARD_CANDIDATE_PAYLOAD',
                'EntryItem_role':'SEPARATE_ENTRY_CHECK_AND_DELETION',
                'guaranteed_original_reward_delivery':False,'actual_score_computation_reaudited':False,
                'original_program_executed':False}}


def derive(exe,npc_zip):
    compiled=compiled_quiz(exe.read_bytes())
    _,members=verified_members(npc_zip,read_json(MANIFEST))
    old=read_json(W23);rows=[];item_ids=set()
    for f in old['files']:
        if not any('Quiz'in ref[8]for ref in f[4]):continue
        data=members[f[0]]
        if sha(data)!=f[2]:raise ValueError('original Quiz file differs')
        op,=[o for o in f[6]if o[1]=='GetItem']
        raw_lines=data.splitlines()
        if sha(raw_lines[op[0]-1])!=op[3]:raise ValueError('original Quiz GetItem line differs')
        pairs=parse_quiz_reward_field(op[2])
        fields={}
        for n,line in enumerate(raw_lines,1):
            if b':'not in line:continue
            k,v=line.split(b':',1)
            if k in (b'Type',b'Answer',b'Level',b'Quiznum',b'EntryItem'):
                fields[k.decode()]={'line':n,'literal':v.decode('ascii'),'line_sha256':sha(line)}
        for p in pairs:item_ids.update(p['ordered_dot_candidate_item_ids'])
        entry=fields.get('EntryItem')
        if entry:
            for t in entry['literal'].split(','):
                m=re.fullmatch(r'(\d+)(?:\*\d+)?',t)
                if m:item_ids.add(int(m[1]))
        rows.append({'path':f[0],'source_bytes':f[1],'source_sha256':f[2],'source_crc32':f[3],
                     'exact_original_CREATE_refs':f[4], 'GetItem_line':op[0],'GetItem_line_sha256':op[3],
                     'GetItem_raw_literal':op[2],'GetItem_source_pairs':pairs,'original_numeric_and_entry_fields':fields,
                     'WORLD23_role_override':{'field':'GetItem','odd_comma_positions':'COMPARISON_THRESHOLD_NOT_ITEM_ID',
                                             'even_comma_positions':'DOT_DELIMITED_REWARD_ITEM_CANDIDATES',
                                             'old_raw_token_record_preserved':True}})
    shard_paths=sorted((RECO/'item-module-01').glob('*.json'))
    index={r[0]:r for p in shard_paths for r in json.loads(p.read_text())['rows']}
    inputs=[RECO/MANIFEST,RECO/W23,RECO/W24,*shard_paths]
    report={'schema':'stoneage.world25.compiled_quiz_item_roles.r1',
            'source_scope':'PRESERVED_COMMUNITY_MIXED25_STATIC_COMPILED_CODE_AND_SOURCE_PARAMETERS_NOT_OFFICIAL_EARLY_DEPLOYMENT',
            'parent_RAR_reread':False,'private_NPC_ZIP_sha256':old['private_source_zip']['sha256'],
            'all_2205_NPC_members_SHA_size_CRC_reverified':True,
            'input_git_blobs':{p.name:hashlib.sha1(b'blob '+str(p.stat().st_size).encode()+b'\0'+p.read_bytes()).hexdigest()for p in inputs},
            'compiled_server':compiled,'source_Quiz_GetItem_rows':rows,
            'counts':{'source_files':len(rows),'GetItem_fields':len(rows),'comparison_threshold_occurrences':sum(len(r['GetItem_source_pairs'])for r in rows),
                      'reward_candidate_positions':sum(len(p['ordered_dot_candidate_item_ids'])for r in rows for p in r['GetItem_source_pairs']),
                      'distinct_reward_item_IDs':len({i for r in rows for p in r['GetItem_source_pairs']for i in p['ordered_dot_candidate_item_ids']})},
            'item01_source_joins':[[i,index.get(i)]for i in sorted(item_ids)],
            'limits':{'original_award_or_entry_consumption_executed':False,'actual_question_or_score_runtime_executed':False,
                      'all_original_GetItem_numbers_are_item_IDs':False,'WORLD23_raw_token_index_rewritten':False,
                      'whole_game_unique_item_count_established':False,'official_TW1_JSS1999_CN182_rule_proven':False,'overall_percent':None},
            'next':'WORLD26: bounded remaining Raceman GetItem source role; then leave item-field helper chain'}
    return report,members


def private_html(report,members,names):
    rows=[]
    for r in report['source_Quiz_GetItem_rows']:
        pairs=''.join('<p>门槛 '+str(p['comparison_threshold'])+' → 奖励候选 '+html.escape(' / '.join(str(i)+' '+names.get(i,'未重读原名')for i in p['ordered_dot_candidate_item_ids']))+'</p>'for p in r['GetItem_source_pairs'])
        fields=r['original_numeric_and_entry_fields'];entry=fields.get('EntryItem',{}).get('literal','缺字段')
        rows.append('<article><h2>'+html.escape(r['path'])+'</h2><p>原GetItem：'+html.escape(r['GetItem_raw_literal'])+'</p>'+pairs+'<p>原入场字段EntryItem：'+html.escape(entry)+'</p><details><summary>原参数全文（私人资料）</summary><pre>'+html.escape(members[r['path']].decode('cp950','replace'))+'</pre></details></article>')
    return '<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>WORLD25 原答题物品字段</title><style>body{max-width:1000px;margin:32px auto;padding:0 24px;background:#f5f1e8;color:#202a32;font:16px/1.65 system-ui}article{background:white;padding:20px;margin:20px 0;border-radius:8px}pre{white-space:pre-wrap;overflow-wrap:anywhere}h2{font-size:19px}</style><h1>WORLD25 · 原答题物品字段</h1><p>保存社区混合2.5编译代码：Quiz的GetItem先门槛、后奖励列表，与SavePoint的消耗条件不同。1和100在下列字段中是门槛，不能算成奖励物品。原入场物品另由EntryItem描述。此为静态代码与参数核对，没有运行原游戏、答题、发奖、扣物或浏览器；不认证初代官方同服。</p>'+''.join(rows)+'</html>'


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--exe',type=Path,required=True);p.add_argument('--npc-zip',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);p.add_argument('--private-html',type=Path);p.add_argument('--private-itemset-a',type=Path)
    a=p.parse_args();r,members=derive(a.exe,a.npc_zip);a.output.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if a.private_html:
        names={}
        if a.private_itemset_a:
            data=a.private_itemset_a.read_bytes()
            if sha(data)!='a415e78f9aab2e5ea5ca92ecb7430253f7be1ba7c876d6b0bb6d067b1b466688':raise ValueError('itemset A identity differs')
            wanted={i:row for i,row in r['item01_source_joins']}
            for line in data.splitlines():
                if not line.strip()or line.lstrip().startswith(b'#'):continue
                f=line.split(b',')
                if len(f)!=94:raise ValueError('itemset A column count differs')
                i=int(f[16])
                if i in wanted:
                    if sha(line)!=wanted[i][1]:raise ValueError('itemset A row differs')
                    names[i]=f[0].decode('cp950')
            if set(names)!=set(wanted):raise ValueError('required item name absent')
        a.private_html.write_text(private_html(r,members,names),encoding='utf-8')
    print(json.dumps(r['counts']))


if __name__=='__main__':main()
