import unittest

from tools.stoneage_jss_saupdate_token_emulation_probe import c_string


class JssSaUpdateTokenEmulationProbeTests(unittest.TestCase):
    def test_c_string(self):
        self.assertEqual(c_string(b"abc\0def"), b"abc")
        self.assertEqual(c_string(b"abc"), b"abc")


if __name__ == "__main__":
    unittest.main()
