import json
import unittest
from tools.stoneage_waei_spr1_patch_probe import parse_rows, detail_id, xpage, entropy, sha1_base32

class WaeiSpr1PatchProbeTests(unittest.TestCase):
    def test_parse(self):
        body=json.dumps([
            ["timestamp","original","statuscode"],
            ["20010605174550","http://x/spr_1.bin","200"]
        ]).encode()
        self.assertEqual(parse_rows(body)[0]["statuscode"],"200")

    def test_detail(self):
        u="http://www7.waei.net/download/dldetial.asp?ID=6&xPage=3"
        self.assertEqual(detail_id(u),"6")
        self.assertEqual(xpage(u),"3")

    def test_hash_base32(self):
        self.assertEqual(sha1_base32(b""),"3I42H3S6NNFQ2MSVX7XZKYAYSCX5QBYJ")

    def test_entropy(self):
        self.assertEqual(entropy(b"aaaa"),0.0)
        self.assertGreater(entropy(bytes(range(256))),7.9)

if __name__=="__main__":
    unittest.main()
