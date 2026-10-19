import copy
import json
import unittest
from tools.stoneage_jp2008_rimfy_source import REPORT,extract,replay,validate


class RimfySource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.report=json.loads(REPORT.read_text())

    def rejects(self,mutate):
        r=copy.deepcopy(self.report);mutate(r)
        with self.assertRaises(ValueError):validate(r)

    def test_six_archive_records_and_source_refs(self):
        validate(self.report)
        c=json.loads((REPORT.parent/'STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json').read_text())['future_website']
        for row in self.report['records']:
            self.assertTrue(set(c['record_contract']['required'])<=row.keys());self.assertIn(row['collection'],c['required_collections'])
            self.assertTrue(set(row['source_refs'])<= {'S1','I1'})
        self.assertEqual(len({r['record_id'] for r in self.report['records']}),6)

    def test_parent_puppy_and_protector_are_three_distinct_roles(self):
        f=self.report['records'][0]['source_facts']
        self.assertEqual([f[k] for k in ('parent_dog_as_written','puppy_as_written','protector_as_written')],['リムファン','リムフィ','ミデル'])
        self.assertEqual(f['completion_reward_pet_label'],'リムフィ')
        self.rejects(lambda r:r['records'][1].__setitem__('gender','FEMALE'))
        self.rejects(lambda r:r['records'][3].__setitem__('quest_start_verified',True))

    def test_colour_and_promotional_image_are_not_elements_growth_or_sprite(self):
        self.assertEqual(self.report['inputs'][1]['dimensions'],[122,99])
        self.rejects(lambda r:r['records'][2].__setitem__('numeric_elements',[0,0,10,0]))
        self.rejects(lambda r:r['records'][2].__setitem__('growth_rates',{'attack':2}))
        self.rejects(lambda r:r['records'][5].__setitem__('original_sprite_binding',123))

    def test_objective_not_escort_implementation_or_reward_individual_identity(self):
        self.assertEqual(self.report['records'][0]['source_facts']['objective'],'TAKE_PUPPY_AND_SEARCH_FOR_PARENT')
        self.rejects(lambda r:r['records'][0].__setitem__('escort_implementation','PET_SLOT_FOLLOW_AI'))
        self.rejects(lambda r:r['records'][2].__setitem__('escorted_individual_equals_reward_individual',True))

    def test_unknown_level_ending_and_maps_stay_null(self):
        self.rejects(lambda r:r['records'][0].__setitem__('minimum_level',30))
        self.rejects(lambda r:r['records'][0].__setitem__('ending_details','PARENT_DIES'))
        self.rejects(lambda r:r['records'][3].__setitem__('spawn_coordinates',[10,20]))
        self.rejects(lambda r:r['records'][4].__setitem__('map_ids',[100]))

    def test_empty_archive_queries_are_bounded_not_historical_authentication(self):
        self.assertEqual(len(self.report['archive_discovery']),2)
        for d in self.report['archive_discovery']:self.assertEqual(d['response']['archived_snapshots'],{})
        self.rejects(lambda r:r['inputs'][0].__setitem__('historical_original_sha256','a'*64))
        self.rejects(lambda r:r['boundaries'].__setitem__('historical_media_or_image_bytes_verified',True))

    def test_media_release_marker_is_required_and_no_named_issuer_invented(self):
        self.rejects(lambda r:r['inputs'][0].__setitem__('authority','NAMED_DIGIPARK_ORIGINAL_HOST'))
        with self.assertRaises(ValueError):extract('親子の絆 株式会社デジパーク'.encode())
        with self.assertRaises(ValueError):extract('以下，リリースより 以下，リリースより'.encode())

    def test_narrative_shadow_hunger_or_publication_is_not_runtime(self):
        f=self.report['records'][0]['source_facts'];self.assertIsNone(f['mysterious_shadow_identity']);self.assertTrue(f['parent_lacks_food_narrative_not_hunger_rule'])
        for key,val in [('mysterious_shadow_is_named_boss',True),('publication_label_proves_actual_deployment',True),('exact_client_build','2008.exe'),('tw10_or_jss1999_backfill',True)]:
            self.rejects(lambda r:r['boundaries'].__setitem__(key,val))

    def test_rights_or_partial_source_promotion_rejected(self):
        self.rejects(lambda r:r['records'][0].__setitem__('rights_status','RELEASE_APPROVED'))
        with self.assertRaises(ValueError):replay(self.report,[b''])
        with self.assertRaises(ValueError):replay(self.report,[b'',b''])

    def test_permanent_ci_replay_and_head_scoped_source_custody(self):
        import hashlib
        receipt=json.loads((REPORT.parent/'STONEAGE-JP2008-RIMFY-CUSTODY-R1.json').read_text())
        saved=json.loads((REPORT.parent/'STONEAGE-JP2008-RIMFY-CI-REPLAY-R1.json').read_text())
        for pin in receipt['permanent_derived_files']:
            b=(REPORT.parents[2]/pin['path']).read_bytes()
            self.assertEqual((len(b),hashlib.sha256(b).hexdigest()),(pin['bytes'],pin['sha256']))
            self.assertEqual(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),pin['git_blob'])
        self.assertEqual(saved['quest'],self.report['inputs'][0]['extracted'])
        self.assertFalse(saved['historical_source_or_original_server_verified'])
        self.assertFalse(saved['raw_html_or_image_in_output'])
        for group,count in [('candidate',11),('main',12)]:
            rows=receipt['validation'][group];self.assertEqual(len(rows),count)
            self.assertTrue(all(r['conclusion']=='success' and r['head']==receipt['content_commit']['sha'] for r in rows))
        self.assertEqual(len(receipt['real_input_adversarial_checks']),7)


if __name__=='__main__':unittest.main()
