import unittest

from tools.stoneage_inium_trial_menu_probe import KEY, P, replay_urls, same_site_page


class IniumTrialMenuProbeTests(unittest.TestCase):
    def test_parser_trial_link(self):
        p=P()
        p.feed('<a href="trial.htm">체험판하기</a>')
        self.assertEqual(p.links[0][2],"trial.htm")
        self.assertTrue(KEY.search(p.links[0][3]))

    def test_same_site_page_keeps_archived_child_pages(self):
        self.assertEqual(
            same_site_page("http://stoneage.enium.co.kr/main_3.htm","trial/menu.asp?mode=demo"),
            "http://stoneage.enium.co.kr/trial/menu.asp?mode=demo",
        )
        self.assertIsNone(
            same_site_page("http://stoneage.enium.co.kr/main_3.htm","http://example.com/trial.htm")
        )
        self.assertIsNone(
            same_site_page("http://stoneage.enium.co.kr/main_3.htm","images/download.gif")
        )

    def test_replay_urls_prefer_availability_url_and_add_fallbacks(self):
        urls=replay_urls(
            "20010413160331",
            "http://stoneage.enium.co.kr/sitemap.htm",
            "http://web.archive.org/web/20010413160331/http://stoneage.enium.co.kr/sitemap.htm",
        )
        self.assertTrue(urls[0].startswith("https://web.archive.org/"))
        self.assertIn(
            "https://web.archive.org/web/20010413160331id_/http://stoneage.enium.co.kr/sitemap.htm",
            urls,
        )
        self.assertEqual(len(urls),3)

    def test_key_recognizes_exact_trial_payload_token(self):
        self.assertTrue(KEY.search("http://stoneage.hananet.net/down/sa_demo.exe"))


if __name__=="__main__":
    unittest.main()
