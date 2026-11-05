#!/usr/bin/env python3
"""Bounded static SavePoint item-use evidence from the preserved compiled GMSV.

Never executes the original program or evaluates an inventory/quest. Public
output contains numeric facts and hashes; original program/prose stay private.
"""
import argparse
import hashlib
import html
import json
from pathlib import Path
import struct

from tools.stoneage_quest_currency_source import MANIFEST, RECO, ROOT, read_json, sha, verified_members
from tools.stoneage_wayi_pe_static_inventory import inventory_pe

EXE_SHA = 'd5b08dbcbf9e8736ba8598e38e5901f123d2bff544a9cae53a9ff88ce1971e00'
W23 = 'STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-23-NPC-ITEM-TRANSFERS-R1.json'
G5 = 'STONEAGE-GAMEPLAY05-ORIGINAL-PETSHOP-SAVEPOINT-HEAL-SOURCE-R1.json'
W18 = 'STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-18-BATTLE-ENTRY-BGM-SOURCE-R1.json'
SYMBOLS = {'_strcpysafe': 0x4062a0, '_NPC_Util_GetStrFromStrWithDelim': 0x48f3c0,
           '_NPC_MessageDisp': 0x498820,
           '_NPC_AndReduce': 0x498b40, '_NPC_SavePointItemDelete': 0x498fd0,
           '_NPC_AndReduceDelete': 0x4991c0, '_NPC_UsedCheck': 0x499440,
           '_NPC_SavePointWindowTalked': 0x4995d0, '_NPC_SavePointTalked': 0x499650,
           '__CHAR_DelItem': 0x433ab0}
CALLS = [(0x499862, 0x499440, 'talk_checks_without_consumption'),
         (0x49962a, 0x499440, 'window_reply_requests_consumption'),
         (0x4994d5, 0x48f3c0, 'GetItem_field_reader'),
         (0x48f4c2, 0x4062a0, 'reader_calls_bounded_copy'),
         (0x499515, 0x407090, 'comma_position_reader'),
         (0x499548, 0x498b40, 'component_condition_check'),
         (0x499587, 0x498b40, 'single_component_condition_check'),
         (0x4995b4, 0x4991c0, 'successful_condition_enters_delete_path'),
         (0x4992a9, 0x498fd0, 'single_quantity_item_delete'),
         (0x499365, 0x498fd0, 'conjunction_quantity_item_delete'),
         (0x4993f8, 0x498fd0, 'conjunction_bare_item_delete'),
         (0x499194, 0x433ab0, 'inventory_item_deletion'),
         (0x4989fb, 0x42dcf0, 'activation_state_write'),
         (0x498a3c, 0x42dcf0, 'last_elder_state_write')]
SPANS = [(0x4062a0,0x40635e), (0x48f3c0,0x48f4e1), (0x498820,0x498a90),
         (0x498b40,0x498fc2), (0x498fd0,0x4991c0),
         (0x4991c0,0x499431), (0x499440,0x4995ce), (0x4995d0,0x499650),
         (0x4997d1,0x4998d2)]


def ascii_copy_projection(value, capacity=128):
    """Only the proven ASCII copy bound; not a game parser or runtime trace."""
    if capacity < 1 or '\0' in value:
        raise ValueError('positive capacity and NUL-free source required')
    raw = value.encode('ascii')
    return raw[:capacity - 1].decode('ascii')


def original_image(data, expected_symbols):
    """Shared, exact-image byte access for bounded compiled NPC investigations."""
    if len(data) != 1897867 or sha(data) != EXE_SHA:
        raise ValueError('complete original compiled GMSV identity differs')
    inv = inventory_pe(data)
    pe = struct.unpack_from('<I', data, 60)[0]
    base = struct.unpack_from('<I', data, pe + 24 + 28)[0]
    def take(va, size):
        for s in inv['sections']:
            delta = va - base - s['rva']
            if 0 <= delta and delta + size <= s['raw_size']:
                off = s['raw_offset'] + delta
                return data[off:off + size]
        raise ValueError('source VA outside original raw section')
    def imm(va, opcode, expected):
        b = take(va, 5)
        if b[0] != opcode or struct.unpack_from('<I', b, 1)[0] != expected:
            raise ValueError('compiled immediate differs')
        return {'va': va, 'value': expected, 'source_instruction_sha256': sha(b)}
    def literal(va, expected):
        if take(va, len(expected) + 1) != expected.encode() + b'\0':
            raise ValueError('compiled literal differs')
        return {'va': va, 'literal': expected, 'source_sha256': sha(take(va,len(expected)+1))}
    ptr, count = struct.unpack_from('<II', data, pe + 12)
    string_table = ptr + 18 * count
    found = {}
    i = 0
    while i < count:
        p = ptr + 18 * i
        name = data[p:p + 8]
        if name[:4] == b'\0' * 4:
            start = string_table + struct.unpack_from('<I', name, 4)[0]
            end = data.index(b'\0', start)
            name = data[start:end]
        name = name.rstrip(b'\0').decode('ascii', 'strict')
        value, section = struct.unpack_from('<Ih', data, p + 8)
        if name in expected_symbols and section > 0:
            address = base + inv['sections'][section - 1]['rva'] + value
            if address != expected_symbols[name] or name in found:
                raise ValueError('original COFF symbol differs')
            found[name] = address
        i += 1 + data[p + 17]
    if found != expected_symbols:
        raise ValueError('original selected COFF symbols missing')
    return base, take, imm, literal, found


