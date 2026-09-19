import unittest

from tools.stoneage_korea2000_arquivopt_probe import QUERIES, clean


class Korea2000ArquivoProbeTests(unittest.TestCase):
    def test_queries_cover_three_distribution_surfaces(self):
        labels = {x[0] for x in QUERIES}
        self.assertIn("inium-url", labels)
        self.assertIn("hananet-korean", labels)
        self.assertIn("cnet-korean", labels)

    def test_clean_removes_controls_and_caps(self):
        s = clean("a\x00b" + ("x" * 2000))
        self.assertNotIn("\x00", s)
        self.assertLessEqual(len(s), 800)


if __name__ == "__main__":
    unittest.main()
