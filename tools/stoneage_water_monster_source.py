"""R77: two water-monster rescue routes, communication shell, ecological motive and scoped rewards."""
import argparse
import hashlib
import io
import json
import re
import urllib.request
from pathlib import Path
from PIL import Image
from tools.stoneage_five_brothers_source import Article, require, sha, compact, one

ROOT=Path(__file__).resolve().parents[1]
STEM='STONEAGE-CN2003-WATER-MONSTER'
REPORT=ROOT/f'research/recovered/{STEM}-SOURCE-R1.json'
PROFILE='CN2003_LABELLED_SINA_EDEN_WATER_MONSTER_GUIDE_EXACT_BUILD_AND_AUTHORSHIP_UNKNOWN'
URLS={'S1':'https://games.sina.com.cn/zhqu/sta/article/2003-06-03/10555.shtml',
 'S2':'https://web.archive.org/web/20160929133108id_/http://games.sina.com.cn:80/zhqu/sta/article/2003-06-03/10555.shtml'}
PARSER='tools/stoneage_five_brothers_source.py'
PARENTS=['research/recovered/STONEAGE-CN2003-LIULI-CAVE-SOURCE-R1.json',
 'research/recovered/STONEAGE-EARLY-CONTENT-GUIDE-MANUAL-R1.json',
 'research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json']
BOUNDARIES={k:False for k in ('official_authorship_verified','capture_2016_is_2003_original_bytes','capture_date_is_publication_or_build',
 'same_build_tw10_membership_verified','original_server_runtime_verified','original_ids_recovered',
 'recommended_level_is_hard_gate','shell_is_proven_entrance_key_or_consumed','three_shell_quests_all_required',
 'bark_party_restriction_applies_to_whole_quest_or_forbids_help','route_b_proves_no_possible_kraken_battle',
 'child_is_reward_pet_or_player_owned_pet','child_spelling_variants_resolved_as_one_original_id',
 'maintenance_wording_proves_quota_reset_or_exact_deadline','frog_dinner_story_is_runtime_feeding_system',
 'ecology_labels_are_complete_capturable_pet_master','html_archive_authenticates_current_image_bytes',
 'original_html_or_assets_committed','stage_b_started')}

class LinkedArticle(Article):
 def __init__(self):super().__init__();self.image_links=[]
 def handle_starttag(self,t,attrs):
  super().handle_starttag(t,attrs);a=dict(attrs)
  if self.active and not self.hidden and t=='a' and re.fullmatch(r'http://image2\.sina\.com\.cn/gm/newgames/0303/images/axiaoshuiguai0603_0\d+\.jpg',a.get('href','')):self.image_links.append(a['href'])


def article(raw):
 text=raw.decode('gb18030',errors='strict');require(re.search(r'charset=["\x27]?gb2312',text,re.I),'Declared charset changed')
 require(compact(one(r'<!-- include 发布时间 begin -->(.*?)<!-- include 发布时间 end -->',text))=='2003-06-0311:57','Visible publication changed')
 p=LinkedArticle();p.feed(text);require(p.roots==1 and p.active is None,'Unique closed visible article required')
 require(compact(''.join(p.visible)).count('《石器时代》任务功略-小水怪事件')==1,'Visible title missing/ambiguous')
 body=compact(''.join(p.parts));require(body.endswith('【我要投稿】【发表查看评论】【进入论坛】'),'Article/footer boundary changed')
 body=body.removesuffix('【我要投稿】【发表查看评论】【进入论坛】')
 require(len(p.image_links)==18 and len(set(p.image_links))==18,'18 ordered original image references required')
 return body,p.image_links


def xy(text):return [[int(a),int(b)] for a,b in re.findall(r'（东(\d+)，南(\d+)）',text)]


