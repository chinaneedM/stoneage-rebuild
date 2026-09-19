import unittest
from tools.stoneage_hananet_pds_catalog_probe import Parser, query_urls

class HananetPdsCatalogProbeTests(unittest.TestCase):
    def test_anchor_and_form(self):
        p=Parser(); p.feed('<form action="sub_list.asp"><a href="sub_view.asp?app_id=1&type=H01">StoneAge</a>')
        self.assertEqual(p.forms[0][1],"GET")
        self.assertIn("StoneAge",p.anchors[0][1])
    def test_korean_query_encoded(self):
        urls=dict(query_urls())
        self.assertIn("%",urls["search-korean-euckr"])

if __name__=="__main__":unittest.main()
