"""R90: Taiwan 8.0 named mount certificate, typed pet equipment and one static panel."""
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
STEM='STONEAGE-TW80-MOUNT-CERTIFICATE-EQUIPMENT'
REPORT=ROOT/f'research/recovered/{STEM}-SOURCE-R1.json'
PROFILE='TW80_2005_LOST_WORLD_SINA_REPUBLICATION_CREDITS_BAHAMUT_EXACT_BUILD_UNKNOWN'
PARSER='tools/stoneage_jp2005_treasure_source.py'
PARENTS=['research/recovered/STONEAGE-CN20-RIDING-TRAINER-COMBAT-SOURCE-R1.json',
 'docs/specs/STONEAGE-PET-80-CONTEMPORARY-RELEASE-EVIDENCE-R1.md',
 'research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json']
URL='https://games.sina.com.cn/o/n/2005-06-09/1552109910.shtml'
GALLERY='https://games.sina.com.cn/o/i/2005-06-09/61677.shtml'
SOURCES=[{'id': 'S1', 'url': 'https://games.sina.com.cn/o/n/2005-06-09/1552109910.shtml', 'http_status': 200, 'no_redirect': True, 'initial_intake_bytes': 48685, 'initial_intake_sha256': 'a67c9ee21070d048c7dae901cf8c505b6ced3c888abd1ebcc190f764c1f7f4d8', 'encoding': 'GB18030_STRICT', 'authority': 'DATED_SINA_REPUBLICATION_CREDITS_BAHAMUT_NOT_INDEPENDENT_PRIMARY', 'current_bytes_authenticate_2005_original': False, 'official_operator_authorship_verified': False}, {'id': 'S2', 'url': 'https://games.sina.com.cn/o/i/2005-06-09/61677.shtml', 'http_status': 200, 'no_redirect': True, 'initial_intake_bytes': 35353, 'initial_intake_sha256': '41ae049999094a87ef0a6a1789c2ab9ef55d226093267d9a1a191a883c5b11fc', 'encoding': 'GB18030_STRICT', 'authority': 'SINA_LINKED_GALLERY_NOT_NATIVE_CLIENT_MASTER', 'current_bytes_authenticate_2005_original': False, 'official_operator_authorship_verified': False}]
IMAGES=[{'id': 'I1', 'url': 'https://image2.sina.com.cn/gm/o/n/2005-06-09/U508P115T9D109910F376DT20050609155230.jpg', 'http_status': 200, 'no_redirect': True, 'bytes': 77930, 'sha256': '3126fbb80a7d379530519840e78563dc850707a17e89764f21ad2b82df52aa23', 'size': [640, 480], 'format': 'JPEG', 'mode': 'RGB', 'frames': 1}]
VISUAL=[{'id':'I1','manual_visual_review':True,'kind':'STATIC_PET_STATUS_AND_EQUIPMENT_PANEL_REFERENCE',
 'visible':['YELLOW_BIRD_LIKE_PET_IN_STATUS','CHARACTER_OVER_YELLOW_BIRD_LIKE_MOUNT','PET_EQUIPMENT_PANEL_WITH_SEVEN_POSITIONS','ITEM_ICONS_IN_GRID','CURSOR_WITH_ITEM_ICON_AND_GREEN_OUTLINE'],
 'panel_label_as_read':'PET STATUS','image_caption':'宠物装备套装',
 'pet_name_or_native_species_id_transcribed':None,'depicted_pet_is_reported_shikalu_or_luoduokelei':False,
 'displayed_stats_are_species_master_or_growth':False,'element_bar_lengths_are_numeric_percentages':False,
 'static_cursor_proves_successful_equipping':False,'all_pet_types_have_same_slots_proven':False,
 'native_sprite_animation_or_button_coordinates_verified':False,'historical_2005_pixels_authenticated':False}]
