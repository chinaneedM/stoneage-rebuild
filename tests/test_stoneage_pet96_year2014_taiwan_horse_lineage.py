"""PET96 year-2014 source discipline: old horse-year attestation != 2014 pet debut."""
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"research/recovered"
P96=BASE/"STONEAGE-PET96-YEAR2014-TW-HORSE-ACQUISITION-AND-EARLIER-ATTESTATION-R1.json"
Q=BASE/"STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"
class Pet96Year2014TaiwanHorse(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=json.loads(P96.read_text(encoding="utf-8"))
        cls.q=json.loads(Q.read_text(encoding="utf-8"))
    def test_2014_still_open_and_receipts_forward_only(self):
        a,q=self.a,self.q
        self.assertEqual((a["year"],a["year_frontier_before"],a["year_frontier_after"]),(2014,2014,2014))
        self.assertEqual(a["review_status"],"PARTIAL_NOT_YEAR_AUDITED")
        self.assertFalse(a["year_source_bounded_closed"])
        self.assertFalse(a["historically_complete"])
        self.assertEqual(q["current_frontier"]["year"],2014)
        self.assertTrue(q["current_frontier"]["next"].startswith("PET97:"))
        self.assertEqual(q["yearly_work_queue"][15]["research_gate"],"NOT_YEAR_AUDITED")
        self.assertEqual(q["root_source_census_receipts"][-1]["id"],a["id"])
        self.assertEqual([x["id"] for x in q["yearly_work_queue"][15]["partial_source_review_receipts"]],[
            "PET95-YEAR2014-CN-TW-ORIGINAL-PC-SOURCE-FIRST-PASS-20261118",a["id"]
        ])
        self.assertEqual(len({x["id"] for x in q["root_source_census_receipts"]}),len(q["root_source_census_receipts"]))
    def test_2011_four_waei_names_and_2013_tz_personal_attestation_not_2014_debut(self):
        a=self.a
        self.assertEqual(len(a["sources"]),5)
        s=a["sources"]
        self.assertEqual(len({x["url"] for x in s}),5)
        y2011=next(x for x in s if x["source_date"]=="2011-06-15")
        self.assertEqual(y2011["claimed_historical_release_year"],2002)
        self.assertEqual(y2011["candidate_names"],["葛雷基歐","葛雷洛比","葛雷吉魯","葛雷馬恩"])
        self.assertFalse(y2011["names_belong_to_2014_same_native_species_verified"])
        self.assertFalse(y2011["first_release_2014_verified"])
        y2013=next(x for x in s if x["source_date"]=="2013-12-31")
        self.assertEqual(y2013["verification"],"DIRECT_HTML_READ")
        self.assertFalse(y2013["first_release_2014_verified"])
        self.assertEqual(y2013["qualified_earliest_documented_player_experience_at_or_before"],"2013-12-31")
    def test_later_player_rules_not_original_2014_and_item_not_pet(self):
        a=self.a
        faq=next(x for x in a["sources"] if x.get("item_label")=="萬馬奔騰罐頭")
        self.assertTrue(faq["item_not_pet"])
        self.assertEqual(faq["verification"],"SEARCH_INDEX_ONLY_URL_FETCH_403")
        three=next(x for x in a["sources"] if "challenge_ticket_count_2015_claim" in x)
        five=next(x for x in a["sources"] if "horse_ticket_exchange_count_claim" in x)
        self.assertEqual((three["challenge_ticket_count_2015_claim"],five["horse_ticket_exchange_count_claim"]),(3,5))
        self.assertEqual(five["source_edited_date"],"2016-01-11")
        self.assertFalse(five["original_2014_rules_verified"])
        self.assertIsNone(a["disambiguation"]["named_2014_horse_species_original_ids"])
        self.assertTrue(a["disambiguation"]["2015_three_tickets_vs_2016_edited_five_tickets"].startswith("DIFFERENT_TIME_CONTEXT"))
    def test_source_qualification_no_false_species_counts(self):
        a,q=self.a,self.q
        self.assertEqual(set(a["region_2014_gap_reviews"]),{"CN","TW","HK_MO","JP","KR","OTHER"})
        sc=a["source_custody"]
        self.assertEqual([sc[k] for k in ["original_2014_client_bytes_acquired","new_native_pet_ids","new_spr_pixels","new_native_skill_functions","actual_original_server_pet_grants"]],[0]*5)
        self.assertIsNone(sc["official_2014_first_release_species_count"])
        self.assertIsNone(sc["global_2014_pet_species_count"])
        self.assertTrue(a["no_paid_sources"])
        self.assertTrue(a["private_server_roster_excluded"])
        self.assertTrue(a["historical_CURRENT_untouched"])
        self.assertEqual(a["startup"]["original_current_blob"],"c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertEqual(a["startup"]["original_current_bytes"],2709173)
        self.assertEqual((q["stage_A"],q["stage_B_wiki"],q["r79"],q["overall_game_completion_percent"]),(a["stage_A"],a["stage_B_wiki"],a["r79"],a["overall_percent"]))
if __name__=="__main__":
    unittest.main()
