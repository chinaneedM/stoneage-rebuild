import unittest
from tools.stoneage_sa25_ruten_physical_probe import IDS,image_urls,detail_rows

class RutenPhysicalProbeTests(unittest.TestCase):
    def test_target_ids(self):
        self.assertIn("22632305238624",IDS)
        self.assertIn("21926883918096",IDS)
        self.assertIn("22242541948520",IDS)

    def test_extract_detail_images(self):
        row={"images":{"url":["https://a.rimg.com.tw/a.jpg","//a.rimg.com.tw/b.jpg"],"m_url":["https://a.rimg.com.tw/a.jpg"]}}
        self.assertEqual(image_urls(row),[
            "https://a.rimg.com.tw/a.jpg",
            "https://a.rimg.com.tw/b.jpg",
        ])

    def test_detail_rows(self):
        self.assertEqual(detail_rows({"data":[{"id":"x"}]}),[{"id":"x"}])
        self.assertEqual(detail_rows([{"id":"y"}]),[{"id":"y"}])

if __name__=="__main__":
    unittest.main()
