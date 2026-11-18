"""PET97: dated 2014 Taiwan PC version-198 player witnesses are not client bytes or native pets."""
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RE=ROOT/"research/recovered"
A=RE/"STONEAGE-PET97-TW2014-TAOZHU-PC198-DOWNLOAD-AND-BYTE-CUSTODY-GATES-R1.json"
Q=RE/"STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"
class Pet97Taozhu198(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=json.loads(A.read_text(encoding="utf-8"))
        cls.q=json.loads(Q.read_text(encoding="utf-8"))
    def test_forward_only_2014_partial_receipt_and_next(self):
        a,q=self.a,self.q
        self.assertEqual((a["year"],a["frontier_before"],a["frontier_after"]),(2014,2014,2014))
        self.assertEqual(a["active_module"],"PET")
        self.assertEqual(a["review_status"],"PARTIAL_NOT_YEAR_AUDITED")
        self.assertFalse(a["year_closed"])
        self.assertFalse(a["historically_complete"])
        self.assertEqual(q["yearly_work_queue"][15]["research_gate"],"NOT_YEAR_AUDITED")
        self.assertEqual(q["current_frontier"]["year"],2014)
        self.assertGreaterEqual(int(q["current_frontier"]["next"].split(":")[0][3:]),98)
        self.assertIn(a["id"],[x["id"] for x in q["root_source_census_receipts"]])
        self.assertIn(a["id"],[x["id"] for x in q["yearly_work_queue"][15]["partial_source_review_receipts"]])
        self.assertEqual(len({x["id"] for x in q["root_source_census_receipts"]}),len(q["root_source_census_receipts"]))
    def test_period_player_version_string_is_not_original_deployment(self):
        a=self.a
        self.assertEqual(a["specific_line"]["year"],2014)
        self.assertEqual(a["specific_line"]["region"],"TW")
        self.assertEqual(a["specific_line"]["operator"],"TAOZHU")
        self.assertEqual(a["specific_line"]["product_line"],"ORIGINAL_PC")
        self.assertEqual(a["specific_line"]["historical_launcher_version_string"],"198")
        self.assertIsNone(a["specific_line"]["original_first_party_build_signature"])
        self.assertIsNone(a["specific_line"]["confirmed_official_client_checksum_sha256"])
        self.assertEqual(len(a["sources"]),5)
        self.assertEqual(len({x["id"] for x in a["sources"]}),5)
        first=next(x for x in a["sources"] if x["source_date"]=="2014-08-31")
        self.assertEqual(first["read_access"],"DIRECT_PUBLIC_HTML_READ_OF_LATER_HOST_MIRROR")
        self.assertFalse(first["official_pet_release_verified"])
        ptt=next(x for x in a["sources"] if x["source_date"]=="2014-09-09")
        self.assertEqual(ptt["read_access"],"SEARCH_INDEX_FULL_SNIPPET_ORIGINAL_PTT_HTML_FETCH_403")
        self.assertFalse(ptt["official_pet_release_verified"])
        self.assertTrue(all(not x["official_pet_release_verified"] for x in a["sources"]))
    def test_three_links_not_three_downloaded_binaries(self):
        a=self.a
        u={x["purpose"]:x for x in a["primary_candidate_paths"]}
        self.assertEqual(len(u),3)
        self.assertEqual({x["url"] for x in u.values()},{
            "http://www.stoneage.tw/download.php?c=1",
            "http://www.stoneage.tw/download.php?c=2",
            "https://www.dropbox.com/s/lpjk9r658h6kxac/Sa_Free_installation.exe?dl=0"
        })
        self.assertTrue(all(x["status"]=="LINK_RECORDED_SOURCE_DID_NOT_RETURN_BYTES" for x in u.values()))
        v=a["access_validation"]
        self.assertEqual((v["local_downloaded_installers"],v["local_downloaded_patch_files"],v["original_bytes_new"]),(0,0,0))
        self.assertFalse(v["sha256_verified"])
        self.assertFalse(v["crc_verified"])
        self.assertFalse(v["malware_scan_possible"])
        self.assertFalse(v["provenance_attested_as_official_bytes"])
        self.assertEqual(v["web_dropbox"],"NOT_ACCESSIBLE_VIA_WEB_TOOL")
        self.assertIn("NO_SERVER_AVAILABILITY_INFERENCE",v["container_http"])
        self.assertTrue(a["negative_controls"]["do_not_claim_link_is_dead_from_tool_inaccessibility"])
    def test_native_pet_counts_unclaimed_and_six_regions_separate(self):
        a,q=self.a,self.q
        n=a["native_pet_evidence"]
        self.assertEqual([n[k] for k in ["new_native_pet_ids","new_native_spr_frames","new_native_pet_skill_code","new_live_2014_issue_records"]],[0,0,0,0])
        self.assertIsNone(n["first_released_2014_species_total"])
        self.assertIsNone(n["global_original_pc_2014_species_total"])
        self.assertFalse(n["per_region_totals_verified"])
        self.assertEqual(set(a["all_2014_regions"]),{"CN","TW","HK_MO","KR","JP","OTHER"})
        self.assertTrue(all(a["negative_controls"].values()))
        self.assertEqual(a["starting_remote"]["current_state_original_blob"],"c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertEqual(a["starting_remote"]["current_state_original_bytes"],2709173)
        self.assertTrue(a["historical_CURRENT_unchanged"])
        self.assertEqual((a["stage_A"],a["stage_B_wiki"],a["r79"],a["overall_completion_percent"]),("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING",None))
        self.assertEqual((q["stage_A"],q["stage_B_wiki"],q["r79"],q["overall_game_completion_percent"]),(a["stage_A"],a["stage_B_wiki"],a["r79"],a["overall_completion_percent"]))
if __name__=="__main__":
    unittest.main()
