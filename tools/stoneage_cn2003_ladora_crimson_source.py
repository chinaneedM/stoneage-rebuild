"""R86: source-scoped Ladora routes, seven ecology occurrences and island myth."""
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
STEM='STONEAGE-CN2003-LADORA-CRIMSON'
REPORT=ROOT/f'research/recovered/{STEM}-SOURCE-R1.json'
PROFILE='CN_SINA2003_LADORA_CRIMSON_GEOGRAPHY_EXACT_BUILD_UNKNOWN'
URL='https://games.sina.com.cn/zhqu/sta/article/2003-06-09/11645.shtml'
TITLE='《石器时代》任务功略-深红洞窟'
PARSER='tools/stoneage_jp2005_treasure_source.py'
PARENTS=['research/recovered/STONEAGE-CN2003-QIANG-EN-FAMILY-SOURCE-R1.json',
 'research/recovered/STONEAGE-CN20-PET-COMMISSION-HABITATS-SOURCE-R1.json',
 'research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json']
SOURCE={'url':URL,'http_status':200,'no_redirect':True,'bytes':59256,
 'sha256':'684983365e929e42d7987e86f962ca2d7641e6185c98464cd4788023909fe3ae',
 'encoding':'GB18030_STRICT','visible_title':TITLE,'visible_publication':'2003-06-09 14:03',
 'publisher_field':'新浪游戏','named_original_author':None,'submission_link_label':'我要投稿',
 'authority':'DATED_PORTAL_GUIDE_NOT_AUTHENTICATED_OPERATOR_SCRIPT','official_authorship_verified':False,
 'current_bytes_authenticate_2003_original':False,'exact_game_build':None,
 'scope':'SELECTED_GEOGRAPHY_ECOLOGY_AND_MYTH_NOT_BOTH_COMPLETE_QUESTS'}
IMAGES=[{'id':'I1','url':'https://image2.sina.com.cn/gm/newgames/0303/images/tuxing0610_03.jpg',
 'http_status':200,'no_redirect':True,'bytes':22812,'sha256':'15f3e751a5828d906815e2b3d514e0d9940e87c52cb2f605789dcd7b2183e9ef',
 'format':'JPEG','mode':'RGB','size':[500,236],'frames':1}]
VISUAL=[{'id':'I1','manual_visual_review':True,'kind':'STATIC_FOUR_ROUTE_SCHEMATIC_NOT_GAME_SCREEN',
 'printed_nodes':[{'label':c,'floor_as_printed':f} for c,f in [('c120302','拉多拉洞窟1楼'),('c120303','拉多拉洞窟2楼'),
 ('c120306','拉多拉洞窟2楼'),('c120305','拉多拉洞窟3楼'),('c120304','拉多拉洞窟3楼'),
 ('c120308','拉多拉洞窟3楼'),('c120307','拉多拉洞窟3楼'),('c120309','拉多拉山顶')]],
 'arrows_as_drawn':[['c120302','c120303'],['c120302','c120306'],['c120303','c120305'],['c120303','c120304'],
 ['c120306','c120308'],['c120306','c120307'],['c120305','c120309'],['c120304','c120309'],['c120308','c120309'],['c120307','c120309']],
 'route_labels_as_printed':['路线一','路线二','路线三','路线四'],
 'one_summit_label_proves_one_native_summit_instance':False,'printed_codes_are_verified_native_map_ids':False,
 'arrow_geometry_or_walkable_tiles_verified':False,'original_client_build_or_historical_pixels_authenticated':False}]
BOUNDARIES={k:False for k in ('official_authorship_verified','current_bytes_authenticate_2003_original',
 'all_article_quests_recovered','water_jug_reward_table_recovered','recommended_80_is_universal_map_gate',
 'adult_ceremony_is_universal_map_gate','paired_coordinates_are_rectangle_or_entry_exit',
 'four_entrances_mapped_one_to_one_to_route_numbers','directed_routes_have_verified_reverse_edges',
 'duplicate_map_names_are_one_or_different_native_instances','gruxi_and_gruxisi_are_verified_aliases',
 'enemy_labels_are_capturable_pet_master','enemy_ranges_are_native_spawn_configuration','volcano_story_is_geological_simulation',
 'phoenix_description_is_observed_runtime_or_original_pet_template','diagram_codes_are_verified_native_map_ids',
 'shared_summit_code_overrides_text_four_summits','other_guide_prerequisites_backfilled',
 'original_html_or_assets_committed','stage_b_started')}
