import unittest

from tools.stoneage_sina_download_target_probe import (
    TARGETS,decode_html,nearest_hrefs
)


class SinaDownloadTargetProbeTests(unittest.TestCase):
    def test_targets_include_early_client_and_full_map_labels(self):
        values=dict(TARGETS)
        self.assertIn("全开地图",values["70-installed-full-map"])
        self.assertIn("全开MAP",values["60-full-map"])
        self.assertEqual(values["182-client"],"石器时代1.82")

    def test_decode_gb18030_page(self):
        raw='<meta charset="gb2312">石器时代1.82'.encode("gb18030")
        text,encoding=decode_html(raw,{})
        self.assertIn("石器时代1.82",text)

    def test_nearest_href_prefers_close_link(self):
        html='''<a href="far.exe">far</a> xxx 真正全开MAP地图 <a href="map.exe"><img></a>'''
        rows=nearest_hrefs(html,"真正全开MAP地图")
        self.assertTrue(rows)
        self.assertTrue(rows[0][1].endswith("map.exe"))


if __name__=="__main__":
    unittest.main()
