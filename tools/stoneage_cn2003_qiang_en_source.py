"""R83: Qiang En family narrative and source-scoped cave ecology; no quest VM."""
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
STEM='STONEAGE-CN2003-QIANG-EN-FAMILY'
REPORT=ROOT/f'research/recovered/{STEM}-SOURCE-R1.json'
PROFILE='CN_SINA_2003_QIANG_EN_GUIDES_EXACT_OFFICIAL_BUILD_UNKNOWN'
PARSER='tools/stoneage_jp2005_treasure_source.py'
PARENTS=['research/recovered/STONEAGE-CN2003-LIULI-CAVE-SOURCE-R1.json',
 'research/recovered/STONEAGE-CN2003-MENGDE-CAVE-SOURCE-R1.json',
 'research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json']
SOURCES=[
 {'id':'S1','url':'https://games.sina.com.cn/zhqu/sta/article/2003-05-30/9898.shtml','bytes':54963,
  'sha256':'33b20cfa59c64834592247eb21aad0a457d5dfa65a0dd532f2a108280c3dc60f',
  'visible_title':'《石器时代》任务功略-强恩一族','visible_publication':'2003-05-30 10:17','scope':'ONE_QUEST_ARTICLE'},
 {'id':'S2','url':'https://games.sina.com.cn/zhqu/sta/sqdt/sqdt_2.shtml','bytes':71509,
  'sha256':'521512039fd1edefd36581e315a52b566f73b90f5673d0211557df6c80f3f727',
  'visible_title':'南岛座标','visible_publication':'2003-04-03 14:19','scope':'ONLY_QIANG_EN_CAVE_ROW_NOT_WHOLE_ISLAND'}]
for s in SOURCES:
 s.update(http_status=200,no_redirect=True,encoding='GB18030_STRICT',replacement_characters=0,
  publisher_field='新浪游戏',submission_label='网友投稿',named_original_author=None,
  official_authorship_verified=False,current_bytes_authenticate_2003_original=False,
  exact_game_version_or_build=None,authority='DATED_PORTAL_GUIDE_AUTHOR_UNVERIFIED_NOT_OPERATOR_SCRIPT')
IMAGES=[
 {'id':'I1','url':'https://image2.sina.com.cn/gm/newgames/0303/images/qiangnen0530_009.jpg',
  'bytes':87716,'sha256':'5e57c456dd9b0cf648e91eca585f6958a704ef14643c2b1a08c01fa546f941e7'},
 {'id':'I2','url':'https://image2.sina.com.cn/gm/newgames/0303/images/qiangnen0530_012.jpg',
  'bytes':116396,'sha256':'68a756ea81d19f4cc63d006c2222defa04a8577832cf5ac05dc12ba2da8550d6'}]
for im in IMAGES:im.update(http_status=200,no_redirect=True,format='JPEG',mode='RGB',size=[640,480],frames=1)
VISUAL=[
 {'id':'I1','manual_visual_review':True,'kind':'STATIC_ROOM_WITH_SELECTED_NPC_LABEL','visible_npc_label':'沙拉',
  'scene':['STONE_WALLS','BED','TABLE','TWO_CHARACTERS'],'dialogue_or_choice_visible':False},
 {'id':'I2','manual_visual_review':True,'kind':'STATIC_INVENTORY_FLUTE_TOOLTIP','visible_npc_label':'吉德',
  'displayed_item_label':'卡娜的木笛','displayed_stats':{'魅':2,'毒':5,'石':-5,'眠':5},
  'displayed_spirit':'复活精灵','displayed_spirit_level':2,'scene':['WOODEN_FLOOR','STONE_WALL','TWO_CHARACTERS']}]
for v in VISUAL:v.update(actual_reward_delivery_or_item_effect_tested=False,original_sprite_or_model=False,
 exact_build_or_historical_pixels_verified=False,native_npc_id_verified=False)
