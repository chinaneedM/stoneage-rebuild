import copy
from hashlib import sha256,sha1
import json
import unittest
from tools.stoneage_jp2008_cooperation_source import REPORT,BOUNDARIES,extract,validate,replay,rewards,jpeg_size

class CooperationSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=json.loads(REPORT.read_text())
    def reject(self,fn):
        r=copy.deepcopy(self.r);fn(r)
        with self.assertRaises(ValueError):validate(r)
    def test_archive_fields_collections_and_seventeen_records(self):
        validate(self.r);contract=json.loads((REPORT.parent/'STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json').read_text())['future_website']
        self.assertEqual(len(self.r['records']),17)
        for row in self.r['records']:
            self.assertTrue(set(contract['record_contract']['required'])<=row.keys())
            self.assertIn(row['collection'],contract['required_collections']);self.assertIsNone(row['game_ids'])
    def test_dew_drop_and_blessing_exchange_are_distinct(self):
        self.assertEqual([x['source_reported']['label'] for x in self.r['records'][:2]],['精霊の雫','精霊の恵み'])
        self.reject(lambda r:r['records'][0]['source_reported'].__setitem__('drop_rate',1))
        self.reject(lambda r:r['boundaries'].__setitem__('exchange_ratio',1))
    def test_four_named_roles_do_not_supply_original_spawn_or_art(self):
        self.assertEqual(self.r['records'][2]['source_reported']['place_as_written'],'マンモスルーム')
        self.reject(lambda r:r['records'][2]['source_reported'].__setitem__('coordinates',[1,2]))
        self.reject(lambda r:r['records'][5]['source_reported'].__setitem__('appearance','BLUE'))
    def test_mammoth_room_hall_variant_remains_unresolved(self):
        f=self.r['inputs'][0]['extracted']['facts'];self.assertEqual(f['tree_location_variant'],'マンモスホール');self.assertFalse(f['tree_location_labels_equivalence_verified'])
        self.reject(lambda r:r['inputs'][0]['extracted']['facts'].__setitem__('tree_location_labels_equivalence_verified',True))
    def test_tree_reward_thresholds_are_not_fees_or_all_required_per_player(self):
        self.assertEqual([x['delivery_total'] for x in rewards()[:5]],[2000,5000,8000,30000,35000])
        self.reject(lambda r:r['records'][8]['source_reported'].__setitem__('individual_cost',2000))
        self.reject(lambda r:r['boundaries'].__setitem__('population_or_server_counter_scope','ALL_SERVERS'))
    def test_three_local_totals_and_different_delivered_item(self):
        self.assertEqual([x['delivery_total'] for x in rewards()[5:]],[3000,3000,10000])
        self.assertTrue(all(x['delivered_item']=='精霊の雫' for x in rewards()[5:]))
        self.reject(lambda r:r['manual_reward_transcription'][5].__setitem__('delivered_item','精霊の恵み'))
    def test_collection_period_is_distinct_from_later_reward_availability(self):
        self.assertEqual(self.r['records'][6]['source_reported']['period']['end'],'2008-07-15 13:00')
        self.assertIn('2008-08-12',rewards()[3]['reported_availability'])
        self.reject(lambda r:r['boundaries'].__setitem__('reward_end_is_event_end',True))
    def test_permanent_label_does_not_prove_unlock_or_modern_service(self):
        self.reject(lambda r:r['records'][8]['source_reported'].__setitem__('actual_unlock_verified',True))
        self.reject(lambda r:r['boundaries'].__setitem__('reported_permanent_is_verified_current_service',True))
    def test_save_point_pet_reroll_and_carpenter_are_not_other_game_rules(self):
        self.assertIn('キヌイ',rewards()[0]['reward_label']);self.assertIn('再抽選',rewards()[4]['reward_label'])
        for k in ['save_point_is_client_local_save_proof','carpenter_three_times_is_player_stat_multiplier']:
            self.reject(lambda r:r['boundaries'].__setitem__(k,True))
        self.reject(lambda r:r['boundaries'].__setitem__('pet_reroll_distribution',{'attack':2}))
    def test_current_images_and_429_not_historical_capture_or_absence(self):
        self.assertEqual(self.r['official_acquisition']['attempts'],1)
        self.reject(lambda r:r['boundaries'].__setitem__('global_archive_absence_proven',True))
        self.reject(lambda r:r['records'][-1]['source_reported'].__setitem__('historical_pixels',True))
    def test_missing_or_partial_source_is_rejected(self):
        with self.assertRaises(ValueError):extract(b'<html>No release</html>')
        with self.assertRaises(ValueError):jpeg_size(b'\xff\xd8broken')
        with self.assertRaises(ValueError):replay(self.r,[b'']*5)
    def test_real_mutated_source_audit_and_region_runtime_gates(self):
        audit=json.loads((REPORT.parent/'STONEAGE-JP2008-COOPERATION-NEGATIVE-AUDIT-R1.json').read_text());self.assertEqual(len(audit['cases']),8)
        self.assertTrue(all(x['rejected'] and x['original_sha256']==self.r['inputs'][0]['sha256'] and x['original_sha256']!=x['mutated_sha256'] for x in audit['cases']))
        for k in ['original_server_execution_verified','same_named_earlier_world_entity_verified','tiger_quest_recovered']:
            self.reject(lambda r:r['boundaries'].__setitem__(k,True))

if __name__=='__main__':unittest.main()

