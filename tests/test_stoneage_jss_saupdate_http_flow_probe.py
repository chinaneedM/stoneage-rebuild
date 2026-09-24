import struct
import unittest

from tools.stoneage_jss_saupdate_http_flow_probe import (
    import_call_sites,
    import_thunks,
    local_call_sites,
    mapped_name,
)


class JssSaUpdateHttpFlowProbeTests(unittest.TestCase):
    def layout(self):
        return {"sections":[{
            "name":".text","vaddr":0x1000,"vsize":0x100,
            "raw_size":0x100,"raw_ptr":0x200,"chars":0x60000020,
        }]}

    def test_mapped_network_ordinal(self):
        self.assertEqual(
            mapped_name("MFC42.DLL","ordinal:3229"),
            "CInternetSession::GetHttpConnection",
        )

    def test_thunk_and_e8_call(self):
        data=bytearray(0x400)
        iat_va=0x405000
        # thunk at RVA 0x1020
        data[0x220:0x226]=b"\xff\x25"+struct.pack("<I",iat_va)
        # call from RVA 0x1010 to thunk 0x1020
        rel=0x1020-(0x1010+5)
        data[0x210]=0xe8
        struct.pack_into("<i",data,0x211,rel)
        iat={iat_va:("MFC42.DLL","ordinal:3229")}
        thunks=import_thunks(bytes(data),self.layout(),iat)
        self.assertEqual(thunks[0x1020],("MFC42.DLL","ordinal:3229"))
        calls=import_call_sites(bytes(data),self.layout(),iat,thunks)
        self.assertIn((0x1010,"MFC42.DLL","ordinal:3229","e8-thunk"),calls)

    def test_direct_ff15_call(self):
        data=bytearray(0x400)
        iat_va=0x405004
        data[0x230:0x236]=b"\xff\x15"+struct.pack("<I",iat_va)
        iat={iat_va:("MSVCRT.dll","fopen")}
        calls=import_call_sites(bytes(data),self.layout(),iat,{})
        self.assertIn((0x1030,"MSVCRT.dll","fopen","ff15"),calls)

    def test_local_call_site(self):
        data=bytearray(0x400)
        rel=0x1050-(0x1010+5)
        data[0x210]=0xe8
        struct.pack_into("<i",data,0x211,rel)
        self.assertIn((0x1010,0x1050),local_call_sites(bytes(data),self.layout()))


if __name__=="__main__":
    unittest.main()
