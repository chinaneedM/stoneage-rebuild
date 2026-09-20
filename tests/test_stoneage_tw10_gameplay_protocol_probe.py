import unittest

from tools.stoneage_tw10_gameplay_protocol_probe import (
    SEND_HELPERS,
    RECV_HELPERS,
    summarize_slice,
)


class TaiwanGameplayProtocolProbeTests(unittest.TestCase):
    def test_summarize_send_helpers(self):
        calls = [
            (0x100, 0x1B480),
            (0x110, 0x1B0B0),
            (0x120, 0x1B060),
            (0x130, 0x1B0F0),
            (0x140, 0x1B060),
            (0x150, 0x1B3F0),
            (0x160, 0x22222),
        ]
        counts, nonhelpers = summarize_slice(calls, SEND_HELPERS)
        self.assertEqual(counts["header"], 1)
        self.assertEqual(counts["int"], 1)
        self.assertEqual(counts["string"], 1)
        self.assertEqual(counts["append"], 2)
        self.assertEqual(counts["send"], 1)
        self.assertEqual(nonhelpers, [(0x160, 0x22222)])

    def test_summarize_recv_helpers(self):
        calls = [
            (0x100, 0x1B120),
            (0x110, 0x1B120),
            (0x120, 0x1B140),
            (0x130, 0x1B4C0),
            (0x140, 0x33333),
        ]
        counts, nonhelpers = summarize_slice(calls, RECV_HELPERS)
        self.assertEqual(counts["int"], 2)
        self.assertEqual(counts["string"], 1)
        self.assertEqual(counts["wrap"], 1)
        self.assertEqual(nonhelpers, [(0x140, 0x33333)])


if __name__ == "__main__":
    unittest.main()
