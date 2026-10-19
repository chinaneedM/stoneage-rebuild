"""Do not turn sequel narrative into gift deployment, mapped NPCs or copied rewards."""
import json
from pathlib import Path
import unittest
from tools.stoneage_wayi_newbie_riding_successor import INDEX_URL, URL, PLAN, REPORT, build, validate_report


class RidingSuccessorTests(unittest.TestCase):
    def reject(self,i,key,value,message):
        o=json.loads(REPORT.read_text());o['records'][i]['source_described_claims'][key]=value
        with self.assertRaisesRegex(ValueError,message):validate_report(o)

    def test_adult_and_riding_narrative_does_not_confirm_free_tiger_implementation(self):
        self.reject(0,'specific_free_tiger_plan_implementation_or_stats_confirmed',True,'implemented gift')

    def test_ore_researcher_role_not_personal_name_map_id_or_reward(self):
        self.reject(1,'personal_npc_name_ids_map_coordinates_or_reward',{'reward_levels':30},'canonical entity/reward')

    def test_generic_fishing_village_not_named_village_alias(self):
        self.reject(1,'fishing_village_equals_named_other_village_proven',True,'generic fishing village')

    def test_previous_courier_thirty_levels_not_ore_job_reward(self):
        self.reject(1,'same_job_as_previous_mammoth_courier',True,'courier reward')
        self.reject(1,'previous_thirty_level_claim_transferred_to_ore_job',True,'courier reward')

    def test_museum_anecdote_not_staff_account_or_universal_pvp_permission(self):
        self.reject(2,'staff_account_identity_or_universal_museum_pvp_rule_proven',True,'staff identity')

    def test_same_author_series_not_independent_implementation_witnesses(self):
        o=json.loads(REPORT.read_text());o['comparison_to_previous_plan']['same_author_series_is_independent_implementation_confirmation']=True
        with self.assertRaisesRegex(ValueError,'independent implementation'):validate_report(o)

    def test_previous_report_byte_pin_and_exact_sources_reject_changed_inputs(self):
        for index_url,body_url,prior in [(INDEX_URL,URL,PLAN.read_bytes()),
                                         (INDEX_URL,URL.replace('20051113145307','20031223000000'),PLAN.read_bytes()),
                                         (INDEX_URL,URL,PLAN.read_bytes()+b'\n')]:
            with self.assertRaises(ValueError):build(b'i'*28883,index_url,b'b'*19686,body_url,prior)

    def test_three_archive_records_and_explicit_unknowns_no_images_or_ids(self):
        o=json.loads(REPORT.read_text());validate_report(o)
        c=json.loads(Path('research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json').read_text())['future_website']['record_contract']['required']
        for r in o['records']:
            self.assertLessEqual(set(c),r.keys());self.assertIsNone(r['original_game_ids_or_same_build_binding'])
        self.assertEqual(o['records'][1]['collection'],'quests')
        self.assertFalse(o['source']['index_date_is_original_release_or_deployment_proven'])
        self.assertEqual(o['coverage']['images_programs_or_original_entity_ids'],0)


if __name__=='__main__':unittest.main()
