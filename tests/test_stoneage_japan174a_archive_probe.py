import unittest

from tools.stoneage_japan174a_archive_probe import (
    DOWNLOAD_EXT,
    INTEREST,
    LinkParser,
    decode_html,
    safe,
    select_launch_snapshots,
)


class Japan174aArchiveProbeTests(unittest.TestCase):
    def test_download_extensions_include_period_formats(self):
        self.assertIsNotNone(DOWNLOAD_EXT.search("http://x/client/sa174a.exe"))
        self.assertIsNotNone(DOWNLOAD_EXT.search("http://x/client/stone.lzh?x=1"))
        self.assertIsNone(DOWNLOAD_EXT.search("http://x/index.html"))

    def test_interest_accepts_japanese_client_terms(self):
        self.assertIsNotNone(INTEREST.search("STONE AGE クライアント"))
        self.assertIsNotNone(INTEREST.search("ダウンロードはこちら"))
        self.assertIsNone(INTEREST.search("generic portal"))

    def test_link_parser_keeps_href_and_anchor(self):
        parser=LinkParser()
        parser.feed('<a href="files/client.exe">クライアント ダウンロード</a>')
        self.assertEqual(
            parser.links,
            [("files/client.exe","クライアント ダウンロード")],
        )

    def test_decode_html_supports_shift_jis(self):
        original="クライアント"
        self.assertEqual(decode_html(original.encode("cp932")),original)

    def test_launch_snapshot_selection_prefers_december_window(self):
        rows=[
            {"timestamp":"20040115000000","original":"http://stoneage.to/"},
            {"timestamp":"20030501000000","original":"http://stoneage.to/"},
            {"timestamp":"20031212000000","original":"http://stoneage.to/"},
        ]
        selected=select_launch_snapshots(rows,limit=3)
        self.assertEqual(
            [row["timestamp"] for row in selected],
            ["20031212000000","20040115000000","20030501000000"],
        )

    def test_safe_strips_controls_and_caps(self):
        value="a\x00b"+("x"*1000)
        out=safe(value)
        self.assertNotIn("\x00",out)
        self.assertLessEqual(len(out),500)


if __name__ == "__main__":
    unittest.main()