CLAUSES=['建议等级80级','特殊要求：解过成人仪式','交通工具：步行或骑宠',
 '吉鲁岛是由石头与火山所构成的岛屿','整座吉鲁岛将瞬间沉没于大海里','火山已经有百余年未曾爆发过',
 '火之女神“伊拉”','有了火之女神的祈祷','达那村（东499，南167）（东511，南152）',
 '“拉特拉的守门人”（东200，南38）','四条路线分别通往四座不同的山顶',
 '只要被玩家找到，不死鸟会立即飞到另一座山顶','建议玩家以注销的方式赶紧换个星系',
 '不死鸟是以奇宝的形体现身且站在草席上','不死鸟面前会有一只奇宝护卫']
ANCHOR='只要被玩家找到，不死鸟会立即飞到另一座山顶'


def selected(raw):
 p=VisibleMarkup();p.feed(raw.decode('gb18030',errors='strict'));text=''.join(p.parts)
 middle=one(r'<!-- include 中间内容 begin -->(.*?)<!-- include 中间内容 end -->',text,re.S)
 require(TITLE in plain(middle),'Visible title changed')
 require(plain(one(r'<!-- include 发布时间 begin -->(.*?)<!-- include 发布时间 end -->',middle,re.S))==plain(SOURCE['visible_publication']),'Publication changed')
 require('作者：新浪游戏' in plain(middle) and '我要投稿' in plain(middle),'Publisher field changed')
 body=one(r'<td width=500 class=l15z><span>(.*?)</td>\s*</tr>\s*</table>\s*<br><br>',middle,re.S)
 intro=one(r'^(.*?)<p>　　深红洞窟（二）——口渴的多洛加</p>',body,re.S)
 # Stop before reward/combat sections, retaining only geography and myth paragraphs.
 intro=one(r'^(.*?不死鸟！</font></p>)',intro,re.S)
 eco=one(r'<p>　　7\. 拉多拉的回廊(.*?)$',body,re.S)
 require('http://image2.sina.com.cn/gm/newgames/0303/images/tuxing0610_03.jpg' in eco,'Actual selected image link changed')
 return plain(intro),plain('拉多拉的回廊'+eco)


def coords(text):return [[int(x),int(y)] for x,y in re.findall(r'（东(\d+)，南(\d+)）',text)]


