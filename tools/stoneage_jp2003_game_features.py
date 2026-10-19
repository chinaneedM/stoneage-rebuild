"""Five row-bound feature descriptions from one authenticated operator page.

Image references are metadata only; no pixels, script or game execution.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
from urllib.request import Request, urlopen

from tools.stoneage_early_content_probe import plain, require, integer

ORIGINAL = 'http://www.hangame.co.jp/publish/sa/game2.asp'
CAPTURE = '20031214050618'
URL = 'https://web.archive.org/web/' + CAPTURE + 'id_/' + ORIGINAL
SOURCE_SHA = '4e92ce95cfb836db9fd78f7b4f64905e60270202d1e2ea0b00cf56b79b6440b0'
REPORT = Path('research/recovered/STONEAGE-JP2003-GAME-FEATURES-R1.json')
HEADINGS = ['石器時代でエンジョイ・ライフ！', '様々なバリエーションが用意されたキャラクター',
            'みんなで協力「グループシステム」', '道具を活用しよう！',
            '初心者でも安心！？馴染みやすい戦闘システム！']
PINS = [(209, '711d424d6b68a52b7fad04222bb2d2841cbf654de1b2fe63dac1e6d08856b83e'),
        (165, 'b3c673a0c4b5c8d07c54c45a2a2509d86bc87723ca1500d02781262f7bfe5754'),
        (184, 'c3983b0ae91cde36b72879b9db75b3c5240fdb319aa50cc86e37fdc010504542'),
        (237, 'd3a96ee444c4ec20b15e1d9faa09d8d4260741b198b29013a7604d7aa89bb4b1'),
        (168, 'cc79557bc90f59497e95c005ecc88d7de97f32a1ae6a8080b10144b26131393d')]
IMAGE_ROOT = 'http://images.hangame.co.jp/_images/game/saj/'


def extract_rows(document):
    document = re.sub(r'<!--.*?-->', '', document, flags=re.S)
    document = re.sub(r'<(script|style)\b[^>]*>.*?</\1>', '', document, flags=re.I | re.S)
    rows = []
    for row in re.findall(r'<tr\b[^>]*>((?:(?!<tr\b).)*?)</tr>', document, re.I | re.S):
        if not re.search(r'<img\b[^>]*src=["\x27][^"\x27]*tokuchopic', row, re.I):
            continue
        cells = re.findall(r'<td\b[^>]*>(.*?)</td>', row, re.I | re.S)
        require(len(cells) == 3, 'Feature image and description must occupy same three-cell row')
        tags = re.findall(r'<img\b[^>]*>', cells[0], re.I)
        require(len(tags) == 1, 'One declared feature image per row required')
        attrs = dict(re.findall(r'([a-z]+)=["\x27]([^"\x27]*)["\x27]', tags[0], re.I))
        require(attrs.get('src') == IMAGE_ROOT + 'tokuchopic' + str(len(rows) + 1) + '.gif',
                'Feature image order or original URL changed')
        require((attrs.get('width'), attrs.get('height')) == ('200', '150'), 'Declared image dimensions changed')
        divs = re.findall(r'<div\b[^>]*>(.*?)</div>', cells[2], re.I | re.S)
        require(len(divs) == 2, 'Feature heading/body binding missing')
        rows.append({'heading': plain(divs[0]), 'body': plain(divs[1]), 'image_ref': attrs['src']})
    require([r['heading'] for r in rows] == HEADINGS, 'Five visible feature headings/order required')
    return rows


def derive(rows):
    require(len(rows) == 5, 'Five feature rows required')
    b = [r['body'] for r in rows]
    def mentions(i, *tokens):
        require(all(t in b[i] for t in tokens), 'Feature meaning changed: ' + str(i + 1))
    mentions(0, 'ビジュアルの選択', 'それぞれ色違い', 'タイプや色などでパラメータが変わるわけではない')
    types = integer(b[0], r'([0-9０-９]+)種類のキャラクター', 'character appearance types')
    colors = integer(b[0], r'色違い([0-9０-９]+)種類', 'colors per appearance')
    elements = integer(b[1], r'([0-9０-９]+)つの属性', 'element categories')
    people = integer(b[2], r'グループは最大([0-9０-９]+)人', 'party player limit')
    require((types, colors, elements, people) == (12, 4, 4, 5), 'Feature numerical descriptions changed')
    mentions(1, '目と口', '顔のグラフィック', '名刺交換')
    mentions(2, '歩く時', '戦闘する時', 'フィールド上を移動', 'リーダー', '意志でいつでも自由に抜け')
    mentions(3, '村の中は安全', '村の外', 'ペット', '一緒に冒険', '道具', '知識や技能', '協力')
    mentions(4, '恐竜の姿は、プレイヤーには見えません', 'フィールドを歩いて', '突然',
             '戦闘画面に切り替わり', 'アイコンをクリック', '助けを求める')
    return [
        {'appearance_types_described': types, 'colors_per_type_described': colors,
         'type_and_color_change_parameters_described': False,
         'forty_eight_distinct_character_entities_or_models_proven': False,
         'appearance_names_colors_sprite_ids_or_ui_coordinates': None},
        {'element_category_count_described': elements, 'eyes_and_mouth_customizable_described': True,
         'created_face_used_during_card_exchange_described': True,
         'element_names_allocation_points_and_simultaneous_choices': None,
         'face_part_ids_counts_or_static_illustration_identity': None},
        {'maximum_group_players_described': people, 'group_field_and_battle_participation_described': True,
         'field_movement_control_described': 'GROUP_LEADER',
         'voluntary_leave_anytime_as_source_prose': True,
         'leader_controls_all_battle_commands_proven': False,
         'five_includes_pets_or_five_additional_followers_proven': False,
         'leave_during_every_runtime_state_or_packet_transaction_verified': False},
        {'village_safety_and_outside_danger_as_promotional_description': True,
         'pet_or_party_adventure_recommended': True,
         'tools_knowledge_skills_and_cooperation_valued_described': True,
         'every_village_tile_or_special_event_no_combat_proven': False,
         'named_items_skill_list_recipes_or_safety_map_flags': None},
        {'encountering_dinosaurs_not_visible_before_field_encounter_described': True,
         'field_walking_can_switch_to_battle_screen_described': True,
         'command_action_icons_clicked_described': True,
         'in_battle_help_request_described': True,
         'all_npcs_or_every_creature_invisible_proven': False,
         'encounter_rate_rng_tables_full_command_list_or_help_turn_cost': None},
    ]


def validate_contract(records):
    require(len(records) == 5, 'Five source-qualified feature tutorials required')
    b = [r['source_described_behavior'] for r in records]
    require(b[0]['appearance_types_described'] == 12 and b[0]['colors_per_type_described'] == 4
            and b[0]['type_and_color_change_parameters_described'] is False
            and b[0]['forty_eight_distinct_character_entities_or_models_proven'] is False,
            'Cosmetic appearance dimensions promoted to stats or forty-eight entities')
    require(b[0]['appearance_names_colors_sprite_ids_or_ui_coordinates'] is None, 'Appearance mapping invented')
    require(b[1]['element_category_count_described'] == 4
            and b[1]['element_names_allocation_points_and_simultaneous_choices'] is None
            and b[1]['face_part_ids_counts_or_static_illustration_identity'] is None,
            'Element choices or face-image identity invented')
    require(b[2]['maximum_group_players_described'] == 5
            and b[2]['field_movement_control_described'] == 'GROUP_LEADER'
            and b[2]['five_includes_pets_or_five_additional_followers_proven'] is False
            and b[2]['leader_controls_all_battle_commands_proven'] is False
            and b[2]['leave_during_every_runtime_state_or_packet_transaction_verified'] is False,
            'Party count leader or leave prose generalized beyond context')
    require(b[3]['every_village_tile_or_special_event_no_combat_proven'] is False
            and b[3]['named_items_skill_list_recipes_or_safety_map_flags'] is None,
            'Promotional safety and tools promoted to map flags or recipes')
    require(b[4]['all_npcs_or_every_creature_invisible_proven'] is False
            and b[4]['encounter_rate_rng_tables_full_command_list_or_help_turn_cost'] is None,
            'Encounter context promoted to universal invisibility or algorithms')
    for r in records:
        image = r['unfetched_image_reference']
        require(image['actual_capture_sha_dimensions_or_frames'] is None
                and image['pixels_acquired_or_inspected'] is False, 'Declared image reference promoted to pixels')
        require(r['original_client_build_or_server_runtime_verified'] is False
                and r['original_game_ids_wire_fields_or_cross_version_binding'] is None,
                'Web feature description promoted to original runtime or identity')


def build(raw, final):
    require(final == URL, 'Exact feature original URL/capture required')
    require(len(raw) == 17136 and sha256(raw).hexdigest() == SOURCE_SHA, 'Feature body byte pin differs')
    doc = raw.decode('cp932', errors='strict'); rows = extract_rows(doc)
    require('<title>ストーンエイジ</title>' in doc.lower(), 'Actual operator page title missing')
    require([(len(r['body']), sha256(r['body'].encode()).hexdigest()) for r in rows] == PINS,
            'Feature body fingerprints differ')
    facts = derive(rows); records = []
    for i, (row, behavior) in enumerate(zip(rows, facts)):
        records.append({'record_id': f'jp2003-game-feature:{i+1:02d}', 'collection': 'tutorials',
                        'entity_type': 'OFFICIAL_GAME_FEATURE_DESCRIPTION', 'record_revision': 1,
                        'version_profile': 'JAPAN_HANGAME_WEB_20031214_NOT_EXACT_CLIENT_BUILD',
                        'source_refs': [{'source': ORIGINAL, 'actual_capture': CAPTURE, 'sha256': SOURCE_SHA,
                                         'row_index': i, 'normalized_body_sha256': PINS[i][1]}],
                        'heading_as_written': row['heading'], 'source_described_behavior': behavior,
                        'verification_status': 'OPERATOR_DESCRIPTION_NOT_ORIGINAL_GAME_EXECUTION',
                        'rights_status': 'RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED',
                        'unfetched_image_reference': {'original_url': row['image_ref'],
                                                     'html_declared_dimensions': [200, 150],
                                                     'actual_capture_sha_dimensions_or_frames': None,
                                                     'pixels_acquired_or_inspected': False},
                        'original_client_build_or_server_runtime_verified': False,
                        'original_game_ids_wire_fields_or_cross_version_binding': None})
    validate_contract(records)
    return {'schema': 'stoneage.jp2003.game_features.r1', 'date': '2026-10-19',
            'task': 'JP2003-OFFICIAL-GAME-FEATURES-SOURCE-01',
            'source': {'original_url': ORIGINAL, 'strict_replay_url': URL, 'actual_capture': CAPTURE,
                       'bytes': len(raw), 'sha256': SOURCE_SHA, 'encoding': 'CP932_STRICT',
                       'actual_title': 'ストーンエイジ', 'actual_visible_section': 'ゲームの特徴',
                       'entry_qualification_report': 'STONEAGE-JP2003-WORLD-PREMISE-R1.json',
                       'initial_requested_capture': '20031214053427',
                       'redirect_to_actual_capture_preserved': True},
            'section_fingerprints': [{'row_index': i, 'normalized_characters': n, 'sha256': h}
                                     for i, (n, h) in enumerate(PINS)],
            'records': records,
            'coverage': {'original_pages': 1, 'feature_tutorial_records': 5, 'image_references_only': 5,
                         'images_programs_linked_content_pages_acquired': 0,
                         'new_named_characters_npcs_species_maps_or_quests': 0},
            'boundaries': {'twelve_types_times_four_colors_is_forty_eight_original_entities': False,
                           'jss1999_tw10_cn182_or_174a_build_identity_proven': False,
                           'source_behavior_equals_original_server_execution': False,
                           'original_html_or_asset_bytes_in_git': False,
                           'stage_a': '7_PARTIAL_2_OPEN', 'stage_b_and_wiki': 'GATED', 'r79': 'PAUSED_NON_BLOCKING'},
            'next': 'JP2003-CHARACTER-CREATION-VISUAL-REFERENCE-JOIN-01'}


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--input'); parser.add_argument('--output', required=True)
    args = parser.parse_args()
    if args.input:
        raw, final = Path(args.input).read_bytes(), URL
    else:
        with urlopen(Request(URL, headers={'User-Agent': 'Mozilla/5.0 StoneAgeHistoricalEvidence'}), timeout=35) as response:
            raw, final = response.read(150001), response.url
    report = build(raw, final); payload = json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + '\n'
    path = Path(args.output); path.parent.mkdir(parents=True, exist_ok=True); path.write_text(payload, encoding='utf-8')
    print('SOURCE_SHA256=' + SOURCE_SHA); print('FEATURE_RECORDS=5 IMAGES_ACQUIRED=0')
    print('DERIVED_SHA256=' + sha256(payload.encode()).hexdigest())


if __name__ == '__main__': main()
