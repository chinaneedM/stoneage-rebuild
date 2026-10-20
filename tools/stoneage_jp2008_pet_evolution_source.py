"""Replay Japanese 2008 pet-evolution release and a separately dated official page."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import struct
import urllib.request
from tools.stoneage_jp2008_shadow_release import compact,require
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'research/recovered/STONEAGE-JP2008-PET-EVOLUTION-SOURCE-R1.json'
URLS=(
'https://www.4gamer.net/games/013/G001377/20081111023/',
'https://web.archive.org/web/20090217151837id_/http://stoneage.to:80/update/20081111_update_ev1.html',
'https://www.4gamer.net/games/013/G001377/20081111023/TN/001.gif',
'https://www.4gamer.net/games/013/G001377/20081111023/TN/002.gif',
'https://www.4gamer.net/games/013/G001377/20081111023/TN/003.gif')
NAMES=('evolution.html','official-historical.html','evolution-reference.gif','pet-002.gif','pet-003.gif')
PETS=['ベルガー','ベルイガー','ゴルシス','キングサーベル']
MASKS=['？？ルガー','？？？イガー','？？シス','？？？サーベル']
COMPONENTS=['進化の秘宝','剣虎進化再抽選チケット','餌付け薬[変:餌付けの輪丙]']
BOUNDARIES=dict(exact_client_build=None,numeric_release_version=None,original_server_execution_verified=False,
 media_2008_original_html_obtained=False,official_page_is_20081111_snapshot=False,first_day_deployment_independently_verified=False,
 evolved_names_unmasked=False,original_pet_npc_map_item_ids=None,relative_northwest_is_coordinates=False,
 quest_min_level_or_rebirth=None,evolution_probability=None,mutation_probability=None,stat_growth_formula=None,
 success_level=None,failure_resets_skills_or_owner_proven=False,failure_initial_stats_numbers=None,
 one_pet_per_ritual_is_carry_limit=False,ordinary_quest_is_100_percent_success=False,ordinary_quest_fee_gstone=None,
 campaign_end_is_system_removal=False,reroll_is_unlimited=False,reroll_once_is_lifetime_limit=False,exp_transfer_fraction=None,
 flavor_spirit_is_named_world_entity=False,image_is_live_runtime_or_original_sprite=False,
 red_or_black_pixels_prove_elements_or_mutation=False,official_image_404_proves_all_images_missing=False,
 historical_image_bytes_obtained=False,cross_region_rebirth_or_fusion_equated=False,
 raw_sources_committed=False,stage_a='7_PARTIAL_2_OPEN',stage_b_and_wiki='GATED',r79='PAUSED_NON_BLOCKING')

def common_location():
    return dict(island='ミライア島',village='カラの村',relative_location='NORTHWEST_OF_VILLAGE',dungeon='進化の洞窟',npc='進化Gさん')

def extract_media(b):
    h=b.decode('utf-8-sig');t=compact(h);marker='メーカー発表文の内容をそのまま掲載しています＞'
    require(t.count(marker)==1 and '配信元デジパーク配信日2008/11/11' in t,'Explicit release attribution missing')
    release=t.split(marker,1)[1];require(release.startswith('株式会社デジパーク'),'Issuer not inside release')
    end='3）『餌付け薬[変:餌付けの輪丙]』';require(end in release,'Bundle boundary missing')
    core=release[:release.index(end)+len(end)]
    clauses=['2008年11月11日に「進化ペットアップデート」と「ペット進化キャンペーン」','生まれ変わりの時、精霊のいたずらにより',
     '「ベルガー」「ベルイガー」「ゴルシス」「キングサーベル」の4種類','ペットの見た目も変化','突然変異により特殊なステータス',
     '始めたばかりのプレイヤーの方にも1つの目標','2008年11月11日（火）定期メンテナンス終了後',
     '「ミライア島」の「カラの村」から北西','NPC「進化Gさん」','クエストをクリアすると一定の確率でペットが進化',
     '失敗した場合は、ペットがLv1の状態','何度でも挑戦','画像はイメージです。実際のゲーム内とは異なります',
     '必ず進化が成功する便利なアイテム「進化の秘宝」','ステータス再抽選が一度できる「剣虎進化再抽選チケット」',
     'キャラクターの取得した経験値をペットに分配','2008年11月18日（火）定期メンテナンス開始時',
     '価格：350Gstone','以下の3点セット']
    for s in clauses:require(s in core,'Material source clause missing: '+s)
    target='http://stoneage.to/update/20081111_update_ev1.html';require('href="'+target+'"' in h,'Actual official outbound link changed')
    refs=re.findall(r'src="(/games/013/G001377/20081111023/TN/\d+\.gif)"',h)
    require(refs==['/games/013/G001377/20081111023/TN/'+n+'.gif' for n in ['001','002','003','004']],'Actual finite image references changed')
    facts=dict(issuer='株式会社デジパーク',published_label='2008/11/11 14:28',announced_implementation='2008-11-11_AFTER_MAINTENANCE',
       eligible_pet_labels=PETS,first_batch_not_complete_game_roster=True,location=common_location(),
       flow=['FIND_EVOLUTION_CAVE_NORTHWEST_OF_KARA','TALK_TO_SHINKA_G_SAN','COMPLETE_TRIAL_QUEST','CHANCE_OF_EVOLUTION','REPEATABLE_TRIAL'],
       failure_level=1,repeatable=True,success='STRONGER_STATUS_AND_CHANGED_APPEARANCE_SOURCE_DESCRIPTION_NO_NUMBERS',
       mutation='SOMETIMES_SPECIAL_STATUS_NO_RATE',new_and_existing_player_goal='EXPLICIT_RELEASE_PURPOSE_NOT_NO_PREREQUISITE_PROOF',
       flavor='SPIRITS_MISCHIEF_POETIC_INTRO_NOT_NAMED_CAUSE',
       campaign=dict(start='2008-11-11_AFTER_MAINTENANCE',end='2008-11-18_BEFORE_MAINTENANCE',bundle='剣虎進化セットチケット',
         price=350,currency_as_written='Gstone',components=COMPONENTS,secret_item='GUARANTEED_EVOLUTION_CLAIM_ITEM_NOT_BASE_PROBABILITY',
         reroll='ONE_STATUS_REROLL_FOR_FOUR_EVOLVED_PET_TYPES',gift='HUMAN_GAINED_EXPERIENCE_DISTRIBUTION_TO_PET_NO_RATIO'))
    return dict(core_utf8_bytes=len(core.encode()),core_sha256=sha256(core.encode()).hexdigest(),facts=facts,official_link=target,image_refs=refs)

def extract_official(b):
    h=b.decode('utf-8-sig');t=compact(h);start='ペット進化アップデート～エボリューション～■第一弾■'
    require(t.count(start)==1 and '[×]ページを閉じる' in t,'Official article boundaries missing')
    core=t.split(start,1)[1].split('[×]ページを閉じる')[0]
    for s in ['2008年11月11日（火）16:00定期メンテナンス完了後','「ミライア島」カラの村の北西','「進化の洞窟」',
       '「進化Gさん」','試練をクリア','進化するかしないかは、時の運','Lv1に戻りステータスやペットの名前なども初期の状態',
       '何度でも受ける','1度に進化できるペットは、1匹のみ','画像はイメージです。実際とは異なる場合',
       '今後のバランス調整等によって、内容を余儀なく変更']:
        require(s in core,'Official-page condition/qualification missing: '+s)
    pairs=re.findall(r'「([^」]+)」⇒進化後「([^」]+)」',core);require(pairs==list(zip(PETS,MASKS)),'Actual masked-name relationships changed')
    require('image/20081111_ev_02.gif' in h,'Actual official image link missing')
    return dict(core_utf8_bytes=len(core.encode()),core_sha256=sha256(core.encode()).hexdigest(),facts=dict(
        date_time_as_written='2008年11月11日（火）16:00定期メンテナンス完了後',location=common_location(),
        chance='LUCK_UNSPECIFIED',repeatable=True,one_pet_per_attempt=1,
        failure=dict(level=1,status='INITIAL_STATE_UNSPECIFIED_NUMBERS',name='INITIAL_STATE_UNSPECIFIED_NAME',skills=None,owner=None),
        eligibility_name_masks=[dict(before=a,evolved_mask=b,canonical_evolved_name=None) for a,b in pairs],
        visual_notice='ILLUSTRATION_MAY_DIFFER_FROM_ACTUAL',balance_notice='CONTENT_SUBJECT_TO_FUTURE_BALANCE_CHANGE'),
        actual_unacquired_image_ref='image/20081111_ev_02.gif')

def image_metadata(b,expected):
    require(b[:6] in (b'GIF87a',b'GIF89a') and len(b)>=13,'Not GIF')
    size=list(struct.unpack('<HH',b[6:10]));require(size==expected,'Image dimensions changed')
    return dict(format='GIF',dimensions=size,original_sprite_or_runtime_verified=False)

def validate(r):
    require(r['schema']=='stoneage.jp2008_pet_evolution.source.r1','Schema')
    require([x['replay_url'] for x in r['inputs']]==list(URLS),'Finite source set')
    require(r['authority']=='MEDIATED_DIGIPARK_RELEASE_PLUS_LATER_CAPTURED_OFFICIAL_HOST','Source authority changed')
    require(r['boundaries']==BOUNDARIES,'Unknown boundary promoted')
    require(len(r['records'])==15,'Fifteen documentary contracts required')
    required={'record_id','entity_type','version_profile','source_refs','verification_status','rights_status','record_revision'}
    for x in r['records']:
        require(required<=x.keys() and x['game_ids'] is None,'Archive fields/IDs')
        require(x['verification_status']=='SOURCE_REPORTED_NOT_RUNTIME' and x['rights_status']=='RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED','Runtime/rights promotion')
    m,o=[x['extracted']['facts'] for x in r['inputs'][:2]]
    require([x['before_label'] for x in r['records'][:4]]==PETS and [x['evolved_mask'] for x in r['records'][:4]]==MASKS,'Pet label/mask changed')
    require(all(x['canonical_evolved_name'] is None and x['original_species_or_sprite_id'] is None for x in r['records'][:4]),'Masked name/ID invented')
    require(r['records'][4]['location']==common_location() and r['records'][4]['coordinates'] is None and r['records'][4]['appearance'] is None,'NPC locator/appearance invented')
    require(r['records'][4]['quest_id'] is None and all(x['element_growth_or_riding'] is None for x in r['records'][:4]),'NPC quest/species rules invented')
    require(r['records'][5]['flow']==m['flow'] and r['records'][5]['one_pet_per_attempt']==1 and r['records'][5]['exact_prerequisites'] is None,'Trial conditions invented')
    require(r['records'][5]['quest_steps_or_battle_encounters'] is None and r['records'][5]['random_roll_timing'] is None,'Trial steps/roll trigger invented')
    require(r['records'][6]['status_formula'] is None and r['records'][6]['mutation_probability'] is None and r['records'][6]['successful_result_level'] is None,'Success formula invented')
    require(r['records'][7]['facts']==o['failure'],'Failure detached')
    require(r['records'][7]['failure_species_or_identity_change'] is None,'Failure pet identity invented')
    require(r['records'][8]['scope']=='ITEM_GUARANTEE_NOT_ORDINARY_QUEST_RATE' and r['records'][8]['use_timing_or_consumption'] is None,'Paid guarantee merged with base rate')
    require(r['records'][9]['rerolls_reported']==1 and r['records'][9]['reroll_distribution'] is None,'Reroll frequency invented')
    require(r['records'][10]['facts']==m['campaign'],'Bundle/campaign detached')
    require(r['records'][10]['purchase_or_transaction_executed'] is False and r['records'][10]['ordinary_quest_fee'] is None,'Transaction/quest fee invented')
    require(r['records'][11]['transfer_ratio_or_duplication'] is None,'Experience transfer invented')
    require(r['records'][11]['exact_activation_or_duration'] is None,'Experience gift duration invented')
    require(all(x['same_time_historical_pixels'] is False and x['runtime_or_sprite_binding'] is None for x in r['records'][12:14]),'Image promoted to original runtime')
    require(r['records'][13]['manual_observation']['named_species_or_mutation_join'] is None,'Concept image bound to named species/mutation')
    require(r['records'][14]['same_source_chain_not_independent_runtime_witnesses'] is True and r['records'][14]['cross_region_rebirth_fusion_equivalence'] is None,'Cross-source/region conflation')
    require(r['next']=='OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-32','Return portfolio')

def replay(r,payloads):
    validate(r);require(len(payloads)==5,'Exactly two HTML and three current GIF references')
    got=[extract_media(payloads[0]),extract_official(payloads[1])]+[image_metadata(b,s) for b,s in zip(payloads[2:],[[400,75],[97,96],[135,115]])]
    for i,(s,b,x) in enumerate(zip(r['inputs'],payloads,got)):
        if i>0:require(len(b)==s['http']['bytes'] and sha256(b).hexdigest()==s['http']['sha256'],'Historical/image source byte pin changed')
        require(x==s['extracted'],'Release/page semantics changed')
    return dict(schema='stoneage.jp2008_pet_evolution.replay.r1',inputs=[dict(source_id=s['id'],bytes=len(b),sha256=sha256(b).hexdigest()) for s,b in zip(r['inputs'],payloads)],extracted=got,
        official_page_capture='20090217151837',media_2008_snapshot_obtained=False,original_server_executed=False,
        unresolved_names_preserved=True,ordinary_chance_not_paid_guarantee=True,raw_sources_in_output=False)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--fetch',action='store_true');p.add_argument('--source-dir',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();require(a.fetch!=bool(a.source_dir),'Fetch or transient directory');payloads=[]
    for u,n in zip(URLS,NAMES):
        if a.fetch:
            with urllib.request.urlopen(u,timeout=45) as response:
                require(response.status==200 and response.url==u,'Unexpected HTTP/redirect');b=response.read(2_000_001);require(len(b)<=2_000_000,'Oversized source')
        else:b=(a.source_dir/n).read_bytes()
        payloads.append(b)
    result=replay(json.loads(REPORT.read_text()),payloads);a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('HTML_VERIFIED=2 GIF_REFERENCE_VERIFIED=3 ELIGIBLE_PET_SOURCE_LABELS=4 MASKED_EVOLVED_NAMES=4 ORIGINAL_SERVER_EXECUTIONS=0')

if __name__=='__main__':main()

