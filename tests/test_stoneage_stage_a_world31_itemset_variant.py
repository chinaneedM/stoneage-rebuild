"""Public, source-bound checks for the WORLD31 alternate-table delta.

The original copyrighted itemset tables and private catalog are not in Git.
Private byte replay is separately reproducible with the script and private ZIP.
"""
from collections import Counter
import json
from pathlib import Path
import re
import unittest

from tools.stoneage_world31_itemset_variant import A, B, REPORT_SCHEMA, class_of

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'research/recovered/STONEAGE-STAGE-A-WORLD31-ITEMSET-VARIANT-R1.json'
WORLD31 = ROOT / 'research/recovered/STONEAGE-STAGE-A-WORLD31-RECOVERY-SOURCE-R1.json'


class OriginalRecoveryItemsetVariantTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = json.loads(MANIFEST.read_text(encoding='utf-8'))
        cls.world31 = json.loads(WORLD31.read_text(encoding='utf-8'))

    def test_scope_and_source_member_separation(self):
        d = self.doc
        self.assertEqual(d['schema'], REPORT_SCHEMA)
        self.assertEqual(d['configured_itemset_from_world31_setup_cf'], A)
        self.assertEqual(d['source_field_count'], 94)
        self.assertEqual(d['callback_function_column_zero_based'], 10)
        self.assertEqual(d['parent_original_mixed25_archive_sha256'], self.world31['archive_sha256'])
        self.assertEqual(d['source_itemsets'][A]['original_member_sha256'],
                         next(x for x in self.world31['selected_source_members'] if x['target'].endswith('/itemset.txt'))['member_sha256'])
        self.assertNotEqual(d['source_itemsets'][A]['original_member_sha256'], d['source_itemsets'][B]['original_member_sha256'])
        self.assertTrue(all(re.fullmatch(r'[0-9a-f]{64}', x['original_member_sha256']) for x in d['source_itemsets'].values()))

    def test_selected_table_matches_frozen_world31_source(self):
        d = self.doc
        selected = d['tables'][A]
        self.assertEqual(selected['callback_rows'], self.world31['catalog']['physical_callback_rows'])
        actual = Counter()
        for shape, scene, target, count in self.world31['catalog']['shape_scene_target_counts']:
            actual[shape] += count
        self.assertEqual(selected['shape_counts'], dict(actual))
        self.assertEqual(selected['callback_rows'], 644)
        self.assertEqual(d['shared_callback_ids'], 644)
        self.assertEqual(d['shared_changed_94_field_rows'], 0)
        self.assertEqual(d['configured_only_callback_ids'], [])

    def test_added_rows_are_not_deployed_recovery_proof(self):
        d = self.doc
        alt = d['tables'][B]
        selected = d['tables'][A]
        extra = d['alternate_only_callback_rows']
        self.assertEqual(len(extra), 19)
        self.assertEqual(alt['callback_rows'] - selected['callback_rows'], len(extra))
        self.assertEqual([r['id'] for r in extra], [1596, 1597, 1732, 1733, 1734, 1735,
            1736, 1737, 1757, 1758, 2186, 2187, 19545, 19546, 19547, 19548,
            20247, 20253, 20259])
        differences = {key: alt['shape_counts'][key] - selected['shape_counts'][key]
                       for key in alt['shape_counts']}
        self.assertEqual(differences, dict(Counter(r['option_shape'] for r in extra)))
        for row in extra:
            self.assertGreater(row['source_row_1based'], 0)
            for key in ('source_row_sha256_from_item01_catalog', 'raw_option_sha256_cp950'):
                self.assertRegex(row[key], r'\A[0-9a-f]{64}\Z')
            self.assertIsInstance(row['scene_raw'], str)
            self.assertIsInstance(row['target_raw'], str)
        self.assertFalse(d['world32_combat_settlement_verified'])
        self.assertFalse(d['source_original_executable_replayed_in_this_package'])
        self.assertFalse(d['source_same_deployment_or_official_version_proven'])
        self.assertFalse(d['original_items_used_in_game'])

    def test_option_tokens_are_not_inferred_from_spaced_or_unknown_parameters(self):
        self.assertEqual(class_of('體320'), 'HP')
        self.assertEqual(class_of('氣25'), 'MP')
        self.assertEqual(class_of('氣20體185'), 'HP_MP')
        for option in ('體 600', '氣 300 體 3000', 'LVUPUP 1140 地', '魅10', '', '氣2氣3', '體7全'):
            self.assertEqual(class_of(option), 'OTHER')


if __name__ == '__main__':
    unittest.main()
