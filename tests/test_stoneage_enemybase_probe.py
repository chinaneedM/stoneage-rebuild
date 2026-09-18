import contextlib,io,tempfile,unittest
from pathlib import Path
from tools.stoneage_enemybase_probe import analyze,emit,INT_NAMES

def row(tempno=1,initnum=10):
    chars=["Pet","","","","",""]
    vals=[0]*len(INT_NAMES)
    vals[0]=tempno; vals[1]=initnum; vals[2]=5
    vals[3:7]=[10,20,30,40]
    vals[9:13]=[3,2,1,4]
    vals[19]=7; vals[30]=1234
    return ",".join(chars+[str(x) for x in vals])

class EnemyBaseProbeTests(unittest.TestCase):
    def test_structural_parse_and_active_file(self):
        with tempfile.TemporaryDirectory() as td:
            d=Path(td); data=d/"data";data.mkdir()
            (data/"enemybase.txt").write_text(row()+"\n"+row(2,11)+"\n",encoding="utf-8")
            (data/"enemybase2.txt").write_text("bad\n",encoding="utf-8")
            setup=d/"setup.cf";setup.write_text("enemybasefile=./data/enemybase.txt\n",encoding="utf-8")
            active,files=analyze(data,setup)
            self.assertEqual(active,"./data/enemybase.txt")
            self.assertEqual(len(files[0]["rows"]),2)
            self.assertEqual(files[0]["raw_row_count"],2)
            self.assertEqual(files[0]["profiles"][0][3],2)
            self.assertEqual(files[0]["profiles"][6][1],2)
            self.assertTrue(files[0]["active"])
            self.assertEqual(files[0]["elem_sums"][10],2)
            self.assertEqual(files[1]["malformed"],1)
            buf=io.StringIO()
            with contextlib.redirect_stdout(buf):emit(data,setup)
            self.assertIn("STAT|enemybase.txt|TEMPNO|min=1|max=2|unique=2",buf.getvalue())
            self.assertIn("UNIQUE_PETSKILL_IDS|enemybase.txt|1",buf.getvalue())
            self.assertIn("COLUMN_PROFILE|enemybase.txt|7|integer=2|empty=0|text=0|missing=0",buf.getvalue())

if __name__=="__main__":unittest.main()
