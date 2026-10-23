"""R89: publisher-reprinted 2000 creation counts and credited title-screen photograph."""
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
STEM='STONEAGE-TW2000-LAUNCH-AVATAR-PHOTO'
REPORT=ROOT/f'research/recovered/{STEM}-SOURCE-R1.json'
URL='https://time.udn.com/udntime/story/122835/7095433'
PROFILE='TW2000_REPRINTED_REPORT_AND_CREDITED_PHOTO_IN_2023_EXACT_BUILD_UNKNOWN'
PARSER='tools/stoneage_jp2005_treasure_source.py'
PARENTS=['research/recovered/STONEAGE-TW10-LOGIN-AVATAR-CATALOG-R1.json',
 'research/recovered/STONEAGE-CN20-CREATION-STATUS-SOURCE-R1.json',
 'research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json']
TITLE='元祖級Online Game！ 2000年上線的「石器時代」'
SOURCE={'url':URL,'http_status':200,'no_redirect':True,'initial_intake_bytes':137674,
 'initial_intake_sha256':'44553c4e5c981b8d28534bf250a32f60496d116b84cc42b14071be441682b238',
 'encoding':'UTF8_STRICT','visible_title':TITLE,'visible_reprint_publication':'2023-04-13 13:22','publisher':'報時光／聯合報系',
 'quoted_report_title':'網路電玩石器時代上線了','quoted_date_as_printed':'2000-04-11','quoted_newspaper':'民生報',
 'quoted_edition':'37版','quoted_section':'3C新聞網','original_reporter_not_named_in_quote':True,
 'photo_credit_date_as_printed':'2000/02/10','photo_credit_photographer':'林信昌',
 'authority':'PUBLISHER_REPRINT_WITH_EXPLICIT_QUOTED_NEWSPAPER_AND_ARCHIVE_PHOTO_CREDIT_NOT_ORIGINAL_SCAN',
 'original_2000_paper_scan_acquired':False,'original_2000_digital_photo_master_acquired':False,
 'current_bytes_authenticate_2000_original':False,'official_operator_authorship_verified':False,'exact_client_build':None,
 'full_wrapper_identity_policy':'RETAIN_EACH_ACTUAL_INPUT_HASH_ALLOW_ONLY_OUTSIDE_SELECTED_CORE_DRIFT'}
IMAGES=[{'id': 'I1', 'url': 'https://pgw.udn.com.tw/gw/photo.php?u=https://uc.udn.com.tw/photo/2023/04/13/0/21173547.jpg&s=Y&x=0&y=0&sw=1280&sh=720&sl=W&fw=800&exp=3600', 'http_status': 200, 'no_redirect': True, 'bytes': 109235, 'sha256': '7477d5b56427520ede444b5d8f8baa105373a4d004efa2420782ff6e3de11ddc', 'format': 'JPEG', 'mode': 'RGB', 'size': [800, 450], 'frames': 1}]
VISUAL=[{'id':'I1','manual_visual_review':True,'kind':'PUBLISHER_CREDITED_EARLY_TITLE_OR_MENU_DISPLAY_PHOTOGRAPH',
 'visible_scene':['PERSON_AT_KEYBOARD','CRT_MONITOR','STONEAGE_WORDMARK','PALE_GREEN_PINK_DECORATIVE_SCREEN','CENTRAL_VERTICAL_MENU_LIKE_PANEL'],
 'visible_modern_watermark':'報時光','button_text_or_account_fields_readable':False,'exact_login_launcher_or_title_state':None,
 'native_screenshot_pixel_coordinates_or_resolution_verified':False,'button_interaction_audio_or_server_login_verified':False,
 '48_avatar_choices_visible':False,'native_avatar_names_ids_or_animation_verified':False,'historical_2000_pixels_authenticated':False,
 'transformation':'CURRENT_PGW_PROXY_CROP_RESIZE_REQUEST_800_WIDE_WITH_CURRENT_WATERMARK',
 'caption_credit_is_actual_2000_file_authentication':False}]
