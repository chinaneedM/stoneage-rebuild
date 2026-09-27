import json
import unittest
from tools.stoneage_waei_download_center_index_census import (
    parse, detail_id, xpage, basename, classify, is_binary
)

class WaeiDownloadCenterIndexCensusTests(unittest.TestCase):
    def test_parse(self):
        body=json.dumps([
            ["timestamp","original","statuscode"],
            ["20010101000000","http://www7.waei.net/download/dldetial.asp?ID=12&xPage=1","200"],
        ]).encode()
        rows=parse(body)
        self.assertEqual(rows[0]["statuscode"],"200")

    def test_detail_id(self):
        u="http://www7.waei.net/download/dldetial.asp?ID=12&xPage=3"
        self.assertEqual(detail_id(u),"12")
        self.assertEqual(xpage(u),"3")

    def test_classify(self):
        self.assertEqual(classify("http://www7.waei.net/download/file/sa.exe"),"file")
        self.assertEqual(classify("http://www7.waei.net/download/dldetial.asp?ID=1"),"detail")
        self.assertEqual(classify("http://www7.waei.net/download/dllist.asp?xPage=1"),"list")

    def test_binary_and_basename(self):
        u="http://www7.waei.net/download/file/stoneage.exe"
        self.assertTrue(is_binary(u))
        self.assertEqual(basename(u),"stoneage.exe")

if __name__=="__main__":
    unittest.main()
