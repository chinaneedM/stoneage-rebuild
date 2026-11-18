"""PET101: 2015 Taiwan original-PC numeric version sources and Hong Kong/Macau license boundary."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REC = ROOT / "research/recovered"
A = REC / "STONEAGE-PET101-TW2015-PC199-200-202-HKMO-ORIGINAL-LICENSE-BOUNDARY-R1.json"
Q = REC / "STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"
REPORT = ROOT / "docs/continuity/STONEAGE-PET101-TW2015-PC199-200-202-HKMO-ORIGINAL-LICENSE-BOUNDARY-20261118.md"

class Pet101Taiwan2015VersionsAndHkMoLicense(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = json.loads(A.read_text(encoding="utf-8"))
        cls.q = json.loads(Q.read_text(encoding="utf-8"))

    def test_source_research_not_annual_close_or_pet_population(self):
        a, q = self.a, self.q
        self.assertEqual((a["year"],a["frontier_before"],a["frontier_after"]),(2015,2015,2015))
        self.assertEqual(a["active_module"], "PET")
        self.assertEqual(a["review_status"], "PARTIAL_NOT_YEAR_AUDITED")
        self.assertFalse(a["year_closed"])
        self.assertFalse(a["historically_complete"])
        self.assertEqual(q["current_frontier"]["year"], 2015)
        self.assertEqual(q["yearly_work_queue"][16]["research_gate"],"NOT_YEAR_AUDITED")
        self.assertEqual(q["yearly_work_queue"][15]["research_gate"],"SOURCE_BOUNDED_REVIEWED")
        self.assertEqual(q["current_frontier"]["latest_partial_root_review"],a["id"])
        self.assertEqual(q["root_source_census_receipts"][-1]["id"],a["id"])
        self.assertEqual(q["root_source_census_receipts"][-2]["id"],a["startup"]["latest_partial_review"])
        self.assertEqual(q["yearly_work_queue"][16]["partial_source_review_receipts"][-1]["id"],a["id"])
        self.assertTrue(a["next"].startswith("PET102:"))
        self.assertTrue(q["current_frontier"]["next"].startswith("PET102:"))
        self.assertTrue(all(a["boundaries"].values()))
        self.assertIn("PET101",REPORT.read_text(encoding="utf-8"))

    def test_199_200_202_are_not_authenticated_clients(self):
        a=self.a
        v=a["tw_version_evidence"]
        self.assertEqual([x["reported_version_label"] if "reported_version_label" in x else x["claimed_version_label"] for x in v],["199","200","202"])
        self.assertEqual(v[0]["date_in_later_guide"],"2015-02-25")
        self.assertTrue(v[0]["post_contains_later_205_reference"])
        self.assertFalse(v[0]["original_2015_installer_bytes_acquired"])
        self.assertFalse(v[0]["original_release_date_confirmed"])
        self.assertEqual(v[1]["source_edit_date"],"2015-03-06")
        self.assertIn("stoneage2.com.tw/download.php?c=2",v[1]["original_taozhu_download_page"])
        self.assertEqual(v[1]["workflow_described"][:2],["launch.exe","Newlaunch.exe"])
        self.assertFalse(v[1]["original_patch_bytes_acquired"])
        self.assertEqual(v[2]["source_date"],"2015-09-22")
        self.assertIn("id=1453",v[2]["original_taozhu_news_url"])
        self.assertFalse(v[2]["original_2015_client_or_patch_bytes_acquired"])
        self.assertTrue(all(not x["pet_identity_proof"] for x in v))

    def test_bounded_access_and_license_not_2015_hkmo_species(self):
        a=self.a
        self.assertEqual(len(a["attempted_historical_access"]),4)
        self.assertTrue(all(x["bytes_verified"]==0 for x in a["attempted_historical_access"]))
        self.assertTrue(all(x["web_open_result"]=="NOT_ACCESSIBLE_VIA_TOOL" for x in a["attempted_historical_access"]))
        p=a["hk_mo_license"]
        self.assertEqual(p["primary_text_publication_date"],"2011-09-08")
        self.assertEqual(p["original_issuer"],"DigiPark Inc.")
        self.assertEqual(p["licensee"],"Taozhu Ltd.")
        self.assertEqual(p["licensed_regions"],["HK","MO"])
        self.assertEqual(p["source_grade"],"CONTEMPORANEOUS_PUBLISHER_PRESS_RELEASE_REPRINTED_VERBATIM_IN_4GAMER")
        self.assertTrue(p["licensed_taiwan_operator_same"])
        self.assertFalse(p["independent_hkmo_server_in_2015_verified"])
        self.assertFalse(p["hkmo_2015_pc_client_proven_same_as_tw202"])
        self.assertFalse(p["hkmo_2015_official_pet_species_verified"])
        self.assertEqual(set(a["region_gaps"]),{"CN","TW","HK_MO","KR","JP","OTHER"})

    def test_no_new_original_pet_bytes_and_immutable_historical_current(self):
        a,q=self.a,self.q
        for k in ["new_authentic_2015_original_pc_client_bytes","new_authentic_2015_original_pc_patch_bytes","new_2015_native_pet_ids","new_native_original_spr_assets","new_native_skill_records","new_verified_server_pet_grants"]:
            self.assertEqual(a[k],0)
        self.assertIsNone(a["official_global_species_total_2015"])
        self.assertIsNone(a["new_official_first_issued_species_2015"])
        raw=(ROOT/"docs/CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(raw),a["startup"]["current_state_git_blob_bytes"])
        digest=hashlib.sha1(b"blob "+str(len(raw)).encode("ascii")+b"\x00"+raw).hexdigest()
        self.assertEqual(digest,a["startup"]["current_state_blob_sha"])
        self.assertTrue(a["original_current_state_unchanged"])
        self.assertEqual((q["stage_A"],q["stage_B_wiki"],q["r79"],q["overall_game_completion_percent"]),("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING",None))
        self.assertEqual((a["stage_A"],a["stage_B_wiki"],a["r79"],a["overall_game_completion_percent"]),(q["stage_A"],q["stage_B_wiki"],q["r79"],q["overall_game_completion_percent"]))

if __name__ == "__main__":
    unittest.main()
