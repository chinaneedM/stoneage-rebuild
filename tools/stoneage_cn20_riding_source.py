"""Replay two 2001 operator HTML pages and a separately dated 2002 linked JPEG.

This is a document contract, not a riding or combat implementation.
"""
import argparse
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import urllib.request

from tools.stoneage_jp2008_shadow_release import compact,require
from tools.stoneage_cn2003_christmas_source import jpeg_dimensions

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'research/recovered/STONEAGE-CN20-RIDING-TRAINER-COMBAT-SOURCE-R1.json'
URLS=(
 'https://web.archive.org/web/20011204194619id_/http://www.waei.com.cn/ZHUANQU/stoneage2/pet/new_pet.asp',
 'https://web.archive.org/web/20011204195948id_/http://www.waei.com.cn/ZHUANQU/stoneage2/pet/qdragon.asp',
 'https://web.archive.org/web/20020402014049id_/http://waei.com.cn/ZHUANQU/stoneage2/pet/img/ridepet/1.jpg')
NAMES=('nav.html','riding.html','riding-reference.jpg')


class Links(HTMLParser):
    def __init__(self):super().__init__();self.href=None;self.parts=[];self.links=[]
    def handle_starttag(self,t,a):
        if t=='a':self.href=dict(a).get('href');self.parts=[]
    def handle_data(self,d):
        if self.href:self.parts.append(d)
    def handle_endtag(self,t):
        if t=='a':
            if self.href:self.links.append((''.join(self.parts).strip(),self.href))
            self.href=None


def extract_nav(b):
    html=b.decode('gb18030');p=Links();p.feed(html)
    matches=[dict(label=label,href=href) for label,href in p.links if label=='骑乘宠物']
    require(matches==[dict(label='骑乘宠物',href='/ZHUANQU/stoneage2/pet/qdragon.asp')],'Actual named navigation changed')
    require('<title>石器时代2.0</title>' in html,'Operator page edition label missing')
    return matches[0]


def extract_body(b):
    html=b.decode('gb18030');text=compact(html)
    require('<title>石器时代2.0</title>' in html,'Edition label missing')
    require(text.count('原始人可以骑宠物！')==1,'Missing/ambiguous riding body')
    body=text.split('原始人可以骑宠物！')[1].split('北京华义联合软件开发有限公司')[0]
    for phrase in ('庄园内的族长家内有一位宠物骑师','查询自己适合骑乘的是哪两只','取得一只带在身上，并缴交学费',
        '骑宠课程分下级、中级与上级共三级','骑宠是训练「人」而不是训练宠物','换只非原来学骑宠用的恐龙是没关系的',
        '生命力为两者之和','受伤损血将等比例分配在人与宠的身上','防御力落在人与宠之间',
        '近程攻击为宠的攻击力','远程攻击为人的攻击力','近程攻击的发动为宠物的敏',
        '远程攻击的发动为人的敏','受攻击时则敏落在人与宠之间'):
        require(phrase in body,'Material source clause missing: '+phrase)
    loyalty=re.search(r'忠诚度也满(\d+)',body)
    require(loyalty and '在宠物栏中选择「骑乘」' in body,'Loyalty/command clause missing')
    require('img/ridepet/1.jpg' in html,'Actual article image reference missing')
    return dict(core_sha256=sha256(body.encode()).hexdigest(),core_utf8_bytes=len(body.encode()),facts=dict(
        trainer_role_as_written='宠物骑师',location='FOUR_MANOR_LEADERS_HOUSES_NEAR_FOUR_VILLAGES',
        eligible_groups_as_written=['雷龙','老虎'],compatible_pair_query=True,
        courses_as_written=['下级','中级','上级'],loyalty_label=int(loyalty[1]),
        command_as_written='骑乘',command_surface='宠物栏',training_target='HUMAN_NOT_PET',replacement_pet_retraining_not_required_reported=True,
        flow=['ASK_TRAINER_FOR_CHARACTER_COMPATIBILITY','OBTAIN_AND_CARRY_ELIGIBLE_PET','PAY_TUITION_AND_LEARN_MATCHING_COURSE','MEET_PET_LEVEL_AND_LOYALTY_CLAUSES','SELECT_RIDE_IN_PET_PANEL'],
        life_force='SUM_OF_HUMAN_AND_PET_SOURCE_TERM',damage_split='PROPORTIONAL_UNSPECIFIED_WEIGHTS',
        defense='BETWEEN_HUMAN_AND_PET_UNSPECIFIED_WEIGHTS',melee_attack='PET_ATTACK',ranged_attack='HUMAN_ATTACK',
        melee_initiation='PET_AGILITY',ranged_initiation='HUMAN_AGILITY',receiving_attack_agility='BETWEEN_HUMAN_AND_PET_UNSPECIFIED_WEIGHTS'))


