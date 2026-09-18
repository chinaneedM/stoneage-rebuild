import contextlib,io,tempfile,unittest
from pathlib import Path
from tools.stoneage_itemset_schema_probe import SCHEMA,INDEX
from tools.stoneage_itemset_revision_probe import analyze,emit

def row(iid,typ=16,dam="",maxd="",magic="",mp="0",image="100"):
    vals=[]
    for name,kind in SCHEMA:
        vals.append("" if kind=="text" else "0")
    vals[INDEX["name"]]="N";vals[INDEX["id"]]=str(iid);vals[INDEX["type"]]=str(typ)
    vals[INDEX["damcrushe"]]=str(dam);vals[INDEX["maxdmce"]]=str(maxd)
    vals[INDEX["magicid"]]=str(magic);vals[INDEX["magicusemp"]]=str(mp);vals[INDEX["imagenumber"]]=str(image)
    return ",".join(vals)

class ItemsetRevisionProbeTests(unittest.TestCase):
    def test_direction_and_new_types(self):
        with tempfile.TemporaryDirectory() as td:
            d=Path(td)
            (d/"itemset.txt").write_text(row(1,16,"","","",0,100)+"\n"+row(2,16,100,100,7,5,101)+"\n",encoding="utf-8")
            (d/"itemset0710.txt").write_text(row(1,16,200,200,"",0,100)+"\n"+row(2,16,150,150,8,7,101)+"\n"+row(3,31,300,300,9,10,102)+"\n",encoding="utf-8")
            r=analyze(d)
            self.assertEqual(r["b_only"],1)
            self.assertEqual(r["new_type_counts"][31],1)
            self.assertEqual(r["transitions"]["damcrushe"]["empty_to_value"],1)
            self.assertEqual(r["transitions"]["damcrushe"]["numeric_changed"],1)
            self.assertEqual(r["delta_sign"]["damcrushe"]["positive"],1)
            self.assertEqual(r["magic_added"],[8,9])
            self.assertEqual(r["magic_removed"],[7])
            buf=io.StringIO()
            with contextlib.redirect_stdout(buf):emit(d)
            self.assertIn("NEW_ID_TYPE_VALUE|31|pet_head|1",buf.getvalue())

if __name__=="__main__":unittest.main()