BOUNDARIES={k:False for k in ('reprint_date_is_original_2000_publication','credited_photo_date_is_newspaper_report_date',
 'original_paper_scan_or_photo_master_acquired','current_bytes_authenticate_2000_original','official_operator_authorship_verified',
 'four_times_forty_eight_means_192_avatars','forty_eight_means_verified_12_models_times_4_colors','complete_avatar_names_or_native_ids_known',
 'reported_counts_fill_tw10_native_selector_or_cn20_counts','photograph_is_direct_client_screenshot_or_full_login_flow',
 'photo_proxy_dimensions_are_native_resolution','modern_watermark_is_present_in_2000_client',
 'quoted_yesterday_means_exact_server_launch_day','reprint_outer_riding_statement_proves_launch_2000_riding',
 'outer_per_session_payment_claim_is_quoted_2000_pricing','defeat_report_is_complete_death_or_loyalty_formula',
 'wrapper_drift_means_selected_quote_can_change','full_html_hash_is_silently_rewritten_to_match_ci',
 'original_html_or_assets_committed','stage_b_started')}
COUNT='共有4種顏色與48種不同造型可供選擇'
CLAUSES=['2000-04-11/民生報/37版/3C新聞網','華義國際昨日發表一款來自日本的網路遊戲「石器時代」',
 'WGS網路遊戲收費系統','以發售預付卡再扣點數的方式收費','不同於一般收取月費的方式',
 '每位玩家都可自己設定人物',COUNT,'即使打輸了也不會喪命','降低對你的忠誠度']


def article(raw):
 p=VisibleMarkup();p.feed(raw.decode('utf-8',errors='strict'));text=''.join(p.parts)
 area=one(r'<article class="article">(.*?)<div id="story_end"',text,re.S)
 require(plain(one(r'<h1 id="story_art_title" class="story_art_title">(.*?)</h1>',area,re.S))==plain(TITLE),'Reprint title changed')
 publication=plain(one(r'<div id="story_bady_info" class="story_bady_info_author">(.*?)</div>',area,re.S))
 require(publication==plain('2023-04-13 13:22報時光'),'Reprint publication changed')
 quote=one(r'<blockquote class="article-blockquote article-blockquote__1">(.*?)</blockquote>',area,re.S)
 core=plain(quote);require(core.startswith('網路電玩石器時代上線了') and core.endswith('降低對你的忠誠度。'),'Quoted report boundaries changed')
 figure=one(r'<figure class="photo_center">(.*?)</figure>',area,re.S)
 image_src=one(r'<img src="([^"]+)"',figure)
 require(image_src==IMAGES[0]['url'],'Actual proxy photograph detached')
 caption=plain(one(r'<figcaption>(.*?)</figcaption>',figure,re.S))
 require('圖／聯合報系資料照（2000/02/10林信昌攝影）' in caption,'Independent photo credit changed')
 require('華義國際今年3月底將推出' in caption,'Photo caption planned announcement changed')
 # Discard retrospective paragraphs, recommendation lists, ads and scripts.
 return core,caption


