"""Negative semantic tests for original client bitmap ID -> physical 5.0 lineage."""
from copy import deepcopy
from pathlib import Path
import unittest
from tools.stoneage_tw10_cn50_static_visual_lineage import (
    build_bridge, load_sources, verify_complete_old_inheritance, git_blob_sha)


class OriginalVisualLineageP2BTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inputs = load_sources(Path(__file__).resolve().parents[1])

    def test_source_pinned_real_conclusions(self):
        record = build_bridge(*self.inputs)
        self.assertEqual(record["metrics"]["identical_cn50_rd_blocks"], 101)
        self.assertEqual(len(record["records"]), 101)
        self.assertEqual(record["records"][0]["tw10_bitmap_id"], 5846)
        self.assertEqual(record["records"][-1]["tw10_bitmap_id"], 5946)
        self.assertEqual(record["metrics"]["cn50_verified_named_npc_entities"], 0)
        self.assertFalse(record["limits"]["same_bitmap_is_same_npc_or_pet_instance"])

    def test_bytes_not_guessed(self):
        self.assertEqual(git_blob_sha(b""), "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391")

    def test_reject_fabricated_named_attribution(self):
        base, diff, custody, manifest, pins = self.inputs
        for field, value in (("npc_name", "invented"), ("original_npc_id", 10),
                             ("world_floor_id", 16000), ("drawn_npc_role_verified", True)):
            with self.subTest(field=field):
                wrong = deepcopy(base)
                wrong["rows"][0][field] = value
                with self.assertRaises(ValueError):
                    build_bridge(wrong, diff, custody, manifest, pins)

    def test_reject_mismatched_original_content(self):
        base, diff, custody, manifest, pins = self.inputs
        wrong = deepcopy(base)
        wrong["rows"][0]["map_number"] = 16001
        with self.assertRaises(ValueError):
            build_bridge(wrong, diff, custody, manifest, pins)
        wrong = deepcopy(base)
        wrong["rows"][1]["bitmapno"] = 5846
        with self.assertRaises(ValueError):
            build_bridge(wrong, diff, custody, manifest, pins)

    def test_reject_source_provenance_upgrade(self):
        base, diff, custody, manifest, pins = self.inputs
        wrong = deepcopy(diff)
        wrong["families"]["bitmap_rd"]["comparison"]["changed_payload_or_segment_count"] = 1
        with self.assertRaises(ValueError):
            build_bridge(base, wrong, custody, manifest, pins)
        wrong = deepcopy(custody)
        wrong["report_blob_sha"] = "0"*40
        with self.assertRaises(ValueError):
            build_bridge(base, diff, wrong, manifest, pins)
        wrong = deepcopy(diff)
        wrong["source_claims"]["CN50"]["official_clean_release_mastering_authenticated"] = True
        with self.assertRaises(ValueError):
            build_bridge(base, wrong, custody, manifest, pins)