def derive(raw):
 intro,eco=selected(raw)
 require(all(plain(v) in intro for v in CLAUSES),'Selected geography/myth qualification changed')
 route_text=one(r'四条路线分别通往四座不同的山顶：(.*?)◆',intro,re.S)
 routes=[]
 for label,section in re.findall(r'路线([一二三四])(.*?)(?=路线[一二三四]|$)',route_text):
  edges=[{'from_floor':a,'to_floor':b,'source_floor_local_coord':[int(x),int(y)]} for a,b,x,y in
   re.findall(r'([123])楼通往([23顶])楼的洞口（东(\d+)，南(\d+)）',section)]
  require([v['from_floor']+v['to_floor'] for v in edges]==['12','23','3顶'],'Three directed floor edges required')
  routes.append({'label':'路线'+label,'directed_edges':edges})
 require(len(routes)==4,'Four ordered source routes required')
 # Occurrence-scoped table grammar; repeated names do not merge rows.
 names='拉多拉的回廊|拉多拉洞窟|北吉鲁山岭|巴那姆的洞窟|深红的洞窟'
 pattern=r'('+names+r')((?:“[^”]+”内)?坐标：.*?)怪物等级：(\d+)~(\d+)级怪物种类：(.*?)(?=(?:'+names+r')|北吉鲁山岭地下1楼|$)'
 occurrences=[]
 for i,(name,location,lo,hi,enemies) in enumerate(re.findall(pattern,eco)):
  frame=one(r'^“([^”]+)”内坐标',location) if location.startswith('“') else 'WORLD_COORDINATES_AS_PRINTED'
  occurrences.append({'occurrence_id':'E'+str(i+1),'name_as_written':name,'coordinate_frame':frame,
   'coordinate_literals':coords(location),'coordinate_roles':None,'monster_levels_as_reported':[int(lo),int(hi)],
   'enemy_labels_as_written':enemies.split('、'),'native_map_id_or_capture_eligibility':None})
 require(len(occurrences)==7 and all(v['coordinate_literals'] for v in occurrences),'Seven nonempty ecology occurrences required')
 return {'geography_occurrences':occurrences,'four_routes':routes,
  'route_entry_mapping':None,'route_reversal_or_walkable_geometry_verified':False,
  'quest_header_context_only':{'recommended_level':80,'hard_map_gate':None,'adult_ceremony_requirement_scope':'ASSOCIATED_QUEST_HEADER_ONLY','transport':['步行','骑宠']},
  'village':{'name':'达那村','coordinate_literals':[[499,167],[511,152]],'coordinate_roles':None},
  'corridor_guard':{'name_as_written':'拉特拉的守门人','corridor_local_coord':[200,38],'same_native_name_as_ladora':None},
  'world_story':{'island':'吉鲁岛','composition_as_told':['石头','火山'],'eruption_consequence_as_told':'WHOLE_ISLAND_SINKS',
   'non_eruption_duration_as_told':'百余年','goddess_name':'伊拉','explanation_as_told':'FIRE_GODDESS_PRAYER','calendar_or_simulation_verified':False},
  'phoenix_context':{'label':'不死鸟','summit_count_as_reported':4,'moves_after_found_as_reported':True,
   'guide_advice':['注销换星系','前往其它山顶'],'display_form_as_written':'奇宝','standing_on':'草席','front_guard_label':'奇宝护卫',
   'observed_runtime_template_or_original_native_pet_id':None},
  'diagram_relationship':{'printed_common_summit_label':'c120309','text_says_four_distinct_summits':True,'native_instance_resolution':None},
  'excluded_scope':['BOTH_COMPLETE_QUESTS','COMBAT_AND_FEATHER_REWARD_STATS','THIRSTY_DUOLUOJIA_WATER_JUG_REWARD_TABLE','OTHER_LINKED_IMAGES'],
  'exact_game_build':None,'original_server_runtime_verified':False,
  'fingerprints':{k:{'characters':len(v),'sha256':sha(v.encode())} for k,v in [('intro',intro),('ecology',eco)]}}


def pin(path):
 b=(ROOT/path).read_bytes();return {'path':path,'bytes':len(b),'sha256':sha(b),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}


def comparison():
 return {'parents':[{'schema':json.loads((ROOT/p).read_text())['schema'],'path':p} for p in PARENTS[:2]],
  'qiang_en_floor_or_adult_ceremony_rules_backfilled':False,'pet_commission_target_means_capturable_ecology':False,
  'different_spelling_or_same_map_label_proves_native_alias':False,'modern_adoption_decided':False}


def catalog(ex):
 rows=[(v['occurrence_id'],'maps','DOCUMENTARY_ECOLOGY_OCCURRENCE',v,['S1']) for v in ex['geography_occurrences']]
 rows += [('routes','maps','DOCUMENTARY_DIRECTED_ROUTE_GROUP',{'routes':ex['four_routes'],'entry_mapping':None},['S1']),
 ('myth','tutorials','DOCUMENTARY_WORLD_STORY_AND_PHOENIX_CONTEXT',{'story':ex['world_story'],'phoenix':ex['phoenix_context']},['S1']),
 ('diagram','screens','DOCUMENTARY_MAP_SCHEMATIC',{'image':IMAGES[0],'observation':VISUAL[0]},['S1','I1'])]
 return [{'record_id':'CN2003-R86-'+i,'entity_type':t,'collection':c,'version_profile':PROFILE,'source_refs':refs,
  'verification_status':'PORTAL_GUIDE_OR_SCHEMATIC_NOT_SERVER_RUNTIME','rights_status':'RESEARCH_METADATA_NOT_RELEASE_APPROVED',
  'record_revision':1,'game_ids':None,'content':v} for i,c,t,v,refs in rows]


