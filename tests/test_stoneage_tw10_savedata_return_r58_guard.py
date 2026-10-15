import copy
import unittest
from tools.stoneage_tw10_savedata_return_r58_guard import audit
from tools.stoneage_tw10_savedata_native_io_r58 import TARGETS

class TestR58Independent(unittest.TestCase):
    def test_expected_target_roots_are_distinct(self):
        roots = [item[1] for item in TARGETS]
        self.assertEqual(roots, [0x4a657, 0x4a53e])
        self.assertEqual(len(set(roots)), 2)

    def test_missing_schema_fails_closed(self):
        with self.assertRaises(ValueError):
            audit({'contexts': []})

    def test_source_queries_never_claim_native_write(self):
        from tools.stoneage_tw10_savedata_native_io_r58 import FLAGS
        self.assertIn('actual_native_flush_close_or_persistence_proven', FLAGS)

if __name__ == '__main__':
    unittest.main()
