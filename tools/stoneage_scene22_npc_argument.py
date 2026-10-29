"""One source-pinned NPC -> template -> argument file; private text stays private.

This recovers a static content input, not an original server execution. The
public report contains hashes/structure and editorial paraphrases only.
"""
from __future__ import annotations
import argparse
import hashlib
import html
import json
from pathlib import Path
import struct
import zlib
from tools.stoneage_scene16_nearby_npc import (
    parse_blocks, inside_target, probe, SOURCE_SHA256, TEMPLATE_SHA256, check,
)

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'research/recovered/STONEAGE-SCENE22-NPC-ARGUMENT-R1.json'
ARCHIVE_SIZE = 361255180
ARCHIVE_SHA = 'd71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5'
MESSAGE_PATH = 'npc/genout/msg_1000_63_103'
MESSAGE_SHA = 'd1138b040fb31d0dc85cfdf4917f1c92facc67323c3a12544a8487039d0492ca'
SCENE21_HTML_SHA = '078a0d2cb5d7af08b98d9ad8f3768303403017a82574e1f23b12e4d56a68fc0e'
PINS = {
 'npc/genout/1000npc_m.create': (4413, SOURCE_SHA256),
 'npc/genout/npcgen.template': (4950, TEMPLATE_SHA256),
 MESSAGE_PATH: (143, MESSAGE_SHA),
}
FALSE = ('original_world_entered', 'original_server_executed',
         'official_tw10_identity_authenticated', 'same_deployed_build_authenticated',
         'native_dialogue_execution_verified', 'shop_transaction_executed',
         'multiple_dialogue_branches_proven', 'raw_dialogue_published',
         'original_source_browser_verified', 'source_action_executed_this_turn')

def sha(b): return hashlib.sha256(b).hexdigest()

def byteshape(raw):
    text = raw.decode('cp950', errors='strict')
    check(text.encode('cp950') == raw, 'CP950 must roundtrip original bytes')
    check(raw.decode('big5') == text, 'Big5 and CP950 must agree for this member')
    return dict(bytes=len(raw), sha256=sha(raw), LF_count=raw.count(b'\n'),
                CR_count=raw.count(b'\r'), ASCII_comma_count=raw.count(b','),
                pipe_count=raw.count(b'|'), decoded_codepoints=len(text),
                CP950_roundtrip=True, Big5_decode_equal=True,
                decoded_UTF8_sha256=sha(text.encode()),
                source_sentence_stop_count=text.count('。'))

def archive_witness(raw, members):
    """Independent RAR4 header/CRC parsing. Does not decompress member data."""
    check((len(raw), sha(raw)) == (ARCHIVE_SIZE, ARCHIVE_SHA), 'parent archive pin')
    check(raw[:7] == b'Rar!\x1a\x07\x00', 'RAR4 header')
    offset=7; found=[]; total_files=0
    while offset < len(raw):
        check(offset+7 <= len(raw), 'short RAR header')
        crc, kind, flags, size = struct.unpack_from('<HBHH', raw, offset)
        check(size >= 7 and offset+size <= len(raw), 'RAR header bounds')
        header=raw[offset:offset+size]
        check(zlib.crc32(header[2:]) & 0xffff == crc, 'RAR header CRC')
        extra=struct.unpack_from('<I',header,7)[0] if flags&0x8000 else 0
        if kind == 0x74:
            total_files+=1
            check(len(header)>=32, 'short RAR file header')
            packed, unpacked, host, data_crc, mtime, ver, method, nlen, attr = struct.unpack_from('<IIBIIBBHI',header,7)
            check(not flags&0x100, 'large file flag needs separate parser')
            name=header[32:32+nlen].split(b'\0',1)[0].replace(b'\\',b'/')
            for rel, (length,digest) in PINS.items():
                if not name.endswith(b'/'+rel.encode()): continue
                check(not flags & (1|2|4|16), 'split/encrypted/solid source refused')
                check((unpacked,len(members[rel]),sha(members[rel]))==(length,length,digest), 'member content pin')
                check(zlib.crc32(members[rel])&0xffffffff==data_crc, 'raw member CRC')
                check(offset+size+packed <= len(raw), 'packed payload bounds')
                found.append(dict(path=rel,header_offset=offset,header_bytes=size,
                    packed_bytes=packed,unpacked_bytes=unpacked,crc32=data_crc,
                    header_sha256=sha(header),packed_sha256=sha(raw[offset+size:offset+size+packed]),
                    sha256=digest))
            extra=packed
        offset+=size+extra
    check(offset==len(raw), 'RAR physical end')
    check(len(found)==3 and {x['path'] for x in found}==set(PINS), 'unique exact three original members')
    return dict(parent_bytes=len(raw),parent_sha256=sha(raw),
                all_file_headers_scanned=total_files,all_header_CRCs_verified=True,
                member_CRCs_and_R18_SHA_verified=True,three_members=found,
                decompressor='system libarchive via ctypes',
                second_decompressor_executed=False,
                header_parser_is_not_second_decompressor=True)

