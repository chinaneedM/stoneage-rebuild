import unittest

from tools.stoneage_gametime_kolis_holding_probe import (
    FormParser,
    call_first_args,
    edition_key,
    holding_rows,
    search_form,
)


class GameTimeKolisHoldingProbeTests(unittest.TestCase):
    def test_edition_key(self):
        raw = """function fnEdtionList(ufKey, tab){ var x=1; }
<a onclick="javascript:fnEdtionList('24118251'); return false;">x</a>"""
        self.assertEqual(edition_key(raw), "24118251")

    def test_call_first_args_ignores_function_definition(self):
        raw = """function fnLibList(bibKey, obj){ return false; }
<a onclick="javascript:fnLibList('10041033', this); return false;">2개관</a>"""
        self.assertEqual(call_first_args(raw,"fnLibList"),["bibKey","10041033"])

    def test_holding_rows_extract_library_key(self):
        raw = """<a href="#lib" onclick="javascript:fnLibDetail('556677', this); return false;">국립중앙도서관</a>"""
        rows=holding_rows(raw,"https://www.nl.go.kr/x")
        self.assertEqual(rows[0][0],"국립중앙도서관")
        self.assertEqual(rows[0][3],"556677")

    def test_search_form_parser(self):
        raw='''<form name="searchParamForm" action="/old">
        <input type="hidden" name="keyword1" value="8995182121">
        <input type="hidden" name="ufKey" value="">
        </form>'''
        attrs,fields=search_form(raw)
        self.assertEqual(attrs["action"],"/old")
        self.assertEqual(fields["keyword1"],"8995182121")
        self.assertEqual(fields["ufKey"],"")

    def test_form_parser_keeps_multiple_forms(self):
        p=FormParser()
        p.feed('<form name="x"><input name="a" value="1"></form><form name="searchParamForm"><input name="ufKey" value=""></form>')
        self.assertEqual(len(p.forms),2)


if __name__=="__main__":
    unittest.main()
