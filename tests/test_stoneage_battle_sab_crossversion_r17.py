import copy
import json
import unittest
from tools.stoneage_battle_sab_crossversion_r17 import build, validate, REPORT, SOURCES, source_lines, parse

class BattleSABSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=build()
    def test_real_archived_full_report(self):
        x=json.loads(REPORT.read_bytes())
        self.assertEqual(x,self.data)
        validate(x)
    def test_full_per_version_identity(self):
        rows=self.data['occurrences']
        self.assertEqual(len(rows),438)
        self.assertEqual((rows[0]['id'],rows[217]['id'],rows[218]['id'],rows[-1]['id']),(0,217,0,219))
        self.assertEqual(self.data['all_unique_sha256_count'],219)
    def test_exact_complete_file_cross_release_hash_alias(self):
        a={x['sha256'] for x in self.data['occurrences'] if x['profile']=='tw10'}
        b={x['sha256'] for x in self.data['occurrences'] if x['profile']=='mixed25'}
        self.assertEqual(len(a&b),217)
    def test_source_provenance(self):
        for key in SOURCES:
            rows=parse(source_lines(key),key)
            self.assertEqual(len(rows),218 if key=='tw' else 220)
    def test_false_original_match_refused(self):
        x=copy.deepcopy(self.data)
        x['same_index_sha256_equal_count']=0
        with self.assertRaises(ValueError): validate(x)
    def test_lost_duplicate_occurrence_refused(self):
        x=copy.deepcopy(self.data)
        x['occurrences']=[v for v in x['occurrences'] if not(v['profile']=='tw10' and v['id']==146)]
        with self.assertRaises(ValueError): validate(x)
    def test_op_notice_filename_false_equivalence_refused(self):
        x=copy.deepcopy(self.data);x['notice_context']['same_file_proven']=True
        with self.assertRaises(ValueError):validate(x)
    def test_fabricated_pet_species_refused(self):
        x=copy.deepcopy(self.data);x['findings']['original_pet_names_recovered']=2
        with self.assertRaises(ValueError):validate(x)
    def test_mixed_official_version_promotion_refused(self):
        x=copy.deepcopy(self.data);x['findings']['all_official_versions_recovered']=True
        with self.assertRaises(ValueError):validate(x)

if __name__=='__main__':unittest.main()