BOUNDARIES={k:False for k in ('official_authorship_verified','current_bytes_authenticate_2003_original',
 'exact_same_build_or_independent_witnesses_verified','recommended_50_is_hard_gate','adult_ceremony_prerequisite_backfilled',
 'two_village_coordinates_are_assigned_entry_exit','secret_document_is_required','document_drop_is_guaranteed',
 'same_labels_mean_same_random_and_fixed_npc_instances','daughter_is_escorted_to_birth_father',
 'chief_sample_feather_is_guaranteed_reward','letter_title_means_birth_mother_alive',
 'kana_spellings_or_mountain_names_are_native_id_aliases','screenshot_floor_labels_prove_total_seven',
 'sara_room_is_eighth_floor','ecology_ranges_silently_merged','59_and_72_are_native_pet_ids',
 'map_transitions_are_undirected','abbreviated_stats_are_percent_immunity_or_damage',
 'static_screens_prove_choice_reward_or_effect','original_html_or_assets_committed','stage_b_started')}

# Small factual anchors protect meanings as well as the full-body fingerprint.
CLAUSES=[
 '建议等级50级','交通工具：步行或骑宠','精灵的羽毛：无','北岛有梦德一族、南岛有强恩一族',
 '奇喀喀村（东140，南1007）（东124，南1048）','"吉德的朋友"（东58，南66）','吉德的朋友"凯伊"',
 '16年前被绑架的女儿','物资从村里运到乌鲁力村','通过阿尔鲁山南侧','开在奇喀喀的花',
 '村长家深处的房间','住在阿鲁姆山的"强恩一族"','"吉德的儿子"','于是在两年后去世','母亲的发饰',
 '"强恩一族的洞窟"（东285，南926）','4楼出口附近','山贼守卫（东11，南54）','红色月亮的光芒',
 '5楼出口附近','第二个山贼守卫（东51，南5）','蓝色山脉即力量',
 '6楼出口附近','山贼守卫（东8，南23）','白色之风即速度',
 '四楼以后会随机遇到的伯恩、玛琼拉和卡鲁德','就有可能获得盗贼的秘密文件',
 '直接对着山贼守卫说出密语就可以上楼，不一定需要获得秘密文件',
 '终于走上七楼','"卡鲁德"、"伯恩"、"玛琼拉"挡路','在击败三人联合的攻击后',
 '山贼头目"强恩"（东68，南7）','抢了一个四岁的小孩','决定将小孩扶养长大',
 '"强恩的妻子"（东70，南8）','最后的决定由女儿自己决定','"沙拉的房间"找"沙拉"',
 '勇者将"母亲的发饰"交给沙拉','更希望陪在强恩双亲的身边，不想离开他们',
 '沙拉请勇者去转告强恩她的决定','会随机赠送勇者一个道具','哇~我得到属于山贼的羽饰喔~',
 '一封"给双亲的信"给吉德','再跟强恩说一声','将"给双亲的信"带回奇喀喀村村长家给吉德',
 '他的妻子卡那在天之灵','卡那生前所做的木笛','"卡娜的木笛"（魅+2毒+5石-5眠+5复活精灵Lv2）',
 '怪物等级：31~48级','怪物种类：卡鲁德、伯恩、玛琼拉、山贼、格鲁西斯、格尔顿']
OPTIONAL='直接对着山贼守卫说出密语就可以上楼，不一定需要获得秘密文件'


def visible(raw):
 p=VisibleMarkup();p.feed(raw.decode('gb18030',errors='strict'));return ''.join(p.parts)


def middle(raw,index):
 s=SOURCES[index];t=visible(raw)
 m=one(r'<!-- include 中间内容 begin -->(.*?)<!-- include 中间内容 end -->',t,re.S)
 require(plain(one(r'<b>(.*?)</b>',m,re.S))==s['visible_title'],'Visible article heading changed')
 require(plain(one(r'<!-- include 发布时间 begin -->(.*?)<!-- include 发布时间 end -->',m,re.S))==plain(s['visible_publication']),'Visible publication changed')
 require('新浪游戏' in plain(m) and '网友投稿' in plain(m),'Publisher/submission changed')
 return m


def article(raw):
 m=middle(raw,0);body=one(r'<td class=l15z>(.*?)<table width=520 cellpadding=0 cellspacing=0 align=center>',m,re.S);core=plain(body)
 require(core.startswith('1.等级要求：') and core.endswith('沙拉的房间'),'Quest boundaries changed')
 pairs=re.findall(r'<a href="(http://image2\.sina\.com\.cn/[^" ]+)" target="_blank"><img src="(http://image2\.sina\.com\.cn/[^" ]+)" border="0" width="150" height="113">',body)
 require(len(pairs)==20 and len(set(pairs))==20,'Twenty actual full/thumbnail pairs required')
 require([pairs[i][0].replace('http:','https:',1) for i in (8,11)]==[v['url'] for v in IMAGES],'Selected actual full images detached')
 return core,body,pairs


