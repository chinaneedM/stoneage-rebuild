"""PET102: contemporaneous 2015 TW player's box item is not a verified live pet release."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/"research/recovered/STONEAGE-PET102-TW2015-DRAGONBOAT-PLAYER-BOX-NOT-VERIFIED-PET-R1.json"
Q=ROOT/"research/recovered/STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"
REPORT=ROOT/"docs/continuity/STONEAGE-PET102-TW2015-DRAGONBOAT-PLAYER-BOX-AND-PET-ISSUANCE-BOUNDARY-20261118.md"

class Pet102FirsthandBoxEvidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=json.loads(A.read_text(encoding="utf-8"))
        cls.q=json.loads(Q.read_text(encoding="utf-8"))

    def test_year2015_remains_open_and_receipt_forward_only(self):
        a,q=self.a,self.q
        self.assertEqual((a["year"],a["year_frontier_before"],a["year_frontier_after"]),(2015,2015,2015))
        self.assertEqual(a["active_module"],"PET")
        self.assertEqual(a["annual_review_status"],"NOT_YEAR_AUDITED")
        self.assertFalse(a["year_closed"])
        self.assertFalse(a["historically_complete"])
        self.assertEqual(q["current_frontier"]["year"],2015)
        self.assertEqual(q["current_frontier"]["latest_partial_root_review"],a["id"])
        self.assertEqual(q["root_source_census_receipts"][-1]["id"],a["id"])
        self.assertEqual(q["root_source_census_receipts"][-2]["id"],a["startup"]["latest_receipt_before"])
        self.assertEqual(q["yearly_work_queue"][16]["partial_source_review_receipts"][-1]["id"],a["id"])
        self.assertEqual(q["yearly_work_queue"][16]["research_gate"],"NOT_YEAR_AUDITED")
        self.assertEqual(q["yearly_work_queue"][15]["research_gate"],"SOURCE_BOUNDED_REVIEWED")
        self.assertTrue(a["next"].startswith("PET103:"))
        self.assertTrue(q["current_frontier"]["next"].startswith("PET103:"))
        self.assertIn("PET102",REPORT.read_text(encoding="utf-8"))

    def test_2015_firsthand_quest_box_not_pet_species_or_live_pet(self):
        a=self.a; new=a["new_evidence"][0]
        self.assertEqual(len(a["new_evidence"]),4)
        self.assertEqual(new["forum_floor"],"5")
        self.assertEqual(new["floor_edited_date"],"2015-09-25 11:54:05")
        self.assertEqual(new["gameplay_claim_date_in_floor"],"09/24")
        self.assertEqual(new["gameplay_claim_year_from_same_floor_context"],2015)
        self.assertTrue(new["original_live_page_directly_read"])
        self.assertEqual(new["claimed_item_label"],"三頭蛇禮盒")
        self.assertEqual(new["quest_label"],"2015五月節的插曲")
        self.assertEqual(new["claimed_holder"],"人物一")
        self.assertTrue(new["contemporaneous_evidence_of_named_item"])
        self.assertTrue(new["claim_grade"].startswith("PLAYER_REPORTED"))
        self.assertFalse(new["original_server_grant_log_verified"])
        self.assertFalse(new["box_opening_pet_contents_verified"])
        self.assertFalse(new["any_live_pet_granted_verified"])
        self.assertFalse(new["three_headed_snake_pet_received_proved"])
        self.assertFalse(new["original_2015_pc_pet_id_verified"])

    def test_2016_retrospective_and_2017_2023_not_backdated(self):
        a=self.a
        later=a["new_evidence"][1]
        self.assertEqual(later["date_claimed_in_later_text"],"2015-06-17")
        self.assertFalse(later["source_is_2015_contemporaneous"])
        self.assertFalse(later["first_party_june_2015_operator_notice_retrieved"])
        self.assertFalse(later["live_first_issuance_confirmed"])
        self.assertEqual(a["new_evidence"][2]["source_year"],2017)
        self.assertEqual(a["new_evidence"][3]["source_year"],2023)
        self.assertFalse(a["new_evidence"][2]["retroactively_confirm_2015_snake_box_contents"])
        self.assertFalse(a["new_evidence"][3]["retroactively_prove_2015_reward_table"])
        self.assertTrue(all(a["historical_cross_year_separation"].values()))
        self.assertTrue(all(a["boundary_guards"].values()))
        self.assertEqual(set(a["region_gaps"]),{"CN","TW","HK_MO","KR","JP","OTHER"})

    def test_no_original_bytes_no_fake_population_original_history_immutable(self):
        a,q=self.a,self.q
        self.assertEqual(a["new_contested_firsthand_player_observed_quest_reward_item_records"],1)
        for k in ["new_authenticated_2015_original_pc_client_bytes","new_authenticated_2015_original_patch_bytes","new_native_pet_ids","new_original_spr_assets","new_native_skill_functions","new_official_verified_live_pet_grants"]:
            self.assertEqual(a[k],0)
        self.assertIsNone(a["global_official_2015_pet_species_count"])
        self.assertIsNone(a["first_issued_2015_pet_species_count"])
        raw=(ROOT/"docs/CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(raw),a["startup"]["original_current_bytes"])
        self.assertEqual(hashlib.sha1(b"blob "+str(len(raw)).encode("ascii")+b"\x00"+raw).hexdigest(),a["startup"]["original_current_blob"])
        self.assertTrue(a["original_current_state_unchanged"])
        self.assertEqual((q["stage_A"],q["stage_B_wiki"],q["r79"],q["overall_game_completion_percent"]),("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING",None))
        self.assertEqual((a["stage_A"],a["stage_B_wiki"],a["r79"],a["overall_percent"]),(q["stage_A"],q["stage_B_wiki"],q["r79"],q["overall_game_completion_percent"]))

if __name__=="__main__":
    unittest.main()
