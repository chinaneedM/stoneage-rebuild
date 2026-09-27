import unittest
from tools.stoneage_waei_2001q4_external_host_probe import binary_url, score, targetish

class WaeiQ4ExternalHostProbeTests(unittest.TestCase):
    def test_binary_and_strong_scoring(self):
        u="http://games.waei.com.cn/accessories/download/stoneage2.0setup.exe"
        self.assertTrue(binary_url(u))
        self.assertTrue(targetish(u))
        self.assertGreaterEqual(score(u), 8)

    def test_generic_root_is_not_target(self):
        self.assertFalse(targetish("http://games.waei.com.cn/"))

    def test_qqskin_is_penalized(self):
        self.assertLess(
            score("http://product.waei.com.cn/qqskin/001.zip"),
            score("http://games.waei.com.cn/accessories/download/client.exe"),
        )

if __name__=="__main__":
    unittest.main()
