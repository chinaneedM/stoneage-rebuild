import unittest

from tools.stoneage_jss_saupdate_manifest_grammar_probe import (
    FIELDS, HELPER_RANGES, MANIFEST_RANGE,
)


class JssSaUpdateManifestGrammarProbeTests(unittest.TestCase):
    def test_manifest_range_is_pinned(self):
        self.assertEqual(MANIFEST_RANGE,(0x19D0,0x1F71))

    def test_expected_manifest_fields_are_unique(self):
        self.assertEqual(len(FIELDS),len(set(FIELDS)))
        self.assertEqual(
            FIELDS,
            (
                "EXE","SPRBIN","SPRADRNBIN","REALBIN","ADRNBIN","SOUNDBIN",
                "SOUNDADDRTXT","BATTLEBIN","BATTLETXT","IP","IP:1","MESSAGE",
            ),
        )

    def test_helper_ranges_are_pinned_and_non_overlapping(self):
        roles=[x[0] for x in HELPER_RANGES]
        self.assertEqual(len(roles),len(set(roles)))
        self.assertEqual(HELPER_RANGES[0],("manifest-line-helper",0x1F80,0x1FDF))
        self.assertEqual(HELPER_RANGES[1],("manifest-load-helper",0x2060,0x209B))
        self.assertLess(HELPER_RANGES[0][2],HELPER_RANGES[1][1])


if __name__=="__main__":
    unittest.main()
