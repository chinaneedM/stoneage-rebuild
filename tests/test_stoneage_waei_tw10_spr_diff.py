import unittest
from tools.stoneage_waei_tw10_spr_diff import parse_index, validate_spr, diff_runs

class SprDiffTests(unittest.TestCase):
    def test_diff_runs(self):
        n,r=diff_runs(b"abcdef",b"abXdeY")
        self.assertEqual(n,2)
        self.assertEqual(r,((2,3),(5,6)))
    def test_empty_index(self):
        groups,a,f=validate_spr(b"",b"")
        self.assertEqual(groups,())
        self.assertEqual((a,f),(0,0))
    def test_parse_index(self):
        import struct
        d=struct.pack("<IIHH",1,0,0,0)
        self.assertEqual(parse_index(d),((1,0,0,0),))
if __name__=="__main__":
    unittest.main()
