"""Finite comparison of five immutable derived reports; no new historical source fetched."""
import argparse
from hashlib import sha256
import json
from pathlib import Path

ROOT=Path('research/recovered')
REPORT=ROOT/'STONEAGE-EARLY-SOURCE-MAIL-VENUE-CROSSWALK-R1.json'
INPUTS={
 'manual':('STONEAGE-JSS2001-MAIL-ITEMS-SHARED-VENUES-R1.json','7a586ce0f16a3922c62f711554e9c158e659d143ad158b4cbea184936ac74122'),
 'early':('STONEAGE-EARLY-CONTENT-GUIDE-MANUAL-R1.json','02c854ace5ff8364fc141dc4ee58e6c518b91af126b89b8c0ee2d4b112c9ae5b'),
 'hangame':('STONEAGE-JP-OFFICIAL-VILLAGE-FACILITIES-R1.json','65ed727327aae1e8b060834c11c33d56685134a6bbd8fb02e250086baf4f5dfb'),
 'arcades':('STONEAGE-WAYI-THEATRE-ARCADES-R1.json','f76d9008a425cc335706510303ceff96be72c1aeba9ee42a1d7b06c87a248669'),
 'cards':('STONEAGE-WAYI-MARINE-SOCIAL-CRAFTING-R1.json','d4772a21b27e50bd66d51fd9e53508a301f9e498f2d777708dd94eb87104dccd'),
}


def require(v,m):
    if not v:raise ValueError(m)


def pointer(obj,path):
    require(path.startswith('/'),'Expected explicit JSON pointer')
    try:
        for token in path[1:].split('/'):
            key=token.replace('~1','/').replace('~0','~')
            obj=obj[int(key)] if isinstance(obj,list) else obj[key]
    except (KeyError,IndexError,ValueError,TypeError) as exc:raise ValueError('Missing input evidence pointer '+path) from exc
    return obj


def validate_report(o):
    require(len(o['records'])==8,'Eight finite boundary comparisons required')
    for r in o['records']:
        require(r['automatic_entity_or_rule_merge_allowed'] is False and r['historical_update_or_rule_removal_proven'] is False,'Unproven entity merge or historical change promoted')
        require(r['numeric_id_price_timer_projection_allowed'] is False and r['original_server_execution_proven'] is False,'Unsupported numeric projection or original runtime')
        require(len(r['source_refs'])>=2 and r['unknown_identity_or_runtime_details'] is None,'Comparison provenance/unknowns lost')
    require(o['coverage']['new_original_urls_fetched']==0 and o['coverage']['derived_inputs']==5 and o['coverage']['distinct_original_bodies_referenced']==4,'Derived reports counted as new/independent original sources')
    require(o['records'][0]['same_original_manual_two_reports_are_independent_witnesses'] is False,'Same manual counted as independent witnesses')
    require(o['records'][2]['source_facts']['later_quiz_threshold_and_fee'] is None,'Early arena exemption projected to later quiz')
    require(o['records'][5]['source_facts']['later_dedicated_slot_count']==1,'Two roles invented as two dedicated slots')