def map_row(raw):
 m=middle(raw,1)
 # Match exact outer cell labels; nested table rows never delimit this entity.
 row=one(r'<td width="18%" align="center" class=l15>强恩一族洞窟</td>(.*?)<td width="18%" align="center" class=l15>基努伊海底通路</td>',m,re.S)
 core=plain('强恩一族洞窟'+row)
 require(core.startswith('强恩一族洞窟285，926构造：地上8楼敌Lv：Lv30～40敌种：山贼59.齐尔格尔顿72.格鲁西斯有强恩一族任务'),'Selected ecology row changed')
 transitions=[{'from':a,'to':b,'coord':[int(x),int(y)]} for a,b,x,y in re.findall(r'([1-7]F)-([1-7]F|出口)\((\d+)\.(\d+)\)',core)]
 require(len(transitions)==13,'Thirteen directed printed transitions required')
 gates=re.findall(r'([456]F)-([567]F)要说密语\(([^)]+)\)',core)
 require(gates==[('4F','5F','红色月亮的光芒'),('5F','6F','蓝色山脉即力量'),('6F','7F','白色之风即速度')],'Map password row changed')
 return core,{'name_as_written':'强恩一族洞窟','world_coord':[285,926],'aboveground_floor_count_as_reported':8,
  'enemy_level_as_reported':[30,40],'enemy_entries_as_written':['山贼','59.齐尔格尔顿','72.格鲁西斯'],
  'catalogue_numbers_are_original_ids':False,'transitions_in_printed_row_order':transitions,
  'password_transitions':[{'from':a,'to':b,'password':c} for a,b,c in gates],
  'runtime_pathfinding_or_reverse_edges_verified':False}


def fingerprint(core):return {'characters':len(core),'utf8_bytes':len(core.encode()),'sha256':sha(core.encode())}


