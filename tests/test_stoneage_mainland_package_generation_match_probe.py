import unittest
from tools.stoneage_mainland_package_generation_match_probe import (
    BLOG_TITLES,
    RUTEN_TARGETS,
    candidate_images,
    discover_links,
)

class MainlandPackageGenerationProbeTests(unittest.TestCase):
    def test_discover_exact_title_links(self):
        html='''<a href="/shiqi262.htm">石器时代1.82时期的客户端新手礼包</a>
        <a href="shiqi263.htm">石器时代2.0版客户端礼盒</a>'''
        rows=discover_links(html,"https://blog.shiqi.so/page2.htm",BLOG_TITLES)
        self.assertIn(("collector-1x","石器时代1.82时期的客户端新手礼包","https://blog.shiqi.so/shiqi262.htm"),rows)
        self.assertIn(("collector-20","石器时代2.0版客户端礼盒","https://blog.shiqi.so/shiqi263.htm"),rows)

    def test_dated_image_filter(self):
        html='''<img src="/zb_users/upload/2020/09/a.jpg"><img src="/theme/logo.png">'''
        rows=candidate_images(html,"https://blog.shiqi.so/shiqi263.htm",dated_only=True)
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]["url"],"https://blog.shiqi.so/zb_users/upload/2020/09/a.jpg")

    def test_mainland_targets_present(self):
        ids=[x[0] for x in RUTEN_TARGETS]
        self.assertIn("22636573895893",ids)
        self.assertIn("22638643800877",ids)
        self.assertIn("22631284715652",ids)

if __name__=="__main__":
    unittest.main()
