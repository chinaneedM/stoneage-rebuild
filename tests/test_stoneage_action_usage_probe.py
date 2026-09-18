import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from tools.stoneage_action_usage_probe import analyze, emit

TPL=b"""NPCTEMPLATE
{
templatename=A
functionset=Action
}
"""
CREATE=b"""NPCCREATE
{
enemy=A|file:a.arg
}
"""
ARG=b"""msgcol:7
normal:hello
attack:ouch
nod:yes
"""

class ProbeTests(unittest.TestCase):
    def build(self):
        td=tempfile.TemporaryDirectory()
        root=Path(td.name)
        (root/"t").write_bytes(TPL)
        (root/"c").write_bytes(CREATE)
        (root/"a.arg").write_bytes(ARG)
        return td,root

    def test_shape(self):
        td,root=self.build()
        try:
            r=analyze(root)
            self.assertEqual(r["counts"]["refs"],1)
            self.assertEqual(r["counts"]["resolved_files"],1)
            self.assertEqual(r["key_blocks"]["attack"],1)
            self.assertEqual(r["key_blocks"]["nod"],1)
            self.assertEqual(r["msgcol_values"][7],1)
        finally:
            td.cleanup()

    def test_output_drops_messages_and_filename(self):
        td,root=self.build()
        try:
            out=io.StringIO()
            with contextlib.redirect_stdout(out):
                emit(analyze(root))
            text=out.getvalue()
            self.assertNotIn("a.arg",text)
            self.assertNotIn("hello",text)
            self.assertNotIn("ouch",text)
            self.assertIn("KEY_BLOCK|attack|1",text)
        finally:
            td.cleanup()

    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            (root/"t").write_bytes(TPL)
            (root/"c").write_bytes(
                b"NPCCREATE\n{\nenemy=A|file:no.arg\n}\n"
            )
            self.assertEqual(analyze(root)["counts"]["missing_files"],1)

if __name__=="__main__":
    unittest.main()
