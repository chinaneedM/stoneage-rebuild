"""Finite CN2.0 creation/status documentary contract, not a character-stat engine."""
import argparse
from hashlib import sha256,sha1
import json
from pathlib import Path
import re
import struct
import urllib.request
from tools.stoneage_jp2008_shadow_release import compact,require
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'research/recovered/STONEAGE-CN20-CREATION-STATUS-SOURCE-R1.json'
URLS=(
'https://web.archive.org/web/20011204194619id_/http://www.waei.com.cn/ZHUANQU/stoneage2/pet/new_pet.asp',
'https://web.archive.org/web/20011201045054id_/http://www.waei.com.cn/ZHUANQU/stoneage2/tyro/creature.asp',
'https://web.archive.org/web/20011221174011id_/http://waei.com.cn/ZHUANQU/stoneage2/tyro/img/3.gif')
NAMES=('nav.html','creation.html','creation-reference.gif')
MAPPING=[['体力','耐久力'],['腕力','攻击力'],['耐力','防御力'],['速度','敏捷力']]
EFFECTS=[
 dict(primary='体力',source_delta=1,reported_effects={'耐久力（HP）':3},unmentioned_effects=None),
 dict(primary='腕力',source_delta=1,reported_effects={'耐久力（HP）':1,'攻击力':1},unmentioned_effects=None),
 dict(primary='耐力',source_delta=1,reported_effects={'耐久力（HP）':1,'防御力':1},unmentioned_effects=None),
 dict(primary='速度',source_delta=1,reported_effects={'耐久力（HP）':1,'敏捷力':1},unmentioned_effects=None)]
BOUNDARIES=dict(operator_authorship_verified=False,original_client_or_server_execution_verified=False,exact_client_build=None,
 original_publication_date=None,cn_initial_stat_points=None,cn_initial_element_points=None,character_type_or_color_counts=None,
 wire_create13_field_join=None,name_limit_bytes_or_unicode_units=None,automatic_levelup_increase_amount=None,
 unmentioned_stat_effects_are_zero=False,reported_deltas_are_verified_full_stat_formula=False,attack_speed_means_extra_attacks=False,
 exact_element_allowed_pair_list=None,element_damage_multiplier=None,starting_village_names_ids_or_starter_species=None,
 build_nicknames_are_classes=False,image_is_creation_or_status_screen=False,image_same_build_as_body=False,
 image_english_labels_authenticate_region_or_language=False,
 source_typo_silently_corrected=False,jss20_creation_or10_element_points_transferred_to_cn=False,
 repeated_three_point_clauses_mean_six_points=False,tw10_or_jss1999_backfill=False,raw_sources_committed=False,
 stage_a='7_PARTIAL_2_OPEN',stage_b_and_wiki='GATED',r79='PAUSED_NON_BLOCKING')
DERIVED_PATHS=('research/recovered/JSS-LOGIN-MANUAL-CREATION-CONTRACT-R1.json','research/recovered/STONEAGE-WAEI-CN20-NEWCOMER-GUIDE-R1.json')

def extract_nav(b):
    from tools.stoneage_cn20_riding_source import Links
    h=b.decode('gb18030');p=Links();p.feed(h);a=[dict(label=t,href=u) for t,u in p.links if t=='人物创造']
    require(a==[dict(label='人物创造',href='/ZHUANQU/stoneage2/tyro/creature.asp')],'Named actual route changed')
    return a[0]

