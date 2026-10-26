"""Adversarial whole-file/hash-extent and lossless material integration checks."""
import copy
import gzip
import hashlib
import json
from pathlib import Path
import unittest
from tools import stoneage_client_content_catalog_r24 as cat
from tools import stoneage_material_review_r23_guard as review
from tools.stoneage_battle_sab_crossversion_r17 import parse


class ClientCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = json.loads(gzip.decompress(cat.OUTPUT.read_bytes()))

    def test_exact_all_four_archived_sources(self):
        cat.validate(self.doc)
        self.assertEqual([self.doc['summary']['per_sample'][x]['file_occurrences']
                          for x in ('TW10', 'MIXED25', 'CN5', 'CLAIMED_TW85')], [383, 2302, 413, 557])

    def test_independent_prior_two_specimen_match(self):
        prior = json.loads((cat.ROOT/cat.BASE/'STONEAGE-TW10-PRESERVED25-FILE-SHA-INTERSECTION-R1.json').read_bytes())
        rows = self.doc['occurrences']
        mixed = {x['sha256'] for x in rows if x['sample'] == 'MIXED25'}
        matched = [x for x in rows if x['sample'] == 'TW10' and x['sha256'] in mixed]
        self.assertEqual(len(matched), prior['counts']['original_core_matched_files'])
        self.assertEqual({x['relative_path'] for x in matched}, {x['path'] for x in prior['matched']})

    def test_header_extent_explains_old_false_difference(self):
        # Same content, two distinct domains. Never compare data[4:] to complete data.
        data = b'SAB '+bytes(800)
        complete = hashlib.sha256(data).hexdigest()
        payload = hashlib.sha256(data[4:]).hexdigest()
        self.assertNotEqual(complete, payload)
        tw = 'CORE_FILE|category=battle_map|path=StoneAge/data/battlemap/battle00.sab|size=804|sha256='+complete
        # Replicate enough original rows to satisfy the production count guard.
        lines = [tw.replace('battle00.sab', 'battle'+str(i).zfill(2)+'.sab') for i in range(218)]
        lines += ['BATTLE_SAB_RECORD|path=StoneAge/data/battlemap/battle00.sab|size=804|payload_sha256='+payload]
        self.assertTrue(all(x['sha256'] == complete for x in parse(lines, 'tw')))

    def test_payload_only_source_cannot_stand_for_whole_file(self):
        with self.assertRaises(ValueError):
            parse(['BATTLE_SAB_RECORD|path=StoneAge/data/battlemap/battle00.sab|size=804|payload_sha256='+'0'*64], 'tw')

    def test_same_digest_inconsistent_size_rejected(self):
        with self.assertRaises(ValueError):
            cat.group_rows([{'sha256': '0'*64, 'bytes': 1, 'reference_id': 'a'},
                            {'sha256': '0'*64, 'bytes': 2, 'reference_id': 'b'}])

    def test_paths_preserve_case_and_refuse_escape(self):
        self.assertNotEqual(cat.safe_relative('data/battleMap/a'), cat.safe_relative('data/battlemap/a'))
        for p in ('../x', '/x', 'a//b', 'a/./b', 'a/../b', 'a\\b'):
            with self.subTest(path=p), self.assertRaises(ValueError): cat.safe_relative(p)

    def test_lost_duplicate_reference_rejected(self):
        doc = copy.deepcopy(self.doc); doc['occurrences'].pop()
        with self.assertRaises(ValueError): cat.validate(doc)

    def test_same_name_different_digest_not_merged(self):
        rows = [x for x in self.doc['occurrences'] if x['relative_path'] == 'StoneAge.exe']
        self.assertEqual(len(rows), 3)
        self.assertGreater(len({x['sha256'] for x in rows}), 1)

    def test_candidate_official_promotion_rejected(self):
        doc = copy.deepcopy(self.doc)
        doc['summary']['profiles']['CLAIMED_TW85']['official_clean_client_authenticated'] = True
        with self.assertRaises(ValueError): cat.validate(doc)

    def test_no_actual_file_savings_or_entity_identity(self):
        for key in ('actual_bytes_saved', 'original_source_files_deleted', 'original_asset_bytes_published'):
            self.assertEqual(self.doc['summary']['boundaries'][key], 0)
        doc = copy.deepcopy(self.doc); doc['summary']['boundaries']['npc_pet_quest_identity_proven'] = True
        with self.assertRaises(ValueError): cat.validate(doc)

    def test_cn5_cab_to_installed_reference_retained(self):
        rows = [x for x in self.doc['occurrences'] if x['sample'] == 'CN5']
        self.assertEqual(len({x['msi_sequence'] for x in rows}), 413)
        self.assertEqual(len({x['cab_index'] for x in rows}), 413)
        self.assertTrue(all(x['cab_file_key'] for x in rows))


class MaterialLayerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = json.loads(review.REPORT.read_bytes())

    def test_exact_pinned_four_layer_review(self): review.validate(self.doc)

    def test_delivery_execution_hearing_identity_not_interchangeable(self):
        for key, value in [('original_client_ever_executed', False), ('original_world_entered', True),
                           ('p2b_original_color_previews_durable_user_delivery', True),
                           ('assistant_heard_audio', True), ('user_playback_confirmed', True),
                           ('named_tw10_entities_added', 1), ('overall_completion_percent', 75)]:
            doc = copy.deepcopy(self.doc); doc['facts'][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError): review.validate(doc)

    def test_old_status_not_silently_promoted(self):
        doc = copy.deepcopy(self.doc); doc['domains'][0]['baseline']['complete'] = True
        with self.assertRaises(ValueError): review.validate(doc)

    def test_missing_domain_or_evidence_layer_refused(self):
        doc = copy.deepcopy(self.doc); doc['domains'].pop()
        with self.assertRaises(ValueError): review.validate(doc)
        doc = copy.deepcopy(self.doc); del doc['domains'][0]['layers']['original_execution']
        with self.assertRaises(ValueError): review.validate(doc)


if __name__ == '__main__': unittest.main()
