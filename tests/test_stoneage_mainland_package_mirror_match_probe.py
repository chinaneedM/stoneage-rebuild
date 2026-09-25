import unittest
from tools.stoneage_mainland_package_mirror_match_probe import (
    DIRECT_MIRRORS, DISCOVERY_MIRRORS, discover_article, page_images
)

class PackageMirrorProbeTests(unittest.TestCase):
    def test_direct_20_mirror_present(self):
        self.assertTrue(any(scope=="mirror-20" and "sa85.com.cn" in url for scope,url,_ in DIRECT_MIRRORS))

    def test_discover_1x_link(self):
        html='<a href="/stoneage-182.html">石器时代182时期的端游客户端新手礼包-石器时代端游发行时间</a>'
        rows=discover_article(html,"https://shiqi.ws/page_35.html","石器时代182时期的端游客户端新手礼包")
        self.assertEqual(rows,("https://shiqi.ws/stoneage-182.html",))

    def test_page_images(self):
        html='<img src="/a.jpg"><img data-src="https://x.example/b.png"><img src="/a.jpg">'
        rows=page_images(html,"https://site.example/p.html")
        self.assertEqual([r["url"] for r in rows],["https://site.example/a.jpg","https://x.example/b.png"])

if __name__=="__main__":
    unittest.main()