def derive(s1,s2):
 core,body,pairs=article(s1);require(all(plain(v) in core for v in CLAUSES),'Source family/gate/reward clause changed')
 row,ecology=map_row(s2)
 guards=[{'exit_floor':int(f),'local_coord':[int(x),int(y)],'password':p} for f,x,y,p in re.findall(
  r'([456])楼出口附近.*?山贼守卫（东(\d+)，南(\d+)）.*?暗号"([^"]+)"才能继续前进',core)]
 require(guards==[{'exit_floor':f,'local_coord':c,'password':p} for f,c,p in
  [(4,[11,54],'红色月亮的光芒'),(5,[51,5],'蓝色山脉即力量'),(6,[8,23],'白色之风即速度')]],'Floor/guard/password association changed')
 return {'name':'强恩一族','recommended_level_as_reported':50,'hard_level_gate':None,'prerequisite_not_specified_in_article':True,
  'transport':['步行','骑宠'],'feather_field_as_written':'无',
  'village':{'name':'奇喀喀村','two_coordinate_literals':[[140,1007],[124,1048]],'coordinate_roles':None},
  'npcs':[
   {'occurrence':'FRIEND','label':'吉德的朋友','name':'凯伊','local_coord':[58,66],'location':'村长家旁'},
   {'occurrence':'FATHER','label':'吉德','name':'吉德','local_coord':None,'location':'村长家深处的房间'},
   {'occurrence':'SON','label':'吉德的儿子','name':None,'local_coord':None,'location':'NOT_SPECIFIED'},
   {'occurrence':'CHIEF','label':'强恩','name':'强恩','local_coord':[68,7],'location':'洞窟深处'},
   {'occurrence':'FOSTER_MOTHER','label':'强恩的妻子','name':None,'local_coord':[70,8],'location':'DUNGEON_LOCATION_AS_COORDINATE_ONLY'},
   {'occurrence':'DAUGHTER','label':'沙拉','name':'沙拉','local_coord':None,'location':'沙拉的房间'}],
  'backstory':{'kidnapping_years_before_as_told':16,'daughter_age_then_as_told':4,'current_age_computed':None,
   'mother_died_years_after_as_told':2,'mother_name_as_father_says':'卡那','destination':'乌鲁力村',
   'mountain_labels_by_context':{'friend_route':'阿尔鲁山南侧','father_thief_location':'阿鲁姆山'},
   'mountain_native_alias_verified':False,'north_south_groups_as_written':['北岛梦德一族','南岛强恩一族']},
  'dungeon':{'entrance_world_coord':[285,926],'direction_from_village':'东北',
   'password_guards':guards,
   'optional_document':{'name':'盗贼的秘密文件','purpose':'CONTAINS_PASSWORDS','required_for_passing':False,
    'random_encounter_labels':['伯恩','玛琼拉','卡鲁德'],'encounter_scope_as_written':'四楼以后',
    'drop_as_reported':'POSSIBLE_AFTER_DEFEAT','drop_probability_or_consumption':None},
   'fixed_blocking_trio':{'floor':7,'labels':['卡鲁德','伯恩','玛琼拉'],'condition':'DEFEAT_JOINT_ATTACK_BEFORE_CHIEF',
    'same_instances_as_random_encounters':None,'guaranteed_document_drop':None},
   'floor_caption_labels':[str(i)+'楼' for i in range(1,8)]+['沙拉的房间'],'total_floor_count_from_article':None,
   'article_ecology':{'enemy_level_as_reported':[31,48],'labels':['卡鲁德','伯恩','玛琼拉','山贼','格鲁西斯','格尔顿']},
   'map_table_source':ecology,'ecology_difference_resolution':None,'room_equals_eighth_floor':None},
  'family_outcome':{'wife_requests_daughter_choice':True,'daughter_choice_as_reported':'STAY_WITH_FOSTER_PARENTS',
   'player_reports_choice_to_chief':True,'escort_to_birth_father':False,'letter_to_birth_father':'给双亲的信',
   'talk_again_to_chief_and_wife_before_return':True,'birth_father_response':'GLAD_DAUGHTER_ALIVE',
   'letter_title_proves_birth_mother_alive':False,'developer_intent_or_original_quest_flags':None},
  'item_flow':[
   {'name':'开在奇喀喀的花','from':'FRIEND','to':'FATHER'},
   {'name':'母亲的发饰','from':'SON','to':'DAUGHTER'},
   {'name':'给双亲的信','from':'DAUGHTER','to':'FATHER'},
   {'name':'卡娜的木笛','from':'FATHER','to':'PLAYER','stats_as_written':{'魅':2,'毒':5,'石':-5,'眠':5},
    'spirit_as_written':'复活精灵','spirit_level':2,'abbreviated_status_semantics':None}],
  'chief_reward':{'kind':'RANDOM_ONE_ITEM_AS_GUIDE_CLAIM','caption_sample':'属于山贼的羽饰','sample_is_guaranteed':False,'full_prize_pool':None},
  'exact_game_build':None,'original_map_npc_quest_item_ids':None,'repeatability_reset_and_item_consumption':None,
  'original_server_runtime_verified':False,
  'image_links':{'full_thumbnail_pairs':20,'selected_full_http':[pairs[i][0] for i in (8,11)],
   'selected_thumbnails_http':[pairs[i][1] for i in (8,11)],'unacquired_full_images':18},
  'fingerprints':{'S1_business_body':fingerprint(core),'S2_selected_row':fingerprint(row)}}


def pin(path):
 b=(ROOT/path).read_bytes();return {'path':path,'bytes':len(b),'sha256':sha(b),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}


def comparison():
 parents=[json.loads((ROOT/p).read_text()) for p in PARENTS[:2]]
 return {'liuli':{'schema':parents[0]['schema'],'family_reunion_or_father_death_backfilled':False},
  'mengde':{'schema':parents[1]['schema'],'north_south_relation_is_textual':True,'same_native_faction_ids':False,
   'mengde_adult_ceremony_or_reward_order_backfilled':False},
  'two_portal_pages':{'same_exact_build_verified':False,'independent_authors_verified':False,
   'enemy_level_ranges_preserved_separately':True,'geerdun_labels_forced_to_alias':False,
   'seven_captions_vs_eight_floor_table_is_proven_contradiction':False},'modern_adoption_decided':False}


