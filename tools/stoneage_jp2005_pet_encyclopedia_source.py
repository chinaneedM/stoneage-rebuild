"""R87: reported pet-encyclopedia name registration and staged JP2005 rollout."""
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
STEM='STONEAGE-JP2005-PET-ENCYCLOPEDIA'
REPORT=ROOT/f'research/recovered/{STEM}-SOURCE-R1.json'
URL='https://www.4gamer.net/news/history/2005.07/20050705162235detail.html'
PROFILE='JP_PC_2005_GAIAX_PET_ENCYCLOPEDIA_REPORTED_20050705_EXACT_BUILD_UNKNOWN'
PARSER='tools/stoneage_jp2005_treasure_source.py'
PARENTS=['research/recovered/STONEAGE-CN20-OPERATION-UI-SOURCE-R1.json',
 'research/recovered/STONEAGE-JP-OFFICIAL-PET-CATALOG-R1.json',
 'research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json']
TITLE='ガイアックス，「ストーンエイジ」で新ペット恐竜を実装'
SOURCE={'url':URL,'http_status':200,'no_redirect':True,'bytes':17834,
 'sha256':'983b11f84dd9c492c4b868bc96921fecbbb582e87a6243c322c9f8ad684f06b9',
 'encoding':'SHIFT_JIS_STRICT','visible_title':TITLE,'visible_publication':'2005/07/05 16:22',
 'author_as_signed':'TET','operator_as_reported':'ガイアックス',
 'authority':'CONTEMPORANEOUS_JOURNALISM_NOT_VERBATIM_OPERATOR_RELEASE',
 'explicit_verbatim_manufacturer_release':False,'actual_operator_update_page_acquired':False,
 'current_bytes_authenticate_2005_original':False,'exact_client_build':None}
IMAGES=[{'id':'I1','url':'https://www.4gamer.net/news/image/2005.07/20050705162235_0.jpg',
 'http_status':200,'no_redirect':True,'bytes':3371,'sha256':'81a547ca33684426e6c9b42fcace9850e543955b379d49487d2da6d276383394',
 'format':'JPEG','mode':'RGB','size':[96,104],'frames':1}]
VISUAL=[{'id':'I1','manual_visual_review':True,'kind':'SMALL_UNCAPTIONED_CREATURE_ILLUSTRATION_NOT_UI_SCREEN',
 'visible_shape':'PALE_BLUE_ARMORED_CRABLIKE_CREATURE_ON_BLACK_BACKGROUND',
 'pet_name_text_visible':False,'encyclopedia_window_visible':False,'native_species_or_original_sprite_assigned':False,
 'registration_or_capture_interaction_observed':False,'historical_2005_pixels_authenticated':False}]
BOUNDARIES={k:False for k in ('direct_operator_update_source_acquired','current_bytes_authenticate_2005_original',
 'schedule_proves_patch_deployment_or_gm_event_execution','exact_client_build_verified','july5_graphics_prove_july5_live_spawns',
 'july12_first_ever_level_one_dinosaur_anywhere','placement_change_means_all_spawns_changed',
 'onscreen_name_registration_requires_capture_or_ownership','registered_name_means_stats_skills_or_obtained_pet',
 'gm_showcase_is_only_possible_registration_trigger','rule_generalized_to_all_old_pets_or_all_versions',
 'registration_persistence_duplicate_or_storage_format_verified','one_image_means_one_new_species_total',
 'image_proves_named_species_or_encyclopedia_layout','original_sprite_animation_model_verified',
 'cn20_owned_pet_album_is_same_registration_rule','website_catalog_is_ingame_encyclopedia',
 'stoneage2_pal_book_rules_backfilled','modern_footer_free_to_play_backfilled_to_july2005',
 'original_html_or_assets_committed','stage_b_started')}
TRIGGER='画面上に新ペットが表示されると，ペット図鑑にその新ペット恐竜の名前が登録される'
CLAUSES=['ガイアックスはMMORPG','本日（7月5日）および7月12日（火）の定期メンテナンス終了後',
 'まず7月5日に配布されるパッチでは，新ペット恐竜と，それに伴う同種のフィールドモンスターのグラフィックスの実装，そしてペット図鑑の拡張',
 '7月12日に配布されるパッチで，これまで未出現だったLv.1の恐竜（フィールドモンスター）が実装される',
 '一部の恐竜の配置が変更される','実際にゲーム内に新しい恐竜が登場するのは，7月12日のパッチ配布後',
 'アップデートが二回にわけて施される','7月12日の22時前後には，GMが新ペット恐竜のお披露目をする予定',TRIGGER,
 '新ペットの名前を知りたい人は，GMを探すといいだろう']


