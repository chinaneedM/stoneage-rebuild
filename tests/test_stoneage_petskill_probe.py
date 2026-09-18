import contextlib,io,tempfile,unittest
from pathlib import Path
from tools.stoneage_petskill_probe import analyze,emit

def enemy_row(skill):
    chars=["Pet","","","","",""]
    vals=[0]*33
    vals[0]=1; vals[1]=10; vals[2]="5.0"; vals[3:7]=[10,10,10,10]
    vals[19]=skill; vals[30]=1234
    return ",".join(chars+[str(x) for x in vals])

class PetSkillProbeTests(unittest.TestCase):
    def test_cfree_schema_and_enemybase_coverage(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); data=root/"data"; data.mkdir()
            (data/"enemybase.txt").write_text(enemy_row(10)+"\n"+enemy_row(20)+"\n",encoding="utf-8")
            # 6 char fields + 5 ints
            (data/"petskill.txt").write_text(
                "A,C,F,O,R,K,10,1,3,0,0\n"+
                "B,C,F,O,R,K,20,1,1,5,0\n"+
                "C,C,F,O,R,K,30,2,5,7,1\n",
                encoding="utf-8"
            )
            setup=root/"setup.cf"
            setup.write_text("enemybasefile=./data/enemybase.txt\npetskillfile1=./data/petskill.txt\n",encoding="utf-8")
            r=analyze(data,setup)
            f=r["files"][0]
            self.assertEqual(f["selected"],"cfree6")
            self.assertEqual(f["trailing_cols"],0)
            self.assertEqual(f["candidates"]["cfree6"]["coverage"],2)
            self.assertEqual(f["enemy_missing"],[])
            self.assertEqual(f["unreferenced"],[30])
            self.assertTrue(f["active"])
            buf=io.StringIO()
            with contextlib.redirect_stdout(buf):emit(data,setup)
            self.assertIn("ENEMYBASE_SKILL_COVERAGE|petskill.txt|covered=2|total=2|missing=0",buf.getvalue())

    def test_prefix_schema_with_trailing_unknown_column(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); data=root/"data"; data.mkdir()
            (data/"enemybase.txt").write_text(enemy_row(10)+"\n",encoding="utf-8")
            (data/"petskill.txt").write_text("A,C,F,O,R,K,10,1,3,2,100,TEXT\n",encoding="utf-8")
            setup=root/"setup.cf"; setup.write_text("enemybasefile=./data/enemybase.txt\n",encoding="utf-8")
            r=analyze(data,setup); f=r["files"][0]
            self.assertEqual(f["selected"],"cfree6")
            self.assertEqual(f["trailing_cols"],1)
            self.assertEqual(f["profiles"][11][3],1)
            self.assertEqual(f["text_stats"][11]["count"],1)
            self.assertEqual(f["text_stats"][11]["unique"],1)
            self.assertEqual(f["text_stats"][11]["minlen"],4)

    def test_legacy_and_usetype_schema_detection(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); data=root/"data"; data.mkdir()
            (data/"enemybase.txt").write_text(enemy_row(7)+"\n",encoding="utf-8")
            (data/"petskill.txt").write_text("N,C,F,O,7,1,2,3,0\n",encoding="utf-8")
            (data/"petskill1.txt").write_text("N,C,F,O,R,K,7,1,2,9,3,0\n",encoding="utf-8")
            setup=root/"setup.cf"; setup.write_text("enemybasefile=./data/enemybase.txt\n",encoding="utf-8")
            r=analyze(data,setup)
            by={f["name"]:f for f in r["files"]}
            self.assertEqual(by["petskill.txt"]["selected"],"legacy4")
            self.assertEqual(by["petskill1.txt"]["selected"],"cfree6_usetype")

if __name__=="__main__":unittest.main()
