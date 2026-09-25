import unittest
from tools.stoneage_sa25_collector_mirror_context_probe import between_rows, rows

class CollectorMirrorContextTests(unittest.TestCase):
    def test_rows_bind_nearby_text_and_url(self):
        s="<p>大陸版光碟</p><img data-src='/disc.jpg' alt='光碟'><p>臺版盤</p>"
        rr=rows(s,"https://example.com/a")
        self.assertEqual(len(rr),1)
        self.assertEqual(rr[0]["url"],"https://example.com/disc.jpg")
        self.assertIn("大陸版光碟",rr[0]["pre"])
        self.assertIn("臺版盤",rr[0]["post"])
        self.assertEqual(rr[0]["alt"],"光碟")

    def test_between_rows_is_exact_interval(self):
        s=(
            "<p>before</p>"
            "<img data-src='/mainland.jpg'>"
            "<p>上面是大陆版客户端统一图案的光盘</p>"
            "<img data-src='/taiwan.jpg'>"
            "<p>下面是台版盘，有点镭射反光</p>"
            "<img data-src='/next.jpg'>"
            "<p>after</p>"
        )
        rr=rows(s,"https://example.com/a")
        bb=between_rows(s,rr)
        self.assertEqual(len(bb),2)
        self.assertEqual(bb[0]["text"],"上面是大陆版客户端统一图案的光盘")
        self.assertEqual(bb[1]["text"],"下面是台版盘，有点镭射反光")
        self.assertNotIn("before",bb[0]["text"])
        self.assertNotIn("after",bb[1]["text"])

if __name__=="__main__":
    unittest.main()
