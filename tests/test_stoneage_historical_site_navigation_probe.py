import unittest
from tools.stoneage_historical_site_navigation_probe import qualify, derived_links


class NavigationTests(unittest.TestCase):
    def url(self, date='20010418090000', original='http://www.titan.co.jp/stoneage/manual.html'):
        return f'https://web.archive.org/web/{date}id_/{original}'

    def doc(self):
        return '<html>STONEAGE<a href="manual02.html#7030">ペット</a><frame src="nav.html"><a href="client.exe">Download</a></html>'.encode('shift_jis')

    def test_actual_capture_not_requested_date_and_no_visual_claim(self):
        r = qualify('jss_manual_index', self.doc(), self.url())
        self.assertEqual(r['actual_capture'], '20010418090000')
        self.assertNotEqual(r['actual_capture'], r['requested_timestamp'])
        self.assertFalse(r['visual_layout_verified']); self.assertFalse(r['linked_destination_contents_verified'])
        self.assertEqual(r['links'][0]['topic_candidates'], ['pet_species'])

    def test_frame_anchor_and_download_are_distinct(self):
        rows = qualify('jss_manual_index', self.doc(), self.url())['links']
        self.assertEqual(rows[0]['target_url'], 'http://www.titan.co.jp/stoneage/manual02.html#7030')
        self.assertEqual(rows[1]['link_kind'], 'FRAME')
        self.assertEqual(rows[2]['target_kind'], 'DOWNLOAD_REFERENCE_NOT_FETCHED')
        self.assertNotIn('label', rows[0])

    def test_wrong_origin_path_future_date_and_non_html_rejected(self):
        for url in [self.url('20100101000000'), self.url(original='http://example.com/stoneage/manual.html'), self.url(original='http://www.titan.co.jp/other.html'), 'https://example.com/']:
            with self.subTest(url=url), self.assertRaises(ValueError): qualify('jss_manual_index', self.doc(), url)
        with self.assertRaises(ValueError): qualify('jss_manual_index', b'error STONEAGE', self.url())

    def test_base_and_rewritten_links_do_not_keep_archive_toolbar_origin(self):
        rows = derived_links('<base href="http://www.titan.co.jp/stoneage/"><a href="https://web.archive.org/web/20010418090000id_/http://www.titan.co.jp/stoneage/manual02.html">manual</a>', 'http://www.titan.co.jp/stoneage/manual.html')
        self.assertEqual(rows[0]['target_url'], 'http://www.titan.co.jp/stoneage/manual02.html')
        self.assertTrue(rows[0]['same_host'])

    def test_active_schemes_and_credentials_excluded(self):
        rows = derived_links('<a href="javascript:alert(1)">x</a><a href="mailto:x@y">y</a><a href="https://user:pass@example.com/">z</a>', 'http://www.titan.co.jp/stoneage/')
        self.assertEqual(rows, [])


if __name__ == '__main__': unittest.main()
