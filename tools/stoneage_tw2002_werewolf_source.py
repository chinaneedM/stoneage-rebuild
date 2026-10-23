"""R82: reported pet form transition and named acquisition context, not runtime."""
import argparse
import hashlib
import io
import json
import re
import urllib.request
from pathlib import Path
from PIL import Image
from tools.stoneage_jp2005_treasure_source import VisibleMarkup, plain, one, require, sha

ROOT=Path(__file__).resolve().parents[1]
STEM='STONEAGE-TW2002-WEREWOLF-FORMS'
REPORT=ROOT/f'research/recovered/{STEM}-SOURCE-R1.json'
ARTICLE_URL='https://gnn.gamer.com.tw/detail.php?sn=5718'
URL='https://web.archive.org/web/20190820052955id_/https://gnn.gamer.com.tw/detail.php?sn=5718'
PROFILE='TW_MARKET_CONTEXT_2002_GNN_WEREWOLF_REPORT_CAPTURE_20190820_EXACT_SERVER_BUILD_UNKNOWN'
PARSER='tools/stoneage_jp2005_treasure_source.py'
PARENTS=['research/recovered/STONEAGE-CN30-SPECIAL-PET-SKILLS-SOURCE-R1.json',
 'research/recovered/STONEAGE-JP2005-AUTUMN-COOKING-SOURCE-R1.json',
 'research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json']
TITLE='「石器時代」大玩寵物變裝秀'
SOURCE={'url':URL,'original_article_url':ARTICLE_URL,'capture':'20190820052955','http_status':200,'no_redirect':True,
 'bytes':25749,'sha256':'860bfa744ce89248eb64d73636e2ccc6bcb26e12b63e62b5506d6e5cf7237998',
 'encoding':'UTF8_STRICT','visible_title':TITLE,'visible_publication':'2002-09-13 21:06:37',
 'byline_as_written':'（GNN 記者  報導）','named_reporter':None,'authority':'ARCHIVED_PRESS_REPORT_NOT_DIRECT_OPERATOR_RELEASE',
 'region_qualification':'TAIWAN_MARKET_CONTEXT_INFERRED_NOT_AUTHENTICATED_SERVER_BUILD',
 'current_article_request_status':403,'current_article_body_acquired':False,'current_body_archive_equality_verified':False,
 'availability_requested_timestamp':'20020914','availability_returned_timestamp':'20190820052955',
 'capture_is_publication_or_build':False,'authenticated_2002_original_bytes':False,'official_authorship_verified':False}
IMAGES=[
 {'id':'I1','url':'https://p2.bahamut.com.tw/S/2KU/55/0000089255.JPG','bytes':14244,'sha256':'fa4fe54fd11130616026702f9f20096284f4496267ea370d9a67e682f9cf81a2'},
 {'id':'I2','url':'https://p2.bahamut.com.tw/S/2KU/56/0000089256.JPG','bytes':15506,'sha256':'f46a29766362cb70270653ba1c62d5e4da28b20c7a1c902d367cbb83110f3994'},
 {'id':'I3','url':'https://p2.bahamut.com.tw/S/2KU/57/0000089257.JPG','bytes':12617,'sha256':'511919de15d047ec0ebe2ad5c8b733fda962ee249dac5427b4df5bc1747bfd74'}]
for im in IMAGES:im.update(http_status=200,no_redirect=True,format='JPEG',mode='RGB',size=[120,120],frames=1,variant='ACTUAL_SMALL_S_GALLERY_REFERENCE',full_original_acquired=False,historical_2002_pixels_authenticated=False)
VISUAL=[
 {'id':'I1','manual_visual_review':True,'kind':'PURPLE_PRODUCT_ART_WITH_CRESCENT_WOLF_HEAD_AND_PEOPLE','in_game_form_transition_observed':False,'exact_product_or_pet_identity_from_pixels_alone':False},
 {'id':'I2','manual_visual_review':True,'kind':'ORANGE_RED_FLAME_LIKE_HORNED_BEAST_ILLUSTRATION','assigned_to_named_fire_beast':False},
 {'id':'I3','manual_visual_review':True,'kind':'GREEN_YELLOW_HORNED_BEAST_ILLUSTRATION','assigned_to_named_earth_beast':False}]
