"""R85: JP2005 two-stage stamp quest and named pet reward, not event execution."""
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
STEM='STONEAGE-JP2005-GW-STAMP-RALLY'
REPORT=ROOT/f'research/recovered/{STEM}-SOURCE-R1.json'
URL='https://www.4gamer.net/news/history/2005.04/20050415190236detail.html'
PROFILE='JP_PC_2005_GAIAX_GW_STAMP_RALLY_REPORTED_20050415_EXACT_BUILD_UNKNOWN'
PARSER='tools/stoneage_jp2005_treasure_source.py'
PARENTS=['research/recovered/STONEAGE-JSS2001-OFFICIAL-EVENT-VENUE-R1.json',
 'research/recovered/STONEAGE-JP2005-TREASURE-EVENT-SOURCE-R1.json',
 'research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json']
TITLE='「ストーンエイジ」二つのスタンプラリーをゴールデンウィークに開催'
SOURCE={'url':URL,'http_status':200,'no_redirect':True,'bytes':16431,
 'sha256':'4e6c10774e52aba19737ca22cd9899c8c066e0fce49022a8a11c645802549f3a',
 'encoding':'SHIFT_JIS_STRICT','visible_title':TITLE,'visible_publication':'2005/04/15 19:02',
 'author_as_signed':'Seirou','operator_as_reported':'ガイアックス','prior_operator_as_reported':'ボーステック',
 'authority':'CONTEMPORANEOUS_JOURNALISM_NOT_VERBATIM_OPERATOR_RELEASE',
 'explicit_verbatim_manufacturer_release':False,'actual_operator_event_page_acquired':False,
 'current_bytes_authenticate_2005_original':False,'exact_client_build':None}
IMAGES=[{'id': 'I1', 'url': 'https://www.4gamer.net/news/image/2005.04/20050415190236_0big.jpg', 'http_status': 200, 'no_redirect': True, 'bytes': 534047, 'sha256': '455b747ed9f0912672a238101b4e17b5469d40e81cef6ac6cc35e583f544bab6', 'format': 'JPEG', 'mode': 'RGB', 'size': [640, 480], 'frames': 1}]
VISUAL=[{'id':'I1','manual_visual_review':True,'kind':'STATIC_GAME_WORLD_GATHERING_SCREEN',
 'scene':['GRASS','STONE_PATH','BRIDGE_AND_WATER','MULTIPLE_HUMAN_AND_PET_FIGURES'],
 'bottom_navigation_labels':['マップ','ステータス','ペット','アイテム','メール','アルバム','システム'],
 'momotora_identity_or_pink_tiger_assigned':False,'stamp_or_quest_text_visible':False,
 'reward_delivery_or_event_execution_observed':False,'navigation_clicks_or_feature_behavior_verified':False,
 'original_sprite_model_animation_or_client_build_verified':False,'historical_2005_pixels_authenticated':False}]
BOUNDARIES={k:False for k in ('direct_operator_event_source_acquired','current_bytes_authenticate_2005_original',
 'schedule_proves_event_execution','exact_client_build_verified','all_players_means_no_account_or_service_fee',
 'four_villages_are_authenticated_four_starting_villages','four_villages_mean_exactly_four_stamp_items',
 'intermediate_is_a_numeric_level_gate','challenge_requires_only_visiting_not_finishing_first_quest',
 'momotora_is_same_native_species_across_regions','momotora_original_stats_growth_or_sprite_known',
 'unnamed_challenge_item_is_named_or_same_as_pet_reward','treasure_repeat_or_trade_rules_backfilled',
 'screenshot_identifies_momotora_or_stamp_npc','screenshot_proves_reward_delivery',
 'visible_navigation_label_proves_interaction_or_feature_completion','640_480_proves_native_client_resolution',
 'modern_footer_free_to_play_backfilled_to_2005','original_html_or_assets_committed','stage_b_started')}
PREREQUISITE='"チャレンジスタンプラリー"を進めるには，"お楽しみスタンプラリー"をクリアする必要がある'


