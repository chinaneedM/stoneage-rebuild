"""Bounded documentary replay of a 2005 Japanese PC cooking/event report.

The report is journalism about an operator announcement, not a quoted release,
an original master table, an observed reward delivery, or a game implementation.
"""
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
STEM='STONEAGE-JP2005-AUTUMN-COOKING'
REPORT=ROOT/f'research/recovered/{STEM}-SOURCE-R1.json'
URL='https://www.4gamer.net/news/history/2005.09/20050921202336detail.html'
IMAGE_URL='https://www.4gamer.net/news/image/2005.09/20050921202336_0.jpg'
PROFILE='JP_PC_2005_GAIAX_AUTUMN_SCHEDULE_REPORTED_20050921_EXACT_BUILD_UNKNOWN'
PARSER='tools/stoneage_jp2005_treasure_source.py'
PARENTS=['research/recovered/STONEAGE-CN20-PET-CRAFTING-SOURCE-R1.json',
 'research/recovered/STONEAGE-JP2005-TREASURE-EVENT-SOURCE-R1.json',
 'research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json']
TITLE='「ストーンエイジ」食欲の秋にちなんだイベントを開催'
LABELS=['ストーンエイジ秋の祭典その1「グルメマスターに挑戦！」',
 'ストーンエイジ秋の祭典その2「食材半額セール」','GMのお料理教室',
 'ストーンエイジ川柳コンテスト ～秋～','ハロウィンイベント（仮称）']
SOURCE={'url':URL,'http_status':200,'no_redirect':True,'bytes':19261,
 'sha256':'fa5f6876b8385ee7851eeafcb57cfbfb065abafb0b2879993208d6f183f1407f',
 'encoding':'CP932_STRICT','visible_title':TITLE,'visible_publication':'2005/09/21 20:23',
 'author_as_signed':'aueki','operator_as_reported':'ガイアックス',
 'authority':'CONTEMPORANEOUS_JOURNALISM_REPORTING_OPERATOR_ANNOUNCEMENT',
 'explicit_verbatim_manufacturer_release':False,'official_event_detail_link_in_article':None,
 'actual_operator_event_page_acquired':False,'current_bytes_authenticate_2005_original':False}
IMAGE={'id':'I1','url':IMAGE_URL,'http_status':200,'no_redirect':True,'bytes':28727,
 'sha256':'9b801c91204166fdfea81ca20f38ab049137c144a9c8edf1d85d7d6bd2f14cab',
 'size':[232,310],'format':'JPEG','mode':'RGB','frames':1}
VISUAL={'manual_visual_review':True,'kind':'COOKING_THEME_CHARACTER_ILLUSTRATION',
 'visible':['SPIKY_HAIRED_CHARACTER','STEAMING_CAULDRON_OVER_FIRE_AND_STONES','STIRRING_UTENSIL'],
 'identified_as_gavi_or_gourmet_master':False,'game_screenshot':False,
 'recipe_ui_or_reward_delivery':False,'original_sprite_model_animation':False,
 'species_npc_or_character_id':None,'native_client_resolution_proven':False}
BOUNDARIES={k:False for k in ('direct_operator_source_acquired','manufacturer_verbatim_release',
 'current_bytes_authenticate_2005_original','schedule_proves_event_execution','exact_client_build_verified',
 'gourmet_master_controller_or_npc_id_known','complete_recipes_restored','quest_reward_is_capture_buff_meal',
 'sale_covers_all_items_or_all_shops','same_village_ids_across_regions_verified',
 'lesson_server_scope_is_all_servers','gavi_is_wild_catch_or_quest_reward',
 'promotional_unique_pet_claim_is_instance_census','contest_prize_distribution_executed',
 'capture_buff_formula_duration_guarantee_known','illustration_identifies_named_pet_or_actor',
 'halloween_candy_is_monster_drop','source_era_free_to_play_verified',
 'original_html_or_assets_committed','stage_b_started')}


