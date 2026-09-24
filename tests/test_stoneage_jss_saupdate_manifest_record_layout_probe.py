import unittest

from tools.stoneage_jss_saupdate_manifest_record_layout_probe import (
    MEMBERS, RVA_MAX, RVA_MIN,
)


class JssSaUpdateManifestRecordLayoutProbeTests(unittest.TestCase):
    def test_members_are_unique(self):
        roles=[x[0] for x in MEMBERS]
        disps=[x[1] for x in MEMBERS]
        self.assertEqual(len(roles),len(set(roles)))
        self.assertEqual(len(disps),len(set(disps)))

    def test_record_layout_offsets(self):
        self.assertEqual(
            MEMBERS[:5],
            (
                ("selector",0x100),
                ("field4-checksum",0x104),
                ("field3",0x108),
                ("filename-generation",0x10C),
                ("runtime-flag",0x110),
            ),
        )
        self.assertEqual(MEMBERS[5],("filename-from-meta",-0x100))

    def test_probe_window_covers_manifest_consumers(self):
        self.assertLessEqual(RVA_MIN,0x19D0)
        self.assertGreaterEqual(RVA_MAX,0x3500)


if __name__=="__main__":
    unittest.main()
