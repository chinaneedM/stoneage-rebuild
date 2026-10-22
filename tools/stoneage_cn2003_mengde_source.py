"""R81: a documentary quest/order contract; no original quest-engine execution."""
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
STEM='STONEAGE-CN2003-MENGDE-CAVE'
REPORT=ROOT/f'research/recovered/{STEM}-SOURCE-R1.json'
URL='https://games.sina.com.cn/zhqu/sta/rwgl1_11.shtml'
PROFILE='CN_SINA_GUIDE_MENGDE_20030529_EXACT_OFFICIAL_BUILD_UNKNOWN'
PARSER='tools/stoneage_jp2005_treasure_source.py'
PARENTS=['research/recovered/STONEAGE-CN20-RECORDPOINT-SOURCE-R1.json',
 'research/recovered/STONEAGE-CN2003-FIVE-BROTHERS-SOURCE-R1.json',
 'research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json']
TITLE='《石器时代》任务攻略—梦德洞窟'
SOURCE={'url':URL,'http_status':200,'no_redirect':True,'bytes':50035,
 'sha256':'85b08eec3a4235de8e9a19f8e88abd4698573a74e2c96afb8667fcc4a8208d8b',
 'encoding':'GB18030_STRICT','replacement_characters':0,'visible_title':TITLE,
 'visible_publication':'2003-05-29 17:00','publisher_field':'新浪游戏','submission_label':'网友投稿',
 'named_original_author':None,'official_authorship_verified':False,'authenticated_2003_snapshot':False,
 'authority':'DATED_PORTAL_GUIDE_AUTHOR_UNVERIFIED_NOT_OPERATOR_SCRIPT',
 'current_bytes_authenticate_2003_original':False,'exact_game_version_or_build':None}
IMAGES=[
 {'id':'I1','url':'https://image2.sina.com.cn/gm/zhqu/sta/article/2003-05-29/1_115-15-232-572_2003052917425.jpg',
  'http_status':200,'no_redirect':True,'bytes':92532,'sha256':'9489d96399a014a090b3265e00af75e2241a96c20e98af75922c3319bc889948','format':'JPEG','mode':'RGB','size':[640,480],'frames':1},
 {'id':'I2','url':'https://image2.sina.com.cn/gm/zhqu/sta/article/2003-05-29/1_115-15-238-572_2003052917425.jpg',
  'http_status':200,'no_redirect':True,'bytes':94389,'sha256':'c5196cae526922f517fe5e146c068e0e23b389b6fe4581d926660f3bab59a5e6','format':'JPEG','mode':'RGB','size':[640,480],'frames':1}]
VISUAL=[
 {'id':'I1','manual_visual_review':True,'kind':'STATIC_INVENTORY_ARMOR_TOOLTIP_WITH_DESERT_CHARACTERS',
  'displayed_item_label':'芙蕾雅Lv1铠6','displayed_stats':{'防':20,'敏':-6},'displayed_spirit':'滋润的精灵Lv1',
  'scene':['DESERT','CACTUS','TWO_CHARACTERS'],'npc_identity_independently_visible':False,
  'actual_reward_delivery_or_item_effect_tested':False,'original_sprite_or_model':False,'exact_build_or_native_resolution_verified':False},
 {'id':'I2','manual_visual_review':True,'kind':'STATIC_INVENTORY_ACCESSORY_TOOLTIP_WITH_GRASS_ROCKS',
  'displayed_item_label':'黄色大首饰','displayed_stats':{'魅':5,'睡眠耐性':30},
  'scene':['GRASS','ROCK_WALL','TWO_CHARACTERS'],'npc_identity_independently_visible':False,
  'actual_reward_delivery_or_item_effect_tested':False,'original_sprite_or_model':False,'exact_build_or_native_resolution_verified':False}]
