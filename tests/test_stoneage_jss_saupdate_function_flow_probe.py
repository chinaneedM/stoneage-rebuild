import struct
import unittest

from tools.stoneage_jss_saupdate_function_flow_probe import (
    SEEDED_FUNCTION_RVAS,
    ascii_strings,
    mapped_import,
    recover_xref_instruction,
)


class JssSaUpdateFunctionFlowProbeTests(unittest.TestCase):
    def layout(self):
        return {"sections":[
            {"name":".text","vaddr":0x1000,"vsize":0x100,"raw_size":0x100,"raw_ptr":0x200,"chars":0x60000020},
            {"name":".rdata","vaddr":0x2000,"vsize":0x100,"raw_size":0x100,"raw_ptr":0x300,"chars":0x40000040},
        ]}

    def test_ascii_strings_maps_exact_start_va(self):
        data=bytearray(0x500)
        data[0x320:0x326]=b"hello\0"
        out=ascii_strings(bytes(data),self.layout(),0x400000)
        self.assertEqual(out[0x402020],"hello")

    def test_recover_exact_pointer_instruction(self):
        data=bytearray(0x500)
        target_rva=0x2020
        # push 0x402020 at .text raw offset 0x210
        data[0x210]=0x68
        struct.pack_into("<I",data,0x211,0x400000+target_rva)
        ins=recover_xref_instruction(
            bytes(data),self.layout(),0x400000,target_rva,0x211
        )
        self.assertIsNotNone(ins)
        self.assertEqual(ins.mnemonic,"push")
        self.assertEqual(ins.address,0x401010)

    def test_seed_roles_are_unique(self):
        roles=[role for role,_ in SEEDED_FUNCTION_RVAS]
        rvas=[rva for _,rva in SEEDED_FUNCTION_RVAS]
        self.assertEqual(len(roles),len(set(roles)))
        self.assertEqual(len(rvas),len(set(rvas)))

    def test_known_mfc_mapping(self):
        self.assertEqual(
            mapped_import("MFC42.DLL","ordinal:537"),
            "CString::CString(char const*)",
        )
        self.assertEqual(
            mapped_import("MFC42.DLL","ordinal:800"),
            "CString::~CString",
        )
        self.assertEqual(
            mapped_import("MFC42.DLL","ordinal:5444"),
            "ordinal:5444",
        )


if __name__=="__main__":
    unittest.main()
