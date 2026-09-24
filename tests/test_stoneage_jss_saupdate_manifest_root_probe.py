import unittest

from tools.stoneage_jss_saupdate_manifest_root_probe import clean


class JssSaUpdateManifestRootProbeTests(unittest.TestCase):
    def test_clean(self):
        self.assertEqual(clean("a  b|c"),"a b%7Cc")


if __name__=="__main__":
    unittest.main()
