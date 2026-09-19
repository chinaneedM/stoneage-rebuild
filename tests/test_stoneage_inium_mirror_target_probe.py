import unittest
from tools.stoneage_inium_mirror_target_probe import Parser, normalize

class IniumMirrorTargetProbeTests(unittest.TestCase):
    def test_parser_anchor(self):
        p=Parser();p.feed('<a href="sa.exe">정식 다운로드</a>')
        self.assertIn(("a","anchor","sa.exe || 정식 다운로드"),p.attrs)
    def test_normalize(self):
        self.assertEqual(
            normalize("http://pds.hananet.net/view.asp?x=1","/files/sa.exe"),
            "http://pds.hananet.net/files/sa.exe"
        )

if __name__=="__main__":unittest.main()