def article(raw):
 p=VisibleMarkup();p.feed(raw.decode('shift_jis',errors='strict'));text=''.join(p.parts)
 title=one(r'<!--↓大見出し-->(.*?)<!--↑大見出し-->',text,re.S)
 require(plain(one(r'<h5>(.*?)</h5>',title,re.S))==TITLE,'Article title changed')
 require(plain(one(r'<div class="news_txt1">(.*?)</div>',text,re.S))==plain('2005/04/15 19:02'),'Publication changed')
 area=one(r'<td class="newstext">(.*?)<!-- tDialy:END -->',text,re.S)
 blocks=[b for b in re.findall(r'<!-- 本文開始 -->(.*?)<!-- 本文終了 -->',area,re.S) if plain(b)]
 require(len(blocks)==1,'One nonempty visible body required; empty layout slots are not articles')
 core=one(r'^(.*?（Seirou）)',plain(blocks[0]),re.S)
 require(core.startswith('ボーステックから営業譲渡され') and core.endswith('（Seirou）'),'Journalistic boundaries changed')
 pairs=re.findall(r'<A href="([^"]+_0big\.jpg)"[^>]*><IMG SRC="([^"]+_0\.jpg)" WIDTH=(\d+) HEIGHT=(\d+)',area)
 require(pairs==[('/news/image/2005.04/20050415190236_0big.jpg','/news/image/2005.04/20050415190236_0.jpg','180','135')],'Actual full/thumbnail pair changed')
 return core


def derive(raw):
 c=article(raw)
 clauses=['ガイアックスがサービスを提供している','4月28日から5月10日まで',
  'ゴールデンウィークイベント「ストーンエイジ・GWスタンプラリー」が開催される',
  '二つのクエスト','すべてのプレイヤーを対象にした"お楽しみスタンプラリー"',
  '四つの村を巡りスタンプを集めると，ピンク色のトラ型ペット"Lv1ペットモモトラ"がもらえる',
  '中級以上のプレイヤーを対象にした"チャレンジスタンプラリー"',
  '世界中を巡ってスタンプを集め，クリアするとゴールデンウィーク限定アイテムがもらえる',PREREQUISITE]
 require(all(plain(v) in c for v in clauses),'Source quest, scope, reward or prerequisite clause changed')
 return {'event':{'name':'ストーンエイジ・GWスタンプラリー','year_context':2005,
   'window_month_day':['04-28','05-10'],'exact_hours_maintenance_or_timezone':None,
   'status_at_publication':'FORWARD_LOOKING_JOURNALISTIC_ANNOUNCEMENT','actual_event_execution_verified':False,
   'server_scope_or_account_payment_requirements':None},
  'quests':[
   {'name':'お楽しみスタンプラリー','audience_as_reported':'ALL_PLAYERS','route_as_reported':'VISIT_FOUR_UNNAMED_VILLAGES_AND_COLLECT_STAMPS',
    'village_count':4,'named_villages_order_coordinates_npcs_or_map_ids':None,
    'stamp_count_item_identity_consumption_and_storage':None,'completion_reward_label':'Lv1ペット モモトラ',
    'prerequisite_not_mentioned_in_article':True,'no_possible_prerequisites_in_original_server_proven':False},
   {'name':'チャレンジスタンプラリー','audience_as_reported':'INTERMEDIATE_AND_ABOVE','numeric_level_requirement':None,
    'route_as_reported':'TRAVEL_WORLD_AND_COLLECT_STAMPS','concrete_maps_order_npcs_and_stamp_count':None,
    'progress_prerequisite':'COMPLETE_OTANOSHIMI_STAMP_RALLY','prerequisite_scope':'PROGRESS_CHALLENGE_NOT_AUTOMATIC_REWARD_OR_START',
    'completion_reward_kind':'UNNAMED_GOLDEN_WEEK_LIMITED_ITEM','reward_name_quantity_effect_and_original_id':None}],
  'pet_reward':{'name_as_written':'モモトラ','reward_label_as_written':'Lv1ペット モモトラ','reported_level':1,
   'color_as_reported':'ピンク色','shape_as_reported':'トラ型','acquisition_as_reported':'COMPLETE_OTANOSHIMI_STAMP_RALLY',
   'grant_quantity_repeatability_or_per_account_limit':None,'wild_habitat_or_capture_eligibility':None,
   'stats_growth_skills_elements_native_id_or_original_sprite':None,'cross_region_alias_or_same_native_species':None},
  'repeatability_reset_and_server_quest_flags':None,'exact_client_build':None,'original_server_runtime_verified':False,
  'image_link':{'actual_full_path':'/news/image/2005.04/20050415190236_0big.jpg',
   'actual_thumbnail_path':'/news/image/2005.04/20050415190236_0.jpg','thumbnail_html_dimensions':[180,135],
   'full_image_selected':True,'thumbnail_acquired':False,'caption_as_written':'','screenshot_named_pet_binding':None},
  'core_fingerprint':{'characters':len(c),'utf8_bytes':len(c.encode()),'sha256':sha(c.encode())}}


