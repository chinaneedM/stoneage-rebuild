import unittest

from tools.stoneage_hananet_stad_detail_probe import (
    Parser, relevant_text, normalize, FILE_RE
)


class HananetStadDetailProbeTests(unittest.TestCase):
    def test_parser_captures_download_attr(self):
        p = Parser()
        p.feed('<a href="/down/sa.exe" onclick="go(\'sa.exe\')">다운로드</a>')
        vals = [x[2] for x in p.attrs]
        self.assertIn("/down/sa.exe", vals)
        self.assertTrue(any("sa.exe" in x for x in vals))

    def test_relevant_text_filters(self):
        rows = relevant_text(["hello", "스톤에이지 다운로드", "첨부 파일"])
        self.assertEqual(len(rows), 2)

    def test_normalize(self):
        self.assertEqual(
            normalize("http://www.hananet.net/cgi-bin/pkboard.cgi", "/down/sa.exe"),
            "http://www.hananet.net/down/sa.exe",
        )

    def test_file_pattern(self):
        self.assertEqual(FILE_RE.findall("get stoneage.zip now"), ["stoneage.zip"])


if __name__ == "__main__":
    unittest.main()