def extract_body(b):
    h=b.decode('gb18030');t=compact(h)
    require('<title>石器时代2.0</title>' in h,'Edition label absent')
    require(t.count('北京华义联合软件开发有限公司')==1,'Operator footer ambiguous')
    require(t.count('一、人物创建')==1 and t.count('二、状态与属性')==1,'Article sections missing/ambiguous')
    core=t.split('人物创建',1)[1].split('北京华义联合软件开发有限公司')[0]
    for clause in ['最多可以输入全角8个字符','用"<"">"键选择各个脸部的表情','体力（影响任务的HP）',
                   '腕力（影响人物的攻击力）','耐力（影响人物的防御力）','速度（影响人物的攻击速度）',
                   '对应游戏的状态窗口中，分别是耐久力、攻击力、防御力、敏捷力',
                   '升等后的人物体力值会增加','另外还会有三点分配能力值','可以获得三点能力分配点数',
                   '属性值没有办法一次选择3种以上的属性','分配到的属性，与其相反的属性就不能再选择了',
                   '只能选择两种相邻的属性','地克水、水克火、火克风、风克地',
                   '四个可供选择的出生地，北岛、南岛各两个','每个出生地降生时所拥有的原始宠物各不相同',
                   '点击"决定"键后，选好出生村落的名称','「血人」','「攻人」','「防人」','「敏人」']:
        require(clause in core,'Material creation/status clause missing: '+clause)
    effects=[]
    for primary,expected in zip(['体力','腕力','耐力','速度'],EFFECTS):
        match=re.search(primary+r'\+1点--(.*?)(?=(?:体力|腕力|耐力|速度)\+1点--|2\.属性分为)',core)
        require(match is not None,'Missing exact stat clause')
        values=dict((key,int(n)) for key,n in re.findall(r'(耐久力（HP）|攻击力|防御力|敏捷力)\+(\d+)点',match[1]))
        require(values==expected['reported_effects'],'Source marginal delta changed')
        effects.append(dict(primary=primary,source_delta=1,reported_effects=values,unmentioned_effects=None))
    require(core.count('地克水、水克火、火克风、风克地')==2,'Element cycle repetitions changed')
    require('href="img/3.gif"' in h and 'src="img/3s.gif"' in h,'Actual linked illustration missing')
    return dict(core_utf8_bytes=len(core.encode()),core_sha256=sha256(core.encode()).hexdigest(),
        facts=dict(name=dict(maximum_fullwidth_characters_as_written=8,engine_counting_units=None),face='ANGLE_CONTROLS_SELECT_EXPRESSIONS_NOT_CHARACTER_CENSUS',
        primary_status_mapping=MAPPING,first_hp_wording_as_written='体力（影响任务的HP）',primary_effects=effects,
        levelup=dict(distributable_points=3,same_claim_occurrences=2,automatic_increase_source_term='体力值',automatic_increase_amount=None,initial_pool=None),
        element=dict(names_in_creation_order=['地','水','火','风'],maximum_types=2,second_type='ADJACENT_ONLY_SOURCE_TERM',opposite='CANNOT_SELECT_OPPOSITE_SOURCE_TERM',
        cycle=[['地','水'],['水','火'],['火','风'],['风','地']],initial_pool=None,exact_damage_formula=None),
        birth=dict(total=4,north_island=2,south_island=2,selection_after='决定',different_starter_pet_by_birthplace_source_claim=True,village_names=None,starter_species=None),
        labels=['血人','攻人','防人','敏人'],labels_are='RELATIVE_HIGH_STATUS_NICKNAMES_NOT_CLASSES_OR_THRESHOLDS',
        creation_flow=['NAME','FACE_EXPRESSION','ALLOCATE_PRIMARY_POINTS','ALLOCATE_ELEMENT_POINTS','DECIDE','CHOOSE_BIRTHPLACE','CONFIRM_START']),
        image_ref=dict(full='img/3.gif',thumbnail='img/3s.gif',declared_inline_size=[240,180]))

def image_metadata(b):
    require(b[:6] in (b'GIF87a',b'GIF89a') and len(b)>=13,'Not GIF')
    w,h=struct.unpack('<HH',b[6:10]);require((w,h)==(640,480),'Image dimensions changed')
    return dict(format='GIF',width=w,height=h,manual_observation='OUTDOOR_HUMAN_AND_BLUE_CREATURE_NO_CREATION_OR_STATUS_PANEL',visible_labels=['MENU','Mail','Action','Eng'],original_character_or_pet_identity=None)

def derived_comparison(r):
    pins=r['derived_inputs'];require([s['path'] for s in pins]==list(DERIVED_PATHS),'Finite derived inputs changed')
    inputs=[]
    for s in pins:
        b=(ROOT/s['path']).read_bytes();require(len(b)==s['bytes'] and sha256(b).hexdigest()==s['sha256'] and sha1(b'blob '+str(len(b)).encode()+bytes([0])+b).hexdigest()==s['git_blob'],'Derived source pin changed');inputs.append(json.loads(b))
    jss=inputs[0]['pages']['manual01']['creation_contract']
    require(jss['initial_stat_allocation_points']==20 and jss['initial_element_allocation_points']==10,'Japanese creation scope changed')
    advice=inputs[1]['records'][4]['source_described_claims']
    require(advice['creation_points_recommended_to_endurance']==20 and advice['mandatory_creation_allocation_or_only_attack_source'] is False,'Mainland advice converted to mandatory allocation')
    return dict(jss_initial_stat_points=20,jss_initial_element_points=10,cn_body_initial_stat_points=None,cn_body_initial_element_points=None,
        cn_body_levelup_points=3,relation='DISTINCT_REGIONAL_DOCUMENTARY_SCOPES_NO_VALUE_TRANSFER',
        cn_newcomer_20_endurance='BUILD_ADVICE_NOT_COMPULSORY_CREATION_POOL_IN_THIS_BODY',
        shared_wire_fields_original_build_or_patch_sequence_verified=False)

