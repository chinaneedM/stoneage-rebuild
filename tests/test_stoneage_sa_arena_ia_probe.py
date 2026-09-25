import struct
import unittest

from tools.stoneage_sa_arena_ia_probe import (
    SECTOR, dir_range, optical_candidates, parse_directory, parse_pvd
)


def record(name,extent,size,is_dir=False):
    raw=name if isinstance(name,bytes) else name.encode("ascii")
    n=33+len(raw)+(0 if len(raw)%2 else 1)
    b=bytearray(n)
    b[0]=n
    struct.pack_into("<I",b,2,extent)
    struct.pack_into("<I",b,10,size)
    b[25]=2 if is_dir else 0
    b[32]=len(raw)
    b[33:33+len(raw)]=raw
    return bytes(b)


class SaArenaIAProbeTests(unittest.TestCase):
    def test_optical_candidate_filter(self):
        rows=[
            {"name":"disc.iso","source":"original"},
            {"name":"cover.jpg"},
            {"name":"track.bin"},
        ]
        self.assertEqual([r["name"] for r in optical_candidates(rows)],["disc.iso","track.bin"])

    def test_parse_pvd(self):
        b=bytearray(SECTOR)
        b[0]=1
        b[1:6]=b"CD001"
        b[8:40]=b"TESTSYS".ljust(32,b" ")
        b[40:72]=b"STONEAGE".ljust(32,b" ")
        struct.pack_into("<I",b,80,12345)
        rr=record(b"\x00",22,4096,True)
        b[156:156+len(rr)]=rr
        got=parse_pvd(bytes(b))
        self.assertEqual(got["volume_id"],"STONEAGE")
        self.assertEqual(got["root_extent"],22)
        self.assertEqual(got["root_size"],4096)

    def test_directory_parser(self):
        body=bytearray(SECTOR)
        a=record(b"\x00",20,SECTOR,True)
        b=record("SETUP.EXE;1",30,1234,False)
        body[:len(a)]=a
        body[len(a):len(a)+len(b)]=b
        rows=parse_directory(bytes(body))
        self.assertEqual(rows[0]["name"],".")
        self.assertEqual(rows[1]["name"],"SETUP.EXE")
        self.assertFalse(rows[1]["is_dir"])

    def test_dir_range_is_capped(self):
        start,end=dir_range(10,9999999)
        self.assertEqual(start,10*SECTOR)
        self.assertLessEqual(end-start+1,262144)


if __name__=="__main__":
    unittest.main()
