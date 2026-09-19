import unittest

from tools.stoneage_hananet_frame_probe import Parser, normalize


class HananetFrameProbeTests(unittest.TestCase):
    def test_parser(self):
        p = Parser()
        p.feed('<a href="/down/stoneage.zip">스톤에이지 다운로드</a>')
        self.assertEqual(len(p.links), 1)
        self.assertIn("stoneage.zip", p.links[0][2])

    def test_normalize(self):
        self.assertEqual(
            normalize("http://pds.hananet.net/index2.html", "/games/sa.exe"),
            "http://pds.hananet.net/games/sa.exe",
        )
        self.assertEqual(normalize("http://x/", "javascript:void(0)"), "")


if __name__ == "__main__":
    unittest.main()
