import contextlib,io,tempfile,unittest
from pathlib import Path
from tools.stoneage_exp_probe import analyze,emit

class ExpProbeTests(unittest.TestCase):
    def test_exp_and_setup(self):
        with tempfile.TemporaryDirectory() as td:
            r=Path(td);e=r/"exp.txt";s=r/"setup.cf"
            e.write_text("# c\n1 10\n2 20 # x\n3 40\nbad\n",encoding="utf-8")
            s.write_text("USEREXP=data/exp.txt\nMAXLEVEL=140\nOTHER=1\n",encoding="utf-8")
            out=analyze(e,s)
            self.assertEqual(out["values"],[10,20,40])
            self.assertEqual(out["cumulative"],[10,30,70])
            self.assertEqual(len(out["malformed"]),1)
            self.assertTrue(out["sequential_labels"])
            self.assertEqual(out["setup"]["MAXLEVEL"],"140")
            buf=io.StringIO()
            with contextlib.redirect_stdout(buf):emit(out)
            self.assertIn("EXP_ROWS|3",buf.getvalue())
            self.assertIn("LEVEL_SAMPLE|2|need=20|cumulative=30",buf.getvalue())

if __name__=="__main__":unittest.main()
