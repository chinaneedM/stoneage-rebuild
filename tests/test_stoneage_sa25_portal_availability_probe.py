import unittest
from tools.stoneage_sa25_portal_availability_probe import candidate_href, extract

class PortalAvailabilityTests(unittest.TestCase):
    def test_comment_false_positive_is_excluded(self):
        self.assertFalse(candidate_href("http://games1.sina.com.cn/cgi-bin/comment/comment.cgi?title=stoneage2.5"))
    def test_payload_and_waei_are_kept(self):
        self.assertTrue(candidate_href("http://www.waei.com.cn/files/sa25.exe"))
        self.assertTrue(candidate_href("http://mirror.example/download/client.zip"))
    def test_extract(self):
        raw='<a href="http://x/comment.cgi?title=2.5">c</a><a href="http://www.waei.com.cn/down/a.exe">d</a>'
        rows,_=extract(raw,"http://example.test/")
        self.assertEqual(rows,[("http://www.waei.com.cn/down/a.exe","http://www.waei.com.cn/down/a.exe")])

if __name__=="__main__":
    unittest.main()
