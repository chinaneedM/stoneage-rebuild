import copy
import json
import struct
import unittest
from tools.stoneage_cn20_creation_status_source import REPORT,MAPPING,EFFECTS,extract_nav,extract_body,image_metadata,replay,validate,derived_comparison

class CreationSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.report=json.loads(REPORT.read_text())
    def rejects(self,fn):
        r=copy.deepcopy(self.report);fn(r)
        with self.assertRaises(ValueError):validate(r)
    def test_twelve_records_are_documentary_not_twelve_character_types(self):
        validate(self.report);contract=json.loads((REPORT.parent/'STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json').read_text())['future_website']
        self.assertEqual(len({r['record_id'] for r in self.report['records']}),12)
        for r in self.report['records']:
            self.assertTrue(set(contract['record_contract']['required'])<=r.keys());self.assertIn(r['collection'],contract['required_collections']);self.assertIsNone(r['game_ids'])
        self.assertIsNone(self.report['records'][0]['character_types'])
    def test_actual_navigation_uses_its_original_label_not_the_article_spelling(self):
        b='<a href="/ZHUANQU/stoneage2/tyro/creature.asp">人物创造</a>'.encode('gb18030')
        self.assertEqual(extract_nav(b)['label'],'人物创造')
        for x in [b+b,b.replace('人物创造'.encode('gb18030'),'人物创建'.encode('gb18030')),b.replace(b'creature',b'character')]:
            with self.assertRaises(ValueError):extract_nav(x)
    def test_initial_twenty_and_ten_are_not_cn_per_level_three(self):
        f=derived_comparison(self.report);self.assertEqual([f[k] for k in ['jss_initial_stat_points','jss_initial_element_points','cn_body_levelup_points']],[20,10,3])
        self.assertIsNone(f['cn_body_initial_stat_points']);self.assertIsNone(f['cn_body_initial_element_points'])
        self.rejects(lambda r:r['records'][2]['facts'].__setitem__('distributable_points',20))
        self.rejects(lambda r:r['boundaries'].__setitem__('jss20_creation_or10_element_points_transferred_to_cn',True))
        self.rejects(lambda r:r['boundaries'].__setitem__('repeated_three_point_clauses_mean_six_points',True))
    def test_four_primary_to_status_labels_do_not_supply_wire_fields(self):
        self.assertEqual(self.report['records'][1]['mapping'],MAPPING)
        self.rejects(lambda r:r['records'][1].__setitem__('wire_fields',{'体力':'Create13.4'}))
        self.assertIsNone(self.report['boundaries']['automatic_levelup_increase_amount'])
    def test_four_marginal_rows_keep_unmentioned_effects_unknown(self):
        self.assertEqual([x['facts'] for x in self.report['records'][3:7]],EFFECTS)
        self.assertEqual(EFFECTS[0]['reported_effects'],{'耐久力（HP）':3})
        self.rejects(lambda r:r['records'][3]['facts'].__setitem__('unmentioned_effects',0))
        self.rejects(lambda r:r['records'][4]['facts']['reported_effects'].__setitem__('防御力',0))
        self.rejects(lambda r:r['boundaries'].__setitem__('reported_deltas_are_verified_full_stat_formula',True))
    def test_fullwidth_name_wording_and_source_typo_are_preserved(self):
        self.assertEqual(self.report['records'][0]['name']['maximum_fullwidth_characters_as_written'],8)
        self.assertIsNone(self.report['records'][0]['name']['engine_counting_units'])
        self.assertEqual(self.report['records'][1]['first_hp_wording_as_written'],'体力（影响任务的HP）')
        self.rejects(lambda r:r['records'][1].__setitem__('first_hp_wording_as_written','体力（影响人物的HP）'))
        self.rejects(lambda r:r['boundaries'].__setitem__('name_limit_bytes_or_unicode_units','UTF8_BYTES_16'))
    def test_element_cycles_have_no_damage_multiplier_or_invented_pair_predicate(self):
        f=self.report['records'][7]['facts'];self.assertEqual(f['maximum_types'],2);self.assertEqual(f['cycle'],[['地','水'],['水','火'],['火','风'],['风','地']])
        self.rejects(lambda r:r['records'][7].__setitem__('allowed_pair_engine_predicate','ENUMERATED'))
        self.rejects(lambda r:r['boundaries'].__setitem__('element_damage_multiplier',2))
    def test_four_birthplaces_have_no_names_or_starter_species_join(self):
        f=self.report['records'][8]['facts'];self.assertEqual([f[k] for k in ['total','north_island','south_island']],[4,2,2]);self.assertTrue(f['different_starter_pet_by_birthplace_source_claim'])
        self.rejects(lambda r:r['records'][8]['facts'].__setitem__('village_names',['萨姆吉尔']))
        self.rejects(lambda r:r['records'][8].__setitem__('pet_species_ids',[1,2,3,4]))
        self.rejects(lambda r:r['records'][9].__setitem__('class_ids_or_thresholds',[1,2,3,4]))
    def test_later_image_is_an_outdoor_reference_not_a_creation_screen(self):
        b=b'GIF89a'+struct.pack('<HH',640,480)+b'\0\0\0'
        self.assertIn('OUTDOOR',image_metadata(b)['manual_observation'])
        with self.assertRaises(ValueError):image_metadata(b'PNG'+b)
        self.assertEqual(self.report['inputs'][1]['capture_timestamp'],'20011201045054');self.assertEqual(self.report['inputs'][2]['capture_timestamp'],'20011221174011')
        self.rejects(lambda r:r['records'][10].__setitem__('creation_ui_verified',True))
    def test_partial_source_wrong_author_or_runtime_rights_promotion_rejected(self):
        with self.assertRaises(ValueError):extract_body('<title>石器时代2.0</title>'.encode('gb18030'))
        with self.assertRaises(ValueError):replay(self.report,[b'',b''])
        self.rejects(lambda r:r.__setitem__('authority','OPERATOR_AUTHORED_RUNTIME_SCRIPT'))
        for k,v in [('game_ids',[1]),('rights_status','RELEASE_APPROVED'),('verification_status','RUNTIME_VERIFIED')]:
            self.rejects(lambda r:r['records'][0].__setitem__(k,v))
    def test_individual_unknown_fields_and_derived_source_pins_cannot_be_filled(self):
        for i,k,v in [(0,'layout_coordinates',[0,0]),(0,'colors',4),(2,'exact_exp_thresholds',[1]),(3,'base_stats',{'hp':10}),(4,'rounding_or_caps','FLOOR'),(9,'mandatory_build','ENDURANCE_20'),(10,'character_or_pet_ids',[1])]:
            with self.subTest(record=i,key=k):self.rejects(lambda r:r['records'][i].__setitem__(k,v))
        self.rejects(lambda r:r['derived_inputs'][0].__setitem__('sha256','0'*64))
    def test_visible_english_labels_do_not_certify_region_and_old_git_pins_are_checked(self):
        self.assertEqual(self.report['inputs'][2]['extracted']['visible_labels'],['MENU','Mail','Action','Eng'])
        self.assertFalse(self.report['boundaries']['image_english_labels_authenticate_region_or_language'])
        self.rejects(lambda r:r['boundaries'].__setitem__('image_english_labels_authenticate_region_or_language',True))
        self.rejects(lambda r:r['derived_inputs'][1].__setitem__('git_blob','0'*40))

if __name__=='__main__':unittest.main()

