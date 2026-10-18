import unittest
from tools.stoneage_wayi_intro_detail02_probe import ORIGINAL, check_final_url, inspect

class ProbeTests(unittest.TestCase):
    def test_exact_provenance(self):
        url = "https://web.archive.org/web/20050614002509id_/" + ORIGINAL
        self.assertEqual(check_final_url(url), "20050614002509")
        body = "<html><head><title>石器時代</title></head><body><p>這是寵物相關的文字資料。</p></body></html>".encode("big5") + b" " * 450
        r = inspect(body, url)
        self.assertEqual(r["actual_capture"], "20050614002509")
        self.assertIsNone(r["exact_client_build"])
        self.assertFalse(r["npc_pet_quest_runtime_confirmed"])
    def test_wrong_source(self):
        for u in ("https://www.wayi.com.tw/home",
                  "https://web.archive.org/web/20050614002509id_/http://www.wayi.com.tw/stoneage/game/game01_03.asp",
                  "https://web.archive.org/web/20050614002509id_/http://example.com/game01_02.asp"):
            with self.assertRaises(ValueError):
                check_final_url(u)
    def test_reject_nonhtml(self):
        u = "https://web.archive.org/web/20050614002509id_/" + ORIGINAL
        with self.assertRaises(ValueError):
            inspect(b"x" * 500, u)
        with self.assertRaises(UnicodeDecodeError):
            inspect(b"<html><body>" + bytes([129,0]) * 400, u)
if __name__ == "__main__":
    unittest.main()
