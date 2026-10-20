"""Replay finite 2001 operator crafting pages; distinguish instructions, advice and hearsay."""
import argparse
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import struct
import urllib.request
from tools.stoneage_jp2008_shadow_release import compact,require
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'research/recovered/STONEAGE-CN20-PET-CRAFTING-SOURCE-R1.json'
URLS=(
'https://web.archive.org/web/20011204194619id_/http://www.waei.com.cn/ZHUANQU/stoneage2/pet/new_pet.asp',
'https://web.archive.org/web/20011205052725id_/http://www.waei.com.cn/ZHUANQU/stoneage2/synthesize/course.asp',
'https://web.archive.org/web/20011205052908id_/http://www.waei.com.cn/ZHUANQU/stoneage2/synthesize/cook.asp',
'https://web.archive.org/web/20011204201517id_/http://www.waei.com.cn/ZHUANQU/stoneage2/pet/skill.asp',
'https://web.archive.org/web/20020102225909id_/http://waei.com.cn/ZHUANQU/stoneage2/synthesize/IMG/course/1.gif',
'https://web.archive.org/web/20020102222833id_/http://waei.com.cn/ZHUANQU/stoneage2/synthesize/IMG/cook/1.gif')
NAMES=('nav.html','course.html','cook.html','skill.html','synthesis-reference.gif','cooking-reference.gif')
NAV=[dict(label=a,href=b) for a,b in [('合成讲座','/ZHUANQU/stoneage2/synthesize/course.asp'),('料理制作','/ZHUANQU/stoneage2/synthesize/cook.asp'),('宠物技能','/ZHUANQU/stoneage2/pet/skill.asp')]]
FOOD=[
 dict(category='汤料理',ingredients_as_written=['水'],qualification='REQUIRED_WATER_OTHER_SIMMERED_MATERIALS_UNSPECIFIED',quantities=None),
 dict(category='串烧料理',ingredients_as_written=['木串'],qualification='REQUIRED_SKEWER_OTHER_MATERIALS_UNSPECIFIED',quantities=None),
 dict(category='米饭料理',ingredients_as_written=['水','米','炭'],qualification='SOURCE_SAYS_REQUIRED_NOT_COMPLETE_RECIPE',quantities=None),
 dict(category='饭团料理',ingredients_as_written=['水','米'],qualification='CHARCOAL_HEDGED_NOT_VERY_NEEDED_NOT_PROVEN_FORBIDDEN_OR_ABSENT',quantities=None),
 dict(category='面包料理',ingredients_as_written=['橡树果'],qualification='PRIMARY_MATERIAL_NOT_EXCLUSIVE_OR_COMPLETE',quantities=None)]
FLOW=['LEARN_PROCESSING_AT_PET_SHOP','RIGHT_CLICK_ITEMS_IN_INVENTORY','CONFIRM_PROCESSING_MARKS_AND_TWO_OR_MORE_SOURCE_ITEMS','OPEN_PET_PANEL_SELECT_SKILLED_PET','SELECT_SKILL_AND_CONFIRM_MARKS','INVOKE_PROCESSING']
BOUNDARIES=dict(original_server_execution_verified=False,exact_client_build=None,first_release_date=None,
 source_host_guarantees_every_claim_is_verified=False,low_level_and_loyalty_recommendation_is_hard_requirement=False,
 suggested_pet_names_are_species_ids=False,source_skill_price_is_per_craft_fee=False,price_currency_unit=None,
 recipes_complete=False,success_formula=None,item_consumption_formula=None,storage_is_authenticated_persistent_bank=False,
 not_taking_ground_items_is_engine_enforced=False,image_same_build_as_2001_text=False,images_prove_successful_cooking=False,
 enchantment_hearsay_is_verified_formula=False,tw10_or_jss1999_backfill=False,raw_sources_committed=False,
 stage_a='7_PARTIAL_2_OPEN',stage_b_and_wiki='GATED',r79='PAUSED_NON_BLOCKING')

class Table(HTMLParser):
    def __init__(self):super().__init__();self.row=None;self.cell=None;self.rows=[]
    def handle_starttag(self,t,a):
        if t=='tr':self.row=[]
        if t in ('td','th'):self.cell=[]
    def handle_data(self,d):
        if self.cell is not None:self.cell.append(d)
    def handle_endtag(self,t):
        if t in ('td','th') and self.cell is not None:
            if self.row is not None:self.row.append(re.sub(r'\s+','',''.join(self.cell)))
            self.cell=None
        if t=='tr' and self.row is not None:self.rows.append(self.row);self.row=None

def html_core(b,title):
    h=b.decode('gb18030');require('<title>石器时代2.0</title>' in h,'Edition label missing')
    t=compact(h);require(t.count('北京华义联合软件开发有限公司')==1,'Operator footer missing/ambiguous')
    require(title in t,'Article title absent');body=t.rsplit(title,1)[1].split('北京华义联合软件开发有限公司')[0]
    return h,body

