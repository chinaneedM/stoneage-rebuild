import unittest
from tools.stoneage_waei_tw10_spr_field_diff import changed_runs,unpack_frame
class FieldDiffTests(unittest.TestCase):
    def test_runs(self): self.assertEqual(changed_runs(b"abcdef",b"abXdeY"),[(2,3),(5,6)])
    def test_frame(self):
        import struct
        d=struct.pack("<IhhH",10,-2,3,4)
        self.assertEqual(unpack_frame(d,0),{"bmp_no":10,"pos_x":-2,"pos_y":3,"sound_no":4})
if __name__=="__main__": unittest.main()
