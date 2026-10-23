"""R84: announced TW2002 fusion/egg/hatching stages, not a breeding engine."""
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
STEM='STONEAGE-TW2002-FUSION-HATCHING'
REPORT=ROOT/f'research/recovered/{STEM}-SOURCE-R1.json'
ARTICLE_URL='https://gnn.gamer.com.tw/detail.php?sn=6751'
URL='https://web.archive.org/web/20190821163207id_/https://gnn.gamer.com.tw/detail.php?sn=6751'
PROFILE='TW_MARKET_2002_PET_EVOLUTION_HISTORY_REPORT_CAPTURE_20190821_EXACT_BUILD_UNKNOWN'
PARSER='tools/stoneage_jp2005_treasure_source.py'
PARENTS=['research/recovered/STONEAGE-JP2008-PET-EVOLUTION-SOURCE-R1.json',
 'research/recovered/STONEAGE-TW2002-WEREWOLF-FORMS-SOURCE-R1.json',
 'research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json']
TITLE='許慧欣見證「寵物進化史」'
SOURCE={'url':URL,'original_article_url':ARTICLE_URL,'capture':'20190821163207','http_status':200,'no_redirect':True,
 'bytes':26265,'sha256':'c9bbe57924b5f3e8fa69ee1494d53934b07d7181926ef9b24166688629add7a9',
 'encoding':'UTF8_STRICT','visible_title':TITLE,'visible_publication':'2002-11-14 21:41:11',
 'byline_as_written':'（GNN 記者  報導）','named_reporter':None,'authority':'ARCHIVED_PRESS_REPORT_NOT_DIRECT_OPERATOR_RELEASE',
 'region_qualification':'TAIWAN_MARKET_CONTEXT_INFERRED_NOT_AUTHENTICATED_SERVER_BUILD',
 'current_article_request_status':403,'current_article_body_acquired':False,'current_body_archive_equality_verified':False,
 'availability_requested_timestamp':'20021201','availability_returned_timestamp':'20190821163207',
 'capture_is_publication_or_build':False,'authenticated_2002_original_bytes':False,'official_authorship_verified':False}
IMAGES=[{'id': 'I1', 'url': 'https://p2.bahamut.com.tw/S/2KU/21/0000092621.JPG', 'http_status': 200, 'no_redirect': True, 'bytes': 12389, 'sha256': 'bfa82936606a9207af6484866c20325b5893461233792a13ebdfa02ce56d4b1c', 'format': 'JPEG', 'mode': 'RGB', 'size': [120, 120], 'frames': 1, 'variant': 'ACTUAL_SMALL_S_GALLERY_REFERENCE', 'full_original_acquired': False, 'historical_2002_pixels_authenticated': False}, {'id': 'I2', 'url': 'https://p2.bahamut.com.tw/S/2KU/28/0000092628.JPG', 'http_status': 200, 'no_redirect': True, 'bytes': 12778, 'sha256': '826855871234f9d260ca58511a269d289c36248a6bc1e7433fa87e50ecd5e6f0', 'format': 'JPEG', 'mode': 'RGB', 'size': [120, 120], 'frames': 1, 'variant': 'ACTUAL_SMALL_S_GALLERY_REFERENCE', 'full_original_acquired': False, 'historical_2002_pixels_authenticated': False}]
GALLERY=['https://p2.bahamut.com.tw/S/2KU/21/0000092621.JPG', 'https://p2.bahamut.com.tw/S/2KU/22/0000092622.JPG', 'https://p2.bahamut.com.tw/S/2KU/23/0000092623.JPG', 'https://p2.bahamut.com.tw/S/2KU/24/0000092624.JPG', 'https://p2.bahamut.com.tw/S/2KU/25/0000092625.JPG', 'https://p2.bahamut.com.tw/S/2KU/26/0000092626.JPG', 'https://p2.bahamut.com.tw/S/2KU/27/0000092627.JPG', 'https://p2.bahamut.com.tw/S/2KU/28/0000092628.JPG']
VISUAL=[
 {'id':'I1','manual_visual_review':True,'kind':'SMALL_STAGE_PHOTO_MULTIPLE_PERFORMERS_WITH_SAXOPHONES'},
 {'id':'I2','manual_visual_review':True,'kind':'SMALL_EVENT_PHOTO_PERSON_BETWEEN_COSTUMED_FIGURES'}]
for v in VISUAL:v.update(named_pet_or_third_generation_species_assigned=False,in_game_fusion_or_hatching_observed=False,
 original_sprite_model_or_animation=False,exact_person_identity_from_pixels_alone=False)
