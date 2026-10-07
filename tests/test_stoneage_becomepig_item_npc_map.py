import unittest

from tools.stoneage_becomepig_item_npc_map_native_audit import expected_rows


class ItemNpcMapTimerOracleTests(unittest.TestCase):
    def test_expected_composition_rows(self):
        rows = expected_rows()
        self.assertEqual(rows[0], (5, 0, 0, 2))
        self.assertEqual(rows[1], (-1, 1, 1, 1, 1, 1))
        self.assertEqual(rows[2], (0, 0, 5, 1, 0, 1, 1, -3, 2))
        self.assertEqual(rows[3], (100, 7, 5, 0))
        self.assertEqual(rows[4], (10, 5, 0, 0))


if __name__ == "__main__":
    unittest.main()
