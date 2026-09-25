import unittest
from tools.stoneage_sa40_sina_exact_href_probe import source_hrefs

class ExactHrefProbeTests(unittest.TestCase):
    def test_extracts_complete_download_href(self):
        html=b'''<a href="http://games1.sina.com.cn/cgi-bin/games/downgames/download.pl?aid=61620&amp;col=updatex&amp;filename=shiqi4updatex_02_11_08.zip&amp;size=3440">x</a>'''
        rows=source_hrefs(html)
        self.assertEqual(len(rows),1)
        self.assertIn("aid=61620",rows[0])
        self.assertIn("filename=shiqi4updatex_02_11_08.zip",rows[0])
        self.assertIn("size=3440",rows[0])

if __name__=="__main__":
    unittest.main()