def article(raw):
 p=VisibleMarkup();p.feed(raw.decode('cp932',errors='strict'));text=''.join(p.parts)
 title=one(r'<!--↓大見出し-->(.*?)<!--↑大見出し-->',text,re.S)
 require(plain(one(r'<h5>(.*?)</h5>',title,re.S))==TITLE,'Article title changed')
 require(plain(one(r'<div class="news_txt1">(.*?)</div>',text,re.S))==plain('2005/09/21 20:23'),'Publication label changed')
 area=one(r'<td class="newstext">(.*?)<!-- tDialy:END -->',text,re.S)
 blocks=[v for v in re.findall(r'<!-- 本文開始 -->(.*?)<!-- 本文終了 -->',area,re.S) if plain(v)]
 require(len(blocks)==1,'Exactly one visible nonempty article body required')
 body=blocks[0]
 parts=re.split(r'<FONT class="headline">(.*?)</FONT>',body,flags=re.S|re.I)
 require([plain(v).removeprefix('■') for v in parts[1::2]]==[plain(v) for v in LABELS],'Five ordered event headings required')
 sections={label:plain(value) for label,value in zip(LABELS,parts[2::2])}
 require(re.findall(r'<IMG SRC="([^"]+)" WIDTH=(\d+) HEIGHT=(\d+)',area)==[('/news/image/2005.09/20050921202336_0.jpg','232','310')],'Actual image link changed')
 require(re.findall(r'<A href="([^"]+)"',body,re.I)==['http://www.4gamer.net/DataContents/game/1377.html'],'Article link inventory changed')
 require('ガイアックスは' in plain(parts[0]) and '10月のイベントスケジュールを発表した' in plain(parts[0]),'Operator/scheduled status changed')
 require(plain(body).endswith('（aueki）'),'Signed journalistic tail changed')
 return plain(body),sections


def derive(raw):
 core,s=article(raw)
 def must(i,*clauses):require(all(plain(v) in s[LABELS[i]] for v in clauses),'Changed event clause: '+LABELS[i])
 must(0,'日時：10月4日～10月11日','場所：全サーバーチャットルームよりスタート',
  'イベント期間中，チャットルームにグルメマスターが現れる',
  'グルメマスターの指定する料理をすべて完成させると，新アイテム「石器時代フルコース」がもらえる')
 must(1,'日時：10月4日～10月11日','場所：全サーバー ジャジャ村，マリナスの漁村',
  'ジャジャ村およびマリナスの漁村のコンビニで売られている食材がすべて半額となる')
 must(2,'日時：10月8日','昼の部：14:00～14:30 火星サーバー ジャジャ村のコンビニ',
  '夜の部：20:00～20:30 水星サーバー マリナス漁村のコンビニ',
  'GMがコンビニで秋にちなんだ料理のレシピをレクチャーする')
 must(3,'日時：10月4日～10月18日','場所：公式サイト上','秋をテーマにしたストーンエイジの川柳を募集する（それって俳句では？）',
  '最優秀作，佳作に選ばれると，以下のようなプレゼントがもらえる',
  '最優秀作：ペット恐竜「ガーヴィ」世界に1匹のレアペット',
  '佳作： 「すらすらペン」自作の合成装備に名前を付けられるペン',
  '「秋の満腹セット」捕獲率が大幅にアップする料理')
 must(4,'日時：10月29日 21:00～22:00','場所：全サーバー（いろいろな場所に出現）',
  'GMがさまざまな場所に出現し，いろいろな姿に変身できるようになるアイテム（お菓子）などを配布する')
 return {'year_context':2005,'year_repeated_in_each_window':False,'timezone':None,'actual_execution_verified':False,
  'challenge':{'name':'グルメマスターに挑戦！','window_month_day':['10-04','10-11'],'exact_hours':None,
   'start':'ALL_SERVERS_CHATROOM','role':'グルメマスター','role_controller_npc_or_gm':None,
   'condition':'COMPLETE_ALL_DISHES_SPECIFIED_BY_GOURMET_MASTER','reward':'石器時代フルコース',
   'recipes_quantities_turnin_consumption_repeatability':None,'reward_effect':None},
  'sale':{'name':'食材半額セール','window_month_day':['10-04','10-11'],'servers':'ALL',
   'villages_as_written':['ジャジャ村','マリナスの漁村'],'shops':'CONVENIENCE_STORES_OF_THESE_TWO_VILLAGES',
   'goods':'ALL_FOOD_INGREDIENTS_SOLD_THERE','price_fraction_as_reported':[1,2],
   'base_prices_currency_rounding_inventory_transactions':None},
  'lessons':{'name':'GMのお料理教室','date_month_day':'10-08','sessions':[
   {'part':'昼の部','hours':['14:00','14:30'],'server':'火星サーバー','place':'ジャジャ村のコンビニ'},
   {'part':'夜の部','hours':['20:00','20:30'],'server':'水星サーバー','place':'マリナス漁村のコンビニ'}],
   'actor':'GM','purpose':'LECTURE_ON_AUTUMN_COOKING_RECIPES','actual_recipes_and_gm_names':None},
  'contest':{'name':'ストーンエイジ川柳コンテスト ～秋～','window_month_day':['10-04','10-18'],
   'venue':'OFFICIAL_WEBSITE','theme':'AUTUMN_STONEAGE_SENRYU','haiku_question':'EDITORIAL_ASIDE_NOT_OFFICIAL_RECLASSIFICATION',
   'best_prize':{'name':'ガーヴィ','kind_as_reported':'ペット恐竜','claim_as_written':'世界に1匹のレアペット',
    'verified_world_instance_count':None,'stats_growth_skills_habitat_native_id':None},
   'honorable_mentions':[
    {'name':'すらすらペン','effect':'NAME_ONES_OWN_SYNTHESIZED_EQUIPMENT','uses_consumption':None},
    {'name':'秋の満腹セット','effect':'GREATLY_BOOST_CAPTURE_RATE_AS_REPORTED','formula_duration_guarantee':None}],
   'winner_count_each_winner_gets_both_and_actual_award':None},
  'halloween':{'name':'ハロウィンイベント（仮称）','provisional_title':True,'date_month_day':'10-29',
   'hours':['21:00','22:00'],'servers':'ALL','places':'VARIOUS_UNSPECIFIED','actor':'GM',
   'distribution':'TRANSFORMATION_ITEMS_CANDY_AND_OTHER_ITEMS_AS_REPORTED',
   'item_names_forms_duration_spawn_algorithm_and_drop_rules':None},
  'original_event_npc_item_pet_recipe_ids':None,'exact_client_build':None,
  'section_fingerprints':[{'label':k,'characters':len(v),'sha256':sha(v.encode())} for k,v in s.items()],
  'core_fingerprint':{'characters':len(core),'utf8_bytes':len(core.encode()),'sha256':sha(core.encode())}}


