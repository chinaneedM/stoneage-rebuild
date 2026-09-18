import contextlib,io,tempfile,unittest
from pathlib import Path
from tools.stoneage_itemset_schema_probe import SCHEMA,INDEX,analyze,emit

def make_row(itemid,magicid=-1,change=None):
    vals=[]
    for name,kind in SCHEMA:
        if kind=="text": vals.append("")
        elif kind=="bool": vals.append("0")
        else: vals.append("0")
    vals[INDEX["name"]]="N"
    vals[INDEX["id"]]=str(itemid)
    vals[INDEX["magicid"]]=str(magicid)
    vals[INDEX["attack_raw_a"]]="1";vals[INDEX["attack_raw_b"]]="3"
    if change:
        vals[INDEX[change[0]]]=str(change[1])
    return ",".join(vals)

class ItemsetSchemaProbeTests(unittest.TestCase):
    def test_exact_94_schema_and_magic_crosslink(self):
        self.assertEqual(len(SCHEMA),94)
        self.assertEqual(INDEX["id"]+1,17)
        self.assertEqual(INDEX["magicid"]+1,56)
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);data=root/"data";data.mkdir()
            (data/"magic.txt").write_text("M,C,F,O,7,1,1,0,\n",encoding="utf-8")
            (data/"itemset.txt").write_text(make_row(100,7)+"\n"+make_row(101,-1)+"\n",encoding="utf-8")
            (data/"itemset0710.txt").write_text(make_row(100,7,("cost",50))+"\n"+make_row(101,-1)+"\n"+make_row(102,7)+"\n",encoding="utf-8")
            setup=root/"setup.cf";setup.write_text("itemset6file=data/itemset.txt\n",encoding="utf-8")
            r=analyze(data,setup);by={f["name"]:f for f in r["files"]}
            self.assertEqual(by["itemset.txt"]["wrong_width"],0)
            self.assertEqual(sum(s["invalid"] for s in by["itemset.txt"]["stats"]),0)
            self.assertEqual(by["itemset.txt"]["magic_matched"],{7})
            d=r["diffs"][0]
            self.assertEqual(d["shared"],2)
            self.assertEqual(d["b_only"],1)
            self.assertEqual(d["changed_rows"],1)
            self.assertEqual(d["changed_cells"]["cost"],1)
            buf=io.StringIO()
            with contextlib.redirect_stdout(buf):emit(data,setup)
            self.assertIn("SCHEMA_COLUMNS|94",buf.getvalue())

    def test_bool_validation(self):
        with tempfile.TemporaryDirectory() as td:
            data=Path(td)
            (data/"itemset.txt").write_text(make_row(1,-1,("canpetmail",2))+"\n",encoding="utf-8")
            r=analyze(data)
            f=r["files"][0]
            stat=next(s for s in f["stats"] if s["name"]=="canpetmail")
            self.assertEqual(stat["invalid"],1)

if __name__=="__main__":unittest.main()
