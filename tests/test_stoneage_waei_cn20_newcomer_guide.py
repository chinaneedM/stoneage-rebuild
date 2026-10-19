"""Prevent a hosted beginner guide from becoming fabricated original rules."""
import json
from pathlib import Path
import unittest
from tools.stoneage_waei_cn20_newcomer_guide import REPORT, URL, ENTRY_REPORT, build, validate_report


class NewcomerGuideTests(unittest.TestCase):
    def report(self):return json.loads(REPORT.read_text())

    def reject(self,i,key,value,message):
        o=self.report();o['records'][i]['source_described_claims'][key]=value
        with self.assertRaisesRegex(ValueError,message):validate_report(o)

    def test_official_host_does_not_establish_operator_authorship(self):
        o=self.report();o['source']['operator_authored_or_independently_runtime_verified']=True
        with self.assertRaisesRegex(ValueError,'Official hosting'):validate_report(o)

    def test_first_pet_not_fixed_species_or_riding_achievement(self):
        self.reject(0,'first_following_pet_species_ids_or_universal_starter_table',{'species':1001},'First pet')
        self.reject(0,'first_pet_care_is_source_narrative_not_riding_achievement',False,'first mount')

    def test_approximate_level_three_and_possible_meat_not_guarantees(self):
        self.reject(1,'exact_battle_count_exp_or_guaranteed_outcome',{'battles':3},'Approximate early level')
        self.reject(2,'meat_drop_is_possible_not_guaranteed',False,'Meat typo')
        self.reject(2,'actual_drop_rate_heal_value_prices_or_item_ids',{'drop_rate':1},'exact rule')

    def test_source_typo_preserved_without_silent_certainty(self):
        self.reject(2,'blood_use_phrase_as_written','补自己的血','Meat typo')
        self.reject(2,'read_as_healing_is_editorial_interpretation','FACT','Meat typo')

    def test_free_clinic_not_known_threshold_or_named_npc(self):
        self.reject(3,'free_treatment_level_threshold_or_universal_price',{'free_through_level':10},'numeric threshold')
        self.reject(3,'nurse_is_named_npc_or_recovered_quest',True,'named NPC')

    def test_all_endurance_and_weapon_attack_remain_advice(self):
        self.reject(4,'status','MANDATORY_GAME_RULE','Allocation advice')
        self.reject(4,'mandatory_creation_allocation_or_only_attack_source',True,'compulsory build')
        self.reject(4,'later_levelup_points_per_level_or_stat_formula',3,'formula')
        self.reject(5,'party_size_matchmaking_or_combo_formula',{'capacity':5},'unsupported capacity')

    def test_minus_four_and_minus_one_not_minus_five_or_three_refund(self):
        self.reject(6,'knockout_charm_change_as_written',-5,'Charm comparison')
        self.reject(6,'both_penalties_stack_or_three_point_refund_proven',True,'stacked penalty')
        self.reject(6,'cosmetic_level_price_formula_or_runtime_timing',{'refund':3},'fee algorithm')

    def test_pet_advice_not_other_source_capture_gap_or_loyalty_cap(self):
        self.reject(7,'levelup_loyalty_gain_cap_capture_gap_or_probability',{'capture_gap':6,'loyalty_cap':60},'Qualitative pet advice')

    def test_defense_warning_not_forced_reset_or_map_alias(self):
        self.reject(8,'mandatory_reset_or_verified_death_save_transaction',True,'forced reset')
        self.reject(8,'map_ids_coordinates_or_confirmed_aliases',{'沙母岛':'沙姆岛'},'map identity')

    def test_cost_token_and_destination_not_charm_gain_cap_or_safe_handoff(self):
        self.reject(9,'charm_gain_plus_100_or_universal_cap_100',True,'Charm destination')
        self.reject(9,'unconditional_fixed_fee_or_safe_transfer_implemented',True,'guaranteed transfer')
        self.reject(9,'cost_token_as_written','2000元固定费用','fee')

    def test_reference_not_pixels_and_story_sequence_not_quest_graph(self):
        o=self.report();o['unacquired_image_refs'][0]['actual_dimensions']=[240,180]
        with self.assertRaisesRegex(ValueError,'actual pixels'):validate_report(o)
        o=self.report();o['narrative_sequence']['is_quest_dependency_or_mandatory_tutorial_graph']=True
        with self.assertRaisesRegex(ValueError,'quest dependency graph'):validate_report(o)

    def test_exact_entry_bytes_capture_and_error_body_rejected(self):
        for entry,final in [(b'{}',URL),(ENTRY_REPORT.read_bytes(),URL),(ENTRY_REPORT.read_bytes(),URL.replace('20011204212409','20020201000000'))]:
            with self.assertRaises(ValueError):build(entry,b'x'*65653,final)

    def test_required_archive_fields_and_no_original_execution(self):
        o=self.report();validate_report(o)
        required=json.loads(Path('research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json').read_text())['future_website']['record_contract']['required']
        for r in o['records']:
            self.assertLessEqual(set(required),r.keys());self.assertEqual(r['collection'],'tutorials')
        self.assertFalse(o['entry_provenance']['original_entry_page_reacquired_by_this_job'])
        o['records'][0]['actual_server_rule_or_execution_verified']=True
        with self.assertRaisesRegex(ValueError,'original execution'):validate_report(o)


if __name__=='__main__':unittest.main()