def validate(r):
    require(r['schema']=='stoneage.cn20_creation_status.source.r1','Schema')
    require([s['replay_url'] for s in r['inputs']]==list(URLS),'Fixed source set changed')
    require(r['authority']=='OPERATOR_HOSTED_UNSIGNED_GUIDE_AUTHOR_UNVERIFIED','Hosting promoted to authorship')
    require(r['boundaries']==BOUNDARIES,'Unknown boundary promoted')
    require(len(r['records'])==12,'Twelve documentary records, not twelve character types')
    required={'record_id','entity_type','version_profile','source_refs','verification_status','rights_status','record_revision'}
    for row in r['records']:
        require(required<=row.keys() and row['game_ids'] is None,'Archive fields/IDs')
        require(row['verification_status']=='SOURCE_REPORTED_NOT_RUNTIME' and row['rights_status']=='RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED','Runtime/rights promotion')
    f=r['inputs'][1]['extracted']['facts']
    require(r['records'][0]['name']==f['name'] and r['records'][0]['flow']==f['creation_flow'] and r['records'][0]['character_types'] is None,'Creation choices changed')
    require(r['records'][0]['face']==f['face'] and r['records'][0]['colors'] is None and r['records'][0]['layout_coordinates'] is None,'Appearance count/layout invented')
    require(r['records'][1]['mapping']==MAPPING and r['records'][1]['first_hp_wording_as_written']=='体力（影响任务的HP）','Primary mapping/source typo changed')
    require(r['records'][2]['facts']==f['levelup'] and f['levelup']['distributable_points']==3 and f['levelup']['initial_pool'] is None,'Level-up/initial points conflated')
    require(r['records'][1]['wire_fields'] is None and r['records'][2]['initial_stat_points'] is None and r['records'][2]['exact_exp_thresholds'] is None,'Wire/initial/EXP values invented')
    require([x['facts'] for x in r['records'][3:7]]==EFFECTS,'Reported marginal effects changed or omitted effects set to zero')
    require(all(x['base_stats'] is None and x['rounding_or_caps'] is None for x in r['records'][3:7]),'Marginal effect promoted to complete formula')
    require(r['records'][7]['facts']==f['element'] and f['element']['initial_pool'] is None,'Element facts detached')
    require(r['records'][8]['facts']==f['birth'] and f['birth']['village_names'] is None and f['birth']['starter_species'] is None,'Birthplace names/pets invented')
    require(r['records'][7]['allowed_pair_engine_predicate'] is None and r['records'][8]['original_location_ids'] is None and r['records'][8]['pet_species_ids'] is None,'Element predicate/birthplace IDs invented')
    require(r['records'][9]['labels']==f['labels'] and r['records'][9]['class_ids_or_thresholds'] is None,'Nicknames turned into classes')
    require(r['records'][10]['same_build_as_body'] is False and r['records'][10]['creation_ui_verified'] is False,'Image promoted to creation UI')
    require(r['records'][9]['mandatory_build'] is None and r['records'][10]['character_or_pet_ids'] is None,'Class/image identity invented')
    require(r['records'][11]['facts']==derived_comparison(r),'Cross-source values detached')
    require(r['next']=='OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-31','Portfolio return required')

def replay(r,payloads):
    validate(r);require(len(payloads)==3,'Exactly two HTML and one GIF required')
    got=[fn(b) for fn,b in zip((extract_nav,extract_body,image_metadata),payloads)]
    for s,b,x in zip(r['inputs'],payloads,got):
        require(len(b)==s['http']['bytes'] and sha256(b).hexdigest()==s['http']['sha256'],'Exact historical source byte pin changed')
        require(x==s['extracted'],'Derived extraction changed')
    return dict(schema='stoneage.cn20_creation_status.replay.r1',inputs=[dict(source_id=s['id'],bytes=len(b),sha256=sha256(b).hexdigest(),capture_timestamp=s['capture_timestamp']) for s,b in zip(r['inputs'],payloads)],extracted=got,derived_source_comparison=derived_comparison(r),raw_sources_in_output=False,operator_authorship_verified=False,original_client_or_server_executed=False,image_creation_ui_or_same_build_verified=False)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--fetch',action='store_true');p.add_argument('--source-dir',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();require(a.fetch!=bool(a.source_dir),'Fetch or transient files required');payloads=[]
    for u,n in zip(URLS,NAMES):
        if a.fetch:
            with urllib.request.urlopen(u,timeout=45) as response:
                require(response.status==200 and response.url==u,'Unexpected HTTP/redirect');b=response.read(2_000_001);require(len(b)<=2_000_000,'Oversized source')
        else:b=(a.source_dir/n).read_bytes()
        payloads.append(b)
    result=replay(json.loads(REPORT.read_text()),payloads);a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('HTML_VERIFIED=2 GIF_REFERENCE_VERIFIED=1 PRIMARY_STAT_SOURCE_ROWS=4 CN_LEVELUP_POINTS_REPORTED=3 ORIGINAL_CLIENT_SERVER_EXECUTIONS=0')

if __name__=='__main__':main()

