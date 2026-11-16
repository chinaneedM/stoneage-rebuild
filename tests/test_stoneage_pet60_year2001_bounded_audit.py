"""PET60: a source-bounded five-region 2001 audit may move the cursor to 2002 without inventing pet population."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REC = ROOT / "research" / "recovered"

def load(name):
    return json.loads((REC / name).read_text(encoding="utf-8"))

class TestPET60Year2001Bounded(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = load("STONEAGE-PET60-YEAR2001-SOURCE-BOUNDED-AUDIT-R1.json")
        cls.q = load("STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json")
        cls.tw = load("STONEAGE-PET39-TW10-RETAIL-CLIENT-ALBUM-R1.json")
        cls.prev = load("STONEAGE-PET59-2001-JSS-PLAYER-GIFT-TW10-CLIENT-NAME-BOUNDARY-R1.json")

    def test_previous_2001_root_receipts_all_retained_once(self):
        a, q = self.a, self.q
        ids = [x["id"] for x in q["root_source_census_receipts"]]
        self.assertEqual(len(a["previous_root_receipt_ids"]), 9)
        self.assertEqual(len(set(a["previous_root_receipt_ids"])), 9)
        for id_ in a["previous_root_receipt_ids"]:
            self.assertEqual(ids.count(id_), 1, id_)
        self.assertEqual(ids.count(a["id"]), 1)
        self.assertEqual(q["current_frontier"]["latest_partial_root_review"], a["id"])
        self.assertEqual(len(q["yearly_work_queue"][2]["partial_source_review_receipts"]), 10)

    def test_2001_review_is_not_historical_completion(self):
        a,q=self.a,self.q
        y=q["yearly_work_queue"][2]
        self.assertEqual((a["year"],a["review_status"]),(2001,"SOURCE_BOUNDED_REVIEWED"))
        self.assertEqual(y["research_gate"],"SOURCE_BOUNDED_REVIEWED")
        self.assertEqual(y["source_bounded_review_receipt"],"research/recovered/STONEAGE-PET60-YEAR2001-SOURCE-BOUNDED-AUDIT-R1.json")
        self.assertFalse(a["historically_complete"])
        self.assertFalse(y["historically_complete"])
        self.assertIsNone(y["historical_species_count"])
        self.assertIsNone(a["global_historical_2001_pet_population"])
        self.assertFalse(a["global_historical_official_pets_2001_never_existed"])
        self.assertTrue(a["year2001_PET25_PET26_rows_are_not_full_universe"])
        self.assertEqual(a["year2001_PET25_PET26_documentary_operator_release_event_rows"],0)
        self.assertEqual(a["new_named_official_live_2001_pet_release_proofs_this_review"],0)

    def test_five_independent_regions_missing_deployment_rosters(self):
        a,q=self.a,self.q
        tracks=a["region_source_reviews"]
        self.assertEqual(set(tracks),{"CN","TW","JP","KR","OTHER"})
        self.assertEqual(set(q["yearly_work_queue"][2]["region_source_reviews"]),set(tracks))
        self.assertEqual(len(a["residual_reopen_triggers"]),5)
        self.assertEqual(a["residual_reopen_triggers"],q["yearly_work_queue"][2]["residual_reopen_triggers"])
        for region,track in tracks.items():
            self.assertIsNone(track["pet_population"],region)
            self.assertTrue(track["reopen"],region)
            self.assertTrue(track["reopen_trigger"],region)
            self.assertFalse(track["live_named_pet_roster_verified"],region)
            self.assertTrue(q["yearly_work_queue"][2]["region_source_reviews"][region]["authentic_2001_full_original_client_missing"])
        self.assertFalse(tracks["OTHER"]["all_other_regions_or_products_proven_absent"])

    def test_early_tw_client_and_player_claims_never_become_2001_issuance(self):
        a=self.a
        self.assertEqual(len(self.tw["records"]),124)
        self.assertEqual(a["region_source_reviews"]["TW"]["authenticated_local_client_resource_basis"],
            "TW1_0_RETAIL_124_NAMED_LOCAL_ALBUM_SPR_CANDIDATES_DATED_BUILD_ERA_NOT_LIVE_ROSTER")
        self.assertEqual(a["region_source_reviews"]["TW"]["year2001_operator_hosted_player_museum_positions"],128)
        self.assertFalse(a["region_source_reviews"]["TW"]["year2001_player_museum_is_operator_approved_live_roster"])
        self.assertEqual(a["region_source_reviews"]["JP"]["player_2001_JSS_gift_claims"],9)
        self.assertEqual(a["region_source_reviews"]["JP"]["other_region_TW1_local_names_textual_matches"],8)
        self.assertEqual(self.prev["bounds"]["verified_actual_JP_JSS_2001_prize_gift_names"],0)
        self.assertFalse(a["sources_reused_not_new_2001_client_bytes"][1]["complete_original_2_0_installer_attested"])
        self.assertFalse(a["sources_reused_not_new_2001_client_bytes"][1]["pe_timestamp_is_first_release"])

    def test_search_stop_and_2002_new_frontier(self):
        a,q=self.a,self.q
        self.assertEqual((a["year_frontier_before"],a["year_frontier_after"]),(2001,2002))
        self.assertEqual(q["current_frontier"]["year"],2002)
        self.assertEqual(q["current_frontier"]["status"],"OPEN_NOT_YEAR_CLOSED")
        self.assertEqual(q["yearly_work_queue"][3]["research_gate"],"NOT_YEAR_AUDITED")
        self.assertEqual(q["yearly_work_queue"][3]["documented_release_event_count_NOT_species"] if "documented_release_event_count_NOT_species" in q["yearly_work_queue"][3] else q["yearly_work_queue"][3]["documentary_event_count_NOT_species"],4)
        self.assertEqual(q["yearly_work_queue"][3]["documented_release_event_ids_from_existing_PET25_PET26"],a["next_2002_candidate_existing_release_event_ids"])
        self.assertTrue(q["current_frontier"]["next"].startswith("PET61:"))
        self.assertFalse(a["next_2002_facts_are_species_total"])
        self.assertEqual(a["new_original_2001_client_bytes_this_review"],0)
        self.assertEqual(a["free_direct_public_client_source_search"]["new_complete_original_installers_downloaded"],0)
        self.assertFalse(a["free_direct_public_client_source_search"]["claim_all_public_copies_exhausted"])
        self.assertTrue(a["no_paid_secondhand_carrier_research"])

    def test_historical_original_state_and_stage_stay_unmodified(self):
        a=self.a
        self.assertEqual(a["historical_CURRENT_blob_unchanged"],"c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertEqual(a["baseline_remote"]["historical_current_size_bytes"],2709173)
        self.assertEqual((a["stage_A"],a["stage_B_wiki"],a["r79"]),("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING"))
        self.assertIsNone(a["overall_percent"])
        self.assertFalse(a["copyright_original_assets_committed"])

if __name__=="__main__":
    unittest.main()
