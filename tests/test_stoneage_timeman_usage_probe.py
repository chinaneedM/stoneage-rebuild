import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from tools.stoneage_timeman_usage_probe import analyze, emit

TPL = b"""NPCTEMPLATE
{
templatename=T
functionset=TimeMan
}
"""

CREATE = b"""NPCCREATE
{
enemy=T|file:t.arg
}
"""

ARG = b"""time:ALLNOON
change_no:CLS
main_msg:a,b
change_msg:c
"""

class TimeManUsageProbeTests(unittest.TestCase):
    def build(self):
        td = tempfile.TemporaryDirectory()
        root = Path(td.name)
        (root / "t").write_bytes(TPL)
        (root / "c").write_bytes(CREATE)
        (root / "t.arg").write_bytes(ARG)
        return td, root

    def test_shape(self):
        td, root = self.build()
        try:
            r = analyze(root)
            self.assertEqual(r["counts"]["refs"], 1)
            self.assertEqual(r["counts"]["resolved_files"], 1)
            self.assertEqual(r["time_resolved"][("ALLNOON", 701, 300)], 1)
            self.assertEqual(r["change_modes"]["cls_hidden"], 1)
            self.assertEqual(r["message_counts"][("main_msg", 2)], 1)
        finally:
            td.cleanup()

    def test_output_drops_dialogue_and_filename(self):
        td, root = self.build()
        try:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                emit(analyze(root))
            text = out.getvalue()
            self.assertNotIn("t.arg", text)
            self.assertNotIn("a,b", text)
            self.assertIn("CHANGE_MODE|cls_hidden|blocks=1", text)
        finally:
            td.cleanup()

    def test_unknown_time(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "t").write_bytes(TPL)
            (root / "c").write_bytes(
                b"NPCCREATE\n{\nenemy=T|time:UNKNOWN\n}\n"
            )
            r = analyze(root)
            self.assertEqual(r["counts"]["missing_or_unknown_time"], 1)
            self.assertEqual(r["counts"]["inline"], 1)

if __name__ == "__main__":
    unittest.main()