def compiled_evidence(data):
    base, take, imm, literal, found = original_image(data, SYMBOLS)
    calls = []
    for va, target, purpose in CALLS:
        b = take(va, 5)
        if b[0] != 0xe8 or va + 5 + struct.unpack_from('<i', b, 1)[0] != target:
            raise ValueError('compiled call target differs')
        calls.append({'va': va, 'target_va': target, 'purpose': purpose, 'instruction_sha256': sha(b)})
    # Original relative jump after the successful confirmation callback.
    b = take(0x49964b, 5)
    if b[0] != 0xe9 or 0x499650 + struct.unpack_from('<i',b,1)[0] != 0x498820:
        raise ValueError('success path does not tail-call activation display')
    return {'bytes': len(data), 'sha256': sha(data), 'base': base, 'COFF_symbols': found,
            'call_witnesses': calls,
            'immediates': {'GetItem_reader_capacity': imm(0x4994b3,0xba,128),
                           'window_UsedCheck_mode': imm(0x49961e,0xbf,1),
                           'first_inventory_slot': imm(0x498fd5,0xbe,5)},
            'literals': [literal(0x59c6b5,'GetItem'), literal(0x59c631,','), literal(0x59c68f,'&'), literal(0x59c68d,'*'),literal(0x59c6e9,'NOITEM')],
            'code_windows': [{'first_VA':a,'end_VA_exclusive':b,'sha256':sha(take(a,b-a))} for a,b in SPANS],
            'manual_objdump_dataflow': {'talk_UsedCheck_mode':0, 'confirmation_mode':1,
              'confirmation_distance_max':2,'confirmation_sequence_literal':230,'confirmation_selection_literal':4,
              'GetItem_copy_capacity':128,'ASCII_max_copied_bytes':127,
              'GetArgStr_failure_returns':0,'missing_GetItem_after_successful_GetArgStr_returns':1,
              'check_and_delete_inventory_slot_domain':[5,19],
              'GetItem_role':'ACTIVATION_REQUIREMENT_AND_CONDITIONAL_CONSUMPTION_NOT_REWARD',
              'inventory_consumption_reaches_CHAR_DelItem':True,
              'confirmation_success_reaches_activation_state_writes':True,
              'original_program_executed':False}}


