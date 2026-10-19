"""Island prose and a Taiwan-labelled hero guide hosted on the Mainland site."""
import argparse
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import re
from urllib.parse import urljoin
from tools.stoneage_early_content_probe import plain, require
from tools.stoneage_wayi_newbie_riding_plan import fetch
from tools.stoneage_waei_cn20_new_pet_catalog import Images, grid_digest
from tools.stoneage_waei_cn20_facilities import URL as ENTRY_URL, SOURCE_SHA as ENTRY_SHA

REPORT = Path('research/recovered/STONEAGE-WAEI-CN20-ISLAND-HERO-CONTENT-R1.json')
SOURCES = [
 {'original_url':'http://www.waei.com.cn/zhuanqu/stoneage2/strategy/index.asp','actual_capture':'20011201212305',
  'bytes':69680,'sha256':'6b29b0115bcc37c4afbbe72e9061ea3ddc13d139a63753919e1a2260bd95e63c'},
 {'original_url':'http://www.waei.com.cn/zhuanqu/stoneage2/strategy/hero/1.asp','actual_capture':'20011201035642',
  'bytes':65205,'sha256':'1f5ce2dd27e58b9ad3f90b847559bfec1a10667c41c38e23b7c5475de89c198a'}]
for source in SOURCES:
 source['strict_replay_url']='https://web.archive.org/web/'+source['actual_capture']+'id_/'+source['original_url']
PANELS = [
 ['girl1m',73,'1fce1fc598837f69ad5d2421b473cbd956923ec32ceac06ff241e6823eeaffeb'],
 ['men1m',63,'8710fcd42ea104586c9def74870bf0d3fd497cace1d5b111b8c9b487a75513b2'],
 ['men2m',35,'1ab23df785c92d3c57984c044c11d137dad6b49d73061518af6579747ecf1c2d'],
 ['girl2m',97,'fef637b4ce1a5fa6003b5c0f579cd18d5bf6b0dcb6c3f86714a33512a0eb2d7f'],
 ['girl5m',94,'ab46ce56aeb067a6228490a5071e6b00787ae46f4116007983dcebef97b16135']]
PANEL_GRID_SHA='37c1efbe215dcd03f3b1902cf49d60647cb771f733b9d9fa1056bac09a4a7186'
HERO_LINES = [
 [19,'f05e65d6a646e8361871f91c65af9d3cc52c5b0a651ac8a25b7fe56db6bc49af'],
 [52,'8500c888ff3d4589ae1244bec394591d1841c24591a766af6b55f805ec8d4993'],
 [33,'e2f16db56ff95546ff57b45e8591efedbd81b499832bad938dc5e6695ad84db2'],
 [38,'13c680689b534370c489680a3dd1ecedd06d9fa7bc443ed26ac0d24ad467c03d'],
 [20,'6dbb646ef9af77a7e621ca5f44907a424723662a111431a54d9b92fcc0b0ce5f'],
 [20,'1bf7df4df74e904499984e72971782edd30584474170a8e9b8b8f32338d16375']]
NAMES=['吉鲁岛','波拉岛','沙姆岛','塞伊那斯岛','加鲁卡岛']
MAP_CLAIMS=[
 {'description':'山地与连通山洞的石之世界，文中相对另两岛更危险。','named_mountain_caves_or_encounters':None},
 {'description':'英雄萨姆吉尔的出生地，叙述龙群占领的过去，可由萨姆吉尔村小黑猪帮助返回。',
  'relative_story_years_before':50,'absolute_world_year_or_release_date':None,'little_black_boar_is_named_hero_guide_npc_proven':False},
 {'description':'三大岛间的中转小岛，文中描述海底隧道通往各岛。','exact_three_destination_ids_or_routes':None},
 {'description':'尼斯大陆东侧出海口附近，提及玛丽娜丝村、萨姆吉尔村、英雄雕像和海产。',
  'village_labels':['玛丽娜丝村','萨姆吉尔村'],'unresolved_source_fragments':['萨姆吉尔村村','英雄萨姆吉尔村'],
  'marinas_sea_spirit_meaning_is_source_claim':True},
 {'description':'热带森林、木的文明，提及加加村及由十数个小岛构成的卡鲁它那渔村。',
  'village_labels':['加加村','卡鲁它那村'],'exact_islet_count':None}]
