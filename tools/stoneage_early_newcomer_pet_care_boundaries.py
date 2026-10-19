"""Offline documentary comparison; no new original acquisition or rule merging."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
from tools.stoneage_early_content_probe import require

ROOT=Path('research/recovered')
INPUTS={
    'cn':('STONEAGE-WAEI-CN20-NEWCOMER-GUIDE-R1.json','aecc1e18d291d6af8e7fd6e4ca913baf9aedb6e883cabad295f47a842705bed6'),
    'creation':('JSS-LOGIN-MANUAL-CREATION-CONTRACT-R1.json','fb1bc22fbb6e42dfaf39f1ff928ab4278595b0eb3f61e98c33b50d1009690768'),
    'pet':('STONEAGE-JSS2001-PET-MANUAL-CONTRACT-R1.json','ec4c1602472fb5daa2d458e455f06df3318011e560be053abd460d7d5fba5a13'),
    'player':('STONEAGE-JSS2001-PLAYER-STATUS-LEVELUP-KNOCKOUT-R1.json','13df1d32a44127f80c3e042c335dc01d9cf926011f5b7908b1b71be77d818277'),
}
REPORT=ROOT/'STONEAGE-EARLY-NEWCOMER-PET-CARE-BOUNDARIES-R1.json'


def pointer(o,p):
    for k in p.strip('/').split('/'):
        o=o[int(k)] if isinstance(o,list) else o[k.replace('~1','/').replace('~0','~')]
    return o


def validate_report(o):
    require(len(o['records'])==8,'Eight finite source relations required')
    b=[r['bounded_comparison'] for r in o['records']]
    require(b[0]['cn_recommended_endurance_points']==20 and b[0]['jss_initial_stat_points']==20
            and b[0]['same_number_proves_mandatory_allocation_or_stat_identity'] is False,
            'Equal twenty points promoted to compulsory or identical stat allocation')
    require(b[1]['jss_selectable_primary_stats']==['体力','腕力','丈夫さ','素早さ']
            and b[1]['creation_twenty_is_per_level_bonus'] is False
            and b[1]['cross_language_primary_to_derived_mapping_or_points_per_level'] is None,
            'Creation pool or language labels promoted to level-up formula')
    require(b[2]['cn_levelup_subject']=='PET' and b[2]['jss_levelup_example_subject']=='OWNER'
            and 'OWNER_LEVEL_UP' in b[2]['jss_loyalty_increase_examples']
            and 'PET_LEVEL_UP' not in b[2]['jss_loyalty_increase_examples']
            and b[2]['different_subjects_prove_patch_or_exhaustive_contradiction'] is False
            and b[2]['sum_or_shared_loyalty_formula'] is None,
            'Pet versus owner level-up conflated or promoted to proven patch')
    require(b[3]['owner_charm_and_pet_loyalty_are_same_field'] is False
            and b[3]['cn_cosmetic_target_100_is_jss_cap_or_gain'] is False
            and b[3]['cross_version_cosmetic_price_or_control_formula'] is None,
            'Charm and loyalty merged or cosmetic target transferred')
    require(b[4]['jss_capture_blocked_gap_at_least']==6
            and b[4]['jss_initial_capture_loyalty_upper_bound']==60
            and b[4]['cn_numeric_capture_gap_or_loyalty_value']==None
            and b[4]['jss_initial_60_is_lifetime_cap_or_cn_rule'] is False,
            'Capture eligibility, qualitative loyalty and initial bound merged')
    require(b[5]['cn_charm_outcomes']==[-4,-1]
            and b[5]['jss_character_consequence']=='CHARM_DECREASES_SLIGHTLY'
            and b[5]['stacked_minus_five_refund_three_or_jss_numeric_delta_proven'] is False
            and b[5]['jss_rescue_omission_proves_no_rescue_feature'] is False,
            'Knockout source comparison promoted to numeric transaction or absence')
    require(b[6]['jss_return_to_savepoint']=='POSSIBLE_DEPENDING_ON_DAMAGE_AT_KNOCKOUT'
            and b[6]['jss_revival_value']==1 and b[6]['jss_revival_timing']=='AFTER_BATTLE_END'
            and b[6]['cn_defense40_level20_is_death_save_threshold'] is False
            and b[6]['unmentioned_exp_money_inventory_or_pet_loss_proven_absent'] is False,
            'Guide build warning promoted to death threshold or absent loss')
    require(b[7]['cn_approximate_early_level']==3
            and b[7]['jss_exp_eligibility_statement']=='ONLY_CHARACTERS_AND_PETS_THAT_KNOCK_OUT_ENEMIES'
            and b[7]['fixed_party_xp_schedule_or_cn_table_filled'] is False,
            'Party advice or manual eligibility promoted to fixed XP schedule')
    require(o['source_accounting']['original_bodies_used']==3
            and o['source_accounting']['jss_pet_and_player_share_manual02'] is True
            and o['source_accounting']['four_reports_are_four_independent_originals'] is False,
            'Derived report count promoted to independent original sources')
    require(o['source_accounting']['original_bodies_reacquired_in_this_job']==0
            and o['source_accounting']['images_programs_or_game_entities_added']==0,
            'Offline comparison promoted to new original acquisition or game entities')
    for r in o['records']:
        require(r['cross_version_rule_transfer_allowed'] is False and r['original_runtime_or_same_build_verified'] is False,
                'Documentary relation promoted to cross-version rule or runtime')


def build(raws):
    require(set(raws)==set(INPUTS),'Exact four fixed Git reports required')
    d={}
    for key,(_,digest) in INPUTS.items():
        require(sha256(raws[key]).hexdigest()==digest,'Pinned Git input differs: '+key)
        d[key]=json.loads(raws[key])
    cn=[r['source_described_claims'] for r in d['cn']['records']]
    player=[r['source_described_behavior'] for r in d['player']['records']]
    pet=d['pet']['contracts'];creation=d['creation']['pages']['manual01']['creation_contract']
    require(cn[7]['levelup_increases_loyalty_is_guide_claim'] is True
            and 'OWNER_LEVEL_UP' in pet['loyalty']['increase_examples'], 'Exact level-up subjects not supported')
    source_meta={
        'cn':{'original_url':d['cn']['source']['original_url'],'actual_capture':d['cn']['source']['actual_capture'],
              'original_sha256':d['cn']['source']['sha256']},
        'creation':{'original_url':'http://www.titan.co.jp/stoneage/manual01.html',
                    'actual_capture':d['creation']['pages']['manual01']['actual_capture'],
                    'original_sha256':d['creation']['pages']['manual01']['sha256']},
        'pet':{'original_url':'http://www.titan.co.jp/stoneage/manual02.html',
               'actual_capture':d['pet']['source']['actual_capture'],'original_sha256':d['pet']['source']['sha256']},
        'player':{'original_url':d['player']['source']['original_url'],
                  'actual_capture':d['player']['source']['actual_capture'],'original_sha256':d['player']['source']['sha256']},
    }
    require(source_meta['pet']==source_meta['player'],'Shared manual02 original identity differs')
    def cnref(i):return ('cn',f'/records/{i}/source_described_claims')
    def pref(i):return ('player',f'/records/{i}/source_described_behavior')
    specs=[
        ('CREATION_POOL_VERSUS_BUILD_ADVICE',[cnref(4),('creation','/pages/manual01/creation_contract')],
         {'cn_recommended_endurance_points':cn[4]['creation_points_recommended_to_endurance'],
          'jss_initial_stat_points':creation['initial_stat_allocation_points'],
          'same_number_proves_mandatory_allocation_or_stat_identity':False}),
        ('CREATION_AND_LEVELUP_ARE_DISTINCT',[cnref(4),pref(0),pref(2)],
         {'jss_selectable_primary_stats':player[2]['player_selectable_bonus_stats_as_written'],
          'creation_twenty_is_per_level_bonus':False,'cross_language_primary_to_derived_mapping_or_points_per_level':None}),
        ('PET_AND_OWNER_LEVELUP_SUBJECTS',[cnref(7),('pet','/contracts/loyalty')],
         {'cn_levelup_subject':'PET','jss_levelup_example_subject':'OWNER',
          'jss_loyalty_increase_examples':pet['loyalty']['increase_examples'],
          'different_subjects_prove_patch_or_exhaustive_contradiction':False,'sum_or_shared_loyalty_formula':None}),
        ('OWNER_CHARM_VERSUS_PET_LOYALTY',[cnref(6),cnref(9),('pet','/contracts/loyalty'),pref(0)],
         {'owner_charm_and_pet_loyalty_are_same_field':False,'cn_cosmetic_target_100_is_jss_cap_or_gain':False,
          'cross_version_cosmetic_price_or_control_formula':None}),
        ('CAPTURE_ELIGIBILITY_VERSUS_LOYALTY_ADVICE',[cnref(7),('pet','/contracts/capture')],
         {'jss_capture_blocked_gap_at_least':pet['capture']['blocked_if_target_level_minus_player_level_at_least'],
          'jss_initial_capture_loyalty_upper_bound':pet['capture']['initial_loyalty_upper_bound'],
          'cn_numeric_capture_gap_or_loyalty_value':cn[7]['levelup_loyalty_gain_cap_capture_gap_or_probability'],
          'jss_initial_60_is_lifetime_cap_or_cn_rule':False}),
        ('KNOCKOUT_AND_MEDICINE_RESCUE',[cnref(6),pref(1)],
         {'cn_charm_outcomes':[cn[6]['knockout_charm_change_as_written'],cn[6]['medicine_rescue_charm_change_as_written']],
          'jss_character_consequence':player[1]['player_knockout_consequence'],
          'stacked_minus_five_refund_three_or_jss_numeric_delta_proven':False,
          'jss_rescue_omission_proves_no_rescue_feature':False}),
        ('BUILD_WARNING_VERSUS_KNOCKOUT_RETURN',[cnref(8),pref(1)],
         {'jss_return_to_savepoint':player[1]['return_to_savepoint'],
          'jss_revival_value':player[1]['after_battle_revival_value_as_written'],'jss_revival_timing':player[1]['revival_timing'],
          'cn_defense40_level20_is_death_save_threshold':False,
          'unmentioned_exp_money_inventory_or_pet_loss_proven_absent':False}),
        ('EARLY_GROWTH_AND_PARTY_XP',[cnref(1),cnref(5),pref(0)],
         {'cn_approximate_early_level':cn[1]['approximate_early_level_label'],
          'jss_exp_eligibility_statement':player[0]['exp_eligibility_source_statement'],
          'fixed_party_xp_schedule_or_cn_table_filled':False}),
    ]
    records=[]
    for i,(topic,refs,comparison) in enumerate(specs):
        source_refs=[]
        for key,ptr in refs:
            pointer(d[key],ptr)
            source_refs.append({'path':str(ROOT/INPUTS[key][0]),'derived_sha256':INPUTS[key][1],
                                'json_pointer':ptr,**source_meta[key]})
        records.append({'record_id':f'early-newcomer-pet-care:source-relation:{i+1:02d}',
                        'collection':'sources','entity_type':'CROSS_SOURCE_DOCUMENTARY_BOUNDARY', 'record_revision':1,
                        'version_profile':'CN20_2001_GUIDE_VERSUS_JSS2001_MANUAL_NOT_SAME_BUILD',
                        'source_refs':source_refs,'bounded_comparison':comparison,'topic':topic,
                        'verification_status':'SOURCE_RELATION_NOT_ORIGINAL_RUNTIME_OR_PROVEN_PATCH',
                        'rights_status':'RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED',
                        'cross_version_rule_transfer_allowed':False,'original_runtime_or_same_build_verified':False})
    o={'schema':'stoneage.early_newcomer_pet_care_boundaries.r1','date':'2026-10-19',
       'task':'EARLY-OFFICIAL-NEWCOMER-AND-PET-CARE-BOUNDARIES-01',
       'pinned_git_inputs':[{'key':k,'path':str(ROOT/p),'sha256':h} for k,(p,h) in INPUTS.items()],
       'records':records,'source_accounting':{'fixed_git_reports':4,'original_bodies_used':3,
                                             'jss_pet_and_player_share_manual02':True,
                                             'four_reports_are_four_independent_originals':False,
                                             'original_bodies_reacquired_in_this_job':0,
                                             'images_programs_or_game_entities_added':0},
       'boundaries':{'source_capture_order_proves_patch_sequence':False,'new_original_source_or_server_execution':False,
                      'source_advice_is_new_game_design':False,'stage_a':'7_PARTIAL_2_OPEN',
                      'stage_b_and_wiki':'GATED','r79':'PAUSED_NON_BLOCKING'},
       'next':'OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-14'}
    validate_report(o);return o


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
    o=build({k:(ROOT/name).read_bytes() for k,(name,_) in INPUTS.items()})
    payload=json.dumps(o,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(payload,encoding='utf-8')
    print('PINNED_GIT_REPORTS=4 ORIGINAL_BODIES_REFERENCED=3 NEW_ORIGINAL_REQUESTS=0 SOURCE_RELATIONS=8')
    print('DERIVED_SHA256='+sha256(payload.encode()).hexdigest())


if __name__=='__main__':main()
