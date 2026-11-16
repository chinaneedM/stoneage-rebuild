"""PET52 2001 mainland 2.0 carrier and live-issuance boundary safeguards."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"research"/"recovered"

class TestPET52(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.x=json.loads((P/"STONEAGE-PET52-CN2001-SA20-PERIOD-CARRIER-PET-RELEASE-R1.json").read_text(encoding="utf-8"))
        cls.q=json.loads((P/"STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json").read_text(encoding="utf-8"))

    def test_exact_announced_dates_not_native_execution(self):
        x=self.x
        self.assertEqual((x["historical_year"],x["region"],x["operator"]),(2001,"CN","BEIJING_WAEI"))
        e=x["source_operator_notice"]["events"]
        self.assertEqual([(a["date"],a["time_local"]) for a in e],[("2001-10-29","09:00"),("2001-11-01","09:00"),("2001-11-01","09:00")])
        self.assertTrue(all(a["actually_executed_proven"] is False for a in e))
        self.assertIsNone(x["source_operator_notice"]["exact_article_publication_day"])
        self.assertFalse(x["source_upgrade_guide"]["all_server_transition_as_done_proven"])

    def test_advertised_period_sources_not_obtained_client_files(self):
        s=self.x["source_upgrade_guide"]
        rows=s["advertised_carriers"]
        self.assertEqual(len(rows),13)
        self.assertEqual((s["periodical_or_disc_carriers"],s["guide_publication_carriers"]),(11,2))
        self.assertEqual(set(r["ordinal"] for r in rows),set(range(1,14)))
        self.assertEqual(len(set(r["source_name"] for r in rows)),13)
        self.assertTrue(all(r["original_disc_bytes_acquired"] is False and r["original_disc_sha256"] is None for r in rows))
        self.assertTrue(all(r["proven_same_build_client_pet_table"] is False for r in rows))
        self.assertEqual(len(self.x["prior_work_not_newly_recovered"]),3)
        self.assertTrue(self.x["prior_waei_cn_site_archive_relayed_taiwan_2_0_promotion_not_china_deployment"])

    def test_pet_raffle_announcement_not_actual_delivery(self):
        p=self.x["pet_release_evidence"]
        self.assertTrue(p["red_pet_raffle_registration_announcement"])
        self.assertFalse(p["actual_red_pet_winner_and_delivery_verified"])
        self.assertFalse(p["original_server_or_same_build_gameplay_proven"])
        self.assertEqual((p["new_original_2001_client_bytes"],p["new_named_official_live_release_proofs"]),(0,0))
        self.assertIsNone(p["historical_2001_official_species_total"])

    def test_no_frontier_or_current_state_promotion(self):
        q=self.q
        # PET52 is a historical receipt: newer PET milestones may advance the frontier.
        self.assertGreaterEqual(q["current_frontier"]["year"],2001)
        self.assertRegex(q["current_frontier"]["next"],r"^PET\d+:")
        self.assertIn(next(y for y in q["yearly_work_queue"] if y["year"]==2001)["research_gate"],
                      {"NOT_YEAR_AUDITED","SOURCE_BOUNDED_REVIEWED"})
        ids=[r["id"] for r in q["root_source_census_receipts"]]
        self.assertEqual(ids.count("PET52-2001-CN-SA20-CARRIER-RELEASE-20261116"),1)
        self.assertIn("PET51-2001-TWCN-2_0-PET-MUSEUM-SOURCE-20261116",ids)
        self.assertLess(ids.index("PET51-2001-TWCN-2_0-PET-MUSEUM-SOURCE-20261116"),
                        ids.index("PET52-2001-CN-SA20-CARRIER-RELEASE-20261116"))
        self.assertIn(q["current_frontier"]["latest_partial_root_review"],ids)
        self.assertEqual(self.x["baseline"]["current_state_blob_sha"],"c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertFalse(self.x["year_2001_review_finished"])
        self.assertEqual(self.x["stage_A"],"7_PARTIAL_2_OPEN")
        self.assertEqual(self.x["stage_B_wiki"],"GATED")
        self.assertIsNone(self.x["overall_completion_percent"])

if __name__=="__main__":
    unittest.main()
