import unittest

from tools.stoneage_hananet_pds_h01_detail_probe import extract_candidates, safe


class HananetPdsH01DetailProbeTests(unittest.TestCase):
    def test_extract_candidates(self):
        html='''<a href="sub_view.asp?app_id=123&type=H01">A</a>
        <a href="sub_view.asp?app_id=456&type=H04">B</a>
        <a href="/sub_view.asp?app_id=123&type=H01">dup</a>'''
        rows=extract_candidates(html)
        self.assertEqual(rows,[("123","http://pds.hananet.net:80/sub_view.asp?app_id=123&type=H01")])

    def test_safe(self):
        self.assertEqual(safe(" a\n b "), "a b")


if __name__=="__main__":unittest.main()
