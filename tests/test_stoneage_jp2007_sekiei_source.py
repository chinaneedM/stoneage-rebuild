import copy
import json
import unittest

from tools.stoneage_jp2007_sekiei_source import REPORT, OFFICIAL_LINK, extract, replay, validate


class SekieiSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.report=json.loads(REPORT.read_text())

    def rejects(self, mutate):
        r=copy.deepcopy(self.report);mutate(r)
        with self.assertRaises(ValueError):validate(r)

    def test_eight_archive_contract_records_not_eight_original_entities(self):
        validate(self.report)
        contract=json.loads((REPORT.parent/'STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json').read_text())['future_website']
        known={s['id'] for s in self.report['inputs']}
        self.assertEqual(len({r['record_id'] for r in self.report['records']}),8)
        for row in self.report['records']:
            self.assertTrue(set(contract['record_contract']['required'])<=row.keys())
            self.assertIn(row['collection'],contract['required_collections'])
            self.assertTrue(set(row['source_refs'])<=known)

    def test_three_representations_two_wording_cores_one_issuer_chain(self):
        a,b,c=self.report['inputs'][:3]
        self.assertEqual(a['extracted'],b['extracted'])
        self.assertEqual(a['extracted']['facts'],c['extracted']['facts'])
        self.assertNotEqual(a['extracted']['core_sha256'],c['extracted']['core_sha256'])
        self.assertEqual((a['extracted']['core_utf8_bytes'],c['extracted']['core_utf8_bytes']),(1427,1460))
        self.rejects(lambda r:r['boundaries'].__setitem__('two_host_representations_are_independent_factual_witnesses',True))

    def test_exact_capture_dates_and_distinct_encodings(self):
        a,b,c=self.report['inputs'][:3]
        self.assertEqual([s['encoding'] for s in (a,b,c)],['UTF-8','EUC-JP','UTF-8'])
        self.assertEqual([b['capture_timestamp'],c['capture_timestamp']],['20071223094402','20080220173517'])
        self.assertEqual([b['http']['bytes'],c['http']['bytes']],[61462,6511])
        self.assertEqual(c['page_update_label'],'2007/11/20')
        self.assertNotEqual(b['http']['sha256'],a['http']['sha256'])

    def test_unqualified_spirit_king_is_not_cn_light_or_dark_king(self):
        f=self.report['records'][0]['source_facts']
        self.assertEqual(f['sealing_actor_as_written'],'精霊王')
        self.assertEqual(f['soul_labels'],['善良の魂','邪悪な魂'])
        self.assertEqual(f['vessels_reported'],2)
        self.rejects(lambda r:r['records'][3].__setitem__('light_or_dark_king_identity','光明精灵王'))
        self.rejects(lambda r:r['boundaries'].__setitem__('unqualified_spirit_king_is_cn_light_or_dark_king',True))

    def test_topology_has_three_labels_not_original_map_ids(self):
        f=self.report['records'][0]['source_facts']
        self.assertEqual(f['islands_connected_by_source_seabed_passage'],['ジャルガ島','サイナス島','ギール島'])
        self.assertTrue(f['eruption_to_earthquake_to_fissure_reported'])
        self.rejects(lambda r:r['records'][1].__setitem__('final_map_ids',[100,200]))
        self.rejects(lambda r:r['records'][1].__setitem__('spawn_coordinates',[10,20]))

    def test_rumour_and_hunting_expedition_are_not_quest_ending(self):
        f=self.report['records'][0]['source_facts']
        self.assertEqual(f['vessel_presence_in_current_dungeon'],'RUMORED_NOT_CONFIRMED')
        self.assertIsNone(f['ending_and_vessel_recovery'])
        self.assertTrue(f['many_expedition_members_did_not_return_reported'])
        self.assertTrue(f['unique_returnee_reported'])
        self.rejects(lambda r:r['records'][5].__setitem__('script','SEAL_BROKEN_ENDING'))

    def test_unknown_rewards_level_and_species_master_stay_null(self):
        for row,key,value in [(5,'reward','プレミアム☆チケット'),(5,'minimum_level',80),(4,'species_id',123),(4,'stats',{'hp':100})]:
            with self.subTest(key=key):self.rejects(lambda r:r['records'][row].__setitem__(key,value))
        self.rejects(lambda r:r['boundaries'].__setitem__('commercial_ticket_is_quest_reward',True))
        self.rejects(lambda r:r['boundaries'].__setitem__('future_or_rumored_treasure_is_recovered_reward',True))

    def test_current_image_and_development_disclaimer_do_not_prove_release_sprites(self):
        self.assertTrue(self.report['inputs'][2]['development_screenshot_disclaimer_present'])
        self.assertEqual(self.report['records'][7]['dimensions'],[410,410])
        self.assertEqual(len(self.report['records'][7]['panels_observed']),4)
        self.rejects(lambda r:r['records'][7].__setitem__('original_sprite_binding',123))
        for key in ('historic_image_bytes_verified','current_press_image_is_operator_image_byte_match','production_screenshot_or_original_sprite_verified'):
            self.rejects(lambda r:r['boundaries'].__setitem__(key,True))

    def test_missing_issuer_date_or_operator_link_fails_before_semantics(self):
        for text in ['◆赤影の角獣伝説',
                     'メーカー発表文の内容をそのまま掲載しています 他の会社 2007年11月20日 '+OFFICIAL_LINK,
                     'メーカー発表文の内容をそのまま掲載しています 株式会社デジパーク 2007年11月20日']:
            with self.subTest(text=text[:30]),self.assertRaises(ValueError):extract(text.encode(),'current_press')

    def test_utf8_current_cannot_be_treated_as_early_eucjp_source(self):
        with self.assertRaises((ValueError,UnicodeDecodeError)):
            extract('日本語の現在のページ'.encode(),'early_press')

    def test_operator_capture_requires_both_update_label_and_development_warning(self):
        for text in ['赤影の迷宮 [2007/11/20 - アップデート]', '画面写真は開発中のものです。実際とは異なる場合があります']:
            with self.subTest(text=text),self.assertRaises(ValueError):extract(text.encode(),'operator_capture')

    def test_cross_source_fact_mutation_and_capture_substitution_rejected(self):
        self.rejects(lambda r:r['inputs'][2]['extracted']['facts'].__setitem__('vessels_reported',3))
        self.rejects(lambda r:r['inputs'][2]['extracted'].__setitem__('core_sha256',r['inputs'][0]['extracted']['core_sha256']))
        with self.assertRaises(ValueError):replay(self.report,[b'',b'',b''])
        with self.assertRaises(ValueError):replay(self.report,[b'',b'',b'',b''])

    def test_rights_runtime_and_early_version_promotions_rejected(self):
        self.rejects(lambda r:r['records'][0].__setitem__('rights_status','RELEASE_APPROVED'))
        for key,val in [('original_server_execution_verified',True),('exact_client_build','2007.exe'),('tw10_or_jss1999_backfill',True)]:
            self.rejects(lambda r:r['boundaries'].__setitem__(key,val))


if __name__=='__main__':unittest.main()
