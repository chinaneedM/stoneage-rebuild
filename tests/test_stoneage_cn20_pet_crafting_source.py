import copy
import json
import struct
import unittest
from tools.stoneage_cn20_pet_crafting_source import REPORT,NAV,FOOD,extract_nav,extract_course,extract_cook,extract_skill,image_metadata,replay,validate

class CraftingSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.report=json.loads(REPORT.read_text())
    def rejects(self,fn):
        r=copy.deepcopy(self.report);fn(r)
        with self.assertRaises(ValueError):validate(r)
    def test_fourteen_records_follow_archive_contract(self):
        validate(self.report);c=json.loads((REPORT.parent/'STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json').read_text())['future_website']
        self.assertEqual(len({r['record_id'] for r in self.report['records']}),14)
        for row in self.report['records']:
            self.assertTrue(set(c['record_contract']['required'])<=row.keys());self.assertIn(row['collection'],c['required_collections']);self.assertIsNone(row['game_ids'])
    def test_three_named_navigation_routes_are_real_and_unique(self):
        b=''.join('<a href="'+r['href']+'">'+r['label']+'</a>' for r in NAV).encode('gb18030')
        self.assertEqual(extract_nav(b),dict(routes=NAV))
        for bad in [b+b,b.replace(b'course.asp',b'unknown.asp'),b'no links']:
            with self.assertRaises(ValueError):extract_nav(bad)
    def test_skill_prices_do_not_become_per_craft_fee_or_currency(self):
        skills=[r['facts'] for r in self.report['records'][1:3]]
        self.assertEqual([(x['name'],x['price_label']) for x in skills],[('加工',1500),('料理',1000)])
        self.assertTrue(all(x['price_currency'] is None for x in skills))
        self.rejects(lambda r:r['records'][11].__setitem__('per_craft_fee',1500))
        self.rejects(lambda r:r['boundaries'].__setitem__('source_skill_price_is_per_craft_fee',True))
    def test_five_categories_keep_incomplete_recipe_and_charcoal_hedge(self):
        self.assertEqual([r['facts'] for r in self.report['records'][3:8]],FOOD)
        self.assertEqual(FOOD[2]['ingredients_as_written'],['水','米','炭'])
        self.assertIn('HEDGED',FOOD[3]['qualification']);self.assertIn('NOT_EXCLUSIVE',FOOD[4]['qualification'])
        self.rejects(lambda r:r['records'][6]['facts'].__setitem__('qualification','CHARCOAL_FORBIDDEN'))
        self.rejects(lambda r:r['boundaries'].__setitem__('recipes_complete',True))
    def test_storage_warning_is_not_a_persistent_bank_implementation(self):
        f=self.report['records'][8]['facts'];self.assertEqual(f['source_limit'],5);self.assertIsNone(f['unit_or_persistence'])
        self.rejects(lambda r:r['records'][8]['facts'].__setitem__('source_limit',6))
        self.rejects(lambda r:r['boundaries'].__setitem__('storage_is_authenticated_persistent_bank',True))
        self.rejects(lambda r:r['boundaries'].__setitem__('not_taking_ground_items_is_engine_enforced',True))
    def test_recommendations_and_hearsay_not_promoted_to_access_or_formula(self):
        self.assertIn('EXPERIENCE',self.report['records'][9]['status']);self.assertEqual(self.report['records'][10]['source_qualifier'],'有消息指出')
        self.rejects(lambda r:r['records'][9].__setitem__('status','LEVEL_1_REQUIRED'))
        self.rejects(lambda r:r['records'][10].__setitem__('status','VERIFIED_FORMULA'))
        for k in ['low_level_and_loyalty_recommendation_is_hard_requirement','enchantment_hearsay_is_verified_formula']:
            self.rejects(lambda r:r['boundaries'].__setitem__(k,True))
    def test_failure_possibilities_do_not_supply_probability_or_consumption(self):
        f=self.report['records'][0]['facts'];self.assertIsNone(f['probabilities']);self.assertEqual(len(f['failure_outcomes_reported']),2)
        self.assertIsNone(f['distinct_species_or_stack_predicate'])
        for k,v in [('success_formula',{'luck':1}),('item_consumption_formula','ALL_ALWAYS'),('exact_client_build','2.0')]:
            self.rejects(lambda r:r['boundaries'].__setitem__(k,v))
    def test_later_image_headers_and_non_execution_contract(self):
        b=b'GIF89a'+struct.pack('<HH',640,480)+b'\0\0\0'
        self.assertEqual(image_metadata(b)['width'],640)
        for bad in [b'PNG'+b,b[:6]+struct.pack('<HH',320,240)+b'\0\0\0']:
            with self.assertRaises(ValueError):image_metadata(bad)
        self.assertEqual([s['capture_timestamp'][:6] for s in self.report['inputs'][4:]],['200201','200201'])
        self.rejects(lambda r:r['records'][12].__setitem__('same_build_as_2001_text',True))
        self.rejects(lambda r:r['records'][13].__setitem__('successful_craft_verified',True))
    def test_missing_body_or_partial_source_replay_rejected(self):
        for fn in [extract_course,extract_cook,extract_skill]:
            with self.assertRaises(ValueError):fn('<title>石器时代2.0</title>'.encode('gb18030'))
        with self.assertRaises(ValueError):replay(self.report,[b'']*5)
        with self.assertRaises(ValueError):replay(self.report,[b'']*6)
    def test_runtime_ids_rights_and_early_version_promotion_rejected(self):
        self.rejects(lambda r:r['records'][0].__setitem__('game_ids',[1]))
        self.rejects(lambda r:r['records'][0].__setitem__('verification_status','RUNTIME_VERIFIED'))
        self.rejects(lambda r:r['records'][0].__setitem__('rights_status','RELEASE_APPROVED'))
        for k in ['original_server_execution_verified','source_host_guarantees_every_claim_is_verified','tw10_or_jss1999_backfill']:
            self.rejects(lambda r:r['boundaries'].__setitem__(k,True))
    def test_individual_records_cannot_contradict_the_global_unknown_boundaries(self):
        cases=[(0,'teacher_npc_id',42),(0,'pet_shop_coordinates',[1,2]),(1,'success_formula',{'luck':1}),(3,'full_recipe',True),(4,'recipe_id',123),(5,'result_item_ids',[1]),(8,'ownership_and_logout_behavior','PERSISTENT_BANK'),(9,'species_master_ids',[1]),(9,'success_rates',[1.0]),(9,'level_one_loyalty_hundred','HARD_REQUIREMENT'),(10,'implemented_formula',{'mp':8}),(10,'original_server_verified',True)]
        for i,k,v in cases:
            with self.subTest(record=i,key=k):self.rejects(lambda r:r['records'][i].__setitem__(k,v))

if __name__=='__main__':unittest.main()

