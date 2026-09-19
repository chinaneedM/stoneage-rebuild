import unittest

from tools.stoneage_gametime_library_probe import (
    AnchorParser,
    contexts,
    interesting_anchor,
    strip_markup,
    structural_tokens,
)


class GameTimeLibraryProbeTests(unittest.TestCase):
    def test_anchor_parser_keeps_navigation_attributes(self):
        p=AnchorParser()
        p.feed('<a href="/detail.do?id=U10029631" onclick="goDetail(\'U10029631\')">스톤 에이지</a>')
        attrs,label=p.anchors[0]
        self.assertEqual(attrs["href"],"/detail.do?id=U10029631")
        self.assertIn("goDetail",attrs["onclick"])
        self.assertEqual(label,"스톤 에이지")
        self.assertTrue(interesting_anchor(attrs,label))

    def test_strip_markup_preserves_catalog_text(self):
        text=strip_markup("<html><body>318p. + 컴팩트디스크 1매(12cm).</body></html>")
        self.assertIn("컴팩트디스크",text)

    def test_contexts_find_holdings_text(self):
        rows=contexts("스톤 에이지 / 게임타임. 2 개 도서관 소장.",("2 개 도서관 소장",))
        self.assertEqual(len(rows),1)
        self.assertIn("2 개 도서관 소장",rows[0][1])

    def test_structural_tokens_find_riss_and_control_hash(self):
        rows=structural_tokens("id=U10029631 control_no=9b505f870e768aa6ffe0bdc3ef48d419")
        joined=" ".join(rows)
        self.assertIn("U10029631",joined)
        self.assertIn("9b505f870e768aa6ffe0bdc3ef48d419",joined)


if __name__=="__main__":
    unittest.main()