MAP_AREAS=[['jilu/index.asp','281,48,344,70'],['north/index.asp','92,252,156,278'],
 ['shamu/index.asp','375,169,439,193'],['bola/index.asp','508,158,572,183'],['south/index.asp','320,404,384,429']]
GUIDE = {
 'title_as_written':'前 往 英 雄 岛',
 'regional_notice_as_written':'英雄岛在台湾已经开放,大陆目前还没有开放！！',
 'publication_host_region':'CN_BEIJING_WAEI','described_availability':'GUIDE_SAYS_TW_OPEN_CN_NOT_YET_OPEN',
 'article_author_and_initial_publication_date':None,'exact_taiwan_client_build':None,
 'prerequisites':{'level_label_as_written':'LV80以上','adulthood_rite_completed_as_source_claim':True,
                  'executable_level_predicate_or_quest_flag':None,'birth_branch_waives_prerequisites_proven':False},
 'steps':[
  {'number':1,'npc_label':'日美子','village_locator_as_written':'萨村村口','coordinate_string_as_written':'56.124',
   'action':'对话接送花给鱼村弥生的委托；页面将细节指向本站北岛介绍。','cross_referenced_north_guide_read':False},
  {'number':2,'npc_label':'弥生','village_locator_as_written':'鱼村','coordinate_string_as_written':'55.93',
   'action':'把花交给弥生，攻略称会得到不可思议的贝。','received_item_label_as_written':'不可思议的贝'},
  {'number':3,'npc_label':'黑乌力','village_locator_as_written':'萨村村內','coordinate_string_as_written':'70.40',
   'action':'与黑乌力说话后可以进入攻略所称拨拉岛-英雄岛。','destination_label_as_written':'拨拉岛-英雄岛',
   'shell_consumption_or_handoff_explicitly_described':False}],
 'birth_routes':[
  {'birthplace_label_as_written':'鱼村','source_step_order':[2,3],'step_2_variant':'可直接找弥生取贝壳，不要求本分支先送花。'},
  {'birthplace_label_as_written':'其他村','source_step_order':[1,2,3],'step_2_variant':'先找日美子接任务，再送花。'}],
 'story_relative_years_from_this_guide_alone':None,
 'item_master_id_reward_pet_or_experience':None,'save_flags_and_failure_rollback':None,
 'unread_sibling_navigation':[['找寻找孙女','2.asp'],['红暴之谜','3.asp'],['不可思议的贝壳','4.asp']],
 'sibling_nav_shell_label_is_current_reward_item_verified':False,
 'map_ids_and_real_server_coordinate_binding':None}
BOUNDARIES={'same_capture_instant_or_exact_build':False,'official_host_means_operator_authored_or_independent_witness':False,
 'cn20_title_means_mainland_hero_island_deployed':False,'world_map_html_rects_are_game_coordinates':False,
 'island_panel_to_area_route_identity_inferred':False,'wave_bola_and_bo_bola_names_canonicalized':False,
 'little_black_boar_equals_black_wuli_verified':False,'recovered25_himiko_yayoi_same_entities_verified':False,
 'actual_original_server_execution_or_script':False,'automatic_new_game_adoption':False,
 'raw_html_images_programs_in_git':False,'stage_a':'7_PARTIAL_2_OPEN','stage_b_and_wiki':'GATED','r79':'PAUSED_NON_BLOCKING'}


class Areas(Images):
 def __init__(self):super().__init__();self.areas=[]
 def handle_starttag(self,tag,attrs):
  super().handle_starttag(tag,attrs)
  if tag=='area':self.areas.append(dict(attrs))


def parse_index(doc):
 require(re.search(r'<title>\s*石器时代2\.0\s*</title>',doc,re.I) is not None,'Actual index title required')
 found=[]
 for key,body in re.findall(r'<div\b[^>]*id="([^"]+)"[^>]*>(.*?)</div>',doc,re.I|re.S):
  if key in [p[0] for p in PANELS]:
   t=plain(body);found.append([key,len(t),sha256(t.encode()).hexdigest()])
 require(found==PANELS,'Five exact static HTML text panels required, no inferred hover pixels')
 m=re.findall(r'<map\b[^>]*name="Map2"[^>]*>(.*?)</map>',doc,re.I|re.S)
 require(len(m)==1,'One actual map element required')
 parser=Areas();parser.feed(m[0])
 require([[a['href'],a['coords']] for a in parser.areas]==MAP_AREAS
         and all(a['shape']=='rect' for a in parser.areas),'Map HTML href/rectangle source bindings differ')
 p=Images();p.feed(doc)
 require([a for a in p.images if a.get('usemap')=='#Map2']==[{'src':'img/Map_V2.gif','width':'580','height':'468','border':'0','usemap':'#Map2'}],
         'Selected unacquired map reference/declarations differ')
 return found


