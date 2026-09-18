import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from tools.stoneage_npc_secondary_arg_queue_probe import analyze, emit


TEMPLATE = b"""NPCTEMPLATE
{
templatename=A
functionset=Bus
}
{
templatename=B
functionset=CheckMan
}
{
templatename=Dup
functionset=Action
}
{
templatename=Dup
functionset=Warp
}
"""

CREATE = b"""NPCCREATE
{
floorid=1
borncenter=1,1,1,1
enemy=A|file:args/a.arg
enemy=B|x:secret
enemy=B
enemy=Dup|x:ambiguous
enemy=Missing|x:unresolved
}
"""


class SecondaryArgQueueProbeTests(unittest.TestCase):
    def build(self):
        td = tempfile.TemporaryDirectory()
        root = Path(td.name)
        (root / "args").mkdir()
        (root / "all.template").write_bytes(TEMPLATE)
        (root / "world.create").write_bytes(CREATE)
        (root / "args/a.arg").write_text("hidden", encoding="utf-8")
        return td, root

    def test_counts_only_unambiguous_resolved_refs_by_functionset(self):
        td, root = self.build()
        try:
            r = analyze(root)
            self.assertEqual(r["refs"]["Bus"], 1)
            self.assertEqual(r["file_refs"]["Bus"], 1)
            self.assertEqual(r["refs"]["CheckMan"], 2)
            self.assertEqual(r["inline_refs"]["CheckMan"], 1)
            self.assertEqual(r["noarg_refs"]["CheckMan"], 1)
            self.assertEqual(r["counts"]["create_refs_ambiguous"], 1)
            self.assertEqual(r["counts"]["create_refs_unresolved"], 1)
        finally:
            td.cleanup()

    def test_missing_arg_file_is_counted_per_functionset(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "x.template").write_bytes(b"NPCTEMPLATE\n{\ntemplatename=A\nfunctionset=Bus\n}\n")
            (root / "x.create").write_bytes(
                b"NPCCREATE\n{\nfloorid=1\nborncenter=1,1,1,1\nenemy=A|file:nope.arg\n}\n"
            )
            r = analyze(root)
            self.assertEqual(r["missing_files"]["Bus"], 1)
            self.assertEqual(r["counts"]["secondary_argument_files_missing"], 1)

    def test_output_retains_functionset_but_not_payload_identity(self):
        td, root = self.build()
        try:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                emit(analyze(root))
            text = out.getvalue()
            self.assertIn("FUNCTIONSET_USAGE|Bus|", text)
            self.assertIn("FUNCTIONSET_USAGE|CheckMan|", text)
            self.assertNotIn("args/a.arg", text)
            self.assertNotIn("hidden", text)
            self.assertNotIn("x:secret", text)
            self.assertNotIn("templatename=A", text)
        finally:
            td.cleanup()


if __name__ == "__main__":
    unittest.main()
