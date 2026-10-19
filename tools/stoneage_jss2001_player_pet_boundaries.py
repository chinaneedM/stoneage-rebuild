"""Seven finite semantic joins of existing JSS reports; no network acquisition."""
import argparse
from hashlib import sha256
import json
from pathlib import Path

from tools.stoneage_early_mail_venue_crosswalk import pointer, require

ROOT = Path('research/recovered')
REPORT = ROOT / 'STONEAGE-JSS2001-PLAYER-PET-CREATION-BOUNDARIES-R1.json'
INPUTS = {
    'player': ('STONEAGE-JSS2001-PLAYER-STATUS-LEVELUP-KNOCKOUT-R1.json',
               '13df1d32a44127f80c3e042c335dc01d9cf926011f5b7908b1b71be77d818277'),
    'creation': ('JSS-LOGIN-MANUAL-CREATION-CONTRACT-R1.json',
                 'fb1bc22fbb6e42dfaf39f1ff928ab4278595b0eb3f61e98c33b50d1009690768'),
    'pet': ('STONEAGE-JSS2001-PET-MANUAL-CONTRACT-R1.json',
            'ec4c1602472fb5daa2d458e455f06df3318011e560be053abd460d7d5fba5a13'),
    'arena': ('STONEAGE-JSS2001-MAIL-ITEMS-SHARED-VENUES-R1.json',
              '7a586ce0f16a3922c62f711554e9c158e659d143ad158b4cbea184936ac74122'),
}


def validate_report(o):
    require(len(o['records']) == 7, 'Seven finite semantic comparisons required')
    for r in o['records']:
        require(len(r['source_refs']) >= 2 and r['automatic_numeric_or_field_identity_join_allowed'] is False,
                'Comparison provenance missing or unsupported automatic join')
        require(r['same_original_body_counts_as_independent_confirmation'] is False
                and r['original_server_execution_proven'] is False, 'Derived reports promoted to independent source/runtime')
        require(r['original_unknown_values_and_wire_binding'] is None, 'Original missing values invented')
    facts = [r['source_facts'] for r in o['records']]
    require(facts[0]['creation_stat_points'] == 20 and facts[0]['per_level_points'] is None,
            'Creation stat points projected to level-up')
    require(facts[1]['creation_element_points'] == 10 and facts[1]['creation_max_element_types'] == 2
            and facts[1]['level_up_element_allocation_proven'] is False, 'Creation elements projected to level-up')
    require(facts[2]['player_knockout_effect'] == 'CHARM_DECREASES_SLIGHTLY'
            and facts[2]['pet_knockout_effect'] == 'LOYALTY_DECREASES'
            and facts[2]['charm_change_is_loyalty_same_field'] is False, 'Charm and loyalty conflated')
    require(facts[3]['knockout_appearance_in_loyalty_decrease_examples'] == 'PET_UNCONSCIOUS'
            and facts[3]['loyalty_decrease_numeric_delta'] is None, 'Same-body knockout repeated as numeric proof')
    require(facts[4]['owner_level_up_is_loyalty_increase_example'] is True
            and facts[4]['pet_gets_player_up_allocation_ui'] is False
            and facts[4]['total_or_recursive_loyalty_increment'] is None, 'Owner level-up promoted to pet growth formula')
    require(facts[5]['arena_free_cases'] == [{'level_at_most': 9}, {'duel_rank_exact': 77}, {'duel_rank_exact': 777}]
            and facts[5]['dp_to_rank_conversion'] is None, 'Duel rank positions treated as DP balance')
    require(facts[6]['capture_or_pickup_blocked_gap_at_least'] == 6
            and facts[6]['pickup_blocked_gap_at_least'] == 6
            and facts[6]['initial_capture_loyalty_upper_bound'] == 60
            and facts[6]['universal_loyalty_cap_or_exp_reward_formula'] is None, 'Capture bounds projected to universal cap or EXP')
    require(o['coverage'] == {'derived_reports': 4, 'original_bodies_referenced': 2,
                             'new_original_requests': 0, 'new_assets_or_game_entities': 0,
                             'finite_semantic_comparisons': 7}, 'Source report counts mistaken for new independent originals')


