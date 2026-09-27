import unittest
from tools.stoneage_mainland_sa10_test_carrier_bahamut_images import (
    PAGE, ANCHORS, RUMOR_ANCHOR, CLAIM_ANCHOR,
    article_images, first_post_bounds, image_dimensions,
)

class T(unittest.TestCase):
    def test_target(self):
        self.assertIn("snA=81396", PAGE)
        self.assertTrue(any("測試說明書" in a for a in ANCHORS))

    def test_first_post_bounds_exclude_recommendations(self):
        raw=(
            "prefix 首先慣例一張全家福 "
            '<img src="https://truth.bahamut.com.tw/s01/202009/main.JPG">'
            f" {RUMOR_ANCHOR} "
            '<img src="https://truth.bahamut.com.tw/s01/202009/rumor.JPG">'
            f" {CLAIM_ANCHOR} 有空再和大傢俱體聊了哈 "
            "延伸閱讀 "
            '<img src="https://cos.stoneage.cn/uploads/article/minisnsimg/20201222/recommend.jpg">'
        )
        start,end=first_post_bounds(raw)
        self.assertLess(start,end)
        rows=article_images(raw,start,end)
        self.assertEqual([u.rsplit("/",1)[-1] for _,u in rows],["main.JPG","rumor.JPG"])
        claim=raw.find(CLAIM_ANCHOR,start,end)
        self.assertEqual(len([(p,u) for p,u in rows if p>claim]),0)

    def test_excludes_thumbnail_query_and_ui_hosts(self):
        raw=(
            "首先慣例一張全家福 "
            '<img src="https://truth.bahamut.com.tw/s01/202009/a.JPG?w=300&h=300">'
            '<img src="https://i2.bahamut.com.tw/editor/emotion/1.gif">'
            " 延伸閱讀"
        )
        start,end=first_post_bounds(raw)
        self.assertEqual(article_images(raw,start,end),())

    def test_png_dimensions(self):
        body=b"\x89PNG\r\n\x1a\n"+b"\x00"*8+(12).to_bytes(4,"big")+(34).to_bytes(4,"big")
        w,h,fmt=image_dimensions(body)
        self.assertEqual((w,h,fmt),(12,34,"png"))

if __name__=="__main__":
    unittest.main()
