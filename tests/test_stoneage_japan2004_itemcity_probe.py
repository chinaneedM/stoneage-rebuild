import unittest
from unittest.mock import patch

from tools.stoneage_japan2004_itemcity_probe import (
    TARGET,
    availability,
    derived_facts,
    relevant_ref,
)


class Japan2004ItemCityProbeTests(unittest.TestCase):
    def test_target_is_exact_recovered_product_423(self):
        self.assertIn("product_id=423",TARGET)
        self.assertIn("ten_id=itemcity",TARGET)

    @patch("tools.stoneage_japan2004_itemcity_probe.get_json")
    def test_availability_normalizes_product_capture(self,mock_get):
        mock_get.return_value={
            "archived_snapshots":{
                "closest":{
                    "available":True,
                    "status":"200",
                    "timestamp":"20040605010101",
                    "url":"http://web.archive.org/web/20040605010101/http://www.item-city.com/x",
                }
            }
        }
        self.assertEqual(
            availability("20040604")["timestamp"],
            "20040605010101",
        )

    def test_product_facts_extract_identifiers_price_and_image(self):
        body=(
            '<html><body>ストーンエイジ WR-04156 '
            '4988609011565 3,980円 '
            '<img src="/images/product423.jpg"></body></html>'
        ).encode("utf-8")
        facts=derived_facts(body)
        self.assertEqual(facts["jan"],("4988609011565",))
        self.assertEqual(facts["prices"],("3,980",))
        self.assertIn("WR-04156",facts["model_codes"])
        self.assertEqual(facts["wr04156_occurrences"],1)
        self.assertGreater(facts["stoneage_occurrences"],0)
        self.assertEqual(len(facts["visible_text_sha256"]),64)
        self.assertTrue(any("product423.jpg" in ref for ref in facts["refs"]))

    def test_relevant_ref_filters_generic_navigation(self):
        self.assertTrue(relevant_ref("http://x/images/product423.jpg"))
        self.assertTrue(relevant_ref("http://x/shopping/item.asp"))
        self.assertFalse(relevant_ref("http://x/privacy.html"))


if __name__=="__main__":
    unittest.main()