def semantic(ex):return {k:v for k,v in ex.items() if k!='fingerprints'}
SEMANTIC_SHA='bc8f38a99710ed3e23979085855bdcb32223d1094e0b1a0b65ce4366ba0649a3'


def validate(r):
 require(r['schema']=='stoneage.cn2003_ladora_crimson.source.r1' and r['version_profile']==PROFILE,'Version/schema changed')
 require(r['source']==SOURCE and r['images']==IMAGES and r['visual_observations']==VISUAL and r['negative_boundaries']==BOUNDARIES,'Source/visual/authority boundaries changed')
 require(r['parent_pins']==[pin(p) for p in PARENTS] and r['parser_pin']==pin(PARSER),'Parent/parser bytes changed')
 require(r['comparison']==comparison(),'Cross-source distinctions changed')
 require(sha(json.dumps(semantic(r['extraction']),ensure_ascii=False,sort_keys=True).encode())==SEMANTIC_SHA,'Documentary geography contract changed')
 require(r['catalog_records']==catalog(r['extraction']),'Catalog detached')
 c=json.loads((ROOT/PARENTS[-1]).read_text())['future_website']
 require(len(r['catalog_records'])==10 and len({v['record_id'] for v in r['catalog_records']})==10,'Catalog count/identity changed')
 require(all(set(c['record_contract']['required']).issubset(v) and v['collection'] in c['required_collections'] for v in r['catalog_records']),'Archive required fields changed')

MUTATIONS=[('建议等级80级','必须等级80级'),('解过成人仪式','无需成人仪式'),('百余年','千余年'),('女神“伊拉”','女神“伊娜”'),
 ('整座吉鲁岛将瞬间沉没','整座吉鲁岛不会沉没'),('东499，南167','东498，南167'),('东200，南38','东201，南38'),
 ('四座不同的山顶','同一座山顶'),('会立即飞到另一座山顶','不会飞到另一座山顶'),('建议玩家以注销','要求玩家以注销'),
 ('奇宝的形体现身','幼年暴龙的形体现身'),('一只奇宝护卫','一只水龙护卫'),
 ('东38，南87','东39，南87'),('东11，南6','东11，南7'),('东44，南75','东44，南76'),
 ('东8，南43','东8，南44'),('东65，南5','东65，南6'),('东64，南87','东63，南87'),
 ('东15，南17','东15，南18'),('东66，南47','东66，南48'),('东34，南59','东34，南60'),('东8，南31','东8，南32'),
 ('1楼通往2楼','2楼通往1楼'),('东421，南577','东422，南577'),('东228，南27','东229，南27'),
 ('东275，南149','东276，南149'),('东295，南259','东296，南259'),('东388，南337','东389，南337'),
 ('东45，南41','东45，南42'),('东26，南5','东26，南6'),('地下2楼”内坐标','地下1楼”内坐标'),
 ('25~30级','25~31级'),('51~59级','51~60级'),('51~56级','51~57级'),('55~58级','55~59级'),('57~75级','57~76级'),
 ('加美、加比','加美、加斯'),('呼拔拔、鲁尼帖斯','呼拔拔、未知'),('加克拉、石龟','加克拉、岩龟'),
 ('多洛加、格鲁西 <br>','多洛加、格鲁西斯 <br>'),('多洛加、格鲁西斯 \n','多洛加、格鲁西 \n')]


def audit(raw,expected):
 text=raw.decode('gb18030');target=semantic(expected)
 for old,new in MUTATIONS:
  require(old in text,'Missing real source mutation: '+old)
  try:actual=derive(text.replace(old,new).encode('gb18030'))
  except (ValueError,IndexError):continue
  require(semantic(actual)!=target,'Meaning changed but only fingerprint detected it: '+old)
 require(derive(raw+b'<script>outside=1</script>')==expected,'Peripheral script changed meaning')
 for replacement in ('','<script>'+ANCHOR+'</script>'):
  changed=text.replace(ANCHOR,replacement)+'<div>'+ANCHOR+'</div>'
  try:derive(changed.encode('gb18030'))
  except ValueError:pass
  else:raise ValueError('Hidden/outside body repaired missing phoenix scope')
 return {'semantic_mutations_without_all_fingerprints':len(MUTATIONS),'hidden_and_outside_article_counterexamples':2,'outside_script_positive':True}


