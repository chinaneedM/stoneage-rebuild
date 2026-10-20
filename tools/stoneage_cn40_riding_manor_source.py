"""Preserve two malformed source bytes while replaying a 4.0-labelled portal table."""
import argparse
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import urllib.request
from tools.stoneage_jp2008_shadow_release import compact,require

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'research/recovered/STONEAGE-CN40-RIDING-CERTIFICATE-MANOR-SOURCE-R1.json'
URLS=('https://games.sina.com.cn/zhuanqu/stoneage3/stoneage4_3.shtml',
 'https://web.archive.org/web/20021201125523id_/http://games.sina.com.cn:80/zhuanqu/stoneage3/stoneage4_3.shtml')


def decode_preserving_faults(b):
    parts=[];issues=[];offset=0
    while offset<len(b):
        try:parts.append(b[offset:].decode('gb18030'));break
        except UnicodeDecodeError as e:
            parts.append(b[offset:offset+e.start].decode('gb18030'));bad=b[offset+e.start:offset+e.end]
            issues.append(dict(offset=offset+e.start,hex=bad.hex()));parts.append(''.join(chr(92)+'x%02x'%x for x in bad));offset+=e.end
    require(len(issues)==2 and all(x['hex']=='b1' for x in issues),'Unexpected source encoding fault; no silent replacement')
    return ''.join(parts),issues


class Cells(HTMLParser):
    def __init__(self):super().__init__();self.rows=[];self.row=None;self.parts=None
    def handle_starttag(self,t,a):
        if t=='tr':self.row=[]
        if t=='td':self.parts=[]
        if t=='br' and self.parts is not None:self.parts.append('\x1f')
    def handle_data(self,d):
        if self.parts is not None:self.parts.append(d)
    def handle_endtag(self,t):
        if t=='td' and self.parts is not None:
            self.row.append([re.sub(r'\s+','',x) for x in ''.join(self.parts).split('\x1f')]);self.parts=None
        if t=='tr' and self.row is not None:self.rows.append(self.row);self.row=None


def extract(b):
    html,issues=decode_preserving_faults(b);text=compact(html)
    require('石器时代4.0新系统' in text,'4.0 content label missing')
    require(text.count('新骑宠规则')==text.count('新经济系统')==1,'Ambiguous rule boundaries')
    core=text.split('新骑宠规则')[1].split('新经济系统')[0]
    for clause in ('每个人物依旧可以骑老虎和雷龙','一旦使用过骑宠证明书之后，将永远可骑',
                  '每人最多可骑目前开放之十二种宠','骑宠证明书除族长可制作之外，长老亦可',
                  '帖拉所伊朵（机暴）之骑乘条件为五转人物，且寻找流浪骑宠师习得技能',
                  '从原先的前十大家族，改成前二十大','其它人须有家族邀请函才能进去',
                  '不是直接贩售，NPC会要求玩家给予材料，再帮玩家合成'):
        require(clause in core,'Material riding/manor clause missing: '+clause)
    # The original table has a header row and ONE data row of five cells;
    # each cell contains nine line-separated entries, including leading blanks.
    pos=html.index('庄园名称');start=html.rfind('<table',0,pos);end=html.index('</table>',pos)+8
    p=Cells();p.feed(html[start:end]);require(len(p.rows)==2,'Unexpected source table row structure')
    require(p.rows[0]==[[x] for x in ['庄园名称','地理地址','骑宠','开放式商店','封闭式商店']],'Wrong table headers')
    cols=p.rows[1];require(len(cols)==5,'Five source columns required')
    if len(cols[1])==10 and cols[1][-1]=='':cols[1].pop()  # actual trailing BR in geography cell
    require([len(c) for c in cols]==[9]*5,'Nine aligned entries per column required; preserve blanks')
    rows=[dict(position=i+1,manor=cols[0][i],geography=cols[1][i],mount_label_escaped=cols[2][i],
               mount_main_name=cols[2][i].split('(')[0],open_shop_as_written=cols[3][i],
               closed_shop_as_written=cols[4][i] or None,
               closed_shop_status='UNSTATED_BLANK' if cols[4][i]=='' else 'SOURCE_LABEL_NOT_STOCK_OR_SERVICE_ID') for i in range(9)]
    return dict(core_sha256=sha256(core.encode()).hexdigest(),core_utf8_bytes=len(core.encode()),encoding_issues=issues,
        facts=dict(character_tiger_and_thunder_mounts_retained=True,certificate_use_permanent_riding_claim=True,
        certificate_manufacturers=['族长','长老'],advertised_mount_type_cap=12,manor_rows=9,
        special_mount_as_written='帖拉所伊朵（机暴）',rebirth_condition_as_written='五转人物',teacher_as_written='流浪骑宠师',
        challenge_family_rank_change=[10,20],closed_shop_access='OWN_FAMILY_OR_OTHER_WITH_INVITATION',closed_shop_fulfilment='MATERIAL_FOR_CRAFT_NOT_DIRECT_SALE'),
        manor_rows=rows,table_shape=dict(html_rows=2,columns=5,entries_per_column=[9]*5))