def derive(raw):
 body,links=article(raw);head,rest=body.split('5.任务情节：（A路线）');a,rest=rest.split('7.任务情节：（B路线）');b,eco=rest.split('10.地下水路')
 recommended=int(one(r'等级要求：建议等级(\d+)级',head))
 require('特殊要求：带有不可思议的贝壳、解过金飞任务' in head and '交通工具：步行或骑宠。4.传送师：尼克斯城。' in head,'Header requirements/travel changed')
 guard=one(r'与漂亮的"([^"]+)"对话',a)
 spirit=one(r'女王和精灵"([^"]+)"都希望',a)
 require(all('而且尽量不要以武力的方式解决' in section for section in (a,b)),'Nonviolent preference changed')
 soldier=one(r'附近的"([^"]+)"（东(\d+)，南(\d+)）说话',a)
 kraken=one(r'地下水路第八层，就会看到"([^"]+)"（东(\d+)，南(\d+)）',a)
 water_level=int(one(r'打倒(\d+)级的水怪后',a))
 require('用网子给抓走' in a and a.index('水怪一看到人类就开始展开攻击') < a.index('根据水怪的说法') < a.index('交出给勇者') < a.index('将小水怪交还给水怪'), 'Route A conflict/investigation/rescue order changed')
 require(b.index('找「副园长巴克') < b.index('勇者接过小水怪') < b.index('当水怪注意到勇者欲交还的小水怪'), 'Route B investigation-first/return order changed')
 require('想要听得懂水怪说的话，玩家身上就必须带有"不可思议的贝壳"，否则只会听到水怪咕噜咕噜地乱叫' in a and '能与动物沟通的"不可思议的贝壳"' in b,'Communication shell scope changed')
 origins=one(r'以下任务得到不可思议的贝壳：(.*?)可疑的动物园',a)
 require(origins=='北岛弥生与日美子的友谊南岛哥亚山小猪传情任务吉鲁岛小猪爱情故事','Three source-labelled alternative shell origins changed')
 bark_a=one(r'找"([^\"]+)"（东(\d+)，南(\d+)）',a);bark_b=one(r'找「([^\"]+)"（东(\d+)，南(\d+)）',b)
 require(bark_a==bark_b,'Bark occurrence coordinates differ between routes')
 fights=[]
 for section in (a,b):
  lv,minion=one(r'与(\d+)级的巴克和(\d+)级巴克的跟班',section);fights.append([int(lv),int(minion)])
  require('与巴克副园长的对战不能组队' in section and '建议玩家可以先将巴克打倒，再对付他的跟班' in section,'Local party restriction or advisory target order changed')
 require(fights[0]==fights[1],'Shared Bark battle descriptions disagree')
 child_a=one(r'小水怪"([^\"]+)"交出给勇者',a);child_caption=one(r'终于救出小水怪"([^\"]+)"',a);child_b=one(r'接过小水怪"([^\"]+)"后',b)
 require(child_a==child_b,'Body child names differ between routes')
 entrance=xy(one(r'再去一趟地下水路(（东\d+，南\d+）)',a))[0]
 b_return=one(r'地下水路（东(\d+)，南(\d+)）第八层，一见到水怪"([^\"]+)"（东(\d+)，南(\d+)）',b)
 require([int(v) for v in b_return[:2]]==entrance and [int(v) for v in b_return[3:]]==[int(v) for v in kraken[1:]],'Return locations disagree')
 require(all('原本要当作' in section and '蛙送给勇者' in section for section in (a,b)) and '不会再恣意攻击人类' in b and '就没有理由和人类为敌' in a,'Return/peace/frog dinner motif changed')
 pet_a=one(r'6.获得宠物："([^\"]+)"',a);pet_b=one(r'9.获得宠物："([^\"]+)"',b);require(pet_a==pet_b,'Pet reward differs between routes')
 weapon,attack,speed,skill,skill_lv=one(r'8.获得物品："([^\"]+)"（攻([+-]\d+)敏([+-]\d+)([^L]+)Lv(\d+)）',b)
 require('服务器维修过后第一时间去拿，才拿得到' in b and '否则就算完成任务也拿不到'+weapon in b,'Unquantified post-maintenance condition changed')
 require('这把长枪是尼克斯近卫队的象征' in b,'Weapon narrative role changed')
 eco_entrance=xy(one(r'坐标：(（东\d+，南\d+）)怪物等级',eco))[0];require(eco_entrance==entrance,'Ecology entrance differs')
 lo,hi=map(int,one(r'怪物等级：(\d+)~(\d+)级',eco));labels=one(r'怪物种类：(.+?)地下水路第一层',eco).split('、');require(len(labels)==5,'Five source ecology labels required')
 require(re.findall(r'地下水路第([一二三四五六七八])层',eco)==list('一二三四五六七八'),'Eight reported floor captions required')
 npcs=[{'name':guard,'role':'REQUEST_AND_CITY_RECONCILIATION','location':'尼克斯王宫前','coord':None,'original_id':None},
  {'name':soldier[0],'role':'ROUTE_A_SEWER_TELEPORT','coord':[int(v) for v in soldier[1:]],'destination':'地下水路','original_id':None},
  {'name':kraken[0],'role':'AGGRIEVED_PARENT_CREATURE','floor_as_reported':8,'coord':[int(v) for v in kraken[1:]],'original_id':None},
  {'name':bark_a[0],'role':'ZOO_ABDUCTOR_AND_WAREHOUSE_OPPONENT','coord':[int(v) for v in bark_a[1:]],'battle_location':'动物园仓库','original_id':None}]
 return {'city':'尼克斯城','recommended_level':recommended,'hard_entry_level':None,
  'header_requirements':{'holds_communication_shell_as_reported':True,'completed_golden_flight_quest_as_reported':True,'server_flags_verified':False},
  'shell':{'name':'不可思议的贝壳','function':'UNDERSTAND_CREATURE_SPEECH','absence_description':'ONLY_GURGLING_AS_REPORTED',
   'origins_as_reported':['北岛弥生与日美子的友谊','南岛哥亚山小猪传情任务','吉鲁岛小猪爱情故事'],'all_three_required':False,
   'entrance_key':None,'consumed':None,'equipment_slot':None,'original_item_id':None},
  'narrative':{'initial_damage':'SOUTHEAST_CITY_HOUSES_AND_RESIDENTS','usual_habitat':'EAST_CITY_UNDERGROUND_WATERWAY',
   'initially_not_attacking_residents_as_reported':True,'motive':'CHILD_ABDUCTED_BY_NET_WIELDING_HUMANS','abductor':'副园长巴克',
   'royal_preference':'RESOLVE_WITHOUT_FORCE_IF_POSSIBLE','mentioned_spirit':spirit,'queen_original_identity':None,
   'child_body_name':child_a,'child_caption_name':child_caption,'child_spelling_conflict_unresolved':child_a!=child_caption,
   'child_original_id':None,'child_is_reward_pet_proven':False,'child_returned_in_described_outcome':True,
   'reconciliation_described':True,'actual_reunion_runtime_observed':False,'frog_dinner_motif':'REPORTED_STORY_NOT_FEEDING_AI'},
  'routes':[{'route':'A','sequence':['CITY_REQUEST','SOLDIER_TELEPORT','FIGHT_PARENT_WATER_MONSTER','LEARN_ABDUCTION','INVESTIGATE_ZOO','FIGHT_BARK','RETURN_CHILD','REPORT_TO_GUARD'],
    'parent_battle_described':True,'parent_level_as_reported':water_level,'pet_reward':pet_a,'weapon_reward_described':False},
   {'route':'B','sequence':['CITY_REQUEST','INVESTIGATE_ZOO_FIRST','FIGHT_BARK','RETURN_CHILD','REPORT_TO_GUARD'],
    'parent_battle_described':False,'no_parent_battle_server_guarantee':None,'pet_reward':pet_b,'weapon_reward_described':True}],
  'bark_battle':{'boss_level_as_reported':fights[0][0],'henchman_level_as_reported':fights[0][1],
   'party_prohibited_as_reported':True,'restriction_scope':'BARK_BATTLE_ONLY','help_behavior':None,'pets_allowed':None,
   'advisory_target_order':['BARK','HENCHMEN'],'mandatory_target_order':None},
  'reward_pet':{'name':pet_a,'routes':['A','B'],'level':None,'stats':None,'growth':None,'original_id':None},
  'weapon':{'name':weapon,'route':'B','stats_as_reported':{'攻':int(attack),'敏':int(speed)},'spirit_as_reported':skill,'spirit_level_as_reported':int(skill_lv),
   'role':'NYX_GUARD_SYMBOL','additional_condition':'FIRST_OPPORTUNITY_AFTER_SERVER_MAINTENANCE_AS_GUIDE_CLAIM',
   'every_completion_guaranteed':False,'deadline_seconds':None,'quota':None,'reset_cycle':None,'original_id':None},
  'npc_occurrences':npcs,'ecology':{'map_label':'地下水路','entrance_as_reported':entrance,'floors_captioned':8,'level_range_as_reported':[lo,hi],
   'source_labels':labels,'complete_roster_proven':False,'capturability':None,'original_map_ids':None,'full_geometry':None,'stray_caption_prefix_7_8_as_written':'果'},
  'core_fingerprint':{'characters':len(body),'utf8_bytes':len(body.encode()),'sha256':sha(body.encode())},
  'image_references':links,'exact_build':None,'official_authorship_verified':False,'original_server_runtime_verified':False}


