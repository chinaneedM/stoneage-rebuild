"""Replay an early Mainland-hosted battle guide; never execute original combat."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import struct
import urllib.request
from tools.stoneage_jp2008_shadow_release import compact,require
from tools.stoneage_cn20_riding_source import Links
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'research/recovered/STONEAGE-CN20-BATTLE-COMMANDS-DEFEAT-SOURCE-R1.json'
URLS=(
'https://web.archive.org/web/20011204194619id_/http://www.waei.com.cn/ZHUANQU/stoneage2/pet/new_pet.asp',
'https://web.archive.org/web/20011201043456id_/http://www.waei.com.cn/ZHUANQU/stoneage2/tyro/combat.asp',
'https://web.archive.org/web/20011023202109id_/http://waei.com.cn/ZHUANQU/stoneage2/tyro/img/5.gif')
NAMES=('nav.html','combat.html','battle-reference.gif')
LABELS=['攻击','咒术','捕获','请求帮助','防御','道具','宠物','脱离']
POSITIONS=['UPPER_LEFT','UPPER_SECOND','UPPER_THIRD','UPPER_RIGHT','LOWER_LEFT','LOWER_SECOND','LOWER_THIRD','LOWER_RIGHT']
BOUNDARIES=dict(operator_authorship_verified=False,named_guide_author=None,original_server_execution_verified=False,exact_client_build=None,
 original_command_npc_pet_map_or_item_ids=None,command_pixel_rectangles_or_wire_ids=None,player_round_input_is_agility_execution_order=False,
 exact_command_timeout=None,capture_success_rate=None,capture_species_or_map_rules=None,post_rebirth_capacity=None,
 five_is_all_versions_or_post_rebirth_cap=False,help_is_unrestricted_join=False,help_turn_cost=None,
 defense_is_guaranteed_or_half_damage=False,escape_success_probability=None,leader_flee_is_automatic_leader_transfer=False,
 pet_standby_is_original_numeric_state=False,protect_loyalty_threshold_or_probability=None,
 no_death_means_no_penalties=False,all_faints_go_to_record_point=False,solo_hp1_is_max_hp_or_percent=False,
 team_condition_is_formal_boolean=False,overkill_damage_multiplier=None,savepoint_id_or_transition_protocol=None,
 source_typo_silently_corrected=False,image_is_battle_command_screen=False,image_and_body_same_build=False,
 image_english_labels_authenticate_region_or_language=False,image_has_original_sprite_binding=False,
 tw10_or_jss1999_backfill=False,raw_sources_committed=False,stage_a='7_PARTIAL_2_OPEN',stage_b_and_wiki='GATED',r79='PAUSED_NON_BLOCKING')

def facts():
 return dict(edition_label='石器时代2.0',encounter='FIELD_MOVEMENT_RANDOM_ENCOUNTERS_SOURCE_DESCRIPTION_NO_RATE',
  scene='PLAYER_OR_PARTY_LOWER_RIGHT_SOURCE_PROSE_NOT_PIXELS',network_delay='GUIDE_ATTRIBUTES_OCCASIONAL_DELAY_TO_SERVER_TRANSFER',
  loop=['BATTLE_SCREEN','WAIT_FOR_COMMANDS','PLAYER_COMMAND_INPUTS_IN_TURN_AS_WRITTEN','PARTICIPATING_PET_COMMANDS','CONFIRM_OR_WAIT_TIMEOUT','BATTLE_RESOLUTION','IF_UNFINISHED_WAIT_AGAIN'],
  labels=LABELS,positions=POSITIONS,attack='SELECT_COMMAND_THEN_TARGET',spell='SPIRIT_MAGIC_ATTACHED_TO_EQUIPMENT',
  capture=dict(chance='MAY_FAIL',full_capacity_blocks_capture=True,pre_rebirth_capacity=5,post_rebirth='INCREASED_UNSPECIFIED_AMOUNT'),
  help=dict(symbol='HELP',other_players_can_join_reported=True,slots_eligibility_timing=None),
  defense='OFTEN_REDUCES_DAMAGE_NO_MULTIPLIER',item='USE_ITEM_UNSPECIFIED',
  pet=dict(actions_as_written=['参战','退避'],command_eligible_state_as_written='待机',state_numeric_id=None),
  escape=dict(after_member_leaves_battle='LEAVES_PARTY',after_leader_leaves_battle='PARTY_DISBANDS',success_probability=None),
  pet_skill=dict(input_surface='SKILL_LIST_THEN_TARGET',actions=['ATTACK_USING_SKILL','DEFEND'],protection='SOME_HIGH_LOYALTY_PETS_MAY_BLOCK_FATAL_BLOW',source_typo_as_written='宠物义何中技能'),
  solo_defeat=dict(hp_trigger=0,state_label='气绝',result='BATTLE_FAILURE',on_return_to_scene_hp=1,return_location=None),
  team_defeat=dict(continuation='TEAMMATE_NOT_LEFT_OR_NOT_FAINTED_AS_SOURCE_WORDING',until='ONE_SIDE_WIPED_OUT',formal_boolean=None),
  overkill=dict(damage='FAR_ABOVE_CURRENT_HP_SOURCE_WORDING',visual='SPINS_AND_FLIES_OUT',destination='纪录点',exact_threshold=None))

def records():
 f=facts();rows=[]
 def add(kind,collection,data,refs):
  rows.append(dict(record_id=f'CN20-BATTLE-{len(rows)+1:02}',entity_type=kind,collection=collection,
   version_profile='CN_OPERATOR_HOST_2.0_GUIDE_CAPTURE_2001_NOT_EXACT_BUILD',source_refs=refs,
   verification_status='DOCUMENT_OR_IMAGE_DESCRIPTION_NOT_RUNTIME',rights_status='RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED',record_revision=1,game_ids=None,source_reported=data))
 meanings=[f['attack'],f['spell'],f['capture'],f['help'],f['defense'],f['item'],f['pet'],f['escape']]
 for a,b,c in zip(LABELS,POSITIONS,meanings):add('PLAYER_BATTLE_COMMAND','tutorials',dict(label=a,relative_position=b,meaning=c,wire_or_pixel_binding=None),['B1'])
 add('ENCOUNTER_AND_ROUND_INPUT','tutorials',dict(encounter=f['encounter'],scene=f['scene'],network=f['network_delay'],loop=f['loop'],timeout_seconds=None),['B1'])
 add('PET_SKILL_AND_PROTECTION','skills',f['pet_skill'],['B1'])
 for key in ['solo_defeat','team_defeat','overkill']:add(key.upper(),'tutorials',f[key],['B1'])
 add('ILLUSTRATION_MISMATCH','screens',dict(observation='OUTDOOR_RIDER_ON_QUADRUPED_WITH_NEARBY_HUMAN_NO_BATTLE_COMMAND_GRID',
  visible_labels=['MENU','Mail','Action','Eng'],original_character_pet_or_sprite_ids=None,battle_ui_verified=False,body_same_build=False),['B1','I1'])
 return rows

def extract_nav(b):
 h=b.decode('gb18030',errors='strict');p=Links();p.feed(h)
 matches=[dict(label=a,href=u) for a,u in p.links if a=='战斗系统']
 require(matches==[dict(label='战斗系统',href='/ZHUANQU/stoneage2/tyro/combat.asp')],'Actual named combat route changed')
 return matches[0]

def extract_body(b):
 h=b.decode('gb18030',errors='strict');t=compact(h)
 require('<title>石器时代2.0</title>' in h,'Edition label absent')
 marker='《石器时代2.0》的战斗采用回合制';require(t.count(marker)==1 and t.count('北京华义联合软件开发有限公司')==1,'Body/footer boundary missing or ambiguous')
 core=t.split(marker,1)[1].split('北京华义联合软件开发有限公司')[0]
 for clause in ['玩家或玩家所属的队伍会在画面的右下方','由右上方的指令视窗选择指令','由各个玩家轮流下指令',
 '按决定键或待机时间结束后，战斗开始','使用装备上所附带的精灵魔法','但不一定能成功',
 '为转生之前为5，转生后所持宠物的最大数有所增加','其他人在这时可以看到画面上出现HELP符号',
 '往往能减轻所受到的伤害','战斗时，能接受指令的只有待机状态的宠物而已','如果是领袖退出战斗的话，表示解散这个队伍',
 '宠物义何中技能','某些忠诚度高的宠物还可以替主人挡住致命的一击',
 '单人战斗中如果HP降到0','回到场景画面时HP会自动恢复为1','只要同队队友还没退出战斗或没有气绝',
 '战斗将持续到某一方全军覆没为止','伤害远远高于你现有的HP','直接在纪录点出现']:
  require(clause in core,'Material battle clause missing: '+clause)
 hp=re.search(r'回到场景画面时HP会自动恢复为(\d+)；',core)
 require(hp is not None and int(hp[1])==1,'Solo return HP must be exactly one, not a numeric prefix')
 labels=re.findall(r'(攻击|咒术|捕获|请求帮助|防御|道具|宠物|脱离)（(?:上部|下部)[^）]+）：',core)
 require(labels==LABELS,'Eight source-position command sequence changed')
 require('href="img/5.gif"' in h and 'src="img/5s.gif"' in h,'Actual illustration full/thumbnail link missing')
 require(not any(x in core for x in ['作者：','作者:','来源：','来源:']),'Article authorship needs fresh review')
 return dict(core_utf8_bytes=len(core.encode()),core_sha256=sha256(core.encode()).hexdigest(),facts=facts(),image_ref=dict(full='img/5.gif',thumbnail='img/5s.gif',declared_thumbnail_size=[240,180]),named_guide_author=None)

def image_metadata(b):
 require(b[:6] in (b'GIF87a',b'GIF89a') and len(b)>=13,'Not GIF')
 size=list(struct.unpack('<HH',b[6:10]));require(size==[640,480],'Unexpected image dimensions')
 return dict(format='GIF',dimensions=size,observation='OUTDOOR_RIDING_SCENE_NOT_BATTLE_MENU',original_sprite_binding=None)

def validate(r):
 require(r['schema']=='stoneage.cn20_battle_commands_defeat.source.r1','Schema')
 require([x['url'] for x in r['inputs']]==list(URLS),'Three exact source inputs')
 require(r['authority']=='OPERATOR_HOSTED_UNSIGNED_GUIDE_AUTHOR_UNVERIFIED','Hosting promoted to authored rule')
 require(r['boundaries']==BOUNDARIES,'Unknown or regional boundary promoted')
 require(r['records']==records(),'Commands, flow or defeat contracts changed')
 require([x['capture_timestamp'] for x in r['inputs']]==['20011204194619','20011201043456','20011023202109'],'Capture dates conflated')
 require(r['next']=='OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-35','Return whole portfolio')

def replay(r,payloads):
 validate(r);require(len(payloads)==3,'One known navigation, one body and one linked GIF')
 for s,b in zip(r['inputs'],payloads):
  require(len(b)==s['bytes'] and sha256(b).hexdigest()==s['sha256'],'Exact historical input byte pin changed')
 extracted=[extract_nav(payloads[0]),extract_body(payloads[1]),image_metadata(payloads[2])]
 require(extracted==[s['extracted'] for s in r['inputs']],'Documentary semantics changed')
 return dict(schema='stoneage.cn20_battle_commands_defeat.replay.r1',inputs=[dict(id=s['id'],bytes=len(b),sha256=sha256(b).hexdigest()) for s,b in zip(r['inputs'],payloads)],
  extracted=extracted,command_labels=LABELS,solo_hp0_returns_hp1_reported=True,all_faints_return_savepoint_proven=False,
  original_server_executed=False,image_battle_ui_verified=False,raw_sources_in_output=False)

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
 print('HISTORICAL_HTML_VERIFIED=2 GIF_VERIFIED=1 PLAYER_COMMAND_LABELS=8 ORIGINAL_SERVER_EXECUTIONS=0')
if __name__=='__main__':main()
