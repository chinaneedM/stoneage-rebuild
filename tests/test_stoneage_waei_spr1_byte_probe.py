import unittest
from tools.stoneage_waei_spr1_byte_probe import sha1b32, entropy, looks_html

class WaeiSpr1ByteProbeTests(unittest.TestCase):
    def test_sha1b32(self):
        self.assertEqual(sha1b32(b""),"3I42H3S6NNFQ2MSVX7XZKYAYSCX5QBYJ")
    def test_entropy(self):
        self.assertEqual(entropy(b"aaaa"),0.0)
        self.assertGreater(entropy(bytes(range(256))),7.9)
    def test_html(self):
        self.assertTrue(looks_html(b"<html>x</html>",{}))
        self.assertFalse(looks_html(b"\x01\x02\x03",{"Content-Type":"application/octet-stream"}))
if __name__=="__main__":
    unittest.main()
