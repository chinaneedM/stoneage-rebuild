import unittest

from tools.stoneage_jss_saupdate_generation_suffix_emulation_probe import (
    ATOI_IAT_RVA, CASES, FUNC_RVA, c_atoi,
)


class JssSaUpdateGenerationSuffixEmulationProbeTests(unittest.TestCase):
    def test_rvas_are_pinned(self):
        self.assertEqual(FUNC_RVA,0x2060)
        self.assertEqual(ATOI_IAT_RVA,0x5264)

    def test_c_atoi_stub_matches_required_cases(self):
        self.assertEqual(c_atoi("12"),12)
        self.assertEqual(c_atoi("0017"),17)
        self.assertEqual(c_atoi("42extra"),42)
        self.assertEqual(c_atoi("-3"),-3)
        self.assertEqual(c_atoi("beta"),0)
        self.assertEqual(c_atoi("   +9x"),9)

    def test_case_labels_are_unique(self):
        labels=[row[0] for row in CASES]
        self.assertEqual(len(labels),len(set(labels)))


if __name__=="__main__":
    unittest.main()
