import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from tools.stoneage_presentation_usage_probe import analyze, emit

TPL=b"""NPCTEMPLATE
{
templatename=S
functionset=SignBoard
}
{
templatename=T
functionset=TownPeople
}
{
templatename=M
functionset=Mic
}
"""
CREATE=b"""NPCCREATE
{
enemy=S|file:s.arg
}
{
enemy=T|hello,world
}
{
enemy=M|1|2|3|4|5|FREE|WIND|9
}
"""

class ProbeTests(unittest.TestCase):
    def build(self):
        td=tempfile.TemporaryDirectory()
        root=Path(td.name)
        (root/"t").write_bytes(TPL)
        (root/"c").write_bytes(CREATE)
        (root/"s.arg").write_bytes(b"text %manorid:1% tail")
        return td,root

    def test_shapes(self):
        td,root=self.build()
        try:
            r=analyze(root)
            self.assertEqual(r["counts"][("SignBoard","refs")],1)
            self.assertEqual(r["sign_modes"]["manor_placeholder"],1)
            self.assertEqual(r["town_variants"][2],1)
            self.assertEqual(r["mic_modes"]["free"],1)
            self.assertEqual(r["mic_modes"]["wind"],1)
            self.assertEqual(r["mic_modes"]["family_flag_nonzero"],1)
        finally:
            td.cleanup()

    def test_output_drops_payloads(self):
        td,root=self.build()
        try:
            out=io.StringIO()
            with contextlib.redirect_stdout(out):
                emit(analyze(root))
            text=out.getvalue()
            self.assertNotIn("hello,world",text)
            self.assertNotIn("manorid:1",text)
            self.assertNotIn("s.arg",text)
            self.assertIn("SIGNBOARD_MODE|manor_placeholder|blocks=1",text)
        finally:
            td.cleanup()

    def test_missing_sign_file(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            (root/"t").write_bytes(TPL)
            (root/"c").write_bytes(
                b"NPCCREATE\n{\nenemy=S|file:no.arg\n}\n"
            )
            r=analyze(root)
            self.assertEqual(r["counts"][("SignBoard","missing_files")],1)

if __name__=="__main__":
    unittest.main()