def source_report(create, template, message, archive):
    probe(create,template)  # Independently enforces the established SCENE16 source pins.
    members=dict(zip(PINS,(create,template,message)))
    inventory=json.loads((ROOT/'research/recovered/STONEAGE-MIXED25-SERVER-FULL-SOURCE-R18.json').read_bytes())
    for path,(size,digest) in PINS.items():
        rows=[r for r in inventory['all_server_occurrences'] if r['path']==path]
        check(len(rows)==1 and (rows[0]['size'],rows[0]['sha256'])==(size,digest), 'exact R18 inventory row')
    candidates=[b for b in parse_blocks(create,b'NPCCREATE') if inside_target(b['fields'])]
    check(len(candidates)==1, 'unique NPC at exact coordinate')
    block=candidates[0];f=block['fields'];token,sep,argument=f['enemy'].partition(b'|')
    check(token==b'npcgen_man' and sep==b'|' and argument==b'file:genout/msg_1000_63_103', 'exact source argument, not a guessed filename')
    templates=[b for b in parse_blocks(template,b'NPCTEMPLATE') if b['fields'].get('templatename')==token]
    check(len(templates)==1 and templates[0]['fields']['functionset']==b'TownPeople','exact template function')
    shape=byteshape(message)
    check((len(message),sha(message))==PINS[MESSAGE_PATH], 'exact message pin')
    r=dict(schema='stoneage.scene22.single_NPC_argument.r1',
      source_scope='LATER_RECOVERED_MIXED_COMMUNITY25_STATIC_CONTENT_NOT_OFFICIAL_TW10',
      source_status='THREE_ORIGINAL_MEMBERS_FULL_SHA_STATIC_LINK_VERIFIED',
      custody=archive_witness(archive,members),
      source_inputs=[dict(path=p,bytes=n,sha256=h) for p,(n,h) in PINS.items()],
      target=dict(floor=1000,xy=[63,103],graphic=16048,direction_raw=4,
        create_block_ordinal=block['ordinal'],create_block_byte_range=[block['byte_start'],block['byte_end']],
        create_block_sha256=block['block_sha256'],name=byteshape(f['name']),
        enemy_bytes=len(f['enemy']),enemy_sha256=sha(f['enemy']),
        argument_bytes=len(argument),argument_sha256=sha(argument),
        template_token=token.decode(),functionset='TownPeople',
        template_block_sha256=templates[0]['block_sha256'],exact_file_reference=MESSAGE_PATH),
      message=shape,
      interpretation=dict(static_argument_has_ASCII_comma=False,
        descendant_comma_split_candidate_count=1,
        descendant_rule_is_same_server_certification=False,
        original_message_observation='ONE_LINE_NOVICE_INFORMATION_AND_SHOP_SPEECH_HINT',
        editorial_simplified_paraphrases=[
          '与村民交谈可收集信息。','同一位村民也可能提供不同信息。',
          '提示在店内用购买口令交易。','提示在店内用出售口令交易。'],
        hint_is_not_transaction_runtime_proof=True,
        all_other_NPC_messages_exhausted=False),
      original_source_bytes_verified_locally=True,
      source_action_run_id=None,overall_completion_percent=None,
      **{k:False for k in FALSE})
    validate(r)
    return r

