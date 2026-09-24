import unittest

from tools.stoneage_tw10_archive_timeout_retry_probe import ATTEMPTS,TARGET


class TaiwanV1ArchiveTimeoutRetryProbeTests(unittest.TestCase):
    def test_target_is_the_single_prior_timeout(self):
        self.assertEqual(TARGET,"NPWK19720801")

    def test_retry_budget_is_bounded(self):
        self.assertGreaterEqual(ATTEMPTS,2)
        self.assertLessEqual(ATTEMPTS,5)


if __name__=="__main__":
    unittest.main()