def build(raw_inputs):
    require(set(raw_inputs)==set(INPUTS),'Exact five input reports required')
    data={}
    for key,(filename,pin) in INPUTS.items():
        raw=raw_inputs[key];require(sha256(raw).hexdigest()==pin,'Derived input byte pin differs: '+key);data[key]=json.loads(raw)
    m=data['manual']['records'];jp=data['hangame']['records'];cards=data['cards']['business_cards'];arc=data['arcades']['records'];early=data['early']['observations']['manual_contracts']
    def evidence(key,path):
        pointer(data[key],path)
        if key=='early':s=data[key]['sources']['jss_manual'];original=s['replay_url'].split('id_/',1)[1];capture=data[key]['manual_capture'];source_sha=s['sha256']
        else:
            s=data[key]['source'];original=s['original_url'];capture=s['actual_capture'];source_sha=s['sha256']
        return {'derived_report':str(ROOT/INPUTS[key][0]),'derived_sha256':INPUTS[key][1],'json_pointer':path,'original_source':original,'actual_capture':capture,'original_sha256':source_sha}
    cases=[
      ('MAIL_GRACE_VERSUS_STRAY_AND_ORDINARY_ITEM_TIMERS','DISTINCT_LIFECYCLE_EVENT_AND_UNSPECIFIED_TIMER',[('manual','/records/1/source_described_behavior'),('early','/observations/manual_contracts/ground_item')],{'mail_grace_and_stray_timer_values':m[1]['source_described_behavior']['grace_hours_stray_ttl_pet_ids_or_persistence_format'],'ordinary_ground_item_expires_after_unspecified_time':early['ground_item']['ordinary_ground_item_expires_after_unspecified_time'],'ordinary_ground_item_duration':early['ground_item']['duration']}),
      ('SPECIAL_TICKET_DROP_VERSUS_ORDINARY_ITEM_EXPIRY','CONTEXT_SPECIFIC_IMMEDIATE_DROP_NOT_UNIVERSAL_EXPIRY',[('manual','/records/8/source_described_behavior/ticket_warning'),('early','/observations/manual_contracts/ground_item')],{'special_ticket_immediate_drop_disappearance':m[8]['source_described_behavior']['ticket_warning']['drop_causes_immediate_disappearance_described'],'same_ticket_or_generic_item_id':None,'ordinary_duration':early['ground_item']['duration']}),
      ('EARLY_DUEL_ARENA_VERSUS_LATER_QUIZ','DIFFERENT_SOURCE_LABEL_AND_CONTEXT_NO_ENTITY_JOIN',[('manual','/records/8/source_described_behavior'),('hangame','/records/8/source_described_behaviors')],{'early_free_admission_cases':m[8]['source_described_behavior']['free_admission_enumerated_cases'],'later_quiz_level_restriction_described':jp[8]['source_described_behaviors']['level_restriction_required'],'later_quiz_entry_fee_described':jp[8]['source_described_behaviors']['entry_fee_required'],'later_quiz_threshold_and_fee':jp[8]['source_described_behaviors']['threshold_fee_item_ids_event_sequence']}),
      ('LOCAL_ARENA_FREE_RECOVERY_VERSUS_LATER_HOSPITAL','EARLY_LOCAL_SPECIFIC_LATER_PRICE_UNSPECIFIED_NOT_PROVEN_REMOVAL',[('manual','/records/8/source_described_behavior'),('hangame','/records/1/source_described_behaviors')],{'early_arena_hospital_free':m[8]['source_described_behavior']['hospital_recovery_free_in_arena_context'],'later_hp_recovery_offered':jp[1]['source_described_behaviors']['hp_recovery_offered'],'later_targets_amount_and_price':jp[1]['source_described_behaviors']['actor_full_heal_mp_pet_targets_amount_price']}),
      ('EARLY_CHATROOM_FREE_VERSUS_LATER_ENTRY_ONLY','EARLY_EXPLICIT_FEE_STATE_LATER_OMISSION_NOT_PROVEN_CHANGE',[('manual','/records/7/source_described_behavior'),('hangame','/records/7/source_described_behaviors')],{'early_chatroom_free':m[7]['source_described_behavior']['direct_chatroom_admission_described_as_free'],'later_entry_described':jp[7]['source_described_behaviors']['chat_room_entry_described'],'later_fee':None}),
      ('CARD_CONSENT_RESET_VERSUS_LATER_ROLE_CARD_RETENTION','DIFFERENT_STATE_OBJECT_PERMISSION_VERSUS_ROLE_CONTACT_SLOT',[('manual','/records/5/source_described_behavior'),('cards','/business_cards')],{'early_logout_resets_exchange_permission_to_no':m[5]['source_described_behavior']['logout_resets_exchange_setting_to_no'],'early_logout_deletes_contacts_proven':m[5]['source_described_behavior']['logout_deletes_contact_records_proven'],'later_ordinary_capacity_before':cards['ordinary_capacity_before_described'],'later_ordinary_capacity_after':cards['ordinary_capacity_after_described'],'later_dedicated_slot_count':cards['additional_dedicated_slot_described'],'later_role_card_end_state':cards['end_of_summoning_task'],'later_role_card_next_assignment':cards['next_role_assignment'],'early_capacity':None}),
      ('DUEL_RANK_VERSUS_ART_VALUE_AND_ARCADE_POINTS','DIFFERENT_MEASURES_AND_UNKNOWN_LEDGER_OR_CONVERSION',[('manual','/records/8/source_described_behavior/free_admission_enumerated_cases'),('arcades','/records')],{'early_measure':'DUEL_RANK_POSITION_NOT_REDEEMABLE_BALANCE','later_point_labels':[r['points_label_as_written'] for r in arc],'shared_wallet_or_conversion_rate':None}),
      ('PET_ITEM_MAIL_VERSUS_MAMMOTH_DELIVERY_JOB','DIFFERENT_DELIVERY_FUNCTION_NOT_ONE_PET_OWNERSHIP_OR_PAYROLL_PIPELINE',[('manual','/records/1/source_described_behavior'),('hangame','/records/10/source_described_behaviors')],{'early_pet_can_carry_message_or_item':m[1]['source_described_behavior']['pet_mail_can_carry_message_or_item_described'],'later_item_delivery_job':jp[10]['source_described_behaviors']['item_delivery_part_time_job_described'],'later_farther_pay_relation_described':jp[10]['source_described_behaviors']['source_says_farther_delivery_higher_wage'],'common_pet_or_item_id_and_pay_formula':None}),
    ]
    records=[]
    for i,(topic,relation,refs,facts) in enumerate(cases):
        records.append({'record_id':f'source-boundary:early-mail-venues:{i+1:02d}','collection':'sources','entity_type':'CROSS_SOURCE_SCOPE_AND_NON_EQUIVALENCE_RECORD','record_revision':1,'version_profile':'CROSS_SOURCE_DOCUMENTARY_COMPARISON_NOT_UNIVERSAL_RULESET','source_refs':[evidence(key,path) for key,path in refs],'verification_status':'BOUNDED_COMPARISON_NOT_ENTITY_IDENTITY_OR_PATCH_HISTORY','rights_status':'RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED','topic':topic,'relation':relation,'source_facts':facts,'automatic_entity_or_rule_merge_allowed':False,'historical_update_or_rule_removal_proven':False,'numeric_id_price_timer_projection_allowed':False,'original_server_execution_proven':False,'unknown_identity_or_runtime_details':None})
    records[0]['same_original_manual_two_reports_are_independent_witnesses']=False
    o={'schema':'stoneage.early_source_mail_venue.crosswalk.r1','date':'2026-10-19','task':'EARLY-SOURCE-MAIL-VENUE-CROSS-VERSION-BOUNDARY-01','inputs':{k:{'path':str(ROOT/v[0]),'sha256':v[1]} for k,v in INPUTS.items()},'records':records,'coverage':{'derived_inputs':5,'distinct_original_bodies_referenced':4,'boundary_comparisons':8,'new_original_urls_fetched':0,'new_game_entities_or_server_rules_recovered':0},'boundaries':{'same_names_or_shared_delivery_word_establish_identity':False,'omission_is_proven_historical_rule_change':False,'new_original_sources_or_assets_acquired':False,'stage_a_families':'7_PARTIAL_2_OPEN','stage_b_and_wiki':'GATED','r79':'PAUSED_NON_BLOCKING'},'next':'JSS2001-PLAYER-STATUS-LEVELUP-AND-KNOCKOUT-01'}
    validate_report(o);return o


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args()
    o=build({k:(ROOT/f).read_bytes() for k,(f,_) in INPUTS.items()});payload=json.dumps(o,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(payload,encoding='utf-8')
    print('BOUNDARY_COMPARISONS=8 NEW_ORIGINAL_SOURCES=0');print('DERIVED_SHA256='+sha256(payload.encode()).hexdigest())


if __name__=='__main__':main()
