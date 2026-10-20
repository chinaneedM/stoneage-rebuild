import copy
import json
import struct
import unittest
from tools.stoneage_jp2008_pet_evolution_source import REPORT,PETS,MASKS,COMPONENTS,extract_media,extract_official,image_metadata,replay,validate

class PetEvolutionSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.report=json.loads(REPORT.read_text())
    def rejects(self,fn):
        r=copy.deepcopy(self.report);fn(r)
        with self.assertRaises(ValueError):validate(r)
    def test_fifteen_records_follow_archive_without_original_entity_ids(self):
        validate(self.report);c=json.loads((REPORT.parent/'STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json').read_text())['future_website']
        self.assertEqual(len({x['record_id'] for x in self.report['records']}),15)
        for x in self.report['records']:
            self.assertTrue(set(c['record_contract']['required'])<=x.keys());self.assertIn(x['collection'],c['required_collections']);self.assertIsNone(x['game_ids'])
    def test_first_batch_labels_and_official_question_marks_are_not_unmasked(self):
        self.assertEqual([x['before_label'] for x in self.report['records'][:4]],PETS);self.assertEqual([x['evolved_mask'] for x in self.report['records'][:4]],MASKS)
        self.rejects(lambda r:r['records'][0].__setitem__('canonical_evolved_name','NEW_NAME'))
        self.rejects(lambda r:r['records'][0].__setitem__('original_species_or_sprite_id',1))
    def test_named_npc_relative_dungeon_location_not_coordinates_or_sprite(self):
        n=self.report['records'][4];self.assertEqual(n['location']['npc'],'進化Gさん');self.assertEqual(n['location']['relative_location'],'NORTHWEST_OF_VILLAGE')
        self.rejects(lambda r:r['records'][4].__setitem__('coordinates',[1,2]))
        self.rejects(lambda r:r['records'][4].__setitem__('appearance','BLUE_NPC'))
    def test_trial_repeatability_and_one_pet_are_not_inventory_capacity(self):
        q=self.report['records'][5];self.assertEqual(q['one_pet_per_attempt'],1);self.assertEqual(q['flow'][-1],'REPEATABLE_TRIAL')
        self.rejects(lambda r:r['records'][5].__setitem__('one_pet_per_attempt',5))
        self.rejects(lambda r:r['records'][5].__setitem__('exact_prerequisites',{'level':100}))
        self.rejects(lambda r:r['boundaries'].__setitem__('one_pet_per_ritual_is_carry_limit',True))
    def test_failed_level_one_initial_status_name_do_not_reset_unmentioned_fields(self):
        f=self.report['records'][7]['facts'];self.assertEqual(f['level'],1);self.assertEqual(f['name'],'INITIAL_STATE_UNSPECIFIED_NAME');self.assertIsNone(f['skills']);self.assertIsNone(f['owner'])
        self.rejects(lambda r:r['records'][7]['facts'].__setitem__('skills','ALL_LOST'))
        self.rejects(lambda r:r['records'][7].__setitem__('failure_species_or_identity_change','NEW_PET'))
        self.rejects(lambda r:r['boundaries'].__setitem__('failure_initial_stats_numbers',{'hp':10}))
    def test_growth_mutation_and_success_level_have_no_formula(self):
        self.assertIn('SOMETIMES',self.report['records'][6]['source_claim'])
        for k,v in [('mutation_probability',0.1),('status_formula',{'attack':2}),('successful_result_level',1)]:
            self.rejects(lambda r:r['records'][6].__setitem__(k,v))
        self.rejects(lambda r:r['boundaries'].__setitem__('flavor_spirit_is_named_world_entity',True))
    def test_guarantee_item_is_distinct_from_base_chance_and_quest_fee(self):
        self.assertEqual(self.report['records'][8]['scope'],'ITEM_GUARANTEE_NOT_ORDINARY_QUEST_RATE')
        b=self.report['records'][10]['facts'];self.assertEqual((b['price'],b['currency_as_written']),(350,'Gstone'));self.assertEqual(b['components'],COMPONENTS)
        self.rejects(lambda r:r['boundaries'].__setitem__('ordinary_quest_is_100_percent_success',True))
        self.rejects(lambda r:r['records'][10].__setitem__('ordinary_quest_fee',350))
        self.rejects(lambda r:r['records'][10].__setitem__('purchase_or_transaction_executed',True))
    def test_campaign_end_reroll_once_and_experience_distribution_stay_separate(self):
        self.assertEqual(self.report['records'][9]['rerolls_reported'],1)
        self.rejects(lambda r:r['records'][9].__setitem__('rerolls_reported','UNLIMITED'))
        self.rejects(lambda r:r['records'][11].__setitem__('transfer_ratio_or_duplication',0.5))
        self.rejects(lambda r:r['boundaries'].__setitem__('campaign_end_is_system_removal',True))
    def test_separately_dated_source_and_single_failed_image_scope(self):
        a=self.report['acquisition'];self.assertEqual(a['official_image_failure']['http_status'],404);self.assertEqual(a['media_availability']['response']['archived_snapshots'],{})
        self.assertEqual(self.report['inputs'][1]['capture_timestamp'],'20090217151837')
        for k in ['official_page_is_20081111_snapshot','official_image_404_proves_all_images_missing','media_2008_original_html_obtained']:
            self.rejects(lambda r:r['boundaries'].__setitem__(k,True))
    def test_concept_images_do_not_bind_elements_mutants_or_live_runtime(self):
        b=b'GIF89a'+struct.pack('<HH',97,96)+b'\0\0\0';self.assertEqual(image_metadata(b,[97,96])['dimensions'],[97,96])
        with self.assertRaises(ValueError):image_metadata(b,[135,115])
        self.rejects(lambda r:r['records'][13].__setitem__('runtime_or_sprite_binding',123))
        self.rejects(lambda r:r['boundaries'].__setitem__('red_or_black_pixels_prove_elements_or_mutation',True))
    def test_partial_attribution_rights_and_cross_region_promotion_fail(self):
        for fn in [extract_media,extract_official]:
            with self.assertRaises(ValueError):fn(b'<html>missing original source</html>')
        with self.assertRaises(ValueError):replay(self.report,[b'']*4)
        for k,v in [('game_ids',[1]),('rights_status','RELEASE_APPROVED'),('verification_status','RUNTIME_VERIFIED')]:
            self.rejects(lambda r:r['records'][0].__setitem__(k,v))
        self.rejects(lambda r:r['records'][14].__setitem__('cross_region_rebirth_fusion_equivalence','SAME'))
        self.rejects(lambda r:r['boundaries'].__setitem__('original_server_execution_verified',True))

    def test_downloaded_candidate_main_replay_and_durable_custody(self):
        from hashlib import sha256,sha1
        c=json.loads((REPORT.parent/'STONEAGE-JP2008-PET-EVOLUTION-CUSTODY-R1.json').read_text());self.assertEqual([len(c['runs'][k]) for k in ('candidate','main')],[10,11])
        for rows in c['runs'].values():self.assertTrue(all(r['head_sha']==c['content_head'] and r['conclusion']=='success' for r in rows))
        for pin in c['pins']:
            b=(REPORT.parents[2]/pin['path']).read_bytes();self.assertEqual(len(b),pin['bytes']);self.assertEqual(sha256(b).hexdigest(),pin['sha256']);self.assertEqual(sha1(b'blob '+str(len(b)).encode()+bytes([0])+b).hexdigest(),pin['git_blob'])
        payloads=[(REPORT.parent/name).read_bytes() for name in ['STONEAGE-JP2008-PET-EVOLUTION-CI-REPLAY-R1.json','STONEAGE-JP2008-PET-EVOLUTION-CI-MAIN-REPLAY-R1.json']]
        for a,b in zip(c['artifacts'],payloads):self.assertEqual(a['member_sha256'],sha256(b).hexdigest());self.assertEqual(json.loads(b)['extracted'],[x['extracted'] for x in self.report['inputs']])
        candidate,main=[json.loads(b) for b in payloads];self.assertEqual(candidate['inputs'][1:],main['inputs'][1:]);self.assertNotEqual(candidate['inputs'][0]['sha256'],main['inputs'][0]['sha256']);self.assertFalse(c['current_media_byte_drift']['byte_change_location_independently_identified'])
        a=json.loads((REPORT.parent/'STONEAGE-JP2008-PET-EVOLUTION-NEGATIVE-AUDIT-R1.json').read_text());self.assertEqual(len(a['cases']),8);pins={s['id']:s['http']['sha256'] for s in self.report['inputs']}
        self.assertTrue(all(x['full_replay_rejected'] and x['original_sha256']==pins[x['source_id']] and x['original_sha256']!=x['mutated_sha256'] for x in a['cases']))
        self.assertTrue(a['outside_release_metadata_boundary']['current_wrapper_change_accepted']);self.assertTrue(a['outside_release_metadata_boundary']['release_semantics_unchanged'])
        self.assertTrue(c['evolved_names_masked']);self.assertFalse(c['raw_sources_committed']);self.assertFalse(c['original_server_execution_verified'])

if __name__=='__main__':unittest.main()

