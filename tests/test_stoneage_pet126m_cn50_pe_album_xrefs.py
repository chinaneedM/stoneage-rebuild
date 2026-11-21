"""PET126M source-bounded static instruction attribution, no runtime or pet release claims."""
import unittest
from tools.stoneage_pet126m_cn50_pe_album_xrefs import parse_objdump, locate_xrefs

class PET126MDisassembly(unittest.TestCase):
    def test_single_instruction_exact_address_and_bounded_context(self):
        text = """
 00403000: 55                   push   ebp
 00403001: b8 68 2f 48 00       mov    eax,0x482f68
 00403006: 5d                   pop    ebp
"""
        ins = parse_objdump(text)
        self.assertEqual(len(ins),3)
        out = locate_xrefs(ins,[{"file_offset":2048,"rva":0x3002}],0x400000)
        self.assertEqual(out[0]["decoded_instruction_count"],1)
        self.assertEqual(out[0]["decoded_instruction_virtual_address"],0x403001)
        self.assertEqual(out[0]["literal_offset_within_decoded_instruction"],1)
        self.assertEqual(len(out[0]["context"]),3)
        self.assertTrue(out[0]["context"][1]["contains_original_table_literal"])
        self.assertNotIn("raw_bytes",out[0]["context"][1])

    def test_unparsed_reference_is_not_promoted(self):
        ins=parse_objdump("00403000: 55 push ebp")
        out=locate_xrefs(ins,[{"file_offset":1,"rva":0x3008}],0x400000)
        self.assertEqual(out[0]["instruction_attribution"],"AMBIGUOUS_OR_UNPARSED")
        self.assertEqual(out[0]["context"],[])

    def test_reject_zero_instruction(self):
        with self.assertRaises(ValueError):
            parse_objdump("missing image data")
if __name__=="__main__":
    unittest.main()
