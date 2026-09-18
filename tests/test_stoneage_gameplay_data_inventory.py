import contextlib,hashlib,io,tempfile,unittest
from pathlib import Path
from tools.stoneage_gameplay_data_inventory import analyze,emit,labels_for

class GameplayInventoryTests(unittest.TestCase):
    def test_labels_and_map_exclusion(self):
        self.assertIn("pet",labels_for("enemybase.txt"))
        self.assertIn("item",labels_for("item/itemset.txt"))
        self.assertIn("skill_magic",labels_for("petskill.dat"))
        self.assertIn("battle_progression",labels_for("encount.tbl"))
        with tempfile.TemporaryDirectory() as td:
            r=Path(td); c=r/"client"; s=r/"server"; c.mkdir();s.mkdir()
            (c/"item.dat").write_bytes(b"abc")
            (s/"enemybase.txt").write_bytes(b"x")
            (s/"map").mkdir();(s/"map"/"100").write_bytes(b"hidden")
            (s/"misc.cfg").write_bytes(b"y")
            out=analyze(c,s)
            self.assertEqual(len(out["client"]),1)
            self.assertEqual(len(out["server"]),2)
            self.assertEqual(len(out["candidates"]),2)
            buf=io.StringIO()
            with contextlib.redirect_stdout(buf):emit(out,c,s)
            text=buf.getvalue()
            self.assertIn("CANDIDATE|client|item|item.dat|3|.dat|",text)
            self.assertIn("CANDIDATE|server|pet,character_npc_enemy|enemybase.txt|1|.txt|",text)
            self.assertNotIn("map/100",text)

if __name__=="__main__":unittest.main()