BOUNDARIES={k:False for k in ('gnn_original_article_acquired_this_round','sina_reprint_is_independent_second_primary_witness',
 'sina_republication_today_is_exact_taiwan_launch_date','current_bytes_authenticate_2005_original','official_operator_authorship_verified',
 'exact_build_or_native_ids_verified','two_new_mounts_are_two_new_species','obtaining_pet_is_same_as_obtaining_riding_certificate',
 'chief_certificate_applies_to_both_reported_mounts','cn20_courses_loyalty_or_combat_formula_backfilled',
 'all_pet_types_equip_all_seven_categories','foot_subtypes_are_three_extra_equipment_categories','elemental_effect_numeric_formula_recovered',
 'crafting_cap15_means_all_recipes_recovered','screenshot_pet_is_one_of_two_named_mounts','static_cursor_proves_server_equipping',
 'screenshot_proves_opcode127_or_enabled_pet_item_build','picture_proves_gear_base_stats_or_growth',
 'original_html_or_assets_committed','stage_b_started')}


def markup(raw):
 p=VisibleMarkup();p.feed(raw.decode('gb18030',errors='strict'));return ''.join(p.parts)


def article(raw):
 text=markup(raw)
 require(plain(one(r'<th class=f21 height=44>(.*?)</th>',text,re.S))=='《石器时代8.0》开放全新宠物装备(图)','Visible title changed')
 require(plain(one(r'<tr><td height=24 align=center>(.*?)</td></tr>',text,re.S))=='http://games.sina.com.cn2005-06-0915:52巴哈姆特','Reprint time/source changed')
 area=one(r'<!-- 内容 begin -->(.*?)<!-- 内容 end -->',text,re.S)
 require('以下是来自中国台湾地区的消息：' in plain(area) and '编辑：梁凌' in plain(area),'Taiwan attribution/editor missing')
 paras=[plain(v) for v in re.findall(r'<p>(.*?)</p>',area,re.S)]
 starts=['“宠物装备”系统可依照','8.0版将开放2只骑宠','原本的合成只到等级']
 chosen=[]
 for start in starts:
  rows=[v for v in paras if v.startswith(start)];require(len(rows)==1,'Missing/duplicated selected paragraph: '+start);chosen.append(rows[0])
 route=one(r"<a href='(http://games.sina.com.cn/o/i/2005-06-09/61677.shtml)' target=_blank><img src='([^']+)'[^>]*></a>",area)
 require(route==(GALLERY.replace('https:','http:'),IMAGES[0]['url'].replace('https:','http:').replace('.jpg','_c.jpg')),'Article gallery/thumbnail link changed')
 return chosen


def gallery(raw):
 text=markup(raw)
 require(plain(one(r'<th class=f14 colspan=2>(.*?)</th>',text,re.S))=='宠物装备套装','Gallery title changed')
 require(plain(one(r'<td style="padding:20 48 10 0" align=right colspan=2>(.*?)</td>',text,re.S))=='http://games.sina.com.cn2005-06-0915:52新浪游戏','Gallery time/publisher changed')
 pic=one(r'<!-- 图片 -->(.*?)<!-- 评论 begin -->',text,re.S)
 src=one(r'''<img name='myImage' src="([^"]+)" alt='宠物装备套装' ''',pic)
 require(src==IMAGES[0]['url'].replace('https:','http:'),'Actual gallery image changed')
 require(one(r'<A HREF=([^ >]+) target=_blank class=n01>点击查看原图</a>',pic)==src,'Gallery original-image link detached')
 caption=plain(one(r'<td class=l15 bgcolor=#F4F4F4 style="padding:0 20 20 20"><font id="zoom">(.*?)<br>',pic,re.S))
 require(caption.startswith('《石器时代8.0：失落的世界》全新改版今日正式上线。') and '2只新的骑宠' in caption and '宠物装备系统' in caption,'Gallery caption changed')
 return caption


