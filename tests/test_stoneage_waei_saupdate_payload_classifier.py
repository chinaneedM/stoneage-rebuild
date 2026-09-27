import unittest
from tools.stoneage_waei_saupdate_payload_classifier import TARGETS,pe_info,sha1_b32,sigs

class WaeiSaupdatePayloadClassifierTests(unittest.TestCase):
    def test_targets(self):
        names=[x[0] for x in TARGETS]
        self.assertEqual(names,["sa40","sa42"])
        self.assertIn("sa_40.exe",TARGETS[0][2])
        self.assertIn("sa_42.exe",TARGETS[1][2])
    def test_hash_b32(self):
        self.assertEqual(sha1_b32(b""),"3I42H3S6NNFQ2MSVX7XZKYAYSCX5QBYJ")
    def test_non_pe(self):
        self.assertEqual(pe_info(b"abc")["is_mz"],0)
    def test_signature(self):
        self.assertIn(("cab",2),sigs(b"xxMSCFyy"))

if __name__=="__main__":
    unittest.main()
