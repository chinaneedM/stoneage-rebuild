"""PET120: 2020 source-bounded original-PC six-region audit and 2021 handoff."""
import json
import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REC = ROOT / "research/recovered"
AUDIT = REC / "STONEAGE-PET120-YEAR2020-SIX-REGION-CLASSIC-PC-BOUNDED-AUDIT-R1.json"
QUEUE = REC / "STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json"
REPORT = ROOT / "docs/continuity/STONEAGE-PET120-YEAR2020-SIX-REGION-CLASSIC-PC-BOUNDED-AUDIT-20261119.md"
REGIONS = {"CN","TW","HK_MO","KR","JP","OTHER"}

class Pet120Year2020SourceBounded(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=json.loads(AUDIT.read_text(encoding="utf-8"))
        cls.q=json.loads(QUEUE.read_text(encoding="utf-8"))

    def test_forward_only_2020_review_and_2021_earliest_year(self):
        a,q=self.a,self.q
        y=next(v for v in q["yearly_work_queue"] if v["year"]==2020)
        n=next(v for v in q["yearly_work_queue"] if v["year"]==2021)
        self.assertEqual((a["year_frontier_before"],a["year_frontier_after"]),(2020,2021))
        self.assertEqual(y["research_gate"],"SOURCE_BOUNDED_REVIEWED")
        self.assertIn(n["research_gate"],{"NOT_YEAR_AUDITED","SOURCE_BOUNDED_REVIEWED"})  # subsequent PET121 annual audit is forward-only
        self.assertGreaterEqual(q["current_frontier"]["year"],2021)
        self.assertEqual(q["active_module"],"PET")
        self.assertFalse(a["historically_complete"])
        self.assertFalse(y["historically_complete"])
        self.assertTrue(a["year_reopenable"])
        self.assertIsNone(a["original_pc_global_2020_species_count"])
        self.assertIsNone(a["original_pc_2020_first_release_species_count"])
        self.assertIsNone(y["historical_species_count"])
        self.assertEqual(y["source_bounded_review_receipt"],str(AUDIT.relative_to(ROOT)))
        self.assertIn(a["id"],[x["id"] for x in y["partial_source_review_receipts"]])
        self.assertIn(a["id"],[x["id"] for x in q["root_source_census_receipts"]])
        self.assertIn("PET119-TW2020-RAT-FESTIVAL-AND-KR-WORLD-MOBILE-SEPARATION-20261119",
                      [x["id"] for x in y["partial_source_review_receipts"]])
        self.assertGreaterEqual(int(q["current_frontier"]["next"].split(":")[0][3:]),121)

    def test_six_regions_original_pc_reopen_and_no_native_species_promotion(self):
        a,q=self.a,self.q
        self.assertEqual(set(a["region_reviews"]),REGIONS)
        y=next(v for v in q["yearly_work_queue"] if v["year"]==2020)
        self.assertEqual(set(y["region_source_reviews"]),REGIONS-{"HK_MO"})
        self.assertEqual(set(y["additional_region_reviews"]),{"HK_MO"})
        for region,v in a["region_reviews"].items():
            qv=y["region_source_reviews"].get(region) or y["additional_region_reviews"][region]
            self.assertEqual(qv["reopen_trigger"],v["reopen_trigger"])
            self.assertIsNone(qv["pet_population"])
            self.assertIsNone(qv["official_2020_first_release_species_count"])
            self.assertFalse(qv["historically_complete"])
            self.assertEqual(qv["native_pet_id_rows_verified"],0)
        for k in ("new_original_pc_client_bytes","new_original_pc_patch_bytes",
                  "new_native_pet_id_rows","new_original_pc_spr_frames",
                  "new_native_skill_functions","new_original_server_pet_grants"):
            self.assertEqual(a[k],0)
        self.assertTrue(all(a["negative_controls"].values()))

    def test_no_mutable_list_as_original_operator_or_mobile_as_pc(self):
        a=self.a
        sources={x["id"]:x for x in a["sources"]}
        self.assertEqual(len(sources),len(a["sources"]))
        self.assertIn("NOT_INDEPENDENT",sources["TW2020-JUL01-LV1-SAME-MOBILE"]["grade"])
        self.assertIn("EDIT",sources["TW2020-AUG29-EDITABLE-LIST"]["grade"])
        self.assertIn("那提拉",sources["TW2020-AUG29-EDITABLE-LIST"]["claim"])
        self.assertIn("未開放",sources["TW2020-AUG29-EDITABLE-LIST"]["claim"])
        self.assertIn("2017",sources["TW2017-OLDER-MART"]["id"])
        self.assertIn("NOT_2020_FIRST",a["source_boundaries"]["older_same_name"])
        self.assertIn("MOBILE",sources["KR2020-WORLD-MOBILE-ONLY"]["grade"])
        self.assertIn("2020",REPORT.read_text(encoding="utf-8"))
        self.assertIn("PET120",(ROOT/"docs/STONEAGE-PET-CHRONOLOGICAL-RESTORATION-ORDER-R1.md").read_text(encoding="utf-8"))

    def test_historical_state_blob_preserved_exactly(self):
        a,q=self.a,self.q
        raw=(ROOT/"docs/CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(raw),a["baseline"]["current_state_bytes"])
        sha=hashlib.sha1(b"blob "+str(len(raw)).encode("ascii")+b"\x00"+raw).hexdigest()
        self.assertEqual(sha,a["baseline"]["current_state_blob"])
        self.assertEqual((a["stage_A"],a["stage_B_wiki"],a["r79"],a["overall_percent"]),
                         (q["stage_A"],q["stage_B_wiki"],q["r79"],q["overall_game_completion_percent"]))

if __name__=="__main__":
    unittest.main()
