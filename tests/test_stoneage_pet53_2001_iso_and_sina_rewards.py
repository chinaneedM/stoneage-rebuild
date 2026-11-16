"""PET53: distinguish a catalogue-advertised ISO and planned pet prizes from original client/issuance proof."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"research"/"recovered"

class PET53Year2001(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.x=json.loads((P/"STONEAGE-PET53-2001-CN-ISO-CARRIER-AND-SINA-PET-PRIZES-R1.json").read_text(encoding="utf-8"))
        cls.q=json.loads((P/"STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json").read_text(encoding="utf-8"))

    def test_iso_sha1_is_a_claim_not_verified_game_client(self):
        x=self.x
        f=x["client_search_boundary"]["new_nearby_unverified_coverdisc"]
        self.assertEqual(f["listing_iso_filename"],"PCFan200111.iso")
        self.assertEqual(f["listing_exact_byte_size"],654030848)
        self.assertEqual(f["listing_sha1"],"A69EECB5A1C3FB4A5B69D9A2128A8BE82F6D51E0")
        self.assertFalse(f["claimed_hash_verified_against_bytes"])
        self.assertFalse(f["original_iso_downloaded_this_unit"])
        self.assertFalse(f["game_client_inside_iso_verified"])
        self.assertFalse(f["client_file_tree_available"])
        self.assertIsNone(x["contemporaneous_distribution_campaign"]["prize_pet_name_or_native_id"])
        self.assertEqual(x["client_search_boundary"]["no_new_authenticated_2001_original_client_bytes"],0)
        self.assertIn("UNRESOLVED",f["related_to_17173_电脑报_游戏世界_claim"])

    def test_2001_sina_planned_rewards_not_proven_actual_distribution(self):
        v=self.x["contemporaneous_distribution_campaign"]
        tiers=v["offered_prize_categories"]
        self.assertEqual([t["slots"] for t in tiers],[1,3,9,27])
        self.assertEqual(sum(t["slots"] for t in tiers),40)
        self.assertEqual(v["advertised_prize_slots"],40)
        self.assertEqual(v["claimed_pet_prize_label"],"梦幻宠物")
        self.assertFalse(v["same_pet_species_in_all_slots_proven"])
        self.assertFalse(v["per_species_historic_official_release_claim"])
        self.assertIsNone(v["independently_confirmed_nominated_winners_count"])
        self.assertEqual(v["independently_verified_actual_pet_award_count"],0)
        self.assertIn("FRAMESET_ONLY",v["clickthrough_observation"])

    def test_country_and_earlier_censuses_not_silently_promoted(self):
        x=self.x
        self.assertTrue(x["no_bridge_from_separately_announced_red_pet_raffle_to_unnamed_sina_dream_pet"])
        self.assertTrue(x["no_identity_bridge_from_taiwan_version_to_mainland_campaign"])
        self.assertEqual(len(x["client_search_boundary"]["existing_prior_disc_censuses"]),4)
        self.assertEqual(x["new_qualifying_official_live_pet_release_proofs"],0)
        self.assertIsNone(x["historical_2001_official_pet_population"])
        self.assertEqual((x["active_content_module"],x["historical_year"],x["region"]),("PET",2001,"CN"))

    def test_append_only_chronology_and_immutable_current_state(self):
        x,q=self.x,self.q
        self.assertGreaterEqual(q["current_frontier"]["year"],2001)
        self.assertIn(next(y for y in q["yearly_work_queue"] if y["year"]==2001)["research_gate"],{"NOT_YEAR_AUDITED","SOURCE_BOUNDED_REVIEWED"})
        ident="PET53-CN2001-PCFAN-ISO-SINA-FAMILY-PET-PRIZES-20261116"
        receipts=[r["id"] for r in q["root_source_census_receipts"]]
        self.assertEqual(receipts.count(ident),1)
        self.assertIn("PET52-2001-CN-SA20-CARRIER-RELEASE-20261116",receipts)
        self.assertLess(receipts.index("PET52-2001-CN-SA20-CARRIER-RELEASE-20261116"),receipts.index(ident))
        self.assertEqual(x["baseline"]["current_state_blob"],"c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertEqual(x["baseline"]["current_state_bytes"],2709173)
        self.assertEqual((x["stage_A"],x["stage_B_wiki"],x["r79"]),("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING"))
        self.assertIsNone(x["overall_completion_percent"])

if __name__=="__main__":
    unittest.main()