def article(raw):
 p=VisibleMarkup();p.feed(raw.decode('shift_jis',errors='strict'));text=''.join(p.parts)
 title=one(r'<!--↓大見出し-->(.*?)<!--↑大見出し-->',text,re.S)
 require(plain(one(r'<h5>(.*?)</h5>',title,re.S))==TITLE,'Visible title changed')
 require(plain(one(r'<div class="news_txt1">(.*?)</div>',text,re.S))==plain(SOURCE['visible_publication']),'Publication changed')
 area=one(r'<td class="newstext">(.*?)<!-- tDialy:END -->',text,re.S)
 blocks=[b for b in re.findall(r'<!-- 本文開始 -->(.*?)<!-- 本文終了 -->',area,re.S) if plain(b)]
 require(len(blocks)==1,'One nonempty visible body required')
 core=plain(blocks[0]);require(core.startswith('ガイアックスはMMORPG') and core.endswith('（TET）'),'Signed article boundaries changed')
 linked=re.findall(r'<IMG SRC="(/news/image/2005\.07/20050705162235_0\.jpg)" WIDTH=(\d+) HEIGHT=(\d+)',area)
 require(linked==[('/news/image/2005.07/20050705162235_0.jpg','96','104')],'Actual image path/dimensions detached')
 return core


def derive(raw):
 c=article(raw);require(all(plain(v) in c for v in CLAUSES),'Patch phase, scope or registration trigger changed')
 return {'rollout':{'year_context':2005,'maintenance_relation':'AFTER_REGULAR_MAINTENANCE_ON_EACH_DATE',
   'stages':[
    {'date_month_day':'07-05','scope':['NEW_PET_GRAPHICS','SAME_KIND_FIELD_MONSTER_GRAPHICS','PET_ENCYCLOPEDIA_EXPANSION'],
     'new_creatures_live_in_world_on_this_stage':False},
    {'date_month_day':'07-12','scope':['PREVIOUSLY_UNAPPEARING_LEVEL_ONE_FIELD_DINOSAURS','SOME_DINOSAUR_PLACEMENTS_CHANGED','ACTUAL_NEW_CREATURE_APPEARANCE_AFTER_PATCH'],
     'reported_new_field_level':1,'specific_names_counts_locations_coordinates_and_spawn_rates':None}],
   'patch_distribution_and_world_activation_are_distinct':True,'actual_deployment_verified':False,'exact_patch_files_build_or_maintenance_times':None},
  'encyclopedia':{'source_label':'ペット図鑑','reported_scope':'NEW_PETS_DESCRIBED_IN_THIS_UPDATE',
   'reported_trigger':'NEW_PET_DISPLAYED_ON_SCREEN','reported_result':'THAT_NEW_PET_NAME_REGISTERED',
   'capture_or_ownership_required_by_this_sentence':False,'all_possible_conditions_or_exclusions_known':False,
   'registered_stats_skills_images_or_pet_ownership_proven':False,'applies_to_all_old_pets_or_other_versions':None,
   'exact_button_layout_input_action_persistence_duplicates_or_storage_format':None,'actual_ui_interaction_verified':False},
  'gm_showcase':{'planned_date_month_day':'07-12','approximate_hour':22,'exact_minute_or_timezone':None,
   'status_as_reported':'PLANNED','purpose_as_reported':'SHOW_NEW_PET_DINOSAURS','guide_advice':'FIND_GM_TO_LEARN_NEW_PET_NAMES',
   'only_gm_pets_can_register':None,'actual_showcase_execution_verified':False},
  'new_pet_identity':{'species_names_original_ids_stats_growth_skills_and_sprite_binding':None,'number_of_new_species':None,
   'one_illustration_proves_one_new_species':False},
  'image_link':{'actual_path':'/news/image/2005.07/20050705162235_0.jpg','html_dimensions':[96,104],
   'caption_as_written':'','unlinked_big_image_guessed_or_acquired':False,'named_pet_or_ui_binding':None},
  'exact_client_build':None,'original_server_runtime_verified':False,
  'core_fingerprint':{'characters':len(c),'utf8_bytes':len(c.encode()),'sha256':sha(c.encode())}}