def catalog(ex):
 rows=[('quest','quests','DOCUMENTARY_FAMILY_CHOICE_QUEST',ex,['S1','S2'])]
 rows += [(n['occurrence'],'npcs','DOCUMENTARY_STORY_NPC_OCCURRENCE',n,['S1']) for n in ex['npcs']]
 rows += [('gate-'+str(n['exit_floor']),'npcs','DOCUMENTARY_UNNAMED_PASSWORD_GUARD_OCCURRENCE',n,['S1','S2']) for n in ex['dungeon']['password_guards']]
 rows += [('trio','npcs','DOCUMENTARY_BLOCKING_GROUP_NOT_ONE_NATIVE_NPC',ex['dungeon']['fixed_blocking_trio'],['S1']),
  ('cave','maps','DOCUMENTARY_SOURCE_SCOPED_CAVE_RELATIONS',ex['dungeon'],['S1','S2'])]
 rows += [('item-'+str(i),'items','DOCUMENTARY_ITEM_FLOW_NOT_NATIVE_MASTER',v,['S1']) for i,v in enumerate(ex['item_flow'])]
 rows += [(im['id'],'screens','DOCUMENTARY_STATIC_SCREEN',{'image':im,'observation':v},['S1',im['id']]) for im,v in zip(IMAGES,VISUAL)]
 return [{'record_id':'CN2003-R83-'+ident,'entity_type':kind,'collection':coll,'version_profile':PROFILE,
  'source_refs':refs,'verification_status':'DATED_PORTAL_GUIDE_OR_STATIC_SCREEN_NOT_SERVER_RUNTIME',
  'rights_status':'RESEARCH_METADATA_NOT_RELEASE_APPROVED','record_revision':1,'game_ids':None,'content':content}
  for ident,coll,kind,content,refs in rows]


def semantic(ex):return {k:v for k,v in ex.items() if k!='fingerprints'}
SEMANTIC_SHA='c75c784ead632a2204794de0080df98de1b54ebb3de9013ddf9619e3a3a0c96b'


def validate(r):
 require(r['schema']=='stoneage.cn2003_qiang_en.source.r1' and r['version_profile']==PROFILE,'Version/schema changed')
 require(r['sources']==SOURCES and r['images']==IMAGES and r['visual_observations']==VISUAL and r['negative_boundaries']==BOUNDARIES,'Source/visual/authority boundaries changed')
 require(r['parent_pins']==[pin(p) for p in PARENTS] and r['parser_pin']==pin(PARSER),'Original parent/parser bytes changed')
 require(r['comparison']==comparison(),'Cross-source distinctions changed')
 require(sha(json.dumps(semantic(r['extraction']),ensure_ascii=False,sort_keys=True).encode())==SEMANTIC_SHA,'Documentary family contract changed')
 require(r['catalog_records']==catalog(r['extraction']),'Catalog detached from source semantics')
 contract=json.loads((ROOT/PARENTS[-1]).read_text())['future_website']
 require(len(r['catalog_records'])==18 and len({v['record_id'] for v in r['catalog_records']})==18,'Catalog count/IDs changed')
 require(all(set(contract['record_contract']['required']).issubset(v) and v['collection'] in contract['required_collections'] for v in r['catalog_records']),'Archive required fields/collections changed')


MUTATIONS=[('S1',a,b) for a,b in [
 ('建议等级50级','等级限制50级'),('东140，南1007','东139，南1007'),('东58，南66','东58，南67'),
 ('16年前被绑架','15年前被绑架'),('于是在两年后去世','于是在三年后去世'),('阿尔鲁山南侧','阿鲁姆山南侧'),
 ('开在奇喀喀的花','普通的花'),('东285，南926','东286，南926'),('东11，南54','东11，南55'),
 ('东51，南5','东52，南5'),('东8，南23','东8，南24'),('红色月亮的光芒','红色月亮的力量'),
 ('蓝色山脉即力量','蓝色山脉即速度'),('白色之风即速度','白色之风即力量'),
 ('就有可能获得盗贼的秘密文件','就一定获得盗贼的秘密文件'),('不一定需要获得秘密文件','一定需要获得秘密文件'),
 ('四楼以后会随机遇到','一楼以后会随机遇到'),('在击败三人联合的攻击后','不必击败三人联合的攻击'),
 ('东68，南7','东69，南7'),('东70，南8','东71，南8'),('四岁的小孩','五岁的小孩'),
 ('更希望陪在强恩双亲的身边，不想离开他们','更希望返回亲生父母身边，离开他们'),
 ('会随机赠送勇者一个道具','会固定赠送勇者一个道具'),('给双亲的信','给养父母的信'),
 ('卡那在天之灵','卡那听说此事'),('魅+2毒+5石-5眠+5','魅+2毒+5石+5眠+5'),
 ('复活精灵Lv2','复活精灵Lv3'),('31~48级','30~40级')]]+[
 ('S2','地上8楼','地上7楼'),('S2','Lv30～40','Lv31～48'),('S2','59.齐尔格尔顿','59.格尔顿'),
 ('S2','(49.4)','(49.5)'),('S2','7F-6F','6F-7F'),('S2','白色之风即速度','白色之风即力量')]