def derive(raw):
 core,caption=article(raw);require(all(plain(v) in core for v in CLAUSES),'Quoted count, source or scoped claim changed')
 colors,appearances=map(int,one(r'共有(\d+)種顏色與(\d+)種不同造型可供選擇',core))
 return {'quoted_report':{'date_as_written':'2000-04-11','newspaper':'民生報','edition':'37版','section':'3C新聞網',
   'reported_announcement':'YESTERDAY_PRESENTED_GAME_FROM_JAPAN','exact_server_launch_day_inferred':None,
   'original_scan_or_original_typography_verified':False},
  'character_selection':{'reported_color_count':colors,'reported_different_appearance_count':appearances,
   'relationship_between_two_counts':'AS_WRITTEN_NOT_DETERMINED_AS_CARTESIAN_PRODUCT_OR_TOTAL_VARIANT_FACTORIZATION',
   'computed_192_or_12_base_models':None,'original_names_ids_selector_values_or_complete_roster':None,
   'same_exact_build_as_preserved_tw10_client_or_cn20_guide':False},
  'defeat_claim':{'scope':'SIMPLIFIED_NEWCOMER_NEWSPAPER_DESCRIPTION_AS_REPRINTED','does_not_die_as_reported':True,
   'pet_loyalty_reduction_described':True,'hp_zero_injury_revive_exact_penalty_or_condition_formula':None,
   'tested_original_server_behavior':False},
  'payment_claim':{'scope':'ONLY_QUOTED_REPORT_NOT_OUTER_2023_RETROSPECTIVE','system_as_written':'WGS',
   'mechanism_as_reported':'PREPAID_CARD_POINTS_DEDUCTED_CONTRASTED_WITH_ORDINARY_MONTHLY_FEE',
   'per_minute_or_per_session_unit_prices_and_all_titles_equal_cost':None},
  'photo_context':{'credit_date_as_written':'2000/02/10','photographer_as_written':'林信昌',
   'photo_date_is_quoted_report_date':False,'caption_relative_announcement':'THIS_YEAR_LATE_MARCH_PLANNED',
   'exact_game_state_or_original_file_date_verified':False,'photograph_is_direct_screenshot':False,
   'proxy_native_source_parameter':'https://uc.udn.com.tw/photo/2023/04/13/0/21173547.jpg',
   'direct_source_request_status_at_intake':403,'direct_master_bytes_acquired':False},
  'excluded_outer_claims':['2000_LAUNCH_RIDING_AS_RETROSPECTIVE_GENERALIZATION','PAY_PER_SESSION_NOT_TIME_AS_OUTER_RETROSPECTIVE','2008_CLOSURE_AND_CAUSES'],
  'exact_client_build':None,'original_server_runtime_verified':False,
  'fingerprints':{k:{'characters':len(v),'utf8_bytes':len(v.encode()),'sha256':sha(v.encode())} for k,v in [('quoted_report',core),('photo_caption',caption)]}}


def pin(path):
 b=(ROOT/path).read_bytes();return {'path':path,'bytes':len(b),'sha256':sha(b),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}


def comparison():
 tw=json.loads((ROOT/PARENTS[0]).read_text());cn=json.loads((ROOT/PARENTS[1]).read_text())
 require(tw['original_character_count'] is None and tw['original_screen_layout_verified'] is False,'TW10 native unknowns changed')
 require(cn['boundaries']['character_type_or_color_counts'] is None,'CN20 missing counts changed')
 return {'tw10':{'schema':tw['schema'],'original_character_count_remains_null':True,'native_13_create_field_values_or_layout_filled':False},
  'cn20':{'schema':cn['schema'],'type_or_color_counts_remain_unknown':True,'counts_backfilled_from_tw_report':False},
  'reprint_and_photo_are_independent_same_build_witnesses':False,'modern_adoption_decided':False}


def catalog(ex):
 rows=[('appearance-counts','characters','DOCUMENTARY_REPORTED_SELECTION_COUNTS_NOT_AVATAR_ROSTER',ex['character_selection'],['S1']),
 ('defeat','tutorials','DOCUMENTARY_SIMPLIFIED_DEFEAT_DESCRIPTION',ex['defeat_claim'],['S1']),
 ('payment','tutorials','DOCUMENTARY_PREPAID_WGS_DESCRIPTION',ex['payment_claim'],['S1']),
 ('title-photo','screens','DOCUMENTARY_CREDITED_PHOTOGRAPH_NOT_NATIVE_SCREENSHOT',{'context':ex['photo_context'],'image':IMAGES[0],'observation':VISUAL[0]},['S1','I1'])]
 return [{'record_id':'TW2000-R89-'+i,'entity_type':t,'collection':coll,'version_profile':PROFILE,'source_refs':refs,
  'verification_status':'PUBLISHER_REPRINT_OR_CREDITED_PHOTOGRAPH_NOT_ORIGINAL_CLIENT_TRACE','rights_status':'RESEARCH_METADATA_NOT_RELEASE_APPROVED',
  'record_revision':1,'game_ids':None,'content':v} for i,coll,t,v,refs in rows]


