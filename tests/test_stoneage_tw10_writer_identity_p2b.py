import unittest
from tools import stoneage_tw10_writer_identity_p2b as m

class OriginalWriterBoundary(unittest.TestCase):
    def test_parent_exact_identity(self):
        self.assertEqual(sorted(m.parents()),m.EXPECTED)
        self.assertEqual(len(set(m.parents().values())),4)

    def test_local_source_labels_are_not_dataflow(self):
        self.assertEqual(m.classify({"mnemonic":"mov","operands":"eax, dword ptr [esp + 0x14]"}),"STACK_FRAME_MEMORY")
        self.assertEqual(m.classify({"mnemonic":"mov","operands":"ecx, dword ptr [esi + 0x458e28]"}),"OTHER_MEMORY")
        self.assertEqual(m.classify({"mnemonic":"add","operands":"eax, ecx"}),"COMPUTED_OR_BITWISE")
        self.assertEqual(m.classify(None),"NO_LOCAL_ASSIGNMENT")

    def test_fake_binary_cannot_be_audited(self):
        for raw in [b"",b"MZ"+b"\0"*425982,b"fake"]:
            with self.assertRaisesRegex(ValueError,"not exact authenticated retail"):
                m.audit(raw)

if __name__=="__main__":unittest.main()