def pin(path):
 b=(ROOT/path).read_bytes();return {'path':path,'bytes':len(b),'sha256':sha(b),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}


def comparison():
 cn=json.loads((ROOT/PARENTS[0]).read_text());jp=json.loads((ROOT/PARENTS[1]).read_text())
 return {'cn20_crafting':{'parent_schema':cn['schema'],'source_region':'EARLY_CN_OPERATOR_HOSTED_GUIDE',
  'shared_native_village_recipe_or_item_ids_verified':False,'cn_skill_price_is_jp_sale_price':False,
  'cn_partial_categories_complete_jp_recipes':False,'cn_recipe_gaps_remain_open':True},
  'jp_treasure':{'parent_schema':jp['schema'],'separate_event':'トレジャーハント大作戦！',
   'crystal_collection_and_light_spirit_actor_backfilled':False,'trade_or_repeat_rules_backfilled':False,
   'old_official_detail_availability_is_current_event_page':False},
  'modern_adoption_decided':False,'free_to_play_footer_backfilled_to_september_2005':False}


def catalog(ex):
 rows=[('challenge','quests','DOCUMENTARY_NAMED_COOKING_CHALLENGE',ex['challenge'],['S1']),
  ('gourmet-role','npcs','DOCUMENTARY_EVENT_ROLE_NPC_STATUS_UNVERIFIED',
   {'name':'グルメマスター','place':'CHATROOM','npc_or_gm_controller':None,'original_id':None},['S1']),
  ('full-course','items','DOCUMENTARY_CHALLENGE_REWARD',{'name':'石器時代フルコース','condition':ex['challenge']['condition'],'effect':None},['S1']),
  ('sale','tutorials','DOCUMENTARY_TIMED_SHOP_INGREDIENT_SALE',ex['sale'],['S1']),
  ('lessons','tutorials','DOCUMENTARY_GM_LESSON_SCHEDULE',ex['lessons'],['S1']),
  ('contest','tutorials','DOCUMENTARY_WEBSITE_CONTEST',ex['contest'],['S1']),
  ('gavi','pets','DOCUMENTARY_CONTEST_PET_PRIZE_NOT_SPECIES_MASTER',ex['contest']['best_prize'],['S1']),
  ('pen','items','DOCUMENTARY_CONTEST_EQUIPMENT_NAMING_PRIZE',ex['contest']['honorable_mentions'][0],['S1']),
  ('meal','items','DOCUMENTARY_CONTEST_CAPTURE_MEAL_PRIZE',ex['contest']['honorable_mentions'][1],['S1']),
  ('halloween','tutorials','DOCUMENTARY_PROVISIONAL_TRANSFORMATION_EVENT',ex['halloween'],['S1']),
  ('illustration','screens','DOCUMENTARY_ILLUSTRATION_NOT_GAME_SCREEN',{'image':IMAGE,'observation':VISUAL},['S1','I1'])]
 return [{'record_id':'JP2005-R80-'+ident,'entity_type':kind,'collection':coll,'version_profile':PROFILE,
  'source_refs':refs,'verification_status':'JOURNALISTIC_SCHEDULE_OR_ILLUSTRATION_NOT_RUNTIME',
  'rights_status':'RESEARCH_METADATA_NOT_RELEASE_APPROVED','record_revision':1,'game_ids':None,'content':content}
  for ident,coll,kind,content,refs in rows]