def derive(raws):
 equip,mount,craft=article(raws['S1']);caption=gallery(raws['S2'])
 clauses=['不同类型的宠物，给予不同的装备字段','玩家也可以透过合成系统制作宠物装备','宠物装备本身就带有属性','依照地水火风相生相克关系产生能力的增减效果']
 require(all(v in equip for v in clauses),'Typed equipment or elemental effect changed')
 n,labels=one(r'宠物装备区分为(\d+)大类，分别是([^。]+)。',equip)
 upper,feet=one(r'(.*?)、脚\((.*?)\)',labels)
 require(int(n)==7 and upper.split('、')==['头','牙','爪','胸','背','翅'] and feet.split('、')==['两只脚','四只脚','鱼鳍'],'Equipment categories changed')
 require('水魔鬼鱼“史卡鲁”' in mount and '恐龙系中常被遗忘的“罗多克雷”' in mount,'Named mount pair changed')
 require('“史卡鲁”是这一次新庄园的庄园宠，主要出现在“泪之海”' in mount,'Shikalu habitat/manor role changed')
 require('取得不算困难，不过若是想要骑它，则要新庄园的族长发给骑宠证' in mount,'Obtaining versus certificate condition changed')
 before,after=map(int,one(r'原本的合成只到等级(\d+)级，这一次改版则提升到(\d+)级',craft))
 require((before,after)==(11,15) and '料理、合成' in craft,'Crafting cap/scope changed')
 return {'riding':{'reported_new_mount_count':2,'pets':[{'name_as_written':'史卡鲁','description_as_written':'水魔鬼鱼','manor_pet_reported':True,'main_habitat_as_written':'泪之海','riding_condition':'NEW_MANOR_CHIEF_ISSUES_MOUNT_CERTIFICATE','obtaining_difficulty':'QUALITATIVE_NOT_DIFFICULT_NOT_CAPTURE_RATE','certificate_item_id_issuer_name_coordinates_cost_or_consumption':None},
 {'name_as_written':'罗多克雷','description_as_written':'恐龙系中常被遗忘','manor_pet_reported':None,'main_habitat_as_written':None,'riding_condition':None,'certificate_item_id_issuer_name_coordinates_cost_or_consumption':None}],
 'announced_mount_addition_is_new_species_introduction':False,'training_level_loyalty_combat_stats_or_character_compatibility':None},
 'equipment':{'reported_category_count':7,'categories_as_written':['头','牙','爪','胸','背','翅','脚'],'foot_type_parenthetical_as_written':['两只脚','四只脚','鱼鳍'],
 'slots_depend_on_pet_type':True,'crafting_equipment_reported':True,'equipment_has_elements_reported':True,'element_order_as_written':['地','水','火','风'],
 'equipping_can_increase_or_decrease_abilities_reported':True,'all_seven_slots_for_every_pet_or_body_type_matrix':None,'numeric_modifiers_stacking_rounding_or_gear_base_stats':None},
 'crafting_context':{'reported_previous_cap':before,'reported_new_cap':after,'scope_as_written':['料理','合成'],'character_level_or_all_recipe_ids':None},
 'source_scope':{'reported_region':'台湾','reported_version':'8.0：失落的世界','sina_republication_as_written':'2005-06-09 15:52','credited_source':'巴哈姆特','editor_as_written':'梁凌',
 'today_resolved_to_exact_launch_day':None,'gnn_original_retrieved_this_round':False,'original_operator_script_or_exact_build':None},
 'original_server_runtime_verified':False,'fingerprints':{k:{'utf8_bytes':len(v.encode()),'sha256':sha(v.encode())} for k,v in [('equipment',equip),('riding',mount),('crafting',craft),('gallery_caption',caption)]}}


def pin(path):
 b=(ROOT/path).read_bytes();return {'path':path,'bytes':len(b),'sha256':sha(b),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}


def comparison():
 r=json.loads((ROOT/PARENTS[0]).read_text());s=(ROOT/PARENTS[1]).read_text()
 require(r['boundaries']['original_server_execution_verified'] is False and '999ffdf1' in s and '_PET_ITEM' in s and 'opcode 127' in s,'Earlier source-only boundaries changed')
 return {'cn20':{'schema':r['schema'],'four_manor_trainer_courses_or_loyalty100_backfilled':False,'same_build_combat_formula_established':False},
 'pet80_prior_gate':{'contemporary_feature_release_already_recorded':True,'new_result_is_first_discovery_of_equipment_system':False,'default_pet_item_macro_or_paired_binary_gate_changed':False,'opcode127_or_inventory_lifecycle_execution_verified':False},'modern_adoption_decided':False}


