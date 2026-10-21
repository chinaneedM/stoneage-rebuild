"""R56 derived web-guide source integrity only; no HTTP or game runtime replay."""
import json
import pathlib
import unittest

P = pathlib.Path(__file__).resolve().parents[1] / "research/recovered/STONEAGE-CN2004-PET-SKILL-TRAINER-SOURCE-R1.json"

class TestCn2004PetSkillTrainerSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.x = json.loads(P.read_text(encoding="utf-8"))

    def test_sources_and_non_execution(self):
        d = self.x
        self.assertEqual(d["task"], "OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-56")
        self.assertIn("NOT_SAME_CLIENT_BUILD", d["scope"])
        self.assertEqual([s["id"] for s in d["sources"]], ["S1", "S2"])
        self.assertEqual(d["sources"][0]["page_date"], "2004-02-23 15:24")
        self.assertIsNone(d["sources"][1]["page_date"])
        for s in d["sources"]:
            self.assertIsNone(s["raw_html_sha256"])
            self.assertIsNone(s["raw_http_bytes"])
        self.assertFalse(d["source_replay"]["original_game_executed"])
        self.assertFalse(d["source_replay"]["raw_http_bytes_retrieved"])

    def test_complete_s1_visible_rows(self):
        a = self.x["first_guide_trainer_rows"]
        self.assertEqual(len(a), 19)
        self.assertEqual([row["row_index"] for row in a], list(range(1, 20)))
        self.assertEqual(a[2]["trainer_location_as_page"], "各村庄都有、达那除外")
        self.assertEqual((a[6]["name_as_page"], a[6]["listed_price"]), ("猛毒攻击", 4400))
        self.assertEqual((a[16]["name_as_page"], a[16]["listed_price"]), ("地球一周", 2399))
        for r in a:
            self.assertIsNone(r["original_skill_id"])
            self.assertIsNone(r["source_client_build"])
            self.assertFalse(r["source_execution_verified"])

    def test_bounded_s2_supplement(self):
        b = self.x["second_guide_selected_rows"]
        self.assertEqual(len(b), 11)
        self.assertEqual((b[0]["name_as_page"], b[0]["listed_price"]), ("猛毒攻击", 4000))
        self.assertEqual((b[1]["name_as_page"], b[1]["listed_price"]), ("一击必杀", 2500))
        self.assertEqual((b[-2]["name_as_page"], b[-2]["listed_price"]), ("修复", 359))
        self.assertEqual(b[-1]["name_as_page"], "镶宝石")
        for r in b:
            self.assertFalse(r["confirmed_same_exact_version_as_S1"])
            self.assertIsNone(r["original_skill_id"])

    def test_conflicts_survive_without_version_merging(self):
        q = {t["topic"]: t for t in self.x["crosssource_tensions"]}
        self.assertEqual(len(q), 5)
        c = q["POISON_STATS_AND_PRICE"]
        self.assertEqual((c["s1_claim"]["attack_reduction_percent"], c["s1_claim"]["poison_turns"], c["s1_claim"]["price"]), (30, 3, 4400))
        self.assertEqual((c["s2_claim"]["attack_reduction_percent"], c["s2_claim"]["poison_turns"], c["s2_claim"]["price"]), (50, 5, 4000))
        r = q["RIDING_COURSE_LEVEL_COUNT"]
        self.assertEqual((r["s1_claim"]["number_of_course_levels"], r["s2_claim"]["number_of_course_levels"]), (4, 3))
        self.assertIsNone(r["exact_dates_or_patch_cause"])
        self.assertTrue(all(v["do_not_merge"] and not v["same_build_proven"] for v in q.values()))
        self.assertFalse(q["TRAVEL_COMPANION_WORDING"]["target_equivalence_proven"])

    def test_prior_domains_not_overclaimed(self):
        self.assertFalse(self.x["crossdomain_links"][0]["crafting_success_rate_proven_by_join"])
        self.assertFalse(self.x["crossdomain_links"][1]["shell_item_specifically_checked_in_S2"])
        self.assertFalse(self.x["extra_claims"]["s2_pet_mail"]["actual_server_validation"])
        self.assertFalse(self.x["extra_claims"]["s1_pet_loyalty_thresholds"]["original_runtime_tested"])


    def test_permanent_receipt_matches_source_bytes(self):
        import hashlib
        p = P.parents[0] / "research/recovered/STONEAGE-CN2004-PET-SKILL-TRAINER-ACCEPTANCE-R1.json"
        receipt = json.loads(p.read_text(encoding="utf-8"))
        raw = P.read_bytes()
        info = receipt["derived_source"]
        self.assertEqual(len(raw), info["raw_utf8_bytes"])
        self.assertEqual(hashlib.sha256(raw).hexdigest(), info["raw_sha256"])
        self.assertEqual(info["native_git_blob_sha1"], "b6f42811c23cadc8b80fabb0a53b98a6aa9e8b2f")
        self.assertTrue(info["persisted_in_git"])
        self.assertFalse(info["contains_original_html_or_game_assets"])
        self.assertIsNone(receipt["web_sources"][0]["raw_http_sha256"])
        self.assertIsNone(receipt["web_sources"][1]["raw_http_sha256"])
        self.assertEqual(receipt["candidate_validation"]["run_artifacts_count"], 0)
        self.assertEqual(receipt["main_validation"]["run_artifacts_count"], 0)
        self.assertTrue(receipt["claim_boundaries"]["history_not_rewritten"])

if __name__ == "__main__":
    unittest.main()
