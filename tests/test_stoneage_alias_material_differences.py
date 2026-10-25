import json
from pathlib import Path
import tempfile
import unittest

from tools import stoneage_alias_material_differences as m


def row(index=0, physical=7, digest='a'*64, size=20):
    return {k: str(v) for k, v in {
        'index': index, 'bitmapno': physical, 'adder': 100, 'size': size,
        'xoff': -1, 'yoff': -2, 'width': 2, 'height': 2,
        'attr_sha256': 'b'*64, 'rd_block_sha256': digest,
        'rd_flag': 0, 'rd_width': 2, 'rd_height': 2, 'rd_size_field': size}.items()}


class MaterialCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fresh = m.build()
        cls.archived = json.loads((m.ROOT/m.OUTPUT).read_bytes())

    def test_entire_report_replays_from_pinned_complete_sources(self):
        self.assertEqual(self.fresh, self.archived)
        self.assertEqual(self.fresh['reviewed_reference_occurrences'], 17)
        self.assertEqual(self.fresh['reviewed_distinct_blocks'], 9)

    def test_zero_alias_resource_outside_catalog_is_still_found(self):
        r = row(physical=999)
        r['map_number'] = '0'
        found = m.scan([r], {(20, 'a'*64)}, {7}, 1)
        self.assertEqual(len(found['exact_block_matches']), 1)
        self.assertFalse(found['same_physical_id_rows'])

    def test_same_physical_number_does_not_imply_same_block(self):
        found = m.scan([row(digest='c'*64)], {(20, 'a'*64)}, {7}, 1)
        self.assertFalse(found['exact_block_matches'])
        self.assertEqual(len(found['same_physical_id_rows']), 1)

    def test_digest_and_actual_extent_both_participate_in_matching(self):
        self.assertFalse(m.scan([row(size=21)], {(20, 'a'*64)}, {7}, 1)['exact_block_matches'])

    def test_duplicate_physical_ids_preserve_every_occurrence(self):
        found = m.scan([row(0), row(1)], {(20, 'a'*64)}, {7}, 2)
        self.assertEqual([r['source_index'] for r in found['exact_block_matches']], [0, 1])

    def test_complete_source_gaps_reordering_and_truncation_rejected(self):
        for rows, count in [([row(1)], 1), ([row(0), row(0)], 2), ([row()], 2)]:
            with self.subTest(rows=rows, count=count), self.assertRaises(ValueError):
                m.scan(rows, {(20, 'a'*64)}, {7}, count)

    def test_unavailable_native_logical_field_is_not_assumed_zero(self):
        r = m.physical(row())
        self.assertNotIn('logical_alias', r)
        self.assertNotIn('map_number', r)

    def test_source_projection_checks_every_original_header_and_rd_field(self):
        r = m.physical(row())
        for key in ['source_index', *m.HEADER, 'attr_sha256', 'rd_sha256',
                    'rd_flag', 'rd_width', 'rd_height', 'rd_size_field']:
            changed = dict(r)
            changed[key] = changed[key]+1 if type(changed[key]) is int else 'c'*64
            with self.subTest(key=key), self.assertRaises(ValueError):
                m.check_reference(r, changed)

    def test_available_record_hash_is_required_but_unavailable_is_not_invented(self):
        r = m.physical(row())
        m.check_reference(r, r)
        r['record_sha256'] = 'd'*64
        with self.assertRaises(ValueError):
            m.check_reference(r, {**r, 'record_sha256': 'e'*64})

    def test_input_pin_rejects_changed_bytes(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root/'a').write_bytes(b'changed')
            with self.assertRaises(ValueError):
                m.pin(root, 'a', '0'*64)

    def test_set_relation_distinguishes_retained_candidates_from_replacement(self):
        self.assertEqual(m.relation({1}, {1, 2}), 'LEFT_STRICT_SUBSET_OF_RIGHT')
        self.assertEqual(m.relation({1, 2}, {1}), 'RIGHT_STRICT_SUBSET_OF_LEFT')
        self.assertEqual(m.relation({1}, {1}), 'SAME_BLOCK_CANDIDATE_SET')
        self.assertEqual(m.relation({1, 2}, {2, 3}), 'OVERLAPPING_BLOCK_CANDIDATE_SETS')
        self.assertEqual(m.relation({1}, {2}), 'DISJOINT_BLOCK_CANDIDATE_SETS')

    def test_two_cn_only_blocks_absent_from_full_tables_not_just_alias_view(self):
        for case in self.fresh['cases'][:2]:
            self.assertEqual(case['classification'], 'CN50_ONLY_BLOCK_IN_PINNED_PHYSICAL_SAMPLES')
            s = case['complete_physical_search']
            self.assertEqual(s['TW10']['rows_scanned'], 125996)
            self.assertEqual(s['TW85_NATIVE']['rows_scanned'], 416220)
            for profile in ['TW10', 'PATCH129', 'TW85_NATIVE']:
                self.assertFalse(s[profile]['exact_block_matches'])
            self.assertEqual(s['PATCH129']['same_physical_id_rows'][0]['logical_alias'], 0)
            self.assertFalse(case['official_content_deletion_established'])
            self.assertFalse(case['exact_renumbering_established'])

    def test_cn26040_retains_early_bytes_and_different_same_sized_candidate(self):
        case = self.fresh['cases'][2]
        refs = [r for r in case['references'] if r['profile'] == 'CN50']
        self.assertEqual([r['physical_bitmapno'] for r in refs], [9132, 303071])
        self.assertEqual({(r['width'], r['height']) for r in refs}, {(256, 320)})
        self.assertEqual(len({r['rd_sha256'] for r in refs}), 2)
        self.assertEqual(len({r['attr_sha256'] for r in refs}), 1)

    def test_26100_width_change_keeps_both_candidates_in_later_samples(self):
        case = self.fresh['cases'][3]
        self.assertEqual(case['occurrences_by_profile'], {'TW10': 1, 'CN50': 2, 'PATCH129': 2})
        self.assertEqual({r['width'] for r in case['references']}, {104, 204})
        self.assertEqual(case['block_candidate_set_relations'][2]['relation'], 'SAME_BLOCK_CANDIDATE_SET')
        self.assertIsNone(case['effective_runtime_reference'])

    def test_29000_three_blocks_are_not_three_proven_login_screens(self):
        case = self.fresh['cases'][4]
        self.assertEqual(case['occurrences_by_profile'], {'TW10': 1, 'CN50': 3, 'PATCH129': 2})
        self.assertEqual(case['distinct_byte_blocks'], 3)
        self.assertEqual(case['game_role'], 'UNKNOWN_RESOURCE_ALIAS')
        self.assertEqual({(r['width'], r['height']) for r in case['references']}, {(640, 480)})
        self.assertEqual(case['block_candidate_set_relations'][2]['relation'], 'RIGHT_STRICT_SUBSET_OF_LEFT')

    def test_scope_stays_five_cases_with_no_runtime_or_named_entity_promotion(self):
        self.assertEqual([r['logical_alias'] for r in self.fresh['cases']], list(m.ALIASES))
        b = self.fresh['boundaries']
        self.assertEqual(b['new_named_entities'], 0)
        self.assertFalse(b['rd_byte_difference_is_pixel_difference'])
        self.assertFalse(b['original_pixels_decoded_or_rendered'])
        self.assertIsNone(b['overall_restoration_percentage'])


if __name__ == '__main__':
    unittest.main()
