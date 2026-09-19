import unittest

from tools.stoneage_tw10_server_selection_probe import (
    ENDPOINT_APIS,
    NETWORK_APIS,
    SERVER_IP_OFFSET,
    SERVER_PORT_OFFSET,
    SERVER_RECORD_SIZE,
    SERVER_SLOT_COUNT,
    WAEI_XREF_RVA,
)


class TaiwanV10ServerSelectionProbeTests(unittest.TestCase):
    def test_pinned_targets(self):
        self.assertIn("connect", ENDPOINT_APIS)
        self.assertIn("gethostbyname", ENDPOINT_APIS)
        self.assertIn("inet_addr", ENDPOINT_APIS)
        self.assertIn("recv", NETWORK_APIS)
        self.assertEqual(WAEI_XREF_RVA, 0xD4F2)
        self.assertEqual(SERVER_SLOT_COUNT, 10)
        self.assertEqual(SERVER_RECORD_SIZE, 193)
        self.assertEqual(SERVER_IP_OFFSET, 1)
        self.assertEqual(SERVER_PORT_OFFSET, 129)


if __name__ == "__main__":
    unittest.main()
