import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from tools.stoneage_dengon_runtime_probe import (
    ENTRY_SIZE,
    EXPECTED_FILE_SIZE,
    LINE_COUNT,
    analyze,
    emit,
)


def blank_file():
    record = b"0000000000:" + b"\0" * 256 + b"\n"
    return record * LINE_COUNT


class DengonRuntimeProbeTests(unittest.TestCase):
    def test_blank_file_shape(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "Dengon").mkdir()
            (root / "Dengon" / "hidden-coordinate-name").write_bytes(
                blank_file()
            )
            result = analyze(root)
            self.assertEqual(
                result["counts"]["expected_size_files"], 1
            )
            self.assertEqual(
                result["counts"]["valid_counter_records"], 1000
            )
            self.assertEqual(
                result["counts"]["nonzero_counter_records"], 0
            )
            self.assertEqual(result["max_ids"][0], 1)
            self.assertEqual(EXPECTED_FILE_SIZE, ENTRY_SIZE * LINE_COUNT)

    def test_counter_only_zero_stub(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            d = root / "Dengon"
            d.mkdir()
            (d / "stub").write_bytes(b"0000000000:")
            result = analyze(root)
            self.assertEqual(
                result["counts"]["counter_only_stub_files"], 1
            )
            self.assertEqual(
                result["counts"]["zero_counter_stub_files"], 1
            )
            self.assertEqual(result["counts"]["records_examined"], 0)

    def test_nonzero_counter_without_payload_readout(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            d = root / "Dengon"
            d.mkdir()
            data = bytearray(blank_file())
            offset = 7 * ENTRY_SIZE
            data[offset:offset + 11] = b"0000000042:"
            (d / "secret").write_bytes(bytes(data))
            result = analyze(root)
            self.assertEqual(
                result["counts"]["nonzero_counter_records"], 1
            )
            self.assertEqual(result["max_ids"][42], 1)

    def test_output_does_not_emit_filename_or_payload(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            d = root / "Dengon"
            d.mkdir()
            data = bytearray(blank_file())
            secret = b"private-message"
            data[11:11 + len(secret)] = secret
            (d / "123_456_789").write_bytes(bytes(data))
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                emit(analyze(root))
            text = out.getvalue()
            self.assertNotIn("123_456_789", text)
            self.assertNotIn("private-message", text)

    def test_missing_directory(self):
        with tempfile.TemporaryDirectory() as td:
            result = analyze(Path(td))
            self.assertEqual(result["counts"]["directory_missing"], 1)


if __name__ == "__main__":
    unittest.main()
