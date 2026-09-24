import unittest

from tools.stoneage_historical_map_pack_archive_probe import (
    PAGES, basename_hint, target_hrefs
)


class HistoricalMapPackArchiveProbeTests(unittest.TestCase):
    def test_expected_lineage_pages_are_pinned(self):
        labels=[row[0] for row in PAGES]
        self.assertEqual(labels,["40-map-patch","50-full-map","60-full-map"])

    def test_download_cgi_filename_is_recovered(self):
        url="https://games1.sina.com.cn/cgi-bin/games/downgames/download.pl?aid=61620&filename=shiqi4updatex_02_11_08.zip&size=3440"
        self.assertEqual(basename_hint(url),"shiqi4updatex_02_11_08.zip")

    def test_target_hrefs_find_near_anchor(self):
        html='abc 完整地图档下载 <a href="http://example.test/map.exe">MAP</a>'
        rows=target_hrefs(html,"http://base.test/",("完整地图档下载",))
        self.assertTrue(any(row[2]=="http://example.test/map.exe" for row in rows))


if __name__=="__main__":
    unittest.main()
