import copy
import json
import unittest
from tools.stoneage_cn20_riding_source import REPORT,extract_nav,extract_body,replay,validate


class RidingSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.report=json.loads(REPORT.read_text())
    def rejects(self,mutate):
        r=copy.deepcopy(self.report);mutate(r)
        with self.assertRaises(ValueError):validate(r)
    def test_archive_contract_and_named_route(self):
        validate(self.report)
        c=json.loads((REPORT.parent/'STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json').read_text())['future_website']
        for row in self.report['records']:
            self.assertTrue(set(c['record_contract']['required'])<=row.keys());self.assertIn(row['collection'],c['required_collections'])
        self.assertEqual(len({r['record_id'] for r in self.report['records']}),5)
    def test_navigation_uses_real_text_label_and_link_not_guessed_path(self):
        s='<title>石器时代2.0</title><a href="/ZHUANQU/stoneage2/pet/qdragon.asp">骑乘宠物</a>'.encode('gb18030')
        self.assertEqual(extract_nav(s),self.report['inputs'][0]['extracted'])
        for bad in [s.replace(b'qdragon',b'ride'),s+s,s.replace('骑乘宠物'.encode('gb18030'),b'other')]:
            with self.assertRaises(ValueError):extract_nav(bad)
    def test_actual_captures_are_not_the_initial_requested_timestamps(self):
        self.assertEqual(self.report['inputs'][1]['capture_timestamp'],'20011204195948')
        self.assertNotEqual(self.report['inputs'][1]['http']['url'],self.report['inputs'][1]['replay_url'])
        self.assertEqual(self.report['inputs'][2]['capture_timestamp'],'20020402014049')
        self.rejects(lambda r:r['records'][4].__setitem__('same_build_as_2001_text',True))
    def test_five_stage_service_flow_human_training_and_loyalty(self):
        f=self.report['records'][1]['facts'];self.assertEqual(len(f['flow']),5);self.assertEqual(f['loyalty_label'],100)
        self.assertEqual(f['courses_as_written'],['下级','中级','上级']);self.assertEqual(f['training_target'],'HUMAN_NOT_PET')
        self.assertTrue(f['replacement_pet_retraining_not_required_reported'])
        self.rejects(lambda r:r['boundaries'].__setitem__('training_is_pet_skill_slot',True))
    def test_access_fees_level_caps_and_compatibility_are_not_invented(self):
        for row,key,value in [(0,'coordinates',[1,2]),(0,'family_membership_requirement',False),(2,'tuition_amounts',[100,200,300]),(2,'course_level_ranges',[30,60,100]),(2,'character_species_map',{'1':'金虎'}),(2,'simultaneously_learnable_mount_count',2)]:
            with self.subTest(key=key):self.rejects(lambda r:r['records'][row].__setitem__(key,value))
    def test_melee_and_ranged_use_different_documentary_attribute_sources(self):
        f=self.report['records'][1]['facts'];self.assertEqual([f[k] for k in ('melee_attack','ranged_attack','melee_initiation','ranged_initiation')],['PET_ATTACK','HUMAN_ATTACK','PET_AGILITY','HUMAN_AGILITY'])
        self.assertEqual(f['life_force'],'SUM_OF_HUMAN_AND_PET_SOURCE_TERM')
    def test_proportional_and_between_do_not_supply_exact_formula(self):
        for key,val in [('damage_weights',[0.5,0.5]),('rounding','FLOOR'),('defense_weights',[0.5,0.5]),('life_force_current_or_max','MAX_HP'),('element_formula','USE_PET')]:
            self.rejects(lambda r:r['records'][3].__setitem__(key,val))
        for key in ('proportional_damage_means_half_each','between_means_arithmetic_mean','source_life_force_proves_current_or_max_hp'):
            self.rejects(lambda r:r['boundaries'].__setitem__(key,True))
    def test_missing_body_or_partial_inputs_rejected(self):
        with self.assertRaises(ValueError):extract_body('<title>石器时代2.0</title>骑宠'.encode('gb18030'))
        with self.assertRaises(ValueError):replay(self.report,[b'',b''])
        with self.assertRaises(ValueError):replay(self.report,[b'',b'',b''])
    def test_visual_and_runtime_rights_promotion_rejected(self):
        self.rejects(lambda r:r['records'][4].__setitem__('original_sprite_binding',123))
        self.rejects(lambda r:r['records'][0].__setitem__('rights_status','RELEASE_APPROVED'))
        for key,value in [('original_server_execution_verified',True),('exact_client_build','2.0.exe'),('tw10_or_jss1999_backfill',True)]:
            self.rejects(lambda r:r['boundaries'].__setitem__(key,value))

    def test_downloaded_candidate_and_main_replay_custody(self):
        from hashlib import sha256,sha1
        c=json.loads((REPORT.parent/'STONEAGE-CN20-RIDING-CUSTODY-R1.json').read_text())
        self.assertEqual([len(c['runs'][k]) for k in ('candidate','main')],[10,11])
        for rows in c['runs'].values():
            self.assertTrue(all(r['head_sha']==c['content_head'] and r['conclusion']=='success' for r in rows))
        for pin in c['pins']:
            b=(REPORT.parents[2]/pin['path']).read_bytes();self.assertEqual(len(b),pin['bytes']);self.assertEqual(sha256(b).hexdigest(),pin['sha256']);self.assertEqual(sha1(b'blob '+str(len(b)).encode()+bytes([0])+b).hexdigest(),pin['git_blob'])
        self.assertEqual(c['artifacts'][0]['member_sha256'],c['artifacts'][1]['member_sha256'])
        self.assertFalse(c['raw_sources_committed']);self.assertFalse(c['original_server_execution_verified'])


if __name__=='__main__':unittest.main()
