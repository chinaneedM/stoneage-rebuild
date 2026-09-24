import unittest
from tools.stoneage_waei_pre25_upgrade_capture_probe import TIMESTAMP,ORIGINAL,extract,structural_refs,urls
class T(unittest.TestCase):
    def test_anchor(self):
        self.assertEqual(TIMESTAMP,"20011204165711"); self.assertIn("upgrade.asp",ORIGINAL)
    def test_modes(self):
        self.assertEqual([x[0] for x in urls()],["id","if","plain"])
    def test_extract(self):
        b='<body>石器时代2.0升级程序 <a href="http://x/sa_update.exe">下载</a></body>'.encode("gb18030")
        terms,hrefs,ex=extract(b); self.assertIn("升级",terms); self.assertEqual(hrefs[0][1],"http://x/sa_update.exe"); self.assertTrue(ex)
if __name__=="__main__":unittest.main()