def pin(path):
 b=(ROOT/path).read_bytes();return {'path':path,'bytes':len(b),'sha256':sha(b),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}


def comparison():
 jss=json.loads((ROOT/PARENTS[0]).read_text());treasure=json.loads((ROOT/PARENTS[1]).read_text())
 return {'jss2001_venues':{'schema':jss['schema'],'four_venue_villages_are_gw_four_villages':False,
  'old_reception_npcs_coordinates_or_direction_backfilled':False},
  'jp2005_treasure':{'schema':treasure['schema'],'same_collection_event_or_reward':False,
   'light_spirit_npc_crystal_drop_trade_repeatability_backfilled':False},
  'chinese_tiger_alias_or_tw10_species_mapping_verified':False,'modern_adoption_decided':False}


def catalog(ex):
 rows=[('event','tutorials','DOCUMENTARY_TIMED_STAMP_EVENT',ex['event'],['S1'])]
 rows += [('quest-'+str(i),'quests','DOCUMENTARY_ORDERED_STAMP_QUEST',q,['S1']) for i,q in enumerate(ex['quests'])]
 rows += [('momotora','pets','DOCUMENTARY_NAMED_LEVEL_ONE_PET_REWARD_NOT_MASTER',ex['pet_reward'],['S1']),
  ('limited-item','items','DOCUMENTARY_UNNAMED_CHALLENGE_REWARD',{'kind':ex['quests'][1]['completion_reward_kind'],'name_quantity_effect_id':None},['S1']),
  ('world-screen','screens','DOCUMENTARY_UNCAPTIONED_GAME_SCREEN_WITH_VISIBLE_NAVIGATION',{'image':IMAGES[0],'observation':VISUAL[0]},['S1','I1'])]
 return [{'record_id':'JP2005-R85-'+ident,'entity_type':kind,'collection':coll,'version_profile':PROFILE,'source_refs':refs,
  'verification_status':'CONTEMPORANEOUS_REPORT_OR_STATIC_SCREEN_NOT_EVENT_RUNTIME','rights_status':'RESEARCH_METADATA_NOT_RELEASE_APPROVED',
  'record_revision':1,'game_ids':None,'content':content} for ident,coll,kind,content,refs in rows]


def semantic(ex):return {k:v for k,v in ex.items() if k!='core_fingerprint'}
SEMANTIC_SHA='8fc96fd943974072cf2b75b5ebf446949e95d2988150ac68c2e9db24f2dea973'


def validate(r):
 require(r['schema']=='stoneage.jp2005_gw_stamp.source.r1' and r['version_profile']==PROFILE,'Version/schema changed')
 require(r['source']==SOURCE and r['images']==IMAGES and r['visual_observations']==VISUAL and r['negative_boundaries']==BOUNDARIES,'Source/visual/authority boundaries changed')
 require(r['parent_pins']==[pin(p) for p in PARENTS] and r['parser_pin']==pin(PARSER),'Parent/parser bytes changed')
 require(r['comparison']==comparison(),'Cross-source distinctions changed')
 require(sha(json.dumps(semantic(r['extraction']),ensure_ascii=False,sort_keys=True).encode())==SEMANTIC_SHA,'Documentary quest/pet contract changed')
 require(r['catalog_records']==catalog(r['extraction']),'Catalog detached')
 c=json.loads((ROOT/PARENTS[-1]).read_text())['future_website']
 require(len(r['catalog_records'])==6 and len({v['record_id'] for v in r['catalog_records']})==6,'Catalog count/identity changed')
 require(all(set(c['record_contract']['required']).issubset(v) and v['collection'] in c['required_collections'] for v in r['catalog_records']),'Archive required fields changed')


