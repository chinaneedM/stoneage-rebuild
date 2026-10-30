import unittest
from tools.stoneage_scene44_sina_screenshot_index import inspect,URL,TARGETS
def sample(labels=TARGETS,third_href="/shots/one.html",date="2003-04-05 19:35"):
    parts=[f'<a href="{third_href if i==2 else "/shots/%d.html"%i}">{label}</a>' for i,label in enumerate(labels)]
    return ("<html><title>石器截图</title><body>新浪游戏 "+date+" 石器截图 "+
        " ".join(parts)+"</body></html>"+" "*6000).encode("gb18030")
class Scene44Index(unittest.TestCase):
    def test_exact_three_link_bindings(self):
        x=inspect(sample());self.assertEqual([r["exact_anchor_match_count"] for r in x["selected_labels"]],[1,1,1])
        self.assertEqual(x["selected_labels"][2]["anchors"][0]["resolved_url"],
                         "https://games.sina.com.cn/shots/one.html")
        self.assertIs(x["original_screenshot_image_bytes_downloaded"],False)
    def test_wrong_date_rejected(self):
        with self.assertRaises(ValueError):inspect(sample(date="2026-10-30 19:35"))
    def test_missing_label_rejected(self):
        with self.assertRaises(ValueError):inspect(sample(labels=TARGETS[:2]))
    def test_hidden_script_does_not_create_link(self):
        b=sample(labels=TARGETS[:2]);q=b.decode("gb18030").replace("</body>","<script>1.82时的机暴</script></body>")
        with self.assertRaises(ValueError):inspect(q.encode("gb18030"))
    def test_unrelated_redirect_rejected(self):
        with self.assertRaises(ValueError):inspect(sample(),url="https://example.com/")
    def test_no_source_bytes_rejected(self):
        with self.assertRaises(ValueError):inspect(b"123")
    def test_no_original_game_promotion(self):
        x=inspect(sample());self.assertIs(x["original_client_executed_this_round"],False)
        self.assertIs(x["same_version_as_original_tw1_or_jss1999_proven"],False)
