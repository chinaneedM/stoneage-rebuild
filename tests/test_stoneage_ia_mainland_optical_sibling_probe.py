import unittest

from tools.stoneage_ia_mainland_optical_sibling_probe import (
    BASE_QUERIES, optical_rows, relevant_doc
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

    def test_creator_query_is_pinned(self):
        self.assertIn('creator:"北京华义联合软件开发有限公司"',BASE_QUERIES)


if __name__=="__main__":
    unittest.main()
