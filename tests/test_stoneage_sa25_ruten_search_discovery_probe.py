import unittest
from tools.stoneage_sa25_ruten_search_discovery_probe import discovery_urls, ids_from_html, relevant_contexts

class T(unittest.TestCase):
    def test_extract_ids(self):
        s='''<a href="https://www.ruten.com.tw/item/22445165101247/">x</a>
        <a href="/item/22242541948520/">y</a>'''
        self.assertEqual(ids_from_html(s),("22445165101247","22242541948520"))

    def test_relevant_context(self):
        s='''<div>石器時代 2.5版 精靈王傳說
        <a href="/item/22445165101247/">全新完整版</a></div>'''
        rows=relevant_contexts(s,ids_from_html(s))
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0][0],"22445165101247")

    def test_discovery_urls(self):
        s='''<script src="/_nuxt/app.js"></script>
        <script>const x="https://rtapi.ruten.com.tw/api/search/v3/index.php/core/prod?q=x"</script>'''
        urls=discovery_urls(s,"https://www.ruten.com.tw/search/x/")
        self.assertIn("https://rtapi.ruten.com.tw/api/search/v3/index.php/core/prod?q=x",urls)
        self.assertIn("https://www.ruten.com.tw/_nuxt/app.js",urls)

if __name__=="__main__":
    unittest.main()
