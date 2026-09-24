import unittest
from tools.stoneage_sa25_17173_topology_probe import classify_href

class TopologyProbeTests(unittest.TestCase):
    def test_local_html_is_route(self):
        self.assertEqual(classify_href("http://stoneage.17173.com/banben/sa25-up.htm","sa25.htm")[1],"route")
    def test_waei_and_archive_are_payload_candidates(self):
        self.assertEqual(classify_href("http://stoneage.17173.com/x","http://www.waei.com.cn/down/sa25.exe")[1],"payload_candidate")
        self.assertEqual(classify_href("http://stoneage.17173.com/x","files/client.zip")[1],"payload_candidate")
    def test_comment_is_noise(self):
        self.assertEqual(classify_href("http://stoneage.17173.com/x","http://x/comment.cgi?title=2.5")[1],"noise")

if __name__=="__main__":
    unittest.main()