def pin(path):
 b=(ROOT/path).read_bytes();return {'path':path,'bytes':len(b),'sha256':sha(b),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}


def comparison():
 family=json.loads((ROOT/PARENTS[0]).read_text());early=json.loads((ROOT/PARENTS[1]).read_text());shell=next(v for v in early['observations']['guide_profiles'] if v['id']=='FRIENDSHIP_SHELL_DELIVERY')
 return {'source_history':{'visible_publication':'2003-06-03 11:57','archive_actual_capture':'20160929133108',
  'requested_availability_timestamp':'20031201','archive_does_not_authenticate_2003_bytes':True,'wrappers_are_one_source_not_independent_witnesses':True},
  'family_comparison':{'report':PARENTS[0],'liuli_completed_reunion_claim_permitted':family['negative_boundaries']['family_reunion_completed'],
   'this_guide_child_return_is_described_outcome_not_runtime':True,'shared_family_or_quest_id_proven':False},
  'shell_comparison':{'report':PARENTS[1],'early_guide_profile':shell['id'],'early_flow':shell['reported_flow'],
   'same_original_shell_id_proven':False,'communication_function_backfilled_to_early_build':False},'modern_adoption_decided':False}


def catalog(ex,images,visual):
 entries=[('QUEST','quests','DOCUMENTARY_BRANCHING_RESCUE_QUEST',{k:ex[k] for k in ('recommended_level','hard_entry_level','header_requirements','narrative','routes','bark_battle')},['S1','S2'])]
 entries += [('NPC'+str(i),'npcs','DOCUMENTARY_NPC_OR_CREATURE_OCCURRENCE',n,['S1','S2']) for i,n in enumerate(ex['npc_occurrences'],1)]
 entries += [('SHELL','items','DOCUMENTARY_COMMUNICATION_ITEM',ex['shell'],['S1','S2']),('FORK','items','DOCUMENTARY_CONDITIONAL_REWARD_ITEM',ex['weapon'],['S1','S2','I2']),('FROG','pets','DOCUMENTARY_REWARD_PET',ex['reward_pet'],['S1','S2']),('WATERWAY','maps','DOCUMENTARY_ECOLOGY_NOT_GEOMETRY',ex['ecology'],['S1','S2'])]
 entries += [(v['id'],'screens','DOCUMENTARY_CURRENT_IMAGE_REFERENCE',{'image':p,'observation':v},['S1',v['id']]) for p,v in zip(images,visual)]
 return [{'record_id':'CN2003-R77-'+ident,'collection':coll,'entity_type':kind,'version_profile':PROFILE,'source_refs':refs,
  'verification_status':'GUIDE_OR_CURRENT_IMAGE_NOT_ORIGINAL_RUNTIME','rights_status':'RESEARCH_METADATA_NOT_RELEASE_APPROVED','record_revision':1,'game_ids':None,'content':c} for ident,coll,kind,c,refs in entries]


