import unittest

from tools.stoneage_tw10_receive_map_join_probe import (
    DECODE_HELPERS,
    DISPATCH_RVA_MIN,
    DISPATCH_RVA_MAX,
    LOGIN_CALLBACKS,
    MAP_XREF_RVAS,
)


class TaiwanV10ReceiveMapJoinProbeTests(unittest.TestCase):
    def test_pinned_targets(self):
        self.assertEqual(DECODE_HELPERS, (0x1B140, 0x1B4C0))
        self.assertEqual(LOGIN_CALLBACKS["ClientLogin"], 0x2F200)
        self.assertEqual(LOGIN_CALLBACKS["CharLogin"], 0x2F530)
        self.assertEqual(len(MAP_XREF_RVAS), 6)
        self.assertLess(DISPATCH_RVA_MIN, DISPATCH_RVA_MAX)


if __name__ == "__main__":
    unittest.main()