def validate(r):
    check(r['schema']=='stoneage.scene22.single_NPC_argument.r1','schema')
    for key in FALSE:check(r[key] is False, 'evidence promotion: '+key)
    check(r['source_action_run_id'] is None and r['overall_completion_percent'] is None,'no invented source action or completion')
    check(r['source_scope']=='LATER_RECOVERED_MIXED_COMMUNITY25_STATIC_CONTENT_NOT_OFFICIAL_TW10','source scope')
    check(r['original_source_bytes_verified_locally'] is True,'actual local source required')
    check(r['source_status']=='THREE_ORIGINAL_MEMBERS_FULL_SHA_STATIC_LINK_VERIFIED','source status')
    c=r['custody'];check((c['parent_bytes'],c['parent_sha256'])==(ARCHIVE_SIZE,ARCHIVE_SHA),'parent')
    check(c['all_file_headers_scanned']==7952 and c['all_header_CRCs_verified'] is True,'complete RAR header walk')
    check(c['member_CRCs_and_R18_SHA_verified'] is True and c['second_decompressor_executed'] is False and c['header_parser_is_not_second_decompressor'] is True,'extraction witness limits')
    expected={(p,n,h) for p,(n,h) in PINS.items()}
    check(len(r['source_inputs'])==3 and {(x['path'],x['bytes'],x['sha256']) for x in r['source_inputs']}==expected,'three source pins')
    check(len(c['three_members'])==3 and {(x['path'],x['unpacked_bytes'],x['sha256']) for x in c['three_members']}==expected,'three archive entries')
    t=r['target'];check((t['floor'],t['xy'],t['graphic'],t['direction_raw'])==(1000,[63,103],16048,4),'exact original target')
    check(t['template_token']=='npcgen_man' and t['functionset']=='TownPeople' and t['exact_file_reference']==MESSAGE_PATH,'exact link')
    check(t['create_block_sha256']=='bbc86e2ab64fa20e8f6702ee11e97c9ff659041c62fcf257bb8d16b2f06a4ce7' and t['create_block_byte_range']==[287,450],'source block')
    check(t['enemy_sha256']=='54d456c0a574c91f617ea2f196478a8b7694ae7cff01bc36dc57ee7eb2e0ed10','enemy fingerprint')
    check(t['template_block_sha256']=='5f24ae6f815471af9439ed4b824ae494006a8ba6fb7e4bac43b44b8ae5a89b29','template source block')
    check((t['name']['bytes'],t['name']['sha256'])==(8,'b66523220d17805c9e6b91cff10209eef1b1a4161fa2c3c17c09c6efa7a89959'),'name fingerprint')
    m=r['message'];check((m['bytes'],m['sha256'],m['LF_count'],m['CR_count'],m['ASCII_comma_count'],m['pipe_count'],m['decoded_codepoints'],m['source_sentence_stop_count'])==(143,MESSAGE_SHA,1,0,0,0,72,4),'message shape')
    check(m['CP950_roundtrip'] is True and m['Big5_decode_equal'] is True and m['decoded_UTF8_sha256']=='2309fb2a0a8fd2c0484a6964a8dc8224d71f082ad041cea0abbbdca4d3226ff0','decode witness')
    i=r['interpretation'];check(i['descendant_comma_split_candidate_count']==1 and i['static_argument_has_ASCII_comma'] is False,'one candidate, not prose-implied branches')
    check(i['hint_is_not_transaction_runtime_proof'] is True and i['descendant_rule_is_same_server_certification'] is False and i['all_other_NPC_messages_exhausted'] is False,'bounded interpretation')
    return dict(source_status=r['source_status'],target=[1000,63,103],static_message_bytes=143,native_dialogue_execution_verified=False)

def private_html(base,create,message):
    check(sha(base.encode())==SCENE21_HTML_SHA, 'exact prior observer required')
    block=next(b for b in parse_blocks(create,b'NPCCREATE') if inside_target(b['fields']))
    check(sha(create)==SOURCE_SHA256 and sha(message)==MESSAGE_SHA,'private original content pins')
    return append_reader(base,block['fields']['name'].decode('cp950'),message.decode('cp950'))

def append_reader(base,name,text):
    """Escaped text rendering also used by explicitly synthetic UI fixtures."""
    name=html.escape(name);text=html.escape(text)
    panel='<section class="panel" id="scene22"><h2>配置点原对白文件｜离线查阅</h2><p>同保存载体的三份原文件完整SHA已核；这是静态内容输入，不是原服对话执行。</p><button id="readArgument">查看该NPC原对白文件</button><div id="argumentText" hidden><h3>'+name+'</h3><pre id="originalArgument">'+text+'</pre><p>简体释义：交谈可收集信息；同一人可能给出不同消息；店内可使用买入或卖出口令。原文件本身只有一行，没有ASCII逗号分隔的多个候选。提示语不证明交易已执行。</p></div></section>'
    # Content is text-escaped and uses no event attributes or HTML from source.
    check(base.count('</main>')==1 and base.count('</html>')==1,'observer structure')
    base=base.replace('</main>',panel+'</main>')
    base=base.replace('姓名、对白、碰撞、原生遮挡及官方同服身份未认证。','本配置点姓名和对白文件已取得；原对白执行、碰撞、原生遮挡及官方同服身份未认证。')
    return base.replace('</html>',"<script>document.getElementById('readArgument').addEventListener('click',()=>{document.getElementById('argumentText').hidden=false;document.getElementById('focusNpc').click()});</script></html>")

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--private-source',type=Path);p.add_argument('--archive',type=Path);p.add_argument('--report',type=Path);p.add_argument('--base-html',type=Path);p.add_argument('--private-html',type=Path);a=p.parse_args()
    if not a.private_source:
        check(not any((a.archive,a.report,a.base_html,a.private_html)), 'private inputs required')
        print(json.dumps(validate(json.loads(REPORT.read_bytes())),sort_keys=True));return
    check(a.archive and a.report,'private archive and output report required')
    create=(a.private_source/'1000npc_m.create').read_bytes();template=(a.private_source/'npcgen.template').read_bytes();message=(a.private_source/'msg_1000_63_103').read_bytes()
    r=source_report(create,template,message,a.archive.read_bytes());a.report.write_text(json.dumps(r,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
    if a.private_html:
        check(a.base_html is not None,'prior exact observer needed')
        a.private_html.write_text(private_html(a.base_html.read_text(),create,message))
    print(json.dumps(validate(r),sort_keys=True))
if __name__=='__main__':main()
