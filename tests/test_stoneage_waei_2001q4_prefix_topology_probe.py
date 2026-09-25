import unittest
from tools.stoneage_waei_2001q4_prefix_topology_probe import PREFIXES,targetish,known_nonsoftware

class WaeiQ4PrefixTopologyTests(unittest.TestCase):
    def test_both_historical_prefixes(self):
        joined="\n".join(p for _,p in PREFIXES).lower()
        self.assertIn("/zhuanqu/stoneage/",joined)
        self.assertIn("/zhuanqu/stoneage2/",joined)

    def test_targetish(self):
        self.assertTrue(targetish("http://www.waei.com.cn/ZHUANQU/stoneage2/download/client.asp"))
        self.assertTrue(targetish("http://x/setup.exe"))
        self.assertFalse(targetish("http://www.waei.com.cn/ZHUANQU/stoneage2/pet/skill.asp"))

    def test_tyro_upgrade_is_known_nonsoftware_control(self):
        u="http://www.waei.com.cn/ZHUANQU/stoneage2/tyro/upgrade.asp"
        self.assertTrue(known_nonsoftware(u))
        self.assertFalse(targetish(u))

if __name__=="__main__":
    unittest.main()
