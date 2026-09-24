import unittest

from tools.stoneage_sina_182_archive_fallback_probe import (
    TARGETS, KEY_DATES, parse_arquivo
)


class Sina182ArchiveFallbackProbeTests(unittest.TestCase):
    def test_target_forms_are_pinned(self):
        targets=dict(TARGETS)
        self.assertEqual(targets["ftp-original"],"ftp://211.90.133.5/dowload/sa/sa1.82.exe")
        self.assertEqual(targets["http-equivalent"],"http://211.90.133.5/dowload/sa/sa1.82.exe")

    def test_period_key_dates_include_source_page(self):
        self.assertIn("20030403",KEY_DATES)
        self.assertIn("20010123",KEY_DATES)

    def test_parse_arquivo_array(self):
        body=b'[["timestamp","original","statuscode"],["20030403000000","http://x/sa1.82.exe","200"]]'
        rows=parse_arquivo(body)
        self.assertEqual(rows[0]["original"],"http://x/sa1.82.exe")


if __name__=="__main__":
    unittest.main()
