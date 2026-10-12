import unittest
from pathlib import Path

from tools.stoneage_tw10_savedata_geometry import (
    DEFAULT_SOURCE, PINNED_SAVEDATA_SHA256,
    geometry_from_text, format_geometry
)


def synthetic(starts=(4, 8, 12), size=16):
    lines = [
        "SAVEDATA|size=%s|sha256=%s|zero_runs=%s|zero_bytes=%s|nonzero_bytes=%s" %
        (size, PINNED_SAVEDATA_SHA256, len(starts), len(starts), size - len(starts)),
        "SAVEDATA_SPAN|first_nonzero=0|last_nonzero=%s" % (size - 1)
    ]
    lines.extend("ZERO_RUN|start=%d|length=1" % x for x in starts)
    return "\n".join(lines)


class TestTw10SavedataMetadataGeometry(unittest.TestCase):
    def test_accepted_report_geometry_not_fields(self):
        self.assertTrue(DEFAULT_SOURCE.is_file())
        g = geometry_from_text(DEFAULT_SOURCE.read_text(encoding="utf-8"))
        self.assertEqual(g.size, 128)
        self.assertEqual(g.zero_starts, (14, 28, 42, 70, 84, 98, 112))
        self.assertEqual(g.zero_lengths, (1,) * 7)
        self.assertEqual(g.start_gaps, (14, 14, 28, 14, 14, 14))
        self.assertEqual(g.largest_start_divisor, 14)
        self.assertEqual(g.largest_gap_divisor, 14)
        self.assertEqual(g.positive_multiples_unmarked, (56, 126))
        output = format_geometry(g)
        self.assertIn("GEOMETRY_ONLY", output)
        self.assertIn("NOT a proven field width", output)

    def test_synthetic_divisor_is_only_alignment(self):
        g = geometry_from_text(synthetic())
        self.assertEqual(g.largest_start_divisor, 4)
        self.assertEqual(g.positive_multiples_unmarked, ())
        self.assertEqual(g.start_gaps, (4, 4))

    def test_unrecognized_input_sha_rejected(self):
        with self.assertRaisesRegex(ValueError, "hash"):
            geometry_from_text(synthetic().replace(PINNED_SAVEDATA_SHA256, "0" * 64))

    def test_invalid_run_length_and_bounds(self):
        with self.assertRaisesRegex(ValueError, "invalid zero"):
            geometry_from_text(synthetic().replace("start=12|length=1", "start=16|length=1"))
        with self.assertRaisesRegex(ValueError, "invalid zero"):
            geometry_from_text(synthetic().replace("start=4|length=1", "start=4|length=0"))

    def test_overlaps_are_not_counted_twice(self):
        with self.assertRaisesRegex(ValueError, "overlapping"):
            geometry_from_text(synthetic((4, 4, 12)))

    def test_mismatched_counts_and_duplicate_summary_rejected(self):
        with self.assertRaisesRegex(ValueError, "summary inconsistent"):
            geometry_from_text(synthetic().replace("zero_bytes=3", "zero_bytes=2"))
        with self.assertRaisesRegex(ValueError, "exactly one"):
            geometry_from_text(synthetic() + "\n" + synthetic().splitlines()[0])

    def test_unrecognized_digest_not_allowed_even_for_valid_geometry(self):
        with self.assertRaisesRegex(ValueError, "hash"):
            geometry_from_text(synthetic(), "f" * 64)


if __name__ == "__main__":
    unittest.main()
