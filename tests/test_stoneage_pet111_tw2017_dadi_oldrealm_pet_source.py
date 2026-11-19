"""PET111: 2017 Taozhu original-PC new/legacy realm pet rules, no native grant promotion."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REC = ROOT / "research/recovered"
AUDIT = REC / "STONEAGE-PET111-TW2017-DADI-OLDREALM-PET-ISSUANCE-SOURCE-BOUNDARY-R1.json"
QUEUE = REC / "STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"
REPORT = ROOT / "docs/continuity/STONEAGE-PET111-TW2017-DADI-SAYINAS-PET-REWARD-REALM-BOUNDARY-20261118.md"

class Pet111Tw2017RealmPetAcquisition(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=json.loads(AUDIT.read_text(encoding="utf-8"))
        cls.q=json.loads(QUEUE.read_text(encoding="utf-8"))

    def test_active_year_open_and_reusable_2016_review(self):
        a,q=self.a,self.q
        y=next(v for v in q["yearly_work_queue"] if v["year"]==2017)
        self.assertEqual((a["active_module"],q["active_module"]),("PET","PET"))
        self.assertEqual((a["frontier_before"],a["frontier_after"]),(2017,2017))
        self.assertEqual(y["research_gate"],"SOURCE_BOUNDED_REVIEWED")  # preserved 2017 year review
        self.assertGreaterEqual(q["current_frontier"]["year"],2020)  # forward-only later year cursors remain valid
        self.assertFalse(a["year_closed"])
        self.assertFalse(a["historically_complete"])
        self.assertIn(a["id"],[r["id"] for r in y["partial_source_review_receipts"]])
        self.assertEqual(y["partial_source_review_receipts"][0]["id"],a["id"])
        self.assertGreaterEqual(int(q["current_frontier"]["next"].split(":")[0][3:]),112) # forward-only later PET numbers remain admissible
        self.assertEqual(q["yearly_work_queue"][17]["research_gate"],"SOURCE_BOUNDED_REVIEWED")
        self.assertIn(a["main_baseline"].get("previous_annual_id","PET110-YEAR2016-SIX-REGION-SOURCE-BOUNDED-AUDIT-20261118"),[z["id"] for z in q["root_source_census_receipts"]])
        self.assertIn("PET111",REPORT.read_text(encoding="utf-8"))

    def test_same_year_operator_relay_not_operator_native_or_grant(self):
        a=self.a
        sources={x["id"]:x for x in a["sources"]}
        self.assertEqual(len(sources),6)
        notice=sources["TW2017-0427-PTT-CONTEMPORARY-OPERATOR-RELAY"]
        self.assertEqual(notice["post_date"],"2017-04-27 22:56:32")
        self.assertEqual(notice["embedded_announcement_date"],"2017-04-26 00:34")
        self.assertFalse(notice["original_operator_html_obtained"])
        self.assertFalse(notice["native_server_execution_proven"])
        self.assertIn("RELAY",notice["grade"])
        self.assertEqual(sources["TW2020-MAY-LATER-RELAY-SAME-NOTICE"]["prior_notice_duplicate"],notice["id"])
        assert sources["TW2025-2017-SEASONAL-TASK-INDEX"]["listed_task_labels"] == [
          "雞祥如意賀新春(2017春節)","萬聖節舞會(2017萬聖節)"
        ]
        self.assertTrue(all(a["namespace_qualifications"].values()))

    def test_dadi_policy_not_same_as_legacy(self):
        a=self.a
        p=a["planned_dadi_policy_from_period_2017_relay"]
        self.assertEqual((p["new_realm"],p["legacy_realm"]),("大地女神","薩伊那斯"))
        self.assertEqual(p["expected_start"],"2017-05-01 00:00:01")
        self.assertTrue(p["wild_catch_level1_pets"])
        self.assertTrue(p["quest_level1_pets"])
        self.assertTrue(p["pet_store_level1_pets"])
        self.assertTrue(p["lottery_no_longer_provides_pets"])
        self.assertTrue(p["fusion_pets_and_magic_and_professions_and_socketing_disabled"])
        self.assertTrue(p["no_character_migration"])
        self.assertIsNone(p["starting_pet_for_new_character_named"])
        self.assertEqual(p["early_new_char_login_blue_tiger_reward_name"],"藍虎")
        self.assertEqual(p["limited_reward_deadline"],"2017-05-31")
        self.assertFalse(p["actual_server_deployment_and_grants_verified"])
        self.assertTrue(p["operator_2017_original_page_unavailable"])

    def test_zero_new_native_bytes_and_original_history_preserved(self):
        a,q=self.a,self.q
        for key in ("new_original_2017_pc_client_bytes","new_original_2017_pc_patch_bytes",
                    "new_native_pet_ids","new_original_spr_pixels","new_native_skill_functions",
                    "new_original_server_pet_grants"):
            self.assertEqual(a[key],0)
        for key,val in a["original_client_custody"].items():
            if key=="original_2017_build_sha256":
                self.assertIsNone(val)
            else:
                self.assertEqual(val,0)
        self.assertIsNone(a["global_2017_original_pc_species_count"])
        self.assertIsNone(a["first_released_2017_original_pc_species_count"])
        self.assertTrue(all(a["negative_controls"].values()))
        raw=(ROOT/"docs/CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(raw),a["main_baseline"]["original_current_size"])
        git_blob=hashlib.sha1(b"blob "+str(len(raw)).encode("ascii")+b"\x00"+raw).hexdigest()
        self.assertEqual(git_blob,a["main_baseline"]["original_current_blob"])
        self.assertEqual((a["stage_A"],a["stage_B_wiki"],a["r79"],a["overall_percent"]),
                         (q["stage_A"],q["stage_B_wiki"],q["r79"],q["overall_game_completion_percent"]))

if __name__=="__main__":
    unittest.main()
