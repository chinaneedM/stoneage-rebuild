import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from tools.stoneage_enemybase_name_encoding_probe import analyze, emit


def _row(name: bytes, tempno: int) -> bytes:
    fields = [name, b"", b"", b"", b"", b""]
    fields += [
        str(tempno).encode("ascii"),
        b"10",
        b"5.00",
    ]
    fields += [b"0"] * 30
    return b",".join(fields)


class EnemybaseNameEncodingProbeTests(unittest.TestCase):

    def test_cp950_big5_equivalent_names_close_without_emitting_names(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            data = root / "data"
            data.mkdir()
            names = ["薩姆吉爾", "加美航空"].copy()
            payload = b"\n".join(
                _row(name.encode("cp950"), index + 1)
                for index, name in enumerate(names)
            ) + b"\n"
            (data / "enemybase.txt").write_bytes(payload)
            setup = root / "setup.cf"
            setup.write_text(
                "enemybasefile=./data/enemybase.txt\n",
                encoding="utf-8",
            )

            audit = analyze(data_dir=data, setup=setup)
            self.assertEqual(audit.row_count, 2)
            self.assertEqual(audit.count("cp950"), 2)
            self.assertEqual(audit.count("big5"), 2)
            self.assertEqual(audit.cp950_big5_different_text, 0)

            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                emit(audit)
            report = out.getvalue()
            self.assertIn(
                "RESOLUTION|RECOVERED25_ENEMYBASE_NAME_ENCODING_CLOSED_CP950",
                report,
            )
            for name in names:
                self.assertNotIn(name, report)

    def test_non_cp950_name_keeps_runtime_decoder_open(self):
        with tempfile.TemporaryDirectory() as td:
            data = Path(td)
            (data / "enemybase.txt").write_bytes(
                _row("😀".encode("utf-8"), 1) + b"\n"
            )
            audit = analyze(data_dir=data)
            self.assertEqual(audit.row_count, 1)
            self.assertNotEqual(audit.count("cp950"), 1)

            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                emit(audit)
            self.assertIn(
                "RESOLUTION|RECOVERED25_ENEMYBASE_NAME_ENCODING_OPEN",
                out.getvalue(),
            )


if __name__ == "__main__":
    unittest.main()
