import contextlib,io,tempfile,unittest
from pathlib import Path
from tools.stoneage_itemset_shape_probe import analyze,emit

def row(cols,idcol,itemid,other=0):
    x=["0"]*cols
    x[0]="Name"
    x[idcol-1]=str(itemid)
    if idcol!=15 and cols>=15:x[14]=str(other)
    return ",".join(x)

class ItemsetShapeProbeTests(unittest.TestCase):
    def test_selects_unique_id_column_and_compares_files(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);data=root/"data";data.mkdir()
            (data/"itemset.txt").write_text(
                row(20,17,100,5)+"\n"+row(20,17,101,5)+"\n",encoding="utf-8")
            (data/"itemset0710.txt").write_text(
                row(15,15,100)+"\n"+row(15,15,102)+"\n",encoding="utf-8")
            setup=root/"setup.cf";setup.write_text("itemset6file=./data/itemset.txt\n",encoding="utf-8")
            r=analyze(data,setup)
            by={f["name"]:f for f in r["files"]}
            self.assertEqual(by["itemset.txt"]["selected_id_col"],17)
            self.assertEqual(by["itemset0710.txt"]["selected_id_col"],15)
            self.assertTrue(by["itemset.txt"]["active"])
            self.assertEqual(r["comparisons"][0]["intersection"],1)
            buf=io.StringIO()
            with contextlib.redirect_stdout(buf):emit(data,setup)
            self.assertIn("ID_CANDIDATE|itemset.txt|col=17",buf.getvalue())

if __name__=="__main__":unittest.main()
