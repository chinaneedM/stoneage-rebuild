import unittest

from tools.stoneage_tw10_protocol_handoff_probe import (
    SEND_RVA, MAX_BYTES, MAX_INSNS
)


class TaiwanV10ProtocolHandoffProbeTests(unittest.TestCase):
    def test_pinned_send_helper_and_bounds(self):
        self.assertEqual(SEND_RVA, 0x1B3F0)
        self.assertLessEqual(MAX_BYTES, 0x800)
        self.assertLessEqual(MAX_INSNS, 400)


if __name__ == "__main__":
    unittest.main()
