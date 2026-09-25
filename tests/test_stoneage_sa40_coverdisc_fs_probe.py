import struct,unittest
from tools.stoneage_sa40_coverdisc_fs_probe import descriptor,relevance,SECTOR
class CoverdiscTests(unittest.TestCase):
    def test_relevance_size(self):
        self.assertIn("archive_size_near_3440K",relevance("PATCH/FOO.ZIP",3440*1024))
        self.assertTrue(any(x.startswith("token:") for x in relevance("GAME/SHIQI4UP.ZIP",100)))
    def test_joliet_descriptor(self):
        b=bytearray(SECTOR);b[0]=2;b[1:6]=b"CD001";b[88:91]=b"%/E";b[156]=34
        struct.pack_into("<I",b,158,20);struct.pack_into("<I",b,166,2048)
        d=descriptor(bytes(b),17);self.assertTrue(d["joliet"]);self.assertEqual(d["root_extent"],20)
if __name__=="__main__":unittest.main()