BOUNDARIES={k:False for k in ('official_authorship_verified','current_bytes_authenticate_2003_original',
 'named_version_182_or_tw10_verified','recommended_60_is_hard_gate','generic_village_girls_are_one_npc',
 'village_world_coordinates_are_local_npc_coordinates','source_quotation_typo_is_server_parser_rule',
 'reward_order_is_verified_server_flag','both_stones_share_one_original_item_id','magatama_sale_is_automatic_cash_reward',
 'steal_warning_supplies_drop_or_theft_algorithm','checkpoint_advice_proves_savedata_format',
 'parent_nearby_checkpoint_row_is_same_village_checkpoint','five_brothers_ecology_is_this_dungeon_ecology',
 'static_tooltip_proves_reward_delivery_or_buff','current_jpeg_authenticates_2003_original_pixels',
 'original_html_or_assets_committed','stage_b_started')}


def article(raw):
 p=VisibleMarkup();p.feed(raw.decode('gb18030',errors='strict'));text=''.join(p.parts)
 require(plain(one(r'<title>(.*?)</title>',text,re.S)).startswith(TITLE),'Page title changed')
 middle=one(r'<!-- include 中间内容 begin -->(.*?)<!-- include 中间内容 end -->',text,re.S)
 require(plain(one(r'<b>(《石器时代》任务攻略—梦德洞窟)</b>',middle,re.S))==TITLE,'Visible article heading changed')
 require(plain(one(r'<!-- include 发布时间 begin -->(.*?)<!-- include 发布时间 end -->',middle,re.S))=='2003-05-2917:00','Publication label changed')
 require('新浪游戏' in plain(middle) and '网友投稿' in plain(middle),'Publisher/submission field changed')
 body=one(r'<td class=l15z>(.*?)<table width=520 cellpadding=0 cellspacing=0 align=center>',middle,re.S)
 core=plain(body)
 require(core.startswith('1.等级要求：') and core.endswith('之后再去解会比较保险。'),'Quest business boundaries changed')
 pairs=re.findall(r'<a href=(http://image2\.sina\.com\.cn/[^ >]+) target=_blank><img src=(http://image2\.sina\.com\.cn/[^ >]+) border=0></a>',body)
 require(len(pairs)==12 and len(set(pairs))==12,'Twelve actual full/thumbnail pairs required')
 selected=[pairs[9],pairs[11]]
 require([a.replace('http:','https:',1) for a,b in selected]==[v['url'] for v in IMAGES],'Selected full-size reward images detached')
 return core,body,pairs