BOUNDARIES={k:False for k in ('direct_operator_release_acquired','capture_is_publication_date','original_2002_bytes_authenticated',
 'current_article_body_matches_archive','tw10_jss1999_or_exact_5_0_build_authenticated','third_generation_is_third_filial_generation',
 'three_different_pets_means_three_distinct_species','all_pets_cannot_be_captured_or_quest_rewards',
 'fusion_inputs_consumed_or_success_rate_verified','special_drug_and_feed_are_named_item_master_entries',
 'feed_is_birth_drug_or_known_recipe','jp2008_failure_level1_or_evolution_ticket_backfilled',
 'werewolf_or_two_named_card_beasts_are_fusion_outputs','promotional_future_tense_proves_deployment_date',
 'pet_designer_is_sole_mmo_creator','advertising_song_is_game_bgm_or_event_audio',
 'stage_costume_is_authenticated_pet_model','original_html_or_assets_committed','stage_b_started')}


def article(raw):
 p=VisibleMarkup();p.feed(raw.decode('utf8',errors='strict'));text=''.join(p.parts)
 require(plain(one(r'<h1>(.*?)</h1>',text,re.S))==TITLE,'Visible article title changed')
 require(plain(one(r'<span class="GN-lbox3C">(.*?)</span>',text,re.S))=='（GNN記者報導）2002-11-1421:41:11','Visible byline/publication changed')
 body=one(r'<!-- 新聞內容 -->(.*?)<!-- 新聞內容結束 -->',text,re.S)
 parts=[plain(v) for v in re.split(r'<br\s*/>\s*<br\s*/>',body)];require(len(parts)==4 and all(parts),'Four visible paragraphs required')
 require([v[:7] for v in parts]==['寵物養成的線上','此外華義國際還','從「石器時代-','除了外型和能力'],'Ordered article paragraphs changed')
 gallery=one(r'<!-- 圖片區塊 -->(.*?)<!-- 圖片區塊結束 -->',text,re.S)
 require(re.findall(r'<img src="([^"]+)" name="gnnPIC" title="" alt="">',gallery)==GALLERY,'Eight actual uncaptioned S-gallery references changed')
 require([GALLERY[i] for i in (0,7)]==[v['url'] for v in IMAGES],'Selected first/eighth photo detached')
 return plain(body),parts


ACQUISITION='第三代寵物將無法用捕捉或是任務方式取得'

def derive(raw):
 core,p=article(raw)
 def must(i,*clauses):require(all(plain(c) in p[i] for c in clauses),'Changed fusion/report clause in paragraph '+str(i+1))
 must(0,'「石器時代-寵物進化史」','結合全新的第三代寵物以及寵物融合功能')
 must(1,'許慧欣','來代言「石器時代」','新專輯中的「連接」做為此次「石器時代」廣告的主題曲')
 must(2,'從「石器時代-寵物進化史」開始，將推出嶄新的第三代寵物','透過孵化與飼育的過程',
  '造型奇特','華義國際聘請日本設定畫家柴垣秀樹來設計')
 must(3,'外型和能力技能與前二代的寵物不同',ACQUISITION,'必需透過「融合」才能擁有第三代寵物',
  '使用特殊的藥材將三隻不同的寵物融合成一個寵物蛋','玩家必須細心以特殊飼料來孵化寵物蛋',
  '才能孵育出全新的第三代寵物')
 return {'release':{'name_as_written':'石器時代-寵物進化史','numeric_version_in_body':None,
   'introductory_tense':'EDITORIAL_INTRODUCED_CLAIM','detailed_third_generation_tense':'將推出',
   'exact_deployment_date_or_successful_server_execution':None,'marketing_third_generation_is_filial_generation':False},
  'third_generation':{'category_label':'第三代寵物','named_species_list':None,
   'appearance_ability_skill_difference':'QUALITATIVE_COMPARISON_WITH_PREVIOUS_TWO_GENERATIONS',
   'previous_two_generations_are_two_specific_client_versions':None,
   'capture_or_quest_acquisition_as_reported':False,'restriction_scope':'ANNOUNCED_THIRD_GENERATION_ONLY',
   'native_species_ids_stats_growth_skills':None,'original_model_or_sprite_ids':None},
  'fusion_hatching':{'reported_stage_order':['THREE_DIFFERENT_PETS_WITH_SPECIAL_DRUG','ONE_PET_EGG','SPECIAL_FEED_HATCHING','NEW_THIRD_GENERATION_PET'],
   'input_pet_count':3,'different_pets_phrase':'三隻不同的寵物','distinctness_species_or_individual_criterion':None,
   'input_sex_level_rebirth_or_kinship_requirement':None,'drug_descriptor_as_written':'特殊的藥材',
   'egg_count_as_reported':1,'egg_descriptor_as_written':'寵物蛋','feed_descriptor_as_written':'特殊飼料',
   'drug_or_feed_item_ids_recipe_and_quantity':None,'feeding_interval_hatching_duration_or_offline_clock':None,
   'input_consumption_failure_probability_success_rate_and_retry':None,'offspring_species_selection_inheritance_or_model_composition':None,
   'egg_transfer_inventory_slot_capacity_persistence':None,'original_server_runtime_verified':False},
  'design_credit':{'name_as_reported':'柴垣秀樹','commissioner_as_reported':'華義國際',
   'role_as_reported':'日本設定畫家','credited_scope':'THIRD_GENERATION_PET_APPEARANCE_DESIGN',
   'sole_mmo_creator_or_formula_author_verified':False},
  'advertising_context':{'endorser_name_as_reported':'許慧欣','song_title_as_reported':'連接',
   'song_use_as_reported':'ADVERTISEMENT_THEME_SONG','lyrics_extracted':False,
   'game_bgm_or_fusion_hatching_sound_binding_verified':False,'audio_bytes_acquired':False},
  'timezone_explicit_in_visible_text':None,'region_or_exact_server_build_authenticated':False,
  'original_server_runtime_verified':False,'gallery':{'count':8,'selected_indices_one_based':[1,8],
   'selected_photo_count':2,'unacquired_references':6,'captions_as_written':['']*8,
   'full_originals_acquired':False,'pet_names_or_models_assigned_by_order':False},
  'paragraph_fingerprints':[{'index':i+1,'characters':len(v),'sha256':sha(v.encode())} for i,v in enumerate(p)],
  'core_fingerprint':{'characters':len(core),'utf8_bytes':len(core.encode()),'sha256':sha(core.encode())}}


