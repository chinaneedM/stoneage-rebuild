import copy
import json
import unittest
from tools.stoneage_tw85_mixed25_map_archive import ROOT, REPORT, replay, validate, layer_catalog


class ArchiveTests(unittest.TestCase):
    def test_actual_archive(self):
        self.assertEqual(validate()['status'], 'PASS')

    def test_lossless_occurrence_conservation_and_no_source_deletion(self):
        catalog = layer_catalog()
        refs = [x for group in catalog['groups'] for x in group['occurrences']]
        self.assertEqual(len(refs), 231)
        self.assertEqual(len({(x['sample'], x['path'], x['ordinal']) for x in refs}), 231)
        self.assertEqual(sum(x['sample'] == 'TW85' for x in refs), 126)
        self.assertEqual(sum(x['sample'] == 'MIXED25' for x in refs), 105)
        self.assertEqual(catalog['distinct_layer_byte_blocks'], 210)
        self.assertEqual(catalog['logical_layer_bytes']-catalog['distinct_layer_bytes'], 41950)
        self.assertTrue(all(v is False for v in catalog['boundaries'].values()))

    def test_semantic_mutations_without_digest_gate(self):
        original = json.loads((ROOT/REPORT).read_bytes())
        changes = [
            lambda r: r['boundaries'].__setitem__('same_named_place_proven', True),
            lambda r: r['boundaries'].__setitem__('changed_cells_computed', True),
            lambda r: r.__setitem__('source_class', 'OFFICIAL_CLEAN_25'),
            lambda r: r['compared_files'][0]['plane_equal'].__setitem__(0, True),
            lambda r: r['compared_files'][0].__setitem__('whole_file_equal', True),
            lambda r: r['compared_files'][0].__setitem__('original_place_name', 'invented'),
            lambda r: r['compared_files'][0]['mixed25_structure'].__setitem__('width', 1),
            lambda r: r['compared_files'][0]['mixed25_structure']['planes'][0].__setitem__('ordinal', 2),
            lambda r: r['compared_files'][0].__setitem__('mixed25_sha256', '0'*64),
            lambda r: r['counts']['plane_equality_masks'].__setitem__('111', 35),
            lambda r: r['tw85_paths_absent_from_mixed25'].pop(),
            lambda r: r['compared_files'].pop(),
            lambda r: r['source_pins'].clear(),
            lambda r: r['compared_files'][0]['mixed25_structure']['planes'][0].__setitem__('sha256', '0'*64),
        ]
        for index, change in enumerate(changes):
            value = copy.deepcopy(original)
            change(value)
            with self.subTest(case=index), self.assertRaises(ValueError):
                replay(value)


if __name__ == '__main__':
    unittest.main()
