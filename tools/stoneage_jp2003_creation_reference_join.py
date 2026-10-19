"""Finite offline joins of feature prose, web positions and early creation controls."""
import argparse
from hashlib import sha256
import json
from pathlib import Path

from tools.stoneage_early_mail_venue_crosswalk import pointer, require

ROOT = Path('research/recovered')
REPORT = ROOT / 'STONEAGE-JP2003-CREATION-VISUAL-REFERENCE-JOIN-R1.json'
INPUTS = {
    'features': ('STONEAGE-JP2003-GAME-FEATURES-R1.json', 'f74bb9f07cdf02ca7ddb2f2e9bbeac2cd7f90b3ecb977343608e0dde626a6743'),
    'characters': ('STONEAGE-JP2003-CHARACTER-VISUAL-SOURCE-R1.json', '00ef16a71581ebadeed139143ab572ff5ac27c9944e82c7badcdb31611a46192'),
    'creation': ('JSS-LOGIN-MANUAL-CREATION-CONTRACT-R1.json', 'fb1bc22fbb6e42dfaf39f1ff928ab4278595b0eb3f61e98c33b50d1009690768'),
}


def validate_report(o):
    require(len(o['records']) == 5, 'Five finite creation reference comparisons required')
    f = [r['source_facts'] for r in o['records']]
    require(f[0]['advertised_appearance_types'] == 12 and f[0]['colors_per_type'] == 4
            and f[0]['web_positions'] == 12 and len(f[0]['position_reference_index']) == 12,
            'Appearance dimension or existing position denominator changed')
    require(all(x['exact_appearance_type_or_color_ids'] is None for x in f[0]['position_reference_index'])
            and f[0]['forty_eight_new_character_entities'] is False,
            'Matching cardinality promoted to exact model/color join')
    require([x['web_ordinal'] for x in f[0]['position_reference_index']] == list(range(1, 13))
            and [x['existing_report_pointer'] for x in f[0]['position_reference_index']]
                == ['/characters/' + str(i) for i in range(12)]
            and len({x['existing_record_id'] for x in f[0]['position_reference_index']}) == 12,
            'Existing position index duplicated or misbound')
    require(f[1]['operator_no_fixed_names'] is True and f[1]['player_naming_described'] is True
            and f[1]['canonical_names_or_later_nickname_aliases'] is None, 'Player naming promoted to canonical identity')
    require(f[2]['eyes_mouth_customization_and_card_face'] is True
            and f[2]['static_illustration_or_companion_is_face_editor_asset'] is None
            and f[2]['companion_reference_role'] == 'UNINSPECTED',
            'Face editor confused with static web illustration')
    require(f[3]['page_capture'] == '20031214051427' and f[3]['reviewed_image_capture'] == '20060619160353'
            and f[3]['known_illustration_pixels'] == 1 and f[3]['unacquired_character_page_references'] == 23
            and f[3]['four_colors_names_or_animation_sets'] is None,
            'Later illustration promoted to four colors or full original animation')
    require(f[4]['early_creation_stat_points'] == 20 and f[4]['early_creation_element_points'] == 10
            and f[4]['early_max_element_types'] == 2 and f[4]['later_element_categories'] == 4
            and f[4]['same_allocation_values_or_same_build_proven'] is False,
            'Earlier allocation values projected into later feature prose')
    for r in o['records']:
        require(len(r['source_refs']) >= 2 and r['automatic_entity_model_or_field_merge_allowed'] is False
                and r['original_client_build_or_runtime_proven'] is False
                and r['unknown_color_face_sprite_or_creation_values'] is None,
                'Reference relationship promoted to original entity/runtime identity')
    require(o['coverage'] == {'pinned_derived_reports': 3, 'distinct_original_text_bodies_referenced': 3,
                             'previously_reviewed_image_objects_referenced': 1,
                             'comparison_records': 5, 'existing_position_references_indexed': 12,
                             'new_original_requests_images_or_entities': 0},
            'Derived references counted as new originals or entities')


