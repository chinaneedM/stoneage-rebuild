"""R88: Eden zoo rescue, moving named actors, item gates and source stat ambiguity."""
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
STEM='STONEAGE-CN2003-ZOO-RESCUE'
REPORT=ROOT/f'research/recovered/{STEM}-SOURCE-R1.json'
URL='https://games.sina.com.cn/zhqu/sta/article/2003-06-03/10646.shtml'
PROFILE='CN_SINA2003_EDEN_ZOO_RESCUE_EXACT_BUILD_UNKNOWN'
PARSER='tools/stoneage_jp2005_treasure_source.py'
PARENTS=['research/recovered/STONEAGE-CN2001-2003-SHELL-QUEST-SOURCE-R1.json',
 'research/recovered/STONEAGE-WAEI-CN20-NEW-PET-FINITE-CATALOG-R1.json',
 'research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json']
TITLE='《石器时代》任务功略-动物园任务'
SOURCE={'url':URL,'http_status':200,'no_redirect':True,'bytes':72640,
 'sha256':'e92f92126182fb0834f7ec329a615cb1b7629e54da1de1943dd016af828ad046',
 'encoding':'GB18030_STRICT','visible_title':TITLE,'visible_publication':'2003-06-03 17:58',
 'publisher_field':'新浪游戏','named_original_author':None,'submission_link_label':'我要投稿',
 'authority':'DATED_PORTAL_GUIDE_NOT_AUTHENTICATED_OPERATOR_SCRIPT',
 'official_authorship_verified':False,'actual_operator_script_acquired':False,
 'current_bytes_authenticate_2003_original':False,'exact_client_build':None}
IMAGES=[{'id': 'I1', 'url': 'https://image2.sina.com.cn/gm/newgames/0303/images/dongwu0603_08.jpg', 'http_status': 200, 'no_redirect': True, 'bytes': 108055, 'sha256': '3cdfea6514804d9ee9d7a0dd6b72c40df4bc2dafbf5c94654a190360dda82301', 'format': 'JPEG', 'mode': 'RGB', 'size': [640, 480], 'frames': 1}, {'id': 'I2', 'url': 'https://image2.sina.com.cn/gm/newgames/0303/images/dongwu0603_020.jpg', 'http_status': 200, 'no_redirect': True, 'bytes': 88503, 'sha256': '1afc3b40e06f874c4b5b016bc2c852769ded5bcfa6c04a19bccee75d39425b8c', 'format': 'JPEG', 'mode': 'RGB', 'size': [640, 480], 'frames': 1}]
VISUAL=[{'id': 'I1', 'manual_visual_review': True, 'kind': 'STATIC_INVENTORY_SHOVEL_TOOLTIP', 'displayed_item_name': '可以挖萝卜的铲子', 'displayed_description': '好用的铲子', 'item_selected': True, 'npc_name_readable': False, 'original_item_id_or_actual_delivery_verified': False, 'original_sprite_animation_or_native_id_verified': False, 'historical_2003_pixels_authenticated': False, 'interaction_or_item_effect_tested': False}, {'id': 'I2', 'manual_visual_review': True, 'kind': 'STATIC_NAMED_RESCUED_PET_STATUS_SAMPLE', 'displayed_pet_name': '动物园养的拉斯基', 'displayed_level': 1, 'displayed_next': 2, 'displayed_stats': {'耐久力': {'current': 17, 'maximum': 17}, '攻击力': 2, '防御力': 3, '敏捷力': 2, '忠诚度': 100}, 'visible_nonempty_element_bars': ['火属性', '风属性'], 'element_numeric_ratios': None, 'appearance': 'RED_RABBITLIKE_FIGURE', 'one_displayed_pet_proves_species_initial_stats_or_growth': False, 'npc_name_readable': False, 'actual_combat_handover_or_reward_verified': False, 'original_sprite_animation_or_native_id_verified': False, 'historical_2003_pixels_authenticated': False, 'interaction_or_item_effect_tested': False}]
BOUNDARIES={k:False for k in ('official_authorship_verified','current_bytes_authenticate_2003_original',
 'recommended90_is_hard_gate','moving_actor_coordinates_share_one_world_frame','restart_notes_are_observed_server_behavior',
 'bert_five_points_prove_timed_closed_cycle','rabbit_twenty_two_points_prove_random_uniform_spawn',
 'all_buipang_are_quest_leierpang','all_popodun_levels_are_valid','correct_feed_guarantees_encounter_or_capture',
 'hit_first_advice_is_capture_probability_formula','shell_is_consumed_on_every_dialogue','bad_white_radish_spellings_are_verified_native_aliases',
 'shovel_or_red_radish_confiscation_is_global_item_rule','after_fifth_narrative_is_verified_sixth_server_counter',
 'forestry_clue_is_actual_lasiji_location','collar_and_black_clothes_are_guaranteed_drop_rates',
 'duplicate_attack700_is_silently_defense700','enemy_samples_are_pet_master_stats','reported_lower_bounds_are_exact_values',
 'map_header0_64_corrected_to_floor_entry20_64','report_safety_after_pet_return_still_guarantees_armour',
 'buipang_newborn_means_verified_level1_stats','static_screen_proves_dialogue_choices_reward_or_combat_execution',
 'web_catalog_positions_are_native_ids_or_same_instances','original_html_or_assets_committed','stage_b_started')}
