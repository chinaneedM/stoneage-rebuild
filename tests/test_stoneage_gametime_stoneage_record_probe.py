import unittest

from tools.stoneage_gametime_stoneage_record_probe import (
    INTEREST,
    Parser,
    js_urls,
    snippets,
)


class GameTimeStoneAgeRecordProbeTests(unittest.TestCase):
    def test_parser_keeps_href_and_onclick(self):
        p=Parser()
        p.feed('<a href="data_view.asp?GW_IDX=9&GW_Name=Online" onclick="Down(9)">스톤에이지</a>')
        values=[x[2] for x in p.links]
        self.assertIn("data_view.asp?GW_IDX=9&GW_Name=Online",values)
        self.assertIn("Down(9)",values)

    def test_js_urls_expands_download_index(self):
        rows=js_urls(
            "http://www.gametime.co.kr/data/data_list.asp",
            "javascript:Down(9)",
        )
        self.assertIn(
            "http://www.gametime.co.kr/data/download.asp?GW_IDX=9&GW_Name=Online",
            rows,
        )

    def test_interest_matches_stoneage_and_download(self):
        self.assertTrue(INTEREST.search("스톤에이지"))
        self.assertTrue(INTEREST.search("download.asp?GW_IDX=9"))

    def test_snippets_preserve_context(self):
        rows=snippets("AAA 스톤에이지 BBB download.asp?GW_IDX=9 CCC")
        self.assertTrue(any("스톤에이지" in row for row in rows))
        self.assertTrue(any("GW_IDX=9" in row for row in rows))


if __name__=="__main__":
    unittest.main()
