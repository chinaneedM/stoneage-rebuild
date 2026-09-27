import unittest

from tools.stoneage_jhpop_root_replay import (
    ORIGINAL,
    TIMESTAMP,
    replay_url,
    targets,
    token_hits,
)


class JHPOPRootReplayTests(unittest.TestCase):
    def test_exact_capture(self):
        self.assertEqual(TIMESTAMP, "20001204160300")
        self.assertEqual(ORIGINAL, "http://www.jhpop.com:80/")
        self.assertIn("20001204160300id_", replay_url())

    def test_extracts_frame_and_meta_refresh(self):
        html = """
        <html><head><meta http-equiv="refresh" content="0; URL=/home/index.asp"></head>
        <frameset><frame src="/top.htm"><frame src="body.asp"></frameset></html>
        """
        got = set(targets(html))
        self.assertIn(("meta-refresh", "http://www.jhpop.com:80/home/index.asp"), got)
        self.assertIn(("frame", "http://www.jhpop.com:80/top.htm"), got)
        self.assertIn(("frame", "http://www.jhpop.com:80/body.asp"), got)

    def test_semantic_tokens(self):
        hits = token_hits("欢迎进入石器时代 WGS download")
        self.assertIn("石器时代", hits)
        self.assertIn("WGS", hits)
        self.assertIn("download", hits)


if __name__ == "__main__":
    unittest.main()
