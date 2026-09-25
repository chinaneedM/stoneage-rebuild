import tempfile, pathlib, unittest
from tools.stoneage_mapexe_sa25_compare import load_mapexe

class CompareTests(unittest.TestCase):
    def test_parse_inventory_rows(self):
        t=tempfile.NamedTemporaryFile("w",delete=False,encoding="utf-8")
        t.write("DAT|path=map/100.DAT|size=14|sha256="+"a"*64+"|width=1|height=1|cells=1|expected=14|valid_three_layer=1\n")
        t.close()
        try:
            d=load_mapexe(t.name)
            self.assertEqual(d["100.dat"]["size"],14)
            self.assertEqual(d["100.dat"]["w"],1)
            self.assertEqual(d["100.dat"]["valid"],1)
        finally:
            pathlib.Path(t.name).unlink()
if __name__=="__main__": unittest.main()
