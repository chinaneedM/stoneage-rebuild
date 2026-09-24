import math
import struct
import unittest

from tools.stoneage_jss_launcher_deep_probe import (
    entropy,
    magic,
    parse_pe_layout,
    resource_type,
)


class JssLauncherDeepProbeTests(unittest.TestCase):
    def test_entropy_constant(self):
        self.assertEqual(entropy(b"\x00"*64),0.0)

    def test_entropy_two_symbols(self):
        self.assertAlmostEqual(entropy(b"\x00\x01"*32),1.0,places=6)

    def test_magic(self):
        self.assertEqual(magic(b"MZ"+b"\0"*8),"MZ")
        self.assertEqual(magic(b"PK\x03\x04abc"),"ZIP")
        self.assertEqual(magic(b"MSCFabc"),"CAB")

    def test_resource_type_id(self):
        self.assertEqual(resource_type({"path":("16","1","1033")}),"VERSION")
        self.assertEqual(resource_type({"path":("10","1","1033")}),"RCDATA")

    def test_minimal_pe_layout(self):
        data=bytearray(512)
        data[:2]=b"MZ"
        struct.pack_into("<I",data,0x3c,0x80)
        data[0x80:0x84]=b"PE\0\0"
        struct.pack_into("<HHIIIHH",data,0x84,0x14c,1,946684800,0,0,224,0x010f)
        opt=0x98
        struct.pack_into("<H",data,opt,0x10b)
        struct.pack_into("<I",data,opt+92,16)
        sec=opt+224
        data[sec:sec+8]=b".text\0\0\0"
        struct.pack_into("<IIII",data,sec+8,0x100,0x1000,0x100,0x100)
        out=parse_pe_layout(bytes(data))
        self.assertEqual(out["machine"],0x14c)
        self.assertEqual(out["sections"][0]["name"],".text")


if __name__=="__main__":
    unittest.main()
