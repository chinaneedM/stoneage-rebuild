import unittest

from tools.stoneage_ia_exact_artifact_audit import (
    EXACT_CLIENT,
    TARGET_ITEMS,
    source_kind,
)


class ExactIAArtifactAuditTests(unittest.TestCase):
    def test_targets_are_bounded(self):
        self.assertEqual(
            TARGET_ITEMS,
            ("stoneage_tw_2000_win", "Stoneage-5", "sa-arena"),
        )

    def test_exact_client_names(self):
        for name in (
            "sa.exe",
            "dir/sa_demo.exe",
            "StoneAge.exe",
            "payload/stone_demo.exe",
            "onlStoneAge.zip",
            "mirror/stoneagebeta.zip",
            "StoneAge.zip",
        ):
            self.assertIsNotNone(EXACT_CLIENT.search(name), name)
        self.assertIsNone(EXACT_CLIENT.search("rsa_demo.exe"))
        self.assertIsNone(EXACT_CLIENT.search("StoneAge_manual.pdf"))

    def test_source_kind(self):
        self.assertEqual(
            source_kind({"name": "disc.iso", "size": 600_000_000, "source": "original"}),
            "disc",
        )
        self.assertEqual(
            source_kind({"name": "client.zip", "size": 50_000_000, "source": "original"}),
            "zip",
        )
        self.assertEqual(
            source_kind({"name": "client.7z", "size": 50_000_000, "source": "original"}),
            "archive-metadata-only",
        )
        self.assertEqual(
            source_kind({"name": "setup.exe", "size": 10_000_000, "source": "original"}),
            "executable",
        )


if __name__ == "__main__":
    unittest.main()
