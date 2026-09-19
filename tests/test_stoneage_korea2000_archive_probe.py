import unittest

from tools.stoneage_korea2000_archive_probe import (
    DOWNLOAD_EXT,
    INTEREST,
    LinkParser,
    safe_token,
)


class Korea2000ArchiveProbeTests(unittest.TestCase):
    def test_download_extensions(self):
        self.assertIsNotNone(DOWNLOAD_EXT.search("http://x/y/setup.exe"))
        self.assertIsNotNone(DOWNLOAD_EXT.search("http://x/y/a.ZIP?x=1"))
        self.assertIsNone(DOWNLOAD_EXT.search("http://x/y/index.html"))

    def test_interest_terms(self):
        self.assertIsNotNone(INTEREST.search("StoneAge client download"))
        self.assertIsNotNone(INTEREST.search("스톤에이지 다운로드"))
        self.assertIsNone(INTEREST.search("generic portal page"))

    def test_link_parser(self):
        p = LinkParser()
        p.feed('<a href="client/setup.exe">Download StoneAge</a>')
        self.assertEqual(
            p.links,
            [("client/setup.exe", "Download StoneAge")],
        )

    def test_safe_token_strips_controls_and_caps(self):
        value = "a\x00b" + ("x" * 1000)
        out = safe_token(value)
        self.assertNotIn("\x00", out)
        self.assertLessEqual(len(out), 500)


if __name__ == "__main__":
    unittest.main()