def pin(path):
 b=(ROOT/path).read_bytes();return {'path':path,'bytes':len(b),'sha256':sha(b),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}


def comparison():
 jp=json.loads((ROOT/PARENTS[0]).read_text());wolf=json.loads((ROOT/PARENTS[1]).read_text())
 return {'jp2008_evolution':{'schema':jp['schema'],'same_mechanism_as_tw2002_fusion':False,
  'four_saber_pet_labels_or_failure_level1_backfilled':False,'evolution_cave_trial_or_paid_ticket_backfilled':False},
  'tw2002_werewolf':{'schema':wolf['schema'],'werewolf_or_card_beasts_are_third_generation_fusion_outputs':False,
   'human_wolf_battle_transition_is_fusion_or_hatching':False,'card_dice_are_fusion_rng':False,
   'same_artist_credit_means_same_native_asset_id':False},
  'later_chronicle_5_0_label_backfilled_to_article':False,'modern_adoption_decided':False}


def catalog(ex):
 rows=[('release','versions','DOCUMENTARY_NAMED_RELEASE_NOT_EXACT_BUILD',ex['release'],['S1']),
  ('category','pets','DOCUMENTARY_UNNAMED_PET_CATEGORY_NOT_SPECIES_MASTER',ex['third_generation'],['S1']),
  ('stages','growth_profiles','DOCUMENTARY_FUSION_EGG_HATCHING_STAGES_NOT_FORMULA',ex['fusion_hatching'],['S1']),
  ('credit-context','tutorials','DOCUMENTARY_DESIGN_CREDIT_AND_ADVERTISING_NOT_GAME_AUDIO',
   {'design_credit':ex['design_credit'],'advertising_context':ex['advertising_context']},['S1'])]
 rows += [(label,'items','DOCUMENTARY_GENERIC_MATERIAL_OR_EGG_NOT_ITEM_MASTER',{'descriptor_as_written':ex['fusion_hatching'][field],
  'category_role':role,'native_id':None,'consumption_quantity':None},['S1']) for label,field,role in
  [('drug','drug_descriptor_as_written','FUSION_MATERIAL'),('egg','egg_descriptor_as_written','INTERMEDIATE_EGG'),('feed','feed_descriptor_as_written','HATCHING_FEED')]]
 rows += [(im['id'],'screens','DOCUMENTARY_SMALL_EVENT_PHOTO_NOT_GAME_SCREEN',{'image':im,'observation':v},['S1',im['id']]) for im,v in zip(IMAGES,VISUAL)]
 return [{'record_id':'TW2002-R84-'+ident,'entity_type':kind,'collection':coll,'version_profile':PROFILE,'source_refs':refs,
  'verification_status':'ARCHIVED_PRESS_ANNOUNCEMENT_OR_CURRENT_SMALL_PHOTO_NOT_RUNTIME','rights_status':'RESEARCH_METADATA_NOT_RELEASE_APPROVED',
  'record_revision':1,'game_ids':None,'content':content} for ident,coll,kind,content,refs in rows]


