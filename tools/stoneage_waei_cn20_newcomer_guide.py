"""Official-hosted anonymous novice guide: narrative/advice, not server rules."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
from tools.stoneage_early_content_probe import plain, require
from tools.stoneage_wayi_newbie_riding_plan import fetch

ENTRY_REPORT = Path('research/recovered/STONEAGE-WAEI-CN20-LEVEL-EXP-TABLE-R1.json')
ENTRY_REPORT_SHA = 'e012249c799f9789e65f13c5fbb6e0ac746966d7660bb30b68bec9a0150d3b87'
ENTRY_ORIGINAL = 'http://www.waei.com.cn:80/ZHUANQU/stoneage2/sw/adventure.asp'
ORIGINAL = 'http://www.waei.com.cn/ZHUANQU/stoneage2/sw/adventure.asp'
CAPTURE = '20011204212409'
URL = 'https://web.archive.org/web/' + CAPTURE + 'id_/' + ORIGINAL
SOURCE_SHA = 'ef63a7b33db0a967823af8356bbd2369487b20781a3272e1e2c3b0d1500ec1ab'
REPORT = Path('research/recovered/STONEAGE-WAEI-CN20-NEWCOMER-GUIDE-R1.json')
PINS = [(88,'e7fdf9ebbfd29d969f7267e7848b05a27c4839ae724fdd3e91ed135fd92f8eca'),
        (14,'a989279f997f6c687e4324b3b1afc94e558f7fecdec14f1a7bf72072150dd81b'),
        (89,'8dee830419561a6ee9a2e57e7845e98dc26e99bca4bed7372c9be2822cbb4342'),
        (110,'bb99327d5d0a96c12dfb775d33e3e18c244470b1933fe1ddc7d801d003385d07'),
        (165,'2b189317774e19a970176ab40f66f160056be02aae423c0f2e2aa7351963c09b'),
        (18,'3f7ea2ac9c2c9647dc10fe288ed95aad199fc248c8e8ade088dcbbbc151d6159'),
        (98,'96c967bc6a737c5e24d166fcc333224d2922a46fd4989fd9222743bf93b688a2'),
        (59,'ee6dd2eb1c85e33e1c900dc3abf05bad8b0353cc3ec853cdd748c55f8457a989'),
        (117,'f093d03ca50e862cc8bf299fee6c44f70d2f8cb019e610adfe0cdfc1a372a611'),
        (102,'15ac8f5d4033a8faf126040d656c792907bd8cfdde3f1bd71a281c05d2e05652'),
        (139,'aa826d79edb7d55d1f60d60193e52cefe6ab2754b6896b252b648349733d4bc6')]


def sections(doc):
    require(doc.count('新 入 石 器') == 1, 'One actual newcomer heading required')
    m = re.search(r'<td\b[^>]*>(.*?)</td>', doc.split('新 入 石 器',1)[1], re.I | re.S)
    require(m is not None, 'Actual newcomer content cell missing')
    cell = m.group(1)
    ps = [plain(p) for p in re.split(r'(?:<br\s*/?>\s*){2,}', cell.split('<p>',1)[0], flags=re.I) if plain(p)]
    ps += [plain(p) for p in re.findall(r'<p\b[^>]*>(.*?)</p>', cell, re.I | re.S)]
    require(re.findall(r'(?:src|href)="([^"]+)"',cell) == ['img/adventure/1.gif','img/adventure/1s.gif'],
            'Article image references differ')
    return ps


def validate_report(o):
    require(o['source']['authorship'] == 'UNSIGNED_GUIDE_ON_OFFICIAL_OPERATOR_SITE'
            and o['source']['operator_authored_or_independently_runtime_verified'] is False,
            'Official hosting promoted to operator authorship or independent execution')
    require(len(o['records']) == 10, 'Ten source descriptions, not original game entities')
    c = [r['source_described_claims'] for r in o['records']]
    require(c[0]['first_following_pet_species_ids_or_universal_starter_table'] is None
            and c[0]['first_pet_care_is_source_narrative_not_riding_achievement'] is True,
            'First pet narrative promoted to original species, injury loss or first mount')
    require(c[1]['approximate_early_level_label'] == 3 and c[1]['exact_battle_count_exp_or_guaranteed_outcome'] is None,
            'Approximate early level promoted to fixed XP schedule')
    require(c[2]['meat_drop_is_possible_not_guaranteed'] is True
            and c[2]['blood_use_phrase_as_written'] == '捕自己的血'
            and c[2]['read_as_healing_is_editorial_interpretation'] == 'HYPOTHESIS'
            and c[2]['actual_drop_rate_heal_value_prices_or_item_ids'] is None,
            'Meat typo, chance or trade description promoted to exact rule')
    require(c[3]['narrator_low_level_free_treatment_claim'] is True
            and c[3]['free_treatment_level_threshold_or_universal_price'] is None
            and c[3]['nurse_is_named_npc_or_recovered_quest'] is False,
            'Narrative clinic promoted to numeric threshold or named NPC')
    require(c[4]['status'] == 'GUIDE_RECOMMENDATION'
            and c[4]['creation_points_recommended_to_endurance'] == 20
            and c[4]['later_levelups_also_endurance_as_advice'] is True
            and c[4]['mandatory_creation_allocation_or_only_attack_source'] is False
            and c[4]['later_levelup_points_per_level_or_stat_formula'] is None,
            'Allocation advice promoted to compulsory build or formula')
    require(c[5]['party_help_combo_and_chat_are_guide_descriptions'] is True
            and c[5]['party_size_matchmaking_or_combo_formula'] is None,
            'Party advice given unsupported capacity or combo formula')
    require(c[6]['knockout_charm_change_as_written'] == -4
            and c[6]['medicine_rescue_charm_change_as_written'] == -1
            and c[6]['both_penalties_stack_or_three_point_refund_proven'] is False
            and c[6]['cosmetic_level_price_formula_or_runtime_timing'] is None,
            'Charm comparison promoted to stacked penalty, refund or fee algorithm')
    require(c[7]['high_level_caught_pet_lower_loyalty_is_guide_claim'] is True
            and c[7]['raising_level_one_pet_is_recommendation'] is True
            and c[7]['levelup_loyalty_gain_cap_capture_gap_or_probability'] is None,
            'Qualitative pet advice given numeric loyalty, capture rule or cap')
    require(c[8]['status'] == 'GUIDE_RECOMMENDATION'
            and c[8]['conditions_as_written'] == {'level_phrase':'lv 20 以上','defense_phrase':'防低于40','higher_level_friends_absent':True}
            and c[8]['place_labels_as_written'] == ['沙母岛','吉鲁岛']
            and c[8]['mandatory_reset_or_verified_death_save_transaction'] is False
            and c[8]['map_ids_coordinates_or_confirmed_aliases'] is None,
            'Harsh build advice promoted to forced reset, death transaction or map identity')
    require(c[9]['status'] == 'GUIDE_RECOMMENDATION'
            and c[9]['cost_token_as_written'] == '$2000'
            and c[9]['charm_destination_as_written'] == 100
            and c[9]['charm_gain_plus_100_or_universal_cap_100'] is False
            and c[9]['unconditional_fixed_fee_or_safe_transfer_implemented'] is False,
            'Charm destination or social handoff promoted to gain, cap, fee or guaranteed transfer')
    for r in o['records']:
        require(not r['actual_server_rule_or_execution_verified'] and r['original_game_ids_or_same_build_binding'] is None,
                'Guide descriptions promoted to original execution or build')
    require(all(not x['pixels_requested'] and x['actual_capture'] is None and x['sha256'] is None and x['actual_dimensions'] is None
                for x in o['unacquired_image_refs']), 'Source reference promoted to actual pixels')
    require(o['narrative_sequence']['is_quest_dependency_or_mandatory_tutorial_graph'] is False,
            'Documentary story sequence promoted to quest dependency graph')


def build(entry_bytes, body, final):
    require(sha256(entry_bytes).hexdigest() == ENTRY_REPORT_SHA, 'Pinned entry report differs')
    entry = json.loads(entry_bytes)
    require(entry['qualified_unread_entry'] == {'label':'新入石器','original_url':ENTRY_ORIGINAL,'body_or_images_read':False},
            'Authentic prior entry qualification differs')
    require(final == URL, 'Exact final original URL and actual capture required')
    require(len(body) == 65653 and sha256(body).hexdigest() == SOURCE_SHA, 'Newcomer original byte pin differs')
    doc = body.decode('gb18030',errors='strict')
    require(re.search(r'<title>\s*石器时代2\.0\s*</title>',doc,re.I) is not None, 'Actual page version title differs')
    ps = sections(doc)
    require([(len(p),sha256(p.encode()).hexdigest()) for p in ps] == PINS, 'Newcomer section fingerprints differ')
    claims = [
        {'topic':'ARRIVAL_FIRST_PET_AND_CARE','sections':[0,1,2],
         'narrator_begins_with_one_following_pet_and_meets_villagers_and_players':True,
         'first_pet_injury_concern_and_near_village_caution_in_source':True,
         'first_pet_care_is_source_narrative_not_riding_achievement':True,
         'first_following_pet_species_ids_or_universal_starter_table':None},
        {'topic':'APPROXIMATE_EARLY_GROWTH','sections':[3],'approximate_early_level_label':3,
         'exact_battle_count_exp_or_guaranteed_outcome':None},
        {'topic':'MEAT_USE_AND_FIRST_STONE_CURRENCY','sections':[3],
         'meat_drop_is_possible_not_guaranteed':True,'blood_use_phrase_as_written':'捕自己的血',
         'read_as_healing_is_editorial_interpretation':'HYPOTHESIS',
         'village_meat_shop_sale_for_stones_described':True,'actual_drop_rate_heal_value_prices_or_item_ids':None},
        {'topic':'CLINIC_EQUIPMENT_AND_PARTY_JOURNEY','sections':[4],
         'narrator_low_level_free_treatment_claim':True,'free_treatment_level_threshold_or_universal_price':None,
         'nurse_is_named_npc_or_recovered_quest':False,
         'weapon_armor_purchase_then_joining_party_for_further_travel_described':True},
        {'topic':'ENDURANCE_ALLOCATION_ADVICE','sections':[5,6],'status':'GUIDE_RECOMMENDATION',
         'creation_points_recommended_to_endurance':20,'stat_label_as_written':'耐力',
         'later_levelups_also_endurance_as_advice':True,'mandatory_creation_allocation_or_only_attack_source':False,
         'later_levelup_points_per_level_or_stat_formula':None},
        {'topic':'PARTY_COOPERATION_AND_CHAT','sections':[6,7],
         'party_help_combo_and_chat_are_guide_descriptions':True,'combo_label_as_written':'合击',
         'party_size_matchmaking_or_combo_formula':None},
        {'topic':'CHARM_COSMETIC_AND_RESCUE_CLAIMS','sections':[8],
         'cosmetic_charm_helping_pet_control_and_costlier_at_high_level_is_guide_claim':True,
         'knockout_charm_change_as_written':-4,'medicine_rescue_charm_change_as_written':-1,
         'both_penalties_stack_or_three_point_refund_proven':False,'cosmetic_level_price_formula_or_runtime_timing':None},
        {'topic':'PET_LEVEL_AND_LOYALTY_ADVICE','sections':[9],
         'high_level_caught_pet_lower_loyalty_is_guide_claim':True,
         'raising_level_one_pet_is_recommendation':True,'levelup_increases_loyalty_is_guide_claim':True,
         'levelup_loyalty_gain_cap_capture_gap_or_probability':None},
        {'topic':'LOW_DEFENSE_TRAVEL_WARNING','sections':[10],'status':'GUIDE_RECOMMENDATION',
         'conditions_as_written':{'level_phrase':'lv 20 以上','defense_phrase':'防低于40','higher_level_friends_absent':True},
         'place_labels_as_written':['沙母岛','吉鲁岛'],
         'mandatory_reset_or_verified_death_save_transaction':False,'map_ids_coordinates_or_confirmed_aliases':None},
        {'topic':'SOCIAL_HANDOFF_AND_COSMETIC_TARGET','sections':[10],'status':'GUIDE_RECOMMENDATION',
         'handoff_money_items_to_another_person_and_arrange_meeting_suggested':True,
         'cost_token_as_written':'$2000','charm_destination_as_written':100,
         'charm_gain_plus_100_or_universal_cap_100':False,'unconditional_fixed_fee_or_safe_transfer_implemented':False},
    ]
    records=[]
    for i,c in enumerate(claims):
        records.append({'record_id':f'waei-cn20:newcomer-guide:{i+1:02d}','collection':'tutorials',
                        'entity_type':'OFFICIAL_HOSTED_UNSIGNED_NEWCOMER_GUIDE_DESCRIPTION','record_revision':1,
                        'version_profile':'CN_BEIJING_WAEI_PAGE_LABEL_2_0_CAPTURE_2001_NOT_EXACT_BUILD',
                        'source_refs':[{'original_url':ORIGINAL,'actual_capture':CAPTURE,'sha256':SOURCE_SHA,
                                        'section_indices':c['sections'],'normalized_section_sha256':[PINS[n][1] for n in c['sections']]}],
                        'verification_status':'NARRATIVE_ADVICE_OR_NUMERIC_SOURCE_CLAIM_NOT_SERVER_RULE',
                        'rights_status':'RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED','source_described_claims':c,
                        'actual_server_rule_or_execution_verified':False,'original_game_ids_or_same_build_binding':None})
    o={'schema':'stoneage.waei_cn20.newcomer_guide.r1','date':'2026-10-19',
       'task':'CN20-OFFICIAL-NAMED-NEWCOMER-CONTENT-SOURCE-01',
       'source':{'original_url':ORIGINAL,'strict_replay_url':URL,'actual_capture':CAPTURE,'bytes':len(body),'sha256':SOURCE_SHA,
                 'encoding':'GB18030_STRICT','page_title_as_written':'石器时代2.0','article_heading_as_written':'新 入 石 器',
                 'authorship':'UNSIGNED_GUIDE_ON_OFFICIAL_OPERATOR_SITE','operator_authored_or_independently_runtime_verified':False,
                 'capture_is_unchanged_launch_body_or_deployment_proven':False},
       'entry_provenance':{'path':str(ENTRY_REPORT),'sha256':ENTRY_REPORT_SHA,'json_pointer':'/qualified_unread_entry',
                           'label':'新入石器','qualified_original_url':ENTRY_ORIGINAL,
                           'original_entry_page_reacquired_by_this_job':False},
       'section_fingerprints':[{'index':i,'normalized_characters':n,'sha256':h} for i,(n,h) in enumerate(PINS)],
       'records':records,
       'narrative_sequence':{'source_section_indices':[0,2,3,4],
                             'source_described_order':['ARRIVE_WITH_FIRST_PET','MEET_PEOPLE_AND_KEEP_NEAR_VILLAGE',
                                                       'EARLY_BATTLES_AND_POSSIBLE_MEAT','VILLAGE_MEAT_SALE',
                                                       'CLINIC_VISIT','BASIC_WEAPON_AND_ARMOR_PURCHASE','JOIN_PARTY_AND_TRAVEL_FURTHER'],
                             'is_quest_dependency_or_mandatory_tutorial_graph':False},
       'unacquired_image_refs':[{'original_url':'http://www.waei.com.cn/ZHUANQU/stoneage2/sw/img/adventure/'+v+'.gif',
                                  'role':role,'html_declared_dimensions':dims,'pixels_requested':False,
                                  'actual_capture':None,'sha256':None,'actual_dimensions':None}
                                 for v,role,dims in [('1','LINKED_IMAGE',None),('1s','INLINE_IMAGE',[240,180])]],
       'coverage':{'guide_descriptions':10,'named_place_mentions_not_verified_maps':2,'new_original_body':1,
                    'original_game_entities_or_server_transactions_restored':0,'images_binaries_or_other_pages_acquired':0},
       'boundaries':{'cn25_jss1999_tw10_cn182_same_rule_or_build_proven':False,'automatic_new_game_design_adoption':False,
                      'raw_original_html_or_assets_in_git':False,'stage_a':'7_PARTIAL_2_OPEN',
                      'stage_b_and_wiki':'GATED','r79':'PAUSED_NON_BLOCKING'},
       'next':'EARLY-OFFICIAL-NEWCOMER-AND-PET-CARE-BOUNDARIES-01'}
    validate_report(o);return o


def main():
    p=argparse.ArgumentParser();p.add_argument('--input');p.add_argument('--output',required=True);a=p.parse_args()
    body,final=(Path(a.input).read_bytes(),URL) if a.input else fetch(URL)
    o=build(ENTRY_REPORT.read_bytes(),body,final);payload=json.dumps(o,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(payload,encoding='utf-8')
    print('SOURCE_SHA256='+SOURCE_SHA);print('ENTRY_REPORT_SHA256='+ENTRY_REPORT_SHA)
    print('GUIDE_DESCRIPTIONS=10 NEW_ORIGINAL_BODY=1 ACTUAL_SERVER_RULES=0')
    print('DERIVED_SHA256='+sha256(payload.encode()).hexdigest())


if __name__=='__main__':main()
