import json
import unittest
import urllib.parse

from tools.stoneage_sa25_sa25up_exact_probe import (
    HISTORICAL_URL,
    TOKEN,
    arquivo_url,
    parse_wayback,
    wayback_url,
)


class SA25Sa25upExactProbeTests(unittest.TestCase):
    def test_target_is_exact_historical_token(self):
        self.assertEqual(TOKEN, "sa25up.zip")
        self.assertEqual(
            HISTORICAL_URL,
            "http://202.104.32.168/file/game/maoxian/sa25up.zip",
        )

    def test_wayback_query_pins_exact_url(self):
        parsed = urllib.parse.urlparse(wayback_url("20020205"))
        q = urllib.parse.parse_qs(parsed.query)
        self.assertEqual(q["url"], [HISTORICAL_URL])
        self.assertEqual(q["timestamp"], ["20020205"])

    def test_parse_available_snapshot(self):
        payload = {
            "archived_snapshots": {
                "closest": {
                    "available": True,
                    "timestamp": "20020205000000",
                    "status": "200",
                    "url": "http://web.archive.org/web/20020205000000/" + HISTORICAL_URL,
                }
            }
        }
        row = parse_wayback(payload)
        self.assertEqual(row["timestamp"], "20020205000000")
        self.assertEqual(row["status"], "200")

    def test_parse_unavailable_snapshot(self):
        self.assertIsNone(parse_wayback({"archived_snapshots": {}}))

    def test_arquivo_query_pins_exact_url(self):
        parsed = urllib.parse.urlparse(arquivo_url())
        q = urllib.parse.parse_qs(parsed.query)
        self.assertEqual(q["url"], [HISTORICAL_URL])
        self.assertEqual(q["from"], ["2001"])
        self.assertEqual(q["to"], ["2005"])


if __name__ == "__main__":
    unittest.main()
