import unittest

from tools.stoneage_ia_netpower_uploader_probe import (
    ANCHORS,
    TARGET_MONTHS,
    candidate_score,
    month_hits,
)


class NetPowerUploaderProbeTests(unittest.TestCase):
    def test_scope_is_bounded(self):
        self.assertEqual(
            ANCHORS,
            ("pcgm-cd-dump", "GAMEPIA_cd_dump", "20230716_20230716_0953"),
        )
        self.assertEqual(TARGET_MONTHS, ("2000-12", "2001-01"))

    def test_month_patterns_cover_korean_and_compact_forms(self):
        self.assertEqual(month_hits("NetPower_200012_CD1.iso"), ["2000-12"])
        self.assertEqual(month_hits("2001-01/Disc1.bin"), ["2001-01"])
        self.assertEqual(month_hits("netpower_cd_2001_01"), ["2001-01"])
        self.assertEqual(month_hits("netpower_cd_2001_11"), [])
        self.assertEqual(month_hits("2001-10/Disc1.bin"), [])

    def test_candidate_scoring_requires_real_signals(self):
        doc = {"identifier": "x", "title": "NetPower 2001.01 CD"}
        carriers = [{"name": "NetPower_0101.iso"}]
        score, has_netpower, months = candidate_score(doc, carriers)
        self.assertTrue(has_netpower)
        self.assertIn("2001-01", months)
        self.assertGreaterEqual(score, 3)

        score, has_netpower, months = candidate_score(
            {"identifier": "unrelated", "title": "Random Korean software"},
            [{"name": "disc.iso"}],
        )
        self.assertEqual((score, has_netpower, months), (0, False, []))


if __name__ == "__main__":
    unittest.main()
