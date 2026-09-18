import tempfile,unittest
from pathlib import Path

from tools.stoneage_pet_growth_probe import analyze


def row(tempno,base):
    chars=["Pet","","","","",""]
    vals=[0]*33
    vals[0]=tempno
    vals[1]=10
    vals[2]="5.0"
    vals[3:7]=base
    vals[30]=1234
    return ",".join(chars+[str(x) for x in vals])


class PetGrowthProbeTests(unittest.TestCase):
    def test_enemybase_rank_distribution(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);data=root/"data";data.mkdir()
            (data/"enemybase.txt").write_text(
                row(1,[25,25,25,25])+"\n"+
                row(2,[20,20,20,20])+"\n"+
                row(3,[10,10,10,10])+"\n",
                encoding="utf-8",
            )
            setup=root/"setup.cf"
            setup.write_text("enemybasefile=./data/enemybase.txt\n",encoding="utf-8")
            active,files=analyze(data,setup)
            f=files[0]
            self.assertTrue(f["active"])
            self.assertEqual(f["rank_counts"][0],1)
            self.assertEqual(f["rank_counts"][4],1)
            self.assertEqual(f["rank_counts"][5],1)
            self.assertEqual(f["min_sum"],40)
            self.assertEqual(f["max_sum"],100)


if __name__=="__main__":
    unittest.main()
