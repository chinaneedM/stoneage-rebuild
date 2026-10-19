"""Adversarial documentary gates for a profession-access proposal."""
import json
from pathlib import Path
import unittest
from tools.stoneage_wayi_profession_access_plan import REPORT, URL, INDEX_URL, build, validate_report


class ProfessionAccessPlanTests(unittest.TestCase):
    def reject(self, i, key, value, message):
        o=json.loads(REPORT.read_text());o['records'][i]['source_described_claims'][key]=value
        with self.assertRaisesRegex(ValueError,message):validate_report(o)

    def test_entry_change_remains_plan(self):
        self.reject(2,'status','DEPLOYED_SERVER_RULE','Entry proposal')
        self.reject(2,'unreincarnated_entry_is_caption_and_plan_not_deployment',False,'Entry proposal')

    def test_eighty_level_rite_not_level_alone_or_imported_script(self):
        self.reject(2,'current_level_gte_80_alone_is_sufficient_proven',True,'level-only')
        self.reject(2,'original_ceremony_quest_script_ids_rewards_or_exact_comparator',{'required_level':80},'quest rule')
        self.reject(2,'proposed_entry_condition_as_written','一轉成人禮','Entry proposal')

    def test_second_tier_not_level_two_or_two_skills(self):
        self.reject(3,'tier_is_character_level_2_or_two_skills',True,'Skill-tier')
        self.reject(3,'skill_tier_as_written','角色等級二','Skill-tier')

    def test_entry_and_later_learning_are_separate(self):
        self.reject(3,'all_profession_access_still_requires_reincarnation',True,'entry gate')
        self.reject(3,'learning_condition_as_written','八十級成人禮','Skill-tier')

    def test_no_later_guide_profession_list_skill_costs_or_tree(self):
        self.reject(3,'profession_names_skill_names_ids_costs_or_tree',['法師','戰士','獵人'],'imported class list')

    def test_operator_motive_not_numeric_economy(self):
        self.reject(1,'easier_training_and_earning_exact_rates',{'exp_multiplier':2},'numeric progression')

    def test_framing_and_future_discussion_not_live_content(self):
        self.reject(0,'airline_scene_is_verified_transport_or_npc',True,'Column frame')
        self.reject(4,'content_or_release_implemented_proven',True,'Future nostalgia')

    def test_three_dates_not_deployment_and_reference_not_pixels(self):
        o=json.loads(REPORT.read_text());o['source']['index_date_is_verified_body_release_or_deployment']=True
        with self.assertRaisesRegex(ValueError,'Index date'):validate_report(o)
        o=json.loads(REPORT.read_text());o['unacquired_image_refs'][1]['sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'actual pixels'):validate_report(o)
        o=json.loads(REPORT.read_text());o['unacquired_image_refs'][1]['actual_dimensions']=[300,225]
        with self.assertRaisesRegex(ValueError,'actual pixels'):validate_report(o)

    def test_error_bytes_and_capture_mismatch_rejected(self):
        for index_url,body_url in [(INDEX_URL,URL),(INDEX_URL,URL.replace('20041206141244','20031114000000'))]:
            with self.assertRaises(ValueError):build(b'i'*28883,index_url,b'b'*17678,body_url)

    def test_archive_fields_and_no_original_entities_or_execution(self):
        o=json.loads(REPORT.read_text());validate_report(o)
        required=json.loads(Path('research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json').read_text())['future_website']['record_contract']['required']
        for r in o['records']:
            self.assertLessEqual(set(required),r.keys());self.assertIn(r['collection'],['sources','tutorials'])
            self.assertIsNone(r['original_game_ids_or_same_build_binding'])
        self.assertEqual(o['coverage']['original_npc_quest_skill_or_profession_entities_restored'],0)
        o['records'][3]['actual_server_rule_or_execution_verified']=True
        with self.assertRaisesRegex(ValueError,'original execution'):validate_report(o)
        o=json.loads(REPORT.read_text());o['coverage']['original_npc_quest_skill_or_profession_entities_restored']=5
        with self.assertRaisesRegex(ValueError,'restored original classes'):validate_report(o)


if __name__=='__main__':unittest.main()
