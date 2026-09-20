import unittest

from tools.stoneage_tw10_gameplay_callback_probe import shared_direct_targets


class TaiwanGameplayCallbackProbeTests(unittest.TestCase):
    def test_shared_direct_targets(self):
        cfgs = {
            "S": {"direct_calls": {0x1000: 9, 0x2000: 2}},
            "C": {"direct_calls": {0x1000: 4, 0x3000: 1}},
            "I": {"direct_calls": {0x1000: 7, 0x2000: 3}},
        }
        got = shared_direct_targets(cfgs)
        self.assertEqual(got[0x1000], {"S": 9, "C": 4, "I": 7})
        self.assertEqual(got[0x2000], {"S": 2, "I": 3})
        self.assertNotIn(0x3000, got)


if __name__ == "__main__":
    unittest.main()