def audit(inputs,expected):
 target=semantic(expected)
 for key,old,new in MUTATIONS:
  text=inputs[key].decode('gb18030');require(old in text,'Missing real source mutation: '+old)
  changed=dict(inputs);changed[key]=text.replace(old,new).encode('gb18030')
  try:actual=derive(changed['S1'],changed['S2'])
  except (ValueError,IndexError):continue
  require(semantic(actual)!=target,'Only fingerprint noticed source meaning change: '+old)
 for replacement in ('','<script>'+OPTIONAL+'</script>'):
  changed=inputs['S1'].decode('gb18030').replace(OPTIONAL,replacement)+'<div>'+OPTIONAL+'</div>'
  try:derive(changed.encode('gb18030'),inputs['S2'])
  except ValueError:pass
  else:raise ValueError('Outside/hidden text repaired optional document clause')
 # A neighboring map entity cannot repair this selected row's ecology.
 changed=inputs['S2'].decode('gb18030').replace('Lv30～40','Lv99～99')+'<div>敌Lv：Lv30～40</div>'
 try:derive(inputs['S1'],changed.encode('gb18030'))
 except ValueError:pass
 else:raise ValueError('Outside map row repaired ecology')
 for key in ('S1','S2'):
  changed=dict(inputs);changed[key]+=b'<script>outside=1</script>'
  require(derive(changed['S1'],changed['S2'])==expected,'Peripheral script changed meaning')
 return {'semantic_mutations_without_all_fingerprints':len(MUTATIONS),'hidden_and_outside_article_counterexamples':2,
  'outside_map_row_counterexamples':1,'outside_script_positives':2}


def inspect_images(inputs):
 for expected in IMAGES:
  raw=inputs[expected['id']]
  with Image.open(io.BytesIO(raw)) as im:
   im.load();actual={'bytes':len(raw),'sha256':sha(raw),'size':list(im.size),'format':im.format,'mode':im.mode,'frames':getattr(im,'n_frames',1)}
  require(all(expected[k]==v for k,v in actual.items()),'Reviewed screenshot bytes/full decode changed')


def replay(inputs,r):
 validate(r);ex=derive(inputs['S1'],inputs['S2']);require(ex==r['extraction'],'Family/ecology extraction or fingerprint changed');inspect_images(inputs)
 for s in SOURCES:require(len(inputs[s['id']])==s['bytes'] and sha(inputs[s['id']])==s['sha256'],'Exact body bytes changed')
 refs={v['id']:v for v in SOURCES+IMAGES}
 return {'schema':'stoneage.cn2003_qiang_en.replay.r1','inputs':[{'id':k,'url':refs[k]['url'],'bytes':len(v),'sha256':sha(v)} for k,v in inputs.items()],
  'extraction':ex,'images':IMAGES,'visual_observations':VISUAL,'comparison':comparison(),'catalog_records':catalog(ex),
  'audit':audit(inputs,ex),'original_html_or_assets_in_output':False,'original_server_runtime_verified':False}


def read_inputs(directory=None):
 result={}
 for v in SOURCES+IMAGES:
  key,url=v['id'],v['url']
  if directory:result[key]=(Path(directory)/(key+('.html' if key.startswith('S') else '.jpg'))).read_bytes()
  else:
   with urllib.request.urlopen(url,timeout=50) as h:
    require(h.status==200 and h.url==url,'Exact acquisition URL/status changed');result[key]=h.read()
 return result


def main():
 p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--fetch',action='store_true');g.add_argument('--input-dir');p.add_argument('--output',required=True);a=p.parse_args()
 r=json.loads(REPORT.read_text());out=replay(read_inputs(a.input_dir),r)
 path=Path(a.output);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print('R83 Qiang En family choice, optional document, three gates and source-scoped ecology replayed; original flags/IDs/runtime remain unknown.')


if __name__=='__main__':main()