SAFETY='玩家们将宠物们送回动物园之前，一定要记得先带救出的拉斯基去跟里拉拉报平安'
CLAUSES=['建议等级90级','特殊要求：解过金飞任务','长毛象公车（萨姆吉尔村←→玛丽娜丝渔村）',
 '走失的动物分别是“雷尔胖”、“波波顿”跟“拉斯基”','原本名叫布伊胖的它，现在大家都叫它雷尔胖','雷尔大人的爱宠','这里的格尔希洛并没有林务局那里的凶悍',
 '他会交给你“雷尔胖专用饲料”','员工宿舍后面（东75，南170）抓到蓝色的雷尔胖',
 '布伊太郎的鉴定通过后','将雷尔胖专用饲料收回','肉食性饲料2','水池边（东170，南181）找到波波顿',
 '饲料桶中找到草食性饲料','在身上只带一种正确的饲料','如果一次带很多种饲料在身上，将很难遇到想抓的宠物',
 '先打一下想要抓的宠物，再去抓，就会比较好抓到','只有“雷尔胖”才是真正要抓的宠物','只有“等级1”的波波顿才是真正的波波顿',
 '鲛岛太郎','他会在园长室隔壁等你','它并没有专用饲料','必须拿着“不可思议的贝壳”，才能跟白兔子说话',
 '北岛弥生与日美子的友谊','南岛哥亚山事件','吉鲁岛小猪爱情故事','藏匿的22处地点',
 '勇者必须和白兔子“里拉拉”叫“啦啦”','第一颗“白菜”会说话','总共有5个地方，而且他是照着顺序下去走的',
 '先对着他喊一下“伯特”','对着伯特说“铲子”','给你一把“可以挖萝卜的铲子”','可以挖到白萝卜跟红萝卜3',
 '只要将铲子丢在地上，它就会消失不见','再跟伯特说“铲子”','再给你一把铲子',
 '拿着红萝卜3给伯特鉴定','柯奥产的红萝卜4','红萝卜4和不太差的白萝卜','并试着对伯特说“啦啦”',
 '一根“上等白萝卜”并收回你的红萝卜4和还不差的白萝卜',
 '先把铲子丢了','把铲子和上等白萝卜收走','身上也不可以有红萝卜','收走红萝卜和上等白萝卜',
 '萝卜可是会像铲子一样消失得无影无踪','找到它第二次时也是如此','第三次时里拉拉已经开始有了戒心',
 '第四次找到里拉拉时','第五次找到里拉拉时','拉斯基的名字“拉拉”','主谋就是里拉拉',
 '顺便也把布伊胖跟波波顿给放走','林务局不过是个晃子','高兴地将项圈收走','伊甸园南边的雷尔大雕像',
 '里拉拉拿走黑色的服','走到4楼之后','取得「黑色的旗”','上到第五楼后','领导者“席格”展开激战',
 '身为塔尔塔战士团一员的席格','为了寻找失踪的老团长','认为动物园真正的面目是可怕的驯兽中心',
 '乔装成不良少年','并不在他们的规划中','席格最后还是会交出拉斯基',
 '先带拉斯基去跟里拉拉报平安','将三只宠物送回动物园','一只刚出生的“布伊胖”',
 '收下咬过的白萝卜','赠送“里拉拉赠送的铠”',SAFETY,'防+40敏+10恩惠的精灵Lv4',
 '伊甸地下信道（不良少年洞窟）坐标：（东0，南64）怪物等级：70～90级怪物种类：席格、不良少年、凶悍的格尔希洛']