def derive(exe, npc_zip):
    binary = compiled_evidence(exe.read_bytes())
    _, members = verified_members(npc_zip, read_json(MANIFEST))
    g5, w23 = read_json(G5), read_json(W23)
    files23 = {f[0]:f for f in w23['files']}
    rows = []
    for ref in g5['original_CREATE_refs_and_derived_numeric_fields']:
        if ref.get('source_function') != 'npcgen_savepoint':
            continue
        path = ref['source_parameter_path']
        data = members[path]
        if sha(data) != ref['source_parameter_sha256']:
            raise ValueError('SavePoint original source differs')
        fields = [(n,l.split(b':',1)[1].decode('ascii')) for n,l in enumerate(data.splitlines(),1) if l.startswith(b'GetItem:')]
        if len(fields) > 1:
            raise ValueError('multiple source GetItem fields need separate qualification')
        row = {'path':path,'source_bytes':len(data),'source_sha256':sha(data),
               'source_CREATE':{k:ref[k] for k in ['create_path','create_ordinal','create_block_sha256','floorid','graphicname']},
               'source_ID':ref['source_fields']['source_save_ID_number'],
               'source_Born':ref['source_fields']['source_Born_triplet'],
               'NOITEM_literal_in_source_file':b'NOITEM' in data,'GetItem':None}
        if fields:
            line, value = fields[0]
            op, = [o for o in files23[path][6] if o[0]==line and o[1]=='GetItem']
            if op[2]!=value or op[3]!=sha(data.splitlines()[line-1]):
                raise ValueError('WORLD23 original field mismatch')
            copied = ascii_copy_projection(value)
            cut = len(copied) < len(value)
            row['GetItem'] = {'physical_line':line,'line_sha256':op[3],'raw_literal':value,
                             'raw_ASCII_bytes':len(value),'raw_comma_slots':len(value.split(',')),
                             'conditional_ASCII_copy':copied,'copied_ASCII_bytes':len(copied),
                             'copy_truncates':cut,'projected_comma_positions_not_validated_choices':len(copied.split(',')),
                             'cut_tail_fragment':copied.split(',')[-1] if cut else None}
        rows.append(row)
    inputs = [MANIFEST, G5, W23, W18]
    return {'schema':'stoneage.world24.compiled_savepoint_item_role_and_copy_bound.r1',
            'source_scope':'PRESERVED_COMMUNITY_MIXED25_SAME_ARCHIVE_STATIC_CODE_AND_PARAMETERS_NOT_AUTHENTICATED_OFFICIAL_DEPLOYMENT',
            'source_original_parent_RAR_reread':False,
            'published_input_git_blobs':{n:hashlib.sha1(b'blob '+str((RECO/n).stat().st_size).encode()+b'\0'+(RECO/n).read_bytes()).hexdigest() for n in inputs},
            'compiled_server':binary,'source_SavePoint_rows':rows,
            'counts':{'SavePoint_source_references':len(rows),'GetItem_fields':sum(r['GetItem'] is not None for r in rows),
                      'missing_GetItem_fields':sum(r['GetItem'] is None for r in rows),
                      'raw_comma_slots':sum(r['GetItem']['raw_comma_slots'] for r in rows if r['GetItem']),
                      'ASCII_copy_truncated_fields':sum(r['GetItem']['copy_truncates'] for r in rows if r['GetItem']),
                      'conditional_copied_comma_positions':sum(r['GetItem']['projected_comma_positions_not_validated_choices'] for r in rows if r['GetItem'])},
            'limits':{'actual_GetArgStr_load_observed':False,'original_inventory_or_activation_executed':False,
                      'all_raw_source_options_fit_compiled_reader':False,'post_copy_fragments_proven_intended_requirements':False,
                      'same_archive_equals_same_historical_deployment':False,'official_TW1_JSS1999_CN182_rule_proven':False,
                      'Quiz_GetItem_semantics_proven_by_SavePoint':False,'overall_percent':None},
            'next':'WORLD25: finite original Quiz item-role evidence; no full parser/server infrastructure'}, members


def private_html(report, members):
    sections=[]
    for r in report['source_SavePoint_rows']:
        g=r['GetItem']
        content='<p>未保存GetItem字段；按已核编译路径，前提GetArgStr成功时，此字段缺省返回1。未执行存点。</p>' if g is None else '<p>原字段：</p><pre>'+html.escape(g['raw_literal'])+'</pre><p>条件性ASCII读取投影（最多127字节）：</p><pre>'+html.escape(g['conditional_ASCII_copy'])+'</pre><p>截断：'+str(g['copy_truncates'])+'；此处位置数不是可运行的有效选项数。</p>'
        sections.append('<article><h2>'+html.escape(r['path'])+'</h2><p>原存点ID '+str(r['source_ID'])+' / 地图 '+str(r['source_CREATE']['floorid'])+'</p>'+content+'<details><summary>原参数全文（私人资料）</summary><pre>'+html.escape(members[r['path']].decode('cp950','replace'))+'</pre></details></article>')
    return '<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>WORLD24 原存点物品条件</title><style>body{max-width:1000px;margin:32px auto;padding:0 24px;background:#f5f1e8;color:#202a32;font:16px/1.65 system-ui}article{background:white;margin:20px 0;padding:20px;border-radius:8px}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:14px/1.6 monospace}h2{font-size:19px}</style><h1>WORLD24 · 原存点物品条件</h1><p>同保存社区混合2.5编译服务端：SavePoint的GetItem是检查和确认后消耗的条件，不是给玩家奖励。21份原字段中7份超过127字节；下面对照原文与固定容量的条件性读取投影。没有运行原程序、实际库存、存点或浏览器。不能视为早期官方规则，也不能将截断尾片段猜成有意设计的新条件。</p>'+''.join(sections)+'</html>'


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--exe',type=Path,required=True);p.add_argument('--npc-zip',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);p.add_argument('--private-html',type=Path)
    a=p.parse_args();report,members=derive(a.exe,a.npc_zip)
    a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if a.private_html:a.private_html.write_text(private_html(report,members),encoding='utf-8')
    print(json.dumps(report['counts']))


if __name__=='__main__':main()