def catalog(ex):
 rows=[('mount-'+str(i+1),'pets','DOCUMENTARY_NAMED_MOUNT_ELIGIBILITY',v,['S1']) for i,v in enumerate(ex['riding']['pets'])]
 rows += [('equipment','tutorials','DOCUMENTARY_PET_TYPE_EQUIPMENT_CATEGORIES',ex['equipment'],['S1']),('crafting-cap','tutorials','DOCUMENTARY_CAP_CONTEXT_NOT_RECIPE_CATALOG',ex['crafting_context'],['S1']),('panel','screens','STATIC_PET_EQUIPMENT_REFERENCE_NOT_IO_TRACE',{'image':IMAGES[0],'observation':VISUAL[0]},['S1','S2','I1'])]
 return [{'record_id':'TW80-R90-'+i,'entity_type':t,'collection':c,'version_profile':PROFILE,'source_refs':refs,'verification_status':'DATED_DERIVATIVE_PRESS_OR_STATIC_REFERENCE_NOT_RUNTIME',
 'rights_status':'RESEARCH_METADATA_NOT_RELEASE_APPROVED','record_revision':1,'game_ids':None,'content':v} for i,c,t,v,refs in rows]


def semantic(ex):return {k:v for k,v in ex.items() if k!='fingerprints'}
SEMANTIC_SHA='0693da598e9f3a03daa84b5b0bf3b0a5d154f4672c6e2cdd99ac683ea5548fdf'


def validate(r):
 require(r['schema']=='stoneage.tw80_mount_certificate_equipment.source.r1' and r['version_profile']==PROFILE,'Version/schema changed')
 require(r['sources']==SOURCES and r['images']==IMAGES and r['visual_observations']==VISUAL and r['negative_boundaries']==BOUNDARIES,'Source/visual/authority boundaries changed')
 require(r['parent_pins']==[pin(p) for p in PARENTS] and r['parser_pin']==pin(PARSER),'Parent/parser bytes changed')
 require(r['comparison']==comparison(),'Prior source/build distinction changed')
 require(sha(json.dumps(semantic(r['extraction']),ensure_ascii=False,sort_keys=True).encode())==SEMANTIC_SHA,'Mount/equipment contract changed')
 require(r['catalog_records']==catalog(r['extraction']),'Catalog detached')
 c=json.loads((ROOT/PARENTS[-1]).read_text())['future_website'];require(len(r['catalog_records'])==5,'Five documentary rows required')
 require(all(set(c['record_contract']['required']).issubset(v) and v['collection'] in c['required_collections'] for v in r['catalog_records']),'Archive fields changed')

MUTATIONS=[('编辑：梁凌','编辑：别人'),('台湾地区','大陆地区'),('7 大类','8 大类'),('头、 牙','尾、 牙'),('两只脚、四只脚、鱼鳍','两只脚、四只脚、翅膀'),('不同类型的宠物，给予不同','所有类型的宠物，给予相同'),('透过合成系统制作宠物装备','不能透过合成系统制作宠物装备'),('本身就带有属性','本身不带有属性'),('地水火风','地火水风'),('增减效果','只增加效果'),('水魔鬼鱼“史卡鲁”','火魔鬼鱼“史卡鲁”'),('恐龙系中常被遗忘的“罗多克雷”','恐龙系中常被遗忘的“罗多克雷改”'),('主要出现在“泪之海”','主要出现在“萨村”'),('是这一次新庄园的庄园宠','不是这一次新庄园的庄园宠'),('取得不算困难','取得极其困难'),('若是想要骑它','若是想要取得它'),('新庄园的族长发给骑宠证','任一商人卖给骑宠证'),('等级 11 级','等级 12 级'),('提升到 15 级','提升到 16 级'),('料理、合成','战斗、捕获')]


