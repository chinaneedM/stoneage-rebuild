import unittest
from tools.stoneage_china2000_legacy_shiqi_url_census import FROM, TO, TARGETS, cdx_url, score


class TestLegacyShiqiCensus(unittest.TestCase):
    def test_window(self):
        self.assertEqual(FROM,"20001201")
        self.assertEqual(TO,"20010331")

    def test_source_prefix(self):
        prefixes={p for _,p in TARGETS}
        self.assertIn("http://game.china.com/hotspot/shiqi/",prefixes)

    def test_prefix_cdx(self):
        url=cdx_url("http://game.china.com/hotspot/shiqi/")
        self.assertIn("matchType=prefix",url)
        self.assertIn("collapse=urlkey",url)

    def test_rank_download(self):
        self.assertGreater(score("http://game.china.com/hotspot/shiqi/download/client.zip")[0],0)


if __name__=="__main__":
    unittest.main()
