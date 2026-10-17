"""Static evidence boundaries for the bounded early 17173 media article bridge."""
import json
import unittest
from pathlib import Path

P = Path(__file__).resolve().parents[1] / "research/recovered/STONEAGE-EARLY-MEDIA-ARTICLE-PET-SOURCE-R1.json"

class EarlyMediaArticleSourceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(P.read_text(encoding="utf-8"))

    def test_sources_have_individual_urls_and_bounded_dates(self):
        s = self.data["sources"]
        self.assertEqual(len(s), 5)
        self.assertEqual(len({x["id"] for x in s}), 5)
        self.assertEqual(len({x["url"] for x in s}), 5)
        for x in s:
            self.assertTrue(x["url"].startswith("https://news.17173.com/z/stoneage/content/2001-"))
            self.assertTrue(x["date_as_displayed"].startswith("2001-"))
        self.assertEqual(sum(x["read_method"] == "SEARCH_EXCERPT_ONLY_PAGE_OPEN_TIMEOUT" for x in s), 1)

    def test_all_twenty_rows_are_only_candidates(self):
        pets = self.data["pet_name_candidates"]
        self.assertEqual(len(pets), 20)
        self.assertEqual([p["source_row_ordinal"] for p in pets], list(range(1, 21)))
        self.assertEqual(len({p["record_id"] for p in pets}), 20)
        self.assertEqual(len({p["source_name"] for p in pets}), 20)
        for p in pets:
            self.assertEqual(p["article_id"], "MEDIA17173_20010614_PET20")
            self.assertIsNone(p["claimed_version"])
            self.assertIsNone(p["tw10_graphic_id"])
            self.assertIsNone(p["spr_no"])
            self.assertIsNone(p["original_species_id"])
            self.assertFalse(p["original_server_location_verified"])
            self.assertEqual(p["qualification"], "PLAYER_REPORT_ONLY_NOT_SAME_BUILD_GAME_DATA")

    def test_no_modern_site_or_player_report_promoted_to_historical_fact(self):
        a = self.data["archive_replay"]
        for key in ("original_2001_page_snapshot_obtained", "media_1999_2002_site_tree_verified",
                    "old_category_temporaneous_layout_verified", "site_original_publication_dates_independently_verified"):
            self.assertFalse(a[key])
        self.assertTrue(a["migrated_category_now_contains_later_content"])
        self.assertEqual(a["old_category_url"], "http://stoneage.17173.com/jingyan/jingyan.shtml")
        self.assertTrue(all(v is False for v in self.data["boundaries"].values()))
        self.assertEqual(len(self.data["cross_domain_claims"]), 4)
        self.assertTrue(all(x["claim_status"] != "FACT_SAME_BUILD_SERVER_RULE" for x in self.data["cross_domain_claims"]))

if __name__ == "__main__": unittest.main()
