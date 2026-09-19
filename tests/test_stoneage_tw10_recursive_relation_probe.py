import unittest

from tools.stoneage_tw10_recursive_relation_probe import roots_for_target


class TaiwanV10RecursiveRelationProbeTests(unittest.TestCase):
    def test_constants(self):
        # Function accepts capstone instructions in production; unit coverage here
        # ensures the module imports and its search policy remains bounded.
        from tools.stoneage_tw10_recursive_relation_probe import (
            MAX_DEPTH, MAX_NODES, SEARCH_RADII, WINDOW_BYTES
        )
        self.assertLessEqual(MAX_DEPTH, 5)
        self.assertLessEqual(MAX_NODES, 320)
        self.assertLessEqual(WINDOW_BYTES, 0x1000)
        self.assertEqual(SEARCH_RADII[0], 0)
        self.assertLessEqual(SEARCH_RADII[-1], 0x2000)


if __name__ == "__main__":
    unittest.main()
