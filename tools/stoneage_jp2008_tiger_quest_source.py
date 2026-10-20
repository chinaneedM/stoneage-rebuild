"""Replay named tiger quest story evidence, preserving poem, reward and image gaps."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import urllib.request
from tools.stoneage_jp2008_shadow_release import compact, require
from tools.stoneage_jp2008_cooperation_source import jpeg_size

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'research/recovered/STONEAGE-JP2008-TIGER-QUEST-SOURCE-R1.json'
MEDIA='https://www.4gamer.net/games/013/G001377/20080620060/'
ORIGINAL='http://stoneage.to/update/20080624_update_tora_quest.html'
OFFICIAL='https://web.archive.org/web/20080929194642id_/'+ORIGINAL
URLS=[MEDIA,OFFICIAL]+[MEDIA+'SS/'+n+'.jpg' for n in ['001','002','003','004']]
NAMES=['M1.html','O1.html','001.jpg','002.jpg','003.jpg','004.jpg']
OFFICIAL_IMAGE_REFS=['http://stoneage.to/img/update/20080624_quest_banner.gif']+['http://www.stoneage.to/img/update/20080624_quest'+s+'.gif' for s in ['','1','2','3','4']]
BOUNDARIES=dict(exact_client_build=None,version_number=None,original_server_execution_verified=False,
 announced_date_is_verified_rollout=False,official_september_capture_is_june_launch_bytes=False,
 current_media_images_are_2008_captured_bytes=False,six_official_image_404s_prove_global_absence=False,
 media_images_substitute_for_missing_official_gif_bytes=False,seven_poem_chapters_are_seven_quest_chapters=False,
 full_seven_chapter_poem_recovered=False,three_tigers_are_three_species_or_complete_roster=False,
 tiger_names_stats_or_original_ids=None,mountain_is_proven_on_geel_island=False,original_map_coordinates=None,
 mysterious_arrival_named_or_caused_by_known_entity=False,nisu_incident_identified_or_dated=False,
 riddle_motifs_are_verified_quest_rewards=False,pure_water_is_verified_item_name_or_pet=False,
 weapon_armor_names_stats_or_reward_chances=None,capture_steps_or_probability=None,
 entry_level_or_prerequisite=None,script_dialogue_branch_or_save_flags=None,
 image_party_count_is_party_capacity=False,image_figures_have_verified_npc_or_pet_identity=False,
 image_is_native_client_resolution=False,manual_observation_is_independent_ocr=False,
 screenshot_is_successful_capture_or_reward_delivery=False,tw10_or_jss1999_backfill=False,
 raw_sources_committed=False,stage_a='7_PARTIAL_2_OPEN',stage_b_and_wiki='GATED',r79='PAUSED_NON_BLOCKING')

def facts():
 return dict(announcement=dict(published='2008/06/20 22:28',announced_update_date='2008-06-24',timezone=None,
   operator_editorially_attributed='デジパーク',release_marked_as_quotation=True,rollout_verified=False),
  named_content=dict(dungeon='虎追い山',quest_media='三匹の虎 〜虎追いの詩〜',quest_official='三匹の虎～虎追いの詩～',
   quest_official_size_label='大規模クエスト',poem='虎追いの詩',poem_reported_chapters=7,
   mountain_reported_resident_tigers=3,actual_species_roster=None),
  poem_context=dict(place_of_recirculation='ギール島',purpose='TRADITIONAL_VERSE_ABOUT_CAPTURING_CUNNING_TIGERS',
   role='DUNGEON_STRATEGY_KEY',full_chapter_text_obtained=False,quest_chapter_count=None),
  world_story=dict(incident_label='ニースの異変',other_cause='CHANGES_IN_PEOPLES_LIVES',
   narrative_chain=['INCIDENT_AND_LIFE_CHANGES','CUNNING_TIGERS_DISAPPEARED','POEM_FORGOTTEN',
                    'UNSPECIFIED_ARRIVAL','POEM_RECIRCULATES'],arrival_identity=None,original_era_identification=None),
  official_enigma=dict(motifs=['PURE_WATER','PURSUED_TIGER_WEAPON','PURSUED_TIGER_ARMOR','FUTURE_ENCOUNTER_REVEALS_MEANING'],
   interpretation='UNRESOLVED_POETIC_TEASER_NOT_VERIFIED_ITEM_TABLE_OR_REWARD',full_seven_chapters=False),
  official_disclaimers=dict(images_are_illustrative_may_differ=True,future_balance_may_change_content=True,
   official_capture_timestamp='20080929194642'))

def observations():
 return [dict(image='I1',scene='RED_BLACK_STRIPED_TIGER_NEAR_PARTY_STRAW_AND_BONES_ON_RED_GROUND'),
  dict(image='I2',scene='PARTY_IN_GRAY_ROCK_CORRIDOR_WITH_BLACK_UNEXPLORED_SURROUND'),
  dict(image='I3',scene='PARTY_AND_ADDITIONAL_HUMANOID_FIGURE_IN_GRAY_ROCK_INTERIOR'),
  dict(image='I4',scene='PARTY_ON_SAND_NEAR_PALM_AND_LARGE_RIB_BONES')]

def records():
 rows=[]
 for key,value in facts().items():
  rows.append(dict(record_id=f'JP2008-TIGER-{len(rows)+1:02}',entity_type=key.upper(),
   collection='versions' if key=='announcement' else 'quests',
   version_profile='LATER_OFFICIAL:JP_DIGIPARK_2008_TIGER_QUEST_UNNUMBERED',source_refs=['M1','O1'] if key not in ['official_enigma','official_disclaimers'] else ['O1'],
   verification_status='SOURCE_REPORTED_NOT_RUNTIME',rights_status='RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED',
   record_revision=1,game_ids=None,source_reported=value))
 for o in observations():
  rows.append(dict(record_id=f'JP2008-TIGER-{len(rows)+1:02}',entity_type='QUEST_ASSOCIATED_SCENE',collection='screens',
   version_profile='CURRENT_MEDIA_IMAGE_ASSOCIATED_WITH_JP_2008_RELEASE_NOT_2008_CAPTURE',source_refs=['M1',o['image']],
   verification_status='MANUAL_VISUAL_OBSERVATION_NOT_RUNTIME',rights_status='RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED',
   record_revision=1,game_ids=None,source_reported=o))
 return rows

def extract_media(b):
 h=b.decode('utf-8-sig');require(h.count('以下，リリースより')==1,'Release boundary ambiguous')
 before,quoted=h.split('以下，リリースより',1);require('2008/06/2022:28' in compact(before) and 'デジパークは' in compact(before),'Editorial date/operator attribution')
 q=quoted.split('<span class="blockquote">',1)[1].split('初夏の二大協力イベント',1)[0];core=compact(q)
 require(len(core.encode())==1180 and sha256(core.encode()).hexdigest()=='e55c11ff1dddbbd7674b2f3b8c55f231b9096e5b6a710d7d62b7110fbeee0f01','Tiger release core semantics changed')
 require('href="'+ORIGINAL+'"' in q,'Exact official outbound')
 intro=h.split('<div class="entry-content">',1)[1].split('以下，リリースより',1)[0]
 refs=re.findall(r"OVERLAY_SS_open\(event,'(/games/013/G001377/20080620060/SS/00[1-4]\.jpg)'",intro)
 require(refs==['/games/013/G001377/20080620060/SS/'+n+'.jpg' for n in ['001','002','003','004']],'Actual four linked scene images changed')
 return dict(core_utf8_bytes=len(core.encode()),core_sha256=sha256(core.encode()).hexdigest(),
  direct_full_image_refs=refs,announcement=facts()['announcement'],named_content=facts()['named_content'],
  poem_context=facts()['poem_context'],world_story=facts()['world_story'])

def extract_official(b):
 h=b.decode('utf-8-sig');require('charset=UTF-8' in h,'Actual official encoding')
 require(h.count('<!-- start 内容 -->')==1 and h.count('<!-- end 内容 -->')==1,'Official content boundaries')
 section=h.split('<!-- start 内容 -->',1)[1].split('<!-- end 内容 -->',1)[0];core=compact(section)
 require(len(core.encode())==1220 and sha256(core.encode()).hexdigest()=='8787c1edf9cdbdd8d331382e5efe20b5f2d4db006eb10b5879a62f8f7a3238cf','Official story/enigma/warnings changed')
 refs=re.findall(r'<img[^>]+src="([^"]*/img/update/20080624_[^"]+)"',section)
 # Banner precedes the content wrapper; retain its actual reference too.
 refs=[re.search(r'<img[^>]+src="([^"]*20080624_quest_banner.gif)"',h)[1]]+refs
 require(refs==OFFICIAL_IMAGE_REFS,'Actual official image references changed')
 return dict(core_utf8_bytes=len(core.encode()),core_sha256=sha256(core.encode()).hexdigest(),
  direct_image_refs=refs,official_enigma=facts()['official_enigma'],official_disclaimers=facts()['official_disclaimers'])

def validate(r):
 require(r['schema']=='stoneage.jp2008_tiger_quest.source.r1','Schema')
 require([s['url'] for s in r['inputs']]==URLS,'Exact two HTML/four JPEG scope')
 require(r['records']==records() and r['boundaries']==BOUNDARIES,'Story, reward, chapter or visual boundary promoted')
 require(r['manual_image_observations']==observations(),'Bounded visual observations')
 require(len(r['official_image_attempts'])==6 and [x['original_url'] for x in r['official_image_attempts']]==OFFICIAL_IMAGE_REFS and all(x['status']==404 and x['page_obtained'] is False for x in r['official_image_attempts']),'Six finite actual failed original image requests')
 require(r['inputs'][1]['capture_timestamp']=='20080929194642','September official snapshot distinct from June announcement')
 require(r['next']=='OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-38','Return whole portfolio')

def replay(r,payloads):
 validate(r);require(len(payloads)==6,'Exactly two HTML and four inspected JPEG')
 require(len(payloads[1])==r['inputs'][1]['bytes'] and sha256(payloads[1]).hexdigest()==r['inputs'][1]['sha256'],'Historical official byte pin changed')
 e=[extract_media(payloads[0]),extract_official(payloads[1])];require(e==r['extracted'],'Documentary derivation changed')
 for s,b in zip(r['inputs'][2:],payloads[2:]):
  require(len(b)==s['bytes'] and sha256(b).hexdigest()==s['sha256'] and jpeg_size(b)==s['dimensions']==[250,200],'Inspected media image bytes or dimensions changed')
 return dict(schema='stoneage.jp2008_tiger_quest.replay.r1',inputs=[dict(id=s['id'],bytes=len(b),sha256=sha256(b).hexdigest()) for s,b in zip(r['inputs'],payloads)],
  extracted=e,manual_image_observations=observations(),image_dimensions=[jpeg_size(b) for b in payloads[2:]],
  original_server_executed=False,full_seven_chapter_poem_recovered=False,quest_rewards_verified=False,
  official_gif_bytes_obtained=0,raw_sources_in_output=False)

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--fetch',action='store_true');p.add_argument('--source-dir',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();require(a.fetch!=bool(a.source_dir),'Choose fetch or transient directory')
 r=json.loads(REPORT.read_text());payloads=[]
 for u,n in zip(URLS,NAMES):
  if a.fetch:
   with urllib.request.urlopen(u,timeout=45) as response:
    require(response.status==200 and response.url==u,'Unexpected status/redirect');b=response.read(2_000_001);require(len(b)<=2_000_000,'Oversized source')
  else:b=(a.source_dir/n).read_bytes()
  payloads.append(b)
 out=replay(r,payloads);a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print('HTML_VERIFIED=2 JPEG_VERIFIED=4 ORIGINAL_SERVER_EXECUTIONS=0 FULL_POEM_RECOVERED=0 REWARDS_VERIFIED=0')
if __name__=='__main__':main()
