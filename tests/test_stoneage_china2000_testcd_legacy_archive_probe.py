import json
import unittest
from tools.stoneage_china2000_testcd_legacy_archive_probe import parse_rows,article_id,wb_url,EXACT_TARGETS

class China2000TestCDLegacyArchiveProbeTests(unittest.TestCase):
    def test_parse_wayback_array(self):
        body=json.dumps([
            ["timestamp","original","statuscode","mimetype","digest","length","redirect"],
            ["20010101000000","http://game.china.com/x/63271.html","200","text/html","ABC","123",""],
        ]).encode()
        rows=parse_rows(body)
        self.assertEqual(rows[0]["original"],"http://game.china.com/x/63271.html")

    def test_article_id(self):
        self.assertEqual(article_id("http://x/y/63271.html"),"63271")
        self.assertEqual(article_id("http://x/y/index.html"),"")

    def test_wayback_prefix_url(self):
        u=wb_url("http://game.china.com/zh_cn/news/news1/444/20001220/","prefix")
        self.assertIn("matchType=prefix",u)
        self.assertIn("from=2000",u)

    def test_exact_63271_registered(self):
        urls={u for _,u in EXACT_TARGETS}
        self.assertIn("http://game.china.com/zh_cn/news/news1/444/20001220/63271.html",urls)

if __name__=="__main__":
    unittest.main()