def derive(raw):
 core,body,pairs=article(raw)
 def must(*clauses):require(all(plain(v) in core for v in clauses),'Source quest clause changed')
 must('1. 等级要求：建议等级60级。','2. 特殊要求：解过成人仪式。','3. 交通工具：步行或骑宠。','4. 精灵的羽毛：卡坦村、霍特尔村。')
 must('介于卡坦村和霍特尔村的沙漠地带人烟稀少','盗贼--"梦德一族"','没有守护石的保护，霍特尔村将会发生不吉利的事',
  '一旦村庄的守护石遭窃后，村庄的重要祭典就无法举行')
 must('先前往柯尔克村（东43，南49）','"往柯尔克的道路"（东318，南428）','穿著红色战斗装的"村姑"（东96，南75）',
  '霍特尔村（东622，南193）','"村姑"（东64，南65）','穿著绿色战斗装的村姑',
  '卡坦村（东259，南170）','"年轻人"（东71，南76）','霍特尔山西边的水井')
 must('进入梦德洞窟的暗号为"在卡坦有梦德"','梦德洞窟（东443，南127）','对着守在水井前的盗贼说出暗号「在卡坦有梦德"，即可进入盗贼的基地')
 must('只要一个不小心，身边的东西就会被盗贼摸走','基地最底层','大块头"唐"（东23，南42）、"悟"（东22，南42）',
  '顺利击败唐、悟后，就可以见到盗贼的首领"梦德"（族长）','将"霍特尔的保护石"和"卡坦的保护石"交出来')
 must('首先前往卡坦村，将卡坦村的守护石交给卡坦的年轻人','赠送勇者"芙蕾雅Lv1铠6"',
  '接着前往霍特尔村，将霍特尔村的守护石交给村姑','获得美丽的"勾玉"','拿这只勾玉去换钱还可以换到2000S',
  '必须再回柯尔克村将好消息跟村姑讲','村姑就会送给勇者"黄色大首饰"',
  '一定要先去卡坦村找年轻人，再去霍特尔村找村姑；如果玩家的顺序相反的话，最后柯尔克村的村姑是不会给你黄色大首饰')
 must('芙蕾雅Lv1铠6（防+20敏-6滋润的精灵Lv1）','黄色大首饰（魅+5睡眠耐性+30）',
  '并没有任何羽毛可瞬间飞行至柯尔克村','适合利用贝洛恩的肉在纪录点存盘','先在柯尔克村存盘，再前往其它两个村庄',
  '敌人都是盗贼，攻击力较高','建议玩家能多找几个朋友一起解谜，或是等玩家等级超过60级之后再去解会比较保险')
 return {'name':'梦德洞窟','recommended_level_as_reported':60,'hard_level_gate':None,
  'prerequisite_as_reported':'解过成人仪式','transport':['步行','骑宠'],'feather_labels':['卡坦村','霍特尔村'],
  'village_interactions':[
   {'occurrence':'KELKE_GIRL','village':'柯尔克村','world_coord':[43,49],'npc_label':'村姑','local_coord':[96,75],'outfit':'红色战斗装','role':'INTRODUCE_FRIENDS_IN_TWO_VILLAGES'},
   {'occurrence':'HOTER_GIRL','village':'霍特尔村','world_coord':[622,193],'npc_label':'村姑','local_coord':[64,65],'outfit':'绿色战斗装','role':'REPORT_STOLEN_STONE_AND_ASK_TO_VISIT_KATAN'},
   {'occurrence':'KATAN_YOUTH','village':'卡坦村','world_coord':[259,170],'npc_label':'年轻人','local_coord':[71,76],'outfit':None,'role':'REPORT_STOLEN_STONE_AND_TELL_PASSWORD'}],
  'story':{'setting':'SPARSE_DESERT_BETWEEN_KATAN_AND_HOTER_CONTROLLED_BY_MENGDE_THIEVES',
   'hoter_consequence_as_told':'BAD_OMENS_WITHOUT_GUARDIAN_STONE','katan_consequence_as_told':'IMPORTANT_FESTIVAL_CANNOT_BE_HELD',
   'chief_response_as_told':'SURRENDERS_STONES_AFTER_TANG_WU_DEFEATED','developer_intent_or_real_world_history':None},
  'dungeon':{'road_label':'往柯尔克的道路','road_coord':[318,428],'entrance_world_coord':[443,127],
   'entrance_description':'WELL_WEST_OF_HOTER_MOUNTAIN','gate_actor':'UNNAMED_THIEF','password':'在卡坦有梦德',
   'quote_delimiters_as_written':['"在卡坦有梦德"','「在卡坦有梦德"'],'server_case_encoding_or_punctuation_match':None,
   'guards':[{'name':'唐','local_coord':[23,42]},{'name':'悟','local_coord':[22,42]}],
   'guard_floor_description':'最底层','numeric_floor_count':None,'chief':'梦德','chief_coord':None,
   'theft_warning':'BELONGINGS_MAY_BE_STOLEN','theft_targets_algorithm_probability':None,'enemy_stats_or_spawn_table':None},
  'stones':[{'name_as_quoted':'霍特尔的保护石','return_context':'霍特尔村的守护石','recipient':'HOTER_GIRL'},
   {'name_as_quoted':'卡坦的保护石','return_context':'卡坦村的守护石','recipient':'KATAN_YOUTH'}],
  'reward_sequence_as_reported':['KATAN_YOUTH_RETURN_STONE','HOTER_GIRL_RETURN_STONE','KELKE_GIRL_REPORT_SUCCESS'],
  'reversed_first_two_warning':'NO_YELLOW_ACCESSORY_FROM_KELKE_GIRL_AS_GUIDE_CLAIM',
  'reward_order_server_flag_or_atomic_transaction':None,
  'rewards':[
   {'name':'芙蕾雅Lv1铠6','from':'KATAN_YOUTH','stats':{'防':20,'敏':-6},'spirit':'滋润的精灵','spirit_level':1,'label_number_6_is_native_equipment_level_verified':False},
   {'name':'勾玉','from':'HOTER_GIRL','description':'美丽的勾玉','sale_value_as_reported':2000,'currency_label_as_written':'S','sale_venue_or_actual_sale':None,'automatic_cash_reward':False},
   {'name':'黄色大首饰','from':'KELKE_GIRL','stats':{'魅':5,'睡眠耐性':30},'condition':'RETURN_KATAN_THEN_HOTER_THEN_REPORT_KELKE','actual_status_resistance_tested':False}],
  'route_advice':{'kelke_feather_unavailable_as_guide_claim':True,'recordpoint_meat_as_written':'贝洛恩的肉',
   'suggested_first_checkpoint':'柯尔克村','meat_quantity_consumption_original_id':None,'storage_format_or_original_io_test':None,
   'party_or_over_60_is_advice_not_admission_rule':True},
  'exact_game_build':None,'original_map_npc_quest_item_ids':None,'repeatability_reset_and_item_consumption':None,
  'original_server_runtime_verified':False,
  'image_links':{'full_thumbnail_pairs':len(pairs),'selected_full_http':[pairs[9][0],pairs[11][0]],'selected_thumbnails_http':[pairs[9][1],pairs[11][1]],'unacquired_full_images':10},
  'core_fingerprint':{'characters':len(core),'utf8_bytes':len(core.encode()),'sha256':sha(core.encode())}}