def semantic(ex):return {k:v for k,v in ex.items() if k!='fingerprints'}
SEMANTIC_SHA='808e9749784edf61b4efca4da6364a99722b7eb9e5a8ece42f84476422ebccc8'


def validate(r):
 require(r['schema']=='stoneage.tw2000_launch_avatar_photo.source.r1' and r['version_profile']==PROFILE,'Version/schema changed')
 require(r['source']==SOURCE and r['images']==IMAGES and r['visual_observations']==VISUAL and r['negative_boundaries']==BOUNDARIES,'Source/visual/authority boundaries changed')
 require(r['parent_pins']==[pin(p) for p in PARENTS] and r['parser_pin']==pin(PARSER),'Parent/parser bytes changed')
 require(r['comparison']==comparison(),'Native-versus-reprint distinction changed')
 require(sha(json.dumps(semantic(r['extraction']),ensure_ascii=False,sort_keys=True).encode())==SEMANTIC_SHA,'Quoted report contract changed')
 require(r['catalog_records']==catalog(r['extraction']),'Catalog detached')
 c=json.loads((ROOT/PARENTS[-1]).read_text())['future_website'];require(len(r['catalog_records'])==4 and len({v['record_id'] for v in r['catalog_records']})==4,'Four documentary rows required')
 require(all(set(c['record_contract']['required']).issubset(v) and v['collection'] in c['required_collections'] for v in r['catalog_records']),'Archive fields changed')

MUTATIONS=[('今年3月底將推出','今年4月底將推出'),('2000-04-11/民生報','2000-04-12/民生報'),('民生報/37版','聯合報/37版'),('37版/3C 新聞網','38版/3C 新聞網'),
 ('昨日發表一款','本日發表一款'),('來自日本的網路遊戲','來自台灣的網路遊戲'),('WGS網路遊戲收費系統','MONTHLY網路遊戲收費系統'),
 ('以發售預付卡再扣點數','以收取月費不扣點數'),('不同於一般收取月費','採用一般收取月費'),
 ('4種顏色','5種顏色'),('48種不同造型','192種不同造型'),('每位玩家都可自己設定人物','只能選定同一人物'),
 ('即使打輸了也不會喪命','即使打輸了也會喪命'),('降低對你的忠誠度','提高對你的忠誠度'),
 ('2000/02/10 林信昌攝影','2000/04/11 林信昌攝影'),('2000/02/10 林信昌攝影','2000/02/10 別人攝影')]


def audit(raw,expected):
 text=raw.decode('utf-8');target=semantic(expected)
 for old,new in MUTATIONS:
  require(old in text,'Missing real source mutation: '+old)
  try:actual=derive(text.replace(old,new).encode())
  except (ValueError,IndexError):continue
  require(semantic(actual)!=target,'Only fingerprint detected meaning change: '+old)
 require(derive(raw+b'<script>outside=1</script>')==expected,'Outside wrapper drift affected selected core')
 require(derive(text.replace('而計算費用方式採計次而非計時','而計算費用方式外文被改寫').encode())==expected,'Outer retrospective leaked into quoted source')
 for replacement in ('','<script>'+COUNT+'</script>'):
  changed=text.replace(COUNT,replacement)+'<div>'+COUNT+'</div>'
  try:derive(changed.encode())
  except ValueError:pass
  else:raise ValueError('Hidden/outside quotation repaired missing appearance counts')
 return {'semantic_mutations_without_all_fingerprints':len(MUTATIONS),'hidden_and_outside_article_counterexamples':2,'outside_script_positive':True,'outside_retrospective_positive':True}


def inspect_images(inputs):
 for expected in IMAGES:
  raw=inputs[expected['id']]
  with Image.open(io.BytesIO(raw)) as im:
   im.load();actual={'bytes':len(raw),'sha256':sha(raw),'size':list(im.size),'format':im.format,'mode':im.mode,'frames':getattr(im,'n_frames',1)}
  require(all(expected[k]==v for k,v in actual.items()),'Reviewed illustration bytes/full decode changed')


