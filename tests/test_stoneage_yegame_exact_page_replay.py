import unittest

from tools.stoneage_yegame_exact_page_replay import (
    CAPTURES,
    raw_targets,
    same_domain,
    score_target,
    token_hits,
)


class YegameExactPageReplayTests(unittest.TestCase):
    def test_known_capture_set(self):
        self.assertEqual(len(CAPTURES), 7)
        self.assertEqual(CAPTURES[0][0], "root")
        self.assertEqual(CAPTURES[0][1], "20010202023100")
        self.assertIn("yegame.com", CAPTURES[0][2])

    def test_relative_and_script_targets(self):
        sample = """
        <a href="/download/demo.exe">demo</a>
        <script>window.location="http://example.com/game/";</script>
        """
        targets = raw_targets(sample, "http://www.yegame.com/root/")
        urls = {url for _kind, url in targets}
        self.assertIn("http://www.yegame.com/download/demo.exe", urls)
        self.assertIn("http://example.com/game/", urls)

    def test_scoring_and_domain(self):
        self.assertGreaterEqual(score_target("http://www.yegame.com/game/download/demo.exe"), 3)
        self.assertTrue(same_domain("http://www.yegame.com/product/"))
        self.assertFalse(same_domain("http://example.com/product/"))

    def test_token_hits(self):
        hits = token_hits("石器时代 游戏客户端下载")
        self.assertIn("石器时代", hits)
        self.assertIn("客户端", hits)
        self.assertIn("下载", hits)


if __name__ == "__main__":
    unittest.main()
