import contextlib,io,struct,tempfile,unittest
from pathlib import Path
from tools.stoneage_dat_probe import analyze,emit,parse_dat

def rec(bitmapno,bmpnumber,hit=1,xy=(1,1)):
    b=bytearray(80); struct.pack_into("<I",b,0,bitmapno); b[28],b[29]=xy
    struct.pack_into("<H",b,30,hit); struct.pack_into("<I",b,76,bmpnumber); return bytes(b)
def dat(w,h,t,p,e):
    return struct.pack("<II",w,h)+struct.pack("<"+"H"*len(t),*t)+struct.pack("<"+"H"*len(p),*p)+struct.pack("<"+"H"*len(e),*e)

class DatProbeTests(unittest.TestCase):
    def test_layers_events_and_graphic_mapping(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); maps=root/"map"; maps.mkdir(); adrn=root/"adrn.bin"
            adrn.write_bytes(rec(0,0)+rec(1,100,0,(2,3))+rec(2,101,202,(4,5)))
            maps.joinpath("100.DAT").write_bytes(dat(2,2,[100,20,0,101],[0,101,40,60],[0xc001,0xc003,0x8002,0]))
            maps.joinpath("bgm0.DAT").write_bytes(b"xx")
            w,h,t,p,e=parse_dat(maps/"100.DAT")
            self.assertEqual((w,h),(2,2)); self.assertEqual(list(t),[100,20,0,101])
            r=analyze(maps,adrn)
            self.assertEqual(len(r["valid"]),1); self.assertEqual(len(r["invalid"]),1)
            self.assertEqual(r["event_low"][1],1); self.assertEqual(r["event_low"][3],1)
            self.assertEqual(r["both"],2)
            self.assertEqual(r["tile_graphics"]["mapped"],2)
            self.assertEqual(r["tile_graphics"]["hit"][0],1)
            self.assertEqual(r["tile_graphics"]["hit"][2],1)
            out=io.StringIO()
            with contextlib.redirect_stdout(out):emit(r)
            self.assertIn("DAT_VALID_COUNT|1",out.getvalue())
            self.assertIn("EVENT_LOW12|3|WARP|1",out.getvalue())
if __name__=="__main__":unittest.main()
