"""Bounded rotation: stop an unqualified encounter card, read one static NPC.

Private text, source files and reader stay outside Git. Public CI sees only
derived fingerprints and synthetic text; no historical program is executed.
"""
import argparse
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import subprocess
import zipfile
from tools.stoneage_scene16_nearby_npc import parse_blocks
from tools.stoneage_scene33_source_pair import rar_receipt,ARCHIVE_SHA

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'research/recovered/STONEAGE-SCENE35-CONTENT-ROTATION-R1.json'
AUDIT=ROOT/'research/recovered/STONEAGE-SCENE35-PRIVATE-CARD-AUDIT-R1.json'
AUDIT_FROZEN='94701288249a0102e63a04f5430d6c9a0e4542fc576d575de0a8c4e5a1a257c9'
CREATE='npc/genout/1000npc_m.create'
TEMPLATE='npc/genout/npcgen.template'
MESSAGE='npc/genout/msg_1000_128_36'
NPC_PINS={
 CREATE:(4413,'c9b000a836b0aae3d88358097039f1beea020d92ba84f6ccc338bb54bc478240'),
 TEMPLATE:(4950,'0c5a58d5e31cafd3b58ccc1fa88fee7d1f95d12c0b87b04db9f06fea3b2a4df3'),
 MESSAGE:(76,'147fd7ad70d8fcc81a1cf3b525a3b5a248f1f1eabdcd54725f361a94ad42e46e'),
}
STOP_PINS={
 'encount.txt':(43420,'70bbd997d98508a0587df183b5bdd48222ff42db91bf21bea632e0ed6f2fea87'),
 'group1.txt':(70176,'4a02f2a3fa3d2dcf5589d8a2a560313c35d5a0a7e5e0589cc8df5f7df159ea8f'),
 'enemy.txt':(222463,'cc7418d3b6726f1c458fef9e44a24696d05f076b67c62a56ed2293e26ae63bb6'),
 'enemybase.txt':(147750,'1be7d5226798f7abaabe1f1e74aa1533fcd10e3eaf43f6497d63afa91df3e8b7'),
}
SETUP=(9715,'b4936c103efb7b3cad359e5c85c7965187306883a68c0be712ece6c374e3b12d')
FALSE=('original_client_executed','original_server_executed','original_world_entered',
 'native_dialogue_execution_verified','runtime_branch_selection_verified',
 'official_TW10_identity_authenticated','same_deployed_build_authenticated',
 'island_identity_or_route_authenticated','quest_classification_authenticated',
 'quest_rewards_or_flags_authenticated','encounter_card_built',
 'original_table_field_layout_authenticated','source_text_published_in_Git',
 'original_source_browser_verified')
FROZEN='fc4fd99665027ca36ad67f755f40a2b386a55db87cf7d8a970093c5bd7c17a8c'

def need(ok,message):
    if not ok:raise ValueError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(r):return json.dumps(r,sort_keys=True,separators=(',',':')).encode()
def pin(raw,expected):need((len(raw),sha(raw))==expected,'exact original input identity')

def text_shape(raw):
    text=raw.decode('cp950')
    need(text.encode('cp950')==raw and raw.decode('big5')==text,'CP950/Big5 exact source decoding')
    return dict(bytes=len(raw),sha256=sha(raw),decoded_codepoints=len(text),
        decoded_UTF8_sha256=sha(text.encode()),LF_count=raw.count(b'\n'),
        CR_count=raw.count(b'\r'),ASCII_comma_count=raw.count(b','),
        CP950_roundtrip=True,Big5_same=True)

def target(create,template,message):
    pin(create,NPC_PINS[CREATE]);pin(template,NPC_PINS[TEMPLATE]);pin(message,NPC_PINS[MESSAGE])
    blocks=parse_blocks(create,b'NPCCREATE')
    matches=[b for b in blocks if b['fields'].get('floorid')==b'1000' and b['fields'].get('borncorner')==b'128,36,128,36']
    need(len(matches)==1,'one exact original NPC point')
    block=matches[0];f=block['fields'];token,sep,arg=f['enemy'].partition(b'|')
    need(token==b'npcgen_man' and sep==b'|' and arg==b'file:genout/msg_1000_128_36','exact declared argument reference')
    ts=[b for b in parse_blocks(template,b'NPCTEMPLATE')if b['fields'].get('templatename')==token]
    need(len(ts)==1 and ts[0]['fields']['functionset']==b'TownPeople','unique original named template')
    return block,ts[0]