def inspect_images(inputs):
 for expected in IMAGES:
  raw=inputs[expected['id']]
  with Image.open(io.BytesIO(raw)) as im:
   im.load();actual={'bytes':len(raw),'sha256':sha(raw),'size':list(im.size),'format':im.format,'mode':im.mode,'frames':getattr(im,'n_frames',1)}
  require(all(expected[k]==v for k,v in actual.items()),'Reviewed schematic bytes/full decode changed')


def replay(inputs,r):
 validate(r);ex=derive(inputs['S1']);require(ex==r['extraction'],'Current selected geography changed');inspect_images(inputs)
 require(len(inputs['S1'])==SOURCE['bytes'] and sha(inputs['S1'])==SOURCE['sha256'],'Current source bytes changed')
 return {'schema':'stoneage.cn2003_ladora_crimson.replay.r1','inputs':[{'id':k,'url':URL if k=='S1' else next(v['url'] for v in IMAGES if v['id']==k),'bytes':len(v),'sha256':sha(v)} for k,v in inputs.items()],
  'extraction':ex,'images':IMAGES,'visual_observations':VISUAL,'comparison':comparison(),'catalog_records':catalog(ex),
  'audit':audit(inputs['S1'],ex),'original_html_or_assets_in_output':False,'original_server_runtime_verified':False}


def read_inputs(directory=None):
 result={}
 for key,url in [('S1',URL)]+[(v['id'],v['url']) for v in IMAGES]:
  if directory:result[key]=(Path(directory)/(key+('.html' if key=='S1' else '.jpg'))).read_bytes()
  else:
   with urllib.request.urlopen(url,timeout=50) as h:
    require(h.status==200 and h.url==url,'Exact source URL/status changed');result[key]=h.read()
 return result