def extract_nav(b):
    from tools.stoneage_cn20_riding_source import Links
    h=b.decode('gb18030');p=Links();p.feed(h)
    found=[dict(label=a,href=u) for a,u in p.links if a in {x['label'] for x in NAV}]
    require(sorted(found,key=lambda x:x['label'])==sorted(NAV,key=lambda x:x['label']),'Actual three named routes changed')
    return dict(routes=NAV)

def extract_course(b):
    h,t=html_core(b,'合成讲座')
    for s in ['宠物店让宠物学加工的技能','按鼠标右键点选想要加工的道具','选择两种以上的道具','该道具会出现加工的标记','选择持有加工技能的宠物','选择宠物的加工技能',
              '玩家的运气也会影响到加工合成的成功率','最好都要等级1的，忠诚100','传说中适合合成的宠物','失败以后原有的东西都会不见，或是变成其他的东西',
              '有消息指出：双数等级的武器','魔法等级1花8mp，魔法等级2花9mp','单数等级武器','不花费mp']:
        require(s in t,'Instruction/advice/hearsay distinction lost: '+s)
    require('IMG/course/1.gif' in h and 'IMG/course/1s.gif' in h,'Actual illustration link changed')
    return dict(core_sha256=sha256(t.encode()).hexdigest(),core_utf8_bytes=len(t.encode()),
        facts=dict(flow=FLOW,minimum_items_source_wording='两种以上 / 两项',distinct_species_or_stack_predicate=None,
        skill_taught_to='PET',teacher_surface='宠物店',action_surface='INVENTORY_RIGHT_CLICK_THEN_PET_SKILL_PANEL',
        failure_outcomes_reported=['ORIGINALS_DISAPPEAR','TRANSFORM_TO_OTHER_ITEMS'],probabilities=None,
        low_level_1_loyalty_100='SITE_RECOMMENDATION_NOT_ACCESS_PREDICATE',pet_list='SOURCE_SAYS_POPULAR_OR_LEGENDARY_NOT_SPECIES_MASTER',
        fortune_telling='SOURCE_ADVICE_AT_VILLAGE_CHIEF_HOUSE_NOT_PROVEN_ENGINE_DEPENDENCY',
        enchantment_parity_mp_duration='EXPLICIT_YOU_XIAOXI_ZHICHU_HEARSAY_NOT_RUNTIME_FORMULA'),
        image_ref=dict(full='IMG/course/1.gif',thumbnail='IMG/course/1s.gif'))

def extract_cook(b):
    h,t=html_core(b,'料理制作')
    for s in ['玛莉娜丝村或加加村的便利商店','打到的肉除了补血也可以当料理材料','先问问看人家要不要给你','右下角有一个物品寄放处',
              '不能超过5个不然最先放进去的东西会不见','依玩家的经验，听说等级越低','一般料理分为五种类','水是绝对需要的','木串是必要品','水，米及炭',
              '水及米仍是需要炭则不太需要的样子','主要是要有橡树果','等级相当并不是指价格']:
        require(s in t,'Cooking ingredient/hedge/storage clause missing: '+s)
    require('IMG/cook/1.gif' in h and 'IMG/cook/1s.gif' in h,'Actual illustration link changed')
    return dict(core_sha256=sha256(t.encode()).hexdigest(),core_utf8_bytes=len(t.encode()),
        facts=dict(food_categories=FOOD,material_sources=['玛莉娜丝村便利商店','加加村便利商店','战斗取得的肉'],
        material_grade_is_not_price=True,ground_items='ASK_OWNER_FIRST_SOCIAL_ADVICE_NOT_GAME_LOCK',
        temporary_storage=dict(surface='便利屋右下角物品寄放处',source_limit=5,overflow='EARLIEST_ITEM_DISAPPEARS_SOURCE_WARNING',unit_or_persistence=None),
        low_level_pet='PLAYER_EXPERIENCE_HEARSAY',material_price_difference='LOCAL_SPECIALTY_AT_CONVENIENCE_STORE_REPORTED_MORE_EXPENSIVE_NO_PRICE_LIST'),
        image_ref=dict(full='IMG/cook/1.gif',thumbnail='IMG/cook/1s.gif'))

def extract_skill(b):
    h,t=html_core(b,'宠物技能')
    for s in ['「合成」与「料理」技能','不一定会百分之百成功','要视宠物的特性与运气']:require(s in t,'Skill context missing')
    p=Table();p.feed(h);rows=[x for x in p.rows if x and x[0] in ('加工','料理')]
    require(rows==[['加工','使用素材合成制作道具','1500'],['料理','使用素材合成制作料理','1000']],'Exact crafting skill rows/price columns changed')
    return dict(core_sha256=sha256(t.encode()).hexdigest(),core_utf8_bytes=len(t.encode()),facts=dict(
        skills=[dict(name=x[0],description=x[1],price_label=int(x[2]),price_currency=None,price_role='SKILL_PRICE_COLUMN_NOT_PER_CRAFT_FEE') for x in rows],
        success='NOT_GUARANTEED_PET_TRAITS_AND_LUCK_NO_FORMULA',processing_synthesis='SAME_SOURCE_CONTEXT_TERMS_NOT_GLOBAL_CROSS_VERSION_SKILL_ID'))

