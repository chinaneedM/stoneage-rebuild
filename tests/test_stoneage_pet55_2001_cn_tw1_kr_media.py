"""PET55: only source-graded 2001 CN player to authenticated TW1 names; KR 2002 review is not official original client."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"research"/"recovered"
ID="PET55-2001-KR20-CNPLAYER-TW1SPR-20261116"

class TestPET55(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.x=json.loads((P/"STONEAGE-PET55-2001-KR20-CNPLAYER-TW1-SPR-R1.json").read_text(encoding="utf-8"))
        cls.tw=json.loads((P/"STONEAGE-PET46-TW1-ALBUM-NAME-2D-CROSSWALK-R1.json").read_text(encoding="utf-8"))
        cls.old=json.loads((P/"STONEAGE-EARLY-MEDIA-ARTICLE-PET-SOURCE-R1.json").read_text(encoding="utf-8"))
        cls.q=json.loads((P/"STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json").read_text(encoding="utf-8"))

    def test_previously_registered_player_page_not_species_count(self):
        x=self.x["player_2001_cn_list"]
        self.assertEqual((x["visible_date_label"],x["byline"],len(x["derived_source_rows"])),("2001-06-14","俄罗斯牛奶",20))
        self.assertTrue(x["previously_registered"])
        self.assertFalse(x["original_2001_HTML_bytes_recovered"])
        self.assertFalse(x["player_capture_probability_as_native_logic"])
        self.assertTrue(all(z["verified_original_server_pet_id"] is None and z["claimed_in_game_release_confirmed"] is False for z in x["derived_source_rows"]))
        self.assertEqual({z["position"] for z in x["derived_source_rows"]},set(range(1,21)))
        self.assertIn("MEDIA17173_20010614_CATCH_GUIDE",{z["id"] for z in self.old["sources"]})

    def test_seven_name_links_replay_exact_prior_tw1_original_hashes(self):
        x=self.x["graded_cross_source_links"]
        links=x["rows"]
        self.assertEqual((len(links),x["exact_text"],x["simplified_script"],x["different_player_page_alias"]),(7,2,2,3))
        self.assertEqual(x["remaining_unlinked_source_rows"],13)
        self.assertEqual(x["actual_CN2001_native_build_pet_id_matches"],0)
        self.assertEqual(x["official_live_2001_pets_proven_by_links"],0)
        original={z["graphic_number"]:z for z in self.tw["candidate_records"]}
        older={z["source_row_ordinal"]:z for z in self.old["pet_name_candidates"]}
        seen_spr=set()
        for link in links:
            row=original[link["TW1_original_local_graphic"]]
            self.assertEqual(link["TW1_original_client_album_name"],row["client_original_album_name"])
            self.assertEqual(link["TW1_original_album_row_sha256"],row["client_original_album_row_sha256"])
            self.assertEqual(link["TW1_original_complete_SPR_sha256"],row["pet07_original_whole_SPR_sha256"])
            self.assertEqual(link["TW1_original_animation_count"],row["pet07_source_total_animations"])
            self.assertEqual(len(link["TW1_original_complete_SPR_sha256"]),64)
            self.assertNotIn(link["TW1_original_complete_SPR_sha256"],seen_spr)
            seen_spr.add(link["TW1_original_complete_SPR_sha256"])
            self.assertFalse(link["qualified_CN2001_same_build_identity"])
            self.assertFalse(link["qualified_CN2001_live_pet_release"])
            if link["grade"]=="EXACT":
                self.assertEqual(link["source_name"],link["TW1_original_client_album_name"])
            if link["grade"]=="PLAYER_ALIAS":
                prior=older[link["earlier_player_alias_source_row"]]
                self.assertEqual(link["earlier_player_alias_source_label"],prior["source_name"])
                self.assertIn(link["source_name"],prior["source_name"])
        self.assertEqual(len(seen_spr),7)

    def test_korean_2001_december_period_does_not_become_exact_build_or_roster(self):
        k=self.x["Korean_2_0_editorial"]
        self.assertEqual((k["published"],k["reported_upgrade_period"],k["reported_operator"],k["previous_release_label"]),("2002-03-30T10:04:42","2001-12","INIUM","1.74"))
        self.assertEqual(k["source_grade"],"NEAR_PERIOD_EDITORIAL_REVIEW_NOT_2001_FIRST_PARTY_CHANGELOG")
        self.assertIsNone(k["exact_2001_deployment_date"])
        self.assertIsNone(k["original_installer_build_sha"])
        self.assertFalse(k["phrase_is_exact_species_count"])
        self.assertTrue(k["pet_riding_limited_to_subset"])
        self.assertFalse(k["named_official_live_KR2001_pet_issuance_proven"])
        self.assertTrue(k["different_from_TW_CN_2_0_build_unresolved"])

    def test_year_pets_only_and_all_history_append_only(self):
        x,q=self.x,self.q
        ids=[i["id"] for i in q["root_source_census_receipts"]]
        self.assertEqual(ids.count(ID),1)
        self.assertEqual(ids.count("PET54-2001-CNTW-PELUXIA-NAME-REWARD-CONFLICT-20261116"),1)
        self.assertLess(ids.index("PET54-2001-CNTW-PELUXIA-NAME-REWARD-CONFLICT-20261116"),ids.index(ID))
        self.assertEqual(q["active_module"],"PET")
        self.assertGreaterEqual(q["current_frontier"]["year"],2001)
        self.assertIn(next(z for z in q["yearly_work_queue"] if z["year"]==2001)["research_gate"],{"NOT_YEAR_AUDITED","SOURCE_BOUNDED_REVIEWED"})
        self.assertEqual((x["new_2001_client_bytes"],x["new_official_living_pet_identities"]),(0,0))
        self.assertIsNone(x["historical_2001_worldwide_pet_total"])
        self.assertEqual(x["baseline"]["current_sha"],"c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertEqual(x["baseline"]["current_bytes"],2709173)
        self.assertEqual((x["stage_A"],x["stage_B_wiki"],x["r79"]),("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING"))
        self.assertIsNone(x["overall_percent"])

if __name__=="__main__":
    unittest.main()
