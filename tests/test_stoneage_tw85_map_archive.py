import copy
import json
import unittest
from tools.stoneage_tw85_map_archive import ROOT, REPORT, validate, validate_report


class ArchiveTests(unittest.TestCase):
    def test_actual_archive(self):
        self.assertEqual(validate()['status'], 'PASS')

    def test_semantic_mutations_even_without_digest_gate(self):
        source = json.loads((ROOT/REPORT).read_bytes())
        changes = [
            lambda r: r['boundaries'].__setitem__('full_world_coverage_proven', True),
            lambda r: r['files'][0].__setitem__('original_place_name', 'invented'),
            lambda r: r['files'][0].__setitem__('width', 1),
            lambda r: r['files'][0]['planes'][0].__setitem__('ordinal', 3),
            lambda r: r['files'][0]['planes'][0].__setitem__('nonzero_cells', -1),
            lambda r: r['files'][0]['planes'][0]['most_frequent'][0].__setitem__('cells', 999999999),
            lambda r: r['files'][0].__setitem__('sha256', '0'*64),
            lambda r: r['files'].pop(),
            lambda r: r['source_pins'].clear(),
        ]
        for change in changes:
            report = copy.deepcopy(source)
            change(report)
            with self.subTest(change=changes.index(change)), self.assertRaises(ValueError):
                validate_report(report)


if __name__ == '__main__':
    unittest.main()