BOUNDARIES={k:False for k in ('direct_operator_release_acquired','capture_is_publication_date','original_2002_bytes_authenticated',
 'current_article_body_matches_archive','tw10_jss1999_or_exact_4_0_build_authenticated','human_form_is_playable_character',
 'moon_named_skill_proves_lunar_or_day_night_gate','battle_end_reverse_transition_verified','best_pet_claim_is_numeric_master_or_growth',
 'limited_issuance_is_world_instance_census_or_encounter_rate','package_acquisition_is_wild_capture',
 'wgs_points_or_stone_are_purchase_price','mail_phone_condition_is_virtual_pet_redemption_condition',
 'tabletop_dice_are_mmo_combat_rng','140_cards_are_140_pets','two_beast_prizes_medium_or_actual_grant_verified',
 'flame_or_green_color_authenticates_named_species','small_gallery_jpeg_is_original_sprite_model_or_animation',
 'original_html_or_assets_committed','stage_b_started')}


def article(raw):
 p=VisibleMarkup();p.feed(raw.decode('utf8',errors='strict'));text=''.join(p.parts)
 require(plain(one(r'<h1>(.*?)</h1>',text,re.S))==TITLE,'Visible article title changed')
 require(plain(one(r'<span class="GN-lbox3C">(.*?)</span>',text,re.S))=='（GNN記者報導）2002-09-1321:06:37','Visible byline/publication changed')
 body=one(r'<!-- 新聞內容 -->(.*?)<!-- 新聞內容結束 -->',text,re.S)
 parts=[plain(v) for v in re.split(r'<br\s*/>\s*<br\s*/>',body)];require(len(parts)==4 and all(parts),'Four visible article paragraphs required')
 require([v[:6] for v in parts]==['在石器虛擬的','狼人寵平時是','除了新增變身','預計推出第一'],'Ordered article paragraphs changed')
 gallery=one(r'<!-- 圖片區塊 -->(.*?)<!-- 圖片區塊結束 -->',text,re.S)
 require(re.findall(r'<img src="([^"]+)" name="gnnPIC" title="" alt="">',gallery)==[v['url'] for v in IMAGES],'Actual uncaptioned S-gallery links changed')
 return plain(body),parts


