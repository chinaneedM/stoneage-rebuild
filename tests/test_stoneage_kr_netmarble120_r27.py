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


class SourceStopTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import json
        from tools import stoneage_kr_netmarble120_r27 as material
        cls.material=material;cls.source=json.loads(material.SOURCE.read_bytes())
        cls.custody=json.loads(material.CUSTODY.read_bytes());cls.doc=json.loads(material.REPORT.read_bytes())

    def test_actual_raw_report_custody_and_bounded_outcome(self):self.material.validate(self.doc)

    def test_http200_and_title_are_not_post_or_package_access(self):
        import copy
        for key,value in [('target_token_in_post',True),('public_package_links',[{'url':'invented'}])]:
            source=copy.deepcopy(self.source);source['observation'][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):self.material.build(source,self.custody)

    def test_false_download_version_or_official_identity_refused(self):
        import copy
        for key,value in [('downloaded',True),('bytes',1),('sha256','0'*64),
                          ('declared_version','1.74'),('official_clean_authenticated',True)]:
            source=copy.deepcopy(self.source);source['package'][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):self.material.build(source,self.custody)

    def test_gate_does_not_prove_absence_or_specific_login_payment_mechanism(self):
        import copy
        for key in ['historical_client_or_website_does_not_exist_proven',
                    'source_requires_specific_account_or_payment_mechanism_proven',
                    'source_workflow_success_means_download_success']:
            doc=copy.deepcopy(self.doc);doc['boundaries'][key]=True
            with self.subTest(key=key),self.assertRaises(ValueError):self.material.validate(doc)

    def test_wrong_source_custody_or_extra_artifact_member_refused(self):
        import copy
        custody=copy.deepcopy(self.custody);custody['source_job']=0
        with self.assertRaises(ValueError):self.material.build(self.source,custody)
        custody=copy.deepcopy(self.custody);custody['artifact_member_allowlist'].append('installer.exe')
        with self.assertRaises(ValueError):self.material.build(self.source,custody)


if __name__=='__main__':unittest.main()
