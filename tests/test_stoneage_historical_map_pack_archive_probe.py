import unittest

from tools.stoneage_historical_map_pack_archive_probe import (
    PAGE_40, PAGE_50, PAGE_60, KNOWN_60_MAP_TARGETS,
    basename_hint, extract_40, extract_50
)


class HistoricalMapPackArchiveProbeTests(unittest.TestCase):
    def test_expected_lineage_pages_are_pinned(self):
        self.assertIn("11084599.shtml",PAGE_40)
        self.assertIn("ltxs/sqxz.shtml",PAGE_50)
        self.assertTrue(PAGE_60.endswith("/download.shtml"))

    def test_download_cgi_filename_is_recovered(self):
        url="https://games1.sina.com.cn/cgi-bin/games/downgames/download.pl?aid=61620&filename=shiqi4updatex_02_11_08.zip&size=3440"
        self.assertEqual(basename_hint(url),"shiqi4updatex_02_11_08.zip")

    def test_40_extractor_requires_exact_patch_identity(self):
        html='<a href="download.pl?aid=61620&filename=shiqi4updatex_02_11_08.zip">x</a>'
        rows=extract_40(html,"https://games.sina.com.cn/")
        self.assertEqual(len(rows),1)
        self.assertIn("shiqi4updatex_02_11_08.zip",rows[0])

    def test_50_extractor_is_forward_and_bounded(self):
        html='完整地图档下载 <a href="http://example.test/map.exe">MAP</a> later'
        rows=extract_50(html,"http://base.test/")
        self.assertEqual(rows,("http://example.test/map.exe",))

    def test_60_targets_are_source_derived(self):
        self.assertEqual(
            KNOWN_60_MAP_TARGETS,
            (
                "ftp://211.90.133.5/dowload/sa/map.exe",
                "http://www.wuxitianlong.com/sa/map.exe",
            ),
        )


if __name__=="__main__":
    unittest.main()
