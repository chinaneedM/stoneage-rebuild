"""Adversarial guards for cross-source novice and pet-care comparisons."""
import json
from pathlib import Path
import unittest
from tools.stoneage_early_newcomer_pet_care_boundaries import INPUTS,ROOT,REPORT,build,pointer,validate_report


class EarlyNewcomerPetCareTests(unittest.TestCase):
    def report(self):return json.loads(REPORT.read_text())

    def reject(self,i,key,value,message):
        o=self.report();o['records'][i]['bounded_comparison'][key]=value
        with self.assertRaisesRegex(ValueError,message):validate_report(o)

    def test_twenty_creation_points_not_compulsory_endurance_or_per_level_bonus(self):
        self.reject(0,'same_number_proves_mandatory_allocation_or_stat_identity',True,'twenty points')
        self.reject(1,'creation_twenty_is_per_level_bonus',True,'level-up formula')
        self.reject(1,'cross_language_primary_to_derived_mapping_or_points_per_level',{'耐力':'体力'},'language labels')

    def test_pet_and_owner_levelup_are_different_subjects_without_proven_patch(self):
        self.reject(2,'cn_levelup_subject','OWNER','Pet versus owner')
        self.reject(2,'jss_levelup_example_subject','PET','Pet versus owner')
        self.reject(2,'different_subjects_prove_patch_or_exhaustive_contradiction',True,'proven patch')
        self.reject(2,'sum_or_shared_loyalty_formula',{'gain':1},'conflated')
        self.reject(2,'jss_loyalty_increase_examples',['PET_LEVEL_UP'],'Pet versus owner')

    def test_charm_not_pet_loyalty_and_100_not_cross_version_cap(self):
        self.reject(3,'owner_charm_and_pet_loyalty_are_same_field',True,'Charm and loyalty')
        self.reject(3,'cn_cosmetic_target_100_is_jss_cap_or_gain',True,'cosmetic target')

    def test_jss_capture_numbers_not_cn_rules_or_lifetime_cap(self):
        self.reject(4,'cn_numeric_capture_gap_or_loyalty_value',{'gap':6,'loyalty':60},'eligibility')
        self.reject(4,'jss_initial_60_is_lifetime_cap_or_cn_rule',True,'initial bound')

    def test_charm_outcomes_not_stacked_or_omission_based_absence(self):
        self.reject(5,'stacked_minus_five_refund_three_or_jss_numeric_delta_proven',True,'numeric transaction')
        self.reject(5,'jss_rescue_omission_proves_no_rescue_feature',True,'absence')

    def test_defense_and_early_party_not_death_or_xp_formula(self):
        self.reject(6,'cn_defense40_level20_is_death_save_threshold',True,'death threshold')
        self.reject(6,'unmentioned_exp_money_inventory_or_pet_loss_proven_absent',True,'absent loss')
        self.reject(7,'fixed_party_xp_schedule_or_cn_table_filled',True,'fixed XP schedule')

    def test_exact_git_inputs_pointers_and_reproducible_full_report(self):
        raws={k:(ROOT/name).read_bytes() for k,(name,_) in INPUTS.items()}
        self.assertEqual(build(raws),self.report())
        broken=dict(raws);broken['cn']=b'{}'
        with self.assertRaisesRegex(ValueError,'Pinned Git input'):build(broken)
        for r in self.report()['records']:
            for ref in r['source_refs']:self.assertIsNotNone(pointer(json.loads(Path(ref['path']).read_bytes()),ref['json_pointer']))

    def test_shared_original_not_four_sources_and_no_version_promotion(self):
        o=self.report();o['source_accounting']['four_reports_are_four_independent_originals']=True
        with self.assertRaisesRegex(ValueError,'independent original'):validate_report(o)
        o=self.report();o['records'][0]['cross_version_rule_transfer_allowed']=True
        with self.assertRaisesRegex(ValueError,'cross-version rule'):validate_report(o)
        o=self.report();validate_report(o)
        required=json.loads(Path('research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json').read_text())['future_website']['record_contract']['required']
        for r in o['records']:self.assertLessEqual(set(required),r.keys())
        self.assertEqual(o['source_accounting']['original_bodies_reacquired_in_this_job'],0)
        o['source_accounting']['original_bodies_reacquired_in_this_job']=3
        with self.assertRaisesRegex(ValueError,'Offline comparison'):validate_report(o)


if __name__=='__main__':unittest.main()
