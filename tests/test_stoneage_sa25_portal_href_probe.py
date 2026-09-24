import unittest
from tools.stoneage_sa25_portal_href_probe import extract_hrefs, text_contexts, anchor_contexts

class PortalHrefProbeTests(unittest.TestCase):
    def test_extracts_waei_and_payload_links(self):
        raw = """
        <a href="http://www.waei.com.cn/down/sa25full.exe">full</a>
        <a href="/images/logo.gif">logo</a>
        <a href="http://mirror.example/client/stoneage25.zip">mirror</a>
        """
        rows = extract_hrefs(raw, "http://example.test/page.html")
        abs_urls = {x[1] for x in rows}
        self.assertIn("http://www.waei.com.cn/down/sa25full.exe", abs_urls)
        self.assertIn("http://mirror.example/client/stoneage25.zip", abs_urls)
        self.assertNotIn("http://example.test/images/logo.gif", abs_urls)

    def test_text_contexts_find_distribution_terms(self):
        rows = text_contexts("<p>可到指定网址下载石器时代2.5完整升级版（580兆）和升级程序（8.25兆）。</p>")
        self.assertTrue(any("580兆" in x for x in rows))
        self.assertTrue(any("8.25兆" in x for x in rows))

    def test_anchor_context_retains_nearby_href(self):
        rows = anchor_contexts('<p>可到<a href="http://x/sa25.exe">指定网址</a>下载完整升级版</p>')
        self.assertTrue(any("sa25.exe" in x for x in rows))

if __name__ == "__main__":
    unittest.main()
