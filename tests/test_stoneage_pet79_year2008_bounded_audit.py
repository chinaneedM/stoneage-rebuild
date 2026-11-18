"""PET79: 2008 Korean official pet and bounded five-region chronology handoff."""
import json, hashlib, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
REC = ROOT / "research" / "recovered"
def load(name):
    return json.loads((REC / name).read_text(encoding="utf-8"))
class TestPet79(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = load("STONEAGE-PET79-YEAR2008-FIVE-REGION-SOURCE-BOUNDED-AUDIT-R1.json")
        cls.q = load("STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json")
    def test_year_gate_historical_not_complete(self):
        a, q = self.a, self.q
        y = q["yearly_work_queue"][2008-1999]
        self.assertEqual((a["year_frontier_before"],a["year_frontier_after"]),(2008,2009))
        self.assertGreaterEqual(q["current_frontier"]["year"],2009)
        self.assertEqual(y["research_gate"],"SOURCE_BOUNDED_REVIEWED")
        self.assertFalse(y["historically_complete"])
        self.assertIsNone(y["historical_species_count"])
        self.assertEqual(y["source_bounded_review_receipt"],"research/recovered/STONEAGE-PET79-YEAR2008-FIVE-REGION-SOURCE-BOUNDED-AUDIT-R1.json")
        self.assertEqual(q["yearly_work_queue"][2009-1999]["research_gate"],"NOT_YEAR_AUDITED" if q["current_frontier"]["year"]==2009 else "SOURCE_BOUNDED_REVIEWED")
    def test_doedic_named_but_not_icecastle_nine(self):
        s = {x["id"]:x for x in self.a["source_records"]}
        self.assertEqual(s["KR-2008-1117-DOEDIC"]["original_pet_name"],"도에디크")
        self.assertEqual(s["KR-2008-1117-DOEDIC"]["quest_name"],"설녀의 전설")
        self.assertEqual(s["KR-2008-1117-DOEDIC"]["minimum_level"],80)
        self.assertTrue(s["KR-2008-1117-DOEDIC"]["obtainable_on_completion_announced"])
        self.assertFalse(s["KR-2008-1117-DOEDIC"]["icecastle_nine_membership_proven"])
        self.assertEqual(s["KR-2008-0114-ICECASTLE"]["original_nine_names_recovered"],0)
        self.assertTrue(s["KR-2008-0825-TARIEN"]["distinct_from_ice_castle"])
        self.assertEqual(s["KR-2008-0825-TARIEN"]["pet_reward_names_recovered"],0)
    def test_five_region_reopen_and_zero_native_bytes(self):
        a, q = self.a, self.q
        y = q["yearly_work_queue"][9]
        self.assertEqual(set(a["region_reviews"]),{"CN","TW","JP","KR","OTHER"})
        self.assertEqual(y["residual_reopen_triggers"],a["five_region_reopen_triggers"])
        self.assertEqual(len(a["five_region_reopen_triggers"]),5)
        for region, r in a["region_reviews"].items():
            self.assertIsNone(r["pet_population"])
            self.assertEqual(r["reopen_trigger"],y["region_source_reviews"][region]["reopen_trigger"])
            self.assertEqual(r["native_pet_id_rows_verified"],0)
        self.assertIsNone(a["global_2008_historical_species_count"])
        self.assertIsNone(a["confirmed_2008_first_new_species_count"])
        self.assertEqual((a["original_2008_client_bytes_acquired"],a["new_2008_native_pet_ids"],a["real_2008_reward_grant_logs"]),(0,0,0))
        self.assertTrue(all(a["boundaries"].values()))
    def test_immutable_receipts_and_large_state(self):
        a, q = self.a, self.q
        y = q["yearly_work_queue"][9]
        self.assertEqual([r["id"] for r in y["partial_source_review_receipts"]][-3:],a["prior_partial_receipts"]+[a["id"]])
        self.assertEqual(sum(r["id"]==a["id"] for r in q["root_source_census_receipts"]),1)
        self.assertEqual(len({r["id"] for r in q["root_source_census_receipts"]}),len(q["root_source_census_receipts"]))
        raw = (ROOT / "docs" / "CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(raw),2709173)
        self.assertEqual(hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\x00"+raw).hexdigest(),"c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertEqual((a["stage_A"],a["stage_B_wiki"],a["r79"]),("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING"))
if __name__ == '__main__': unittest.main()
