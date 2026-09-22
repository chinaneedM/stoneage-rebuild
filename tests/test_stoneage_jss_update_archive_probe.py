import unittest

from tools.stoneage_jss_update_archive_probe import (
    classify_archive_path,
    manifest_tokens,
    parse_cdx,
    resolution,
)


class JssUpdateArchiveProbeTests(unittest.TestCase):
    def test_parse_cdx_table(self):
        rows = parse_cdx(
            b'[["timestamp","original","statuscode"],'
            b'["20000101000000","http://x/~stoneage/newest.txt","200"]]'
        )
        self.assertEqual(rows[0]["timestamp"], "20000101000000")
        self.assertEqual(rows[0]["statuscode"], "200")

    def test_manifest_tokens_are_derived(self):
        files, urls = manifest_tokens(
            b"real_2.bin 123\\r\\n"
            b"data\\\\battle_7.bin xyz\\r\\n"
            b"http://update.gamersdream.ne.jp/~stoneage/sa_3.exe\\r\\n"
        )
        self.assertTrue(any("real_2.bin" in x for x in files))
        self.assertTrue(any("battle_7.bin" in x for x in files))
        self.assertEqual(
            urls,
            ("http://update.gamersdream.ne.jp/~stoneage/sa_3.exe",),
        )

    def test_classify_resource_and_map(self):
        flags = classify_archive_path("http://x/~stoneage/adrn_3.bin")
        self.assertTrue(flags["resource_family"])
        self.assertFalse(flags["map_like"])
        flags = classify_archive_path("http://x/~stoneage/fieldmap_1.dat")
        self.assertTrue(flags["map_like"])

    def test_resolution_preserves_uncertainty(self):
        self.assertEqual(
            resolution([object()], [], [], [], False),
            "UPDATE_MANIFEST_RECOVERED",
        )
        self.assertEqual(
            resolution([], [object()], [], [], False),
            "MANIFEST_CAPTURE_INDEXED",
        )
        self.assertEqual(
            resolution([], [], [object()], [], False),
            "UPDATE_PREFIX_INDEXED_NO_MANIFEST",
        )
        self.assertEqual(
            resolution([], [], [], [("error",)], False),
            "INCONCLUSIVE",
        )
        self.assertEqual(
            resolution([], [], [], [], True),
            "INCONCLUSIVE",
        )
        self.assertEqual(
            resolution([], [], [], [], False),
            "BOUNDED_NO_INDEX_ROWS",
        )


if __name__ == "__main__":
    unittest.main()
