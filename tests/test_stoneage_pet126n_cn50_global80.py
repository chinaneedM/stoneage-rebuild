"""PET126N synthetic PE-section and bounded source-XREF tests."""
import struct
import unittest
from tools.stoneage_pet126n_cn50_global80 import (
    immediate_refs, nearest_context, pe_sections, section_for_va
)
class Pet126N(unittest.TestCase):
    def test_pe_virtual_unbacked_data_is_not_physical_original(self):
        data=bytearray(1000)
        struct.pack_into("<I",data,0x3c,0x80)
        data[0x80:0x84]=b"PE\x00\x00"
        struct.pack_into("<H",data,0x86,1)
        struct.pack_into("<H",data,0x94,224)
        struct.pack_into("<H",data,0x98,0x10b)
        struct.pack_into("<I",data,0x98+28,0x400000)
        struct.pack_into("<I",data,0x98+56,0x5000)
        off=0x98+224
        data[off:off+8]=b".data\x00\x00\x00"
        struct.pack_into("<IIII",data,off+8,0x1000,0x2000,0x100,0x200)
        struct.pack_into("<I",data,off+36,0x80000000)
        base,size,sections=pe_sections(bytes(data))
        self.assertEqual(base,0x400000)
        self.assertEqual(size,0x5000)
        self.assertEqual(len(sections),1)
        present=section_for_va(base,sections,0x402400)
        self.assertEqual(present[0]["section"],".data")
        self.assertFalse(present[0]["backed_by_file_at_same_section_offset"])
        self.assertTrue(present[0]["writable"])
        self.assertEqual(section_for_va(base,sections,0x404000),[])
    def test_immediate_refs_count_same_hex_token_and_nearby(self):
        lines=[{"address":0x401000,"instruction":"cmp DWORD PTR [eax+0x3300cf4],0x0","encoded_length":7},
               {"address":0x401008,"instruction":"mov eax,DWORD PTR [esi+0x3300d04]","encoded_length":6},
               {"address":0x401010,"instruction":"push 0x3300cf4","encoded_length":5}]
        matches=immediate_refs(lines,0x3300cf4,16)
        self.assertEqual(len(matches),3)
        self.assertEqual([x["relative_offset"] for x in matches],[0,16,0])
        self.assertEqual(len(immediate_refs(lines,0x3300cf4)),2)
        self.assertEqual(nearest_context(lines,0x401009)["instruction"],lines[1]["instruction"])
        self.assertIsNone(nearest_context(lines,0x401020)["instruction"])

if __name__=="__main__":
    unittest.main()
