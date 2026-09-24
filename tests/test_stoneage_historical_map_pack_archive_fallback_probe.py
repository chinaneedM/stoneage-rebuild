import unittest

from tools.stoneage_historical_map_pack_archive_fallback_probe import (
    TARGETS, KEY_DATES, parse_arquivo
)


class HistoricalMapPackArchiveFallbackTests(unittest.TestCase):
    def test_exact_source_derived_targets_are_pinned(self):
        targets=dict(TARGETS)
        self.assertIn("shiqi4updatex_02_11_08.zip",targets["40-map-patch"])
        self.assertEqual(targets["50-60-map-ftp"],"ftp://211.90.133.5/dowload/sa/map.exe")
        self.assertEqual(targets["50-60-map-http-mirror"],"http://www.wuxitianlong.com/sa/map.exe")

    def test_key_dates_cover_40_and_sina_hub_periods(self):
        self.assertIn("20021108",KEY_DATES)
        self.assertIn("20030403",KEY_DATES)

    def test_parse_arquivo_array(self):
        body=b'[["timestamp","original","statuscode"],["20021108000000","http://x/map.exe","200"]]'
        rows=parse_arquivo(body)
        self.assertEqual(rows[0]["statuscode"],"200")


if __name__=="__main__":
    unittest.main()