def article(raw):
 p=VisibleMarkup();p.feed(raw.decode('gb18030',errors='strict'));text=''.join(p.parts)
 middle=one(r'<!-- include 中间内容 begin -->(.*?)<!-- include 中间内容 end -->',text,re.S)
 require(TITLE in plain(middle),'Visible title changed')
 require(plain(one(r'<!-- include 发布时间 begin -->(.*?)<!-- include 发布时间 end -->',middle,re.S))==plain(SOURCE['visible_publication']),'Publication changed')
 require('作者：新浪游戏' in plain(middle) and '我要投稿' in plain(middle),'Publisher changed')
 body=one(r'<td width=500 class=l15z><span>(.*?)</td>\s*</tr>\s*</table>\s*<br><br>',middle,re.S)
 core=plain(body);require(core.startswith('1.等级要求：') and core.endswith('伊甸地下信道第五层'),'Quest body boundary changed')
 pairs=re.findall(r'<a href="(http://image2\.sina\.com\.cn/[^" ]+)" target="_blank"><img src="(http://image2\.sina\.com\.cn/[^" ]+)" border="0" width="150" height="113">',body)
 require(len(pairs)==26 and len(set(pairs))==26,'Twenty six actual full/thumbnail pairs required')
 require([pairs[i][0].replace('http:','https:',1) for i in (7,19)]==[v['url'] for v in IMAGES],'Selected actual image links changed')
 return core,body


def moving_table(body,heading,count,interior_start=None):
 table=one(re.escape(heading)+r'</p>\s*<table[^>]*>(.*?)</table>',body,re.S)
 result=[]
 for row in re.findall(r'<tr\b[^>]*>(.*?)</tr>',table,re.S):
  cells=[plain(v) for v in re.findall(r'<td\b[^>]*>(.*?)</td>',row,re.S)]
  if cells==['坐标','备注']:continue
  require(len(cells)==2,'Moving actor row shape changed')
  x,y=map(int,one(r'（(\d+),(\d+)）',cells[0]));note=cells[1]
  result.append({'coordinate':[x,y],'note_as_written':note,
   'coordinate_scope':'INTERIOR_AS_NAMED_NOT_WORLD' if interior_start is not None and len(result)>=interior_start else 'EDEN_OUTDOOR_AS_GUIDE',
   'restart_only_as_guide_claim':'服务器重开机' in note,'original_map_id':None})
 require(len(result)==count,'Moving actor site count changed');return result


def enemy_tables(body):
 labels=['凶悍的格尔希洛（林务局）','不良少年','凶悍的格尔希洛（不良少年洞窟）','席格'];out=[]
 tables=[plain(v) for v in re.findall(r'<table\b[^>]*>(.*?)</table>',body,re.S)]
 for label in labels:
  found=[v for v in tables if v.startswith(label+'等级：')];require(len(found)==1,'One source enemy sample required: '+label)
  c=found[0][len(label):];stats=[]
  for key,value in re.findall(r'(等级|耐久力|攻击力|防御力|敏捷力)[:：]?(.*?)(?=等级|耐久力|攻击力|防御力|敏捷力|技能：)',c):
   stats.append({'label_as_written':key,'value_as_written':value})
  skills=one(r'技能：(.*)$',c)
  out.append({'context_label':label,'ordered_stat_entries':stats,'skills_as_written':skills.split('、'),
   'duplicate_attack_label_unresolved':label=='席格','native_enemy_or_pet_master_id':None})
 return out


