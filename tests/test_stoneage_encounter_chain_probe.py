import contextlib,io,tempfile,unittest
from pathlib import Path
from tools.stoneage_encounter_chain_probe import analyze

def enemy(eid):
    vals=[eid,1,1,1,1,0,1,-1,0,0,1]+[0]*20
    return ",".join(["E","at","cond"]+[str(x) for x in vals])

def group(gid,eid):
    vals=[gid,-1,-1]+[eid]+[-1]*9+[100]+[-1]*9
    return ",".join(["G"]+[str(x) for x in vals])

def enc(gid,extended=True):
    vals=[1,100,10,20,30,40,5,10,4,1]+[gid]+[-1]*9+[100]+[-1]*9
    if extended:vals += [-1,-1,-1]
    return ",".join(str(x) for x in vals)

class EncounterChainProbeTests(unittest.TestCase):
    def test_crosslinks_and_schema(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);data=root/"data";data.mkdir()
            (data/"enemy.txt").write_text(enemy(7)+"\n",encoding="utf-8")
            (data/"group.txt").write_text(group(9,7)+"\n",encoding="utf-8")
            (data/"encount.txt").write_text(enc(9)+"\n",encoding="utf-8")
            setup=root/"setup.cf"
            setup.write_text("enemyfile=./data/enemy.txt\ngroupfile=./data/group.txt\nencountfile=./data/encount.txt\n",encoding="utf-8")
            _,_,_,ec,groups,e=analyze(data,setup)
            self.assertEqual(ec,1)
            self.assertTrue(groups[0]["active"])
            self.assertEqual(groups[0]["loaded_rows"][0]["_raw_unresolved"],0)
            self.assertEqual(e["rows"][0]["_unresolved"],0)
            self.assertEqual(e["schemas"]["extended_33"],1)
            self.assertEqual(groups[0]["rejected_no_enemy"],0)
            self.assertEqual(groups[0]["rejected_duplicate"],0)

    def test_blank_group_slots_remain_minus_one(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);data=root/"data";data.mkdir()
            (data/"enemy.txt").write_text(enemy(7)+"\n",encoding="utf-8")
            fields=["G","9","-1","-1","7"]+[""]*9+["100"]+[""]*9
            (data/"group.txt").write_text(",".join(fields)+"\n",encoding="utf-8")
            (data/"encount.txt").write_text(enc(9)+"\n",encoding="utf-8")
            setup=root/"setup.cf";setup.write_text("enemyfile=./data/enemy.txt\ngroupfile=./data/group.txt\nencountfile=./data/encount.txt\n",encoding="utf-8")
            *_,groups,e=analyze(data,setup)
            self.assertEqual(groups[0]["loaded_rows"][0]["ENEMY_ID2"],-1)
            self.assertEqual(e["rows"][0]["_unresolved"],0)

    def test_loader_rejects_group_with_only_unresolved_enemy_and_encount_then_dangles(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);data=root/"data";data.mkdir()
            (data/"enemy.txt").write_text(enemy(7)+"\n",encoding="utf-8")
            (data/"group.txt").write_text(group(9,999)+"\n",encoding="utf-8")
            (data/"encount.txt").write_text(enc(9)+"\n",encoding="utf-8")
            setup=root/"setup.cf";setup.write_text("enemyfile=./data/enemy.txt\ngroupfile=./data/group.txt\nencountfile=./data/encount.txt\n",encoding="utf-8")
            *_,groups,e=analyze(data,setup)
            self.assertEqual(groups[0]["rejected_no_enemy"],1)
            self.assertEqual(len(groups[0]["loaded_rows"]),0)
            self.assertEqual(e["rows"][0]["_unresolved"],1)
            self.assertEqual(e["rows"][0]["_unresolved_positive_weight"],1)

if __name__=="__main__":unittest.main()
