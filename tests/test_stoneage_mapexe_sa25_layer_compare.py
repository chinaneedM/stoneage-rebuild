import tempfile, pathlib, struct, unittest
from tools.stoneage_mapexe_sa25_layer_compare import parse_dat, compare
class LayerCompareTests(unittest.TestCase):
    def test_layer_change_counts(self):
        def mk(tile,parts,event):
            return struct.pack("<IIHHHHHH",1,1,tile,parts,event,0,0,0)[:14]
        # build exact 1-cell DAT = 8-byte header + 6 bytes
        a=struct.pack("<IIHHH",1,1,10,20,0x4001)
        b=struct.pack("<IIHHH",1,1,11,20,0x8001)
        with tempfile.TemporaryDirectory() as d:
            pa=pathlib.Path(d)/"a.dat"; pb=pathlib.Path(d)/"b.dat"
            pa.write_bytes(a); pb.write_bytes(b)
            x=parse_dat(pa); y=parse_dat(pb); z=compare(x,y)
            self.assertEqual(z["tile_changed"],1)
            self.assertEqual(z["parts_changed"],0)
            self.assertEqual(z["event_changed"],1)
            self.assertEqual(z["event_low12_changed"],0)
            self.assertEqual(z["event_flags_changed"],1)
if __name__=="__main__": unittest.main()
