"""Check source-limited structured metadata; NOT HTTP or original-game replay."""
import json
import pathlib
import unittest
P=pathlib.Path(__file__).resolve().parents[1]/"research/recovered/STONEAGE-CN2003-CRAFTING-GUIDES-SOURCE-R1.json"
class TestCn2003Guides(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.x=json.loads(P.read_text(encoding="utf-8"))
    def test_provenance_limits(self):
        x=self.x
        self.assertEqual(x["task"],"OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-54")
        self.assertIn("NOT_TW1",x["region_version_scope"])
        self.assertEqual([s["id"] for s in x["sources"]],["S1","S2"])
        self.assertTrue(all(s["source_html_sha256"] is None and s["source_html_bytes"] is None for s in x["sources"]))
    def test_crafting_rows(self):
        rows=self.x["guide_equipment_table"]["rows"]
        self.assertEqual(len(rows),18)
        self.assertEqual([r["row"] for r in rows],list(range(1,19)))
        self.assertEqual(rows[12]["materials_order_as_listed"],["木","？","丝"])
        self.assertEqual([r for r in rows if "？" in r["materials_order_as_listed"]].__len__(),1)
        for r in rows:
            low,high=r["guide_rate_percent_range"]
            self.assertTrue(0 <= low <= high <= 100)
            self.assertIsNone(r["actual_success_frequency"])
            self.assertIsNone(r["item_id"])
    def test_overlap_but_no_runtime_proof(self):
        rows=self.x["guide_equipment_table"]["rows"]
        by_order={tuple(r["materials_order_as_listed"]):r for r in rows}
        self.assertEqual(by_order[("石","木")]["category_as_listed"],"枪")
        self.assertEqual(by_order[("木","石")]["category_as_listed"],"投掷斧")
        x=self.x["cross_source_disagreement"]
        self.assertTrue(x["unordered_material_multiset_overlap"])
        self.assertEqual(x["original_runtime_material_order_semantics"],"UNKNOWN")
        self.assertFalse(x["single_deterministic_recipe_proven"])
        self.assertFalse(x["guide_percentages_measured_in_original_game"])
    def test_seven_guide_meals(self):
        x=self.x["guide_newcomer"]
        self.assertEqual(len(x["meal_rows"]),7)
        self.assertEqual(x["meal_rows"][0]["materials_labels_as_listed"],["贝2","米2"])
        self.assertEqual(x["meal_rows"][-1]["name_as_listed"],"豪华游乐套餐")
        self.assertFalse(x["intro_crafting_example"]["guaranteed"])
        self.assertTrue(all(r["verified_result"] is None for r in x["meal_rows"]))

    def test_permanent_acceptance_receipt(self):
        import hashlib
        receipt_path=pathlib.Path(__file__).resolve().parents[1]/"research/recovered/STONEAGE-CN2003-CRAFTING-GUIDES-ACCEPTANCE-R1.json"
        receipt=json.loads(receipt_path.read_text(encoding="utf-8"))
        raw=P.read_bytes()
        git_blob=hashlib.sha1(b"blob "+str(len(raw)).encode("ascii")+b"\x00"+raw).hexdigest()
        self.assertEqual(receipt["source_report"]["git_blob_sha"],git_blob)
        self.assertEqual(receipt["source_report"]["source_raw_http_sha256"],None)
        self.assertFalse(receipt["source_report"]["source_replay_against_original_html"])
        self.assertEqual(receipt["candidate_ci"]["success_count"],receipt["candidate_ci"]["run_count"])
        self.assertEqual(receipt["main_ci"]["success_count"],receipt["main_ci"]["run_count"])
        self.assertEqual(receipt["candidate_ci"]["derived_unit_test_cases"],4)
        self.assertEqual(receipt["main_ci"]["derived_unit_test_cases"],4)
        self.assertEqual(receipt["acceptance"],"SOURCE_LIMITED_DERIVED_GUIDE_RECORD_ACCEPTED_NOT_ORIGINAL_RUNTIME")
        self.assertFalse(receipt["operational_boundaries"]["original_game_executed"])

if __name__=="__main__": unittest.main()
