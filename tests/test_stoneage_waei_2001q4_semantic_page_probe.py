import unittest

from tools.stoneage_waei_2001q4_semantic_page_probe import contexts, route_refs, route_score


class WaeiQ4SemanticPageProbeTests(unittest.TestCase):
    def test_route_refs_extracts_attributes_and_js(self):
        h = """
        <form action="../down/client.asp"></form>
        <script>window.open('http://1.2.3.4/stoneage2.0setup.exe')</script>
        """
        refs = route_refs(h, "http://www.waei.com.cn/ZHUANQU/stoneage2/stnews/a.asp")
        self.assertIn("http://www.waei.com.cn/ZHUANQU/stoneage2/down/client.asp", refs)
        self.assertIn("http://1.2.3.4/stoneage2.0setup.exe", refs)

    def test_route_score_prioritizes_exact_client_like_url(self):
        self.assertGreater(
            route_score("http://1.2.3.4/stoneage2.0setup.exe"),
            route_score("http://www.waei.com.cn/image/logo.gif"),
        )

    def test_contexts_is_bounded(self):
        out = contexts("前文 " + "石器时代2.0完整升级版下载" + " 后文")
        self.assertTrue(out)
        self.assertTrue(all(len(s) <= 500 for _, s in out))


if __name__ == "__main__":
    unittest.main()
