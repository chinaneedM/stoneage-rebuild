import unittest

from tools.stoneage_discmaster_search_schema_probe import parse_forms


class DiscMasterSearchSchemaProbeTests(unittest.TestCase):
    def test_form_fields_and_selects_are_recovered(self):
        html=b"""
        <html><body>
        <form method="GET" action="/search">
          <input type="text" name="q" value="">
          <input type="checkbox" name="filename" value="1" checked>
          <select name="family">
            <option value="">Either</option>
            <option value="executable" selected>Executable</option>
          </select>
        </form>
        </body></html>
        """
        forms=parse_forms(html)
        self.assertEqual(len(forms),1)
        self.assertEqual(forms[0]["method"],"get")
        self.assertEqual(forms[0]["action"],"/search")
        self.assertEqual(forms[0]["inputs"][0]["name"],"q")
        self.assertTrue(forms[0]["inputs"][1]["checked"])
        self.assertEqual(forms[0]["selects"][0]["name"],"family")
        self.assertTrue(forms[0]["selects"][0]["options"][1]["selected"])

    def test_default_method_is_get(self):
        forms=parse_forms(b'<form action="/search"><input name="search"></form>')
        self.assertEqual(forms[0]["method"],"get")


if __name__=="__main__":
    unittest.main()
