import contextlib,io,tempfile,unittest
from pathlib import Path
from tools.stoneage_itematom_probe import analyze,emit
from tools.stoneage_itemset_schema_probe import SCHEMA,INDEX

def item(iid,atom="",value=0):
    v=["" if k=="text" else "0" for _,k in SCHEMA]
    v[INDEX["name"]]="N";v[INDEX["id"]]=str(iid)
    if atom:
        v[INDEX["ingname0"]]=atom;v[INDEX["ingvalue0"]]=str(value)
    return ",".join(v)
def eb(atom=""):
    c=["Pet",atom,"","","",""];nums=[0]*33
    nums[0]=1;nums[1]=1;nums[2]="5.0";nums[3:7]=[1,1,1,1]
    return ",".join(c+[str(x) for x in nums])

class ItemAtomProbeTests(unittest.TestCase):
    def test_item_and_pet_atom_coverage(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);d=root/"data";d.mkdir()
            (d/"itematom.txt").write_text("wood,0,ignored-a\nmagic,1,ignored-b\n",encoding="utf-8")
            (d/"itemset.txt").write_text(item(1,"wood",3)+"\n"+item(2,"missing",4)+"\n",encoding="utf-8")
            (d/"itemset0710.txt").write_text(item(1,"magic",5)+"\n",encoding="utf-8")
            (d/"enemybase.txt").write_text(eb("wood")+"\n",encoding="utf-8")
            (d/"enemybase2.txt").write_text(eb("missing")+"\n",encoding="utf-8")
            setup=root/"setup.cf";setup.write_text("itematomfile=data/itematom.txt\nitemset6file=data/itemset.txt\nenemybasefile=data/enemybase.txt\n",encoding="utf-8")
            r=analyze(d,setup)
            self.assertEqual(len(r["atomset"]),2)
            self.assertEqual(r["flag_counts"][1],1)
            self.assertEqual(r["bad"],0)
            self.assertEqual(r["widths"][3],2)
            self.assertEqual(r["trailing"][0][3],2)
            self.assertEqual(len(r["itemsets"]["itemset.txt"]["missing"]),1)
            self.assertEqual(len(r["itemsets"]["itemset0710.txt"]["missing"]),0)
            self.assertEqual(len(r["bases"]["enemybase.txt"]["missing"]),0)
            self.assertEqual(len(r["bases"]["enemybase2.txt"]["missing"]),1)
            buf=io.StringIO()
            with contextlib.redirect_stdout(buf):emit(d,setup)
            self.assertIn("ITEMATOM_FILE_EXISTS|1",buf.getvalue())

if __name__=="__main__":unittest.main()