def build(raw_inputs):
    require(set(raw_inputs) == set(INPUTS), 'Exact three pinned input reports required')
    data = {}
    for k, (_, digest) in INPUTS.items():
        require(sha256(raw_inputs[k]).hexdigest() == digest, 'Input byte pin differs: ' + k)
        data[k] = json.loads(raw_inputs[k])
    features = [r['source_described_behavior'] for r in data['features']['records']]
    chars = data['characters']; creation = data['creation']['pages']['manual01']['creation_contract']
    def evidence(k, path, image=False):
        pointer(data[k], path)
        s = data[k]['reviewed_image'] if image else data[k]['page'] if k == 'characters' else data[k]['pages']['manual01'] if k == 'creation' else data[k]['source']
        final = s.get('strict_replay_url', s.get('final_url'))
        return {'derived_report': str(ROOT / INPUTS[k][0]), 'derived_sha256': INPUTS[k][1],
                'json_pointer': path, 'original_url': final.split('id_/', 1)[1],
                'actual_capture': s['actual_capture'], 'original_sha256': s['sha256'],
                'object_kind': 'EXISTING_REVIEWED_WEB_IMAGE' if image else 'ORIGINAL_TEXT_BODY'}
    cases = [
        ('APPEARANCE_DIMENSIONS_AND_EXISTING_WEB_POSITIONS',
         [('features', '/records/0', False), ('characters', '/characters', False)],
         {'advertised_appearance_types': features[0]['appearance_types_described'],
          'colors_per_type': features[0]['colors_per_type_described'],
          'web_positions': chars['grid']['paired_web_positions'],
          'position_reference_index': [{'existing_record_id': r['record_id'],
                                        'existing_report_pointer': '/characters/' + str(i),
                                        'web_ordinal': r['web_ordinal'], 'exact_appearance_type_or_color_ids': None}
                                       for i, r in enumerate(chars['characters'])],
          'forty_eight_new_character_entities': False}),
        ('PLAYER_ASSIGNED_NAME_NOT_ARCHETYPE_NAME',
         [('characters', '/identity', False), ('features', '/records/0', False)],
         {'operator_no_fixed_names': chars['identity']['operator_explicitly_describes_no_fixed_names'],
          'player_naming_described': chars['identity']['player_naming_described'],
          'canonical_names_or_later_nickname_aliases': None}),
        ('CUSTOM_CARD_FACE_NOT_STATIC_ART_OR_COMPANION_ROLE',
         [('features', '/records/1', False), ('characters', '/characters/0', False)],
         {'eyes_mouth_customization_and_card_face': features[1]['eyes_and_mouth_customizable_described']
                                                   and features[1]['created_face_used_during_card_exchange_described'],
          'static_illustration_or_companion_is_face_editor_asset': None,
          'companion_reference_role': chars['characters'][0]['companion_reference']['contents_or_animation_status']}),
        ('ONE_LATER_IMAGE_NOT_ALL_APPEARANCE_COLORS_OR_ANIMATIONS',
         [('characters', '/grid', False), ('characters', '/reviewed_image', True), ('features', '/records/0', False)],
         {'page_capture': chars['page']['actual_capture'],
          'reviewed_image_capture': chars['reviewed_image']['actual_capture'],
          'known_illustration_pixels': chars['grid']['illustrations_visually_inspected'],
          'unacquired_character_page_references': chars['grid']['other_image_references_unacquired'],
          'four_colors_names_or_animation_sets': None}),
        ('EARLY_CREATION_ALLOCATION_VERSUS_LATER_CATEGORY_DESCRIPTION',
         [('creation', '/pages/manual01/creation_contract', False), ('features', '/records/1', False)],
         {'early_creation_stat_points': creation['initial_stat_allocation_points'],
          'early_creation_element_points': creation['initial_element_allocation_points'],
          'early_max_element_types': creation['maximum_allocated_element_types'],
          'later_element_categories': features[1]['element_category_count_described'],
          'same_allocation_values_or_same_build_proven': False}),
    ]
    records = []
    for i, (topic, refs, facts) in enumerate(cases):
        records.append({'record_id': f'jp2003-creation-reference-comparison:{i+1:02d}', 'collection': 'sources',
                        'entity_type': 'CHARACTER_CREATION_REFERENCE_SCOPE_COMPARISON', 'record_revision': 1,
                        'version_profile': 'JP2001_2003_TEXT_AND_2006_IMAGE_SEPARATE_SOURCE_SCOPES',
                        'source_refs': [evidence(*ref) for ref in refs],
                        'verification_status': 'SOURCE_RELATION_NOT_EXACT_CLIENT_ENTITY_JOIN',
                        'rights_status': 'RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED',
                        'topic': topic, 'source_facts': facts, 'automatic_entity_model_or_field_merge_allowed': False,
                        'original_client_build_or_runtime_proven': False,
                        'unknown_color_face_sprite_or_creation_values': None})
    o = {'schema': 'stoneage.jp2003.creation_visual_reference_join.r1', 'date': '2026-10-19',
         'task': 'JP2003-CHARACTER-CREATION-VISUAL-REFERENCE-JOIN-01',
         'inputs': {k: {'path': str(ROOT / v[0]), 'sha256': v[1]} for k, v in INPUTS.items()},
         'records': records,
         'coverage': {'pinned_derived_reports': 3, 'distinct_original_text_bodies_referenced': 3,
                      'previously_reviewed_image_objects_referenced': 1, 'comparison_records': 5,
                      'existing_position_references_indexed': 12, 'new_original_requests_images_or_entities': 0},
         'boundaries': {'source_count_proves_independent_publishers': False,
                        'jss1999_tw10_cn182_174a_same_build_identity': False,
                        'stage_a': '7_PARTIAL_2_OPEN', 'stage_b_and_wiki': 'GATED', 'r79': 'PAUSED_NON_BLOCKING'},
         'next': 'OFFICIAL-VERSION-COVERAGE-MATERIAL-REVIEW-10'}
    validate_report(o)
    return o


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--output', required=True); args = parser.parse_args()
    o = build({k: (ROOT / v[0]).read_bytes() for k, v in INPUTS.items()})
    payload = json.dumps(o, ensure_ascii=False, sort_keys=True, indent=2) + '\n'
    p = Path(args.output); p.parent.mkdir(parents=True, exist_ok=True); p.write_text(payload, encoding='utf-8')
    print('FINITE_COMPARISONS=5 EXISTING_POSITION_REFERENCES=12 NEW_SOURCE_REQUESTS=0')
    print('DERIVED_SHA256=' + sha256(payload.encode()).hexdigest())


if __name__ == '__main__': main()
