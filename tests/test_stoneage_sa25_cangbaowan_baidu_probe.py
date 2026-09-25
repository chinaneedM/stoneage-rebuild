import unittest

from tools.stoneage_sa25_cangbaowan_baidu_probe import (
    SHARE,
    SHARE_ID,
    SAFE_PATTERNS,
)


class T(unittest.TestCase):
    def test_exact_share_identity(self):
        self.assertEqual(SHARE_ID,"1a2cOmPxo5GjFPFfU5Mj2Ug")
        self.assertEqual(SHARE,"https://pan.baidu.com/s/1a2cOmPxo5GjFPFfU5Mj2Ug")

    def test_safe_patterns_find_metadata(self):
        sample='{"server_filename":"StoneAge2.5.rar","size":123456789,"mtime":1730000000}'
        found={}
        for label,patt in SAFE_PATTERNS:
            m=patt.search(sample)
            if m:
                found[label]=m.group(1)
        self.assertEqual(found["server_filename"],"StoneAge2.5.rar")
        self.assertEqual(found["size"],"123456789")
        self.assertEqual(found["mtime"],"1730000000")


if __name__=="__main__":
    unittest.main()