def audit(raws,expected):
 text=raws['S1'].decode('gb18030');target=semantic(expected)
 for old,new in MUTATIONS:
  require(old in text,'Missing real mutation '+old)
  try:actual=derive(dict(raws,S1=text.replace(old,new).encode('gb18030')))
  except (ValueError,IndexError):continue
  require(semantic(actual)!=target,'Only fingerprint detected semantic change '+old)
 for old,new in [('2005-06-09 15:52','2005-06-10 15:52'),('宠物装备套装','宠物骑乘套装'),('F376DT20050609155230.jpg','F373DT20050609155230.jpg')]:
  s=raws['S2'].decode('gb18030');require(old in s,'Gallery mutation absent')
  try:derive(dict(raws,S2=s.replace(old,new).encode('gb18030')))
  except ValueError:pass
  else:raise ValueError('Changed gallery identity accepted')
 require(derive({k:v+b'<script>outside=1</script>' for k,v in raws.items() if k!='I1'}|{'I1':raws['I1']})==expected,'Outside script drift affected selected core')
 needle='新庄园的族长发给骑宠证'
 for repl in ('','<script>'+needle+'</script>'):
  changed=text.replace(needle,repl)+'<div>'+needle+'</div>'
  try:derive(dict(raws,S1=changed.encode('gb18030')))
  except ValueError:pass
  else:raise ValueError('Hidden/outside text repaired certificate condition')
 return {'semantic_mutations_without_all_fingerprints':len(MUTATIONS),'gallery_identity_mutations':3,'hidden_and_outside_article_counterexamples':2,'outside_script_positive':True}


def inspect_images(inputs):
 for expected in IMAGES:
  raw=inputs[expected['id']]
  with Image.open(io.BytesIO(raw)) as im:
   im.load();actual={'bytes':len(raw),'sha256':sha(raw),'size':list(im.size),'format':im.format,'mode':im.mode,'frames':getattr(im,'n_frames',1)}
  require(all(expected[k]==v for k,v in actual.items()),'Reviewed panel image/full decode changed')


def initial_inputs():return [{'id':s['id'],'url':s['url'],'bytes':s['initial_intake_bytes'],'sha256':s['initial_intake_sha256']} for s in SOURCES]+[{k:v[k] for k in ('id','url','bytes','sha256')} for v in IMAGES]


def replay(inputs,r):
 validate(r);ex=derive(inputs);require(ex==r['extraction'],'Selected paragraphs/gallery changed');inspect_images(inputs)
 actual=[{'id':k,'url':(URL if k=='S1' else GALLERY) if k.startswith('S') else IMAGES[0]['url'],'bytes':len(v),'sha256':sha(v)} for k,v in inputs.items()]
 return {'schema':'stoneage.tw80_mount_certificate_equipment.replay.r1','inputs':actual,
 'source_identity':{'html_equals_initial_intake':{v['id']:v==next(x for x in initial_inputs() if x['id']==v['id']) for v in actual if v['id'].startswith('S')},'selected_paragraphs_and_gallery_equal_initial':True,'current_bytes_authenticate_2005_original':False},
 'extraction':ex,'images':IMAGES,'visual_observations':VISUAL,'comparison':comparison(),'catalog_records':catalog(ex),'audit':audit(inputs,ex),'original_html_or_assets_in_output':False,'original_server_runtime_verified':False}


def read_inputs(directory=None):
 result={}
 for key,url in [('S1',URL),('S2',GALLERY),('I1',IMAGES[0]['url'])]:
  if directory:result[key]=(Path(directory)/(key+('.html' if key.startswith('S') else '.jpg'))).read_bytes()
  else:
   with urllib.request.urlopen(url,timeout=50) as h:
    require(h.status==200 and h.url==url,'Exact URL/status changed');result[key]=h.read()
 return result


def main():
 p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--fetch',action='store_true');g.add_argument('--input-dir');p.add_argument('--output',required=True);a=p.parse_args()
 r=json.loads(REPORT.read_text());out=replay(read_inputs(a.input_dir),r)
 path=Path(a.output);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print('R90 Taiwan8 mount certificates, type-dependent equipment and static panel replayed; original IO and named mount skills remain unknown.')


if __name__=='__main__':main()
