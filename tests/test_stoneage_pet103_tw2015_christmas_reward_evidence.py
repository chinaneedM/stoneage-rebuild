"""PET103 source-exact 2015 TW Christmas reward, operator relay and year-open boundaries."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REC=ROOT/"research/recovered"
A=REC/"STONEAGE-PET103-TW2015-CHRISTMAS-PLAYER-REWARDS-NOT-NATIVE-PET-R1.json"
Q=REC/"STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"
REPORT=ROOT/"docs/continuity/STONEAGE-PET103-TW2015-CHRISTMAS-PLAYER-REWARDS-AND-ORIGINAL-NOTICE-RELAY-20261118.md"

class Pet103Tw2015Christmas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=json.loads(A.read_text(encoding="utf-8"))
        cls.q=json.loads(Q.read_text(encoding="utf-8"))

    def test_frontier_preserved_and_additive_receipt(self):
        a,q=self.a,self.q
        self.assertEqual((a["year"],a["year_frontier_before"],a["year_frontier_after"]),(2015,2015,2015))
        self.assertEqual(a["annual_review_status"],"NOT_YEAR_AUDITED")
        self.assertFalse(a["year_closed"])
        self.assertFalse(a["historically_complete"])
        self.assertEqual(a["active_module"],"PET")
        self.assertEqual(q["current_frontier"]["year"],2015)
        self.assertEqual(q["yearly_work_queue"][16]["research_gate"],"NOT_YEAR_AUDITED")
        self.assertEqual(q["yearly_work_queue"][15]["research_gate"],"SOURCE_BOUNDED_REVIEWED")
        self.assertIn(a["id"],[x["id"] for x in q["root_source_census_receipts"]])
        self.assertEqual(q["root_source_census_receipts"][[x["id"] for x in q["root_source_census_receipts"]].index(a["id"])-1]["id"],a["startup"]["previous_receipt"])
        self.assertIn(a["id"],[x["id"] for x in q["yearly_work_queue"][16]["partial_source_review_receipts"]])
        self.assertTrue(a["next"].startswith("PET104:"))
        self.assertIn("PET103",REPORT.read_text(encoding="utf-8"))

    def test_source_is_relay_and_event_spans_2016(self):
        a=self.a;s=a["sources"]
        self.assertEqual(len(s),4)
        self.assertEqual(len(set(x["id"] for x in s)),4)
        op=s[0]
        self.assertEqual(op["forum_floor"],"1")
        self.assertEqual(op["quoted_original_publication"],"2015-12-22 21:00")
        self.assertEqual(op["forum_floor_edit_date"],"2015-12-23 12:15:48")
        self.assertEqual(op["claimed_original_operator_notice_url"],"http://www.stoneage.tw/news.php?id=1486")
        self.assertEqual(op["planned_event_start"],"2015-12-23 after weekly maintenance")
        self.assertEqual(op["planned_event_end"],"2016-01-06 maintenance")
        self.assertFalse(op["original_operator_html_retrieved"])
        self.assertFalse(op["original_notice_has_explicit_pet_prize_list"])
        self.assertFalse(op["original_pc_client_verified"])
        self.assertTrue(all(a["object_identity_boundaries"].values()))
        self.assertFalse(a["potential_other_2015_lead"]["direct_full_page_retrieved"])

    def test_2015_firsthand_reward_claims_not_new_species(self):
        a=self.a;s=a["sources"]
        self.assertEqual(s[1]["post_time"],"2015-12-23 18:25:07")
        self.assertEqual(s[1]["reply_time"],"2015-12-23 19:38:17")
        self.assertEqual(s[1]["reported_results"],["魯道夫","冠軍豬"])
        self.assertFalse(s[1]["champion_pig_live_pet_verified"])
        self.assertFalse(s[1]["rudolph_native_pet_id_verified"])
        self.assertEqual(s[2]["claim_dates"],["2015-12-26 00:30:51","2015-12-27 17:08:43","2015-12-29 18:25:24"])
        self.assertEqual(s[2]["reported_labels"][:4],["庫胖達","胖達利","布伊酷","魯道夫"])
        self.assertFalse(s[2]["first_party_server_grants_verified"])
        kinds={v["name"]:v["kind"] for v in s[3]["reported_reward_objects"]}
        self.assertEqual(kinds["魯道夫的韁繩"],"REIN_ITEM")
        self.assertEqual(kinds["獎杯 冠軍豬"],"TROPHY_ITEM")
        self.assertEqual(kinds["胖達利盒子"],"BOX_ITEM")
        self.assertEqual(kinds["麋鹿套裝"],"EQUIPMENT_SET")
        self.assertFalse(s[3]["same_build_pet_identity_verified"])
        self.assertFalse(s[3]["first_party_probability_known"])

    def test_no_native_pixels_pets_or_mutation_of_current(self):
        a,q=self.a,self.q
        self.assertEqual(a["new_directly_readable_contemporaneous_threads"],1)
        self.assertEqual(a["new_contemporaneous_player_reward_report_groups"],3)
        self.assertEqual(a["new_original_operator_notice_target_urls"],1)
        self.assertEqual(set(a["region_gaps"]),{"CN","TW","HK_MO","KR","JP","OTHER"})
        for k in ["new_authenticated_2015_original_pc_client_bytes","new_authenticated_2015_original_pc_patch_bytes","new_native_pet_ids","new_original_spr_assets","new_native_skill_functions","new_verified_first_party_live_pet_grants"]:
            self.assertEqual(a[k],0)
        self.assertIsNone(a["global_official_2015_original_pc_pet_species_count"])
        self.assertIsNone(a["first_issued_2015_pet_species_count"])
        raw=(ROOT/"docs/CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(raw),a["startup"]["original_current_bytes"])
        sha=hashlib.sha1(b"blob "+str(len(raw)).encode("ascii")+b"\x00"+raw).hexdigest()
        self.assertEqual(sha,a["startup"]["original_current_blob"])
        self.assertTrue(a["original_current_state_unchanged"])
        self.assertEqual((q["stage_A"],q["stage_B_wiki"],q["r79"],q["overall_game_completion_percent"]),("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING",None))
        self.assertEqual((a["stage_A"],a["stage_B_wiki"],a["r79"],a["overall_percent"]),(q["stage_A"],q["stage_B_wiki"],q["r79"],q["overall_game_completion_percent"]))

if __name__=="__main__":
    unittest.main()