def pin(path):
 b=(ROOT/path).read_bytes();return {'path':path,'bytes':len(b),'sha256':sha(b),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}


def comparison():
 early=json.loads((ROOT/PARENTS[0]).read_text());brothers=json.loads((ROOT/PARENTS[1]).read_text())
 return {'early_recordpoint':{'schema':early['schema'],'source_role':'EARLY_OPERATOR_HOSTED_GUIDE',
  'near_kelke_row':[v for v in early['extracted']['rows'] if v['place_as_written']=='柯尔克通路附近'],
  'nearby_row_equals_village_checkpoint':False,'meat_names_forced_to_alias':False,'missing_village_row_means_no_checkpoint':False,
  'later_guide_advice_is_original_save_format':False},
  'five_brothers':{'schema':brothers['schema'],'ecology_region_label':brothers['extraction']['region_label'],
   'beluorn_jilu_ecology_backfilled_to_mengde':False,'recommended_60_is_shared_hard_level':False,
   'reward_reset_after_rebirth_backfilled':False,'same_spirit_name_means_same_item_id':False},
  'modern_adoption_decided':False,'portal_title_authenticates_version_182':False}


def catalog(ex):
 rows=[('quest','quests','DOCUMENTARY_ORDER_SENSITIVE_RECOVERY_QUEST',ex,['S1'])]
 rows += [(v['occurrence'],'npcs','DOCUMENTARY_VILLAGE_NPC_OCCURRENCE_NOT_NATIVE_ID',v,['S1']) for v in ex['village_interactions']]
 rows += [('gate','npcs','DOCUMENTARY_UNNAMED_PASSWORD_GATE_ACTOR',{'label':ex['dungeon']['gate_actor'],'coord':None},['S1'])]
 rows += [(v['name'],'npcs','DOCUMENTARY_NAMED_GUARD',v,['S1']) for v in ex['dungeon']['guards']]
 rows += [('chief','npcs','DOCUMENTARY_THIEF_CHIEF',{'name':'梦德','coord':None},['S1']),
  ('routes','maps','DOCUMENTARY_THREE_VILLAGE_AND_WELL_ROUTE_NOT_MAP_MASTER',{'villages':ex['village_interactions'],'dungeon':ex['dungeon'],'coordinate_frames_not_interchangeable':True},['S1'])]
 rows += [('stone-'+str(i),'items','DOCUMENTARY_RETURN_OBJECT',v,['S1']) for i,v in enumerate(ex['stones'])]
 rows += [('reward-'+str(i),'items','DOCUMENTARY_QUEST_REWARD',v,['S1']) for i,v in enumerate(ex['rewards'])]
 rows += [('checkpoint-advice','tutorials','DOCUMENTARY_ROUTE_CHECKPOINT_ADVICE',ex['route_advice'],['S1'])]
 rows += [(im['id'],'screens','DOCUMENTARY_STATIC_INVENTORY_TOOLTIP',{'image':im,'observation':v},['S1',im['id']]) for im,v in zip(IMAGES,VISUAL)]
 return [{'record_id':'CN2003-R81-'+ident,'entity_type':kind,'collection':coll,'version_profile':PROFILE,
  'source_refs':refs,'verification_status':'DATED_PLAYER_GUIDE_OR_STATIC_SCREEN_NOT_SERVER_RUNTIME',
  'rights_status':'RESEARCH_METADATA_NOT_RELEASE_APPROVED','record_revision':1,'game_ids':None,'content':content}
  for ident,coll,kind,content,refs in rows]


