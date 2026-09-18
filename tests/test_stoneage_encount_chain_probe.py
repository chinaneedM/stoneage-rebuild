import contextlib,io,tempfile,unittest
from pathlib import Path
from tools.stoneage_encount_chain_probe import analyze,emit
from tools.stoneage_itemset_schema_probe import SCHEMA as ITEM_SCHEMA,INDEX as ITEM_INDEX

def enemybase_row(tempno):
    chars=["Pet","","","","",""]
    vals=[0]*33
    vals[0]=tempno;vals[1]=1;vals[2]="5.0";vals[3:7]=[10,10,10,10]
    vals[30]=1234
    return ",".join(chars+[str(x) for x in vals])

def item_row(iid):
    vals=["" if kind=="text" else "0" for _,kind in ITEM_SCHEMA]
    vals[ITEM_INDEX["name"]]="N";vals[ITEM_INDEX["id"]]=str(iid)
    return ",".join(vals)

def enemy_row(enemyid,tempno,itemid,prefix=2):
    chars=["Enemy",""]+([""] if prefix==3 else [])
    nums=[0]*31
    nums[0]=enemyid;nums[1]=tempno;nums[2]=1;nums[3]=5
    nums[4]=2;nums[5]=1;nums[11]=itemid;nums[21]=100
    return ",".join(chars+[str(x) for x in nums])

def group_row(groupid,enemyid,itemid):
    nums=[-1]*23
    nums[0]=groupid;nums[1]=itemid
    nums[3]=enemyid;nums[13]=100
    return ",".join(["Group"]+[str(x) if x!=-1 else "" for x in nums])

def encount_row(groupid):
    vals=[0]*33
    vals[:10]=[1,100,0,0,20,20,5,10,4,1]
    vals[10:20]=[-1]*10;vals[20:30]=[-1]*10
    vals[10]=groupid;vals[20]=100
    vals[30:33]=[-1,-1,-1]
    return ",".join(str(x) if x!=-1 else "" for x in vals)

class EncountChainProbeTests(unittest.TestCase):
    def test_full_chain(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);d=root/"data";d.mkdir()
            (d/"encount.txt").write_text(encount_row(100)+"\n",encoding="utf-8")
            (d/"group.txt").write_text(group_row(100,200,400)+"\n",encoding="utf-8")
            (d/"enemy.txt").write_text(enemy_row(200,300,400,2)+"\n",encoding="utf-8")
            (d/"enemybase.txt").write_text(enemybase_row(300)+"\n",encoding="utf-8")
            (d/"itemset.txt").write_text(item_row(400)+"\n",encoding="utf-8")
            setup=root/"setup.cf"
            setup.write_text("encountfile=./data/encount.txt\ngroupfile=./data/group.txt\nenemyfile=./data/enemy.txt\nenemybasefile=./data/enemybase.txt\nitemset6file=./data/itemset.txt\n",encoding="utf-8")
            r=analyze(d,setup)
            self.assertEqual(r["enc_bad"],0);self.assertEqual(r["group_bad"],0);self.assertEqual(r["enemy_bad"],0)
            self.assertEqual(r["enc_group_missing"],[])
            self.assertEqual(r["group_enemy_missing"],[])
            self.assertEqual(r["temp_missing"],[])
            self.assertEqual(r["drop_missing"],[])
            self.assertEqual(r["cond_missing"],[])
            self.assertEqual(r["enemy_prefix"],2)
            buf=io.StringIO()
            with contextlib.redirect_stdout(buf):emit(d,setup)
            self.assertIn("ENEMY_DROP_ITEM_REF|unique=1|itemset_ids=1|matched=1|missing=0",buf.getvalue())

    def test_alternate_files_resolve_active_gaps(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);d=root/"data";d.mkdir()
            (d/"encount.txt").write_text(encount_row(100)+"\n",encoding="utf-8")
            (d/"group1.txt").write_text(group_row(101,999,0)+"\n",encoding="utf-8")
            (d/"group.txt").write_text(group_row(100,200,0)+"\n",encoding="utf-8")
            (d/"enemy.txt").write_text(enemy_row(200,300,500,2)+"\n",encoding="utf-8")
            (d/"enemy2.txt").write_text(enemy_row(999,300,500,3)+"\n",encoding="utf-8")
            (d/"enemybase.txt").write_text(enemybase_row(300)+"\n",encoding="utf-8")
            (d/"itemset.txt").write_text(item_row(400)+"\n",encoding="utf-8")
            (d/"itemset0710.txt").write_text(item_row(400)+"\n"+item_row(500)+"\n",encoding="utf-8")
            setup=root/"setup.cf"
            setup.write_text("encountfile=data/encount.txt\ngroupfile=data/group1.txt\nenemyfile=data/enemy.txt\nenemybasefile=data/enemybase.txt\nitemset6file=data/itemset.txt\n",encoding="utf-8")
            r=analyze(d,setup)
            self.assertEqual(r["enc_group_missing"],[100])
            self.assertEqual(r["group_cover"]["group.txt"]["resolves_active_missing"],1)
            self.assertEqual(r["group_enemy_missing"],[999])
            self.assertEqual(r["enemy_cover"]["enemy2.txt"]["resolves_active_missing"],1)
            self.assertEqual(r["drop_missing"],[500])
            self.assertEqual(r["item_cover"]["itemset0710.txt"]["drop_resolves_active_missing"],1)
            self.assertEqual(r["all_group_residual"],[])
            self.assertEqual(r["all_enemy_residual"],[])
            self.assertEqual(r["all_drop_residual"],[])

    def test_enemy_three_text_prefix(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);d=root/"data";d.mkdir()
            (d/"encount.txt").write_text(encount_row(100)+"\n",encoding="utf-8")
            (d/"group.txt").write_text(group_row(100,200,0)+"\n",encoding="utf-8")
            (d/"enemy2.txt").write_text(enemy_row(200,300,0,3)+"\n",encoding="utf-8")
            (d/"enemybase.txt").write_text(enemybase_row(300)+"\n",encoding="utf-8")
            (d/"itemset.txt").write_text(item_row(1)+"\n",encoding="utf-8")
            setup=root/"setup.cf"
            setup.write_text("encountfile=data/encount.txt\ngroupfile=data/group.txt\nenemyfile=data/enemy2.txt\nenemybasefile=data/enemybase.txt\nitemset6file=data/itemset.txt\n",encoding="utf-8")
            r=analyze(d,setup)
            self.assertEqual(r["enemy_prefix"],3)
            self.assertEqual(r["enemy_bad"],0)

if __name__=="__main__":unittest.main()
