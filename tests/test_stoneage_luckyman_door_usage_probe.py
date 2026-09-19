import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from tools.stoneage_luckyman_door_usage_probe import analyze, emit

TPL = b"""NPCTEMPLATE
{
templatename=L
functionset=LuckyMan
}
{
templatename=D
functionset=Door
}
"""
CREATE = b"""NPCCREATE
{
enemy=L|file:l.arg
}
{
enemy=D|100|101|secret-name|2|30|1|0
}
"""
LUCKY = b"""Stone:LV*10
main_msg:hidden
NoMoney:hidden
luck0:a,b
luck1:c
"""


class LuckyDoorUsageProbeTests(unittest.TestCase):
    def build(self):
        td = tempfile.TemporaryDirectory()
        root = Path(td.name)
        (root / "t").write_bytes(TPL)
        (root / "c").write_bytes(CREATE)
        (root / "l.arg").write_bytes(LUCKY)
        return td, root

    def test_shapes(self):
        td, root = self.build()
        try:
            result = analyze(root)
            self.assertEqual(result["counts"][("LuckyMan", "template_blocks")], 1)
            self.assertEqual(result["counts"][("Door", "template_blocks")], 1)
            self.assertEqual(result["counts"][("LuckyMan", "stable_template_names")], 1)
            self.assertEqual(result["counts"][("Door", "stable_template_names")], 1)
            self.assertEqual(result["counts"][("LuckyMan", "refs")], 1)
            self.assertEqual(result["counts"][("Door", "refs")], 1)
            self.assertEqual(
                result["values"][("LuckyMan", "stone_multiplier", 10)], 1
            )
            self.assertEqual(
                result["shapes"][("LuckyMan", "luck_key_count", 2)], 1
            )
            self.assertEqual(
                result["values"][("Door", "switch_count", 2)], 1
            )
            self.assertEqual(
                result["values"][("Door", "close_seconds", 30)], 1
            )
            self.assertEqual(
                result["counts"][("Door", "field8_absent")], 1
            )
        finally:
            td.cleanup()

    def test_output_drops_payload(self):
        td, root = self.build()
        try:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                emit(analyze(root))
            text = out.getvalue()
            for secret in ("secret-name", "hidden", "l.arg"):
                self.assertNotIn(secret, text)
            self.assertIn(
                "VALUE|LuckyMan|stone_multiplier|value=10|blocks=1", text
            )
        finally:
            td.cleanup()

    def test_create_template_name_match_is_case_insensitive(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "t").write_bytes(TPL)
            (root / "c").write_bytes(
                b"NPCCREATE\n{\nenemy=l|file:l.arg\n}\n"
                b"{\nenemy=d|1|2|n|0|5|0|0\n}\n"
            )
            (root / "l.arg").write_bytes(LUCKY)
            result = analyze(root)
            self.assertEqual(result["counts"][("LuckyMan", "refs")], 1)
            self.assertEqual(result["counts"][("Door", "refs")], 1)

    def test_numeric_and_title_field8_classification(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "t").write_bytes(TPL)
            (root / "c").write_bytes(
                b"NPCCREATE\n{\nenemy=D|1|2|n|0|5|0|0|100|x|1|2|3\n}\n"
                b"{\nenemy=D|1|2|n|0|5|0|0|title:1|x\n}\n"
            )
            result = analyze(root)
            self.assertEqual(
                result["counts"][("Door", "field8_numeric_roomadmin")], 1
            )
            self.assertEqual(
                result["counts"][("Door", "field8_title")], 1
            )


if __name__ == "__main__":
    unittest.main()
