import unittest

from tools.stoneage_waei_2001q4_launch_window_probe import (
    candidate_ref,
    child_link,
    extract_links,
    score_page,
    semantic_match,
)


class WaeiQ4LaunchWindowProbeTests(unittest.TestCase):
    def test_news_launch_page_scores_above_qqskin_noise(self):
        news = {
            "original": "http://www.waei.com.cn/ZHUANQU/stoneage2/stnews/index.asp",
            "timestamp": "20011102090000",
            "mimetype": "text/html",
        }
        skin = {
            "original": "http://www.waei.com.cn/ZHUANQU/stoneage2/qqskin/index.asp?page=1",
            "timestamp": "20011102090000",
            "mimetype": "text/html",
        }
        self.assertGreater(score_page(news), score_page(skin))

    def test_semantic_match_requires_stoneage_and_download_context(self):
        self.assertTrue(semantic_match("石器时代2.0完整升级版客户端下载"))
        self.assertFalse(semantic_match("石器时代2.0宠物介绍"))
        self.assertFalse(semantic_match("普通软件下载中心"))

    def test_candidate_ref_rejects_known_noise(self):
        self.assertTrue(candidate_ref("http://202.1.2.3/down/stoneage.exe", "下载客户端"))
        self.assertTrue(candidate_ref("http://mirror.example/stoneage2.0setup.exe", "完整升级版"))
        self.assertFalse(candidate_ref("http://product.waei.com.cn/qqskin/160.zip", "立即下载"))
        self.assertFalse(candidate_ref("http://www.waei.com.cn/ZHUANQU/stoneage2/service/record.zip", "数据处理表格"))

    def test_child_link_is_official_html_semantic_only(self):
        self.assertTrue(child_link(
            "http://www.waei.com.cn/ZHUANQU/stoneage2/stnews/client.asp",
            "完整升级版",
        ))
        self.assertFalse(child_link(
            "http://www.waei.com.cn/ZHUANQU/stoneage2/qqskin/index.asp",
            "下载",
        ))
        self.assertFalse(child_link(
            "http://outside.example/client.asp",
            "石器时代2.0客户端",
        ))

    def test_extract_links_resolves_relative_url(self):
        h = '<a href="../down/client.asp">石器时代2.0完整升级版</a>'
        out = extract_links(
            h,
            "http://www.waei.com.cn/ZHUANQU/stoneage2/stnews/index.asp",
        )
        self.assertEqual(
            out[0][0],
            "http://www.waei.com.cn/ZHUANQU/stoneage2/down/client.asp",
        )


if __name__ == "__main__":
    unittest.main()
