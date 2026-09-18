import contextlib,io,tempfile,unittest
from pathlib import Path
from tools.stoneage_gameplay_coherence_probe import analyze,emit
from tools.stoneage_encount_chain_probe import parse_group
from tools.stoneage_itemset_schema_probe import SCHEMA as ITEM_SCHEMA,INDEX as ITEM_INDEX

def eb(tempno):
    chars=["P","","","","",""];v=[0]*33
    v[0]=tempno;v[1]=1;v[2]="5.0";v[3:7]=[1,1,1,1];v[30]=1
    return ",".join(chars+[str(x) for x in v])
def item(i):
    v=["" if k=="text" else "0" for _,k in ITEM_SCHEMA];v[ITEM_INDEX["name"]]="N";v[ITEM_INDEX["id"]]=str(i)
    return ",".join(v)
def enemy(eid,temp,drop,prefix=2):
    c=["E",""]+([""] if prefix==3 else []);v=[0]*31
    v[0]=eid;v[1]=temp;v[2]=1;v[3]=1;v[4]=1;v[5]=1;v[11]=drop;v[21]=100
    return ",".join(c+[str(x) for x in v])
def group(gid,eid,cond):
    v=[-1]*23;v[0]=gid;v[1]=cond;v[3]=eid;v[13]=100
    return ",".join(["G"]+[str(x) if x!=-1 else "" for x in v])
def enc(gid):
    v=[1,1,0,0,1,1,1,2,1,1]+[-1]*20+[-1,-1,-1]
    v[10]=gid;v[20]=100
    return ",".join(str(x) if x!=-1 else "" for x in v)

class CoherenceProbeTests(unittest.TestCase):
    def test_best_tuple_tracks_coherent_snapshot(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);d=root/"data";d.mkdir()
            (d/"encount.txt").write_text(enc(10)+"\n",encoding="utf-8")
            (d/"group.txt").write_text(group(10,20,40)+"\n",encoding="utf-8")
            (d/"group1.txt").write_text(group(11,21,41)+"\n",encoding="utf-8")
            (d/"enemy.txt").write_text(enemy(20,30,40,2)+"\n",encoding="utf-8")
            (d/"enemy2.txt").write_text(enemy(21,31,41,3)+"\n",encoding="utf-8")
            (d/"enemybase.txt").write_text(eb(30)+"\n",encoding="utf-8")
            (d/"enemybase2.txt").write_text(eb(31)+"\n",encoding="utf-8")
            (d/"itemset.txt").write_text(item(40)+"\n",encoding="utf-8")
            (d/"itemset0710.txt").write_text(item(41)+"\n",encoding="utf-8")
            setup=root/"setup.cf";setup.write_text(
                "groupfile=data/group1.txt\nenemyfile=data/enemy2.txt\nenemybasefile=data/enemybase2.txt\nitemset6file=data/itemset0710.txt\n",encoding="utf-8")
            r=analyze(d,setup)
            best=r["tuples"][0]
            self.assertEqual(best["group"],"group.txt")
            self.assertEqual(best["enemy"],"enemy.txt")
            self.assertEqual(best["enemybase"],"enemybase.txt")
            self.assertEqual(best["itemset"],"itemset.txt")
            self.assertEqual(best["total"],0)
            buf=io.StringIO()
            with contextlib.redirect_stdout(buf):emit(d,setup)
            self.assertIn("SCORING|sum of unique foreign-key IDs missing",buf.getvalue())

if __name__=="__main__":unittest.main()
