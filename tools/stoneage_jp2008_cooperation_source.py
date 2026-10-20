"""Replay a bounded Japanese cooperative-event release and inspected reward tables.

No game server is executed. Current source bytes are not historical captures.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import struct
import urllib.request
from tools.stoneage_jp2008_shadow_release import compact, require

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'research/recovered/STONEAGE-JP2008-COOPERATION-SOURCE-R1.json'
MEDIA = 'https://www.4gamer.net/games/013/G001377/20080620060/'
OFFICIAL = 'http://stoneage.to/event/2008/080624_event_Cooperation.html'
NAMES = ('M1.html', '008.jpg', '012.jpg', '010.jpg', '009.jpg', '011.jpg')
URLS = (MEDIA,) + tuple(MEDIA+'TN/'+n for n in NAMES[1:])
SIZES = ([250,200], [433,167], [434,49], [434,49], [434,49])
BOUNDARIES = dict(exact_client_build=None, original_game_ids=None, original_server_execution_verified=False,
 historical_2008_html_or_image_bytes_obtained=False, official_page_obtained=False,
 global_archive_absence_proven=False, drop_species_or_probability=None, exchange_ratio=None,
 per_player_requirement=None, population_or_server_counter_scope=None, reward_actual_unlock_verified=False,
 reward_thresholds_are_costs=False, reward_end_is_event_end=False, reported_permanent_is_verified_current_service=False,
 npc_map_coordinates=None, carpenter_three_times_is_player_stat_multiplier=False,
 save_point_is_client_local_save_proof=False, pet_reroll_distribution=None,
 same_named_earlier_world_entity_verified=False, tiger_quest_recovered=False,
 raw_sources_committed=False, stage_a='7_PARTIAL_2_OPEN', stage_b_and_wiki='GATED', r79='PAUSED_NON_BLOCKING')

def facts():
    return dict(published_label='2008/06/20 22:28', authority='MEDIA_MARKED_RELEASE_QUOTATION_WITH_EDITORIAL_DIGIPARK_ATTRIBUTION',
      collection_period=dict(start='2008-06-24 16:00',end='2008-07-15 13:00',timezone=None),
      items=['精霊の雫','精霊の恵み'],
      tree_flow=['ENEMY_DINOSAUR_DROPS_DEW','EXCHANGE_DEW_WITH_BLESSING_SPIRIT','GIVE_BLESSING_TO_TREE'],
      other_flow=['ENEMY_DINOSAUR_DROPS_DEW','DISTRIBUTE_DEW_TO_LOCAL_RECIPIENTS'],
      roles=[dict(label='恵みの精霊',role='DEW_TO_BLESSING_EXCHANGE',place_as_written='マンモスルーム'),
        dict(label='ザハン一族の族長',role='SEEKS_RECOVERY_OF_SACRED_WATER',place_as_written='アーブの泉'),
        dict(label='クルクの大工',role='RECEIVES_DEW_FOR_SHOP_RENOVATION',place_as_written='クルクのコンビニ'),
        dict(label='転送員',role='RECEIVES_DEW_AFTER_HEAT_COLLAPSE',place_as_written='チャットルーム')],
      tree_location_variant='マンモスホール',tree_location_labels_equivalence_verified=False,
      tree_story='OVERUSED_NATURAL_POWER_AND_LACK_OF_DEW',
      local_stories=['WEAKENED_SACRED_WATER_AND_CLAN_UNABLE_TO_LEAVE_SPRING','ONE_CARPENTER_CAN_WORK_THREE_TIMES_AS_HARD_AFTER_DEW','SHOP_STAFF_WANTS_TRAVEL_BUT_TRANSPORT_WORKER_COLLAPSED'],
      thresholds_are_reported_delivery_totals_not_individual_fees=True)

def rewards():
    rows=[('TREE',2000,'精霊の恵み','キヌイの村にセーブポイントを設置','PERMANENT_FROM_2008-07-22','I2'),
      ('TREE',5000,'精霊の恵み','出張預かり屋NPCの設置','PERMANENT_FROM_2008-07-22','I2'),
      ('TREE',8000,'精霊の恵み','ペット技をゲーム内で追加販売','PERMANENT_FROM_2008-07-22','I2'),
      ('TREE',30000,'精霊の恵み','経験値獲得イベント','2008-07-22_TO_2008-08-12','I2'),
      ('TREE',35000,'精霊の恵み','ペット再抽選NPCの設置','2008-07-22_TO_2008-08-12','I2'),
      ('WATER',3000,'精霊の雫','アーブの水の復活','2008-07-22_TO_2008-08-12','I3'),
      ('SHOP',3000,'精霊の雫','クルクの村のコンビニ開店','PERMANENT_FROM_2008-07-22','I4'),
      ('TRANSPORT',10000,'精霊の雫','転送NPCの設置','2008-07-22_TO_2008-08-12','I5')]
    return [dict(branch=a,delivery_total=b,delivered_item=c,reward_label=d,reported_availability=e,source_ref=f,
      actual_unlock_verified=False,individual_cost=None,exact_effect_or_stock=None) for a,b,c,d,e,f in rows]

def records():
    rows=[]
    def add(kind,collection,data,refs):
        rows.append(dict(record_id=f'JP2008-COOP-{len(rows)+1:02}',entity_type=kind,collection=collection,
          version_profile='LATER_OFFICIAL:JP_DIGIPARK_2008_COOPERATION',source_refs=refs,
          verification_status='SOURCE_REPORTED_NOT_RUNTIME',rights_status='RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED',
          record_revision=1,game_ids=None,source_reported=data))
    f=facts()
    for i,n in enumerate(f['items']):add('EVENT_ITEM','items',dict(label=n,drop_or_exchange='ENEMY_DROP' if i==0 else 'EXCHANGE_FROM_DEW',ratio=None,drop_rate=None),['M1'])
    for x in f['roles']:add('NPC_ROLE','npcs',dict(**x,coordinates=None,appearance=None),['M1'])
    for label,flow in [('TREE',f['tree_flow']),('LOCAL_AID',f['other_flow'])]:add('COOPERATIVE_EVENT','quests',dict(label=label,flow=flow,period=f['collection_period'],counter_scope=None,completion_verified=False),['M1'])
    for x in rewards():add('CONDITIONAL_PUBLIC_REWARD','items',x,[x['source_ref']])
    add('TREE_VISUAL_REFERENCE','screens',dict(observation='GREEN_TREE_CANOPY_WITH_FOREST_FLOOR',named_by_adjacent_caption='神秘の大樹',runtime_or_sprite_id=None,historical_pixels=False),['M1','I1'])
    return rows

def extract(b):
    h=b.decode('utf-8-sig'); marker='以下，リリースより'
    require(h.count(marker)==1,'Release quotation attribution missing/ambiguous')
    quoted=h.split(marker,1)[1];require('<span class="blockquote">' in quoted,'Release container missing')
    quoted=quoted.split('<span class="blockquote">',1)[1].split('</span>',1)[0]
    require(compact(quoted).count('初夏の二大協力イベント')==1,'Cooperation section missing/ambiguous')
    section=quoted.split('初夏の二大協力イベント',1)[1];core=compact(section)
    require('href="'+OFFICIAL+'"' in section,'Actual official event outbound missing')
    require('2008/06/2022:28' in compact(h) and 'デジパークは' in compact(h),'Publication/editorial attribution missing')
    for clause in ['2008年6月24日（火）16：00〜2008年7月15日（火）13：00',
      '敵恐竜が落とすイベントアイテム「精霊の雫」','マンモスルームにいる「恵みの精霊」に「精霊の恵み」と交換',
      '「神秘の大樹」に与えよう','マンモスホール','「ザハン一族の族長」','アーブの泉から離れる事ができません',
      '「クルクの大工」','普通の人の3倍','週休たったの3.5時間','チャットルームでパタリっ','「転送員」']:
        require(clause in core,'Material clause missing: '+clause)
    refs=re.findall(r'src="(/games/013/G001377/20080620060/TN/\d+\.jpg)"',section)
    require(refs==['/games/013/G001377/20080620060/TN/'+x+'.jpg' for x in ['008','012','005','006','007','010','009','011']],'Event image sequence changed')
    return dict(core_sha256=sha256(core.encode()).hexdigest(),core_utf8_bytes=len(core.encode()),facts=facts(),image_refs=refs)

def jpeg_size(b):
    require(b[:2]==b'\xff\xd8' and b[-2:]==b'\xff\xd9','Not a complete JPEG envelope')
    p=2
    while p<len(b):
        require(b[p]==255,'Malformed JPEG marker');p+=1
        while b[p]==255:p+=1
        marker=b[p];p+=1
        if marker in (0xD8,0xD9):continue
        length=struct.unpack('>H',b[p:p+2])[0];require(length>=2 and p+length<=len(b),'Truncated JPEG segment')
        if marker in (0xC0,0xC1,0xC2):
            height,width=struct.unpack('>HH',b[p+3:p+7]);return [width,height]
        p+=length
    raise ValueError('JPEG frame dimensions absent')

def validate(r):
    require(r['schema']=='stoneage.jp2008_cooperation.source.r1','Schema')
    require([x['url'] for x in r['inputs']]==list(URLS),'Bounded six source inputs')
    require(r['boundaries']==BOUNDARIES,'Unknown or regional boundary promoted')
    require(r['records']==records(),'Archive contract/reward/NPC/period drift')
    require(r['inputs'][0]['extracted']['facts']==facts(),'Release facts drift')
    require(r['manual_reward_transcription']==rewards(),'Reward image transcription drift')
    require(r['official_acquisition']['http_status']==429 and not r['official_acquisition']['page_obtained'],'Acquisition failure scope drift')
    require(r['next']=='OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-33','Return whole portfolio')

def replay(r,payloads):
    validate(r);require(len(payloads)==6,'One HTML, one scene, four reward tables required')
    e=extract(payloads[0]);require(e==r['inputs'][0]['extracted'],'Event release core/semantics changed')
    for s,b,size in zip(r['inputs'][1:],payloads[1:],SIZES):
        require(len(b)==s['bytes'] and sha256(b).hexdigest()==s['sha256'],'Inspected image bytes changed')
        require(jpeg_size(b)==size==s['dimensions'],'JPEG dimensions changed')
    return dict(schema='stoneage.jp2008_cooperation.replay.r1',inputs=[dict(id=s['id'],bytes=len(b),sha256=sha256(b).hexdigest()) for s,b in zip(r['inputs'],payloads)],
      extracted=e,manual_reward_transcription=rewards(),image_dimensions=[jpeg_size(b) for b in payloads[1:]],
      manual_transcription_independently_machine_read=False,original_server_executed=False,actual_rewards_unlocked=False,raw_sources_in_output=False)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--fetch',action='store_true');p.add_argument('--source-dir',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    require(a.fetch!=bool(a.source_dir),'Choose live fetch or transient input directory');payloads=[]
    for u,n in zip(URLS,NAMES):
        if a.fetch:
            with urllib.request.urlopen(u,timeout=45) as response:
                require(response.status==200 and response.url==u,'Unexpected HTTP/redirect');b=response.read(2_000_001);require(len(b)<=2_000_000,'Oversized source')
        else:b=(a.source_dir/n).read_bytes()
        payloads.append(b)
    out=replay(json.loads(REPORT.read_text()),payloads);a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print('HTML_VERIFIED=1 JPEG_VERIFIED=5 REWARD_ROWS=8 NPC_ROLES=4 ORIGINAL_SERVER_EXECUTIONS=0')

if __name__=='__main__':main()