def inspect_images(raws,r):
 for p in r['images']:
  b=raws[p['id']]
  with Image.open(io.BytesIO(b)) as im:im.load();actual={'bytes':len(b),'sha256':sha(b),'format':im.format,'mode':im.mode,'size':list(im.size)}
  require(all(actual[k]==p[k] for k in actual),'Actual linked JPEG changed')
  require(p['url_as_written']==r['extraction']['image_references'][p['source_reference_index']] and p['requested_url']==p['url_as_written'].replace('http://','https://',1),'Image not attached to actual article reference')
 return r['images']


def verify_report(r):
 require(r['version_profile']==PROFILE and r['negative_boundaries']==BOUNDARIES,'Version/authority boundary promoted')
 require(r['parent_pins']==[pin(p) for p in PARENTS] and r['parser_dependency_pin']==pin(PARSER),'Parent/shared parser bytes changed')
 require(r['archive_discovery']['requested_target_timestamp']=='20031201' and r['archive_discovery']['closest_timestamp']=='20160929133108' and r['archive_discovery']['actual_verified_archive_url']==URLS['S2'] and r['archive_discovery']['is_2003_original_capture'] is False and r['source_pages'][1]['actual_capture']=='20160929133108','Archive discovery/date promoted')
 require(r['comparison']==comparison() and r['catalog_records']==catalog(r['extraction'],r['images'],r['image_observations']),'Comparison/catalog detached')
 ex=r['extraction'];require(ex['hard_entry_level'] is None and ex['exact_build'] is None and ex['official_authorship_verified'] is False and ex['original_server_runtime_verified'] is False,'Unknown authority/build/level promoted')
 require(all(ex['shell'][k] is None for k in ('entrance_key','consumed','equipment_slot','original_item_id')) and ex['shell']['all_three_required'] is False and ex['shell']['function']=='UNDERSTAND_CREATURE_SPEECH','Communication became access/consumption or combined quests')
 require(ex['bark_battle']['restriction_scope']=='BARK_BATTLE_ONLY' and all(ex['bark_battle'][k] is None for k in ('help_behavior','pets_allowed','mandatory_target_order')),'Local restriction generalized')
 require(ex['routes'][0]['parent_battle_described'] is True and ex['routes'][1]['parent_battle_described'] is False and ex['routes'][1]['no_parent_battle_server_guarantee'] is None,'Two described paths became universal server guarantee')
 require(ex['narrative']['child_spelling_conflict_unresolved'] is True and ex['narrative']['child_original_id'] is None and ex['narrative']['child_is_reward_pet_proven'] is False and ex['narrative']['actual_reunion_runtime_observed'] is False and ex['narrative']['frog_dinner_motif']=='REPORTED_STORY_NOT_FEEDING_AI','Narrative/variant/ownership promoted')
 require(ex['weapon']['route']=='B' and ex['weapon']['every_completion_guaranteed'] is False and all(ex['weapon'][k] is None for k in ('deadline_seconds','quota','reset_cycle','original_id')),'Post-maintenance wording overquantified')
 require(all(n['original_id'] is None for n in ex['npc_occurrences']) and all(ex['reward_pet'][k] is None for k in ('level','stats','growth','original_id')) and all(ex['ecology'][k] is None for k in ('capturability','original_map_ids','full_geometry')) and ex['ecology']['complete_roster_proven'] is False,'NPC/pet/map unknown promoted')
 require(r['unacquired_image_reference_count']==16,'Declared image acquisition coverage promoted')
 require(ex['weapon']['stats_as_reported']==r['image_observations'][1]['displayed_stats'] and ex['weapon']['spirit_as_reported']==r['image_observations'][1]['displayed_spirit'] and ex['weapon']['spirit_level_as_reported']==r['image_observations'][1]['displayed_spirit_level'],'Body/item sample disagreement requires explicit review')
 require(r['image_observations']==[
  {'id':'I1','manual_visual_review':True,'kind':'STATIC_BATTLE_TARGET_SCREEN','readable_target_label':'克拉肯','displayed_target_level':100,'central_25_is_target_level':False,'original_enemy_id':None,'capture_date_authenticated':None,'native_client_resolution_proven':False},
  {'id':'I2','manual_visual_review':True,'kind':'STATIC_ITEM_WINDOW_SCREEN','readable_item_name':'双头叉','displayed_stats':{'攻':75,'敏':-25},'displayed_spirit':'滋润的精灵','displayed_spirit_level':5,'displayed_player_level_sample':87,'sample_level_is_entry_gate':False,'actual_reward_acquisition_observed':False,'original_item_id':None,'capture_date_authenticated':None,'native_client_resolution_proven':False}], 'Visual transcription/authority changed')
 require([(p['bytes'],p['sha256'],p['size']) for p in r['images']]==[(71197,'11afbc0228cba1784870958ae96472595a3fbe9876fc13580ed8a8c067c73f27',[640,480]),(95671,'248f1daeb4d1e9b12c9b523d69971ae604ecabdddcf44500c6d5a06314c1387d',[640,480])],'Manual observations detached from reviewed JPEGs')

