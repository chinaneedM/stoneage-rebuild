import csv,gzip,tempfile,unittest
from pathlib import Path
from tools.stoneage_bitmap_id_lookup import lookup
class LookupTests(unittest.TestCase):
    def test_lookup(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"x.gz"
            with gzip.open(p,"wt",encoding="utf-8",newline="") as f:
                f.write("index\tbitmapno\tadder\n0\t10\t20\n1\t11\t30\n")
            r=lookup(p,{11,12})
            self.assertIn(11,r);self.assertNotIn(12,r)
if __name__=="__main__":unittest.main()
