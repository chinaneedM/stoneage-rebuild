import contextlib,io,tempfile,unittest
from pathlib import Path
from tools.stoneage_magic_probe import analyze,emit

class MagicProbeTests(unittest.TestCase):
    def test_base_and_optional_idx_rows(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); data=root/"data"; data.mkdir()
            (data/"magic.txt").write_text(
                "Name,Comment,F,O,1,0,1,0\n"+
                "Name2,Comment2,F2,O2,2,1,3,1,77\n",
                encoding="utf-8"
            )
            setup=root/"setup.cf"
            setup.write_text("magicfile=./data/magic.txt\n",encoding="utf-8")
            r=analyze(data,setup)
            self.assertTrue(r["active_match"])
            self.assertEqual(r["parsed_rows"],2)
            self.assertEqual(r["malformed"],0)
            self.assertEqual(r["field_counts"][8],1)
            self.assertEqual(r["field_counts"][9],1)
            self.assertEqual(r["counters"]["TARGET_DEADFLG"][1],1)
            self.assertEqual(r["counters"]["EFFECTIVE_TARGET"][103],1)
            self.assertEqual(r["counters"]["IDX"][77],1)
            buf=io.StringIO()
            with contextlib.redirect_stdout(buf): emit(data,setup)
            self.assertIn("ID_STAT|magic.txt|min=1|max=2|unique=2|duplicates=0",buf.getvalue())

    def test_malformed_numeric_column(self):
        with tempfile.TemporaryDirectory() as td:
            data=Path(td)
            (data/"magic.txt").write_text("N,C,F,O,1,X,1,0\n",encoding="utf-8")
            r=analyze(data)
            self.assertEqual(r["parsed_rows"],0)
            self.assertEqual(r["malformed"],1)

if __name__=="__main__": unittest.main()
