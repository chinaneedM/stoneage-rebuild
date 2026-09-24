import unittest

from tools.stoneage_sa25_named_carrier_torrent_probe import (
    classify_path,
    flexible_periodical_match,
)


class NamedCarrierTorrentProbeTests(unittest.TestCase):
    def test_exact_february_issue(self):
        strict, lead = classify_path("ISO/电脑报 游戏世界 2002年2月号/disc.iso")
        self.assertIn(("computer-news-gameworld", "periodical"), strict)

    def test_date_variant(self):
        self.assertTrue(
            flexible_periodical_match(
                "game-king",
                "收藏/游戏王 2002年第2期/gameking.iso",
            )
        )

    def test_wrong_month_not_strict(self):
        strict, lead = classify_path("ISO/家庭电脑世界 2002年3月号.iso")
        self.assertNotIn(("home-computer-world", "periodical"), strict)

    def test_crosspromo_is_lead_without_association(self):
        strict, lead = classify_path("游戏/哇靠轰炸鸡完美中文版.iso")
        self.assertNotIn(("bombing-chicken-game", "crosspromo"), strict)
        self.assertIn(("bombing-chicken-game", "crosspromo"), lead)

    def test_crosspromo_strict_with_stoneage_association(self):
        strict, lead = classify_path("华义/石器时代2.5/轰炸鸡/客户端光盘.iso")
        self.assertIn(("bombing-chicken-game", "crosspromo"), strict)


if __name__ == "__main__":
    unittest.main()
