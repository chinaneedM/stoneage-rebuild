import unittest

from tools.stoneage_tw10_archive_timeout_retry_probe import ATTEMPTS,TARGET
from tools.stoneage_tw10_archive_installed_tree_probe import metadata


class TaiwanV1ArchiveTimeoutRetryProbeTests(unittest.TestCase):
    def test_target_is_the_single_prior_timeout(self):
        self.assertEqual(TARGET,"NPWK19720801")

    def test_retry_budget_is_bounded(self):
        self.assertGreaterEqual(ATTEMPTS,2)
        self.assertLessEqual(ATTEMPTS,5)

    def test_shared_metadata_helper_returns_url_and_data_shape(self):
        # Contract-level guard: the shared helper returns a 2-tuple.
        # Network is not invoked here; inspect the function constants/source shape.
        import inspect
        source=inspect.getsource(metadata)
        self.assertIn("return url,get_json(url)",source)


if __name__=="__main__":
    unittest.main()
