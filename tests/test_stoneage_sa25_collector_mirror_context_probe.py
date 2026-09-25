import unittest
from tools.stoneage_sa25_collector_mirror_context_probe import rows

class CollectorMirrorContextTests(unittest.TestCase):
    def test_rows_bind_nearby_text_and_url(self):
        s="<p>大陸版光碟</p><img data-src='/disc.jpg' alt='光碟'><p>臺版盤</p>"
        rr=rows(s,"https://example.com/a")
        self.assertEqual(len(rr),1)
        self.assertEqual(rr[0]["url"],"https://example.com/disc.jpg")
        self.assertIn("大陸版光碟",rr[0]["pre"])
        self.assertIn("臺版盤",rr[0]["post"])
        self.assertEqual(rr[0]["alt"],"光碟")

if __name__=="__main__":
    unittest.main()
