import unittest
from unittest.mock import patch

from tools.stoneage_japan2004_package_probe import (
    TARGET,
    availability,
    derived_page_facts,
    is_relevant_ref,
)


class Japan2004PackageProbeTests(unittest.TestCase):
    def test_target_is_contemporaneous_official_package_page(self):
        self.assertEqual(TARGET,"http://stoneage.to/package.html")

    @patch("tools.stoneage_japan2004_package_probe.get_json")
    def test_availability_normalizes_closest(self,mock_get):
        mock_get.return_value={
            "archived_snapshots":{
                "closest":{
                    "available":True,
                    "status":"200",
                    "timestamp":"20040520120000",
                    "url":"http://web.archive.org/web/20040520120000/http://stoneage.to/package.html",
                }
            }
        }
        self.assertEqual(
            availability("20040520"),
            {
                "timestamp":"20040520120000",
                "status":"200",
                "url":"http://web.archive.org/web/20040520120000/http://stoneage.to/package.html",
            },
        )

    def test_derived_facts_extract_codes_price_and_refs_without_prose(self):
        body=(
            '<html><body>CD-ROM CD-ROM ウポポ 30日 3,980円 '
            'JAN 1234567890123 MODEL SA-JP2004 '
            '<a href="shop.html">shop</a>'
            '<img src="images/package.jpg"></body></html>'
        ).encode("utf-8")
        facts=derived_page_facts(body)
        self.assertEqual(facts["jan"],("1234567890123",))
        self.assertEqual(facts["prices"],("3,980",))
        self.assertIn("SA-JP2004",facts["model_codes"])
        self.assertEqual(facts["cdrom_occurrences"],2)
        self.assertEqual(facts["upopo_occurrences"],1)
        self.assertEqual(facts["day30_occurrences"],1)
        self.assertTrue(any("package.jpg" in ref for ref in facts["refs"]))
        self.assertEqual(len(facts["visible_text_sha256"]),64)

    def test_relevant_ref_keeps_package_and_store_surfaces(self):
        self.assertTrue(is_relevant_ref("http://stoneage.to/images/package.jpg"))
        self.assertTrue(is_relevant_ref("http://example.test/store/stoneage"))
        self.assertFalse(is_relevant_ref("http://example.test/privacy.html"))


if __name__=="__main__":
    unittest.main()
