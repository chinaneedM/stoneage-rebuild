import unittest
from tools.stoneage_china2000_zhcn_shiqi_download_probe import TARGETS, FROM, TO, cdx_url


class TestChinaComZhCnRoutes(unittest.TestCase):
    def test_window(self):
        self.assertEqual(FROM, "20001201")
        self.assertEqual(TO, "20010120")

    def test_source_paths_present(self):
        urls={row[1] for row in TARGETS}
        self.assertIn("http://game.china.com/zh_cn/hotspot/shiqi/index.html", urls)
        self.assertIn("http://game.china.com/zh_cn/download/index.html", urls)

    def test_exact_cdx(self):
        url=cdx_url("http://game.china.com/zh_cn/hotspot/shiqi/index.html","exact")
        self.assertIn("matchType=exact",url)
        self.assertIn("20001201",url)
        self.assertIn("20010120",url)


if __name__ == "__main__":
    unittest.main()
