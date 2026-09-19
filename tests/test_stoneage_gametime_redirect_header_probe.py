import unittest

from tools.stoneage_gametime_redirect_header_probe import NoRedirect, replay_urls


class GameTimeRedirectHeaderProbeTests(unittest.TestCase):
    def test_no_redirect_handler_refuses_follow(self):
        h=NoRedirect()
        self.assertIsNone(h.redirect_request(None,None,302,"Found",{},"http://example.com/file.exe"))

    def test_replay_urls_include_raw_and_normal(self):
        rows=replay_urls("20010614215330","http://www.gametime.co.kr/data/download.asp?GW_IDX=9&GW_Name=Online")
        self.assertEqual(len(rows),2)
        self.assertIn("20010614215330id_",rows[0])
        self.assertIn("GW_IDX=9",rows[0])


if __name__=="__main__":
    unittest.main()
