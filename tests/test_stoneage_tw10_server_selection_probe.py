import unittest

from tools.stoneage_tw10_server_selection_probe import (
    ENDPOINT_APIS,
    NETWORK_APIS,
    WAEI_XREF_RVA,
)


class TaiwanV10ServerSelectionProbeTests(unittest.TestCase):
    def test_pinned_targets(self):
        self.assertIn("connect", ENDPOINT_APIS)
        self.assertIn("gethostbyname", ENDPOINT_APIS)
        self.assertIn("inet_addr", ENDPOINT_APIS)
        self.assertIn("recv", NETWORK_APIS)
        self.assertEqual(WAEI_XREF_RVA, 0xD4F2)


if __name__ == "__main__":
    unittest.main()
