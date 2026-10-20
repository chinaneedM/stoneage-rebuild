"""Replay a dated Taiwan operator summoning preview and separately captured images."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import urllib.request
from tools.stoneage_early_content_probe import plain,require
from tools.stoneage_wayi_newbie_riding_plan import index_rows
from tools.stoneage_jp2008_cooperation_source import jpeg_size
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'research/recovered/STONEAGE-TW75-SPIRIT-SUMMON-PREVIEW-SOURCE-R1.json'
URLS=(
'https://web.archive.org/web/20050612011406id_/http://www.wayi.com.tw/stoneage/producer/producer01.asp',
'https://web.archive.org/web/20051129125915id_/http://www.wayi.com.tw/stoneage/producer/producer02.asp?idno=84',
'https://web.archive.org/web/20041211081705id_/http://www.wayi.com.tw/images02/sa0527-1.JPG',
'https://web.archive.org/web/20041211082942id_/http://www.wayi.com.tw/images02/sa0527-2.JPG',
'https://web.archive.org/web/20041211084443id_/http://www.wayi.com.tw/images02/sa0527-3.JPG')
NAMES=('P0.html','P1.html','I1.jpg','I2.jpg','I3.jpg')
PINS=[(68,'232781772d6904d2ecdee3ac05bd00d0736262db177738f2c6a63761ac05fe5a'),
(166,'7faeaa9624f9d8478a7ee470bd248ad06a528be6af05fad9862aea5bff69842d'),
(128,'308f7b5a081e3845fd7074933c7b1d4ca6f8ff6a50612d46e2b518ddecfd8834'),
(95,'846f1a16d961fb7d4af0430cb076707596137d05efed8c37754e2a17db18fa4e')]
BOUNDARIES=dict(original_server_execution_verified=False,exact_client_build=None,index_date_is_body_capture_or_deployment=False,
 preview_proves_actual_release=False,summon_is_player_pet_summoning=False,messenger_min_level_or_stat_trigger=None,
 hero_min_level_or_rebirth=None,party_size_or_join_condition=None,universal_quest_timeout=None,
 figure2_timer_is_initial_duration=False,figure3_timer_is_failure=False,three_images_same_character_continuous_run=False,
 generic_token_is_exact_image_token_alias=False,all_quests_reward_spear=False,spear_spell_level_is_quest_requirement=False,
 displayed_money_is_quest_reward=False,spell_damage_or_probability=None,quest_completion_or_reward_transaction_verified=False,
 exact_npc_pet_item_map_or_sprite_ids=None,ancient_gu_label_proves_spawn_or_dialogue=False,
 spirit_is_named_spirit_king=False,demon_invasion_is_cross_region_canon=False,
 index_day_20040528_html_or_image_bytes_verified=False,manual_observation_is_independent_ocr=False,raw_sources_committed=False,
 stage_a='7_PARTIAL_2_OPEN',stage_b_and_wiki='GATED',r79='PAUSED_NON_BLOCKING')

def facts():
 return dict(system='精靈的召喚',preview_development_state='7.5_DEVELOPMENT_NEARING_COMPLETION',
  roles=['使者','勇者'],trigger='UNSPECIFIED_SPECIAL_CONDITION',token_category_as_written='精靈信物',
  flow=['SPIRIT_CALLS_PLAYER','MESSENGER_FINDS_CHOSEN_HERO','HERO_RECEIVES_TOKEN_FROM_MESSENGER','HERO_LEARNS_MISSION','MISSION_COMPLETED','BOTH_ROLES_REPORTED_TO_RECEIVE_REWARDS'],
  rewards='UNSPECIFIED_GENEROUS_REWARDS_FOR_BOTH_NOT_PROVEN_EQUAL_CONTENT',
  purpose='REBUILD_NEWCOMER_VETERAN_TRUST_AND_FIGHT_DEMON_FACTION',newcomer_bridge='DESIGN_RATIONALE_NOT_LEVEL_OR_CLASS_RULE',
  spirit_or_demon_individual_names=None)

def observations():
 return [
 dict(image='I1',dialog='CONSENT_TO_FIND_HERO_AGAINST_DEMONS',buttons=['確定','取消'],visible_call_message=True,actual_audio_obtained=False,choice_effect_or_protocol_binding=None),
 dict(image='I2',mission_target_label='古瓜',mission='FIND_TARGET_AND_LEARN_RECENT_TROUBLES',remaining_time_display=dict(hours=6,minutes=33),timer_initial_duration=None,npc_spawn_or_id=None),
 dict(image='I3',mission_completion_prompt_visible=True,remaining_time_visible_hours=0,remaining_time_visible_minutes=59,full_time_suffix=None,
  handed_over_token_label='精靈勇者信物',received_item_label='柳牙之槍',item_panel=dict(durability_percent=100,attack_modifier=85,agility_modifier=-18,spell_label='毒霧的精靈',spell_level=6),
  money_display=8198620,money_is_reward=False,actual_equip_or_cast_verified=False)]

def records():
 rows=[]
 def add(kind,collection,data,refs):
  rows.append(dict(record_id=f'TW75-SUMMON-{len(rows)+1:02}',entity_type=kind,collection=collection,
   version_profile='TW_WAYI_7.5_PREVIEW_INDEX_2004_BODY_CAPTURE_2005_IMAGES_2004',source_refs=refs,
   verification_status='OFFICIAL_PREVIEW_OR_IMAGE_DESCRIPTION_NOT_RUNTIME',rights_status='RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED',
   record_revision=1,game_ids=None,source_reported=data))
 f=facts()
 add('SYSTEM_PREVIEW','quests',f,['P0','P1'])
 for role in f['roles']:add('PLAYER_ROLE_NOT_NAMED_NPC','characters',dict(role=role,player_role=True,named_npc=False,level_or_id=None),['P1'])
 add('TOKEN_CATEGORY','items',dict(label='精靈信物',exact_image_token_alias=None,consumption_rule=None),['P1'])
 add('SOCIAL_AND_WORLD_RATIONALE','quests',dict(motive=f['purpose'],level_definition=None,spirit_king_identity=None,canonical_worldline_union=None),['P1'])
 for x in observations():add('DOCUMENTARY_SCREEN_OBSERVATION','screens',x,[x['image'],'P1'])
 add('VISUAL_REPORTED_ITEM','items',dict(label='柳牙之槍',panel=observations()[2]['item_panel'],all_missions_reward_this=False,original_item_or_bitmap_id=None),['I3'])
 add('TOKEN_LABEL_IN_ONE_IMAGE','items',dict(label='精靈勇者信物',alias_of_prose_token_verified=False,hand_over_message_not_consumption_script=True),['I3'])
 return rows

def extract_index(b):
 rows=index_rows(b.decode('big5',errors='strict'));selected=next(x for x in rows if x['article_id_as_web_key']==84)
 require(selected==dict(article_id_as_web_key=84,title='7.5版報導之一：精靈的召喚',index_date_as_written='2004-5-28'),'Actual title/date/link association changed')
 return dict(row_count=len(rows),selected=selected,web_key_is_game_quest_id=False)

def extract_body(b):
 h=b.decode('big5',errors='strict');ms=re.findall(r'<span\b[^>]*>\s*(經過幾個月.*?)</span>',h,re.S|re.I)
 require(len(ms)==1,'One authentic preview body required');body=ms[0]
 ps=[plain(x) for x in re.split(r'<BR>\s*<BR>',body,flags=re.I) if plain(x)]
 require([(len(x),sha256(x.encode()).hexdigest()) for x in ps]==PINS,'Preview paragraphs changed')
 for s in ['某種特定的條件','被精靈所揀選的勇者','接獲使者所帶來的精靈信物','勇者與使者將同時','有上進心的新手','魔族的黨羽']:
  require(s in plain(body),'Role/condition/rationale missing')
 refs=re.findall(r'href="(http://www.wayi.com.tw/images02/sa0527-\d.JPG)"',body)
 require(refs==[f'http://www.wayi.com.tw/images02/sa0527-{n}.JPG' for n in [1,2,3]],'Actual three image references changed')
 return dict(paragraphs=[dict(characters=len(x),sha256=sha256(x.encode()).hexdigest()) for x in ps],facts=facts(),image_refs=refs)

def validate(r):
 require(r['schema']=='stoneage.tw75_spirit_summon_preview.source.r1','Schema')
 require([x['url'] for x in r['inputs']]==list(URLS),'Finite exact source set')
 require(r['boundaries']==BOUNDARIES,'Historical/runtime boundary promoted')
 require(r['records']==records(),'Player roles, item labels, visual stats or archive scope changed')
 require(r['manual_image_observations']==observations(),'Screenshot observation changed')
 require(r['source_dates']==dict(index_label='2004-5-28',index_capture='20050612011406',body_capture='20051129125915',image_captures=['20041211081705','20041211082942','20041211084443']),'Dates conflated')
 require(r['next']=='OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-34','Return whole portfolio')

def replay(r,payloads):
 validate(r);require(len(payloads)==5,'Two HTML and three historical JPEG required')
 for s,b in zip(r['inputs'],payloads):
  require(len(b)==s['bytes'] and sha256(b).hexdigest()==s['sha256'],'Exact archived byte pin changed')
 extracted=[extract_index(payloads[0]),extract_body(payloads[1])]
 require(extracted==r['extracted'],'Index/body derived semantics changed')
 sizes=[jpeg_size(b) for b in payloads[2:]];require(sizes==[[640,480]]*3,'Image dimensions changed')
 return dict(schema='stoneage.tw75_spirit_summon_preview.replay.r1',inputs=[dict(id=s['id'],bytes=len(b),sha256=sha256(b).hexdigest()) for s,b in zip(r['inputs'],payloads)],
  extracted=extracted,image_dimensions=sizes,manual_image_observations=observations(),image_text_independently_ocr_verified=False,
  original_server_executed=False,raw_sources_in_output=False)

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--fetch',action='store_true');p.add_argument('--source-dir',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 require(a.fetch!=bool(a.source_dir),'Choose fetch or transient directory');payloads=[]
 for u,n in zip(URLS,NAMES):
  if a.fetch:
   with urllib.request.urlopen(u,timeout=45) as response:
    require(response.status==200 and response.url==u,'Unexpected redirect/status');b=response.read(2_000_001);require(len(b)<=2_000_000,'Oversized source')
  else:b=(a.source_dir/n).read_bytes()
  payloads.append(b)
 out=replay(json.loads(REPORT.read_text()),payloads);a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print('HISTORICAL_HTML_VERIFIED=2 HISTORICAL_JPEG_VERIFIED=3 PLAYER_ROLES=2 ORIGINAL_SERVER_EXECUTIONS=0')
if __name__=='__main__':main()

