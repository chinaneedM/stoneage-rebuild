import contextlib,io,tempfile,unittest
from pathlib import Path
from tools.stoneage_enemy_instance_probe import (
    INT_NAMES, analyze, emit, normalize_levels, parse_enemy_row
)

def row(enemy_id=1,tempno=10,lo=3,hi=5,warp=True,create_max=2,create_min=1):
    vals=[0]*len(INT_NAMES)
    vals[0]=enemy_id;vals[1]=tempno;vals[2]=lo;vals[3]=hi
    vals[4]=create_max;vals[5]=create_min;vals[6]=2;vals[7]=-1
    vals[8]=0;vals[9]=3;vals[10]=1
    vals[11]=100;vals[21]=500
    chars=["Enemy","at=1"]+(["cond"] if warp else [])
    return ",".join(chars+[str(x) for x in vals])

def base(tempno):
    vals=["Pet","","","","","",str(tempno)]
    vals += ["0"]*32
    return ",".join(vals)

class EnemyInstanceProbeTests(unittest.TestCase):
    def test_common_and_warp_schemas(self):
        a,n,s=parse_enemy_row(row(warp=False).encode())
        self.assertEqual(n,33);self.assertEqual(s,"common_2char");self.assertEqual(a["ID"],1)
        b,n,s=parse_enemy_row(row(warp=True).encode())
        self.assertEqual(n,34);self.assertEqual(s,"warp_3char");self.assertEqual(b["TEMPNO"],10)

    def test_level_normalization_matches_loader(self):
        self.assertEqual(normalize_levels(0,7),(7,7))
        self.assertEqual(normalize_levels(9,4),(4,9))

    def test_crosslink_duplicates_and_aggregate_only_report(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);data=root/"data";data.mkdir()
            (data/"enemybase.txt").write_text(base(10)+"\n"+base(11)+"\n",encoding="utf-8")
            (data/"enemy.txt").write_text(
                row(1,10)+"\n"+row(1,99,9,4)+"\n",encoding="utf-8"
            )
            setup=root/"setup.cf"
            setup.write_text("enemyfile=./data/enemy.txt\nenemybasefile=./data/enemybase.txt\n",encoding="utf-8")
            active,basecfg,tempcount,files=analyze(data,setup)
            self.assertEqual(active,"./data/enemy.txt")
            self.assertEqual(tempcount,2)
            f=files[0]
            self.assertEqual(f["duplicate_id_values"],1)
            self.assertEqual(f["missing_temp"],1)
            self.assertEqual(f["reversed_levels"],1)
            buf=io.StringIO()
            with contextlib.redirect_stdout(buf):emit(data,setup)
            text=buf.getvalue()
            self.assertIn("UNRESOLVED_TEMPNO|enemy.txt|1",text)
            self.assertIn("SCHEMA_ROWS|enemy.txt|warp_3char|2",text)
            self.assertNotIn("Enemy,",text)
            self.assertNotIn("cond",text)

if __name__=="__main__":
    unittest.main()
