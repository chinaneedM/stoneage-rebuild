"""PET81 2009 Korean operator press event pet candidates, without first-release or native count promotion."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"research"/"recovered"
def load(name):
    return json.loads((DATA/name).read_text(encoding="utf-8"))

class PET81Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e=load("STONEAGE-PET81-KR2009-COW-SNOWLEOPARD-SOURCE-AUDIT-R1.json")
        cls.q=load("STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json")

    def test_korean_names_and_snow_leopard_eligibility(self):
        e=self.e
        named=e["korean_named_event_pet_candidates"]
        self.assertEqual([p["original_korean_name"] for p in named],["젖소","흑우","화우","하누","설표"])
        self.assertEqual(named[-1]["required_level_for_eligibility"],30)
        self.assertFalse(named[-1]["automatic_permanent_grant_verified"])
        self.assertTrue(e["source_boundaries"]["cows_list_in_original_text_has_et_cetera"])
        self.assertFalse(e["source_boundaries"]["all_event_pet_species_list_complete"])
        self.assertTrue(e["source_boundaries"]["april_29_is_attestation_not_first_release_date"])
        self.assertEqual(e["provenance"]["distinct_original_operator_announcements_proven"],1)
        self.assertTrue(all(p["native_pet_id"] is None and p["native_spr_id"] is None and not p["actual_player_grant_verified"] for p in named))
        self.assertTrue(all(p["first_official_species_release_date"] is None for p in named))

    def test_jp_dec_not_actual_and_2010_separate(self):
        d=self.e["japan_existing_2009_dec_plan"]
        self.assertEqual(d["planned_dates"],["2009-12-01","2009-12-22","2009-12-29"])
        self.assertEqual(d["planned_next_year_dates"],["2010-01-12","2010-01-19"])
        self.assertFalse(d["actual_updated_original_native_version_confirmed"])
        self.assertTrue(d["prior_PET80_source_not_new_independent_evidence"])

    def test_forward_only_cursor_and_no_population_inflation(self):
        e,q=self.e,self.q
        y=q["yearly_work_queue"][2009-1999]
        self.assertEqual((e["year"],e["year_frontier_before"],e["year_frontier_after"],q["current_frontier"]["year"]),(2009,2009,2009,2009))
        self.assertEqual(y["research_gate"],"NOT_YEAR_AUDITED")
        self.assertFalse(e["historically_complete"])
        self.assertEqual(q["current_frontier"]["latest_partial_root_review"],e["id"])
        self.assertEqual(sum(r["id"]==e["id"] for r in y["partial_source_review_receipts"]),1)
        self.assertEqual(sum(r["id"]==e["id"] for r in q["root_source_census_receipts"]),1)
        self.assertEqual(y["documented_release_event_ids_from_existing_PET25_PET26"],["JP-2009-HAKUEN","JP-2009-KOKUEN"])
        self.assertEqual(len({r["id"] for r in q["root_source_census_receipts"]}),len(q["root_source_census_receipts"]))
        self.assertEqual(set(e["region_reviews"]),{"CN","TW","JP","KR","OTHER"})
        self.assertTrue(all(v["official_species_population"] is None for v in e["region_reviews"].values()))
        self.assertIsNone(e["global_official_species_population_2009"])
        self.assertEqual((e["new_raw_authenticated_2009_original_client_bytes"],e["new_native_2009_pet_ids"],e["new_actual_2009_original_server_grants"]),(0,0,0))
        self.assertTrue(e["no_paid_marketplace"] and e["no_private_server_only_pets"] and e["no_proprietary_assets_published"])

    def test_current_historical_blob_unchanged(self):
        e=self.e
        raw=(ROOT/"docs"/"CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(raw),2709173)
        self.assertEqual(hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\x00"+raw).hexdigest(),e["historical_CURRENT_blob"])
        self.assertEqual((e["stage_A"],e["stage_B_wiki"],e["r79"]),("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING"))

if __name__=="__main__":
    unittest.main()
