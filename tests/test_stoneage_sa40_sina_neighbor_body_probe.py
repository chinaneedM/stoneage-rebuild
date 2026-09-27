import unittest
from tools.stoneage_sa40_sina_neighbor_body_probe import refs,score,contexts

class SinaNeighborBodyTests(unittest.TestCase):
    def test_extracts_js_and_href(self):
        h='<a href="http://202.1.2.3/down/a.zip">x</a><script>window.open("http://files.example/b.exe")</script>'
        r=refs(h,"http://games1.sina.com.cn/x")
        self.assertIn("http://202.1.2.3/down/a.zip",r)
        self.assertIn("http://files.example/b.exe",r)

    def test_ip_download_scores_high(self):
        self.assertGreaterEqual(score("http://202.1.2.3/down/a.zip"),7)

    def test_contexts_filename(self):
        c=contexts("下载 foo.zip 请点这里","foo.zip")
        self.assertTrue(c)

if __name__=="__main__":
    unittest.main()
