"""PET100: 2015 CN/TW/KR source-attestation boundary and still-open annual cursor."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REC = ROOT / "research/recovered"
RECEIPT = REC / "STONEAGE-PET100-YEAR2015-CN-TW-KR-ORIGINAL-PC-PET-SOURCE-FIRST-PASS-R1.json"
QUEUE = REC / "STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"
REPORT = ROOT / "docs/continuity/STONEAGE-PET100-YEAR2015-CN-TW-KR-ORIGINAL-PC-SOURCE-FIRST-PASS-20261118.md"

class Pet100Year2015FirstPass(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=json.loads(RECEIPT.read_text(encoding="utf-8"))
        cls.q=json.loads(QUEUE.read_text(encoding="utf-8"))

    def test_year_stays_open_after_real_source_first_pass(self):
        a,q=self.a,self.q
        self.assertEqual((a["year"],a["frontier_before"],a["frontier_after"]),(2015,2015,2015))
        self.assertEqual(a["active_module"],"PET")
        self.assertEqual(a["review_status"],"PARTIAL_NOT_YEAR_AUDITED")
        self.assertFalse(a["year_closed"])
        self.assertFalse(a["historically_complete"])
        self.assertGreaterEqual(q["current_frontier"]["year"],2015)
        self.assertTrue(a["next"].startswith("PET101:"))
        self.assertEqual(q["yearly_work_queue"][16]["research_gate"],"SOURCE_BOUNDED_REVIEWED")
        self.assertEqual(q["yearly_work_queue"][15]["research_gate"],"SOURCE_BOUNDED_REVIEWED")
        self.assertIn(a["id"],[r["id"] for r in q["root_source_census_receipts"]])
        self.assertIn(a["id"],[r["id"] for r in q["yearly_work_queue"][16]["partial_source_review_receipts"]])
        self.assertIn("PET100",REPORT.read_text(encoding="utf-8"))

    def test_six_sources_distinct_grades_and_operator_text_not_native(self):
        a=self.a
        src=a["sources"]
        self.assertEqual(len(src),6)
        self.assertEqual(len(set(s["id"] for s in src)),6)
        cn=next(s for s in src if s["id"].startswith("CN2015"))
        self.assertFalse(cn["original_2015_official_page_acquired"])
        self.assertTrue(cn["direct_html_read"])
        self.assertEqual(len(cn["text_internal_date_inconsistency"]),2)
        self.assertFalse(cn["actual_rewards_granted_verified"])
        self.assertFalse(cn["native_pet_identity_verified"])
        self.assertEqual(len(cn["service_lanes"]),2)
        tw=next(s for s in src if s["id"]=="TW2015-0922-MID_AUTUMN-OPERATOR-NOTICE-RELAY")
        self.assertEqual(tw["source_date"],"2015-09-22")
        self.assertEqual(tw["launcher_update_label"],"202")
        self.assertFalse(tw["official_original_html_directly_read"])
        self.assertFalse(tw["original_patch_bytes_read"])
        self.assertFalse(tw["client_202_verified"])
        self.assertFalse(tw["actual_server_deployed_patch_verified"])
        later=next(s for s in src if s["id"]=="TW2016-RETRO-2015-QUEST-INDEX")
        self.assertFalse(later["first_release_2015_verified"])

    def test_pc_termination_not_same_as_mobile_termination(self):
        a=self.a
        pc=next(s for s in a["sources"] if s["id"].startswith("KR2015-0821"))
        mob=next(s for s in a["sources"] if s["id"].startswith("KR2015-0522"))
        self.assertEqual(pc["pc_original_operator"],"NETMARBLE")
        self.assertEqual(pc["pc_close_effective_date_reported"],"2015-08-21")
        self.assertFalse(pc["actual_pc_shutdown_log_verified"])
        self.assertFalse(pc["original_pet_names_or_new_pet_issuance_verified"])
        self.assertEqual(mob["source_date"],"2015-05-22")
        self.assertEqual(mob["product_line"],"STONEAGE_MOBILE_NOT_PC")
        self.assertEqual(mob["planned_close_date"],pc["pc_close_effective_date_reported"])
        self.assertTrue(mob["grade"].startswith("DIRECT_FIRST_PARTY"))
        self.assertFalse(mob["pc_pet_evidence"])
        self.assertTrue(all(a["boundaries"].values()))

    def test_original_assets_not_inferred_and_history_preserved(self):
        a,q=self.a,self.q
        for k in ["native_2015_original_client_new_bytes","native_2015_original_patch_new_bytes","new_native_pet_ids","new_original_spr_pixels","new_pet_skill_functions","new_verified_server_pet_grants"]:
            self.assertEqual(a[k],0)
        self.assertIsNone(a["global_official_2015_original_pc_pet_species_count"])
        self.assertIsNone(a["new_first_released_species_2015_count"])
        self.assertEqual(set(a["region_gaps"]),{"CN","TW","HK_MO","KR","JP","OTHER"})
        raw=(ROOT/"docs/CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(raw),2709173)
        self.assertEqual(hashlib.sha1(b"blob "+str(len(raw)).encode("ascii")+b"\x00"+raw).hexdigest(),a["startup"]["original_current_blob"])
        self.assertTrue(a["original_current_unchanged"])
        self.assertEqual((q["stage_A"],q["stage_B_wiki"],q["r79"],q["overall_game_completion_percent"]),("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING",None))
        self.assertEqual((a["stage_A"],a["stage_B_wiki"],a["r79"],a["overall_percent"]),(q["stage_A"],q["stage_B_wiki"],q["r79"],q["overall_game_completion_percent"]))

if __name__=="__main__":
    unittest.main()
