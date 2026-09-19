import unittest

from tools.stoneage_gametime_library_probe import (
    LinkParser,
    relevant_link,
    snippets,
    strip_markup,
)


class GameTimeLibraryProbeTests(unittest.TestCase):
    def test_link_parser_extracts_riss_id(self):
        p=LinkParser()
        p.feed('<a href="https://www.riss.kr/link?id=U10029631">스톤 에이지 = Stone age / 게임타임</a>')
        self.assertEqual(p.links[0][0],"https://www.riss.kr/link?id=U10029631")
        self.assertTrue(relevant_link(*p.links[0]))

    def test_strip_markup_preserves_catalog_text(self):
        text=strip_markup("<html><body>318 pages + 1 compact disc (12 cm)</body></html>")
        self.assertIn("compact disc",text)

    def test_snippets_find_supplement_fields(self):
        rows=snippets("국립중앙도서관 소장. 딸림자료: CD-ROM 1매. 청구기호 123")
        joined=" ".join(x[1] for x in rows)
        self.assertIn("딸림자료",joined)
        self.assertIn("청구기호",joined)

    def test_irrelevant_link_rejected(self):
        self.assertFalse(relevant_link("https://example.com/","unrelated"))


if __name__=="__main__":
    unittest.main()
