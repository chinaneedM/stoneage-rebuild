import unittest
from tools.stoneage_waei_www9_exact_postdec6_residual import IDS, ATTEMPTS


class TestExactPostDec6Residual(unittest.TestCase):
    def test_failed_ids_only(self):
        self.assertEqual(IDS, (50, 55, 56, 57, 58, 59, 60))
        self.assertEqual(ATTEMPTS, 2)


if __name__ == "__main__":
    unittest.main()
