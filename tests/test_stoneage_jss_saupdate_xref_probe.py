import struct
import unittest

from tools.stoneage_jss_saupdate_xref_probe import (
    find_va_refs,
    offset_to_rva,
    read_cstring,
)


class JssSaUpdateXrefProbeTests(unittest.TestCase):
    def layout(self):
        return {"sections":[{
            "name":".text","vaddr":0x1000,"vsize":0x100,
            "raw_size":0x100,"raw_ptr":0x200,"chars":0x60000020,
        },{
            "name":".rdata","vaddr":0x2000,"vsize":0x100,
            "raw_size":0x100,"raw_ptr":0x300,"chars":0x40000040,
        }]}

    def test_offset_to_rva(self):
        self.assertEqual(offset_to_rva(self.layout(),0x320),0x2020)

    def test_find_va_refs(self):
        data=bytearray(0x500)
        target_rva=0x2020
        data[0x210:0x214]=struct.pack("<I",0x400000+target_rva)
        refs=find_va_refs(bytes(data),self.layout(),0x400000,target_rva)
        self.assertEqual(refs,(0x1010,))

    def test_read_cstring(self):
        self.assertEqual(read_cstring(b"xxhello\0zz",2),"hello")


if __name__=="__main__":
    unittest.main()
