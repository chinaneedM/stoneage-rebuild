"""PET95: 2014 original-PC source-first boundaries, no false pet species or year closure."""
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REC=ROOT/"research/recovered"
A=REC/"STONEAGE-PET95-YEAR2014-CN-TW-ORIGINAL-PC-SOURCE-FIRST-PASS-R1.json"
Q=REC/"STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"
class PET95(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=json.loads(A.read_text(encoding="utf-8"))
        cls.q=json.loads(Q.read_text(encoding="utf-8"))
    def test_year_open_chronology_and_unique_receipt(self):
        a,q=self.a,self.q
        self.assertEqual((a["year"],a["year_frontier_before"],a["year_frontier_after"]),(2014,2014,2014))
        self.assertEqual(q["current_frontier"]["year"],2014)
        self.assertTrue(q["current_frontier"]["next"].startswith("PET96:"))
        self.assertEqual(q["yearly_work_queue"][15]["research_gate"],"NOT_YEAR_AUDITED")
        self.assertEqual(a["review_status"],"PARTIAL_NOT_YEAR_AUDITED")
        self.assertFalse(a["year_source_bounded_closed"])
        self.assertFalse(a["historically_complete"])
        self.assertTrue(a["year_reopenable"])
        self.assertEqual(q["active_module"],"PET")
        ids=[x["id"] for x in q["root_source_census_receipts"]]
        self.assertEqual(ids[-1],a["id"])
        self.assertEqual(len(set(ids)),len(ids))
        self.assertEqual(q["yearly_work_queue"][15]["partial_source_review_receipts"][-1]["id"],a["id"])
        self.assertIsNone(a["global_2014_original_pc_species_total"])
        self.assertIsNone(a["first_release_2014_pet_species_total"])
    def test_evidence_grades_and_version_lanes(self):
        a=self.a
        self.assertEqual(set(a["regions"]),{"CN","TW","HK_MO","KR","JP","OTHER"})
        self.assertEqual(set(a["region_reviews"]),set(a["regions"]))
        self.assertEqual(len(a["sources"]),5)
        self.assertEqual(len({s["url"] for s in a["sources"]}),5)
        cn=next(s for s in a["sources"] if s["id"].startswith("CN2014"))
        tw=next(s for s in a["sources"] if s["id"].startswith("TW2014-APR08"))
        kr=next(s for s in a["sources"] if s["id"].startswith("KR2014"))
        self.assertEqual(cn["version_lanes"],["2.5","8.5","9.0"])
        self.assertFalse(cn["original_client_verified"])
        self.assertEqual(cn["claimed_original_dates"],["2014-07-17","2014-07-23"])
        self.assertEqual(tw["published_date"],"2014-04-08")
        self.assertEqual(tw["planned_effective_date"],"2014-04-09")
        self.assertEqual(tw["original_operator_page_access"],"TIMEOUT_NOT_READ")
        self.assertFalse(tw["merge_executed_verified"])
        self.assertEqual(kr["product_line"],"STONEAGE_MOBILE_DISTINCT_FROM_ORIGINAL_PC")
        self.assertTrue(all(a["negative_controls"].values()))
    def test_missing_native_and_regional_reopen(self):
        a=self.a
        self.assertEqual(set(a["source_custody"].values()),{0})
        self.assertTrue(all(x["actual_species_total"] is None for x in a["region_reviews"].values()))
        self.assertTrue(all(x["research_gate"]=="NOT_YEAR_AUDITED" for x in a["region_reviews"].values()))
        self.assertTrue(all(x["reopen_trigger"] for x in a["region_reviews"].values()))
        self.assertEqual(a["original_current_blob"],"c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertTrue(a["historical_CURRENT_untouched"])
        self.assertEqual((a["stage_A"],a["stage_B_wiki"],a["r79"],a["overall_percent"]),("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING",None))
        self.assertEqual((self.q["stage_A"],self.q["stage_B_wiki"],self.q["r79"],self.q["overall_game_completion_percent"]),("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING",None))
if __name__=="__main__":
    unittest.main()