def derive(raw):
 core,p=article(raw)
 def must(i,*clauses):require(all(plain(c) in p[i] for c in clauses),'Changed reported clause in paragraph '+str(i+1))
 must(0,'限量的夢幻寵物-狼人','二百多種寵物中唯一具有變裝功能的寵物','此為石器首創之舉')
 must(1,'狼人寵平時是人的形體，進入戰鬥畫面時才會變身為狼','兇猛如暴龍的攻擊力及月夜變身的超炫技能',
  '各項能力屬性及數值最好的一個','NO.1的夢幻寵物','限量發行1萬隻',
  '於9/15在各電腦賣場購買「引狼入室包」，就可獲得狼人寵一隻',
  '另含WGS點數360點-狼人珍藏版、石器4.0版遊戲雙光碟 + 說明書、石幣30萬',
  '寄回印花及申請書即可獲得行動電話-MOTOROLA T190寶貝機一支')
 must(2,'於9/19隆重推出另一週邊商品：「石器時代魔法牌」','日本石器時代原製作團隊的柴垣秀樹先生作原創設計',
  '規則綜合了「魔法風雲會」及「遊戲王」2款最受歡迎的魔法牌優點','投擲骰子的機制')
 must(3,'預計推出第一版「萬事俱備包」中將另外贈送二隻石器魔法獸','地魔獸-赫拉克勒斯、火魔獸-翟貝里恩',
  '石器魔法基本牌二包共140張','魔法牌入門教學光碟','遊戲骰子')
 return {'werewolf':{'name':'狼人','ordinary_form_as_reported':'人的形體','transformed_form_as_reported':'狼',
   'reported_transition':'ENTER_BATTLE_SCREEN','reverse_transition_on_battle_end':None,'lunar_phase_or_clock_condition':None,
   'skill_label_as_written':'月夜變身','actual_cast_action_cost_duration_or_skill_id':None,
   'tyrannosaurus_attack_phrase':'PROMOTIONAL_SIMILE_NOT_EQUAL_NUMERIC_STATS',
   'uniqueness_and_no1':'CONTEMPORANEOUS_PROMOTIONAL_CLAIMS_NOT_COMPLETE_CENSUS_OR_STAT_TABLE',
   'stats_growth_elements_and_native_pet_id':None,'original_form_sprite_or_model_ids':None},
  'werewolf_acquisition':{'context_year':2002,'month_day_as_written':'9/15','actual_sale_or_redemption_executed':False,
   'place_as_written':'各電腦賣場','product_name':'引狼入室包','pet_count_as_reported':1,
   'limited_issuance_as_reported':10000,'current_world_instances_or_capture_probability':None,'purchase_price':None,
   'other_contents':{'WGS_points':360,'points_edition_label':'狼人珍藏版','included_media_label':'石器4.0版遊戲雙光碟','manual':True,'stone':300000},
   'media_label_authenticates_exact_pet_build_or_first_release':False,'redemption_transport_or_original_item_id':None,
   'phone_offer':{'model':'MOTOROLA T190','count_as_reported':1,'requires':['RETURN_STAMPS','APPLICATION_FORM'],
    'actual_fulfillment_or_pet_redemption_precondition':None}},
  'card_product_context':{'name':'石器時代魔法牌','announced_month_day':'9/19','year_context':2002,
   'external_tabletop_product_by_context_inference':True,'designer_as_reported':'柴垣秀樹',
   'designer_is_verified_sole_mmo_creator':False,'rules_comparisons_as_reported':['魔法風雲會','遊戲王'],
   'dice_mechanic':'CARD_PRODUCT_CONTEXT_NOT_MMO_DAMAGE_FORMULA'},
  'first_card_pack':{'name':'萬事俱備包','release_status_as_written':'預計推出','reward_status_as_written':'將另外贈送',
   'exact_pack_launch_date_or_actual_execution':None,'named_beast_count':2,
   'named_beasts':[{'label':'地魔獸','name':'赫拉克勒斯'},{'label':'火魔獸','name':'翟貝里恩'}],
   'beast_medium_redemption_or_native_ids':None,'beast_stats_skills_or_element_proportions':None,
   'physical_card_pack_count':2,'physical_card_count':140,'in_game_pet_count_from_140':None},
  'timezone_explicit_in_visible_text':None,'region_or_exact_server_build_authenticated':False,
  'original_server_runtime_verified':False,'gallery':{'count':3,'captions_as_written':['','',''],'full_originals_acquired':False,'forms_or_beast_names_assigned_by_order':False},
  'paragraph_fingerprints':[{'index':i+1,'characters':len(v),'sha256':sha(v.encode())} for i,v in enumerate(p)],
  'core_fingerprint':{'characters':len(core),'utf8_bytes':len(core.encode()),'sha256':sha(core.encode())}}


def pin(path):
 b=(ROOT/path).read_bytes();return {'path':path,'bytes':len(b),'sha256':sha(b),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}


def comparison():
 cn=json.loads((ROOT/PARENTS[0]).read_text());jp=json.loads((ROOT/PARENTS[1]).read_text())
 return {'cn30_special_skills':{'schema':cn['schema'],'t_prefix_school_donation_or_dismount_rules_backfilled':False,
  'same_skill_id_or_werewolf_is_mechanical_tyrannosaur_verified':False},
  'jp2005_candy':{'schema':jp['schema'],'separate_reported_event':jp['extraction']['halloween']['name'],
   'gm_transformation_candy_is_werewolf_pet_skill':False,'same_effect_protocol_or_art_resource_verified':False},
  'later_reposts_or_player_skill_names_used_to_replace_monthnight_label':False,'modern_adoption_decided':False}