def reader(name,text):
    parts=text.rstrip('\n').split(',')
    cards=''.join('<article><span class="tag">原ASCII逗号分段 '+str(i+1)+'</span><p>'+html.escape(p)+'</p></article>'for i,p in enumerate(parts))
    return '''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>海边的一句问话｜原保存内容卡</title><style>
body{margin:0;background:#f3efe5;color:#243d45;font:17px/1.8 system-ui,sans-serif}
main{max-width:850px;margin:45px auto;padding:0 25px}h1{font-size:34px;line-height:1.35;margin:8px 0 18px}
.eyebrow,.tag{font-size:13px;color:#4e717a;letter-spacing:.06em}.lead{font-size:19px}
.notice{border-left:4px solid #718d86;padding:12px 20px;background:#e6ebe3}
article{background:#fffdf8;border:1px solid #d9d8cc;border-radius:14px;padding:22px 25px;margin:20px 0}
article p{font-size:21px;margin:10px 0;white-space:pre-wrap}pre{white-space:pre-wrap;font:16px/1.9 system-ui}
details{padding:18px 0;border-top:1px solid #c8d1ca}small{color:#617078}a{color:#335f6b}
</style><main><div class="eyebrow">保存版石器内容 · SCENE35 · 静态原文</div>
<h1>海边的一句问话</h1><p class="lead">原配置姓名：<strong id="sourceName">'''+html.escape(name)+'''</strong></p>
<p class="notice">来自社区混合保存包。此页供离线查阅；未运行原客户端或服务端，也未认证早期官方版本。</p>
<h2>这份原文件写了什么</h2>'''+cards+'''
<p>简体释义：少女提到自己睡着了，并好奇对面隐约可见的岛屿上有什么。</p>
<h2>能知道与仍不知道的事</h2><p>原创建配置声明点为floor 1000 / (128,36)，精确引用这份对白文件。
图形整数16009仅为原配置值，本卡没有将它换成图片。文件里有一个ASCII逗号，所以上方分成两段方便阅读；
这不证明原游戏会分两次说、按先后说、随机说，或存在两条任务分支。</p>
<p>这段文字没有为我们认证岛名、航线、任务条件、奖励或完成标志。任务来源仍未定，不能据它创造一个任务。</p>
<details><summary>查看整份原文（保留原顺序与末尾换行）</summary><pre id="rawMessage">'''+html.escape(text)+'''</pre></details>
<details><summary>来源与本卡范围</summary><p>同一父RAR的原创建文件、模板与76字节对白均已按整SHA核对，
创建块 → npcgen_man → TownPeople → file:genout/msg_1000_128_36 为静态引用链。
完整摘要与原文件随此资料包保存；本卡不是原对话窗口、可玩场景或历史世界运行。</p></details>
<small>当前仍在资料恢复阶段。所有控件与排版为现代查阅设计，原文保留繁体，操作说明使用简体。</small></main></html>'''

class TextAudit(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True);self.current=None;self.content={};self.external=[];self.scripts=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='script':self.scripts+=1
        if any(k in a for k in ('src','href','action')):self.external.append((tag,a))
        if a.get('id')in ('sourceName','rawMessage'):
            need(a['id']not in self.content,'duplicate source text ID')
            self.current=(tag,a['id']);self.content[a['id']]=''
    def handle_endtag(self,tag):
        if self.current and self.current[0]==tag:self.current=None
    def handle_data(self,data):
        if self.current:self.content[self.current[1]]+=data

def audit_reader(page,name,text):
    p=TextAudit();p.feed(page)
    need(p.content==dict(sourceName=name,rawMessage=text),'private reader exact original decoded text')
    need(p.scripts==0 and not p.external,'static reader has no script or external resource')
    return dict(exact_original_name_and_message_HTML_roundtrip=True,scripts=0,external_resources=0,
        original_source_browser_verified=False)

