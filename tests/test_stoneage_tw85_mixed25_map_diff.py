import copy
from pathlib import Path
import struct
import tempfile
import unittest
from tools.stoneage_tw85_map_payload import digest, parse
from tools.stoneage_tw85_mixed25_map_diff import compare_one, compare_directory, expected_files


class MapDiffTests(unittest.TestCase):
    def raw(self, values=(10, 20, 0, 5, 1, 1), dimensions=(2, 1)):
        return struct.pack('<II6H', *dimensions, *values)

    def reference(self):
        raw = self.raw()
        return {'path': 'map/100.dat', 'sha256': digest(raw), **parse(raw)}

    def test_exact_control(self):
        row = compare_one(self.reference(), self.raw(), digest(self.raw()))
        self.assertTrue(row['whole_file_equal'])
        self.assertEqual(row['plane_equal'], [True, True, True])

    def test_only_second_layer_changes(self):
        raw = self.raw((10, 20, 0, 6, 1, 1))
        row = compare_one(self.reference(), raw, digest(raw))
        self.assertFalse(row['whole_file_equal'])
        self.assertEqual(row['plane_equal'], [True, False, True])

    def test_equal_cell_count_different_dimensions_not_spatially_compared(self):
        raw = self.raw(dimensions=(1, 2))
        row = compare_one(self.reference(), raw, digest(raw))
        self.assertEqual(row['status'], 'DIMENSIONS_DIFFER')
        self.assertIsNone(row['plane_equal'])

    def test_hash_drift_rejected_before_layout(self):
        with self.assertRaises(ValueError):
            compare_one(self.reference(), b'changed', digest(self.raw()))

    def test_unknown_layout_is_explicit_not_false_equality(self):
        raw = b'unknown'
        row = compare_one(self.reference(), raw, digest(raw))
        self.assertEqual(row['status'], 'MIXED25_LAYOUT_UNRESOLVED')
        self.assertIsNone(row['plane_equal'])

    def test_presence_absence_and_case_alias_guards(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root/'map').mkdir()
            (root/'map/100.dat').write_bytes(self.raw())
            ref = {'files': [self.reference(), {**self.reference(), 'path': 'map/200.dat'}]}
            expected = {'map/100.dat': digest(self.raw())}
            result = compare_directory(root, ref, expected)
            self.assertEqual(result['counts']['plane_equality_masks'], {'111': 1})
            self.assertEqual(result['tw85_paths_absent_from_mixed25'], ['map/200.dat'])
            (root/'map/200.dat').write_bytes(self.raw())
            with self.assertRaises(ValueError):
                compare_directory(root, ref, expected)
            (root/'map/200.dat').unlink()
            (root/'map/100.DAT').write_bytes(self.raw())
            with self.assertRaises(ValueError):
                compare_directory(root, ref, expected)
            (root/'map/100.DAT').unlink()
            (root/'map/100.dat').unlink()
            with self.assertRaises(ValueError):
                compare_directory(root, ref, expected)

    def test_original_mixed_manifest_is_complete_and_pinned(self):
        self.assertEqual(len(expected_files()), 2302)


if __name__ == '__main__':
    unittest.main()
