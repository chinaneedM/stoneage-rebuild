import unittest

from tools.stoneage_gametime_cd_archive_probe import INTEREST_EXT, clean


class GameTimeCDArchiveProbeTests(unittest.TestCase):
    def test_disc_and_archive_extensions(self):
        for name in ("disc.iso", "disc.BIN", "track.cue", "setup.exe", "a.7z"):
            self.assertIsNotNone(INTEREST_EXT.search(name), name)
        self.assertIsNone(INTEREST_EXT.search("cover.jpg"))

    def test_clean_normalizes_and_escapes_pipe(self):
        self.assertEqual(clean(" a  b|c "), "a b%7Cc")
        self.assertEqual(clean(["x", "y"]), "x,y")


if __name__ == "__main__":
    unittest.main()