def semantic(ex):return {k:v for k,v in ex.items() if k not in ('section_fingerprints','core_fingerprint')}


def validate(r):
 require(r['schema']=='stoneage.jp2005_autumn_cooking.source.r1' and r['version_profile']==PROFILE,'Version/schema changed')
 require(r['source']==SOURCE and r['image']==IMAGE and r['visual_observation']==VISUAL and r['negative_boundaries']==BOUNDARIES,'Intake/authority/visual boundaries changed')
 require(r['parent_pins']==[pin(p) for p in PARENTS] and r['parser_pin']==pin(PARSER),'Parent/parser original bytes changed')
 require(r['comparison']==comparison(),'Cross-region/event rules backfilled')
 # Exact semantic contract is deliberately separate from source fingerprints.
 require(semantic(r['extraction'])==r['semantic_contract'] and sha(json.dumps(r['semantic_contract'],ensure_ascii=False,sort_keys=True).encode())=='c1b2d1f9804d705de45cd74072d55be2584feaa81bf7e53b2193d51adefad1c7','Extracted semantic contract changed')
 ex=r['extraction']
 require(ex['challenge']['role_controller_npc_or_gm'] is None and ex['challenge']['reward_effect'] is None and ex['challenge']['recipes_quantities_turnin_consumption_repeatability'] is None,'Unreported quest rules promoted')
 require(ex['challenge']['reward']=='石器時代フルコース' and ex['challenge']['condition']=='COMPLETE_ALL_DISHES_SPECIFIED_BY_GOURMET_MASTER','Challenge reward/condition detached')
 require(ex['contest']['venue']=='OFFICIAL_WEBSITE' and ex['contest']['best_prize']['name']=='ガーヴィ' and ex['contest']['best_prize']['verified_world_instance_count'] is None,'Contest/uniqueness promoted')
 require(ex['contest']['best_prize']['stats_growth_skills_habitat_native_id'] is None and ex['contest']['winner_count_each_winner_gets_both_and_actual_award'] is None and ex['contest']['honorable_mentions'][1]['formula_duration_guarantee'] is None,'Pet/prize execution or formula invented')
 require(ex['sale']['goods']=='ALL_FOOD_INGREDIENTS_SOLD_THERE' and ex['sale']['shops']=='CONVENIENCE_STORES_OF_THESE_TWO_VILLAGES' and ex['sale']['base_prices_currency_rounding_inventory_transactions'] is None,'Sale scope promoted')
 require(ex['lessons']['actual_recipes_and_gm_names'] is None and [v['server'] for v in ex['lessons']['sessions']]==['火星サーバー','水星サーバー'],'Lesson recipe/server scope promoted')
 require(ex['halloween']['provisional_title'] is True and ex['halloween']['item_names_forms_duration_spawn_algorithm_and_drop_rules'] is None,'Provisional event/drop rules changed')
 require(ex['timezone'] is None and ex['actual_execution_verified'] is False and ex['exact_client_build'] is None and ex['original_event_npc_item_pet_recipe_ids'] is None,'Historical/runtime unknowns promoted')
 require(r['catalog_records']==catalog(ex),'Catalog semantics detached')
 contract=json.loads((ROOT/PARENTS[-1]).read_text())['future_website']
 require(len(r['catalog_records'])==11 and len({v['record_id'] for v in r['catalog_records']})==11,'Record identity/count changed')
 require(all(set(contract['record_contract']['required']).issubset(v) and v['collection'] in contract['required_collections'] for v in r['catalog_records']),'Archive record contract incomplete')


