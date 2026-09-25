import unittest

from tools.stoneage_sa25_ruten_provenance_metadata_probe import (
    flatten,
    key_allowed,
    keyword_snippets,
)


class T(unittest.TestCase):
    def test_flatten(self):
        rows=list(flatten({"data":[{"name":"石器時代2.5","num":1}]}))
        self.assertIn(("data[].name","石器時代2.5"),rows)
        self.assertIn(("data[].num",1),rows)

    def test_excludes_seller_contact_paths(self):
        self.assertFalse(key_allowed("data[].seller.email","x@example.com"))
        self.assertFalse(key_allowed("data[].address","Taipei"))
        self.assertTrue(key_allowed("data[].description","石器時代2.5原版光碟"))

    def test_keyword_snippets(self):
        text="前文 "*30+"這是石器時代2.5精靈王傳說原包裝遊戲光碟，保存良好。"+" 後文"*30
        rows=keyword_snippets(text,80)
        self.assertTrue(rows)
        self.assertIn("原包裝",rows[0])


if __name__=="__main__":
    unittest.main()
