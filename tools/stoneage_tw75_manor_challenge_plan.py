"""Replay a Taiwan7.5 manor challenge plan, preserving contradictory threshold evidence."""
import argparse
from fractions import Fraction
from hashlib import sha256,sha1
import json
from pathlib import Path
import re
import urllib.request
from tools.stoneage_early_content_probe import plain,require
from tools.stoneage_wayi_newbie_riding_plan import index_rows
from tools.stoneage_jp2008_cooperation_source import jpeg_size
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'research/recovered/STONEAGE-TW75-MANOR-CHALLENGE-PLAN-SOURCE-R1.json'
URLS=(
'https://web.archive.org/web/20050612011406id_/http://www.wayi.com.tw/stoneage/producer/producer01.asp',
'https://web.archive.org/web/20041206162649id_/http://www.wayi.com.tw/stoneage/producer/producer02.asp?idno=89',
'https://web.archive.org/web/20041207062827id_/http://www.wayi.com.tw/images02/sa0616.JPG')
NAMES=('P0.html','P1.html','I1.jpg')
DERIVED='research/recovered/STONEAGE-CN40-RIDING-CERTIFICATE-MANOR-SOURCE-R1.json'
PINS=[(102,'8f70fa87fc959bdd660f29200c955eff4695c8fa11a17d4c6b28feb5527c5f0b'),
(81,'9eeb1131553dc1e8c2a414cfee105051c920eeb2b4f3a90231d3b42bc405ed4e'),
(140,'77cadb34af123ab9cabccf59c5a5bc854b3542b17f3f77f0fca39da270116828'),
(64,'10630ae42b4e5cfe0be51ebdd3e44c8d09a399bde460ea45c58043866d363971'),
(93,'d351e67fbb39421bc7f1dff892c8c6b92dbc37d90e76a89b4c903fc50234224e'),
(93,'af277f1b35afe9e00e680546c2c3486f303b119e723b823b1179e6bdcab0244d'),
(107,'7abd3062e90ce70ca6b69c084c87ddaca758799d49d418eaf44444cee37c0494'),
(15,'ec323cced68d98d7c6850d3c0953fb1985981cf2864b69b7cd471bbb285af05b')]
BOUNDARIES=dict(original_server_execution_verified=False,exact_client_build=None,index_date_is_body_capture_or_deployment=False,
 proposal_is_verified_patch=False,general_headcount_formula=None,arbitrary_headcount_rounding=None,member_fame_is_five_per_day=False,
 threshold_chosen_engine_comparator=None,threshold_conflict_silently_repaired=False,tie_break_or_replacement_lock_time=None,
 replaced_challenger_resets_24h_timer=None,timezone=None,declaration_endpoints_inclusive=None,cycle_is_weekly=False,
 ceasefire_is_exact_96hours=False,reset_is_all_character_lifetime_fame=False,reward_uses_pre_or_post_reset_momentum=None,
 contribution_point_definition=None,offline_payment_policy=None,challenger_reward=None,no_challenge_reset_rule=None,
 family_bank_transaction_or_persistence_verified=False,crafting_cooking_functions_removed=False,
 image_old_ranking_entries_prove_deployed_retention=False,image_menu_proves_challenge_or_reward_executed=False,
 image_native_client_resolution_proven=False,manual_image_observation_is_independent_ocr=False,
 cn40_top20_rule_transferred_to_tw75=False,regions_are_one_build_or_one_patch_sequence=False,
 original_manor_npc_map_item_or_wire_ids=None,tw10_or_jss1999_backfill=False,raw_sources_committed=False,
 stage_a='7_PARTIAL_2_OPEN',stage_b_and_wiki='GATED',r79='PAUSED_NON_BLOCKING')