def validate(r):
    require(r['schema']=='stoneage.cn20_riding_trainer_combat.source.r1','Wrong schema')
    require([s['replay_url'] for s in r['inputs']]==list(URLS),'Finite source set changed')
    require([s['capture_timestamp'] for s in r['inputs']]==['20011204194619','20011204195948','20020402014049'],'Mixed capture dates flattened')
    require(len(r['records'])==5,'Five source records required')
    required={'record_id','entity_type','version_profile','source_refs','verification_status','rights_status','record_revision'}
    for row in r['records']:
        require(required<=row.keys() and row['game_ids'] is None,'Archive contract/original ID changed')
        require(row['rights_status']=='RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED','Rights promotion')
        require(row['verification_status'] in ('OPERATOR_PAGE_REPORTED_NOT_RUNTIME','MANUAL_LATER_IMAGE_NOT_SAME_BUILD'),'Runtime promotion')
    npc,journey,training,combat,image=r['records']
    require(journey['facts']==r['inputs'][1]['extracted']['facts'],'Journey detached from source')
    require(npc['coordinates'] is None and npc['family_membership_requirement'] is None,'NPC location/access invented')
    require(training['tuition_amounts'] is None and training['course_level_ranges'] is None and training['character_species_map'] is None and training['simultaneously_learnable_mount_count'] is None,'Training amounts/compatibility invented')
    require(combat['damage_weights'] is None and combat['rounding'] is None and combat['defense_weights'] is None and combat['life_force_current_or_max'] is None and combat['element_formula'] is None,'Unsupported mounted combat formula invented')
    require(image['same_build_as_2001_text'] is False and image['original_sprite_binding'] is None,'Later image promoted to same-build original sprite')
    require(r['boundaries']==dict(original_operator_html_captures_verified=True,original_server_execution_verified=False,
        exact_client_build=None,image_and_text_same_capture=False,training_is_pet_skill_slot=False,
        trainer_access_means_family_membership_not_needed=False,compatible_pair_proves_two_simultaneous_mount_skills=False,
        proportional_damage_means_half_each=False,between_means_arithmetic_mean=False,
        source_life_force_proves_current_or_max_hp=False,tw10_or_jss1999_backfill=False,
        raw_html_or_assets_committed=False,stage_a='7_PARTIAL_2_OPEN',stage_b_and_wiki='GATED',r79='PAUSED_NON_BLOCKING'),'Boundary changed')
    require(r['next']=='OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-28','Portfolio return required')


def replay(r,payloads):
    validate(r);require(len(payloads)==3,'Exactly two historical HTML and one later JPEG required')
    for s,b in zip(r['inputs'],payloads):
        require(len(b)==s['http']['bytes'] and sha256(b).hexdigest()==s['http']['sha256'],'Historical bytes changed; substitution forbidden')
    require(extract_nav(payloads[0])==r['inputs'][0]['extracted'],'Named route changed')
    require(extract_body(payloads[1])==r['inputs'][1]['extracted'],'Riding rules changed')
    dims=jpeg_dimensions(payloads[2]);require(dims==r['inputs'][2]['dimensions'],'JPEG dimensions changed')
    return dict(schema='stoneage.cn20_riding_trainer_combat.replay.r1',inputs=[dict(source_id=s['id'],bytes=len(b),sha256=sha256(b).hexdigest()) for s,b in zip(r['inputs'],payloads)],navigation=extract_nav(payloads[0]),riding=extract_body(payloads[1]),image_dimensions=dims,image_capture_timestamp='20020402014049',same_build_or_original_server_verified=False,raw_html_or_images_in_output=False)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--fetch',action='store_true');p.add_argument('--source-dir',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();require(a.fetch!=bool(a.source_dir),'Choose fixed URLs or supplied transient files');payloads=[]
    for url,name in zip(URLS,NAMES):
        if a.fetch:
            with urllib.request.urlopen(url,timeout=45) as response:
                require(response.status==200 and response.url==url,'Unexpected HTTP/redirect');b=response.read(2_000_001);require(len(b)<=2_000_000,'Oversized source')
        else:b=(a.source_dir/name).read_bytes()
        payloads.append(b)
    result=replay(json.loads(REPORT.read_text()),payloads);a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('OPERATOR_2001_HTMLS_VERIFIED=2 LATER_2002_IMAGE_VERIFIED=1 SAME_BUILD_VERIFIED=0 ORIGINAL_SERVER_EXECUTIONS=0')


if __name__=='__main__':main()