def derive(raw):
 core,body=article(raw);require(all(plain(v) in core for v in CLAUSES),'Quest story, condition or reward clause changed')
 rabbit=moving_table(body,'白兔子“里拉拉”现形地：',22,16);bert=moving_table(body,'园丁伯特出没地：',5)
 floors=[{'floor_as_written':f,'entry_local_coord':[int(x),int(y)],'exit_local_coord':[int(a),int(b)]} for f,x,y,a,b in
  re.findall(r'([一二三四])楼入口（东(\d+)，南(\d+)）出口（东(\d+)，南(\d+)）',core)]
 require(len(floors)==4,'Four printed floor entry/exit pairs required')
 npcs=[{'label':label,'role':role,'native_id':None} for label,role in [('沙利斯园长','QUEST_GIVER_AND_PET_RETURN'),('布伊太郎','LEIERPANG_KEEPER_AND_APPRAISER'),
 ('鲛岛太郎','POPODUN_APPRAISER'),('里拉拉','MOVING_WHITE_RABBIT_INFORMATION_AND_ARMOUR'),('伯特','MOVING_GARDENER_SHOVEL_AND_RADISH'),('白菜','TALKING_PLANT_HINT_NOT_NATIVE_NPC_PROOF'),('席格','DISGUISED_RESCUER_COMBAT_AND_LASIJI_HANDOVER')]]
 npcs[3]['sites_as_reported']=rabbit;npcs[4].update(sites_as_reported=bert,ordered_movement_as_claimed=True,cycle_period_and_actual_path=None)
 return {'name':'动物园任务','recommended_level':90,'hard_level_gate':None,'prerequisite_as_reported':'COMPLETE_GOLD_FLYING_QUEST',
  'feather_field_locations_as_written':['玛丽娜丝渔村','卡鲁它那村','福尔德村'],'npcs':npcs,
  'rescue_targets':[
   {'name':'雷尔胖','previous_name_in_story':'布伊胖','owner_as_told':'雷尔大人','appearance_as_written':'蓝色','outdoor_coordinate':[75,170],
    'place':'员工宿舍后面','valid_target':'NAMED_LEIERPANG_NOT_OTHER_BUIPANG','feed':'雷尔胖专用饲料','alternative_feed_as_reported':'草食性饲料',
    'appraiser':'布伊太郎','feed_reclaimed_after_appraisal':True,'pet_consumed_at_appraisal':None},
   {'name':'波波顿','outdoor_coordinate':[170,181],'place':'东南方水池边','valid_target_level_as_reported':1,
    'feed':'肉食性饲料2','feed_location':'园长室最里面房间的饲料桶','appraiser':'鲛岛太郎','appraiser_place':'园长室隔壁'},
   {'name':'拉斯基','appearance_as_written':'红兔子','nickname_as_written':'拉拉','dedicated_feed':None,
    'acquisition_as_reported':'SIGE_HANDOVER_AFTER_FIFTH_FLOOR_BATTLE','capture_coordinate_or_native_id':None,'single_status_screen_sample_ref':'I2'}],
  'capture_advice':{'one_correct_feed_at_a_time':True,'carrying_many_feeds':'DIFFICULT_TO_ENCOUNTER_DESIRED_PET_AS_GUIDE_CLAIM',
   'hit_once_before_capture':'GUIDE_ADVICE_NOT_PROBABILITY_FORMULA','encounter_or_capture_rates':None},
  'shell_communication':{'item':'不可思议的贝壳','needed_as_reported':True,
   'listed_sources':['北岛弥生与日美子的友谊','南岛哥亚山事件','吉鲁岛小猪爱情故事'],'consumption_or_all_other_prerequisites':None},
  'gardener_and_radish_flow':{'spoken_tokens':['伯特','铲子','啦啦'],'shovel':'可以挖萝卜的铲子',
   'dig_products_as_reported':['白萝卜','红萝卜3'],'show_red3_to_bert':True,'bring_red4_from':'柯奥',
   'white_radish_wordings_as_written':['不太差的白萝卜','还不差的白萝卜'],'native_alias_verified':False,
   'exchange_inputs_as_written':['红萝卜4','还不差的白萝卜'],'exchange_output':'上等白萝卜','exchange_quantity_as_reported':1,
   'shovel_ground_disappears_and_reacquire_by_token':True,'radish_ground_disappears_as_reported':True,
   'before_rabbit_discard_shovel':True,'carrying_shovel_confiscates':['铲子','上等白萝卜'],
   'carrying_red_radish_confiscates':['红萝卜','上等白萝卜'],'exact_item_ids_inventory_predicates_and_reset_flags':None},
  'rabbit_story_order':[
   {'source_occurrence':'FIRST','event':'BITES_RADISH_AND_RUNS'}, {'source_occurrence':'SECOND','event':'BITES_AGAIN'},
   {'source_occurrence':'THIRD','event':'SUSPICIOUS_AND_WARNS'}, {'source_occurrence':'FOURTH','event':'ADMITS_LALA_NAME_THEN_RUNS'},
   {'source_occurrence':'FIFTH','event':'REVEALS_LASIJI_LALA_NICKNAME_AND_ESCAPE_PLOT'},
   {'source_occurrence':'FOLLOWUP_AFTER_FIFTH_NOT_NUMBERED_SERVER_COUNTER','event':'ADMITS_RELEASED_ALL_THREE_AND_GIVES_FORESTRY_DECOY'}],
  'clue_item_flow':[{'from':'FORESTRY_GORILLA_BATTLE','item':'格尔希洛的项圈','to':'里拉拉','reclaimed':True,'next_clue':'大雕像'},
   {'from':'ASK_RABBIT_AGAIN','spoken':'啦啦','next_clue':'伊甸园南边的雷尔大雕像'},
   {'from':'STATUE_DELINQUENT_BATTLE','item':'黑色的服','to':'里拉拉','reclaimed':True},
   {'from':'ASK_RABBIT_AGAIN','next_clue':'动物园后方的不良少年老巢'},
   {'from':'DUNGEON_FLOOR4','item':'黑色的旗','purpose_as_reported':'PROVE_ABILITY_TO_BRING_LASIJI_BACK','consumption_or_drop_rate':None}],
  'sige_story':{'group':'塔尔塔战士团','motive_as_told':'FIND_MISSING_OLD_LEADER','zoo_training_center':'CHARACTER_SUSPICION_NOT_OBJECTIVELY_PROVEN',
   'disguised_as_delinquents_to_rescue_animals':True,'rabbit_release_plan_was_theirs':False,'hands_over_lasiji_after_defeat':True,'original_dialogue_or_flags':None},
  'enemy_samples':enemy_tables(body),'enemy_comparison':{'prose_claim':'DEN_GORILLA_LESS_FIERCE_THAN_FORESTRY','numeric_samples_harmonized_to_prose':False},
  'dungeon':{'name_as_written':'伊甸地下信道（不良少年洞窟）','header_coordinate':[0,64],'floor_pairs':floors,
   'header_vs_floor1_entry_resolution':None,'source_enemy_level_range':[70,90],'source_enemy_labels':['席格','不良少年','凶悍的格尔希洛'],
   'fifth_floor_battle':'席格','runtime_map_ids_or_reverse_transitions':None},
  'completion_order':{'report_lasiji_safety_to_rabbit_before_returning_three':True,'return_all_three_to':'沙利斯园长',
   'zoo_reward':{'name':'布伊胖','quantity_as_reported':1,'description_as_written':'刚出生','verified_numeric_level_or_stats':None},
   'armour_followup':{'turn_in':'里拉拉咬过的白萝卜','recipient':'里拉拉','item_wordings':['里拉拉赠送的铠','里拉拉的铠'],
    'stats_as_written':{'防':40,'敏':10},'spirit_as_written':'恩惠的精灵','spirit_level':4,'missed_safety_report_loses_armour_as_guide_claim':True}},
  'image_links':{'actual_full_thumbnail_pairs':26,'selected_full_indexes_one_based':[8,20],'other_full_images_not_acquired':24},
  'exact_client_build':None,'original_server_runtime_verified':False,
  'core_fingerprint':{'characters':len(core),'utf8_bytes':len(core.encode()),'sha256':sha(core.encode())}}


