import unittest

from tools.stoneage_sa_arena_ia_probe import optical_candidates, parse_cue
from tools.stoneage_stoneage5_optical_probe import IDENTIFIER, item_download_url


class Stoneage5OpticalProbeTests(unittest.TestCase):
    def test_target_identifier(self):
        self.assertEqual(IDENTIFIER, "Stoneage-5")

    def test_download_url_quotes_disc_name(self):
        url = item_download_url("CD [STA5].bin")
        self.assertTrue(url.startswith("https://archive.org/download/Stoneage-5/"))
        self.assertTrue(url.endswith("CD%20%5BSTA5%5D.bin"))

    def test_preserved_bin_and_cue_are_candidates(self):
        rows = [
            {"name": "CD [STA5].bin"},
            {"name": "CD [STA5].cue"},
            {"name": "cover.jpg"},
        ]
        self.assertEqual(
            [r["name"] for r in optical_candidates(rows)],
            ["CD [STA5].bin", "CD [STA5].cue"],
        )

    def test_cue_can_reference_sta5_bin(self):
        cue = """FILE "CD [STA5].bin" BINARY
  TRACK 01 MODE1/2352
    INDEX 01 00:00:00
"""
        tracks = parse_cue(cue)
        self.assertEqual(len(tracks), 1)
        self.assertEqual(tracks[0]["file"], "CD [STA5].bin")
        self.assertEqual(tracks[0]["mode"], "MODE1/2352")


if __name__ == "__main__":
    unittest.main()