MUTATIONS=[('建议等级105级','建议等级99级'),('解过金飞任务','无需金飞任务'),('否则只会听到水怪咕噜咕噜地乱叫','否则无法进入地下水路'),
 ('打倒100级的水怪后','打倒101级的水怪后'),('（东96，南24）','（东97，南24）'),('（东18，南13）','（东19，南13）'),
 ('（东41，南5）','（东42，南5）'),('75级巴克的跟班','76级巴克的跟班'),('与巴克副园长的对战不能组队','与巴克副园长的对战可以组队'),
 ('先将巴克打倒，再对付他的跟班','先将跟班打倒，再对付巴克'),('小水怪"莫拉斯"','小水怪"莫拉司"'),('"尤里蛙"','"别的蛙"'),
 ('攻+75敏-25','攻+74敏-25'),('攻+75敏-25','攻+75敏-20'),('滋润的精灵Lv5','滋润的精灵Lv4'),
 ('服务器维修过后第一时间去拿','任何时间去拿'),('怪物等级：80~100级','怪物等级：81~100级'),('、迪加','、不同怪'),
 ('（东291，南34）','（东292，南34）'),('用网子给抓走','自愿跟着走'),('蛙送给勇者','物品送给勇者'),('尽量不要以武力','必须以武力')]


