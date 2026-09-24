import struct
import unittest
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from tools.stoneage_jss_saupdate_call_args_probe import imm_desc, stack_args

class JssSaUpdateCallArgsProbeTests(unittest.TestCase):
    def test_manifest_http_focus_sites_are_pinned(self):
        labels=dict(FOCUS_SITES)
        self.assertEqual(labels[0x157B],"manifest-wrapper-dispatch")
        self.assertEqual(labels[0x2902],"wrapper-to-http-core")
        self.assertEqual(labels[0x2A28],"get-http-connection")
        self.assertEqual(labels[0x2D9B],"per-file-http-core-reentry")

    def decode(self,blob,va=0x401000):
        md=Cs(CS_ARCH_X86,CS_MODE_32); md.detail=True
        return list(md.disasm(blob,va))

    def test_immediate_labels(self):
        self.assertEqual(imm_desc(0,{}),"null")
        self.assertEqual(imm_desc(0x407000,{0x407000:"updated"}),"string:updated")

    def test_global_buffer_labels(self):
        self.assertEqual(
            imm_desc(0x85E6FC,{}),
            "global:sa-executable-buffer@0x85e6fc",
        )
        self.assertEqual(
            imm_desc(0x85E2FC,{}),
            "global:realbin-state-buffer@0x85e2fc",
        )

    def test_nearest_push_is_argument_one(self):
        blob=bytearray()
        blob+=b"\x6a\x00"
        blob+=b"\x68"+struct.pack("<I",0x407000)
        blob+=b"\x50"
        blob+=b"\xe8\x00\x00\x00\x00"
        insns=self.decode(bytes(blob))
        args=stack_args(insns,3,{0x407000:"updated"})
        self.assertEqual(args[0][1],"register:eax")
        self.assertEqual(args[1][1],"string:updated")
        self.assertEqual(args[2][1],"null")

if __name__=="__main__":unittest.main()
