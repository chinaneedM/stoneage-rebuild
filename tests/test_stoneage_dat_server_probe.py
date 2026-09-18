import struct,tempfile,unittest
from pathlib import Path
from tools.stoneage_dat_server_probe import analyze

def dat(w,h,t,p,e):
    return struct.pack("<II",w,h)+struct.pack("<"+"H"*len(t),*t)+struct.pack("<"+"H"*len(p),*p)+struct.pack("<"+"H"*len(e),*e)
def sm(mid,w,h,t,o):
    return b"LS2MAP"+struct.pack(">H",mid)+b"test\0".ljust(32,b"\0")+struct.pack(">HH",w,h)+struct.pack(">"+"H"*len(t),*t)+struct.pack(">"+"H"*len(o),*o)

class T(unittest.TestCase):
    def test_exact_and_1021_event_independence(self):
        with tempfile.TemporaryDirectory() as td:
            r=Path(td);d=r/"d";s=r/"s";d.mkdir();s.mkdir()
            (d/"100.DAT").write_bytes(dat(2,1,[1,2],[3,4],[0,3]))
            (d/"1021.dat").write_bytes(dat(1,1,[5],[6],[0xffff]))
            (s/"100").write_bytes(sm(100,2,1,[1,2],[3,4]));(s/"1021").write_bytes(sm(1021,1,1,[5],[6]))
            c,m,u,x=analyze(d,s)
            self.assertEqual(c["both_exact"],2);self.assertEqual(c["tile_diff_cells"],0);self.assertEqual(c["parts_diff_cells"],0)
            self.assertEqual(u[0][0],"1021.dat");self.assertEqual(x[0][3:],[0,0,1])
if __name__=="__main__":unittest.main()
