"""PET92: verify source-accurate Taiwan PC custody claims and independently named mobile product lines."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REC = ROOT / "research/recovered/STONEAGE-PET92-YEAR2013-TW-ORIGINAL-PC-CN-TW-JP-MOBILE-SOURCE-GATES-R1.json"
QUEUE = ROOT / "research/recovered/STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"

class PET92(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(REC.read_text(encoding="utf-8"))
        cls.q = json.loads(QUEUE.read_text(encoding="utf-8"))

    def test_not_2013_year_end_and_next_remains_same_year(self):
        r,q=self.r,self.q
        self.assertEqual((r["year_frontier_before"],r["year_frontier_after"],q["current_frontier"]["year"]),(2013,2013,2013))
        self.assertEqual(q["yearly_work_queue"][14]["research_gate"],"NOT_YEAR_AUDITED")
        self.assertEqual(r["review_status"],"PARTIAL_NOT_YEAR_AUDITED")
        self.assertFalse(r["historically_complete"])
        self.assertFalse(r["source_bounded_annual_audit_complete"])
        self.assertIsNone(r["year_boundaries"]["global_original_pc_species_count_2013"])
        self.assertIsNone(r["year_boundaries"]["first_introduced_official_pc_pet_species_count_2013"])
        self.assertTrue(q["current_frontier"]["next"].startswith("PET93:"))

    def test_forward_only_2012_2013_receipts(self):
        r,q=self.r,self.q
        ids=[x["id"] for x in q["root_source_census_receipts"]]
        self.assertEqual(ids[-2:],[ "PET91-YEAR2013-CN-OPERATOR-PET-KR-MOBILE-FIRST-PASS-20261118",r["id"]])
        self.assertEqual(len(ids),len(set(ids)))
        self.assertEqual(q["yearly_work_queue"][14]["partial_source_review_receipts"][-1]["id"],r["id"])
        self.assertEqual(q["yearly_work_queue"][13]["research_gate"],"SOURCE_BOUNDED_REVIEWED")
        self.assertFalse(q["yearly_work_queue"][13]["historically_complete"])
        self.assertEqual(q["active_module"],"PET")

    def test_source_counts_and_2012_chronology_negative_control(self):
        r=self.r
        self.assertEqual(r["source_count"],9)
        self.assertEqual(r["source_count"],len(r["sources"]))
        self.assertEqual(r["contemporary_2013_count"],8)
        self.assertEqual(r["prior_2012_reopen_control_count"],1)
        self.assertEqual(len({x["id"] for x in r["sources"]}),9)
        self.assertEqual(len({x["url"] for x in r["sources"]}),9)
        self.assertTrue(all(r["negative_controls"].values()))
        older=[x for x in r["sources"] if x["year"]==2012]
        self.assertEqual(older[0]["id"],"CN-2012-07-04-GOLD-TIGER-EARLIER-PUBLISHED")
        self.assertTrue(older[0]["prior_year_forward_only_reference"])
        self.assertFalse(older[0]["first_release_2013_verified"])

    def test_taiwan_real_192_is_user_claim_no_original_bytes(self):
        r=self.r
        tw=next(x for x in r["sources"] if x["id"]=="TW-2013-04-25-PTT-OFFICIAL-CLIENT-REAL192-PATH")
        self.assertEqual(tw["file_path_as_claimed"],r"Taozhu\StoneAge\data\real_192.bin")
        self.assertEqual(tw["native_client_bytes_acquired"],0)
        self.assertIsNone(tw["verified_sha256"])
        self.assertFalse(tw["original_distribution_verified"])
        self.assertEqual(r["native_custody"]["official_taozhu_download_page_attempt_result"],"TIMEOUT_NO_BINARY")
        self.assertEqual(r["native_custody"]["verified_new_2013_original_pc_installer_bytes"],0)

    def test_mobile_4_colors_bear_wolf_and_japan_release_planned_not_pc(self):
        s={x["id"]:x for x in self.r["sources"]}
        taiwan=s["TW-2013-07-09-JOYBOMB-ACTION-ONLINE-MOBILE-UPDATE"]
        self.assertEqual(len(taiwan["pet_name_attestations"]),4)
        self.assertFalse(taiwan["pc_original_species_eligible"])
        self.assertIn("MOBILE",taiwan["lane"])
        cn=s["CN-2013-09-03-STONEAGE-OL-MOBILE-TWO-PETS"]
        self.assertEqual(cn["pet_name_attestations"],["熊先生","人狼"])
        self.assertFalse(cn["original_pc_eligible"])
        reward=s["CN-2013-09-11-STONEAGE-OL-MOBILE-BEAR-REWARD"]
        self.assertFalse(reward["actual_reward_verified"])
        self.assertFalse(reward["original_pc_eligible"])
        jp=s["JP-2013-08-22-CJ-STONEAGE-MOBILE-PUBLISHING-LICENSE"]
        self.assertEqual(jp["release_date_kind"],"PLANNED_AUTUMN_2013")
        self.assertFalse(jp["actual_release_verified"])
        self.assertFalse(jp["original_jp_pc_eligible"])

    def test_previous_history_immutable_and_rights(self):
        r,q=self.r,self.q
        self.assertEqual(r["startup"]["current_blob"],"c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertEqual(r["startup"]["current_bytes"],2709173)
        self.assertEqual((q["stage_A"],q["stage_B_wiki"],q["r79"],q["overall_game_completion_percent"]),
                         ("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING",None))

if __name__ == "__main__":
    unittest.main()
