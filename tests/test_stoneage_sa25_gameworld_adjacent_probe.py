import unittest

from tools.stoneage_sa25_gameworld_adjacent_probe import candidate_match


class GameWorldAdjacentProbeTests(unittest.TestCase):
    def test_exact_filename(self):
        self.assertTrue(candidate_match("archive/GAMEWORLD200202.iso"))

    def test_chinese_compact_title(self):
        self.assertTrue(candidate_match("电脑报配套光盘之游戏世界200202"))

    def test_january_control_rejected(self):
        self.assertFalse(candidate_match("GAMEWORLD200201.iso"))

    def test_generic_february_text_not_promoted_without_identity(self):
        self.assertFalse(candidate_match("某游戏世界 2002年2月.iso"))


if __name__ == "__main__":
    unittest.main()
