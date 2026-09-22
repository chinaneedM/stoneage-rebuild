import unittest

from tools.stoneage_korea174_archive_probe import (
    DOWNLOAD_EXT,
    INTEREST,
    LinkParser,
    decode_html,
    safe,
    select_launch_snapshots,
)


class Korea174ArchiveProbeTests(unittest.TestCase):
    def test_download_extensions(self):
        self.assertIsNotNone(DOWNLOAD_EXT.search("http://x/stoneage.exe"))
        self.assertIsNotNone(DOWNLOAD_EXT.search("http://x/client.zip?x=1"))
        self.assertIsNone(DOWNLOAD_EXT.search("http://x/index.asp"))

    def test_interest_terms(self):
        self.assertIsNotNone(INTEREST.search("스톤에이지 클라이언트 다운로드"))
        self.assertIsNotNone(INTEREST.search("StoneAge patch"))
        self.assertIsNone(INTEREST.search("generic portal"))

    def test_link_parser(self):
        parser=LinkParser()
        parser.feed('<a href="pds/client.exe">스톤에이지 다운로드</a>')
        self.assertEqual(
            parser.links,
            [("pds/client.exe","스톤에이지 다운로드")],
        )

    def test_decode_html_cp949(self):
        text="스톤에이지"
        self.assertEqual(decode_html(text.encode("cp949")),text)

    def test_launch_snapshot_selection_prefers_july_to_september_2003(self):
        rows=[
            {"timestamp":"20030601000000","original":"http://game3.netmarble.net/stoneage/"},
            {"timestamp":"20030728000000","original":"http://game3.netmarble.net/stoneage/"},
            {"timestamp":"20030901000000","original":"http://game3.netmarble.net/stoneage/"},
        ]
        selected=select_launch_snapshots(rows,limit=3)
        self.assertEqual(
            [row["timestamp"] for row in selected],
            ["20030728000000","20030901000000","20030601000000"],
        )

    def test_safe_caps_and_removes_controls(self):
        out=safe("a\x00b"+("x"*1000))
        self.assertNotIn("\x00",out)
        self.assertLessEqual(len(out),500)


if __name__=="__main__":
    unittest.main()