def pin(path):
 b=(ROOT/path).read_bytes();return {'path':path,'bytes':len(b),'sha256':sha(b),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}


def comparison():
 return {'cn20_album':{'schema':json.loads((ROOT/PARENTS[0]).read_text())['schema'],
   'described_scope':'OWNED_PETS_CAN_BE_PHOTOGRAPHED','same_registration_trigger_as_jp2005':False,'cn20_scope_backfilled':False},
  'jp_official_website_pet_catalog':{'schema':json.loads((ROOT/PARENTS[1]).read_text())['schema'],
   'is_same_as_ingame_encyclopedia':False,'web_names_numbers_bind_this_illustration':False},
  'stoneage2_pal_book_or_later_fan_du_database_backfilled':False,'modern_adoption_decided':False}


def catalog(ex):
 rows=[('stage-'+str(i),'tutorials','DOCUMENTARY_PATCH_STAGE',v,['S1']) for i,v in enumerate(ex['rollout']['stages'])]
 rows += [('encyclopedia','tutorials','DOCUMENTARY_INGAME_NAME_REGISTRATION_RULE',ex['encyclopedia'],['S1']),
 ('showcase','tutorials','DOCUMENTARY_PLANNED_GM_SHOWCASE',ex['gm_showcase'],['S1']),
 ('illustration','screens','DOCUMENTARY_UNNAMED_CREATURE_ILLUSTRATION',{'image':IMAGES[0],'observation':VISUAL[0]},['S1','I1'])]
 return [{'record_id':'JP2005-R87-'+i,'entity_type':t,'collection':coll,'version_profile':PROFILE,'source_refs':refs,
  'verification_status':'CONTEMPORANEOUS_REPORT_OR_ILLUSTRATION_NOT_UI_RUNTIME','rights_status':'RESEARCH_METADATA_NOT_RELEASE_APPROVED',
  'record_revision':1,'game_ids':None,'content':v} for i,coll,t,v,refs in rows]


def semantic(ex):return {k:v for k,v in ex.items() if k!='core_fingerprint'}
SEMANTIC_SHA='a55c3c102c1fecc0006fe18b4f20e3d730e9559ab8d32fc1c8a0991a12041165'


def validate(r):
 require(r['schema']=='stoneage.jp2005_pet_encyclopedia.source.r1' and r['version_profile']==PROFILE,'Version/schema changed')
 require(r['source']==SOURCE and r['images']==IMAGES and r['visual_observations']==VISUAL and r['negative_boundaries']==BOUNDARIES,'Source/visual/authority boundaries changed')
 require(r['parent_pins']==[pin(p) for p in PARENTS] and r['parser_pin']==pin(PARSER),'Parent/parser bytes changed')
 require(r['comparison']==comparison(),'Cross-version distinction changed')
 require(sha(json.dumps(semantic(r['extraction']),ensure_ascii=False,sort_keys=True).encode())==SEMANTIC_SHA,'Documentary UI contract changed')
 require(r['catalog_records']==catalog(r['extraction']),'Catalog detached')
 c=json.loads((ROOT/PARENTS[-1]).read_text())['future_website']
 require(len(r['catalog_records'])==5 and len({v['record_id'] for v in r['catalog_records']})==5,'Five documentary rows required')
 require(all(set(c['record_contract']['required']).issubset(v) and v['collection'] in c['required_collections'] for v in r['catalog_records']),'Archive fields changed')

MUTATIONS=[('ガイアックス</A>はMMORPG','ボーステック</A>はMMORPG'),('本日（7月5日）','本日（7月6日）'),
 ('7月12日（火）の定期','7月13日（水）の定期'),('定期メンテナンス終了後','定期メンテナンス開始前'),
 ('まず7月5日に配布','まず7月6日に配布'),('同種のフィールドモンスター','別種のフィールドモンスター'),
 ('グラフィックスの実装','野外への配置'),('ペット図鑑の拡張','ペット図鑑の削除'),
 ('7月12日に配布されるパッチで','7月5日に配布されるパッチで'),('これまで未出現だった','既に出現していた'),
 ('Lv.1の恐竜','Lv.10の恐竜'),('一部の恐竜の配置','すべての恐竜の配置'),
 ('7月12日のパッチ配布後','7月5日のパッチ配布後'),('二回にわけて','一回のみで'),
 ('7月12日の22時前後','7月12日の21時ちょうど'),('お披露目をする予定','お披露目を完了した'),
 ('画面上に新ペットが表示されると','新ペットを捕獲すると'),('新ペット恐竜の名前が登録','新ペット恐竜の全能力が登録'),
 ('GMを探すといいだろう','ペットショップを探すといいだろう')]