def semantic(ex):return {k:v for k,v in ex.items() if k!='core_fingerprint'}


SEMANTIC_SHA='84b2a0e6cf89cc6b92df80b171ad98288514d95d09e64fa7d24a15e0bcc09203'

def validate(r):
 require(r['schema']=='stoneage.cn2003_mengde.source.r1' and r['version_profile']==PROFILE,'Version/schema changed')
 require(r['source']==SOURCE and r['images']==IMAGES and r['visual_observations']==VISUAL and r['negative_boundaries']==BOUNDARIES,'Source/visual/authority boundaries changed')
 require(r['parent_pins']==[pin(p) for p in PARENTS] and r['parser_pin']==pin(PARSER),'Original parent/parser bytes changed')
 require(r['comparison']==comparison(),'Cross-source distinctions changed')
 require(sha(json.dumps(semantic(r['extraction']),ensure_ascii=False,sort_keys=True).encode())==SEMANTIC_SHA,'Documentary quest contract changed')
 require(r['catalog_records']==catalog(r['extraction']),'Catalog detached from source semantics')
 contract=json.loads((ROOT/PARENTS[-1]).read_text())['future_website']
 require(len(r['catalog_records'])==17 and len({v['record_id'] for v in r['catalog_records']})==17,'Catalog count/IDs changed')
 require(all(set(contract['record_contract']['required']).issubset(v) and v['collection'] in contract['required_collections'] for v in r['catalog_records']),'Archive required fields/collections changed')


MUTATIONS=[('建议等级60级','等级限制60级'),('解过成人仪式','没有特殊要求'),('东43，南49','东44，南49'),('东318，南428','东319，南428'),
 ('东96，南75','东97，南75'),('东64，南65','东65，南65'),('东71，南76','东72，南76'),('东443，南127','东444，南127'),
 ('红色战斗装','蓝色战斗装'),('绿色战斗装','红色战斗装'),('暗号为&quot;在卡坦有梦德','暗号为&quot;在梦德有卡坦'),
 ('东23，南42','东23，南43'),('东22，南42','东22，南43'),('顺利击败唐、悟后','顺利击败唐后'),
 ('&quot;霍特尔的保护石&quot;和&quot;卡坦的保护石&quot;','&quot;霍特尔的保护石&quot;'),
 ('首先前往卡坦村','首先前往霍特尔村'),('接着前往霍特尔村','接着前往卡坦村'),
 ('是不会给你黄色大首饰','还是会给你黄色大首饰'),('换到2000S','换到3000S'),('防+20敏-6','防+30敏-6'),
 ('滋润的精灵Lv1','滋润的精灵Lv2'),('魅+5睡眠耐性+30','魅+6睡眠耐性+30'),
 ('没有任何羽毛可瞬间飞行至柯尔克村','可以用任何羽毛瞬间飞行至柯尔克村'),('贝洛恩的肉','任意宠物的肉'),
 ('身边的东西就会被盗贼摸走','身边的东西不会被盗贼摸走'),('重要祭典就无法举行','重要祭典不受影响'),
 ('霍特尔村将会发生不吉利的事','霍特尔村不会受到影响')]


