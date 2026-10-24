"""Verify source-blobs, reproducible hashes and metadata-only historical boundaries."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from stoneage_tw10_preserved25_file_intersection import replay, validate


class OriginalPreservedBridgeJoinTests(unittest.TestCase):
    def test_full_replay_and_source_pins(self):
        self.assertEqual(validate()["original_core_matched_files"], 235)

    def test_categories_do_not_promote_larger_containers(self):
        report = replay()
        a = report["by_original_file_category"]
        self.assertEqual(a["battle_map"]["sha256_matched_core_files"], 218)
        self.assertEqual(a["palette"]["sha256_matched_core_files"], 16)
        self.assertEqual(a["graphics_world"]["sha256_matched_core_files"], 0)
        self.assertEqual(a["sprite_animation"]["sha256_matched_core_files"], 0)

    def test_duplicate_bridge_paths_not_falsely_unique(self):
        report = replay()
        self.assertEqual(report["counts"]["matched_cross_archive_path_occurrences"], 237)
        self.assertEqual(len(report["matched"]), 235)
        dup = [x for x in report["matched"] if len(x["bridge_paths"]) > 1]
        self.assertEqual(len(dup), 2)
        self.assertTrue(all(x["path"].endswith(("battle145.sab", "battle146.sab"))
                            for x in dup))


if __name__ == "__main__":
    unittest.main()