def audit(raw,expected):
 text=raw.decode('shift_jis');target=semantic(expected)
 for old,new in MUTATIONS:
  require(old in text,'Missing real source mutation: '+old)
  try:actual=derive(text.replace(old,new).encode('shift_jis'))
  except (ValueError,IndexError):continue
  require(semantic(actual)!=target,'Only fingerprint detected meaning change: '+old)
 require(derive(raw+b'<script>outside=1</script>')==expected,'Peripheral script changed meaning')
 for replacement in ('','<script>'+TRIGGER+'</script>'):
  changed=text.replace(TRIGGER,replacement)+'<div>'+TRIGGER+'</div>'
  try:derive(changed.encode('shift_jis'))
  except ValueError:pass
  else:raise ValueError('Hidden/outside body repaired missing registration trigger')
 return {'semantic_mutations_without_all_fingerprints':len(MUTATIONS),'hidden_and_outside_article_counterexamples':2,'outside_script_positive':True}


def inspect_images(inputs):
 for expected in IMAGES:
  raw=inputs[expected['id']]
  with Image.open(io.BytesIO(raw)) as im:
   im.load();actual={'bytes':len(raw),'sha256':sha(raw),'size':list(im.size),'format':im.format,'mode':im.mode,'frames':getattr(im,'n_frames',1)}
  require(all(expected[k]==v for k,v in actual.items()),'Reviewed illustration bytes/full decode changed')


