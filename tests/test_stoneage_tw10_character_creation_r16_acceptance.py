"""Bounded source-integrity and anti-overclaim regression cases for R16."""
import copy
import unittest
from tools.stoneage_tw10_character_creation_r16_acceptance import accept_record, source_groups, verify, PATH

class R16AcceptanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import json
        cls.record=json.loads(PATH.read_bytes())
        cls.groups=source_groups()
    def test_actual_published_primary_bytes(self):
        out=verify()
        self.assertEqual(out['matching_consecutive_spr_group_keys'],12)
        self.assertIsNone(out['runtime_selectable_character_total'])
    def test_independent_exact_semantic_replay(self):
        self.assertEqual(accept_record(copy.deepcopy(self.record),self.groups)['next_raw_dword'],198)
    def test_change_original_source_key_refused(self):
        r=copy.deepcopy(self.record)
        r['bounded_window']['values'][3]['dword'] += 1
        with self.assertRaises(ValueError):
            accept_record(r,self.groups)
    def test_false_label_refused(self):
        r=copy.deepcopy(self.record)
        r['bounded_window']['values'][0]['same_build_role_or_portrait_verified']=True
        with self.assertRaises(ValueError):
            accept_record(r,self.groups)
    def test_fabricated_character_count_refused(self):
        r=copy.deepcopy(self.record)
        r['findings']['original_character_count']=12
        with self.assertRaises(ValueError):
            accept_record(r,self.groups)
    def test_fabricated_table_extent_refused(self):
        r=copy.deepcopy(self.record)
        r['bounded_window']['actual_table_extent_verified']=True
        with self.assertRaises(ValueError):
            accept_record(r,self.groups)
    def test_missing_original_position_refused(self):
        r=copy.deepcopy(self.record)
        r['bounded_window']['values'][11]['relative_index']=0
        with self.assertRaises(ValueError):
            accept_record(r,self.groups)
    def test_bitmap_and_spr_keys_not_interchangeable(self):
        r=copy.deepcopy(self.record)
        r['findings']['selected_bitmap']=100000
        with self.assertRaises(ValueError):
            accept_record(r,self.groups)

if __name__=='__main__':
    unittest.main()
