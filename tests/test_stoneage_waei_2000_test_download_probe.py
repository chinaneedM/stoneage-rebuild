import unittest
from tools.stoneage_waei_2000_test_download_probe import (
    html_candidate,
    is_binary_url,
    link_target,
    page_semantics,
    target_score,
)

class Waei2000TestDownloadProbeTests(unittest.TestCase):
    def test_binary(self):
        self.assertTrue(is_binary_url("http://x/a/setup.exe"))
        self.assertTrue(is_binary_url("http://x/a/client.zip?x=1"))
        self.assertFalse(is_binary_url("http://x/a/index.htm"))

    def test_score(self):
        good={"original":"http://www.waei.com.cn/stoneage/download/test.exe","mimetype":"application/octet-stream"}
        bad={"original":"http://www.waei.com.cn/images/logo.gif","mimetype":"image/gif"}
        self.assertGreater(target_score(good),target_score(bad))

    def test_html_candidate(self):
        self.assertTrue(html_candidate({"original":"http://www.waei.com.cn/stoneage/index.asp","mimetype":"text/html"}))
        self.assertTrue(html_candidate({"original":"http://www.waei.com.cn/download/","mimetype":"text/html"}))
        self.assertFalse(html_candidate({"original":"http://www.waei.com.cn/images/a.htm","mimetype":"text/html"}))

    def test_semantics(self):
        stones,downs,sem=page_semantics("<html>石器时代 试玩版 下载 客户端</html>")
        self.assertTrue(sem)
        self.assertTrue(stones)
        self.assertTrue(downs)

    def test_link_target(self):
        self.assertTrue(link_target("http://files.example.com/stoneage_test.exe","下载试玩版"))
        self.assertFalse(link_target("http://x/images/wallpaper.jpg","石器时代壁纸"))

if __name__=="__main__":
    unittest.main()
