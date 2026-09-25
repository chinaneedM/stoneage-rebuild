import unittest
from tools.stoneage_waei_2001q4_html_link_probe import score_page,targetish,links

class WaeiQ4HtmlLinkProbeTests(unittest.TestCase):
    def test_root_index_scores_above_deep_misc(self):
        self.assertGreater(
          score_page("http://www.waei.com.cn/ZHUANQU/stoneage2/index.asp"),
          score_page("http://www.waei.com.cn/ZHUANQU/stoneage2/a/b/c/pet.asp")
        )

    def test_target_link_detection(self):
        self.assertTrue(targetish("http://x/file.exe","下载客户端"))
        self.assertTrue(targetish("http://x/a","完整升级版"))
        self.assertFalse(targetish("http://x/pet.asp","宠物介绍"))

    def test_cdx_fetch_contract_regression_marker(self):
        # The production CDX caller must unpack fetch()'s status, final URL,
        # headers, and body tuple; this marker guards the four-value contract.
        import inspect
        from tools import stoneage_waei_2001q4_html_link_probe as m
        self.assertIn("st,final,h,b=fetch(cdx_url()",inspect.getsource(m.main))

    def test_extract_links(self):
        h='<a href="../down/a.zip">下载升级版</a>'
        out=links(h,"http://www.waei.com.cn/ZHUANQU/stoneage2/a/index.asp")
        self.assertEqual(out[0][0],"http://www.waei.com.cn/ZHUANQU/stoneage2/down/a.zip")

if __name__=="__main__":
    unittest.main()