def build(raw_inputs):
    require(set(raw_inputs) == set(INPUTS), 'Exact four input reports required')
    data = {}
    for key, (_, digest) in INPUTS.items():
        require(sha256(raw_inputs[key]).hexdigest() == digest, 'Input byte pin differs: ' + key)
        data[key] = json.loads(raw_inputs[key])
    p = [r['source_described_behavior'] for r in data['player']['records']]
    c = data['creation']['pages']['manual01']['creation_contract']
    pet = data['pet']['contracts']; arena = data['arena']['records'][8]['source_described_behavior']

    def evidence(key, path):
        pointer(data[key], path)
        if key == 'creation':
            s = data[key]['pages']['manual01']; url = s['final_url']
        elif key == 'pet':
            s = data[key]['source']; url = s['final_url']
        else:
            s = data[key]['source']; url = s['strict_replay_url']
        return {'derived_report': str(ROOT / INPUTS[key][0]), 'derived_sha256': INPUTS[key][1],
                'json_pointer': path, 'original_source': url.split('id_/', 1)[1],
                'actual_capture': s['actual_capture'], 'original_sha256': s['sha256']}

    cases = [
        ('CREATION_VERSUS_LATER_LEVEL_UP_POINTS',
         [('creation', '/pages/manual01/creation_contract'), ('player', '/records/2/source_described_behavior')],
         {'creation_stat_points': c['initial_stat_allocation_points'],
          'per_level_points': p[2]['bonus_count_per_level_charm_delta_dp_delta_caps_or_respec']},
         'INITIAL_ALLOCATION_DOES_NOT_FILL_LATER_BONUS_COUNT'),
        ('INITIAL_ELEMENTS_VERSUS_LEVEL_UP_AND_INFLUENCE_PAIRS',
         [('creation', '/pages/manual01/creation_contract'), ('player', '/records/0/source_described_behavior'),
          ('player', '/records/2/source_described_behavior')],
         {'creation_element_points': c['initial_element_allocation_points'],
          'creation_max_element_types': c['maximum_allocated_element_types'],
          'level_up_element_allocation_proven': p[2]['element_allocation_inferred_from_character_bonus_ui'],
          'element_damage_coefficients': p[0]['element_advantage_direction_or_coefficients']},
         'INITIAL_CONFIGURATION_NOT_LEVEL_UP_BONUS_OR_ELEMENTAL_DAMAGE_FORMULA'),
        ('CHARACTER_CHARM_AND_PET_LOYALTY_RELATED_NOT_IDENTICAL',
         [('player', '/records/1/source_described_behavior'), ('pet', '/contracts/loyalty')],
         {'player_knockout_effect': p[1]['player_knockout_consequence'],
          'pet_knockout_effect': p[1]['pet_knockout_consequence'],
          'charm_change_is_loyalty_same_field': p[1]['charm_and_loyalty_are_same_field'],
          'owner_charm_change_appears_in_loyalty_examples':
              'OWNER_CHARM_UP' in pet['loyalty']['increase_examples'] and 'OWNER_CHARM_DOWN' in pet['loyalty']['decrease_examples']},
         'DOCUMENTED_RELATION_DOES_NOT_COLLAPSE_TWO_ACTORS_OR_STATE_FIELDS'),
        ('PET_KNOCKOUT_CONCORDANCE_WITHIN_ONE_MANUAL',
         [('player', '/records/1/source_described_behavior'), ('pet', '/contracts/loyalty/decrease_examples')],
         {'knockout_appearance_in_loyalty_decrease_examples':
              next(x for x in pet['loyalty']['decrease_examples'] if x == 'PET_UNCONSCIOUS'),
          'loyalty_decrease_numeric_delta': pet['loyalty']['numeric_deltas_or_formula']},
         'SAME_SOURCE_INTERNAL_CONCORDANCE_NOT_TWO_INDEPENDENT_OBSERVATIONS'),
        ('OWNER_LEVEL_UP_VERSUS_PET_GROWTH_AND_LOYALTY',
         [('player', '/records/2/source_described_behavior'), ('pet', '/contracts/loyalty/increase_examples')],
         {'owner_level_up_is_loyalty_increase_example': 'OWNER_LEVEL_UP' in pet['loyalty']['increase_examples'],
          'automatic_player_stat_increases': p[2]['automatic_increases_as_written'],
          'pet_gets_player_up_allocation_ui': p[2]['pet_growth_distribution_inferred_from_character_bonus_ui'],
          'total_or_recursive_loyalty_increment': None},
         'MULTIPLE_RELATED_EXAMPLES_DO_NOT_PROVE_ADDITIVE_OR_RECURSIVE_FORMULA'),
        ('DP_VALUE_VERSUS_DUEL_RANK_POSITION',
         [('player', '/records/0/source_described_behavior'), ('arena', '/records/8/source_described_behavior')],
         {'dp_increase_triggers': p[0]['dp_increases_described_on'],
          'arena_free_cases': arena['free_admission_enumerated_cases'], 'dp_to_rank_conversion': None},
         'ARENA_RANK_POSITION_NOT_DP_AMOUNT_AND_CHARACTER_LEVEL_IS_SEPARATE'),
        ('CAPTURE_PICKUP_ELIGIBILITY_VERSUS_EXP_AND_LOYALTY_CAP',
         [('pet', '/contracts/capture'), ('pet', '/contracts/pickup'), ('player', '/records/0/source_described_behavior')],
         {'capture_or_pickup_blocked_gap_at_least': pet['capture']['blocked_if_target_level_minus_player_level_at_least'],
          'pickup_blocked_gap_at_least': pet['pickup']['blocked_if_pet_level_minus_player_level_at_least'],
          'initial_capture_loyalty_upper_bound': pet['capture']['initial_loyalty_upper_bound'],
          'exp_eligibility_statement': p[0]['exp_eligibility_source_statement'],
          'universal_loyalty_cap_or_exp_reward_formula': None},
         'CAPTURE_INITIAL_BOUND_NOT_MAXIMUM_LIFETIME_LOYALTY_OR_COMBAT_EXP_RULE'),
    ]
    records = []
    for i, (topic, refs, facts, relation) in enumerate(cases):
        records.append({'record_id': f'jss2001-source-boundary:player-pet:{i+1:02d}',
                        'entity_type': 'INTRA_MANUAL_SEMANTIC_BOUNDARY_COMPARISON', 'collection': 'sources',
                        'record_revision': 1, 'version_profile': 'JSS_JAPAN_WEB_MANUAL_20010418',
                        'source_refs': [evidence(key, path) for key, path in refs],
                        'verification_status': 'SOURCE_SEMANTICS_NOT_ORIGINAL_FIELD_OR_FORMULA_IDENTITY',
                        'rights_status': 'RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED',
                        'topic': topic, 'relation': relation, 'source_facts': facts,
                        'automatic_numeric_or_field_identity_join_allowed': False,
                        'same_original_body_counts_as_independent_confirmation': False,
                        'original_server_execution_proven': False, 'original_unknown_values_and_wire_binding': None})
    o = {'schema': 'stoneage.jss2001.player_pet_creation_boundaries.r1', 'date': '2026-10-19',
         'task': 'JSS2001-PLAYER-PET-STATUS-AND-CREATION-BOUNDARY-01',
         'inputs': {k: {'path': str(ROOT / v[0]), 'sha256': v[1]} for k, v in INPUTS.items()},
         'records': records,
         'coverage': {'derived_reports': 4, 'original_bodies_referenced': 2, 'new_original_requests': 0,
                      'new_assets_or_game_entities': 0, 'finite_semantic_comparisons': 7},
         'boundaries': {'different_original_bodies_mean_independent_publishers': False,
                        'jss1999_tw10_cn182_same_build_identity': False,
                        'original_server_numeric_growth_or_save_io_recovered': False,
                        'stage_a': '7_PARTIAL_2_OPEN', 'stage_b_and_wiki': 'GATED', 'r79': 'PAUSED_NON_BLOCKING'},
         'next': 'OFFICIAL-VERSION-COVERAGE-MATERIAL-REVIEW-09'}
    validate_report(o)
    return o


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--output', required=True)
    args = parser.parse_args()
    o = build({k: (ROOT / v[0]).read_bytes() for k, v in INPUTS.items()})
    payload = json.dumps(o, ensure_ascii=False, sort_keys=True, indent=2) + '\n'
    path = Path(args.output); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload, encoding='utf-8')
    print('FINITE_COMPARISONS=7 NEW_ORIGINAL_REQUESTS=0')
    print('DERIVED_SHA256=' + sha256(payload.encode()).hexdigest())


if __name__ == '__main__':
    main()
