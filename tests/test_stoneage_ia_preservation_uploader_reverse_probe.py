import unittest

from tools.stoneage_ia_preservation_uploader_reverse_probe import (
    GUIDE_ISBNS,
    UPLOADERS,
    EXACT_FILES,
    STONEAGE,
)


class PreservationUploaderReverseProbeTests(unittest.TestCase):
    def test_scope_is_bounded(self):
        self.assertEqual(
            UPLOADERS,
            ("mirubackup1@gmail.com", "marty0837@naver.com"),
        )
        self.assertEqual(GUIDE_ISBNS, ("8995182121", "9788995182123"))

    def test_exact_target_filenames(self):
        for name in (
            "sa.exe",
            "dir/sa_demo.exe",
            "StoneAge.exe",
            "payload/stone_demo.exe",
            "onlStoneAge.zip",
            "mirror/stoneagebeta.zip",
            "StoneAge.zip",
        ):
            self.assertIsNotNone(EXACT_FILES.search(name), name)
        self.assertIsNone(EXACT_FILES.search("StoneAge_manual.txt"))
        self.assertIsNone(EXACT_FILES.search("rsa_demo.exe"))

    def test_stoneage_text_signal(self):
        self.assertTrue(STONEAGE.search("스톤에이지 설치 프로그램"))
        self.assertTrue(STONEAGE.search("Stone Age client"))
        self.assertFalse(STONEAGE.search("unrelated software"))


if __name__ == "__main__":
    unittest.main()
