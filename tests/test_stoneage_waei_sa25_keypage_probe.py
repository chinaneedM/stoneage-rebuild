import unittest

from tools.stoneage_waei_sa25_keypage_probe import (
    SEEDS,
    extract,
    replay_urls,
)

class WaeiSA25KeypageProbeTests(unittest.TestCase):
    def test_seed_set_contains_rollout_pages(self):
        labels={x[0] for x in SEEDS}
        self.assertIn("index",labels)
        self.assertIn("bulletin-315",labels)
        self.assertIn("news-31",labels)

    def test_multiple_replay_modes(self):
        modes=[x[0] for x in replay_urls("20020201000000","http://example.com/a")]
        self.assertEqual(modes,["id","if","plain"])

    def test_extracts_terms_and_href(self):
        body=(
            '<html><body>石器时代2.5完整升级版580兆 '
            '<a href="http://download.example/sa25setup.exe">下载</a></body></html>'
        ).encode("gb18030")
        terms,hrefs,excerpts=extract(body,"http://www.waei.com.cn/")
        self.assertIn("石器时代2.5",terms)
        self.assertEqual(hrefs[0][1],"http://download.example/sa25setup.exe")
        self.assertTrue(excerpts)

if __name__=="__main__":
    unittest.main()
