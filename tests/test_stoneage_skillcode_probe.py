import contextlib,io,tempfile,unittest
from pathlib import Path
from tools.stoneage_skillcode_probe import analyze,emit

def enemy_row(tempno):
    chars=["Pet","","","","",""]
    vals=[0]*33
    vals[0]=tempno;vals[1]=10;vals[2]="5.0";vals[3:7]=[10,10,10,10]
    vals[30]=10000
    return ",".join(chars+[str(x) for x in vals])

class SkillCodeProbeTests(unittest.TestCase):
    def test_crosslinks_enemybase_and_kindcodes(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);data=root/"data";data.mkdir()
            (data/"enemybase.txt").write_text(enemy_row(10)+"\n"+enemy_row(20)+"\n",encoding="utf-8")
            (data/"skillcode.txt").write_text("A 100 10 ABC\nB 200 30 XYZ\n",encoding="utf-8")
            (data/"petskill.txt").write_text(
                "N,C,F,O,,AB,7,1,1,2,0,T\n"+
                "N,C,F,O,,,8,1,1,2,0,T\n"+
                "N,C,F,O,,QQ,9,1,1,2,0,T\n",encoding="utf-8")
            setup=root/"setup.cf";setup.write_text("enemybasefile=./data/enemybase.txt\n",encoding="utf-8")
            r=analyze(data,setup)
            self.assertEqual(r["matched_petids"],1)
            self.assertEqual(r["unmatched_petids"],[30])
            self.assertEqual(r["enemy_without_code"],[20])
            self.assertEqual(r["kind_nonempty"],2)
            self.assertEqual(r["kind_empty"],1)
            self.assertEqual(r["kind_match"],1)
            self.assertEqual(r["kind_nomatch"],[9])
            buf=io.StringIO()
            with contextlib.redirect_stdout(buf):emit(data,setup)
            self.assertIn("PETSKILL_KINDCODE_MATCHED_BY_ANY_CODE|1",buf.getvalue())

if __name__=="__main__":unittest.main()