def replay(inputs,r):
 validate(r);ex=derive(inputs['S1']);require(ex==r['extraction'],'Current encyclopedia report changed');inspect_images(inputs)
 require(len(inputs['S1'])==SOURCE['bytes'] and sha(inputs['S1'])==SOURCE['sha256'],'Current report bytes changed')
 return {'schema':'stoneage.jp2005_pet_encyclopedia.replay.r1','inputs':[{'id':k,'url':URL if k=='S1' else next(v['url'] for v in IMAGES if v['id']==k),'bytes':len(v),'sha256':sha(v)} for k,v in inputs.items()],
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
 require(receipt['schema']=='stoneage.jp2005_pet_encyclopedia.custody.r1','Custody schema')
 require(receipt['content_commit']=='7c734e08fc53540045063816409484c8133732df' and receipt['content_tree']=='8cc44097da5c022ef12e488ec72156411b1b7e7f','Content Git identity')
 require(receipt['candidate_branch']=='agent/named-content-r87-pet-encyclopedia-20261023','Candidate branch')
 require(receipt['server_execution_verified'] is False and receipt['current_bytes_authenticate_2005_original'] is False and receipt['actual_operator_update_page_acquired'] is False,'Custody authority promoted')
 require(all(receipt[k] is False for k in ('illustration_identifies_species','actual_encyclopedia_interaction_verified','registered_name_means_ownership')),'Screenshot, navigation or pet-master coverage promoted')
 paths=[f'research/recovered/{STEM}-SOURCE-R1.json']+PARENTS+[PARSER]+[f'research/recovered/{STEM}-CI-{role}-R1.json' for role in ('CANDIDATE','MAIN')]
 pins=receipt['permanent_pins'];require(sha(json.dumps(pins,sort_keys=True).encode())=='f887d0b6930a91bd188ba77a46cbf6d0badb6218c867b52d463e891435f732cf','Original seven-pin identity list replaced');require([p['path'] for p in pins]==paths,'Seven mandatory permanent evidence pins changed')
 for p in pins:
  b=(root/p['path']).read_bytes()
  require(p=={'path':p['path'],'bytes':len(b),'sha256':sha(b),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()},'Permanent original bytes changed')
 source=json.loads((root/paths[0]).read_text())
 initial=[{'id':'S1','url':URL,'bytes':source['source']['bytes'],'sha256':source['source']['sha256']}]+[{k:v[k] for k in ('id','url','bytes','sha256')} for v in source['images']]
 require(receipt['initial_inputs']==initial,'Original intake/input dates lost')
 runs=receipt['runs'];require(len(runs)==21 and len({v['id'] for v in runs})==21,'Actual gate inventory missing/duplicated')
 require(sha(json.dumps(sorted(runs,key=lambda v:v['id']),sort_keys=True).encode())=='7e31a3de1e83b1dff86a97da28beb7026bb40e83b5e6b70b1db655e971c2f160','Actual immutable run inventory changed')
 branches={'candidate':receipt['candidate_branch'],'main':'main'}
 for role,count in (('candidate',10),('main',11)):
  group=[v for v in runs if v['branch']==branches[role]]
  require(len(group)==count and len({v['name'] for v in group})==count,'Branch gate inventory changed')
 require(all(v['head']==receipt['content_commit'] and v['status']=='completed' and v['conclusion']=='success' for v in runs),'Unverified/failed gate promoted')
 raw_files=[];jobs=[];artifacts=[]
 for role,branch in branches.items():
  proof=receipt['jobs_and_artifacts'][role];artifact=proof['artifact'];run=artifact['workflow_run']
  expected={'candidate': (39935988520, 120355531891, 12494111171), 'main': (39936177726, 120356148265, 12493847454)}[role]
  require((proof['run'],proof['job'],artifact['id'])==expected,'Verified run/job/artifact identity changed')
  require(run['id']==proof['run'] and run['head_sha']==receipt['content_commit'] and run['head_branch']==branch,'Artifact origin detached')
  matching=[v for v in runs if v['id']==proof['run']]
  require(len(matching)==1 and matching[0]['branch']==branch and matching[0]['name']=='Verify JP2005 pet encyclopedia registration and staged rollout','Wrong source workflow')
  require(proof['job_name']=='bounded-source-replay' and proof['job_conclusion']=='success' and artifact['name']=='jp2005-pet-encyclopedia-derived-r87','Wrong job/artifact')
  require(proof['zip_downloaded_and_digest_verified'] is True and artifact['size_in_bytes']>0 and re.fullmatch(r'sha256:[0-9a-f]{64}',artifact['digest']),'ZIP custody missing')
  require((artifact['size_in_bytes'],artifact['digest'])=={'candidate': (2720, 'sha256:0179f8b274a1003612b70f36cab4355ecd3fb257c7d731fcdf8642c8ed8169a4'), 'main': (2720, 'sha256:d65293c7d90e418f886c28c56698424e73bbc5d4d89c3c1fb8ec65f8f5c3815d')}[role],'Actual ZIP byte identity changed')
  jobs.append(proof['job']);artifacts.append(artifact['id'])
  path=f'research/recovered/{STEM}-CI-{role.upper()}-R1.json';raw=(root/path).read_bytes();raw_files.append(raw);replayed=json.loads(raw)
  record=receipt['raw_replays'][role];p=next(v for v in pins if v['path']==path)
  require(all(record[k]==p[k] for k in p) and record['inputs']==replayed['inputs'] and record['equals_initial_inputs']==(replayed['inputs']==initial),'Raw identity/input equality misreported')
  require(all(replayed[k]==source[k] for k in ('extraction','images','visual_observations','comparison','catalog_records')),'Raw replay semantics detached')
  require(replayed['audit']=={'semantic_mutations_without_all_fingerprints':19,'hidden_and_outside_article_counterexamples':2,'outside_script_positive':True} and replayed['original_html_or_assets_in_output'] is False and replayed['original_server_runtime_verified'] is False,'Raw audit/authority promoted')
 require(len(set(jobs))==len(set(artifacts))==2 and receipt['candidate_main_raw_bytes_equal']==(raw_files[0]==raw_files[1]),'Candidate/main evidence substituted')
 return receipt


def main():
 p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--fetch',action='store_true');g.add_argument('--input-dir');p.add_argument('--output',required=True);a=p.parse_args()
 r=json.loads(REPORT.read_text());out=replay(read_inputs(a.input_dir),r)
 verify_custody()
 path=Path(a.output);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print('R87 reported on-screen name registration and staged pet rollout replayed; runtime and species IDs remain unknown.')


if __name__=='__main__':main()
