import io
import struct
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from tools.stoneage_stable_map_name_decode_probe import (
    ENCODING_DISAGREEMENT,
    RESOLVED,
    TEXT_CONFLICT,
    analyze,
    emit,
)


_SHA = "a" * 64


def _lineage():
    return f"""StoneAge later field-map lineage comparison — R1
COUNT|shared_paths|1
COUNT|same_path_same_sha256|1
COUNT|same_path_changed_sha256|0
COUNT|same_sha256_and_tw1_compatible_both|1
STABLE_COMPATIBLE|path=100.dat|width=2|height=2|bytes=32|sha256={_SHA}|required_ids=2|required_cells=2
RULE|same-path+same-sha256 across later corpora is strong later-lineage persistence, not proof of Taiwan-v1 membership
RESOLUTION|LATER_FIELDMAP_LINEAGE_CLASSIFIED
"""


def _server_map(path: Path, *, name: bytes, width=2, height=2):
    cells = width * height
    path.write_bytes(
        b"LS2MAP"
        + struct.pack(">H", 100)
        + name.ljust(32, b"\0")
        + struct.pack(">HH", width, height)
        + b"\0\0" * cells
        + b"\0\0" * cells
    )


class StableMapNameDecodeProbeTests(unittest.TestCase):

    def test_big5_cp950_consensus_promotes_short_place_name(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            server = root / "map"
            server.mkdir()
            lineage = root / "lineage.txt"
            lineage.write_text(_lineage(), encoding="utf-8")
            _server_map(
                server / "100",
                name="薩姆吉爾".encode("big5"),
            )

            rows, counts = analyze(
                lineage_report=lineage,
                server_map_root=server,
            )
            self.assertEqual(len(rows), 1)
            row = rows[0]
            self.assertEqual(row.status, RESOLVED)
            self.assertEqual(row.resolved_text, "薩姆吉爾")
            self.assertEqual(counts[f"status:{RESOLVED}"], 1)

            out = io.StringIO()
            with redirect_stdout(out):
                emit(rows, counts)
            text = out.getvalue()
            self.assertIn("name=薩姆吉爾", text)
            self.assertIn("EVIDENCE_ROLE|LATER_RECOVERED", text)

    def test_server_copy_text_conflict_is_not_selected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            server = root / "map"
            server.mkdir()
            lineage = root / "lineage.txt"
            lineage.write_text(_lineage(), encoding="utf-8")
            _server_map(server / "a", name=b"Alpha")
            _server_map(server / "b", name=b"Beta")

            rows, counts = analyze(
                lineage_report=lineage,
                server_map_root=server,
            )
            row = rows[0]
            self.assertEqual(row.status, TEXT_CONFLICT)
            self.assertIsNone(row.resolved_text)
            self.assertEqual(set(row.candidate_texts), {"Alpha", "Beta"})
            self.assertEqual(counts[f"status:{TEXT_CONFLICT}"], 1)

    def test_non_big5_name_is_not_promoted(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            server = root / "map"
            server.mkdir()
            lineage = root / "lineage.txt"
            lineage.write_text(_lineage(), encoding="utf-8")
            # 0x80 is invalid as a standalone Big5/CP950 byte.
            _server_map(server / "100", name=b"bad\x80")

            rows, _counts = analyze(
                lineage_report=lineage,
                server_map_root=server,
            )
            self.assertEqual(rows[0].status, ENCODING_DISAGREEMENT)
            self.assertIsNone(rows[0].resolved_text)

    def test_report_escapes_field_delimiters(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            server = root / "map"
            server.mkdir()
            lineage = root / "lineage.txt"
            lineage.write_text(_lineage(), encoding="utf-8")
            _server_map(server / "100", name=b"A|B;C%")

            rows, counts = analyze(
                lineage_report=lineage,
                server_map_root=server,
            )
            out = io.StringIO()
            with redirect_stdout(out):
                emit(rows, counts)
            text = out.getvalue()
            self.assertIn("name=A%7CB%3BC%25", text)
            self.assertNotIn("name=A|B;C%", text)


if __name__ == "__main__":
    unittest.main()
