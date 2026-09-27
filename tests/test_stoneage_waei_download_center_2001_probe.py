import unittest
from tools.stoneage_waei_download_center_2001_probe import (
    html_candidate,is_binary,page_score,semantics,target_link
)

class WaeiDownloadCenter2001ProbeTests(unittest.TestCase):
    def test_binary(self):
        self.assertTrue(is_binary("http://www7.waei.net/download/file/sa.exe"))
        self.assertFalse(is_binary("http://www7.waei.net/download/dldetial.asp?ID=1"))

    def test_detail_score(self):
        a={"original":"http://www7.waei.net/download/dldetial.asp?ID=5","mimetype":"text/html","timestamp":"20010104000000"}
        b={"original":"http://www7.waei.net/download/logo.gif","mimetype":"image/gif","timestamp":"20010104000000"}
        self.assertGreater(page_score(a),page_score(b))

    def test_semantics(self):
        s,t,c,d,z=semantics("<html>石器時代 試玩版 客戶端 下載 274MB</html>")
        self.assertTrue(s);self.assertTrue(t);self.assertTrue(c);self.assertTrue(d);self.assertTrue(z)

    def test_html_candidate(self):
        self.assertTrue(html_candidate({"original":"http://www7.waei.net/download/dldetial.asp?ID=1","mimetype":"text/html"}))
        self.assertFalse(html_candidate({"original":"http://www7.waei.net/download/file/x.exe","mimetype":"application/octet-stream"}))

    def test_target_link(self):
        self.assertTrue(target_link("http://x/sa.exe","石器時代下載"))
        self.assertFalse(target_link("http://x/logo.gif","首頁"))

if __name__=="__main__":
    unittest.main()
