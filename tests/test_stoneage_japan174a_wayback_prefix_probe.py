import unittest

from tools.stoneage_japan174a_wayback_prefix_probe import (
    PINNED,
    basename,
    is_exact_payload,
    is_relevant,
    parse_cdx,
    resolution,
)


class Japan174aWaybackPrefixProbeTests(unittest.TestCase):
    def test_parse_cdx_table(self):
        rows = parse_cdx(
            b'[["timestamp","original","statuscode"],'
            b'["20031214010101","http://x/sa174hg.exe","200"]]'
        )
        self.assertEqual(rows[0]["timestamp"], "20031214010101")
        self.assertEqual(rows[0]["statuscode"], "200")

    def test_basename_ignores_query(self):
        self.assertEqual(
            basename("http://x/stoneage/sa174hg.exe?mirror=1"),
            "sa174hg.exe",
        )

    def test_exact_payload(self):
        self.assertTrue(is_exact_payload("http://x/SA174HG.EXE"))
        self.assertFalse(is_exact_payload("http://x/stoneage.exe"))

    def test_relevant_launch_chain(self):
        self.assertIn("sadl.asp", PINNED)
        self.assertTrue(is_relevant("http://x/HgSA.cab"))
        self.assertTrue(is_relevant("http://x/patcher.exe"))
        self.assertFalse(is_relevant("http://x/logo.gif"))

    def test_resolution_is_bounded(self):
        self.assertEqual(resolution(1, [], False), "EXACT_FILENAME_INDEXED")
        self.assertEqual(resolution(0, [("x",)], False), "INCONCLUSIVE")
        self.assertEqual(resolution(0, [], True), "INCONCLUSIVE")
        self.assertEqual(resolution(0, [], False), "BOUNDED_NO_PREFIX_INDEX_HIT")


if __name__ == "__main__":
    unittest.main()
