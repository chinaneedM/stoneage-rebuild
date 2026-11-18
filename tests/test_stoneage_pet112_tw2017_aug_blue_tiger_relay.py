"""PET112: 2017 Aug contemporary operator-voice relay stays distinct from native PET grants."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT/"research/recovered/STONEAGE-PET112-TW2017-AUGUST-BLUE-TIGER-PROMOTION-SOURCE-BOUNDARY-R1.json"
PET111=ROOT/"research/recovered/STONEAGE-PET111-TW2017-DADI-OLDREALM-PET-ISSUANCE-SOURCE-BOUNDARY-R1.json"
QUEUE=ROOT/"research/recovered/STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"
REPORT=ROOT/"docs/continuity/STONEAGE-PET112-TW2017-AUGUST-BLUE-TIGER-REOPENED-PROMOTION-20261118.md"

class Pet112Tw2017AugustBlueTiger(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=json.loads(AUDIT.read_text(encoding="utf-8"))
        cls.p=json.loads(PET111.read_text(encoding="utf-8"))
        cls.q=json.loads(QUEUE.read_text(encoding="utf-8"))

    def test_relay_custody_and_2017_gate(self):
        a,p,q=self.a,self.p,self.q
        y=next(z for z in q["yearly_work_queue"] if z["year"]==2017)
        self.assertEqual((a["year"],a["region"],a["active_module"]),(2017,"TW","PET"))
        self.assertEqual(a["parent_pet111"],p["id"])
        self.assertEqual((q["current_frontier"]["year"],y["research_gate"]),(2019,"SOURCE_BOUNDED_REVIEWED"))  # PET113 forward-only year audit
        self.assertEqual(q["current_frontier"]["latest_2017_partial_source_receipt"],a["id"])
        self.assertTrue(q["current_frontier"]["next"].startswith(("PET113:","PET114:","PET115:","PET116:")))
        self.assertEqual([z["id"] for z in y["partial_source_review_receipts"]][:2],[p["id"],a["id"]])
        self.assertFalse(a["historically_complete"])
        self.assertFalse(a["year_closed"])
        s=a["new_source"]
        self.assertTrue(s["accessible_original_mirror_text"])
        self.assertFalse(s["firstparty_operator_facebook_html_obtained"])
        self.assertFalse(s["native_server_event_proven"])
        self.assertEqual(s["post_date"],"2017-08-28 15:27")
        self.assertIn("RELAY",s["grade"])
        self.assertEqual(s["unique_source_count"],1)

    def test_two_cohorts_different_from_pet111_first_promotion(self):
        a=self.a
        b=a["announced_second_wave"]
        self.assertEqual(b["prior_first_wave_pet111_deadline"],"2017-05-31")
        self.assertEqual(b["reopened_after_maintenance"],"2017-08-30")
        self.assertEqual(b["end_at_maintenance"],"2017-11-01")
        self.assertEqual(b["reward_pet_label"],"藍虎")
        self.assertEqual(b["older_user_cohort"]["strict_character_level_gt"],99)
        self.assertEqual(b["older_user_cohort"]["operator_voice_claim_location"],"薩村廣場")
        self.assertTrue(b["announced_repeat_not_first_release"])
        self.assertTrue(b["not_independent_second_species"])
        self.assertFalse(b["new_user_cohort"]["native_auto_grant_verified"])
        self.assertFalse(b["older_user_cohort"]["native_npc_script_verified"])
        self.assertFalse(b["distinct_reward_item_id_proven"])

    def test_no_native_promotion_and_original_current_untouched(self):
        a=self.a
        for k in ("new_2017_original_pc_client_bytes","new_2017_original_pc_patch_bytes","new_2017_native_pet_ids","new_2017_original_spr_frames","new_2017_native_skill_functions","new_2017_server_pet_grant_logs"):
            self.assertEqual(a[k],0)
        self.assertIsNone(a["global_2017_original_pc_species_count"])
        self.assertIsNone(a["first_released_2017_original_pc_species_count"])
        self.assertTrue(all(a["negative_controls"].values()))
        raw=(ROOT/"docs/CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(raw),a["base"]["unchanged_current_state_bytes"])
        sha=hashlib.sha1(b"blob "+str(len(raw)).encode("ascii")+b"\x00"+raw).hexdigest()
        self.assertEqual(sha,a["base"]["unchanged_current_state_blob"])
        self.assertIn("PET112",REPORT.read_text(encoding="utf-8"))

if __name__=="__main__":
    unittest.main()