def facts():
 return dict(status='OPERATOR_STATED_7.5_PLAN',speaker_as_written='酷哥',
  context=dict(family_function_since_label='2.0',manors_mentioned=9,prior_challenge_basis='聲望值',issues=['CONCENTRATED_ACCESS','UNPOPULAR_VILLAGE_LOW_INCOME']),
  purposes=['MORE_INTERFAMILY_INTERACTION','MANOR_INCOME_REGARDLESS_OF_VILLAGE_POPULARITY'],
  momentum=dict(label='家族氣勢',components=['TRANSFORMED_FAMILY_HEADCOUNT','累計聲望值'],accumulated_fame='SINCE_PREVIOUS_MANOR_BATTLE',general_formula=None),
  example=dict(headcount=100,each_member_fame=5,expression='100*100/10+1+5*100=1501',reported_result=1501,
   arithmetic_result=int(Fraction(100*100,10)+1+5*100),arithmetic_check_only=True,general_formula_proven=False),
  threshold=dict(wording='HIGHER_THAN_NINE_TENTHS_OF_MANOR_FAMILY',challenger_example=900,owner_example=1000,example_eligible=True,
   example_ratio=[9,10],example_relation_to_worded_threshold='EQUAL_NOT_STRICTLY_HIGHER',
   conflict='UNRESOLVED_STRICT_WORDING_VS_EQUALITY_EXAMPLE',chosen_comparator=None),
  displacement=dict(existing_challenger_can_be_replaced=True,replacer_condition='HIGHER_FAMILY_MOMENTUM',tie_policy=None),
  timing=dict(declaration_hours_as_written='晚上6~10點',normalized_hours=[18,22],start_after_successful_declaration_hours=24,
   leader_check_advice_as_written='晚上10點',timezone=None),
  reset=dict(subject='BOTH_FAMILIES_ACCUMULATED_FAME',when='AFTER_MANOR_BATTLE',value=0),
  payout=dict(condition='MANOR_FAMILY_SUCCESSFULLY_DEFENDS',momentum_to_stone_multiplier=10000,
   immediate_recipients='ONLINE_FAMILY_MEMBERS_BY_MOMENTUM_CONTRIBUTION',stone_per_point=5000,
   remainder='FAMILY_BANK',contribution_definition=None,pre_or_post_reset_momentum=None),
  cycle=dict(ceasefire_days=4,declaration_day_ordinal=5,battle_day_ordinal=6,calendar_boundaries=None),
  unchallenged=dict(source_period_term='挑戰期',treated_as='SUCCESSFUL_DEFENSE_WITH_STONE_DISTRIBUTION',reset_rule=None),
  crafting_cooking=dict(planned_removed=['SYNTHESIS_FAME','COOKING_FAME','RELATED_RANKINGS'],crafting_and_cooking_removed=False))

def observation():
 return dict(selected_label='十大家族氣勢',
  other_visible_labels=['十大合成家族','十大料理家族','自己家族氣勢排名'],
  scope='ONE_MENU_SCREEN_NOT_RANKING_RESULTS_OR_MANOR_BATTLE',
  old_entries_and_prospective_removal='COEXIST_IN_SOURCE_NOT_PROOF_OF_DEPLOYED_CANCELLATION_OR_RETENTION',
  original_npc_map_or_sprite_id=None)

def relation():
 return dict(cn40_challenge_rank_change=[10,20],cn40_manor_table_rows=9,
  tw75_proposed_basis='FAMILY_MOMENTUM_WITH_UNRESOLVED_THRESHOLD',cn40_top20_applies_to_tw75=False,
  relation='SEPARATE_REGION_VERSION_DOCUMENTS_NOT_UNIFIED_PATCH_SEQUENCE')

def records():
 f=facts();rows=[]
 def add(kind,data,refs,collection='tutorials'):
  rows.append(dict(record_id=f'TW75-MANOR-{len(rows)+1:02}',entity_type=kind,collection=collection,
   version_profile=('CN40_PORTAL_VS_TW75_OPERATOR_PLAN_SEPARATE_SCOPES' if collection=='versions' else 'TW_WAYI_7.5_PLAN_INDEX_2004_CAPTURED_2004'),source_refs=refs,
   verification_status='SOURCE_DESCRIPTION_NOT_RUNTIME',rights_status='RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED',
   record_revision=1,game_ids=None,source_reported=data))
 add('CONTEXT_AND_PLAN',dict(context=f['context'],purposes=f['purposes'],status=f['status']),['P0','P1'])
 for key in ['momentum','example','threshold','displacement','timing','reset','payout','cycle','unchallenged','crafting_cooking']:
  add(key.upper(),f[key],['P1'])
 add('MENU_VISUAL_AND_PROPOSAL_TENSION',observation(),['P1','I1'],'screens')
 add('CROSS_REGION_RULE_BOUNDARY',relation(),['P1','D1'],'versions')
 return rows

def extract_index(b):
 selected=next(x for x in index_rows(b.decode('big5',errors='strict')) if x['article_id_as_web_key']==89)
 require(selected==dict(article_id_as_web_key=89,title='7.5版報導之二：莊園約戰新規',index_date_as_written='2004-6-17'),'Actual index title/date/link changed')
 return dict(selected=selected,web_key_is_game_id=False)