def audit(raws,expected):
 target={k:v for k,v in expected.items() if k!='core_fingerprint'}
 for sid in URLS:
  text=raws[sid].decode('gb18030')
  for old,new in MUTATIONS:
   require(old in text,'Real source mutation absent: '+old)
   try:actual=derive(text.replace(old,new).encode('gb18030'))
   except (ValueError,IndexError):continue
   actual.pop('core_fingerprint');require(actual!=target,'Semantic mutation masked by body fingerprint: '+old)
  require(derive(raws[sid]+b'<script>peripheral=1</script>')==expected,'Peripheral script changed meaning')
 return {'semantic_mutations_per_input':len(MUTATIONS),'total_semantic_mutations':len(MUTATIONS)*2,'digest_and_whole_body_fingerprint_gate_removed':True,'peripheral_script_positive_each_input':True}


def replay(raws,r):
 verify_report(r);all_ex=[derive(raws[s]) for s in URLS];require(all(ex==r['extraction'] for ex in all_ex),'Current/archive source meaning or body changed')
 images=inspect_images(raws,r);ex=all_ex[0]
 return {'schema':'stoneage.cn2003_water_monster.replay.r1','inputs':[{'id':sid,'url':u,'bytes':len(raws[sid]),'sha256':sha(raws[sid])} for sid,u in URLS.items()],
  'extraction':ex,'images':images,'image_observations':r['image_observations'],'catalog_records':catalog(ex,images,r['image_observations']),'comparison':comparison(),
  'audit':audit(raws,ex),'original_html_or_assets_in_output':False,'original_game_runtime_verified':False}


def read_inputs(directory=None):
 def get(url,name):
  if directory is not None:return (Path(directory)/name).read_bytes()
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'StoneAge-research/1.0'}),timeout=45) as response:
   require(response.status==200 and response.url==url,'HTTP identity changed');raw=response.read(2_000_001)
  require(len(raw)<=2_000_000,'Input too large');return raw
 raws={sid:get(u,sid+'.html') for sid,u in URLS.items()};ex=derive(raws['S1'])
 for ident,index in [('I1',3),('I2',9)]:raws[ident]=get(ex['image_references'][index].replace('http://','https://',1),ident+'.jpg')
 return raws


def main():
 p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--fetch',action='store_true');g.add_argument('--input-dir');p.add_argument('--output',required=True);a=p.parse_args()
 r=json.loads(REPORT.read_text());out=replay(read_inputs(a.input_dir),r)
 if (ROOT/f'research/recovered/{STEM}-CUSTODY-R1.json').exists():verify_custody()
 target=Path(a.output);target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'source_wrappers':2,'routes':2,'linked_original_jpegs':2,'catalog_records':11,'semantic_mutations':44}))

if __name__=='__main__':main()
