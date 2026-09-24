import unittest

from tools.stoneage_jss_saupdate_manifest_line_emulation_probe import CASES, FUNC_RVA


class JssSaUpdateManifestLineEmulationProbeTests(unittest.TestCase):
    def test_function_rva_is_pinned(self):
        self.assertEqual(FUNC_RVA, 0x1F80)

    def test_case_delimiters_cover_manifest_usage(self):
        delimiters = {case[2] for case in CASES}
        self.assertIn(0x0A, delimiters)
        self.assertIn(0x3A, delimiters)


if __name__ == "__main__":
    unittest.main()
