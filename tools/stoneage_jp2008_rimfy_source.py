"""Replay a media-labelled release and one actual linked pet JPEG; no historical-byte claim."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import urllib.request

from tools.stoneage_jp2008_shadow_release import compact,require
from tools.stoneage_cn2003_christmas_source import jpeg_dimensions

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'research/recovered/STONEAGE-JP2008-RIMFY-FAMILY-QUEST-SOURCE-R1.json'
URLS=('https://www.4gamer.net/games/013/G001377/20080707020/',
      'https://www.4gamer.net/games/013/G001377/20080707020/TN/001.jpg')
OFFICIAL_LINK='http://stoneage.to/update/20080708_update_rimfy_quest.html'


def extract(payload):
    html=payload.decode('utf-8-sig');text=compact(html);marker='以下，リリースより'
    require(text.count(marker)==1,'Missing/ambiguous quoted-release boundary')
    release=text.split(marker)[1]
    start,end='新クエストアップデート','クエストをクリアすると新ペット「リムフィ」が手に入ります。'
    require(release.count(start)==release.count(end)==1,'Ambiguous quest body')
    core=release[release.index(start):release.index(end)+len(end)]
    require(OFFICIAL_LINK in core,'Actual operator link missing from quoted body')
    roles=re.search(r'親犬「([^」]+)」と子犬「([^」]+)」',core)
    date=re.search(r'■実施日：(\d+年\d+月\d+日（[^）]+）\d+：\d+)',core)
    add=re.search(r'既存ダンジョン「([^」]+)」に、新ペット「([^」]+)」が手に入るクエスト「([^」]+)」の追加',core)
    protector=re.search(r'１人の男「([^」]+)」の手によって保護された',core)
    require(all((roles,date,add,protector)),'Named family/setting/protector/date missing')
    require(add[2]==roles[2],'Puppy label differs from reported reward label')
    require('ダンジョン「'+add[1]+'」にいる「'+roles[2]+'」を連れて、はぐれてしまった親犬を探してあげよう！' in core,'Companion/search objective missing')
    for clause in ('赤く炎の様な毛並み','ろくに食事も取らず探し回り','洞窟の奥深くへと入っていく','忍び寄る怪しい影','果たして、無事に親子は再会できるのか？！'):
        require(clause in core,'Narrative clause missing: '+clause)
    return dict(core_sha256=sha256(core.encode()).hexdigest(),core_utf8_bytes=len(core.encode()),facts=dict(
        announced_start_as_written=date[1],dungeon_as_written=add[1],quest_as_written=add[3],
        parent_dog_as_written=roles[1],puppy_as_written=roles[2],protector_as_written=protector[1],
        protector_role='PROTECTS_LOST_PUPPY_NOT_PROVEN_QUEST_START',
        puppy_fur_description='RED_FLAME_LIKE_NOT_ELEMENT_STATS',parent_searches_deeper_cave_reported=True,
        parent_lacks_food_narrative_not_hunger_rule=True,objective='TAKE_PUPPY_AND_SEARCH_FOR_PARENT',
        completion_reward_pet_label=roles[2],mysterious_shadow_identity=None,reunion_ending_details=None))


def validate(r):
    require(r['schema']=='stoneage.jp2008_rimfy_family_quest.source.r1','Unknown schema')
    require([s['http']['url'] for s in r['inputs']]==list(URLS),'Finite source list changed')
    require(r['inputs'][0]['authority']=='MEDIA_LABELLED_RELEASE_WITH_OPERATOR_LINK_ISSUER_NOT_NAMED_IN_QUOTE','Source promoted to named operator author')
    require(all(s['historical_original_sha256'] is None for s in r['inputs']),'Current bytes promoted to historical bytes')
    require(len(r['records'])==6,'Six source records required')
    required={'record_id','entity_type','version_profile','source_refs','verification_status','rights_status','record_revision'}
    for row in r['records']:
        require(required<=row.keys() and row['game_ids'] is None,'Original IDs/contract changed')
        require(row['rights_status']=='RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED','Rights promotion')
        require(row['verification_status'] in ('MEDIA_RELEASE_REPORTED_NOT_RUNTIME','MANUAL_IMAGE_REFERENCE_NOT_SPECIES_MASTER'),'Runtime promotion')
    q,parent,puppy,npc,dungeon,screen=r['records']
    require(q['source_facts']==r['inputs'][0]['extracted']['facts'],'Quest detached from source')
    require(q['minimum_level'] is None and q['escort_implementation'] is None and q['ending_details'] is None,'Level/escort/ending invented')
    require(parent['gender'] is None and parent['capture_rule'] is None,'Parent gender/capture invented')
    require(puppy['numeric_elements'] is None and puppy['growth_rates'] is None and puppy['escorted_individual_equals_reward_individual'] is None,'Fur colour or label promoted to original data')
    require(npc['quest_start_verified'] is False and npc['spawn_coordinates'] is None,'Protector promoted to starting NPC/spawn')
    require(dungeon['map_ids'] is None and screen['original_sprite_binding'] is None,'Original map/sprite invented')
    require(r['boundaries']==dict(original_operator_html_recovered=False,historical_media_or_image_bytes_verified=False,
        original_server_execution_verified=False,exact_client_build=None,publication_label_proves_actual_deployment=False,
        image_is_original_client_sprite_master=False,red_flame_fur_proves_fire_attribute=False,
        parent_role_proves_mother_or_father=False,mysterious_shadow_is_named_boss=False,
        raw_html_or_assets_committed=False,tw10_or_jss1999_backfill=False,
        stage_a='7_PARTIAL_2_OPEN',stage_b_and_wiki='GATED',r79='PAUSED_NON_BLOCKING'),'Boundary changed')
    require(r['next']=='OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-27','Portfolio return required')


def replay(r,payloads):
    validate(r);require(len(payloads)==2,'Exactly one current HTML and one linked JPEG required')
    got=extract(payloads[0]);require(got==r['inputs'][0]['extracted'],'Quoted quest core/facts changed')
    require('/games/013/G001377/20080707020/TN/001.jpg' in payloads[0].decode(),'Actual image link missing')
    h=r['inputs'][1]['http'];require(len(payloads[1])==h['bytes'] and sha256(payloads[1]).hexdigest()==h['sha256'],'Pinned current image changed')
    require(jpeg_dimensions(payloads[1])==[122,99],'Actual pet image dimensions changed')
    return dict(schema='stoneage.jp2008_rimfy_family_quest.replay.r1',inputs=[dict(source_id=s['id'],bytes=len(b),sha256=sha256(b).hexdigest()) for s,b in zip(r['inputs'],payloads)],quest=got,image_dimensions=[122,99],historical_source_or_original_server_verified=False,raw_html_or_image_in_output=False)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--fetch',action='store_true');p.add_argument('--source-dir',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    require(a.fetch!=bool(a.source_dir),'Choose fixed fetch or transient supplied files');payloads=[]
    for u,n in zip(URLS,('rimfy.html','rimfy-reference.jpg')):
        if a.fetch:
            with urllib.request.urlopen(u,timeout=45) as response:
                require(response.status==200 and response.url==u,'Unexpected HTTP/redirect');b=response.read(2_000_001);require(len(b)<=2_000_000,'Oversized source')
        else:b=(a.source_dir/n).read_bytes()
        payloads.append(b)
    result=replay(json.loads(REPORT.read_text()),payloads);a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('MEDIA_LABELLED_RELEASE_VERIFIED=1 LINKED_PET_IMAGE_VERIFIED=1 HISTORICAL_HTMLS_VERIFIED=0 ORIGINAL_SERVER_EXECUTIONS=0')


if __name__=='__main__':main()