def image_metadata(b):
    require(b[:6] in (b'GIF87a',b'GIF89a') and len(b)>=13,'Not a GIF')
    w,h=struct.unpack('<HH',b[6:10]);require((w,h)==(640,480),'Reference dimensions changed')
    return dict(format='GIF',width=w,height=h,visual_observation='MANUAL_SOURCE_REFERENCE_ONLY_NOT_EXECUTION')

def validate(r):
    require(r['schema']=='stoneage.cn20_pet_crafting.source.r1','Schema')
    require([s['replay_url'] for s in r['inputs']]==list(URLS),'Finite sources changed')
    require(r['boundaries']==BOUNDARIES,'Boundary promotion')
    require(len(r['records'])==14,'Fourteen documentary records required')
    required={'record_id','entity_type','version_profile','source_refs','verification_status','rights_status','record_revision'}
    for row in r['records']:
        require(required<=row.keys() and row['game_ids'] is None,'Archive contract/IDs')
        require(row['rights_status']=='RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED','Rights')
        require(row['verification_status']=='SOURCE_REPORTED_NOT_RUNTIME','Source promoted to runtime')
    require(r['records'][0]['facts']==r['inputs'][1]['extracted']['facts'],'Workflow detached')
    require([x['facts'] for x in r['records'][1:3]]==r['inputs'][3]['extracted']['facts']['skills'],'Skill prices detached')
    require([(x['facts']['name'],x['facts']['price_label'],x['facts']['price_currency'],x['facts']['price_role']) for x in r['records'][1:3]]==[('加工',1500,None,'SKILL_PRICE_COLUMN_NOT_PER_CRAFT_FEE'),('料理',1000,None,'SKILL_PRICE_COLUMN_NOT_PER_CRAFT_FEE')],'Price meaning changed')
    require([x['facts'] for x in r['records'][3:8]]==FOOD,'Category recipe overclaim')
    require(r['records'][8]['facts']==r['inputs'][2]['extracted']['facts']['temporary_storage'],'Storage detached')
    require(r['records'][9]['status']=='SITE_ADVICE_AND_EXPLICIT_PLAYER_EXPERIENCE_NOT_PREREQUISITE','Advice promoted')
    require(r['records'][10]['status']=='EXPLICIT_SOURCE_HEARSAY_NOT_VERIFIED_FORMULA','Hearsay promoted')
    require(r['records'][11]['per_craft_fee'] is None and r['records'][11]['success_formula'] is None,'Fee/formula invented')
    require(all(x['same_build_as_2001_text'] is False and x['successful_craft_verified'] is False for x in r['records'][12:]),'Image/runtime promotion')
    require(r['next']=='OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-30','Return whole portfolio')

def replay(r,payloads):
    validate(r);require(len(payloads)==6,'Exactly four HTML/two GIF inputs required')
    got=[fn(b) for fn,b in zip((extract_nav,extract_course,extract_cook,extract_skill,image_metadata,image_metadata),payloads)]
    for s,b,x in zip(r['inputs'],payloads,got):
        require(len(b)==s['http']['bytes'] and sha256(b).hexdigest()==s['http']['sha256'],'Exact historical source byte pin changed')
        require(x==s['extracted'],'Historical semantic replay differs')
    return dict(schema='stoneage.cn20_pet_crafting.replay.r1',inputs=[dict(source_id=s['id'],bytes=len(b),sha256=sha256(b).hexdigest(),capture_timestamp=s['capture_timestamp']) for s,b in zip(r['inputs'],payloads)],extracted=got,raw_sources_in_output=False,original_server_execution_verified=False,hearsay_promoted=False,images_same_build_as_text=False)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--fetch',action='store_true');p.add_argument('--source-dir',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();require(a.fetch!=bool(a.source_dir),'Choose fetch or transient files');payloads=[]
    for u,n in zip(URLS,NAMES):
        if a.fetch:
            with urllib.request.urlopen(u,timeout=45) as response:
                require(response.status==200 and response.url==u,'Unexpected HTTP or redirect');b=response.read(2_000_001);require(len(b)<=2_000_000,'Oversized source')
        else:b=(a.source_dir/n).read_bytes()
        payloads.append(b)
    result=replay(json.loads(REPORT.read_text()),payloads);a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('HTML_VERIFIED=4 GIF_REFERENCE_VERIFIED=2 FOOD_CATEGORIES=5 SOURCE_SKILL_PRICES=2 ORIGINAL_SERVER_EXECUTIONS=0')

if __name__=='__main__':main()

