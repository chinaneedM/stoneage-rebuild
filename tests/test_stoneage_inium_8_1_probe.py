import unittest
from tools.stoneage_inium_8_1_probe import HTML_RE, Parser, normalize

class Inium81ProbeTests(unittest.TestCase):
    def test_same_host_html(self):
        self.assertTrue(HTML_RE.match("http://stoneage.enium.co.kr/8_2.htm"))
        self.assertFalse(HTML_RE.match("http://example.com/8_2.htm"))
    def test_parser_onclick(self):
        p=Parser();p.feed('<a href="8_2.htm" onclick="go(\'client.zip\')">x</a>')
        self.assertIn(("a","onclick","go('client.zip')"),p.attrs)
    def test_normalize(self):
        self.assertEqual(normalize("http://stoneage.enium.co.kr/8_1.htm","8_2.htm"),"http://stoneage.enium.co.kr/8_2.htm")

if __name__=="__main__":unittest.main()