def pin(path):
 b=(ROOT/path).read_bytes();return {'path':path,'bytes':len(b),'sha256':sha(b),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}


def comparison():
 return {'shell_quest':{'schema':json.loads((ROOT/PARENTS[0]).read_text())['schema'],'shell_item_is_textual_reference_not_native_id_join':True,
   'southern_and_jilu_complete_quest_rules_backfilled':False},
  'cn20_web_pets':{'schema':json.loads((ROOT/PARENTS[1]).read_text())['schema'],
   'lilara_lasiji_gorilla_name_overlap_proves_same_native_instances':False,'web_positions_are_native_pet_ids':False},
  '2024_mobile_reenactment_or_modern_private_server_rules_backfilled':False,'modern_adoption_decided':False}


def catalog(ex):
 rows=[('quest','quests','DOCUMENTARY_ZOO_RESCUE_FLOW',ex,['S1'])]
 rows += [('npc-'+str(i),'npcs','DOCUMENTARY_NAMED_ACTOR_OR_TALKING_OBJECT',v,['S1']) for i,v in enumerate(ex['npcs'])]
 rows += [('target-'+str(i),'pets','DOCUMENTARY_NAMED_RESCUE_TARGET_NOT_SPECIES_MASTER',v,['S1']) for i,v in enumerate(ex['rescue_targets'])]
 rows += [('reward','pets','DOCUMENTARY_NEWBORN_PET_REWARD',ex['completion_order']['zoo_reward'],['S1']),
  ('dungeon','maps','DOCUMENTARY_QUEST_FLOOR_COORDINATES',ex['dungeon'],['S1']),
  ('armour','items','DOCUMENTARY_ORDER_DEPENDENT_ARMOUR_REWARD',ex['completion_order']['armour_followup'],['S1'])]
 rows += [(v['id'],'screens','DOCUMENTARY_STATIC_NPC_SCREEN',{'image':v,'observation':obs},['S1',v['id']]) for v,obs in zip(IMAGES,VISUAL)]
 return [{'record_id':'CN2003-R88-'+i,'entity_type':t,'collection':coll,'version_profile':PROFILE,'source_refs':refs,
  'verification_status':'PORTAL_GUIDE_OR_STATIC_SCREEN_NOT_SERVER_RUNTIME','rights_status':'RESEARCH_METADATA_NOT_RELEASE_APPROVED',
  'record_revision':1,'game_ids':None,'content':v} for i,coll,t,v,refs in rows]


