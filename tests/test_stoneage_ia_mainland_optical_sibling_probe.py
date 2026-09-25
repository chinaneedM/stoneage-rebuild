import unittest
from unittest.mock import patch

from tools.stoneage_ia_mainland_optical_sibling_probe import (
    BASE_QUERIES, optical_rows, relevant_doc, search_all
)


class MainlandIAOpticalSiblingProbeTests(unittest.TestCase):
    def test_optical_filter_keeps_disc_formats(self):
        rows=optical_rows([
            {"name":"StoneAge.bin","size":"100","md5":"a"},
            {"name":"StoneAge.cue","size":"200","sha1":"b"},
            {"name":"cover.jpg","size":"300"},
        ])
        self.assertEqual([r["name"] for r in rows],["StoneAge.bin","StoneAge.cue"])

    def test_relevant_doc_requires_stoneage_identity(self):
        self.assertTrue(relevant_doc({"title":"石器时代Online 宠物进化史"}))
        self.assertTrue(relevant_doc({"identifier":"Stoneage-5"}))
        self.assertFalse(relevant_doc({"creator":"北京华义联合软件开发有限公司","title":"Unrelated software"}))

    def test_search_all_paginates_to_total(self):
        batches={
            1:("u1",3,[{"identifier":"a"},{"identifier":"b"}]),
            2:("u2",3,[{"identifier":"c"}]),
        }
        with patch("tools.stoneage_ia_mainland_optical_sibling_probe.search",
                   side_effect=lambda q,rows=200,page=1:batches[page]):
            urls,total,rows,complete=search_all("uploader:x",rows=2,max_pages=5)
        self.assertEqual(total,3)
        self.assertEqual([r["identifier"] for r in rows],["a","b","c"])
        self.assertTrue(complete)
        self.assertEqual(urls,["u1","u2"])

    def test_creator_query_is_pinned(self):
        self.assertIn('creator:"北京华义联合软件开发有限公司"',BASE_QUERIES)


if __name__=="__main__":
    unittest.main()
