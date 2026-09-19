import unittest

from tools.stoneage_hananet_board_probe import Parser, normalize, safe


class HananetBoardProbeTests(unittest.TestCase):
    def test_parser_anchor(self):
        p = Parser()
        p.feed('<a href="/x/stoneage.zip">다운로드</a>')
        self.assertEqual(p.links[0][2], "/x/stoneage.zip")
        self.assertEqual(p.links[0][3], "다운로드")

    def test_normalize(self):
        self.assertEqual(
            normalize("http://www.hananet.net/cgi-bin/pkboard.cgi", "/files/a.exe"),
            "http://www.hananet.net/files/a.exe",
        )

    def test_safe(self):
        self.assertEqual(safe(" a\n b "), "a b")


if __name__ == "__main__":
    unittest.main()