def semantic(ex):return {k:v for k,v in ex.items() if k!='core_fingerprint'}
SEMANTIC_SHA='55ddb32f4277b1b438799918e9b72b15ee8f7fb1557394869248e922b59f04fc'


def validate(r):
 require(r['schema']=='stoneage.cn2003_zoo_rescue.source.r1' and r['version_profile']==PROFILE,'Version/schema changed')
 require(r['source']==SOURCE and r['images']==IMAGES and r['visual_observations']==VISUAL and r['negative_boundaries']==BOUNDARIES,'Source/visual/authority boundaries changed')
 require(r['parent_pins']==[pin(p) for p in PARENTS] and r['parser_pin']==pin(PARSER),'Parent/parser bytes changed')
 require(r['comparison']==comparison(),'Cross-source distinction changed')
 require(sha(json.dumps(semantic(r['extraction']),ensure_ascii=False,sort_keys=True).encode())==SEMANTIC_SHA,'Documentary zoo contract changed')
 require(r['catalog_records']==catalog(r['extraction']),'Catalog detached')
 c=json.loads((ROOT/PARENTS[-1]).read_text())['future_website']
 require(len(r['catalog_records'])==16 and len({v['record_id'] for v in r['catalog_records']})==16,'Sixteen documentary rows required')
 require(all(set(c['record_contract']['required']).issubset(v) and v['collection'] in c['required_collections'] for v in r['catalog_records']),'Archive fields changed')

