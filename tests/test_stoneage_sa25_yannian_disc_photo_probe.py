import unittest
from tools.stoneage_sa25_yannian_disc_photo_probe import target_rows, target_urls

class T(unittest.TestCase):
    def test_target_rows_compatibility(self):
        rows=(("u1","普通照片","普通照片"),("u2","2.5時期的光碟","2.5時期的光碟"),)
        t=target_rows(rows)
        self.assertEqual(len(t),1)
        self.assertEqual(t[0][1],"u2")

    def test_target_urls_only_between_disc_and_manual_labels(self):
        s=(
            "<img data-src='https://x.example/old.jpg'>"
            "2.5時期的光碟"
            "<p><img data-src='https://img.example/real25.jpg'></p>"
            "2.5版本的說明書"
            "<img data-src='https://x.example/related.jpg'>"
        )
        urls,seg,start,end=target_urls(s,"https://home.gamer.com.tw/a")
        self.assertEqual(urls,("https://img.example/real25.jpg",))
        self.assertGreaterEqual(start,0)
        self.assertGreater(end,start)
        self.assertIn("2.5時期的光碟",seg)
        self.assertNotIn("related.jpg",seg)

    def test_no_extension_thumbnail_false_positive(self):
        s=(
            "2.5時期的光碟"
            "<span>no image tag here</span>"
            "2.5版本的說明書"
            "<h2>延伸閱讀</h2>"
            "<img data-src='https://cos.stoneage.cn/related.jpg'>"
        )
        urls,_,_,_=target_urls(s,"https://home.gamer.com.tw/a")
        self.assertEqual(urls,())

if __name__=="__main__":
    unittest.main()
