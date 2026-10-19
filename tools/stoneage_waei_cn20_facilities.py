"""One official facilities article: documentary services, never server scripts."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
from urllib.parse import urljoin
from tools.stoneage_early_content_probe import plain, require
from tools.stoneage_wayi_newbie_riding_plan import fetch
from tools.stoneage_waei_cn20_new_pet_catalog import Images, grid_digest
from tools.stoneage_waei_cn20_new_pet_pagination import PAGES

ENTRY = PAGES[0]
ORIGINAL = 'http://www.waei.com.cn/ZHUANQU/stoneage2/sw/facility.asp'
CAPTURE = '20011204213609'
URL = 'https://web.archive.org/web/'+CAPTURE+'id_/'+ORIGINAL
SOURCE_SHA = 'e18f0bced4935358e3be28e328d50a49a6dfbb8c26476a98c211892974e7ba16'
GRID_SHA = 'c5fb28e99d47abf550ec6cdfe0860ecd44a9a3ed0411ecb293f184c4c93f6945'
REPORT = Path('research/recovered/STONEAGE-WAEI-CN20-PUBLIC-FACILITIES-R1.json')
LABELS = ['村长家','医院','武器店和防具店','道具店','宠物店','肉店','便利商店','竞技场','聊天室','道场','纪录点','长毛象快递','长毛象公车','加美航空']
# Paraphrased documentary claims, not original paragraphs or implemented rules.
CLAIMS = [
    ['四大村初生地在村长家；教学NPC提供常识与可能的任务情报。','家族申请及管理员服务设在这里；未给出具名NPC、坐标或任务脚本。'],
    ['护士为人物及宠物恢复体力、气力；页面表述玩家等级10级以下免费。','药剂师出售复活及异常恢复等药；美容师收费提高人物魅力；医师提供咨询。','未规定10级以下是否含10、宠物等级条件、收费公式或魅力增量。'],
    ['武器与防具商店有时合并，也可能只有商人；购买能力不等于满足装备等级。','页面描述宠物加工可制作部分带精灵法术的装备；未列具体库存、等级门槛或合成配方。'],
    ['出售饰品或乐器，可影响人物能力，部分附精灵法术；页面举指环与竖琴为例。','加工段与武防店段重复；两段不是两份独立来源证人。'],
    ['提供卖宠、寄宠、技能教学；页面称随身最多5宠，满额影响捕捉及任务收宠。','超级饲育员收费教学，举背水、忠犬、合成、料理；未给费用、技能完整表或服务器ID。'],
    ['战斗所得肉可以补体力，也可卖给肉店换石币；店肉可作料理原料。','未给怪物掉落率、售价或料理配方。'],
    ['萨尔吉姆村与卡鲁它那村商店偏加工材料，玛丽娜丝与加加偏料理材料；不同素材有等级区别。','店内委托可得报酬与声望，但没有具名任务ID、奖励数值或脚本。'],
    ['斗技场用于玩家对战，含售卖与护理服务；门票表述10级以下免费。','各村入口共用竞技场，原入场券用于返回原村；遗失可注销回纪录点，未给票价公式或地图ID。'],
    ['各村聊天室互通，进出需门票；深处礼堂用于婚礼。','没有票价、婚礼状态机或原服地图坐标。'],
    ['北岛百人道场描述100关、对手等级1至100，途中进道场医院视作放弃，后续从第1关再来。','南岛道场描述回答100题；未给题库、奖励、门票价格或服务器任务标志。'],
    ['文章回顾早期注销后回纪录点，另述原地注销出现后的使用方式；不能据此定补丁日期。','打飞与普通注销涉及回纪录点；可查询在线人数，登记需要肉类贡品且各点不同。'],
    ['限时运货换报酬，报酬随目的地远近；超时打折，接单押金描述为酬金十分之一。','原文营业时间写早上并括注太阳出来前，另称天黑后不能入店；保留措辞，不推精确时钟区间或调和为日出后。'],
    ['村外交通，可往邻近村、途中避敌，费用随距离；搭乘途中能跳车。','没有路线表、坐标、车费公式或跳车安全保证。'],
    ['部分村庄的较远程交通，可跨海、收费较高；部分特殊任务需搭乘抵达。','没有明确航线、村庄清单、票价或任务ID。'],
]
BOUNDARIES = {'article_is_original_server_runtime_verified':False,'same_tw10_jss_cn182_or_later_build':False,
              'every_village_has_every_facility':False,'automatic_new_game_adoption':False,
              'raw_original_html_images_or_programs_in_git':False,'stage_a':'7_PARTIAL_2_OPEN',
              'stage_b_and_wiki':'GATED','r79':'PAUSED_NON_BLOCKING'}


def parse_article(doc):
    require(re.search(r'<title>\s*石器时代2\.0\s*</title>',doc,re.I) is not None, 'Actual title differs')
    require(doc.count('公 共 设 施') == 1, 'One facilities heading required')
    section = doc.split('公 共 设 施',1)[1].split('<span class="p12b">',1)[0]
    tables = re.findall(r'<table\b[^>]*>(.*?)</table>',section,re.I|re.S)
    require(len(tables) == 1, 'One actual facilities table required')
    rows = []
    for tr in re.findall(r'<tr\b[^>]*>(.*?)</tr>',tables[0],re.I|re.S):
        cells = re.findall(r'<td\b[^>]*>(.*?)</td>',tr,re.I|re.S)
        require(len(cells) == 2, 'One image cell and one service cell required')
        parser = Images(); parser.feed(cells[0]); require(len(parser.images) == 1, 'One image reference per facility')
        attrs = parser.images[0]
        labels = re.findall(r'<b>(.*?)</b>',cells[1],re.I|re.S)
        require(len(labels) == 1, 'One facility heading required')
        rows.append([plain(labels[0]),attrs['src'],[int(attrs['width']),int(attrs['height'])],
                     sha256(plain(cells[1]).encode()).hexdigest()])
    require([r[0] for r in rows] == LABELS and grid_digest(rows) == GRID_SHA, 'Facility order, text, image association or declarations differ')
    return rows


def validate_report(o):
    require(o['source'] == {'original_url':ORIGINAL,'strict_replay_url':URL,'actual_capture':CAPTURE,
            'bytes':73356,'sha256':SOURCE_SHA,'encoding':'GB18030_STRICT','page_title':'石器时代2.0',
            'article_heading':'公 共 设 施','grid_sha256':GRID_SHA}, 'Actual facilities source identity differs')
    require(len(o['records']) == 14, 'Fourteen source facility categories required')
    rows = []
    for i,r in enumerate(o['records']):
        im = r['image_reference']
        rows.append([r['name_as_written'],im['relative_src_as_written'],im['html_declared_dimensions'],r['service_text_sha256']])
        require(r['record_id'] == f'waei-cn20:facility-web-section:{i+1:02d}' and r['name_as_written'] == LABELS[i]
                and r['source_qualified_paraphrases'] == CLAIMS[i], 'Literal category or source-qualified service/limits changed')
        require(r['source_refs'] == [{'original_url':ORIGINAL,'actual_capture':CAPTURE,'sha256':SOURCE_SHA,
                                     'table_row':i+1,'service_text_sha256':r['service_text_sha256']}], 'Exact paragraph provenance differs')
        require(im['original_url'] == urljoin(ORIGINAL,im['relative_src_as_written'])
                and im['pixels_requested'] is False and im['actual_dimensions_format_or_capture'] is None, 'Reference promoted to acquired pixels')
        require(all(r[k] is None for k in ['original_npc_ids_or_names','map_coordinates_or_server_script','prices_formulas_or_quest_rewards']),
                'Generic roles or documentary prose promoted to game master data')
        require(r['collection'] == 'tutorials', 'Facility article belongs to documentary tutorials, not new NPC/map masters')
        require(r['entity_type'] == 'OFFICIAL_WEB_FACILITY_CATEGORY_NOT_SERVER_NPC_INSTANCE'
                and r['record_revision'] == 1 and r['version_profile'] == 'CN_WAEI_2_0_LABEL_CAPTURE_20011204_NOT_EXACT_BUILD'
                and r['rights_status'] == 'RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED'
                and r['verification_status'] == 'OFFICIAL_ARTICLE_DESCRIPTION_NOT_RUNTIME_VERIFIED', 'Archive record qualification differs')
    require(grid_digest(rows) == GRID_SHA, 'Exact service paragraph hash/image declaration grid differs')
    require(o['boundaries'] == BOUNDARIES, 'Documentary boundaries promoted')
    require(o['coverage'] == {'new_original_bodies':1,'known_entry_reacquired':1,'facility_categories':14,
            'new_named_npc_instances':0,'new_images_requested':0,'unacquired_image_refs':14}, 'Coverage inflated')
    require(o['next'] == 'OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-16', 'Bounded next differs')


def build(entry, entry_final, body, final):
    require(entry_final == ENTRY['strict_replay_url'] and sha256(entry).hexdigest() == ENTRY['sha256']
            and len(entry) == ENTRY['bytes'], 'Known entry exact capture/bytes required')
    ed = entry.decode('gb18030',errors='strict')
    links = [(href,plain(label)) for href,label in re.findall(r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>',ed,re.I|re.S)
             if plain(label) == '公共设施']
    require(links == [('/ZHUANQU/stoneage2/sw/facility.asp','公共设施')], 'Authenticated sidebar label/href differs')
    require(final == URL and len(body) == 73356 and sha256(body).hexdigest() == SOURCE_SHA, 'Actual facilities body pin differs')
    rows = parse_article(body.decode('gb18030',errors='strict'))
    records = []
    for i,(label,src,dims,text_sha) in enumerate(rows):
        records.append({'record_id':f'waei-cn20:facility-web-section:{i+1:02d}','collection':'tutorials',
            'entity_type':'OFFICIAL_WEB_FACILITY_CATEGORY_NOT_SERVER_NPC_INSTANCE','record_revision':1,
            'version_profile':'CN_WAEI_2_0_LABEL_CAPTURE_20011204_NOT_EXACT_BUILD',
            'source_refs':[{'original_url':ORIGINAL,'actual_capture':CAPTURE,'sha256':SOURCE_SHA,'table_row':i+1,'service_text_sha256':text_sha}],
            'verification_status':'OFFICIAL_ARTICLE_DESCRIPTION_NOT_RUNTIME_VERIFIED',
            'rights_status':'RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED','name_as_written':label,
            'service_text_sha256':text_sha,'source_qualified_paraphrases':CLAIMS[i],
            'image_reference':{'relative_src_as_written':src,'original_url':urljoin(ORIGINAL,src),
                               'html_declared_dimensions':dims,'pixels_requested':False,'actual_dimensions_format_or_capture':None},
            'original_npc_ids_or_names':None,'map_coordinates_or_server_script':None,'prices_formulas_or_quest_rewards':None})
    o = {'schema':'stoneage.waei_cn20.public_facilities.r1','date':'2026-10-19','task':'CN20-OFFICIAL-PUBLIC-FACILITY-CONTENT-SOURCE-01',
         'source':{'original_url':ORIGINAL,'strict_replay_url':URL,'actual_capture':CAPTURE,'bytes':len(body),'sha256':SOURCE_SHA,
                   'encoding':'GB18030_STRICT','page_title':'石器时代2.0','article_heading':'公 共 设 施','grid_sha256':GRID_SHA},
         'authenticated_entry':{'original_url':ENTRY['original_url'],'actual_capture':ENTRY['actual_capture'],
                                'bytes':ENTRY['bytes'],'sha256':ENTRY['sha256'],'label':'公共设施','href':'/ZHUANQU/stoneage2/sw/facility.asp'},
         'records':records,'coverage':{'new_original_bodies':1,'known_entry_reacquired':1,'facility_categories':14,
                    'new_named_npc_instances':0,'new_images_requested':0,'unacquired_image_refs':14},
         'initial_intake':{'reader_unavailable_not_historical_absence':True,'requested_capture':'20011023173210',
                           'actual_capture':CAPTURE,'runner_repeats_initial_redirect_or_failure':False},
         'boundaries':BOUNDARIES.copy(),'next':'OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-16'}
    validate_report(o); return o


def main():
    p = argparse.ArgumentParser();p.add_argument('--input-entry');p.add_argument('--input-body');p.add_argument('--output',required=True);a=p.parse_args()
    require(bool(a.input_entry) == bool(a.input_body), 'Both local inputs or neither required')
    entry, ef = (Path(a.input_entry).read_bytes(),ENTRY['strict_replay_url']) if a.input_entry else fetch(ENTRY['strict_replay_url'])
    body, final = (Path(a.input_body).read_bytes(),URL) if a.input_body else fetch(URL)
    o = build(entry,ef,body,final);payload=json.dumps(o,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(payload,encoding='utf-8')
    print('SOURCE_SHA256='+SOURCE_SHA+' GRID_SHA256='+GRID_SHA)
    print('FACILITY_CATEGORIES=14 NEW_NPC_INSTANCES=0 NEW_IMAGES=0 NEW_ORIGINAL_BODIES=1')
    print('DERIVED_SHA256='+sha256(payload.encode()).hexdigest())


if __name__ == '__main__':main()
