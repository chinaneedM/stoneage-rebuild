"""PET51: 2001 TW/CN press dates and operator-hosted player pet claims bound to TW1 original SPR."""

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REC = ROOT / "research" / "recovered"


def get(name):
    return json.loads((REC / name).read_text(encoding="utf-8"))


class Pet51Year2001SourceCrosswalk(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.x = get("STONEAGE-PET51-YEAR2001-OPERATOR-MUSEUM-PET-CLAIM-CROSSWALK-R1.json")
        cls.museum = get("STONEAGE-PET41-TW-EARLY-WGS-MUSEUM-R1.json")
        cls.album = get("STONEAGE-PET39-TW10-RETAIL-CLIENT-ALBUM-R1.json")
        cls.gaps = get("STONEAGE-PET42-TW10-OPERATOR-MUSEUM-BIDIRECTIONAL-GAP-R1.json")
        cls.queue = get("STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json")

    def test_2001_period_news_regions_and_future_25_are_separate(self):
        press, contest = self.x["year2001_period_sources"]
        self.assertEqual(press["period_report_published"], "2001-11-02")
        self.assertEqual(press["url"], "https://gnn.gamer.com.tw/detail.php?sn=2147")
        c = press["claims"]
        self.assertEqual((c[0]["region"], c[0]["claimed_launch_date"]), ("TW", "2001-08-01"))
        self.assertEqual((c[1]["region"], c[1]["claimed_launch_date"]), ("CN", "2001-11-01"))
        self.assertEqual(c[2]["date_kind"], "AS_OF_2001_11_02_UPCOMING_NOT_RELEASE_CONFIRMED")
        self.assertIsNone(c[2]["claimed_launch_date"])
        self.assertTrue(all(not y["same_build_original_pet_list_acquired"] for y in c))
        other = self.x["retrospective_conflicting_taiwan_2_0"]
        self.assertEqual(other["stated_server_update_date"], "2001-07-01")
        self.assertEqual(other["period_reported_official_product_launch_date"], "2001-08-01")
        self.assertIsNone(other["exact_conflict_resolution"])
        self.assertTrue(other["dates_may_describe_different_operations"])
        self.assertTrue(other["do_not_backdate_2001_08_product_or_any_pet_to_2000"])

    def test_player_proposed_pets_are_not_real_game_pet_release(self):
        contest = self.x["year2001_period_sources"][1]
        self.assertEqual(contest["period_report_published"], "2001-09-13")
        self.assertTrue(all(s["access"].endswith("DIRECT_OPEN_403_NO_ORIGINAL_BYTES") for s in self.x["year2001_period_sources"]))
        self.assertTrue(all(s["original_html_sha256"] is None for s in self.x["year2001_period_sources"]))
        v = contest["pet_submission_competition"]
        self.assertEqual(v["proposed_original_user_drawing_size_px"], [200, 200])
        self.assertEqual(v["original_announced_maximum_kb"], 150)
        self.assertIsNone(v["maximum_bmp_bytes"])
        self.assertEqual(v["pet_name_character_limit"], 5)
        self.assertEqual(v["accepted_submissions_or_pet_names_verified"], [])
        self.assertFalse(v["any_submission_selected_verified"])
        self.assertFalse(v["any_new_live_pet_proven"])
        self.assertTrue(v["contest_is_announced_design_intent_not_existing_live_pet"])

    def test_eight_2001_claims_join_to_real_original_tw1_album(self):
        x = self.x
        rows = {r["web_ordinal"]: r for r in self.museum["rows"]}
        pages = {r["filename"]: r for r in self.museum["pages"]}
        orig = {r["graphic_number"]: r for r in self.album["records"]}
        actual = {r["web_ordinal"]: r for r in x["year2001_same_name_player_claim_to_original_tw1_client_cases"]}
        self.assertEqual(set(actual), {3, 35, 36, 74, 103, 107, 114, 115})
        self.assertEqual(len(actual), 8)
        self.assertEqual({r["claim_kind"] for r in self.museum["selected_contributions"]},
                         {r["player_contributed_claim_kind"] for r in actual.values()})
        for no, entry in actual.items():
            r = rows[no]
            p = pages[r["source_page"]]
            c = orig[entry["tw1_client_original_graphic_number"]]
            self.assertEqual(r["tw10_same_printed_name_graphic"], c["graphic_number"])
            self.assertEqual(r["name_as_written"], c["name_as_written"])
            self.assertEqual(entry["website_printed_name"], c["name_as_written"])
            self.assertEqual(entry["source_webpage_sha256_from_pet41"], p["sha256"])
            self.assertEqual(entry["source_page_archived_capture_timestamp"], p["archive_capture"])
            self.assertEqual(entry["tw1_client_original_album_row_sha256_from_pet39"], c["source_row_sha256"])
            self.assertEqual(entry["tw1_client_original_spr_full_segment_sha256_from_pet39"], c["spr_original_segment_sha256"])
            self.assertEqual(entry["tw1_client_original_spr_group_index"], c["spr_group_index"])
            self.assertEqual(entry["player_contributed_elements_not_native_game_stats"], r["contributed_elements"])
            self.assertEqual(entry["cross_carrier_identity_evidence"], "EXACT_PRINTED_NAME_ONLY")
            self.assertFalse(entry["official_gameplay_availability_proven"])
            self.assertFalse(entry["claimed_event_year_proven"])

    def test_existing_count_boundaries_and_no_old_source_promotion(self):
        x = self.x
        k = x["counts"]
        self.assertEqual((len(self.museum["rows"]), len(self.album["records"])), (128, 124))
        self.assertEqual((k["old_museum_exact_client_name_rows"], k["old_museum_distinct_exact_client_graphics"]), (106, 105))
        self.assertEqual(k["old_museum_web_name_non_exact_count"], 22)
        self.assertEqual(len(self.gaps["website_non_exact_client_name_rows"]), 22)
        self.assertEqual(len(self.gaps["client_named_graphics_not_exactly_listed_on_website"]), 19)
        self.assertEqual((k["selected_clauses_with_actual_acquisition_or_location_claim"],
                          k["selected_exact_original_tw1_client_name_and_spr_crosschecks"]), (8, 8))
        self.assertEqual(k["new_official_2001_named_pet_live_release_proofs"], 0)
        self.assertIsNone(k["historical_year2001_official_species_total"])
        self.assertEqual(x["new_original_2001_client_bytes_acquired"], 0)
        self.assertFalse(x["original_repo_sources_replayed"]["early_client_source"]["version2_game_client_authoritatively_identified"])
        self.assertEqual(x["original_repo_sources_replayed"]["early_client_source"]["sa42_path_string_not_verified_existing_asset"], "data\\album_2.dat")

    def test_year_2001_stays_open_and_current_file_is_protected(self):
        x, q = self.x, self.queue
        self.assertEqual((x["active_module"], x["active_year"], x["year_2001_gate"]), ("PET", 2001, "NOT_YEAR_AUDITED"))
        self.assertEqual(q["yearly_work_queue"][1]["research_gate"], "SOURCE_BOUNDED_REVIEWED")
        self.assertIn(q["yearly_work_queue"][2]["research_gate"], {"NOT_YEAR_AUDITED", "SOURCE_BOUNDED_REVIEWED"})
        self.assertGreaterEqual(q["current_frontier"]["year"], 2001)
        # Future PET sessions may advance the successor task after this report is accepted.
        self.assertRegex(q["current_frontier"]["next"], r"^PET\d+:")
        rows = [r for r in q["root_source_census_receipts"] if r["id"] == "PET51-2001-TWCN-2_0-PET-MUSEUM-SOURCE-20261116"]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["new_official_named_live_release_proofs"], 0)
        self.assertEqual(x["baseline"]["current_state_blob_sha"], "c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertEqual(x["stage_A"], "7_PARTIAL_2_OPEN")
        self.assertEqual(x["stage_B_wiki"], "GATED")
        self.assertIsNone(x["overall_completion_percent"])


if __name__ == "__main__":
    unittest.main()
