"""R28 source and semantic negative gates; never fetch proprietary bytes in unit tests."""
from __future__ import annotations
import copy
import hashlib
from pathlib import Path
import struct
import tempfile
import unittest

from tools import stoneage_tw85_spr137_material_r28 as r28
from tools.stoneage_cn50_spr_metadata import export_cn50_spr


class SPR137R28Tests(unittest.TestCase):
    def test_declared_original_pair_is_exact_and_nonempty(self):
        self.assertEqual(set(r28.ORIGINALS), {"spradrn_137.bin", "spr_137.bin"})
        self.assertEqual(r28.ORIGINALS["spradrn_137.bin"][0], 20868)
        self.assertEqual(r28.ORIGINALS["spr_137.bin"][0], 8721504)
        self.assertTrue(all(len(x[1]) == 64 for x in r28.ORIGINALS.values()))
        self.assertEqual(r28.CLAIM, "TW85-INSTALLER-MSI-CLIENT_UNVERIFIED_COMMUNITY_PRESERVED")

    def test_no_placeholder_or_unchecked_pair_passes(self):
        with tempfile.TemporaryDirectory() as d:
            for name, (length, _) in r28.ORIGINALS.items():
                (Path(d) / name).write_bytes(b"\x00" * min(length, 100))
            with self.assertRaisesRegex(ValueError, "length"):
                r28.qualify_pair(d)

    def test_symlink_refused_before_any_hash(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "untrusted").write_bytes(b"junk")
            (root / "spradrn_137.bin").symlink_to(root / "untrusted")
            with self.assertRaisesRegex(ValueError, "linked"):
                r28.qualify_pair(root)

    def test_exact_source_synthetic_stream_shapes(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            first = struct.pack("<IIHH", 100700, 0, 1, 0)
            header = struct.pack("<HHII", 4, 12, 800, 2)
            frames = struct.pack("<IhhH", 127292, -3, 4, 10000) + struct.pack("<IhhH", 127292, 5, -8, 0)
            (root / "idx").write_bytes(first)
            (root / "spr").write_bytes(header + frames)
            report = export_cn50_spr(root / "idx", root / "spr",
                                     root / "group.gz", root / "animation.gz", root / "frame.gz")
            self.assertEqual((report["groups"], report["animations"], report["frames"],
                              report["exact_group_spans"]), (1, 1, 2, 1))
            rows = list(r28.source_rows(root / "frame.gz"))
            self.assertEqual([(r["bmp_no"], r["pos_x"], r["sound_no"]) for r in rows],
                             [("127292", "-3", "10000"), ("127292", "5", "0")])
            self.assertEqual(list(r28.source_rows(root / "group.gz"))[0]["segment_sha256"],
                             hashlib.sha256(header + frames).hexdigest())

    def test_bad_segment_gap_and_out_of_bounds_fail(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            idx = root / "idx"
            spr = root / "spr"
            idx.write_bytes(struct.pack("<IIHH", 1, 0, 1, 0))
            spr.write_bytes(struct.pack("<HHII", 0, 0, 100, 0) + b"\0")
            with self.assertRaisesRegex(ValueError, "physical-gap"):
                export_cn50_spr(idx, spr, root / "g.gz", root / "a.gz", root / "f.gz")
            spr.write_bytes(struct.pack("<HHII", 0, 0, 100, 100000))
            with self.assertRaisesRegex(ValueError, "frame-range"):
                export_cn50_spr(idx, spr, root / "g2.gz", root / "a2.gz", root / "f2.gz")

    def test_exact_same_id_not_same_bytes_is_different_relation(self):
        groups = [
            {"index": "0", "spr_no": "100700", "segment_sha256": "a" * 64},
            {"index": "1", "spr_no": "100700", "segment_sha256": "b" * 64},
            {"index": "2", "spr_no": "999999", "segment_sha256": "c" * 64},
        ]
        refs = {
            "TW10": {100700: [{"index": 17, "segment_sha256": "a" * 64}]},
            "CN50": {100700: [{"index": 22, "segment_sha256": "b" * 64}]},
        }
        links = r28.compare(groups, refs)
        self.assertEqual(links["source_occurrences"], 3)
        self.assertEqual(links["unique_numeric_group_keys"], 2)
        self.assertEqual(links["duplicate_source_group_keys"], {"100700": 2})
        self.assertEqual(links["per_reference_relationship_counts"]["TW10"],
                         {"SAME_ID_AND_EXACT_FULL_SPR_SEGMENT": 1,
                          "SAME_ID_DIFFERENT_SPR_SEGMENT": 1})
        self.assertTrue(links["no_same_number_is_not_absence_in_other_versions"])
        self.assertTrue(links["same_number_does_not_certify_same_entity"])

    def test_original_report_has_no_source_art_and_no_semantic_fps(self):
        self.assertFalse(r28.ROOT.joinpath("research/recovered/spr_137.bin").exists())
        self.assertEqual(r28.REFERENCE_SHA256["TW10"],
                         "4db7809de4197eb90cca6dc04bda8550025e022c8232e2ebb902db0e9faf0175")
        self.assertEqual(r28.REFERENCE_SHA256["CN50"],
                         "67660d3d8ba5e05293f61f60ab3e1bfe736d7b6bdc4159ed96fcb59f5acfa228")


if __name__ == "__main__":
    unittest.main()
