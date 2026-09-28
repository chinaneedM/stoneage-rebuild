import hashlib
import io
import struct
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from tools.stoneage_stable_map_name_encoding_probe import analyze, emit


_SHA_A = "a" * 64
_SHA_B = "b" * 64


def _lineage():
    return f"""StoneAge later field-map lineage comparison — R1
COUNT|shared_paths|2
COUNT|same_path_same_sha256|2
COUNT|same_path_changed_sha256|0
COUNT|same_sha256_and_tw1_compatible_both|2
STABLE_COMPATIBLE|path=100.dat|width=2|height=2|bytes=32|sha256={_SHA_A}|required_ids=2|required_cells=2
STABLE_COMPATIBLE|path=200.dat|width=3|height=2|bytes=44|sha256={_SHA_B}|required_ids=2|required_cells=2
RULE|same-path+same-sha256 across later corpora is strong later-lineage persistence, not proof of Taiwan-v1 membership
RESOLUTION|LATER_FIELDMAP_LINEAGE_CLASSIFIED
"""


def _server_map(
    path: Path,
    *,
    floor: int,
    width: int,
    height: int,
    name: bytes,
):
    if len(name) > 32:
        raise ValueError("test name too long")
    cells = width * height
    data = (
        b"LS2MAP"
        + struct.pack(">H", floor)
        + name.ljust(32, b"\0")
        + struct.pack(">HH", width, height)
        + b"\0\0" * cells
        + b"\0\0" * cells
    )
    path.write_bytes(data)


class StableMapNameEncodingProbeTests(unittest.TestCase):

    def test_dimension_matched_names_are_anonymous_and_consistent(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            server = root / "map"
            server.mkdir()
            lineage = root / "lineage.txt"
            lineage.write_text(_lineage(), encoding="utf-8")

            raw_name = "薩姆吉爾".encode("cp950")
            _server_map(
                server / "100a",
                floor=100,
                width=2,
                height=2,
                name=raw_name,
            )
            _server_map(
                server / "100b",
                floor=100,
                width=2,
                height=2,
                name=raw_name,
            )
            # Same floor ID but a mismatched map revision must not contribute
            # a name identity to the admitted stable candidate.
            _server_map(
                server / "100-old",
                floor=100,
                width=9,
                height=9,
                name=b"WRONG-REVISION-NAME",
            )
            _server_map(
                server / "200",
                floor=200,
                width=3,
                height=2,
                name=b"",
            )

            rows, counts = analyze(
                lineage_report=lineage,
                server_map_root=server,
            )
            by_floor = {row.floor_id: row for row in rows}

            self.assertEqual(counts["stable_floor_candidates"], 2)
            self.assertEqual(counts["stable_with_server_id"], 2)
            self.assertEqual(
                counts["stable_with_dimension_matched_server_map"],
                2,
            )
            self.assertEqual(
                counts["stable_with_duplicate_dimension_matched_server_copies"],
                1,
            )
            self.assertEqual(counts["stable_with_server_name_conflict"], 0)
            self.assertEqual(counts["stable_with_empty_server_name"], 1)

            row = by_floor[100]
            self.assertEqual(row.server_variant_count, 3)
            self.assertEqual(row.dimension_matched_variant_count, 2)
            self.assertEqual(row.name_variant_count, 1)
            self.assertEqual(
                row.raw_name_hashes,
                (hashlib.sha256(raw_name).hexdigest(),),
            )
            self.assertIn("cp950", row.decodable_encodings)

            out = io.StringIO()
            with redirect_stdout(out):
                emit(rows, counts)
            report = out.getvalue()
            self.assertNotIn("薩姆吉爾", report)
            self.assertNotIn("WRONG-REVISION-NAME", report)
            self.assertIn(hashlib.sha256(raw_name).hexdigest(), report)

    def test_dimension_matched_name_conflict_is_preserved(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            server = root / "map"
            server.mkdir()
            lineage = root / "lineage.txt"
            lineage.write_text(_lineage(), encoding="utf-8")
            _server_map(
                server / "100a",
                floor=100,
                width=2,
                height=2,
                name=b"Alpha",
            )
            _server_map(
                server / "100b",
                floor=100,
                width=2,
                height=2,
                name=b"Beta",
            )

            rows, counts = analyze(
                lineage_report=lineage,
                server_map_root=server,
            )
            row = next(r for r in rows if r.floor_id == 100)
            self.assertEqual(row.name_variant_count, 2)
            self.assertFalse(row.raw_name_consistent)
            self.assertEqual(counts["stable_with_server_name_conflict"], 1)

    def test_server_id_without_dimension_match_is_not_admitted(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            server = root / "map"
            server.mkdir()
            lineage = root / "lineage.txt"
            lineage.write_text(_lineage(), encoding="utf-8")
            _server_map(
                server / "100",
                floor=100,
                width=5,
                height=5,
                name=b"WrongDimensions",
            )

            rows, counts = analyze(
                lineage_report=lineage,
                server_map_root=server,
            )
            row = next(r for r in rows if r.floor_id == 100)
            self.assertEqual(row.server_variant_count, 1)
            self.assertFalse(row.has_dimension_matched_server_map)
            self.assertEqual(row.raw_name_hashes, ())
            self.assertEqual(
                counts["stable_with_dimension_matched_server_map"],
                0,
            )


if __name__ == "__main__":
    unittest.main()
