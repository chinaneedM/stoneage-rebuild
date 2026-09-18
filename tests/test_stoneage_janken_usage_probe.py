import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from tools.stoneage_janken_usage_probe import analyze,emit

TPL=b"""NPCTEMPLATE
{
templatename=J
functionset=Janken
}
"""
CREATE=b"""NPCCREATE
{
enemy=J|file:j.arg
}
"""
ARG=b"""MainMsg:x
EntryItem:100*2,200
NoItem:y
WinItem:300*3
LoseItem:400
WinWarp:1,2,3
LoseWarp:4,5,6
"""

class JankenUsageProbeTests(unittest.TestCase):
    def build(self):
        td=tempfile.TemporaryDirectory()
        root=Path(td.name)
        (root/"t").write_bytes(TPL)
        (root/"c").write_bytes(CREATE)
        (root/"j.arg").write_bytes(ARG)
        return td,root

    def test_shapes(self):
        td,root=self.build()
        try:
            result=analyze(root)
            self.assertEqual(result["counts"]["refs"],1)
            self.assertEqual(result["shapes"][("EntryItem","length",2)],1)
            self.assertEqual(result["quantities"][("EntryItem",2)],1)
            self.assertEqual(result["warp_arity"][("WinWarp",3)],1)
        finally:
            td.cleanup()

    def test_output_drops_payload(self):
        td,root=self.build()
        try:
            out=io.StringIO()
            with contextlib.redirect_stdout(out):
                emit(analyze(root))
            text=out.getvalue()
            self.assertNotIn("100*2",text)
            self.assertNotIn("1,2,3",text)
            self.assertNotIn("j.arg",text)
            self.assertIn(
                "ITEM_QUANTITY|EntryItem|quantity=2|tokens=1",text
            )
        finally:
            td.cleanup()

    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            (root/"t").write_bytes(TPL)
            (root/"c").write_bytes(
                b"NPCCREATE\n{\nenemy=J|file:no.arg\n}\n"
            )
            self.assertEqual(analyze(root)["counts"]["missing_files"],1)

if __name__=="__main__":
    unittest.main()