def validate(r):
    require(r['schema']=='stoneage.cn40_riding_certificate_manor.source.r1','Wrong schema')
    require([s['http']['url'] for s in r['inputs']]==list(URLS),'Finite source set changed')
    require(r['authority']=='PORTAL_40_LABELLED_SYSTEM_GUIDE_OPERATOR_AUTHOR_UNVERIFIED','Portal promoted to operator author')
    a,b=[s['extracted'] for s in r['inputs']]
    require(a['core_sha256']==b['core_sha256'] and a['facts']==b['facts'] and a['manor_rows']==b['manor_rows'],'Source representations differ')
    require(len(r['records'])==13,'Nine table records plus four source contracts required')
    required={'record_id','entity_type','version_profile','source_refs','verification_status','rights_status','record_revision'}
    for row in r['records']:
        require(required<=row.keys() and row['game_ids'] is None,'Contract/original IDs changed')
        require(row['verification_status']=='PORTAL_SOURCE_REPORTED_NOT_RUNTIME' and row['rights_status']=='RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED','Authority/runtime/rights promotion')
    require([x['source_row'] for x in r['records'][:9]]==a['manor_rows'],'Source table detached')
    require(r['records'][9]['rebirth_predicate'] is None and r['records'][9]['coordinates'] is None,'Teacher threshold/coordinates invented')
    require(r['records'][10]['survives_rebirth'] is None and r['records'][10]['consumed_on_use'] is None,'Certificate persistence/consumption invented')
    require(r['records'][11]['stock_quantities'] is None and r['records'][11]['prices'] is None,'Shop inventory invented')
    require(r['boundaries']==dict(original_operator_authorship_verified=False,original_server_execution_verified=False,
        exact_client_build=None,publication_date=None,broken_aliases_repaired=False,twelve_mounts_means_twelve_manors=False,
        blank_shop_means_no_shop=False,material_level_11_means_quantity_11=False,permanent_claim_proves_rebirth_or_account_scope=False,
        old_cn20_compatibility_or_combat_formula_overwritten=False,raw_html_or_assets_committed=False,
        tw10_or_jss1999_backfill=False,stage_a='7_PARTIAL_2_OPEN',stage_b_and_wiki='GATED',r79='PAUSED_NON_BLOCKING'),'Boundary changed')
    require(r['next']=='OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-29','Portfolio return required')


def replay(r,payloads):
    validate(r);require(len(payloads)==2,'Exactly current portal HTML and 2002 capture required')
    got=[extract(b) for b in payloads];require(got==[s['extracted'] for s in r['inputs']],'Source extraction changed')
    h=r['inputs'][1]['http'];require(len(payloads[1])==h['bytes'] and sha256(payloads[1]).hexdigest()==h['sha256'],'Historical byte pin changed')
    return dict(schema='stoneage.cn40_riding_certificate_manor.replay.r1',inputs=[dict(source_id=s['id'],bytes=len(b),sha256=sha256(b).hexdigest()) for s,b in zip(r['inputs'],payloads)],extracted=got,malformed_bytes_preserved=True,historical_capture_timestamp='20021201125523',original_server_or_operator_author_verified=False,raw_html_or_images_in_output=False)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--fetch',action='store_true');p.add_argument('--source-dir',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();require(a.fetch!=bool(a.source_dir),'Choose fixed fetch or transient files');payloads=[]
    for u,n in zip(URLS,('cn40.html','cn40-era.html')):
        if a.fetch:
            with urllib.request.urlopen(u,timeout=45) as response:
                require(response.status==200 and response.url==u,'Unexpected HTTP/redirect');b=response.read(2_000_001);require(len(b)<=2_000_000,'Oversized source')
        else:b=(a.source_dir/n).read_bytes()
        payloads.append(b)
    result=replay(json.loads(REPORT.read_text()),payloads);a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('SOURCE_RULESETS_VERIFIED=1 MANOR_TABLE_ROWS=9 MALFORMED_BYTES_PRESERVED_PER_SOURCE=2 HISTORICAL_HTML_VERIFIED=1 ORIGINAL_SERVER_EXECUTIONS=0')


if __name__=='__main__':main()
