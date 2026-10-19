"""Adversarial checks for practical misreadings of official feature prose."""
import json
from pathlib import Path
import unittest

from tools.stoneage_jp2003_game_features import HEADINGS, IMAGE_ROOT, REPORT, URL, build, derive, extract_rows, validate_contract


class GameFeaturesTests(unittest.TestCase):
    def reject(self, i, key, value, message):
        records = json.loads(REPORT.read_text())['records']
        records[i]['source_described_behavior'][key] = value
        with self.assertRaisesRegex(ValueError, message): validate_contract(records)

    def test_12_appearance_types_with_4_colors_not_48_distinct_bodies_or_stat_bonuses(self):
        self.reject(0, 'forty_eight_distinct_character_entities_or_models_proven', True, 'forty-eight')
        self.reject(0, 'type_and_color_change_parameters_described', True, 'Cosmetic')
        self.reject(0, 'appearance_names_colors_sprite_ids_or_ui_coordinates', {'body': 12}, 'Appearance mapping')

    def test_four_elements_not_four_simultaneous_allocations_or_imported_creation_points(self):
        self.reject(1, 'element_names_allocation_points_and_simultaneous_choices', {'points': 10}, 'Element choices')
        self.reject(1, 'face_part_ids_counts_or_static_illustration_identity', 'charapicillust1.gif', 'face-image')

    def test_group_five_players_not_five_followers_or_pets(self):
        self.reject(2, 'five_includes_pets_or_five_additional_followers_proven', True, 'Party count')
        self.reject(2, 'maximum_group_players_described', 6, 'Party count')

    def test_leader_field_movement_not_others_battle_commands_or_universal_leave_ack(self):
        self.reject(2, 'leader_controls_all_battle_commands_proven', True, 'leader or leave')
        self.reject(2, 'leave_during_every_runtime_state_or_packet_transaction_verified', True, 'leader or leave')

    def test_promotional_village_safety_not_all_tiles_or_events_no_battle(self):
        self.reject(3, 'every_village_tile_or_special_event_no_combat_proven', True, 'Promotional safety')
        self.reject(3, 'named_items_skill_list_recipes_or_safety_map_flags', {'safe_flag': 1}, 'Promotional safety')

    def test_encounter_dinosaurs_not_all_npcs_invisible_or_known_rng(self):
        self.reject(4, 'all_npcs_or_every_creature_invisible_proven', True, 'universal invisibility')
        self.reject(4, 'encounter_rate_rng_tables_full_command_list_or_help_turn_cost', {'rate': 0.1}, 'algorithms')

    def test_declared_image_dimensions_are_not_actual_pixels(self):
        records = json.loads(REPORT.read_text())['records']
        records[0]['unfetched_image_reference']['actual_capture_sha_dimensions_or_frames'] = {'size': [200, 150]}
        with self.assertRaisesRegex(ValueError, 'promoted to pixels'): validate_contract(records)

    def test_leaf_row_binding_does_not_use_comment_or_other_table_image(self):
        rows = ''.join('<tr><td><img src="' + IMAGE_ROOT + 'tokuchopic' + str(i+1) + '.gif" width="200" height="150"></td><td></td><td><div>' + h + '</div><div>synthetic-' + str(i) + '</div></td></tr>' for i,h in enumerate(HEADINGS))
        doc = '<table><tr><td><table>' + rows + '</table></td></tr></table>'
        self.assertEqual(extract_rows('<!--'+rows+'-->'+doc)[2]['body'], 'synthetic-2')
        for bad in [doc.replace('tokuchopic2.gif', 'tokuchopic3.gif'),
                    doc.replace('width="200"', 'width="201"'),
                    doc.replace('<div>synthetic-3</div>', ''), doc+rows]:
            with self.assertRaises(ValueError): extract_rows(bad)

    def test_changed_numeric_source_fragments_rejected(self):
        # Only synthetic fragments of the required propositions, no original body fixture.
        b = ['ビジュアルの選択 12種類のキャラクター それぞれ色違い4種類 タイプや色などでパラメータが変わるわけではない',
             '4つの属性 目と口 顔のグラフィック 名刺交換',
             'グループは最大5人 歩く時 戦闘する時 フィールド上を移動 リーダー 意志でいつでも自由に抜け',
             '村の中は安全 村の外 ペット 一緒に冒険 道具 知識や技能 協力',
             '恐竜の姿は、プレイヤーには見えません フィールドを歩いて 突然 戦闘画面に切り替わり アイコンをクリック 助けを求める']
        self.assertEqual(derive([{'body': t} for t in b])[2]['maximum_group_players_described'], 5)
        for i, a, z in [(0, '12種類', '13種類'), (0, '色違い4種類', '色違い48種類'),
                         (1, '4つの属性', '5つの属性'), (2, '最大5人', '最大6人')]:
            bad = list(b); bad[i] = bad[i].replace(a,z)
            with self.assertRaises(ValueError): derive([{'body': t} for t in bad])

    def test_exact_original_body_and_actual_capture_not_error_page(self):
        for url in [URL, URL.replace('20031214050618', '20031214053427'), URL.replace('hangame.co.jp', 'example.org')]:
            with self.assertRaises(ValueError): build(b'x'*17136, url)

    def test_archive_fields_and_unverified_runtime_are_preserved(self):
        o=json.loads(REPORT.read_text()); validate_contract(o['records'])
        c=json.loads(Path('research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json').read_text())['future_website']
        for r in o['records']:
            self.assertLessEqual(set(c['record_contract']['required']),r.keys())
            self.assertEqual(r['collection'],'tutorials')
            self.assertEqual(r['source_refs'][0]['actual_capture'],'20031214050618')
            self.assertFalse(r['unfetched_image_reference']['pixels_acquired_or_inspected'])
        o['records'][0]['original_client_build_or_server_runtime_verified']=True
        with self.assertRaisesRegex(ValueError,'original runtime'):validate_contract(o['records'])


if __name__ == '__main__': unittest.main()
