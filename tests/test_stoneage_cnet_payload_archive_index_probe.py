import unittest

from tools.stoneage_cnet_payload_archive_index_probe import clean


class CnetPayloadArchiveIndexProbeTests(unittest.TestCase):
    def test_clean(self):
        self.assertEqual(clean("  stoneage.zip\n257MB  "), "stoneage.zip 257MB")
        self.assertNotIn("\x00", clean("a\x00b"))


if __name__ == "__main__":
    unittest.main()