def audit(raw,expected):
 text=raw.decode('gb18030');target=semantic(expected)
 for old,new in MUTATIONS:
  require(old in text,'Missing real source mutation: '+old)
  try:actual=derive(text.replace(old,new).encode('gb18030'))
  except (ValueError,IndexError):continue
  require(semantic(actual)!=target,'Source meaning changed but only fingerprint detected it: '+old)
 require(derive(raw+b'<script>outside=1</script>')==expected,'Peripheral script changed meaning')
 old='如果玩家的顺序相反的话，最后柯尔克村的村姑是不会给你黄色大首饰！'
 for replacement in ('','<script>'+old+'</script>'):
  changed=text.replace(old,replacement)+'<div>'+old+'</div>'
  try:derive(changed.encode('gb18030'))
  except ValueError:pass
  else:raise ValueError('Outside/hidden text repaired missing reward-order warning')
 return {'semantic_mutations_without_all_fingerprints':len(MUTATIONS),'hidden_and_outside_article_counterexamples':2,'outside_script_positive':True}


def inspect_images(inputs):
 for expected in IMAGES:
  raw=inputs[expected['id']]
  with Image.open(io.BytesIO(raw)) as im:
   im.load();actual={'bytes':len(raw),'sha256':sha(raw),'size':list(im.size),'format':im.format,'mode':im.mode,'frames':getattr(im,'n_frames',1)}
  require(all(expected[k]==v for k,v in actual.items()),'Reviewed reward screenshot bytes/full decode changed')


def replay(inputs,r):
 validate(r);ex=derive(inputs['S1']);require(ex==r['extraction'],'Quest extraction or fingerprint changed');inspect_images(inputs)
 require(len(inputs['S1'])==SOURCE['bytes'] and sha(inputs['S1'])==SOURCE['sha256'],'Current body bytes changed')
 return {'schema':'stoneage.cn2003_mengde.replay.r1','inputs':[{'id':k,'url':URL if k=='S1' else next(v['url'] for v in IMAGES if v['id']==k),'bytes':len(v),'sha256':sha(v)} for k,v in inputs.items()],
  'extraction':ex,'images':IMAGES,'visual_observations':VISUAL,'comparison':comparison(),'catalog_records':catalog(ex),
  'audit':audit(inputs['S1'],ex),'original_html_or_assets_in_output':False,'original_server_runtime_verified':False}


def read_inputs(directory=None):
 result={}
 for key,url in [('S1',URL)]+[(v['id'],v['url']) for v in IMAGES]:
  if directory:result[key]=(Path(directory)/(key+('.html' if key=='S1' else '.jpg'))).read_bytes()
  else:
   with urllib.request.urlopen(url,timeout=50) as h:
    require(h.status==200 and h.url==url,'Exact acquisition URL/status changed');result[key]=h.read()
 return result


def main():
 p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--fetch',action='store_true');g.add_argument('--input-dir');p.add_argument('--output',required=True);a=p.parse_args()
 r=json.loads(REPORT.read_text());out=replay(read_inputs(a.input_dir),r)
 path=Path(a.output);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print('R81 Mengde documentary order and two reward screens replayed; original flags, IDs and reward execution remain unknown.')


if __name__=='__main__':main()
