import unittest
from unittest.mock import patch

from tools.stoneage_japan174a_sadl_probe import (
    TARGET,
    availability,
    derived_page_facts,
)


class Japan174aSadlProbeTests(unittest.TestCase):
    def test_derived_page_facts_extract_only_structured_tokens(self):
        facts=derived_page_facts(
            (
                '<html><body>STONE AGE Version 1.74a '
                'client 257 MB '
                '<a href="http://hangame.gamania.co.jp/stoneage/sa174hg.exe">'
                'download</a> stoneage.exe</body></html>'
            ).encode("utf-8")
        )
        self.assertEqual(facts["versions"],("1.74a",))
        self.assertEqual(facts["sizes"],("257MB",))
        self.assertEqual(facts["sa174hg_occurrences"],1)
        self.assertEqual(facts["stoneage_exe_occurrences"],1)
        self.assertGreater(facts["visible_text_chars"],0)
        self.assertEqual(len(facts["visible_text_sha256"]),64)

    def test_target_is_exact_official_download_page(self):
        self.assertEqual(
            TARGET,
            "http://www.hangame.co.jp:80/publish/sa/sadl.asp",
        )

    @patch("tools.stoneage_japan174a_sadl_probe.get_json")
    def test_availability_normalizes_closest(self,mock_get):
        mock_get.return_value={
            "archived_snapshots":{
                "closest":{
                    "available":True,
                    "status":"200",
                    "timestamp":"20031215010101",
                    "url":"http://web.archive.org/web/20031215010101/http://x/",
                }
            }
        }
        self.assertEqual(
            availability("20031215"),
            {
                "timestamp":"20031215010101",
                "status":"200",
                "url":"http://web.archive.org/web/20031215010101/http://x/",
            },
        )


if __name__=="__main__":
    unittest.main()