def catalog(ex):
 rows=[('werewolf','pets','DOCUMENTARY_NAMED_TRANSFORMING_PET',ex['werewolf'],['S1']),
  ('monthnight','skills','DOCUMENTARY_PET_FORM_CHANGE_LABEL_NOT_SKILL_MASTER',{'label':'月夜變身','transition':'ENTER_BATTLE_SCREEN','native_skill_id':None},['S1']),
  ('acquisition','items','DOCUMENTARY_PROMOTION_PRODUCT_NOT_INVENTORY_MASTER',ex['werewolf_acquisition'],['S1']),
  ('first-card-pack','items','DOCUMENTARY_PLANNED_CARD_PRODUCT',ex['first_card_pack'],['S1']),
  ('card-context','tutorials','DOCUMENTARY_PERIPHERAL_CARD_GAME_BOUNDARY',ex['card_product_context'],['S1'])]
 rows += [('beast-'+str(i),'pets','DOCUMENTARY_PLANNED_NAMED_BEAST_GIFT_MEDIUM_UNVERIFIED',v,['S1']) for i,v in enumerate(ex['first_card_pack']['named_beasts'])]
 rows += [(im['id'],'screens','DOCUMENTARY_SMALL_PRESS_ILLUSTRATION_NOT_GAME_SCREEN',{'image':im,'observation':v},['S1',im['id']]) for im,v in zip(IMAGES,VISUAL)]
 return [{'record_id':'TW2002-R82-'+ident,'entity_type':kind,'collection':coll,'version_profile':PROFILE,'source_refs':refs,
  'verification_status':'ARCHIVED_PRESS_CLAIM_OR_CURRENT_SMALL_IMAGE_NOT_RUNTIME','rights_status':'RESEARCH_METADATA_NOT_RELEASE_APPROVED',
  'record_revision':1,'game_ids':None,'content':content} for ident,coll,kind,content,refs in rows]


def semantic(ex):return {k:v for k,v in ex.items() if k not in ('paragraph_fingerprints','core_fingerprint')}


SEMANTIC_SHA='c46e0515a24c932336d8d6b716a969a6fb8249bb7c1704ef491ffc0b4f1b1a3a'

def validate(r):
 require(r['schema']=='stoneage.tw2002_werewolf.source.r1' and r['version_profile']==PROFILE,'Version/schema changed')
 require(r['source']==SOURCE and r['images']==IMAGES and r['visual_observations']==VISUAL and r['negative_boundaries']==BOUNDARIES,'Intake/history/visual/authority boundaries changed')
 require(r['parent_pins']==[pin(p) for p in PARENTS] and r['parser_pin']==pin(PARSER),'Parent/parser bytes changed')
 require(r['comparison']==comparison(),'Cross-region skill distinctions changed')
 require(sha(json.dumps(semantic(r['extraction']),ensure_ascii=False,sort_keys=True).encode())==SEMANTIC_SHA,'Documentary pet/transition/product contract changed')
 require(r['catalog_records']==catalog(r['extraction']),'Catalog detached')
 c=json.loads((ROOT/PARENTS[-1]).read_text())['future_website']
 require(len(r['catalog_records'])==10 and len({v['record_id'] for v in r['catalog_records']})==10,'Catalog count/identity changed')
 require(all(set(c['record_contract']['required']).issubset(v) and v['collection'] in c['required_collections'] for v in r['catalog_records']),'Archive required fields changed')


