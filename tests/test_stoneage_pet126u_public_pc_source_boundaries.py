"""PET126U: evidence-graded original PC source locator and prize-item non-promotion."""
import json
import unittest
from pathlib import Path

R=Path(__file__).resolve().parents[1]/"research"/"recovered"

def read(name):
    return json.loads((R/name).read_text(encoding="utf-8"))

class PET126UOnlyClassicPC(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=read("STONEAGE-PET126U-KR2011-DIRECT-CDN-TW2026-REWARD-ROLES-R1.json")
        cls.prior=read("STONEAGE-KR-NETMARBLE120-R27-R1.json")
        cls.y=read("STONEAGE-PET126-YEAR2026-YTD-CLASSIC-PC-SOURCE-AND-MODULE-GAPS-R1.json")
        cls.t=read("STONEAGE-PET126T-PC-MODULE-SOURCE-COVERAGE-AND-STOP-GATE-R1.json")

    def test_direct_operator_domain_locator_is_not_downloaded_software(self):
        k=self.a["chronological_backfill_2011_KR"]
        self.assertEqual(k["contemporaneous_public_forum"]["url"],
                         "https://lab.welovesa.com/viewthread.php?tid=1326")
        self.assertEqual(k["target"]["url"],
                         "http://nmgame.cdn.netmarble.net/Stoneage/NetmarbleStoneAge120.exe")
        self.assertTrue(k["contemporaneous_public_forum"]["source_grade"].startswith("CONTEMPORANEOUS_PLAYER_POST"))
        self.assertEqual(k["target"]["observed_current_retrieval"],"FETCH_FAILED_HTTP_502_BAD_GATEWAY")
        self.assertEqual(k["target"]["original_exe_bytes_retrieved"],0)
        self.assertIsNone(k["target"]["file_size_bytes"])
        self.assertIsNone(k["target"]["sha256"])
        self.assertIsNone(k["target"]["software_version_by_120_name"])
        self.assertFalse(k["target"]["independent_operator_build_verification"])

    def test_prior_permission_denial_is_retained_without_payment(self):
        k=self.a["chronological_backfill_2011_KR"]
        self.assertEqual(self.prior["status"],"OPEN_PUBLIC_SOURCE_ACCESS_GATED_NO_PACKAGE_OBTAINED")
        self.assertEqual(k["prior_source_comparison"]["r27_prior_forum_url"],self.prior["observed_source"]["url"])
        self.assertNotEqual(k["contemporaneous_public_forum"]["url"],self.prior["observed_source"]["url"])
        self.assertFalse(k["prior_source_comparison"]["old_permission_gated_thread_reopened_or_bypassed"])
        self.assertFalse(k["prior_source_comparison"]["new_original_software_bytes_obtained"])

    def test_2026_horse_reward_family_separate_from_certificate_stones_and_feather(self):
        tw=self.a["year2026_TW_horse_text_bounded"]
        roles=tw["bounded_literally_named_pet_related_entries"]
        self.assertEqual(len(roles),8)
        self.assertEqual(tw["named_enhancement_stone_count"],5)
        self.assertEqual(sum(r["evidence_role"]=="ENHANCEMENT_STONE_ITEM_NOT_LIVE_PET" for r in roles),5)
        self.assertEqual(roles[0]["literal"],"馬年獸")
        self.assertIsNone(roles[0]["distinct_species_count"])
        self.assertEqual(roles[1]["evidence_role"],"ADOPTION_CERTIFICATE_ITEM_NOT_LIVE_PET")
        self.assertTrue(all(r["original_native_pet_id"] is None for r in roles))
        self.assertTrue(all(not r["official_live_issuance_confirmed"] for r in roles))
        self.assertFalse(tw["secondary_mirror"]["original_operator_page_checked_successfully"])
        self.assertTrue(tw["archive_same_episode_not_two_independent_operator_sources"])
        self.assertEqual(tw["release_promotion"],"NO_NEW_OFFICIAL_IN_GAME_RELEASE_CONFIRMED")

    def test_2026_pc_year_gate_and_whole_pet_module_not_closed(self):
        a=self.a
        self.assertEqual(a["source_main_head"],"86d90ea1ba09bde7579a37d36c5bb773a7a4c8c3")
        self.assertEqual(a["scope"],"HISTORICAL_ORIGINAL_CLASSIC_2D_PC_ONLY")
        self.assertEqual(a["raw_original_proprietary_client_or_pet_master_bytes_acquired"],0)
        self.assertEqual(a["new_official_original_PC_species_verified"],0)
        self.assertIsNone(a["worldwide_official_original_PC_species_total"])
        self.assertEqual(self.y["annual_review"]["yearly_research_gate"],"NOT_YEAR_AUDITED")
        self.assertEqual(a["completion_gate"]["year_frontier"],2026)
        self.assertFalse(a["completion_gate"]["module_source_bounded_closed"])
        self.assertFalse(a["completion_gate"]["switch_to_NPC_authorized"])
        self.assertEqual(a["completion_gate"]["historical_current_blob_unmodified"],
                         "c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertIsNone(a["completion_gate"]["overall_percent"])
        self.assertIn("MOBILE_PET_RELEASES",a["unrelated_content_excluded"])
        self.assertIn("PAID_DOWNLOAD_CARRIER",a["unrelated_content_excluded"])

if __name__=="__main__": unittest.main()
