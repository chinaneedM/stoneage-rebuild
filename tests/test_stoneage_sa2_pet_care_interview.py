import copy
import json
import unittest
from tools.stoneage_sa2_pet_care_interview import REPORT, ROOT, STEM, validate


class SA2Care(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(REPORT.read_text())

    def reject(self, keys, value):
        r = copy.deepcopy(self.r)
        node = r
        for k in keys[:-1]:
            node = node[k]
        node[keys[-1]] = value
        with self.assertRaises(ValueError):
            validate(r)

    def test_eight_records_keep_product_and_speaker(self):
        validate(self.r)
        self.reject(['records', 0, 'version_profile'], 'TW10')
        self.reject(['records', 0, 'game_ids'], [2])
        self.reject(['records', 1, 'speaker'], '4Gamer')
        self.reject(['extracted', 'product_relation'], 'SA1_VERSION_2_UPDATE')

    def test_interview_plan_not_deployed_rules_or_publication_date(self):
        self.reject(['extracted', 'evidence_phase'], 'RELEASE_RUNTIME_VERIFIED')
        self.reject(['extracted', 'publication_date'], '2006-07-25')
        self.reject(['extracted', 'footer_is_interview_publication_date'], True)

    def test_ai_upbringing_not_recovered_hidden_formula(self):
        self.reject(['extracted', 'pet_ai', 'speaker'], '長田妙子')
        self.reject(['extracted', 'pet_ai', 'formula_or_hidden_parameter_names'], {'affection': 100})

    def test_den_size_and_parent_qualities_not_complete_tables(self):
        self.reject(['extracted', 'den', 'larger_rooms_allow_more_pets'], False)
        self.reject(['extracted', 'den', 'room_size_to_capacity_table'], {10: 15})
        self.reject(['extracted', 'breeding', 'exact_inheritance_compatibility_cost_time'], 'MEAN_OF_PARENTS')

    def test_pet_skills_not_absence_of_player_actions(self):
        self.reject(['extracted', 'skills', 'learner_reported'], 'PLAYER_CHARACTER')
        self.reject(['extracted', 'skills', 'skill_roster_or_player_has_no_actions_proven'], True)

    def test_types_vs_individuals_and_approximate_capacity(self):
        self.reject(['extracted', 'capacity', 'den_unit_as_written'], '匹')
        self.reject(['extracted', 'capacity', 'combined_unit_as_written'], '匹固定')
        self.reject(['extracted', 'capacity', 'types_to_individual_slots_equivalence_proven'], True)
        self.reject(['extracted', 'capacity', 'exact_species_total'], 20)

    def test_lifespan_rebirth_runaway_unknowns(self):
        self.reject(['extracted', 'lifespan_rebirth', 'exact_duration_clock_cost_and_preserved_state'], {'lifespan_days': 30})
        self.reject(['extracted', 'runaway', 'threshold_probability_and_return_rules'], {'guaranteed_return': True})
        self.reject(['extracted', 'lifespan_rebirth', 'revival_through_rebirth_reported_possible'], False)

    def test_external_email_and_stated_intent_not_project_sending(self):
        self.reject(['extracted', 'notification', 'channel_reported'], 'IN_GAME_MAIL')
        self.reject(['extracted', 'notification', 'delay_content_delivery_guarantee_or_consent_rules'], {'delay_days': 7})
        self.reject(['extracted', 'notification', 'message_sent_by_project'], True)

    def test_sixteen_real_source_changes_and_outer_positive(self):
        r = json.loads((ROOT / ('research/recovered/' + STEM + '-LOCAL-REPLAY-R1.json')).read_text())
        self.assertEqual(r['extracted']['speaker_turn_count'], 29)
        cases = r['audit']['real_source_mutations']
        self.assertEqual(len(cases), 16)
        self.assertEqual(len({x['input_sha256'] for x in cases}), 16)
        self.assertTrue(all(x['rejected_without_digest_gate'] for x in cases))
        self.assertTrue(r['audit']['outer_script_positive'])
        self.assertFalse(r['message_sent'])
        self.assertEqual(r['extracted'], self.r['extracted'])

    def test_source_authority_historical_bytes_and_stage_gates(self):
        self.reject(['source', 'authority'], 'ORIGINAL_SERVER_EXECUTED')
        self.reject(['source', 'authenticated_historical_original_bytes'], True)
        for key in self.r['unproven']:
            with self.subTest(key=key):
                self.reject(['unproven', key], True)
        self.reject(['status', 'stage_b_wiki'], 'OPEN')
        self.reject(['next'], 'EXPAND_SA2_HELPERS')

    def test_later_report_links_recording_month_without_publication_day(self):
        self.reject(['recording_context', 'recorded_month_reported'], '2006-07')
        self.reject(['recording_context', 'exact_interview_publication_date'], '2006-02-14')
        r = json.loads((ROOT / ('research/recovered/' + STEM + '-LOCAL-REPLAY-R1.json')).read_text())
        cases = r['context_audit']['real_source_mutations']
        self.assertEqual(len(cases), 3)
        self.assertTrue(all(x['rejected_without_digest_gate'] for x in cases))
        self.assertTrue(r['context_audit']['outer_script_positive'])


if __name__ == '__main__':
    unittest.main()
