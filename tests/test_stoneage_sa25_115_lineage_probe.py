import json
import unittest
from tools.stoneage_sa25_115_lineage_probe import (
    parse_cdx, norm_row, wayback_url, arquivo_url, ia_url
)

class StoneAge115LineageProbeTests(unittest.TestCase):
    def test_parse_wayback_array(self):
        body=json.dumps([
            ["timestamp","original","statuscode","mimetype","digest","length"],
            ["20110908121200","http://u.115.com/file/clnrsbsc","200","text/html","ABC","1234"],
        ]).encode()
        rows=parse_cdx(body)
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]["timestamp"],"20110908121200")
        self.assertEqual(rows[0]["original"],"http://u.115.com/file/clnrsbsc")

    def test_parse_cdxj(self):
        body=b'2011 {"url":"http://115.com/file/clnrsbsc","timestamp":"20111025234400","status":"200"}\n'
        rows=parse_cdx(body)
        self.assertEqual(len(rows),1)
        n=norm_row(rows[0])
        self.assertEqual(n["timestamp"],"20111025234400")

    def test_query_shapes(self):
        w=wayback_url("http://u.115.com/file/clnrsbsc",True)
        self.assertIn("clnrsbsc%2A",w)
        self.assertIn("statuscode%3A200",w)
        a=arquivo_url("http://u.115.com/file/clnrsbsc")
        self.assertIn("arquivo.pt",a)
        i=ia_url("clnrsbsc")
        self.assertIn("advancedsearch.php",i)
        self.assertIn("clnrsbsc",i)

if __name__=="__main__":
    unittest.main()
