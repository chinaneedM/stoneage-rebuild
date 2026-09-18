import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from tools.stoneage_windowman_usage_probe import analyze, emit

TPL=b"""NPCTEMPLATE
{
templatename=W
functionset=Windowman
}
"""
CREATE=b"""NPCCREATE
{
enemy=W|conff:w.conf
}
"""
CONF=b"""winno=1
wintype=1
yespressed=x
checkhaveitem=123
haveitemgotowin=2
endbutton=x
endwin=x
winno=2
takeitem=999
okpressed=x
gotowin=1
endbutton=x
endwin=x
"""

class ProbeTests(unittest.TestCase):
    def build(self):
        td=tempfile.TemporaryDirectory()
        root=Path(td.name)
        (root/"t").write_bytes(TPL)
        (root/"c").write_bytes(CREATE)
        (root/"w.conf").write_bytes(CONF)
        return td,root

    def test_shape(self):
        td,root=self.build()
        try:
            r=analyze(root)
            self.assertEqual(r["counts"]["refs"],1)
            self.assertEqual(r["control"][(1,"checkhaveitem")],1)
            self.assertEqual(r["control"][(2,"takeitem")],1)
            self.assertEqual(r["gotowin"][(2,1)],1)
        finally:
            td.cleanup()

    def test_output_drops_payload(self):
        td,root=self.build()
        try:
            out=io.StringIO()
            with contextlib.redirect_stdout(out):
                emit(analyze(root))
            text=out.getvalue()
            self.assertNotIn("w.conf",text)
            self.assertNotIn("123",text)
            self.assertNotIn("999",text)
            self.assertIn("key=checkhaveitem",text)
        finally:
            td.cleanup()

    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            (root/"t").write_bytes(TPL)
            (root/"c").write_bytes(
                b"NPCCREATE\n{\nenemy=W|conff:no.conf\n}\n"
            )
            self.assertEqual(analyze(root)["counts"]["missing_conff_file"],1)

if __name__=="__main__":
    unittest.main()
