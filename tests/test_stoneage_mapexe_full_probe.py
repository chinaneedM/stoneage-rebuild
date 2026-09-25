import struct, unittest
from tools.stoneage_mapexe_full_probe import EXPECTED_SIZE, MAX_SIZE, dat_info
class MapExeFullProbeTests(unittest.TestCase):
    def test_bound(self):
        self.assertEqual(EXPECTED_SIZE,4223728)
        self.assertLess(EXPECTED_SIZE,MAX_SIZE)
    def test_three_layer_dat(self):
        b=struct.pack("<II",2,3)+bytes(2*3*6)
        x=dat_info(b)
        self.assertEqual((x["width"],x["height"],x["cells"],x["valid"]),(2,3,6,1))
    def test_wrong_size(self):
        b=struct.pack("<II",2,3)+bytes(5)
        self.assertEqual(dat_info(b)["valid"],0)
if __name__=="__main__": unittest.main()
