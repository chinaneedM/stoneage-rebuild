import unittest
from tools.stoneage_hananet_dated_download_probe import Parser, normalize

class HananetDatedDownloadProbeTests(unittest.TestCase):
    def test_parser_keeps_onclick(self):
        p=Parser();p.feed('<area href="x.htm" onclick="go(\'stoneage.zip\')">')
        self.assertIn(("area","onclick","go('stoneage.zip')"),p.attrs)
    def test_normalize_relative(self):
        self.assertEqual(
            normalize("http://stoneage.hananet.net/main.htm","files/a.exe"),
            "http://stoneage.hananet.net/files/a.exe"
        )
    def test_javascript_preserved(self):
        self.assertEqual(normalize("http://x/","javascript:go()"),"javascript:go()")

if __name__=="__main__":unittest.main()
