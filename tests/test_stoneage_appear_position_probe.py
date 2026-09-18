import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from tools.stoneage_appear_position_probe import emit, parse


class AppearPositionProbeTests(unittest.TestCase):
    def test_whitespace_rows_and_duplicates(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "appear.txt"
            p.write_text(
                "# comment\n"
                "100 10 20\n"
                "100\t30\t40\n"
                "200   50   60\n",
                encoding="utf-8",
            )
            d = parse(p)
            self.assertEqual(len(d["rows"]), 3)
            self.assertEqual(d["unique_floors"], 2)
            self.assertEqual(d["duplicate_floor_values"], 1)
            self.assertEqual(d["duplicate_floor_extra_rows"], 1)

    def test_report_is_aggregate_only(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            data = root / "data"
            data.mkdir()
            (data / "appear.txt").write_text("12345 67 89\n", encoding="utf-8")
            setup = root / "setup.cf"
            setup.write_text(
                "appearpositionfile=data/appear.txt\n",
                encoding="utf-8",
            )
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                emit(data, setup)
            text = buf.getvalue()
            self.assertIn("VALID_ROWS|1", text)
            self.assertIn("ACTIVE_APPEAR_CONFIG|data/appear.txt", text)
            self.assertNotIn("12345 67 89", text)


if __name__ == "__main__":
    unittest.main()
