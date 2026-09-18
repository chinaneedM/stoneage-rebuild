import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from tools.stoneage_riderman_usage_probe import analyze, emit

TPL = b"""NPCTEMPLATE
{
templatename=R
functionset=Riderman
}
"""

CREATE = b"""NPCCREATE
{
enemy=R|conff:rider.conf|foo:bar
}
"""

CONF = b"""# sample
winno=1
wintype=1
yespressed=x
gotowin=6
endbutton=x
endwin=x
winno=6
takegold=1000
letter1=123
okpressed=x
gotowin=1
endbutton=x
endwin=x
"""

class RidermanProbeTests(unittest.TestCase):
    def build(self):
        td = tempfile.TemporaryDirectory()
        root = Path(td.name)
        (root / "t").write_bytes(TPL)
        (root / "c").write_bytes(CREATE)
        (root / "rider.conf").write_bytes(CONF)
        return td, root

    def test_resolves_conff_and_tuition(self):
        td, root = self.build()
        try:
            r = analyze(root)
            self.assertEqual(r["counts"]["refs"], 1)
            self.assertEqual(r["counts"]["resolved_conff"], 1)
            self.assertEqual(r["takegold"][(6, 1000)], 1)
            self.assertEqual(r["gotowin"][(1, 6)], 1)
            self.assertEqual(r["control_key"][(6, "letter1")], 1)
        finally:
            td.cleanup()

    def test_output_drops_filename_and_item_value(self):
        td, root = self.build()
        try:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                emit(analyze(root))
            text = out.getvalue()
            self.assertNotIn("rider.conf", text)
            self.assertNotIn("123", text)
            self.assertIn("TAKEGOLD|winno=6|value=1000|refs=1", text)
        finally:
            td.cleanup()

    def test_missing_conff_file(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "t").write_bytes(TPL)
            (root / "c").write_bytes(
                b"NPCCREATE\n{\nenemy=R|conff:no.conf\n}\n"
            )
            self.assertEqual(analyze(root)["counts"]["missing_conff_file"], 1)

if __name__ == "__main__":
    unittest.main()
