"""PET98: 2014 Taiwan pet reward candidates are not proved 2014 live first-release species."""
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REC=ROOT/"research/recovered"
P=REC/"STONEAGE-PET98-TW2014-SEASONAL-QUEST-PET-REWARD-GRADED-LINKS-R1.json"
Q=REC/"STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"
class Pet98SeasonalRewards(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=json.loads(P.read_text(encoding="utf-8"))
        cls.q=json.loads(Q.read_text(encoding="utf-8"))
    def test_year_still_open_and_receipts_forward_only(self):
        a,q=self.a,self.q
        self.assertEqual((a["year"],a["frontier_before"],a["frontier_after"]),(2014,2014,2014))
        self.assertEqual(a["active_module"],"PET")
        self.assertEqual(a["review_status"],"PARTIAL_NOT_YEAR_AUDITED")
        self.assertFalse(a["historically_complete"])
        self.assertFalse(a["year_closed"])
        self.assertEqual(q["current_frontier"]["year"],2014)
        self.assertTrue(q["current_frontier"]["next"].startswith("PET99:"))
        self.assertEqual(q["yearly_work_queue"][15]["research_gate"],"NOT_YEAR_AUDITED")
        self.assertEqual(q["root_source_census_receipts"][-1]["id"],a["id"])
        self.assertEqual(q["yearly_work_queue"][15]["partial_source_review_receipts"][-1]["id"],a["id"])
        self.assertEqual(len({x["id"] for x in q["root_source_census_receipts"]}),len(q["root_source_census_receipts"]))
    def test_source_grade_not_original_operator_2014(self):
        a=self.a
        sources=a["sources"]
        self.assertEqual(len(sources),4)
        self.assertEqual(len({x["id"] for x in sources}),4)
        self.assertEqual(len({x["url"] for x in sources}),4)
        self.assertTrue(all(x["access_grade"]=="SEARCH_INDEX_FULL_TEXT_ORIGINAL_HTML_403" or x["access_grade"]=="SEARCH_INDEX_HTML_403" for x in sources))
        chronology=next(x for x in sources if x["id"]=="TW2014-QUEST-RETRO-CHRONOLOGY")
        self.assertFalse(chronology["original_2014_operator_notice_verified"])
        faq=next(x for x in sources if x["id"]=="TW2015-0203-PTT-CANCELLED-REWARDS")
        self.assertEqual(faq["document_date"],"2015-02-03")
        self.assertFalse(faq["original_2014_award_or_cancellation_date_verified"])
        guide=next(x for x in sources if x["id"]=="TW2015-0712-BAHAMUT-RESCUED-PLAYER-QUEST")
        self.assertFalse(guide["same_species_black_tiger_and_sagelu_verified"])
        self.assertFalse(guide["original_2014_player_post_date_verified"])
    def test_four_reward_associations_not_four_new_species(self):
        a=self.a
        rows=a["historical_event_candidates"]
        self.assertEqual([x["date"] for x in rows],["2014-05-28","2014-06-11","2014-07-30","2014-09-01"])
        self.assertTrue(all(not x["year2014_operator_original"] for x in rows))
        self.assertTrue(all(not x["first_release_proven"] and x["pet_ids"] is None for x in rows))
        self.assertIn("三頭蛇",rows[0]["candidate_rewards"])
        self.assertIn("2D狼人",rows[3]["candidate_rewards"])
        self.assertIn("薩格魯",rows[3]["candidate_rewards"])
        self.assertIn("黑虎／強化黑虎",rows[3]["candidate_rewards"])
        self.assertIn("NOT_INDEPENDENT",a["object_identity_boundaries"]["黑虎／強化黑虎"])
        self.assertIn("NOT_PET",a["object_identity_boundaries"]["萬馬奔騰罐頭"])
        self.assertIn("NOT_PET",a["object_identity_boundaries"]["靈魂掠奪罐頭"])
        self.assertIn("NOT_PET",a["object_identity_boundaries"]["冰浪湧現罐頭"])
        self.assertIn("NOT_AUTOMATIC_AWARD",a["object_identity_boundaries"]["變種狼人"])
    def test_no_new_native_data_and_original_current_untouched(self):
        a,q=self.a,self.q
        self.assertEqual(set(a["gaps_by_region"]),{"CN","TW","HK_MO","KR","JP","OTHER"})
        n=a["new_native_material"]
        self.assertEqual([n[x] for x in ["client_bytes","patch_bytes","pet_ids","spr_frames","skill_functions","live_grant_records"]],[0]*6)
        self.assertIsNone(n["global_2014_original_pc_species_count"])
        self.assertIsNone(n["first_release_2014_species_count"])
        self.assertTrue(all(a["constraints"].values()))
        self.assertEqual(a["startup"]["original_current_blob"],"c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertEqual(a["startup"]["original_current_bytes"],2709173)
        self.assertEqual((a["stage_A"],a["stage_B_wiki"],a["r79"],a["overall_percent"]),("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING",None))
        self.assertEqual((q["stage_A"],q["stage_B_wiki"],q["r79"],q["overall_game_completion_percent"]),(a["stage_A"],a["stage_B_wiki"],a["r79"],a["overall_percent"]))
if __name__=="__main__":
    unittest.main()
