import unittest
from tools.stoneage_hananet_board_post_probe import Parser, normalize

class HananetBoardPostProbeTests(unittest.TestCase):
    def test_parser(self):
        p=Parser(); p.feed('<a href="/x/stoneage.zip">다운로드</a>')
        self.assertEqual(p.links[0][2],"/x/stoneage.zip")
    def test_normalize(self):
        self.assertEqual(
            normalize("http://www.hananet.net/cgi-bin/pkboard.cgi","/a.exe"),
            "http://www.hananet.net/a.exe"
        )

if __name__=="__main__":unittest.main()