def semantic(ex):return {k:v for k,v in ex.items() if k not in ('paragraph_fingerprints','core_fingerprint')}
SEMANTIC_SHA='62e6e2fc30e4c7f49fa481b2b2ddff0b83541c329439f17915654519b315a868'


def validate(r):
 require(r['schema']=='stoneage.tw2002_fusion_hatching.source.r1' and r['version_profile']==PROFILE,'Version/schema changed')
 require(r['source']==SOURCE and r['images']==IMAGES and r['visual_observations']==VISUAL and r['negative_boundaries']==BOUNDARIES,'Intake/history/visual/authority boundaries changed')
 require(r['parent_pins']==[pin(p) for p in PARENTS] and r['parser_pin']==pin(PARSER),'Parent/parser bytes changed')
 require(r['comparison']==comparison(),'Cross-region and mechanism distinctions changed')
 require(sha(json.dumps(semantic(r['extraction']),ensure_ascii=False,sort_keys=True).encode())==SEMANTIC_SHA,'Documentary fusion contract changed')
 require(r['catalog_records']==catalog(r['extraction']),'Catalog detached')
 c=json.loads((ROOT/PARENTS[-1]).read_text())['future_website']
 require(len(r['catalog_records'])==9 and len({v['record_id'] for v in r['catalog_records']})==9,'Catalog count/identity changed')
 require(all(set(c['record_contract']['required']).issubset(v) and v['collection'] in c['required_collections'] for v in r['catalog_records']),'Archive required fields changed')


MUTATIONS=[('第三代寵物以及寵物融合功能','第二代寵物以及寵物融合功能'),('將推出嶄新的第三代寵物','已經開放所有第三代寵物'),
 ('孵化與飼育的過程','直接捕捉的過程'),('與前二代的寵物不同','與前二代的寵物相同'),
 ('將無法用捕捉或是任務方式取得','可以用捕捉或是任務方式取得'),('必需透過「融合」','不必透過「融合」'),
 ('三隻不同的寵物','兩隻不同的寵物'),('三隻不同的寵物','三隻相同的寵物'),('融合成一個寵物蛋','融合成兩個寵物蛋'),
 ('使用特殊的藥材','使用一般食物'),('以特殊飼料來孵化','以一般飼料來孵化'),('來孵化寵物蛋','來餵養成年寵物'),
 ('全新的第三代寵物','全新的第二代寵物'),('柴垣秀樹','未具名設計師'),('日本設定畫家','遊戲全程唯一作者'),
 ('華義國際聘請','其他公司聘請'),('「連接」做為','「另一首」做為'),('廣告的主題曲','融合過程的背景音樂'),
 ('許慧欣','另一位代言人')]


def audit(raw,expected):
 text=raw.decode('utf8');target=semantic(expected)
 for old,new in MUTATIONS:
  require(old in text,'Missing real source mutation: '+old)
  try:actual=derive(text.replace(old,new).encode())
  except (ValueError,IndexError):continue
  require(semantic(actual)!=target,'Meaning changed but only fingerprint detected it: '+old)
 require(derive(raw+b'<script>outside=1</script>')==expected,'Peripheral script changed meaning')
 for replacement in ('','<script>'+ACQUISITION+'</script>'):
  changed=text.replace(ACQUISITION,replacement)+'<div>'+ACQUISITION+'</div>'
  try:derive(changed.encode())
  except ValueError:pass
  else:raise ValueError('Hidden/outside-body words repaired missing acquisition restriction')
 return {'semantic_mutations_without_all_fingerprints':len(MUTATIONS),'hidden_and_outside_article_counterexamples':2,'outside_script_positive':True}


def inspect_images(inputs):
 for expected in IMAGES:
  raw=inputs[expected['id']]
  with Image.open(io.BytesIO(raw)) as im:
   im.load();actual={'bytes':len(raw),'sha256':sha(raw),'size':list(im.size),'format':im.format,'mode':im.mode,'frames':getattr(im,'n_frames',1)}
  require(all(expected[k]==v for k,v in actual.items()),'Reviewed small event photo bytes/full decode changed')


def replay(inputs,r):
 validate(r);ex=derive(inputs['S1']);require(ex==r['extraction'],'Archived article extraction changed');inspect_images(inputs)
 require(len(inputs['S1'])==SOURCE['bytes'] and sha(inputs['S1'])==SOURCE['sha256'],'Archived current raw bytes changed')
 return {'schema':'stoneage.tw2002_fusion_hatching.replay.r1','inputs':[{'id':k,'url':URL if k=='S1' else next(v['url'] for v in IMAGES if v['id']==k),'bytes':len(v),'sha256':sha(v)} for k,v in inputs.items()],
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
 print('R84 announced fusion stages and two event photos replayed; species, formulas, build and original server execution remain unknown.')


if __name__=='__main__':main()
