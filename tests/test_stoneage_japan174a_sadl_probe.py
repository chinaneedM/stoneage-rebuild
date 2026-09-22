import unittest
from unittest.mock import patch

from tools.stoneage_japan174a_sadl_probe import TARGET, availability


class Japan174aSadlProbeTests(unittest.TestCase):
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