MUTATIONS=[('料理をすべて完成','料理を一つ完成'),('新アイテム「石器時代フルコース」','新アイテム「秋の満腹セット」'),
 ('全サーバーチャットルームよりスタート','火星サーバーチャットルームよりスタート'),('チャットルームにグルメマスターが現れる','村にグルメマスターが現れる'),
 ('10月4日～10月11日','10月5日～10月11日'),('コンビニで売られている食材がすべて半額','コンビニで売られている商品がすべて半額'),
 ('食材がすべて半額','食材がすべて倍額'),('ジャジャ村およびマリナスの漁村','ジャジャ村のみ'),
 ('14:00～14:30','14:00～15:30'),('火星サーバー','全サーバー'),('水星サーバー','火星サーバー'),
 ('マリナス漁村のコンビニ','ジャジャ村のコンビニ'),('料理のレシピをレクチャー','料理のレシピを販売'),
 ('10月4日～10月18日','10月4日～10月28日'),('公式サイト上','チャットルーム'),('川柳を募集する','俳句を募集する'),
 ('最優秀作：</SPAN>ペット恐竜「ガーヴィ」','佳作：</SPAN>ペット恐竜「ガーヴィ」'),('「ガーヴィ」','「別の恐竜」'),
 ('世界に1匹','世界に10匹'),('自作の合成装備','すべての装備'),('名前を付けられる','能力を増やせる'),
 ('捕獲率が大幅にアップ','戦闘力が大幅にアップ'),('10月29日','10月30日'),('21:00～22:00','21:00～23:00'),
 ('ハロウィンイベント（仮称）','ハロウィンイベント'),('GMがさまざまな場所に出現','モンスターがさまざまな場所に出現'),
 ('アイテム（お菓子）などを配布','アイテム（お菓子）などを販売')]


def audit(raw,expected):
 text=raw.decode('cp932');target=semantic(expected)
 for old,new in MUTATIONS:
  require(old in text,'Missing real semantic mutation: '+old)
  try:actual=derive(text.replace(old,new).encode('cp932'))
  except (ValueError,IndexError):continue
  require(semantic(actual)!=target,'Meaning changed but fingerprint alone detected it: '+old)
 require(derive(raw+b'<script>outside=1</script>')==expected,'Peripheral script changed meaning')
 old='グルメマスターの指定する料理をすべて完成させると'
 for replacement in ('','<script>'+old+'</script>'):
  changed=text.replace(old,replacement)+'<div>'+old+'</div>'
  try:derive(changed.encode('cp932'))
  except ValueError:pass
  else:raise ValueError('Hidden/outside-body text repaired missing claim')
 return {'semantic_mutations_without_all_fingerprints':len(MUTATIONS),'hidden_and_outside_article_counterexamples':2,'outside_script_positive':True}


def inspect_image(raw):
 with Image.open(io.BytesIO(raw)) as im:
  im.load();actual={'bytes':len(raw),'sha256':sha(raw),'size':list(im.size),'format':im.format,'mode':im.mode,'frames':getattr(im,'n_frames',1)}
 require(all(IMAGE[k]==v for k,v in actual.items()),'Reviewed illustration bytes/full decode changed')


def replay(inputs,r):
 validate(r);ex=derive(inputs['S1']);require(ex==r['extraction'],'Source extraction/fingerprint changed');inspect_image(inputs['I1'])
 require(len(inputs['S1'])==SOURCE['bytes'] and sha(inputs['S1'])==SOURCE['sha256'],'Current original body bytes changed')
 return {'schema':'stoneage.jp2005_autumn_cooking.replay.r1',
  'inputs':[{'id':k,'url':URL if k=='S1' else IMAGE_URL,'bytes':len(v),'sha256':sha(v)} for k,v in inputs.items()],
  'extraction':ex,'image':IMAGE,'visual_observation':VISUAL,'comparison':comparison(),'catalog_records':catalog(ex),
  'audit':audit(inputs['S1'],ex),'original_html_or_assets_in_output':False,'original_server_runtime_verified':False}


def read_inputs(directory=None):
 result={}
 for key,url in [('S1',URL),('I1',IMAGE_URL)]:
  if directory:result[key]=(Path(directory)/(key+('.html' if key=='S1' else '.jpg'))).read_bytes()
  else:
   with urllib.request.urlopen(url,timeout=50) as h:
    require(h.status==200 and h.url==url,'Exact URL/status changed');result[key]=h.read()
 return result


def main():
 p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--fetch',action='store_true');g.add_argument('--input-dir');p.add_argument('--output',required=True);a=p.parse_args()
 r=json.loads(REPORT.read_text());out=replay(read_inputs(a.input_dir),r)
 path=Path(a.output);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print('R80 five autumn schedules replayed; recipes, NPC controller and server reward execution remain unknown.')


if __name__=='__main__':main()