def replay(inputs,r):
 validate(r);ex=derive(inputs['S1']);require(ex==r['extraction'],'Selected quoted report/caption changed');inspect_images(inputs)
 same=len(inputs['S1'])==SOURCE['initial_intake_bytes'] and sha(inputs['S1'])==SOURCE['initial_intake_sha256']
 return {'schema':'stoneage.tw2000_launch_avatar_photo.replay.r1','inputs':[{'id':k,'url':URL if k=='S1' else next(v['url'] for v in IMAGES if v['id']==k),'bytes':len(v),'sha256':sha(v)} for k,v in inputs.items()],
  'source_identity':{'full_html_equals_initial_intake':same,'selected_quote_and_caption_equal_initial':True,'current_wrapper_change_is_original_2000_authentication':False},
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


def verify_custody(root=None):
 root=ROOT if root is None else Path(root)
 receipt=json.loads((root/f'research/recovered/{STEM}-CUSTODY-R1.json').read_text())
 require(receipt['schema']=='stoneage.tw2000_launch_avatar_photo.custody.r1','Custody schema')
 require(receipt['content_commit']=='6c753de234e5fe173b1f312839e272101d6dbb88' and receipt['content_tree']=='8d7cfe602786543d9d534cd41231d7e2f69baafc','Content Git identity')
 require(receipt['candidate_branch']=='agent/named-content-r89-launch-avatar-photo-20261023','Candidate branch')
 require(receipt['server_execution_verified'] is False and receipt['current_bytes_authenticate_2000_original'] is False and receipt['original_2000_paper_scan_acquired'] is False,'Custody authority promoted')
 require(all(receipt[k] is False for k in ('reported_counts_fill_native_roster','photo_is_direct_screenshot','outer_riding_is_launch_rule')),'Screenshot, navigation or pet-master coverage promoted')
 paths=[f'research/recovered/{STEM}-SOURCE-R1.json']+PARENTS+[PARSER]+[f'research/recovered/{STEM}-CI-{role}-R1.json' for role in ('CANDIDATE','MAIN')]
 pins=receipt['permanent_pins'];require(sha(json.dumps(pins,sort_keys=True).encode())=='6782658ea9e36e926b86464686f984010c371c60b579272ef5c2008b2f41cb10','Original seven-pin identity list replaced');require([p['path'] for p in pins]==paths,'Seven mandatory permanent evidence pins changed')
 for p in pins:
  b=(root/p['path']).read_bytes()
  require(p=={'path':p['path'],'bytes':len(b),'sha256':sha(b),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()},'Permanent original bytes changed')
 source=json.loads((root/paths[0]).read_text())
 initial=[{'id':'S1','url':URL,'bytes':source['source']['initial_intake_bytes'],'sha256':source['source']['initial_intake_sha256']}]+[{k:v[k] for k in ('id','url','bytes','sha256')} for v in source['images']]
 require(receipt['initial_inputs']==initial,'Original intake/input dates lost')
 runs=receipt['runs'];require(len(runs)==21 and len({v['id'] for v in runs})==21,'Actual gate inventory missing/duplicated')
 require(sha(json.dumps(sorted(runs,key=lambda v:v['id']),sort_keys=True).encode())=='4634c8fa9bfcebf63b8ee07f2a4e2c8306d106f2ffdd3207b6d7e06e61ee408a','Actual immutable run inventory changed')
 branches={'candidate':receipt['candidate_branch'],'main':'main'}
 for role,count in (('candidate',10),('main',11)):
  group=[v for v in runs if v['branch']==branches[role]]
  require(len(group)==count and len({v['name'] for v in group})==count,'Branch gate inventory changed')
 require(all(v['head']==receipt['content_commit'] and v['status']=='completed' and v['conclusion']=='success' for v in runs),'Unverified/failed gate promoted')
 raw_files=[];jobs=[];artifacts=[]
 for role,branch in branches.items():
  proof=receipt['jobs_and_artifacts'][role];artifact=proof['artifact'];run=artifact['workflow_run']
  expected={'candidate': (39940945771, 120371931887, 12495304253), 'main': (39941078117, 120372368259, 12496250941)}[role]
  require((proof['run'],proof['job'],artifact['id'])==expected,'Verified run/job/artifact identity changed')
  require(run['id']==proof['run'] and run['head_sha']==receipt['content_commit'] and run['head_branch']==branch,'Artifact origin detached')
  matching=[v for v in runs if v['id']==proof['run']]
  require(len(matching)==1 and matching[0]['branch']==branch and matching[0]['name']=='Verify TW2000 quoted avatar counts and credited title photo','Wrong source workflow')
  require(proof['job_name']=='bounded-source-replay' and proof['job_conclusion']=='success' and artifact['name']=='tw2000-launch-avatar-photo-derived-r89','Wrong job/artifact')
  require(proof['zip_downloaded_and_digest_verified'] is True and artifact['size_in_bytes']>0 and re.fullmatch(r'sha256:[0-9a-f]{64}',artifact['digest']),'ZIP custody missing')
  require((artifact['size_in_bytes'],artifact['digest'])=={'candidate': (3184, 'sha256:ee3f97d59bc297b6058a843e68bd55a9448bb85b4af703a9d231c4142363f77d'), 'main': (3184, 'sha256:a2ba935c6afe0751204efd4bb766ce83eb61060ca3e2226d51bc28ae38aba6db')}[role],'Actual ZIP byte identity changed')
  jobs.append(proof['job']);artifacts.append(artifact['id'])
  path=f'research/recovered/{STEM}-CI-{role.upper()}-R1.json';raw=(root/path).read_bytes();raw_files.append(raw);replayed=json.loads(raw)
  require(replayed['schema']=='stoneage.tw2000_launch_avatar_photo.replay.r1' and len(replayed['inputs'])==2 and replayed['inputs'][0]['id']=='S1' and replayed['inputs'][0]['url']==URL and replayed['inputs'][0]['bytes']>0 and re.fullmatch(r'[0-9a-f]{64}',replayed['inputs'][0]['sha256']) and replayed['inputs'][1]==initial[1],'Actual wrapper/image input identity changed')
  require(replayed['source_identity']=={'full_html_equals_initial_intake':replayed['inputs'][0]==initial[0],'selected_quote_and_caption_equal_initial':True,'current_wrapper_change_is_original_2000_authentication':False},'Wrapper equality or historical authority misreported')
  record=receipt['raw_replays'][role];p=next(v for v in pins if v['path']==path)
  require(all(record[k]==p[k] for k in p) and record['inputs']==replayed['inputs'] and record['equals_initial_inputs']==(replayed['inputs']==initial),'Raw identity/input equality misreported')
  require(all(replayed[k]==source[k] for k in ('extraction','images','visual_observations','comparison','catalog_records')),'Raw replay semantics detached')
  require(replayed['audit']=={'semantic_mutations_without_all_fingerprints':16,'hidden_and_outside_article_counterexamples':2,'outside_script_positive':True,'outside_retrospective_positive':True} and replayed['original_html_or_assets_in_output'] is False and replayed['original_server_runtime_verified'] is False,'Raw audit/authority promoted')
 require(len(set(jobs))==len(set(artifacts))==2 and receipt['candidate_main_raw_bytes_equal']==(raw_files[0]==raw_files[1]),'Candidate/main evidence substituted')
 return receipt


def main():
 p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--fetch',action='store_true');g.add_argument('--input-dir');p.add_argument('--output',required=True);a=p.parse_args()
 r=json.loads(REPORT.read_text());out=replay(read_inputs(a.input_dir),r)
 verify_custody()
 path=Path(a.output);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print('R89 reprinted 4/48 counts and credited early title photo replayed; native roster and login runtime remain unknown.')


if __name__=='__main__':main()
