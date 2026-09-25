import unittest
from tools.stoneage_ruten_early_carrier_probe import TARGETS
from tools.stoneage_ruten_early_carrier_fingerprint_probe import metadata

class EarlyCarrierFingerprintProbeTests(unittest.TestCase):
    def test_target_roles_unique(self):
        ids=[pid for pid,_ in TARGETS]
        self.assertEqual(len(ids),len(set(ids)))

    def test_metadata_callable(self):
        self.assertTrue(callable(metadata))

if __name__=="__main__":
    unittest.main()
