import unittest

from tools.stoneage_korean_payload_filename_index_probe import (
    basename,
    strict_candidate,
)


class KoreanPayloadFilenameIndexProbeTests(unittest.TestCase):
    def test_distinctive_exact(self):
        self.assertTrue(
            strict_candidate("onlStoneAge.zip", "distinctive", filename="/x/onlStoneAge.zip")
        )
        self.assertFalse(
            strict_candidate("stone_demo.exe", "distinctive", filename="/x/darkstone_demo.exe")
        )

    def test_ambiguous_large_size(self):
        self.assertTrue(
            strict_candidate("stoneage.zip", "ambiguous-large", filename="stoneage.zip", size=257*1024*1024)
        )
        self.assertFalse(
            strict_candidate("stoneage.zip", "ambiguous-large", filename="stoneage.zip", size=2*1024*1024)
        )

    def test_ambiguous_context(self):
        self.assertTrue(
            strict_candidate(
                "sa.exe", "ambiguous-large", filename="sa.exe",
                context="Korean StoneAge Hananet formal client",
            )
        )
        self.assertFalse(
            strict_candidate("sa.exe", "ambiguous-large", filename="sa.exe", context="random utility")
        )

    def test_basename_exact(self):
        self.assertEqual(basename(r"C:\\StoneAge\\sa_demo.exe"), "sa_demo.exe")


if __name__ == "__main__":
    unittest.main()