MUTATIONS=[('進入戰鬥畫面時才會變身為狼','夜晚滿月時才會變身為狼'),('平時是人的形體','平時是狼的形體'),
 ('月夜變身','暗月變身'),('兇猛如暴龍','攻擊值等同暴龍'),('唯一具有變裝功能','所有寵物都有變裝功能'),
 ('限量發行1萬隻','限量發行2萬隻'),('於9/15','於9/16'),('購買「引狼入室包」','野外捕獲「引狼入室包」'),
 ('狼人寵一隻','狼人寵二隻'),('WGS點數360點','WGS點數630點'),('石器4.0版','石器1.0版'),('石幣30萬','石幣3萬'),
 ('寄回印花及申請書','只需口頭申請'),('MOTOROLA T190','MOTOROLA T200'),('於9/19','於9/20'),
 ('另一週邊商品','原遊戲戰鬥系統'),('柴垣秀樹','未具名設計師'),('投擲骰子的機制','即時戰鬥的機制'),
 ('預計推出第一版','已實際推出第一版'),('將另外贈送二隻','已實際贈送二隻'),('地魔獸-赫拉克勒斯','水魔獸-赫拉克勒斯'),
 ('火魔獸-翟貝里恩','火魔獸-另一物種'),('二包共140張','二包共150張')]


def audit(raw,expected):
 text=raw.decode('utf8');target=semantic(expected)
 for old,new in MUTATIONS:
  require(old in text,'Missing real source mutation: '+old)
  try:actual=derive(text.replace(old,new).encode())
  except (ValueError,IndexError):continue
  require(semantic(actual)!=target,'Meaning changed but only fingerprint detected it: '+old)
 require(derive(raw+b'<script>outside=1</script>')==expected,'Peripheral script changed meaning')
 old='進入戰鬥畫面時才會變身為狼'
 for replacement in ('','<script>'+old+'</script>'):
  changed=text.replace(old,replacement)+'<div>'+old+'</div>'
  try:derive(changed.encode())
  except ValueError:pass
  else:raise ValueError('Hidden/outside-body words repaired missing battle trigger')
 return {'semantic_mutations_without_all_fingerprints':len(MUTATIONS),'hidden_and_outside_article_counterexamples':2,'outside_script_positive':True}


def inspect_images(inputs):
 for expected in IMAGES:
  raw=inputs[expected['id']]
  with Image.open(io.BytesIO(raw)) as im:
   im.load();actual={'bytes':len(raw),'sha256':sha(raw),'size':list(im.size),'format':im.format,'mode':im.mode,'frames':getattr(im,'n_frames',1)}
  require(all(expected[k]==v for k,v in actual.items()),'Reviewed small illustration bytes/full decode changed')


def replay(inputs,r):
 validate(r);ex=derive(inputs['S1']);require(ex==r['extraction'],'Archived article extraction changed');inspect_images(inputs)
 require(len(inputs['S1'])==SOURCE['bytes'] and sha(inputs['S1'])==SOURCE['sha256'],'Archived current raw bytes changed')
 return {'schema':'stoneage.tw2002_werewolf.replay.r1','inputs':[{'id':k,'url':URL if k=='S1' else next(v['url'] for v in IMAGES if v['id']==k),'bytes':len(v),'sha256':sha(v)} for k,v in inputs.items()],
  'extraction':ex,'images':IMAGES,'visual_observations':VISUAL,'comparison':comparison(),'catalog_records':catalog(ex),
  'audit':audit(inputs['S1'],ex),'original_html_or_assets_in_output':False,'original_server_runtime_verified':False}


def read_inputs(directory=None):
 result={}
 for key,url in [('S1',URL)]+[(v['id'],v['url']) for v in IMAGES]:
  if directory:result[key]=(Path(directory)/(key+('.html' if key=='S1' else '.jpg'))).read_bytes()
  else:
   with urllib.request.urlopen(url,timeout=50) as h:
    require(h.status==200 and h.url==url,'Exact capture/image URL or status changed');result[key]=h.read()
 return result


def main():
 p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--fetch',action='store_true');g.add_argument('--input-dir');p.add_argument('--output',required=True);a=p.parse_args()
 r=json.loads(REPORT.read_text());out=replay(read_inputs(a.input_dir),r)
 path=Path(a.output);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print('R82 archived werewolf battle-form report and three small illustrations replayed; original IDs, full models and runtime remain unknown.')


if __name__=='__main__':main()