def extract_body(b):
 h=b.decode('big5',errors='strict');ms=re.findall(r'<span\b[^>]*>\s*(從2.0版.*?)</span>',h,re.S|re.I)
 require(len(ms)==1,'Exactly one actual manor-column body required');body=ms[0]
 ps=[plain(x) for x in re.split(r'<BR>\s*<BR>',body,flags=re.I) if plain(x)]
 require([(len(x),sha256(x.encode()).hexdigest()) for x in ps]==PINS,'Manor source paragraph semantics changed')
 for clause in ['酷哥打算在7.5版','家族人數經運算後加上「累計聲望值」','100*100/10+1+5*100=1501',
 '高於莊園家族九成','氣勢為900','氣勢為1000','氣勢」更高的流浪家族給頂替掉','晚上6~10點',
 '宣戰成功後24小時','兩家族的累計聲望值將同時歸零','家族氣勢將會乘上一萬','在線的家族成員',
 '每點5000石幣','多餘的部份歸家族銀行','休戰期定為四天','第五天為宣戰期','第六天為戰鬥期',
 '視同守莊成功','這兩個部份的聲望值與相關的排行將被完全取消']:
  require(clause in plain(body),'Material plan qualifier missing: '+clause)
 require('src="http://www.wayi.com.tw/images02/sa0616.JPG"' in body,'Actual direct image source changed')
 return dict(paragraphs=[dict(characters=len(x),sha256=sha256(x.encode()).hexdigest()) for x in ps],facts=facts(),
  actual_image_ref='http://www.wayi.com.tw/images02/sa0616.JPG')

def compare_derived(r):
 p=r['derived_input'];require(p['path']==DERIVED,'Finite accepted comparison input')
 b=(ROOT/p['path']).read_bytes();require(len(b)==p['bytes'] and sha256(b).hexdigest()==p['sha256'] and sha1(b'blob '+str(len(b)).encode()+bytes([0])+b).hexdigest()==p['git_blob'],'Accepted CN4 report byte/blob pin changed')
 x=json.loads(b)['inputs'][0]['extracted']['facts']
 require(x['challenge_family_rank_change']==[10,20] and x['manor_rows']==9,'Accepted Mainland documentary facts changed')
 return relation()

def validate(r):
 require(r['schema']=='stoneage.tw75_manor_challenge_plan.source.r1','Schema')
 require([x['url'] for x in r['inputs']]==list(URLS),'Three exact historical inputs')
 require([x['capture_timestamp'] for x in r['inputs']]==['20050612011406','20041206162649','20041207062827'],'Capture scopes conflated')
 require(r['authority']=='OFFICIAL_TW_OPERATOR_PLAN_WITH_SEPARATE_ACCEPTED_CN40_PORTAL_COMPARISON','Authority scope changed')
 require(r['boundaries']==BOUNDARIES and r['records']==records(),'Plan, conflict, reward or evidence boundary promoted')
 require(r['manual_image_observation']==observation() and r['derived_relation']==relation(),'Visual or regional relation changed')
 require(r['next']=='OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-36','Return full portfolio')

def replay(r,payloads):
 validate(r);require(len(payloads)==3,'Two HTML and one original JPEG required')
 for s,b in zip(r['inputs'],payloads):
  require(len(b)==s['bytes'] and sha256(b).hexdigest()==s['sha256'],'Historical byte pin changed')
 extracted=[extract_index(payloads[0]),extract_body(payloads[1])]
 require(extracted==r['extracted'],'Actual documentary derivation changed')
 require(jpeg_size(payloads[2])==[450,338],'Original image dimensions changed')
 return dict(schema='stoneage.tw75_manor_challenge_plan.replay.r1',
  inputs=[dict(id=s['id'],bytes=len(b),sha256=sha256(b).hexdigest()) for s,b in zip(r['inputs'],payloads)],
  extracted=extracted,image_dimensions=[450,338],manual_image_observation=observation(),derived_relation=compare_derived(r),
  equality_threshold_conflict_preserved=True,general_formula_or_reward_engine_executed=False,
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
 print('HISTORICAL_HTML_VERIFIED=2 JPEG_VERIFIED=1 ACCEPTED_DERIVED_INPUT=1 THRESHOLD_CONFLICT_PRESERVED=1 ORIGINAL_SERVER_EXECUTIONS=0')
if __name__=='__main__':main()
