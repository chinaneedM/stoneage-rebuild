"""Replay the bounded Taiwan operator's April 2004 mage attribute repair proposal."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import urllib.request
from tools.stoneage_early_content_probe import plain, require
from tools.stoneage_wayi_newbie_riding_plan import index_rows
from tools.stoneage_jp2008_cooperation_source import jpeg_size

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT/'research/recovered/STONEAGE-TW2004-MAGE-ATTRIBUTE-PLAN-SOURCE-R1.json'
URLS = ['https://web.archive.org/web/20050612011406id_/http://www.wayi.com.tw/stoneage/producer/producer01.asp',
 'https://web.archive.org/web/20041206160744id_/http://www.wayi.com.tw/stoneage/producer/producer02.asp?idno=69',
 'https://web.archive.org/web/20150408182032id_/http://www.wayi.com.tw/images02/sa0405-1s.jpg',
 'https://web.archive.org/web/20040408015726id_/http://www.wayi.com.tw/images02/sa0405-1.jpg']
CAPTURES = ['20050612011406','20041206160744','20150408182032','20040408015726']
PINS = [(56,'fa80ce0be0e9106979fef3459eb49e90e2647b4dce8d96bc8d01c6dbbe704e37'),
 (61,'80e66e2432772a5aca6f4a1f80cb8a417fbc1e0bd77130f99d8836799224ff6f'),
 (148,'cd3664e319ce94499e9d05ccd3a3551c6e00abf005d2365032aff8017187a571'),
 (123,'300fed5ed724ab2c2e11267f9dd5fc111c07faccfc51f3facb671e9768f2f0eb'),
 (147,'2c7e9658c7a67d006602ed1215c36329b04ed48bc6d1c969f088e87f53984729'),
 (88,'05b28d0626a6124477a18c9a0702122061ae89c866d718bfba6534e9b7c065f0'),
 (25,'334fecd8335837cc69e4df299acad7721a4e5d17904f4e4997ecd96f960035d2')]
BOUNDARIES = dict(original_server_execution_verified=False, exact_client_build=None,
 version_number=None, page_template_title_is_article_title=False, index_date_is_deployment=False,
 proposal_is_deployed_patch=False, bug_randomness_is_verified_probability_distribution=False,
 gold_flying_alias_is_original_species_id=False, physical_fire_equals_magic_fire=False,
 mage_damage_is_unconditionally_half_to_each=False, exact_damage_formula=None,
 battlefield_advantage_coefficients=None, spirit_cost_duration_or_stack_rules=None,
 attribute_equality_is_stat_or_species_equality=False, wines_have_verified_names=False,
 wine_attribute_directions_or_amounts=None, wine_price_or_acquisition_steps=None,
 quest_script_dialogue_or_reward_flags_verified=False, npc_name_or_coordinates=None,
 image_is_native_resolution_or_same_build=False, image_visual_is_independent_ocr=False,
 thumbnail_2015_bytes_are_contemporary_2004=False, pictured_mount_is_identified_as_金飛=False,
 pictured_character_is_identified_quest_npc=False, pictured_chat_is_quest_dialogue=False,
 tw10_or_jss1999_backfill=False, raw_sources_committed=False,
 stage_a='7_PARTIAL_2_OPEN', stage_b_and_wiki='GATED', r79='PAUSED_NON_BLOCKING')

def facts():
 return dict(context=dict(status='OPERATOR_REPORTED_BUG_AND_PROPOSED_REPAIR', speaker_as_written='酷哥',
   target='MAGE_ATTACK_SKILL_AGAINST_MOUNTED_ENEMY', distribution_subjects=['RIDER','MOUNT']),
  diagnosis=dict(character_elements=['地','水','火','風'],mage_attack_elements=['火','冰','雷'],
   operator_explanation='MISMATCHED_ELEMENT_SETS_IN_DAMAGE_DISTRIBUTION',
   reported_symptoms=['EARTH_CHARACTER_MORE_EASILY_HURT','RIDER_OF_金飛_LESS_EASILY_HURT','UNCERTAIN_RANDOM_INJURY'],
   original_bug_code_or_probability=None),
  proposed_element_model=dict(physical=['地','水','火','風'],dark_spirit_energy=['火','冰','雷'],
   fire_labels_share_spelling_not_identity=True,physical_interaction='MUTUAL_ELEMENT_RELATIONS',
   magic_relative_to_physical='ATTRIBUTE_NEUTRAL',default_distribution='IN_PRINCIPLE_EQUAL_RIDER_AND_MOUNT'),
  battlefield=dict(replacement_label='戰場屬性優勢',example_spirit='火的精靈',example_effect='STRENGTHEN_FIRE_BATTLEFIELD_ADVANTAGE',
   purpose='REDISTRIBUTE_RIDER_AND_MOUNT_INJURY',coefficients=None),
  directional_examples=dict(setup='EARTH_CHARACTER_RIDING_金飛',
   examples=[dict(spirit='地的精靈',from_subject='RIDER',to_subject='MOUNT'),
             dict(spirit='風的精靈',from_subject='MOUNT',to_subject='RIDER')],
   exact_shift_amount=None,alias_not_species_master=True),
  equality_condition=dict(condition='CHARACTER_ELEMENTS_EXACTLY_MATCH_MOUNT_ELEMENTS',
   stated_result='KEEP_INJURY_EQUALLY_DISTRIBUTED',attribute_point_vector=None),
  wine_plan=dict(quest_label='訐譙龍',planned_new_wines=2,purpose='ASSIST_CHARACTER_ATTRIBUTE_POINT_ADJUSTMENT',
   names=None,point_amounts=None,quest_steps=None,deployment_verified=False))

def observation():
 return dict(scene='ROCKY_CAVE_EDGE_WITH_BLUE_WATER_RED_ORANGE_LONG_NECK_MOUNT_RIDER_AND_SMALL_STANDING_FIGURE',
  full_image_dimensions=[640,480],thumbnail_dimensions=[300,225],
  shared_composition='VISUALLY_SIMILAR_NOT_PROVEN_SAME_CAPTURE_OR_RESAMPLE_PIPELINE',
  capture_relation='FULL_IMAGE_CAPTURE_APRIL_2004_THUMBNAIL_CAPTURE_APRIL_2015',
  visible_chat_speaker_label='酷哥',chat_is_quest_dialogue=False,
  npc_identity=None,mount_species_id=None,wine_menu_or_effect_visible=False,
  mage_attack_or_damage_distribution_visible=False)

def records():
 rows=[]
 for key,value in facts().items():
  rows.append(dict(record_id=f'TW2004-MAGE-{len(rows)+1:02}',entity_type=key.upper(),collection='tutorials',
   version_profile='TW_WAYI_INDEX_APRIL_2004_CAPTURE_DECEMBER_2004_UNNUMBERED',source_refs=['P0','P1'],
   verification_status='OPERATOR_DOCUMENT_DESCRIPTION_NOT_RUNTIME',rights_status='RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED',
   record_revision=1,game_ids=None,source_reported=value))
 rows.append(dict(record_id='TW2004-MAGE-08',entity_type='QUEST_RELATED_IMAGE_CONTEXT',collection='screens',
  version_profile='TW_WAYI_LINKED_IMAGE_CAPTURE_2004_THUMBNAIL_2015_SEPARATE',source_refs=['P1','I1','I2'],
  verification_status='MANUAL_VISUAL_OBSERVATION_NOT_RUNTIME',rights_status='RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED',
  record_revision=1,game_ids=None,source_reported=observation()))
 return rows

def extract_index(b):
 row=next(x for x in index_rows(b.decode('big5',errors='strict')) if x['article_id_as_web_key']==69)
 require(row==dict(article_id_as_web_key=69,title='解開法師變強之謎？！',index_date_as_written='2004-4-5'),'Actual index leaf row changed')
 return dict(selected=row,web_key_is_game_id=False)

def extract_body(b):
 h=b.decode('big5',errors='strict')
 matches=re.findall(r'<span class="font_01">(.*?)</span>',h,re.S)
 require(len(matches)==1,'Exactly one actual mage column required')
 body=matches[0]
 paragraphs=[plain(x) for x in re.split(r'\r?\n\s*\r?\n',body) if plain(x)]
 require([(len(x),sha256(x.encode()).hexdigest()) for x in paragraphs]==PINS,'Mage paragraph semantics changed')
 refs=['http://www.wayi.com.tw/images02/sa0405-1s.jpg','http://www.wayi.com.tw/images02/sa0405-1.jpg']
 require('src="'+refs[0]+'"' in body and 'href="'+refs[1]+'"' in body,'Actual thumbnail and linked image changed')
 return dict(paragraphs=[dict(characters=len(x),sha256=sha256(x.encode()).hexdigest()) for x in paragraphs],
  facts=facts(),direct_image_refs=refs,template_title='石器時代--精靈的召喚',template_title_is_article_title=False)

def validate(r):
 require(r['schema']=='stoneage.tw2004_mage_attribute_plan.source.r1','Schema')
 require(r['authority']=='OFFICIAL_TW_OPERATOR_DIAGNOSIS_AND_PROPOSAL_UNNUMBERED_APRIL_2004','Authority/version scope')
 require(r['records']==records() and r['boundaries']==BOUNDARIES,'Rule, proposal or identity boundary promoted')
 require([x['id'] for x in r['inputs']]==['P0','P1','I1','I2'],'Finite index/body/thumbnail/linked original')
 require([x['url'] for x in r['inputs']]==URLS and [x['capture_timestamp'] for x in r['inputs']]==CAPTURES,'Actual independent capture timestamps')
 require(r['manual_image_observation']==observation() and r['image_dimensions']==[[300,225],[640,480]],'Bounded visual observation')
 require(r['next']=='OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-37','Return full portfolio')

def replay(r,payloads):
 validate(r);require(len(payloads)==4,'Two HTML and two JPEG required')
 for s,b in zip(r['inputs'],payloads):
  require(len(b)==s['bytes'] and sha256(b).hexdigest()==s['sha256'],'Historical byte pin changed')
 extracted=[extract_index(payloads[0]),extract_body(payloads[1])]
 require(extracted==r['extracted'],'Source derivation changed')
 dimensions=[jpeg_size(b) for b in payloads[2:]]
 require(dimensions==r['image_dimensions'],'Image dimensions changed')
 return dict(schema='stoneage.tw2004_mage_attribute_plan.replay.r1',
  inputs=[dict(id=s['id'],bytes=len(b),sha256=sha256(b).hexdigest()) for s,b in zip(r['inputs'],payloads)],
  extracted=extracted,image_dimensions=dimensions,manual_image_observation=r['manual_image_observation'],
  original_server_executed=False,proposal_deployment_verified=False,raw_sources_in_output=False)

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--fetch',action='store_true');p.add_argument('--source-dir',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 require(a.fetch!=bool(a.source_dir),'Choose fetch or transient directory')
 r=json.loads(REPORT.read_text());payloads=[]
 for s,n in zip(r['inputs'],['P0.html','P1.html','I1.jpg','I2.jpg']):
  if a.fetch:
   with urllib.request.urlopen(s['url'],timeout=45) as response:
    require(response.status==200 and response.url==s['url'],'Unexpected redirect/status');b=response.read(2_000_001);require(len(b)<=2_000_000,'Oversized source')
  else:b=(a.source_dir/n).read_bytes()
  payloads.append(b)
 out=replay(r,payloads);a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print('HISTORICAL_HTML_VERIFIED=2 JPEG_VERIFIED=2 ORIGINAL_SERVER_EXECUTIONS=0 PROPOSAL_DEPLOYMENT_VERIFIED=0')
if __name__=='__main__':main()
