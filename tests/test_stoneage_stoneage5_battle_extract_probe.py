import hashlib
import os
import tempfile
import unittest

from tools.stoneage_stoneage5_battle_extract_probe import (
    TARGETS,
    V1_BATTLE_SIZE,
    V1_BATTLETXT_SIZE,
    decode_text,
    sha256,
)


class Stoneage5BattleExtractProbeTests(unittest.TestCase):
    def test_reference_sizes(self):
        self.assertEqual(V1_BATTLE_SIZE, 185892)
        self.assertEqual(V1_BATTLETXT_SIZE, 5792)

    def test_targets_are_small_early_payloads(self):
        self.assertEqual(
            TARGETS,
            ("soundaddr_3.txt", "battle_2.bin", "data_1.bin", "battletxt_2.txt"),
        )

    def test_sha_helper(self):
        self.assertEqual(
            sha256(b"abc"),
            hashlib.sha256(b"abc").hexdigest(),
        )

    def test_decode_ascii(self):
        enc, text=decode_text(b"0:804:battle00.sab\r\n")
        self.assertEqual(enc, "utf-8")
        self.assertIn("battle00.sab", text)


if __name__=="__main__":
    unittest.main()
