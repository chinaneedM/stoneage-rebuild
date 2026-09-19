import unittest

from tools.stoneage_wayback_available_probe import parse_closest


class WaybackAvailableProbeTests(unittest.TestCase):
    def test_parse_available_snapshot(self):
        payload = {
            "archived_snapshots": {
                "closest": {
                    "available": True,
                    "status": "200",
                    "timestamp": "20001228123456",
                    "url": "http://web.archive.org/web/20001228123456/http://example.test/",
                }
            }
        }
        self.assertEqual(
            parse_closest(payload),
            {
                "timestamp": "20001228123456",
                "status": "200",
                "url": "http://web.archive.org/web/20001228123456/http://example.test/",
            },
        )

    def test_parse_missing_snapshot(self):
        self.assertIsNone(parse_closest({"archived_snapshots": {}}))
        self.assertIsNone(
            parse_closest(
                {"archived_snapshots": {"closest": {"available": False}}}
            )
        )


if __name__ == "__main__":
    unittest.main()