def parse_hero(doc):
 require(re.search(r'<title>\s*石器时代2\.0\s*</title>',doc,re.I) is not None,'Actual guide title required')
 require(doc.count(GUIDE['regional_notice_as_written'])==1 and doc.count('前 往 英 雄 岛')==1,'Regional notice or article heading differs')
 require(doc.count('任务条件：')==1,'One actual condition block required')
 block=doc.split('任务条件：',1)[1].split('</p>',1)[0]
 lines=['任务条件：'+plain(x) if i==0 else plain(x) for i,x in enumerate(re.split(r'<br\s*/?>',block,flags=re.I)) if plain(x)]
 require([[len(t),sha256(t.encode()).hexdigest()] for t in lines]==HERO_LINES,'Exact condition, numbered steps or birth branch text differs')
 section=doc.split('英 雄 岛 任 务 全 攻 略',1)[1].split('</table>',1)[0]
 nav=[(plain(t),h) for h,t in re.findall(r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>',section,re.I|re.S)]
 require(nav==[tuple(x) for x in GUIDE['unread_sibling_navigation']],'Actual unread sibling labels/hrefs differ')
 return lines


def source_ref(index,fragment,paragraph_sha):
 s=SOURCES[index]
 return {'original_url':s['original_url'],'actual_capture':s['actual_capture'],'sha256':s['sha256'],
         'source_fragment':fragment,'normalized_text_sha256':paragraph_sha}


def record_base(record_id,collection,profile,refs,kind):
 return {'record_id':record_id,'collection':collection,'entity_type':kind,'record_revision':1,
         'version_profile':profile,'source_refs':refs,'verification_status':'OFFICIAL_HOST_WEB_DESCRIPTION_NOT_ORIGINAL_SERVER_MASTER',
         'rights_status':'RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED','original_game_entity_id_or_cross_build_identity':None}


def validate_report(o):
 require(o['panel_grid_sha256']==PANEL_GRID_SHA, 'Panel fingerprint differs')
 require(o['known_hero_entry']=={'original_url':'http://www.waei.com.cn/ZHUANQU/stoneage2/sw/facility.asp',
          'actual_capture':'20011204213609','bytes':73356,'sha256':ENTRY_SHA,'label':'英雄岛',
          'href':'/zhuanqu/stoneage2/strategy/hero/1.asp'}, 'Hero sidebar provenance differs; root is a probe')
 require(o['sources']==SOURCES and o['boundaries']==BOUNDARIES,'Source pins or historical/runtime boundary changed')
 records=o['records'];require(len(records)==9,'Five island descriptions, one guide and three NPC mentions required')
 for i,r in enumerate(records[:5]):
  require(r['record_id']==f'waei-cn20:island-text:{PANELS[i][0]}' and r['name_as_written']==NAMES[i]
          and r['source_qualified_description']==MAP_CLAIMS[i]
          and r['source_refs']==[source_ref(0,PANELS[i][0],PANELS[i][2])], 'Source panel identity, prose or story date promoted')
 require(records[5]['source_qualified_guide']==GUIDE,'Exact guide flow, region, birth exception or unknowns changed')
 require(records[5]['source_refs']==[source_ref(1,'condition-and-step-block',grid_digest(HERO_LINES))], 'Guide paragraph custody changed')
 for i,r in enumerate(records[6:]):
  step=GUIDE['steps'][i]
  require(r['record_id']==f'waei-host-tw-guide:npc-mention:{i+1}' and r['name_as_written']==step['npc_label']
          and r['village_locator_as_written']==step['village_locator_as_written']
          and r['coordinate_string_as_written']==step['coordinate_string_as_written']
          and r['source_refs']==[source_ref(1,'numbered-step-'+str(i+1),HERO_LINES[i+1][1])]
          and r['original_server_map_id_or_spawn_or_look'] is None,'NPC mention promoted to spawn/name alias or runtime coordinate')
 for i,r in enumerate(records):
  expected_collection='maps' if i<5 else 'quests' if i==5 else 'npcs'
  expected_profile='CN_WAEI_2_0_LABEL_WORLD_PROSE_CAPTURE_20011201_NOT_EXACT_BUILD' if i<5 else 'CN_HOSTED_TW_OPEN_CN_NOT_OPEN_HERO_GUIDE_NOT_EXACT_BUILD'
  expected_kind='OFFICIAL_WEB_ISLAND_DESCRIPTION_NOT_SERVER_MAP' if i<5 else 'HOSTED_GUIDE_FLOW_NOT_SERVER_QUEST' if i==5 else 'SOURCE_NPC_MENTION_NOT_SERVER_SPAWN'
  require(r['entity_type']==expected_kind, 'Documentary record promoted to game entity')
  require(r['collection']==expected_collection and r['record_revision']==1 and r['version_profile']==expected_profile
          and r['original_game_entity_id_or_cross_build_identity'] is None
          and r['verification_status']=='OFFICIAL_HOST_WEB_DESCRIPTION_NOT_ORIGINAL_SERVER_MASTER'
          and r['rights_status']=='RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED','Required archive record scope promoted')
 require(o['selected_map_reference']=={'relative_src_as_written':'img/Map_V2.gif','original_url':urljoin(SOURCES[0]['original_url'],'img/Map_V2.gif'),
          'html_declared_dimensions':[580,468],'pixels_requested':False,'actual_format_dimensions_capture_or_hash':None,
          'html_areas':MAP_AREAS,'destination_bodies_read':False}, 'Map refs promoted to acquired geography or image data')
 require(o['coverage']=={'new_original_bodies':2,'known_facilities_entry_reacquired':1,'island_text_descriptions':5,
          'source_qualified_quest_guides':1,'npc_mentions':3,'actual_server_npc_instances_verified':0,'new_images_requested':0,
          'sibling_guide_bodies_unread':3}, 'Finite material accounting differs')
 require(o['source_relations']=={'world_text_wave_bola':'波拉岛','guide_destination_bo_bola':'拨拉岛-英雄岛',
          'relation_status':'UNRESOLVED_SPELLING_ALIAS_OR_DISTINCT_PLACE_NOT_ENTITY_MERGE',
          'fifty_years_belongs_to_world_text_not_guide_prerequisite':True,
          'root_probed_not_authenticated_facility_sidebar_href':True}, 'Unproven geographical or temporal identity normalized')
 require(o['next']=='CN20-HERO-GUIDE-SOURCE-RELATIONS-01','Finite stop/next changed')


def build(entry,entry_final,inputs):
 require(entry_final==ENTRY_URL and len(entry)==73356 and sha256(entry).hexdigest()==ENTRY_SHA,'Known facilities entry exact bytes/capture required')
 links=[(h,plain(t)) for h,t in re.findall(r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>',entry.decode('gb18030',errors='strict'),re.I|re.S) if plain(t)=='英雄岛']
 require(links==[('/zhuanqu/stoneage2/strategy/hero/1.asp','英雄岛')],'Actual facilities sidebar hero link differs; root index is not this href')
 require(len(inputs)==2,'Only two selected new bodies required')
 for (body,final),s in zip(inputs,SOURCES):
  require(final==s['strict_replay_url'] and len(body)==s['bytes'] and sha256(body).hexdigest()==s['sha256'],'Exact actual final URL/capture/bytes required')
 panels=parse_index(inputs[0][0].decode('gb18030',errors='strict'));parse_hero(inputs[1][0].decode('gb18030',errors='strict'))
 records=[]
 for i,p in enumerate(panels):
  r=record_base(f'waei-cn20:island-text:{p[0]}','maps','CN_WAEI_2_0_LABEL_WORLD_PROSE_CAPTURE_20011201_NOT_EXACT_BUILD',
                [source_ref(0,p[0],p[2])],'OFFICIAL_WEB_ISLAND_DESCRIPTION_NOT_SERVER_MAP')
  r.update(name_as_written=NAMES[i],source_qualified_description=deepcopy(MAP_CLAIMS[i]));records.append(r)
 q=record_base('waei-host-tw-guide:quest:hero-entry','quests','CN_HOSTED_TW_OPEN_CN_NOT_OPEN_HERO_GUIDE_NOT_EXACT_BUILD',
               [source_ref(1,'condition-and-step-block',grid_digest(HERO_LINES))],'HOSTED_GUIDE_FLOW_NOT_SERVER_QUEST')
 q['source_qualified_guide']=deepcopy(GUIDE);records.append(q)
 for i,step in enumerate(GUIDE['steps']):
  r=record_base(f'waei-host-tw-guide:npc-mention:{i+1}','npcs','CN_HOSTED_TW_OPEN_CN_NOT_OPEN_HERO_GUIDE_NOT_EXACT_BUILD',
                [source_ref(1,'numbered-step-'+str(i+1),HERO_LINES[i+1][1])],'SOURCE_NPC_MENTION_NOT_SERVER_SPAWN')
  r.update(name_as_written=step['npc_label'],village_locator_as_written=step['village_locator_as_written'],
           coordinate_string_as_written=step['coordinate_string_as_written'],original_server_map_id_or_spawn_or_look=None);records.append(r)
 o={'schema':'stoneage.waei_cn20.island_hero_content.r1','date':'2026-10-19','task':'CN20-OFFICIAL-ISLAND-HERO-CONTENT-SOURCE-01',
    'sources':deepcopy(SOURCES),'known_hero_entry':{'original_url':'http://www.waei.com.cn/ZHUANQU/stoneage2/sw/facility.asp',
     'actual_capture':'20011204213609','bytes':73356,'sha256':ENTRY_SHA,'label':'英雄岛','href':links[0][0]},
    'panel_grid_sha256':PANEL_GRID_SHA,'records':records,
    'selected_map_reference':{'relative_src_as_written':'img/Map_V2.gif','original_url':urljoin(SOURCES[0]['original_url'],'img/Map_V2.gif'),
      'html_declared_dimensions':[580,468],'pixels_requested':False,'actual_format_dimensions_capture_or_hash':None,
      'html_areas':deepcopy(MAP_AREAS),'destination_bodies_read':False},
    'coverage':{'new_original_bodies':2,'known_facilities_entry_reacquired':1,'island_text_descriptions':5,
      'source_qualified_quest_guides':1,'npc_mentions':3,'actual_server_npc_instances_verified':0,'new_images_requested':0,'sibling_guide_bodies_unread':3},
    'source_relations':{'world_text_wave_bola':'波拉岛','guide_destination_bo_bola':'拨拉岛-英雄岛',
      'relation_status':'UNRESOLVED_SPELLING_ALIAS_OR_DISTINCT_PLACE_NOT_ENTITY_MERGE',
      'fifty_years_belongs_to_world_text_not_guide_prerequisite':True,'root_probed_not_authenticated_facility_sidebar_href':True},
    'initial_intake':{'requested_capture':'20011204213609','actual_captures':[s['actual_capture'] for s in SOURCES],
      'reader_unavailable_not_historical_absence':True,'initial_root_uppercase_path_redirected_to_lowercase':True,
      'runner_repeats_initial_failures_or_redirects':False,'root_static_panels_read_without_executing_javascript':True},
    'boundaries':deepcopy(BOUNDARIES),'next':'CN20-HERO-GUIDE-SOURCE-RELATIONS-01'}
 validate_report(o);return o


def main():
 p=argparse.ArgumentParser();p.add_argument('--input-entry');p.add_argument('--input-index');p.add_argument('--input-guide');p.add_argument('--output',required=True);a=p.parse_args()
 require(all([a.input_entry,a.input_index,a.input_guide]) or not any([a.input_entry,a.input_index,a.input_guide]),'All local originals or none required')
 entry,ef=(Path(a.input_entry).read_bytes(),ENTRY_URL) if a.input_entry else fetch(ENTRY_URL)
 inputs=[(Path(path).read_bytes(),s['strict_replay_url']) if path else fetch(s['strict_replay_url']) for path,s in zip([a.input_index,a.input_guide],SOURCES)]
 o=build(entry,ef,inputs);payload=json.dumps(o,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
 out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(payload,encoding='utf-8')
 for s in SOURCES:print('SOURCE_SHA256='+s['sha256'])
 print('ISLAND_TEXTS=5 GUIDE=1 NPC_MENTIONS=3 RUNTIME_NPCS=0 NEW_IMAGES=0 NEW_BODIES=2')
 print('DERIVED_SHA256='+sha256(payload.encode()).hexdigest())


if __name__=='__main__':main()
