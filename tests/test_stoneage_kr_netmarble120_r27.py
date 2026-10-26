import unittest
from tools import stoneage_kr_netmarble120_r27_source as source


def html(post='',title=source.TOKEN):
    return ('<html><title>'+title+'</title><body><a href="logging.php">登录</a><div id="postmessage_1">'+post+'</div></body></html>').encode()


class PublicSourceTests(unittest.TestCase):
    def inspect(self,raw,url=source.URL):return source.inspect(raw,url,200,'text/html')

    def test_explicit_single_public_file_link_is_lead_not_bytes(self):
        r=self.inspect(html('<a href="https://example.com/NetmarbleStoneAge120.exe">NetmarbleStoneAge120.exe</a>'))
        self.assertEqual(r['state'],'ONE_PUBLIC_PACKAGE_LINK_OBSERVED_NOT_YET_DOWNLOADED')
        self.assertEqual(len(r['public_package_links']),1)

    def test_generic_login_navigation_does_not_hide_public_post(self):
        r=self.inspect(html('NetmarbleStoneAge120 preserved'))
        self.assertEqual(r['state'],'NO_UNAMBIGUOUS_PUBLIC_PACKAGE_LINK_STOP')
        self.assertFalse(r['access_gate_markers'])

    def test_login_reply_credit_gate_stops_before_any_package(self):
        for text in ['您需要登录后才能查看','本帖隐藏的内容需要回复','下载附件需要积分']:
            r=self.inspect(html(text+'<a href="https://example.com/NetmarbleStoneAge120.exe">file</a>'))
            self.assertEqual(r['state'],'PUBLIC_SOURCE_ACCESS_GATED_STOP')
            self.assertEqual(r['public_package_links'],[])

    def test_wrong_thread_or_login_redirect_unqualified(self):
        for url in ['https://lab.welovesa.com/logging.php?action=login','https://lab.welovesa.com/viewthread.php?tid=1654','https://example.com/viewthread.php?tid=2117']:
            self.assertEqual(self.inspect(html(source.TOKEN),url)['state'],'SOURCE_REDIRECTED_OR_LOGIN_WALL')

    def test_scripts_hidden_links_and_navigation_not_package_candidates(self):
        raw=html('<script><a href="https://example.com/NetmarbleStoneAge120.exe">x</a></script><div style="display:none"><a href="https://example.com/NetmarbleStoneAge120.zip">x</a></div>')
        self.assertEqual(self.inspect(raw)['public_package_links'],[])

    def test_title_only_or_unrelated_file_cannot_prove_package(self):
        r=self.inspect(html('<a href="https://example.com/OtherGame.exe">other</a>'))
        self.assertEqual(r['public_package_links'],[])
        r=self.inspect(html(source.TOKEN,title='Different topic'))
        self.assertEqual(r['state'],'SOURCE_TOPIC_OR_POST_UNQUALIFIED_STOP')

    def test_two_explicit_candidates_are_not_arbitrarily_selected(self):
        r=self.inspect(html('<a href="https://example.com/NetmarbleStoneAge120.exe">a</a><a href="https://example.com/NetmarbleStoneAge120.zip">b</a>'))
        self.assertEqual(r['state'],'NO_UNAMBIGUOUS_PUBLIC_PACKAGE_LINK_STOP')
        self.assertEqual(len(r['public_package_links']),2)

    def test_network_failure_remains_one_attempt_no_download_or_absence_claim(self):
        calls=[]
        def fetch(url):calls.append(url);raise TimeoutError('synthetic')
        r=source.run(fetch)
        self.assertEqual(calls,[source.URL]);self.assertFalse(r['package']['downloaded'])
        self.assertIsNone(r['package']['sha256']);self.assertFalse(r['boundaries']['historical_package_or_site_absence_proven'])

    def test_oversized_response_is_unqualified(self):
        with self.assertRaises(ValueError):self.inspect(b'x'*(source.MAX_HTML_BYTES+1))


if __name__=='__main__':unittest.main()
