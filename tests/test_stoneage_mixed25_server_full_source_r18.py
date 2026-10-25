import copy
import json
import unittest
from tools.stoneage_mixed25_server_full_source_r18 import (
    OUTPUT, PRIOR_MISSING, build, validate, load_sources, parse,
)

class R18SourceConservationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc=json.loads(OUTPUT.read_bytes())
    def test_complete_regeneration_from_git_pinned_parent(self):
        self.assertEqual(self.doc,build())
        validate(self.doc)
    def test_omissions_have_actual_source_hashes(self):
        omissions=self.doc['omitted_from_previous_candidate']
        self.assertEqual(tuple(r['path'] for r in omissions),PRIOR_MISSING)
        self.assertEqual(sum(r['size'] for r in omissions),731424)
        self.assertTrue(all(len(r['sha256'])==64 and not r['prior_candidate_selected'] for r in omissions))
    def test_all_2245_source_occurrences_retained(self):
        rows=self.doc['all_server_occurrences']
        self.assertEqual(len(rows),2245)
        self.assertEqual(len(set(r['path'] for r in rows)),2245)
        self.assertEqual(sum(r['size'] for r in rows),10465523)
    def test_sha_dedup_preserves_124_original_occurrences(self):
        rows=self.doc['all_server_occurrences']
        self.assertEqual(len({r['sha256'] for r in rows}),2121)
        dup=self.doc['duplicate_content_groups']
        self.assertEqual(len(dup),53)
        self.assertEqual(sum(len(x['occurrences'])-1 for x in dup),124)
        self.assertEqual(self.doc['summary']['extracted_real_bytes_deleted'],0)
    def test_actual_filename_scope(self):
        r={x['relative_path']:x for x in self.doc['master_presence']}
        self.assertFalse(r['enemy1.txt']['in_full_original_tree'])
        self.assertFalse(r['enemybase1.txt']['in_full_original_tree'])
        self.assertTrue(r['enemybase.txt']['in_full_original_tree'])
        self.assertTrue(r['group1.txt']['in_full_original_tree'])
        self.assertFalse(r['group1.txt']['in_prior_candidate_subset'])
    def test_original_source_diff_not_two_independent_downloads(self):
        self.assertFalse(self.doc['source_parent']['payload_downloaded_this_round'])
        self.assertFalse(self.doc['vocabulary_boundary']['source_is_clean_official_build'])
        self.assertEqual(self.doc['summary']['early_official_quest_master_restored'],0)
    def test_mutated_missing_source_occurrence_refused(self):
        x=copy.deepcopy(self.doc);x['all_server_occurrences'].pop()
        with self.assertRaises(ValueError):validate(x)
    def test_mutated_omission_sha_refused(self):
        x=copy.deepcopy(self.doc);x['omitted_from_previous_candidate'][0]['sha256']='0'*64
        with self.assertRaises(ValueError):validate(x)
    def test_mutated_event_classifier_refused(self):
        x=copy.deepcopy(self.doc);x['vocabulary_boundary']['file_path_tokens_are_not_quest_event_classification']=False
        with self.assertRaises(ValueError):validate(x)
    def test_fabricated_early_pet_roster_refused(self):
        x=copy.deepcopy(self.doc);x['summary']['early_official_pet_species_restored']=1
        with self.assertRaises(ValueError):validate(x)
    def test_source_file_parsing_full_coverage(self):
        full,game=load_sources()
        files,candidates=parse(full,game)
        self.assertEqual(len(files),2245)
        self.assertEqual(len(candidates),2227)
        self.assertEqual(sum(not x['prior_candidate_selected'] for x in files),18)

if __name__=="__main__":
    unittest.main()