def source_probe(npc_root,stop_root,archive,out):
    need(not out.exists() and ROOT not in out.resolve().parents,'new private output outside Git')
    npc={p:(npc_root/p).read_bytes()for p in NPC_PINS}
    for p,b in npc.items():pin(b,NPC_PINS[p])
    stopped={p:(stop_root/'data'/p).read_bytes()for p in STOP_PINS}
    for p,b in stopped.items():pin(b,STOP_PINS[p])
    setup=(stop_root/'setup.cf').read_bytes();pin(setup,SETUP)
    index=json.loads((ROOT/'research/recovered/STONEAGE-MIXED25-SERVER-FULL-SOURCE-R18.json').read_bytes())
    for p,b in {**npc,**stopped}.items():
        found=[x for x in index['all_server_occurrences']if x['path']==p]
        need(len(found)==1 and (found[0]['size'],found[0]['sha256'])==(len(b),sha(b)),'exact R18 original occurrence')
    block,t=target(npc[CREATE],npc[TEMPLATE],npc[MESSAGE]);f=block['fields']
    text=npc[MESSAGE].decode('cp950');name=f['name'].decode('cp950')
    # Independent implementation of the selected bytes -> Unicode conversion.
    iconv=subprocess.run(['iconv','-f','CP950','-t','UTF-8'],input=npc[MESSAGE],capture_output=True,check=True).stdout
    need(iconv==text.encode(),'independent iconv and Python source text equal')
    members={'gmsv/data/'+p:b for p,b in {**npc,**stopped}.items()};members['gmsv/setup.cf']=setup
    raw=archive.read_bytes();w=rar_receipt(raw,members)
    stopped_rows=[dict(path=p,bytes=len(b),sha256=sha(b),comment_line_count=sum(x.lstrip().startswith(b'#')for x in b.splitlines()),
        first_nonempty_record_field_count=len(next(x for x in b.splitlines()if x.strip()).split(b',')),
        source_field_names_authenticated=False)for p,b in stopped.items()]
    need(all(x['comment_line_count']==0 for x in stopped_rows),'bounded no-comment source finding')
    message_shape=text_shape(npc[MESSAGE]);segments=npc[MESSAGE].rstrip(b'\n').split(b',')
    report=dict(schema='stoneage.scene35.content_rotation.r1',
        scope='MIXED_MODIFIED_COMMUNITY_STATIC_CONTENT_NOT_OFFICIAL_TW1',
        parent_archive=dict(bytes=len(raw),sha256=sha(raw)),RAR_witness=w,
        encounter_stop=dict(status='NOT_BUILT_SOURCE_FIELD_LAYOUT_UNAUTHENTICATED',
            originals=stopped_rows,existing_structural_chain_and_WORLD01_routes_already_reviewed=True,
            prior_column_labels_come_from_descendant_code=True,old_encounter_audit_rerun=False),
        NPC_inputs=[dict(path=p,bytes=len(b),sha256=sha(b))for p,b in npc.items()],
        NPC=dict(floor=1000,xy=[128,36],block_ordinal=block['ordinal'],
            block_byte_range=[block['byte_start'],block['byte_end']],block_sha256=block['block_sha256'],
            name=text_shape(f['name']),graphic_raw=int(f['graphicname']),direction_raw=int(f['dir']),
            exact_argument_file=MESSAGE,template_token='npcgen_man',functionset='TownPeople',
            template_block_sha256=t['block_sha256']),
        message=message_shape,
        literal_comma_segments=[dict(ordinal=i,bytes=len(b),sha256=sha(b))for i,b in enumerate(segments)],
        independent_iconv_UTF8_equal=True,quest_origin='ORIGIN_UNRESOLVED',new_authenticated_quests=0,
        editorial_simplified_paraphrase='少女提到自己睡着了，并好奇对面隐约可见的岛屿上有什么。',
        new_content_is_one_static_NPC_argument_not_a_new_table_or_runtime=True,
        source_action_run_id=None,overall_percent=None,**{k:False for k in FALSE})
    page=reader(name,text);report['private_reader_audit']=audit_reader(page,name,text)
    out.mkdir(mode=0o700,parents=True)
    (out/'reader.html').write_text(page,encoding='utf-8')
    for p,b in npc.items():
        dest=out/'source'/p;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
    (out/'private-source-note.json').write_text(json.dumps(dict(name=name,original_message=text,block_fields={k:v.decode('cp950')for k,v in f.items()},
        public_report=report),ensure_ascii=False,indent=2)+'\n')
    (out/'source-derived-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    package=out/'SCENE35-private-seaside-dialogue-card.zip'
    with zipfile.ZipFile(package,'w',zipfile.ZIP_DEFLATED)as z:
        for p in sorted(out.rglob('*')):
            if p.is_file() and p!=package:z.write(p,p.relative_to(out).as_posix())
    return report,package

def validate(r):
    need(r['scope']=='MIXED_MODIFIED_COMMUNITY_STATIC_CONTENT_NOT_OFFICIAL_TW1','source/version scope')
    need(r['parent_archive']==dict(bytes=361255180,sha256=ARCHIVE_SHA),'original parent identity')
    need(all(r[k]is False for k in FALSE),'static source cannot become runtime/official/quest evidence')
    need(r['encounter_stop']['status']=='NOT_BUILT_SOURCE_FIELD_LAYOUT_UNAUTHENTICATED' and r['encounter_stop']['old_encounter_audit_rerun']is False,'encounter stop retained')
    stopped=r['encounter_stop']['originals']
    need(len(stopped)==4 and {x['path']:(x['bytes'],x['sha256'])for x in stopped}==STOP_PINS,'four stopped original file identities')
    need(all(x['comment_line_count']==0 and x['source_field_names_authenticated']is False for x in stopped) and r['encounter_stop']['prior_column_labels_come_from_descendant_code']is True,'column-layout evidence not promoted')
    need({x['path']:(x['bytes'],x['sha256'])for x in r['NPC_inputs']}==NPC_PINS and len(r['NPC_inputs'])==3,'three exact NPC source identities')
    n=r['NPC'];need(n['floor']==1000 and n['xy']==[128,36] and n['exact_argument_file']==MESSAGE,'exact source-declared point/reference')
    need((n['block_ordinal'],n['block_byte_range'],n['block_sha256'],n['graphic_raw'],n['direction_raw'])==(17,[3075,3240],'87b9666c06fb4660b0634a0c5321f63a9aa0459289ff6ccbfd91578ce1f92aa7',16009,6),'exact original block and uninterpreted integers')
    need(n['template_token']=='npcgen_man' and n['functionset']=='TownPeople','unique static template')
    need(r['message']['ASCII_comma_count']==1 and len(r['literal_comma_segments'])==2 and [x['ordinal']for x in r['literal_comma_segments']]==[0,1] and [x['bytes']for x in r['literal_comma_segments']]==[22,52],'two literal comma segments retained')
    need(r['quest_origin']=='ORIGIN_UNRESOLVED' and r['new_authenticated_quests']==0,'no invented quest')
    need(r['source_action_run_id']is None and r['overall_percent']is None,'no invented source Action/progress')
    need(sha(canonical(r))==FROZEN,'frozen actual source result')
    return dict(static_NPC_arguments_observed=1,literal_comma_segments=2,encounter_card_built=False,original_world_entered=False)

def validate_audit(a,r):
    need(a['source_report_sha256']==sha(REPORT.read_bytes()) and a['canonical_source_report_sha256']==sha(canonical(r)),'private audit/source report binding')
    need(a['private_original_member_count']==3 and a['private_original_member_bytes']==9439 and a['private_package_members']==6,'bounded original card membership')
    need(a['all_ZIP_member_CRCs_and_original_SHA_verified']is True and a['private_source_card_saved']is True and a['local_identity_metadata_applied']is True,'actual card verification and save acknowledgement')
    need(a['actual_browser_execution_performed']is False and a['original_programs_executed']is False and a['raw_gameplay_content_published']is False,'private static card is not browser/game execution')
    need(a['successful_second_decompressor_executed']is False and a['RAR_header_walk_is_not_second_decompressor']is True,'single decompressor boundary')
    need(a['read_back_after_save']is False,'save acknowledgement not independent readback')
    need(sha(canonical(a))==AUDIT_FROZEN,'frozen actual private audit')
    return True

def main():
    p=argparse.ArgumentParser();p.add_argument('--npc-root',type=Path);p.add_argument('--stopped-root',type=Path);p.add_argument('--archive',type=Path);p.add_argument('--private-output',type=Path);a=p.parse_args()
    if a.npc_root:
        need(all((a.stopped_root,a.archive,a.private_output)),'explicit private original inputs and output')
        r,z=source_probe(a.npc_root,a.stopped_root,a.archive,a.private_output)
        print(json.dumps(dict(canonical_report_SHA256=sha(canonical(r)),package=str(z),package_bytes=z.stat().st_size,package_sha256=sha(z.read_bytes()))))
    else:
        r=json.loads(REPORT.read_bytes());result=validate(r)
        validate_audit(json.loads(AUDIT.read_bytes()),r);print(json.dumps(result))

if __name__=='__main__':main()
