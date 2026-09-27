import unittest
from tools.stoneage_2001_mainland_jinhaiwan_probe import strict, interesting_files

class JinhaiwanProbeTests(unittest.TestCase):
    def test_strict_requires_title_and_publisher(self):
        self.assertTrue(strict("石器时代网络游戏 广西金海湾电子音像出版社"))
        self.assertTrue(strict("STONEAGE 广西金海湾"))
        self.assertFalse(strict("石器时代 北京华义"))
        self.assertFalse(strict("广西金海湾 其他游戏"))
    def test_interesting_files(self):
        rows=interesting_files({"files":[{"name":"disc.iso"},{"name":"manual.pdf"},{"name":"setup.exe"}]})
        self.assertEqual([x["name"] for x in rows],["disc.iso","setup.exe"])
if __name__=="__main__": unittest.main()
