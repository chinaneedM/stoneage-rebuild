"""Source-bounded player status, knockout and level-up in a known JSS manual.

Keep row identities and context; prose is not an original server formula.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re

from tools.stoneage_early_content_probe import plain, require, section
from tools.stoneage_jss2001_mail_items_venues import ORIGINAL, CAPTURE, URL, SOURCE_SHA, acquire

REPORT = Path('research/recovered/STONEAGE-JSS2001-PLAYER-STATUS-LEVELUP-KNOCKOUT-R1.json')
ANCHORS = ('3040', '8020', '8060')
PINS = {
    '3040': (593, 'fc79e49c446fe2f1fa3e3fa5d9e3be60ada536738ef13c7809ea4edac4548ec3'),
    '8020': (143, '729ae5318221a018679051f6271f4fce9ec8157c8d0d7b3983ee09b805af2f99'),
    '8060': (154, '97f25718e99ce4dfe2e56cfe08dd47e35e1e6128de5134d4cd4f3389b61e5e53'),
}
LABELS = ('DP', '称号', 'レベル', '経験値', 'NEXT', '耐久力', '気力', '攻撃力',
          '防御力', '俊敏力', '魅力', '地属性', '水属性', '火属性', '風属性',
          '体力', '腕力', '丈夫さ', '素早さ')
PRIMARY = ['体力', '腕力', '丈夫さ', '素早さ']
ELEMENT_TARGETS = {'地属性': ['水', '風'], '水属性': ['火', '地'],
                   '火属性': ['風', '水'], '風属性': ['地', '火']}


def status_rows(document):
    start = re.search(r'<a\b[^>]*name="3040"[^>]*>', document, re.I)
    require(start is not None, 'Missing status section')
    tail = document[start.end():]
    end = re.search(r'<a\b[^>]*name="\d+"[^>]*>', tail, re.I)
    require(end is not None, 'Missing next anchor after status')
    tables = re.findall(r'<table\b[^>]*>(.*?)</table>', tail[:end.start()], re.I | re.S)
    require(len(tables) == 1, 'One status table required')
    rows = []
    for tr in re.findall(r'<tr\b[^>]*>(.*?)</tr>', tables[0], re.I | re.S):
        cells = [plain(c) for c in re.findall(r'<td\b[^>]*>(.*?)</td>', tr, re.I | re.S)]
        require(len(cells) == 2, 'Status row must bind one label to one description')
        rows.append(tuple(cells))
    require(tuple(label for label, _ in rows) == LABELS, 'Status row labels/order changed')
    return rows


def derive(parts, rows):
    require(tuple(parts) == ANCHORS, 'Exact three source sections required')
    require(tuple(label for label, _ in rows) == LABELS, 'Status row labels/order changed')
    descriptions = dict(rows)
    def row(label, *tokens):
        require(all(token in descriptions[label] for token in tokens), 'Row meaning changed: ' + label)
    def mentions(anchor, *tokens):
        require(all(token in parts[anchor] for token in tokens), 'Section meaning changed: ' + anchor)
    row('DP', 'レベルアップ時', 'プレイヤー同士の戦闘に勝利', '上昇')
    row('称号', '名前の後ろ', '[称号変更]')
    row('レベル', '総合的な強さ')
    row('経験値', 'ノックアウトさせたキャラクターおよびペットにのみ', '一定の数値でレベルアップ')
    row('NEXT', '次のレベルアップに必要な経験値')
    row('耐久力', 'ダメージ', '減ります', '0になると気絶')
    row('気力', '呪術', '下がります')
    row('攻撃力', '与えるダメージ'); row('防御力', '受けるダメージ')
    row('俊敏力', '攻撃の早さ', 'かわしやすさ')
    row('魅力', 'キャラクターとペットの関係')
    for label, targets in ELEMENT_TARGETS.items():
        row(label, targets[0] + 'と' + targets[1], '攻撃および防御に影響')
    for label, tokens in [('体力', ('耐久力', '関係')), ('腕力', ('攻撃力', '関係')),
                          ('丈夫さ', ('防御力', '関係')), ('素早さ', ('攻撃の早さ', 'かわしやすさ'))]:
        row(label, *tokens)
    mentions('3040', '[Ctrl]+[S]')
    mentions('8020', '体力が0', 'キャラクターおよびペット', '戦闘が終了すると、体力1',
             'ダメージによっては', 'セーブポイントまで戻されることも', '魅力が少し下がります', '忠誠度が下がります')
    mentions('8060', 'キャラクターがレベルアップ', *PRIMARY, 'ボーナスポイント', '[UP]',
             '魅力、デュエルポイント（DP）', '自動的に上昇')
    return [
        {
            'status_rows': [{'source_label': label, 'description_sha256': sha256(desc.encode()).hexdigest()}
                            for label, desc in rows],
            'status_window_shortcut': 'Ctrl+S',
            'title_change_button_described': True,
            'dp_increases_described_on': ['CHARACTER_LEVEL_UP', 'VICTORY_IN_PLAYER_VS_PLAYER_BATTLE'],
            'dp_change_amount_or_complete_award_algorithm': None,
            'exp_eligibility_source_statement': 'ONLY_CHARACTERS_AND_PETS_THAT_KNOCK_OUT_ENEMIES',
            'next_field_meaning': 'EXP_REQUIRED_FOR_NEXT_LEVEL',
            'exp_award_sharing_last_hit_formula_or_level_thresholds': None,
            'durability_damage_and_zero_knockout_described': True,
            'spirit_decreases_on_spell_use_described': True,
            'attack_and_defense_affect_damage_described': True,
            'agility_affects_attack_speed_and_evasion_described': True,
            'charm_mainly_affects_character_pet_relationship_described': True,
            'element_attack_defense_influence_targets': ELEMENT_TARGETS,
            'element_advantage_direction_or_coefficients': None,
            'primary_to_derived_relations': {'体力': ['耐久力'], '腕力': ['攻撃力'],
                                            '丈夫さ': ['防御力'], '素早さ': ['ATTACK_SPEED', 'EVASION']},
            'primary_equals_derived_stat_identity_proven': False,
            'stat_conversion_formula_or_wire_offsets': None,
            'knockout_term_boundary': '3040_USES_DURABILITY_8020_USES_VITALITY_WORDING_NO_WIRE_IDENTITY',
        },
        {
            'applies_to': ['CHARACTER', 'PET'],
            'zero_state_as_written': '体力が0',
            'after_battle_revival_value_as_written': 1,
            'revival_timing': 'AFTER_BATTLE_END',
            'return_to_savepoint': 'POSSIBLE_DEPENDING_ON_DAMAGE_AT_KNOCKOUT',
            'return_to_savepoint_is_unconditional': False,
            'player_knockout_consequence': 'CHARM_DECREASES_SLIGHTLY',
            'pet_knockout_consequence': 'LOYALTY_DECREASES',
            'charm_and_loyalty_are_same_field': False,
            'sp_return_threshold_charm_delta_loyalty_delta_or_operation_order': None,
            'exp_level_money_inventory_or_pet_loss_on_knockout': 'NOT_RESOLVED_BY_SELECTED_SOURCE',
        },
        {
            'subject': 'CHARACTER_LEVEL_UP',
            'bonus_points_obtained_described': True,
            'player_selectable_bonus_stats_as_written': PRIMARY,
            'control': 'STATUS_WINDOW_UP_BUTTON_FOR_CHOSEN_STAT',
            'automatic_increases_as_written': ['魅力', 'デュエルポイント（DP）'],
            'bonus_count_per_level_charm_delta_dp_delta_caps_or_respec': None,
            'pet_growth_distribution_inferred_from_character_bonus_ui': False,
            'element_allocation_inferred_from_character_bonus_ui': False,
        },
    ]


def validate_contract(records):
    require(len(records) == 3, 'Three source-qualified tutorial records required')
    s, k, u = [r['source_described_behavior'] for r in records]
    require(tuple(x['source_label'] for x in s['status_rows']) == LABELS, 'Status table row identity lost')
    require(s['exp_eligibility_source_statement'] == 'ONLY_CHARACTERS_AND_PETS_THAT_KNOCK_OUT_ENEMIES'
            and s['exp_award_sharing_last_hit_formula_or_level_thresholds'] is None, 'EXP prose promoted to server formula')
    require(s['element_attack_defense_influence_targets'] == ELEMENT_TARGETS
            and s['element_advantage_direction_or_coefficients'] is None, 'Element influence promoted to advantage or multiplier')
    require(s['primary_equals_derived_stat_identity_proven'] is False
            and s['stat_conversion_formula_or_wire_offsets'] is None, 'Primary and derived stats conflated')
    require(s['dp_increases_described_on'] == ['CHARACTER_LEVEL_UP', 'VICTORY_IN_PLAYER_VS_PLAYER_BATTLE']
            and s['dp_change_amount_or_complete_award_algorithm'] is None, 'DP triggers or amount changed')
    require(k['applies_to'] == ['CHARACTER', 'PET'] and k['after_battle_revival_value_as_written'] == 1
            and k['revival_timing'] == 'AFTER_BATTLE_END', 'Knockout subject or timing changed')
    require(k['return_to_savepoint'] == 'POSSIBLE_DEPENDING_ON_DAMAGE_AT_KNOCKOUT'
            and k['return_to_savepoint_is_unconditional'] is False, 'Conditional SP return generalized')
    require(k['player_knockout_consequence'] == 'CHARM_DECREASES_SLIGHTLY'
            and k['pet_knockout_consequence'] == 'LOYALTY_DECREASES'
            and k['charm_and_loyalty_are_same_field'] is False, 'Character charm and pet loyalty conflated')
    require(k['sp_return_threshold_charm_delta_loyalty_delta_or_operation_order'] is None
            and k['exp_level_money_inventory_or_pet_loss_on_knockout'] == 'NOT_RESOLVED_BY_SELECTED_SOURCE', 'Knockout loss/threshold invented')
    require(u['subject'] == 'CHARACTER_LEVEL_UP' and u['player_selectable_bonus_stats_as_written'] == PRIMARY
            and u['automatic_increases_as_written'] == ['魅力', 'デュエルポイント（DP）'], 'Manual and automatic level-up choices conflated')
    require(u['bonus_count_per_level_charm_delta_dp_delta_caps_or_respec'] is None
            and u['pet_growth_distribution_inferred_from_character_bonus_ui'] is False
            and u['element_allocation_inferred_from_character_bonus_ui'] is False, 'Character level-up generalized or values invented')
    for r in records:
        require(r['server_runtime_observed'] is False and r['original_ids_wire_fields_and_same_build_binding'] is None,
                'Source description promoted to runtime or original field identity')
        require(r['rights_status'] == 'RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED', 'Asset release rights invented')


def build(raw, final):
    require(final == URL, 'Exact manual original URL and capture required')
    require(len(raw) == 28434 and sha256(raw).hexdigest() == SOURCE_SHA, 'Authenticated manual bytes changed')
    document = raw.decode('shift_jis', errors='strict')
    parts = {anchor: section(document, anchor) for anchor in ANCHORS}
    for a, text in parts.items():
        require((len(text), sha256(text.encode()).hexdigest()) == PINS[a], 'Section fingerprint changed: ' + a)
    facts = derive(parts, status_rows(document))
    records = []
    for a, topic, behavior in zip(ANCHORS, ['PLAYER_STATUS', 'KNOCKOUT', 'CHARACTER_LEVEL_UP'], facts):
        records.append({
            'record_id': 'jss2001-manual:player-status:' + a,
            'entity_type': 'FIRST_PARTY_MANUAL_CHARACTER_RULE_DESCRIPTION', 'collection': 'tutorials',
            'record_revision': 1, 'version_profile': 'JSS_JAPAN_WEB_MANUAL_20010418',
            'source_refs': [{'source': ORIGINAL, 'actual_capture': CAPTURE, 'sha256': SOURCE_SHA,
                             'section_anchor': a, 'normalized_section_sha256': PINS[a][1]}],
            'verification_status': 'MANUAL_DESCRIPTION_NOT_SERVER_EXECUTION',
            'rights_status': 'RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED',
            'topic': topic, 'source_described_behavior': behavior,
            'server_runtime_observed': False, 'original_ids_wire_fields_and_same_build_binding': None,
        })
    validate_contract(records)
    return {
        'schema': 'stoneage.jss2001.player_status_levelup_knockout.r1', 'date': '2026-10-19',
        'task': 'JSS2001-PLAYER-STATUS-LEVELUP-AND-KNOCKOUT-01',
        'source': {'original_url': ORIGINAL, 'strict_replay_url': URL, 'actual_capture': CAPTURE,
                   'bytes': len(raw), 'sha256': SOURCE_SHA, 'encoding': 'SHIFT_JIS_STRICT',
                   'newly_discovered_source': False, 'newly_structured_sections': list(ANCHORS),
                   'previous_generic_fingerprint_catalog': 'research/recovered/JSS-LOGIN-MANUAL-CREATION-CONTRACT-R1.json',
                   'all_three_sections_already_generically_fingerprinted': True,
                   'new_material_is_behavior_semantics_not_first_fingerprint': True},
        'section_fingerprints': {a: {'normalized_characters': n, 'sha256': h} for a, (n, h) in PINS.items()},
        'records': records,
        'coverage': {'new_original_urls': 0, 'known_original_bodies_reacquired': 1,
                     'new_semantic_section_records': 3, 'status_table_labels': 19,
                     'new_images_programs_or_client_entities': 0},
        'boundaries': {'same_build_jss1999_tw10_cn182_proven': False,
                       'original_exp_damage_growth_or_element_formula_recovered': False,
                       'runtime_or_original_save_io_observed': False,
                       'unmentioned_knockout_losses_proven_absent': False,
                       'original_html_or_asset_bytes_in_git': False,
                       'stage_a': '7_PARTIAL_2_OPEN', 'stage_b_and_wiki': 'GATED', 'r79': 'PAUSED_NON_BLOCKING'},
        'next': 'JSS2001-PLAYER-PET-STATUS-AND-CREATION-BOUNDARY-01',
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input'); parser.add_argument('--output', required=True)
    args = parser.parse_args()
    raw, final = (Path(args.input).read_bytes(), URL) if args.input else acquire()
    report = build(raw, final)
    payload = json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + '\n'
    path = Path(args.output); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload, encoding='utf-8')
    print('SOURCE_SHA256=' + SOURCE_SHA)
    print('NEW_SEMANTIC_SECTIONS=3 STATUS_TABLE_LABELS=19 NEW_ORIGINAL_URLS=0')
    print('DERIVED_SHA256=' + sha256(payload.encode()).hexdigest())


if __name__ == '__main__':
    main()