MUTATIONS=[('雷尔大人的爱宠','雷尔大王的爱宠'),('并没有林务局那里的凶悍','比林务局那里更凶悍'),('建议等级90级','必须等级90级'),('解过金飞任务','不用金飞任务'),('东75，南170','东76，南170'),('东170，南181','东171，南181'),
 ('等级1','等级2'),('一种正确的饲料','两种正确的饲料'),('雷尔胖专用饲料收回','雷尔胖专用饲料保留'),
 ('鲛岛太郎','鲛岛次郎'),('不可思议的贝壳','普通的贝壳'),('藏匿的22处','藏匿的21处'),
 ('（166,161）','（167,161）'),('（9,11）','（9,12）'),('伊甸训练所内','伊甸训练所外'),
 ('只有在服务器重开机的时候','平常任何时候'),('（171,72）','（172,72）'),('（186,58）','（186,59）'),
 ('照着顺序下去走','随机挑选地点'),('先对着他喊一下“伯特”','先对着他喊一下“伯恩”'),('对着伯特说“铲子”','对着伯特说“锄头”'),
 ('红萝卜3','红萝卜2'),('红萝卜4','红萝卜5'),('还不差的白萝卜','不太差的白萝卜'),
 ('将铲子丢在地上，它就会消失','将铲子丢在地上，它不会消失'),('先把铲子丢了','记得带着铲子'),
 ('把铲子和上等白萝卜收走','只把铲子收走'),('收走红萝卜和上等白萝卜','只收走红萝卜'),
 ('萝卜可是会像铲子一样消失','萝卜不会像铲子一样消失'),('第五次找到里拉拉','第四次找到里拉拉'),
 ('拉斯基的名字“拉拉”','拉斯基的名字“啦啦”'),('林务局不过是个晃子','林务局就是真正藏身处'),
 ('高兴地将项圈收走','高兴地将项圈留下'),('里拉拉拿走黑色的服','里拉拉留下黑色的服'),
 ('走到4楼之后','走到3楼之后'),('黑色的旗','白色的旗'),('塔尔塔战士团','塔尔塔商队'),('并不在他们的规划中','正是在他们的规划中'),
 ('先带救出的拉斯基去跟里拉拉报平安','交宠之后再跟里拉拉报平安'),('防+40敏+10','防+40敏-10'),('恩惠的精灵Lv4','恩惠的精灵Lv3'),
 ('攻击力：700','防御力：700'),('Lv80以上','Lv80'),('2400以上','2400'),('1700-1900','1700-1800'),('地魔法Lv3-2','地魔法Lv2'),
 ('东0，南64','东20，南64'),('一楼入口（东20，南64）','一楼入口（东20，南65）'),('70～90级','70～80级')]


def audit(raw,expected):
 text=raw.decode('gb18030');target=semantic(expected)
 for old,new in MUTATIONS:
  require(old in text,'Missing real source mutation: '+old)
  try:actual=derive(text.replace(old,new).encode('gb18030'))
  except (ValueError,IndexError):continue
  require(semantic(actual)!=target,'Only fingerprint detected meaning change: '+old)
 require(derive(raw+b'<script>outside=1</script>')==expected,'Peripheral script changed meaning')
 for replacement in ('','<script>'+SAFETY+'</script>'):
  changed=text.replace(SAFETY,replacement)+'<div>'+SAFETY+'</div>'
  try:derive(changed.encode('gb18030'))
  except ValueError:pass
  else:raise ValueError('Hidden/outside body repaired missing pre-return safety gate')
 return {'semantic_mutations_without_all_fingerprints':len(MUTATIONS),'hidden_and_outside_article_counterexamples':2,'outside_script_positive':True}


def inspect_images(inputs):
 for expected in IMAGES:
  raw=inputs[expected['id']]
  with Image.open(io.BytesIO(raw)) as im:
   im.load();actual={'bytes':len(raw),'sha256':sha(raw),'size':list(im.size),'format':im.format,'mode':im.mode,'frames':getattr(im,'n_frames',1)}
  require(all(expected[k]==v for k,v in actual.items()),'Reviewed NPC screen bytes/full decode changed')


def replay(inputs,r):
 validate(r);ex=derive(inputs['S1']);require(ex==r['extraction'],'Current zoo quest changed');inspect_images(inputs)
 require(len(inputs['S1'])==SOURCE['bytes'] and sha(inputs['S1'])==SOURCE['sha256'],'Current report bytes changed')
 return {'schema':'stoneage.cn2003_zoo_rescue.replay.r1','inputs':[{'id':k,'url':URL if k=='S1' else next(v['url'] for v in IMAGES if v['id']==k),'bytes':len(v),'sha256':sha(v)} for k,v in inputs.items()],
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
 print('R88 zoo actors, item conditions, reward order and unresolved duplicate stats replayed; native IDs/runtime remain unknown.')


if __name__=='__main__':main()
