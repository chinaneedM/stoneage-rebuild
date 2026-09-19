import unittest

from tools.stoneage_hananet_pkboard_mechanism_probe import Parser, relevant_snippets


class HananetPkboardMechanismProbeTests(unittest.TestCase):
    def test_parser_assets_and_form(self):
        p = Parser()
        p.feed('<script src="/js/board.js"></script><form action="/cgi-bin/pkboard.cgi"><a onclick="download(8119)">x</a></form>')
        self.assertIn(("external", "/js/board.js"), p.scripts)
        self.assertTrue(any(x[1] == "action" for x in p.attrs))
        self.assertTrue(any(x[1] == "onclick" for x in p.attrs))

    def test_relevant_snippets(self):
        text = "hello\nfunction download(x){location='/cgi-bin/getfile.cgi?id='+x;}\nbye"
        rows = relevant_snippets(text)
        rendered = "\n".join(rows)
        self.assertIn("download", rendered)
        self.assertIn("getfile.cgi", rendered)
        self.assertNotIn("bye", rows)


if __name__ == "__main__":
    unittest.main()