def verify_custody(root=None):
 root=ROOT if root is None else Path(root)
 receipt=json.loads((root/f'research/recovered/{STEM}-CUSTODY-R1.json').read_text())
 require(receipt['schema']=='stoneage.cn2003_ladora_crimson.custody.r1','Custody schema')
 require(receipt['content_commit']=='3c0b80a38ad7cdfc2604496681020b4a7ad126f0' and receipt['content_tree']=='e4be822c5f6e2e594103d896ca7511deb2b73f72','Content Git identity')
 require(receipt['candidate_branch']=='agent/named-content-r86-ladora-crimson-20261023','Candidate branch')
 require(receipt['server_execution_verified'] is False and receipt['current_bytes_authenticate_2003_original'] is False and receipt['official_authorship_verified'] is False,'Custody authority promoted')
 require(all(receipt[k] is False for k in ('diagram_codes_are_verified_native_map_ids','same_summit_instance_verified','ecology_is_capturable_pet_master')),'Screenshot, navigation or pet-master coverage promoted')
 paths=[f'research/recovered/{STEM}-SOURCE-R1.json']+PARENTS+[PARSER]+[f'research/recovered/{STEM}-CI-{role}-R1.json' for role in ('CANDIDATE','MAIN')]
 pins=receipt['permanent_pins'];require([p['path'] for p in pins]==paths,'Seven mandatory permanent evidence pins changed')
 for p in pins:
  b=(root/p['path']).read_bytes()
  require(p=={'path':p['path'],'bytes':len(b),'sha256':sha(b),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()},'Permanent original bytes changed')
 source=json.loads((root/paths[0]).read_text())
 initial=[{'id':'S1','url':URL,'bytes':source['source']['bytes'],'sha256':source['source']['sha256']}]+[{k:v[k] for k in ('id','url','bytes','sha256')} for v in source['images']]
 require(receipt['initial_inputs']==initial,'Original intake/input dates lost')
 runs=receipt['runs'];require(len(runs)==21 and len({v['id'] for v in runs})==21,'Actual gate inventory missing/duplicated')
 require(sha(json.dumps(sorted(runs,key=lambda v:v['id']),sort_keys=True).encode())=='49502370ba5efe90c9863784290c0ba957043c9b32adff61c78aeaa0f753795d','Actual immutable run inventory changed')
 branches={'candidate':receipt['candidate_branch'],'main':'main'}
 for role,count in (('candidate',10),('main',11)):
  group=[v for v in runs if v['branch']==branches[role]]
  require(len(group)==count and len({v['name'] for v in group})==count,'Branch gate inventory changed')
 require(all(v['head']==receipt['content_commit'] and v['status']=='completed' and v['conclusion']=='success' for v in runs),'Unverified/failed gate promoted')
 raw_files=[];jobs=[];artifacts=[]
 for role,branch in branches.items():
  proof=receipt['jobs_and_artifacts'][role];artifact=proof['artifact'];run=artifact['workflow_run']
  expected={'candidate': (39934221560, 120349672167, 12492434392), 'main': (39934550590, 120350775724, 12492594617)}[role]
  require((proof['run'],proof['job'],artifact['id'])==expected,'Verified run/job/artifact identity changed')
  require(run['id']==proof['run'] and run['head_sha']==receipt['content_commit'] and run['head_branch']==branch,'Artifact origin detached')
  matching=[v for v in runs if v['id']==proof['run']]
  require(len(matching)==1 and matching[0]['branch']==branch and matching[0]['name']=='Verify CN2003 Ladora routes and Crimson ecology','Wrong source workflow')
  require(proof['job_name']=='bounded-source-replay' and proof['job_conclusion']=='success' and artifact['name']=='cn2003-ladora-crimson-derived-r86','Wrong job/artifact')
  require(proof['zip_downloaded_and_digest_verified'] is True and artifact['size_in_bytes']>0 and re.fullmatch(r'sha256:[0-9a-f]{64}',artifact['digest']),'ZIP custody missing')
  require((artifact['size_in_bytes'],artifact['digest'])=={'candidate': (4125, 'sha256:369e57a355b72c5795201f05ec71b9b53d3448259546739879e4c041894ea998'), 'main': (4125, 'sha256:46eea10ea08ed5f94b55df2cb8b2a3b7415ee2a07435863536fede12b767b414')}[role],'Actual ZIP byte identity changed')
  jobs.append(proof['job']);artifacts.append(artifact['id'])
  path=f'research/recovered/{STEM}-CI-{role.upper()}-R1.json';raw=(root/path).read_bytes();raw_files.append(raw);replayed=json.loads(raw)
  record=receipt['raw_replays'][role];p=next(v for v in pins if v['path']==path)
  require(all(record[k]==p[k] for k in p) and record['inputs']==replayed['inputs'] and record['equals_initial_inputs']==(replayed['inputs']==initial),'Raw identity/input equality misreported')
  require(all(replayed[k]==source[k] for k in ('extraction','images','visual_observations','comparison','catalog_records')),'Raw replay semantics detached')
  require(replayed['audit']=={'semantic_mutations_without_all_fingerprints':41,'hidden_and_outside_article_counterexamples':2,'outside_script_positive':True} and replayed['original_html_or_assets_in_output'] is False and replayed['original_server_runtime_verified'] is False,'Raw audit/authority promoted')
 require(len(set(jobs))==len(set(artifacts))==2 and receipt['candidate_main_raw_bytes_equal']==(raw_files[0]==raw_files[1]),'Candidate/main evidence substituted')
 return receipt


def main():
 p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--fetch',action='store_true');g.add_argument('--input-dir');p.add_argument('--output',required=True);a=p.parse_args()
 r=json.loads(REPORT.read_text());out=replay(read_inputs(a.input_dir),r)
 verify_custody()
 path=Path(a.output);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print('R86 four directed routes, seven ecology occurrences and bounded myth replayed; native IDs/runtime remain unknown.')

if __name__=='__main__':main()