MUTATIONS=[('4月28日から5月10日','4月29日から5月10日'),('5月10日まで','5月11日まで'),
 ('ガイアックス</A>がサービス','ボーステック</A>がサービス'),('二つのクエスト','一つのクエスト'),
 ('すべてのプレイヤーを対象','一部のプレイヤーを対象'),('四つの村を巡り','三つの村を巡り'),
 ('ピンク色のトラ型','黄色のトラ型'),('トラ型ペット','竜型ペット'),('Lv1ペット モモトラ','Lv10ペット モモトラ'),
 ('モモトラ','別のペット'),('中級以上のプレイヤー','レベル60以上のプレイヤー'),('世界中を巡って','一つの村で'),
 ('ゴールデンウィーク限定アイテム','モモトラ'),('クリアする必要がある','訪問する必要がある'),
 ('クリアする必要がある','クリアする必要はない')]


def audit(raw,expected):
 text=raw.decode('shift_jis');target=semantic(expected)
 for old,new in MUTATIONS:
  require(old in text,'Missing real source mutation: '+old)
  try:actual=derive(text.replace(old,new).encode('shift_jis'))
  except (ValueError,IndexError):continue
  require(semantic(actual)!=target,'Meaning changed but only fingerprint detected it: '+old)
 require(derive(raw+b'<script>outside=1</script>')==expected,'Peripheral script changed meaning')
 # The prerequisite is in a single paragraph with no nested markup.
 for replacement in ('','<script>'+PREREQUISITE+'</script>'):
  changed=text.replace(PREREQUISITE,replacement)+'<div>'+PREREQUISITE+'</div>'
  try:derive(changed.encode('shift_jis'))
  except ValueError:pass
  else:raise ValueError('Hidden/outside-body text repaired missing completed-quest prerequisite')
 return {'semantic_mutations_without_all_fingerprints':len(MUTATIONS),'hidden_and_outside_article_counterexamples':2,'outside_script_positive':True}


def inspect_images(inputs):
 for expected in IMAGES:
  raw=inputs[expected['id']]
  with Image.open(io.BytesIO(raw)) as im:
   im.load();actual={'bytes':len(raw),'sha256':sha(raw),'size':list(im.size),'format':im.format,'mode':im.mode,'frames':getattr(im,'n_frames',1)}
  require(all(expected[k]==v for k,v in actual.items()),'Reviewed game screen bytes/full decode changed')


def replay(inputs,r):
 validate(r);ex=derive(inputs['S1']);require(ex==r['extraction'],'Current reported article extraction changed');inspect_images(inputs)
 require(len(inputs['S1'])==SOURCE['bytes'] and sha(inputs['S1'])==SOURCE['sha256'],'Current report bytes changed')
 return {'schema':'stoneage.jp2005_gw_stamp.replay.r1','inputs':[{'id':k,'url':URL if k=='S1' else next(v['url'] for v in IMAGES if v['id']==k),'bytes':len(v),'sha256':sha(v)} for k,v in inputs.items()],
  'extraction':ex,'images':IMAGES,'visual_observations':VISUAL,'comparison':comparison(),'catalog_records':catalog(ex),
  'audit':audit(inputs['S1'],ex),'original_html_or_assets_in_output':False,'original_server_runtime_verified':False}


def read_inputs(directory=None):
 result={}
 for key,url in [('S1',URL)]+[(v['id'],v['url']) for v in IMAGES]:
  if directory:result[key]=(Path(directory)/(key+('.html' if key=='S1' else '.jpg'))).read_bytes()
  else:
   with urllib.request.urlopen(url,timeout=50) as h:
    require(h.status==200 and h.url==url,'Exact article/image URL or status changed');result[key]=h.read()
 return result


def main():
 p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--fetch',action='store_true');g.add_argument('--input-dir');p.add_argument('--output',required=True);a=p.parse_args()
 r=json.loads(REPORT.read_text());out=replay(read_inputs(a.input_dir),r)
 path=Path(a.output);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print('R85 GW quest prerequisite, Momotora reward and unassigned game screen replayed; IDs and event execution remain unknown.')


if __name__=='__main__':main()
