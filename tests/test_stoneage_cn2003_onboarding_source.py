import copy
import json
import unittest
from tools import stoneage_cn2003_onboarding_source as m


class OnboardingSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(m.REPORT.read_text())
        cls.local = json.loads((m.ROOT / ('research/recovered/' + m.STEM + '-LOCAL-REPLAY-R1.json')).read_text())

    def reject(self, keys, value):
        r = copy.deepcopy(self.r)
        node = r
        for key in keys[:-1]:
            node = node[key]
        node[keys[-1]] = value
        with self.assertRaises(ValueError):
            m.validate(r)

    def test_seven_attributed_records_and_current_source_pins(self):
        m.validate(self.r)
        self.assertEqual([r['source_refs'] for r in self.r['records']], [['S1']]*5 + [['S2'], ['S1']])
        self.reject(['records', 1, 'game_ids'], [100])
        self.reject(['records', 0, 'version_profile'], 'TW10')
        self.reject(['records', 0, 'runtime_verified'], True)

    def test_hosted_guide_is_not_authenticated_official_manual(self):
        self.reject(['sources', 0, 'authority'], 'AUTHENTICATED_OFFICIAL_MANUAL')
        self.reject(['sources', 0, 'displayed_publication'], '2006-10-09 22:51:58')
        self.reject(['sources', 0, 'authenticated_original_bytes'], True)
        self.reject(['extracted', 'guide', 'submission_link_proves_user_authorship'], True)
        self.assertTrue(self.local['audit']['regeneration_comment_positive'])

    def test_source_order_does_not_invent_executed_login_transitions(self):
        self.assertEqual(self.r['extracted']['guide']['entry']['launcher_label'], 'Deeplay')
        self.reject(['extracted', 'guide', 'entry', 'returning_character_view_is_editorial_insertion'], False)
        self.reject(['extracted', 'guide', 'entry', 'fully_executed_login_state_machine'], True)

    def test_roster_keeps_paired_colors_not_independent_cartesian_choices(self):
        self.assertEqual(self.r['extracted']['guide']['roster']['character_types_as_reported'], 12)
        self.assertEqual(self.r['extracted']['guide']['roster']['paired_hair_clothes_color_choices_as_reported'], 4)
        self.reject(['extracted', 'guide', 'roster', 'independent_hair_times_clothes_choices'], 16)

    def test_name_and_literal_experience_do_not_become_encoding_or_stat_rule(self):
        self.assertEqual(self.r['extracted']['guide']['creation']['name_limit_unit_as_written'], '字符')
        self.assertEqual(self.r['extracted']['guide']['creation']['allocation_term_as_written'], '经验值')
        self.reject(['extracted', 'guide', 'creation', 'encoding_byte_limit_or_chinese_character_count'], 8)
        self.reject(['extracted', 'guide', 'creation', 'runtime_exp_or_stat_point_semantics'], 'STAT_POINTS')
        self.reject(['extracted', 'guide', 'creation', 'speed_vitality_advice_is_editorial_not_optimal_build'], False)

    def test_pet_names_do_not_supply_ids_or_birth_skill_roster(self):
        self.assertEqual(self.r['extracted']['guide']['starter_pets']['labels_as_written'], ['乌力乌力', '凯比', '克克尔', '威伯'])
        self.reject(['extracted', 'guide', 'starter_pets', 'skills_ids_names_stats_or_first_release_proven'], ['攻击'])
        self.reject(['extracted', 'guide', 'starter_pets', 'labels_as_written', 0], '乌力')

    def test_newcomer_exit_is_source_report_not_runtime_warp_or_global_level_cap(self):
        self.assertEqual(self.r['extracted']['guide']['newcomer']['destination_label_as_written'], '萨姆吉尔村')
        self.reject(['extracted', 'guide', 'newcomer', 'reentry_disallowed_as_reported'], False)
        self.reject(['extracted', 'guide', 'newcomer', 'actual_warp_id_coordinates_or_execution'], [1000, 1, 1])
        self.reject(['extracted', 'guide', 'newcomer', 'wording_about_levels_not_treated_as_global_level_cap'], False)

    def test_rollout_notice_does_not_authenticate_guide_or_all_server_execution(self):
        self.assertEqual(self.r['extracted']['notice']['announced_first_date'], '2003-06-10')
        self.assertEqual(self.r['extracted']['notice']['announced_first_group'], '中国网通9')
        for k in ['actual_rollout_or_all_groups_complete_proven', 'authenticates_guide_or_current_image_build', 'guide_may30_date_proves_live_deployment']:
            self.reject(['extracted', 'notice', k], True)

    def test_five_transparent_objects_are_not_five_extra_screens(self):
        self.assertEqual(sum(im['role'] == 'CONTENT_IMAGE' for im in self.r['images']), 5)
        blanks = [im for im in self.r['images'] if im['role'] == 'TRANSPARENT_PLACEHOLDER']
        self.assertEqual(len(blanks), 5)
        self.assertTrue(all(im['bytes'] == 73 and im['local_full_alpha_extrema'] == [0, 0] for im in blanks))
        self.reject(['images', 1, 'role'], 'CONTENT_IMAGE')
        self.reject(['images', 0, 'native_client_resolution_proven'], True)
        self.reject(['images', 0, 'exact_build_proven'], True)
        with self.assertRaises(ValueError):
            m.gif_structure(b'GIF89a')

    def test_twenty_actual_source_mutations_and_three_wrapper_positives(self):
        cases = self.local['audit']['real_source_mutations']
        self.assertEqual(len(cases), 20)
        self.assertEqual(len({x['input_sha256'] for x in cases}), 20)
        self.assertTrue(all(x['rejected_without_digest_gate'] for x in cases))
        self.assertEqual(self.local['audit']['outer_script_positives'], 2)
        self.assertTrue(self.local['audit']['regeneration_comment_positive'])
        for k in self.r['unproven']:
            self.reject(['unproven', k], True)
        self.reject(['status', 'stage_b_wiki'], 'OPEN')
        self.reject(['next'], 'EXPAND_FULL_GUIDE_HELPERS')


if __name__ == '__main__':
    unittest.main()
