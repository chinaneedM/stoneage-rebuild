"""R59 contemporaneous portal career examples are NOT original server rules."""
import json
from pathlib import Path
import unittest

SOURCE = Path(__file__).resolve().parents[1] / "research/recovered/STONEAGE-CN2003-PROFESSION-DEPENDENCIES-SOURCE-R1.json"

class TestCn2003ProfessionDependencies(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_two_editorial_sources_not_original_html(self):
        d = self.d
        self.assertEqual(d["task"], "OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-59")
        self.assertEqual([s["id"] for s in d["sources"]], ["S1", "S2"])
        self.assertTrue(all(not s["raw_http_saved"] and s["original_http_sha256"] is None for s in d["sources"]))
        self.assertTrue(all("PORTAL" in s["class"] for s in d["sources"]))

    def test_three_professions_and_shared_skills(self):
        p = self.d["profession_names"]
        self.assertEqual([x["id"] for x in p], ["MAGE", "HUNTER", "WARRIOR"])
        self.assertEqual([x["s1_listed_tier_counts"] for x in p], [[8,7,5,1],[7,7,5,2],[7,9,5]])
        self.assertEqual([x["s2_visible_skill_name_count"] for x in p], [21,19,20])
        self.assertEqual(len(self.d["shared_skill_labels_from_s2"]), 3)

    def test_nine_scoped_explicit_examples(self):
        e = self.d["prerequisite_examples"]
        self.assertEqual(len(e), 9)
        self.assertEqual(len({x["id"] for x in e}), 9)
        self.assertTrue(all(x["source"] == "S1" and not x["original_server_verified"] for x in e))
        by = {x["id"]: x for x in e}
        self.assertEqual(by["HUNTER_POISON_WEAPON"]["prerequisite_group_type"], "ANY_ONE")
        self.assertEqual(len(by["HUNTER_POISON_WEAPON"]["prerequisites"]), 3)
        self.assertEqual(by["WARRIOR_DUAL_WIELD"]["prerequisite_group_type"], "ALL")
        self.assertEqual(len(by["WARRIOR_DUAL_WIELD"]["prerequisites"]), 2)
        self.assertEqual(len(by["MAGE_POSSESSION"]["prerequisites"]), 4)
        self.assertEqual(by["HUNTER_CORPSE"]["level_addendum"]["profession_level_min"], 5)
        self.assertEqual(by["HUNTER_CORPSE"]["prerequisites"], [])
        self.assertTrue(all(x["reported_proficiency_min"] == 70 for e in self.d["prerequisite_examples"] for x in e["prerequisites"]))

    def test_ambiguities_never_resolved_as_same_ids(self):
        a = {x["kind"]: x for x in self.d["ambiguities"]}
        self.assertEqual(len(a), 8)
        self.assertFalse(a["MAGE_NEEDLE_NAME_CONFLICT"]["same_skill_id_proven"])
        self.assertFalse(a["HUNTER_TAMING_LABEL"]["same_skill_id_proven"])
        self.assertFalse(a["SPELL_ALIASES_NOT_CANONICAL"]["same_skill_id_proven"])
        self.assertEqual(a["HUNTER_LEVEL_5_EXCEPTION"]["s1_corpse_skill_profession_level_min"], 5)
        self.assertFalse(a["SKILL_TIER_COUNTERS_NOT_EXECUTION"]["same_complete_skill_pool_proven"])
        self.assertFalse(a["PAGE_TABLE_TEXT_COLLAPSE"]["exact_fourth_tier_dependency_edges_from_flattened_table_proven"])

    def test_not_claim_original_server_or_new_game(self):
        self.assertTrue(all(v is False for v in self.d["negative_claims"].values()))
        self.assertFalse(self.d["s1_summary"]["original_server_verified"])
        self.assertEqual(self.d["next"], "OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-60")


    def test_receipt_immutable_derived_source_not_original_html(self):
        import hashlib
        receipt = SOURCE.parent / "STONEAGE-CN2003-PROFESSION-DEPENDENCIES-ACCEPTANCE-R1.json"
        r = json.loads(receipt.read_text(encoding="utf-8"))
        b = SOURCE.read_bytes()
        info = r["source_derived"]
        self.assertEqual(len(b), info["utf8_byte_length"])
        self.assertEqual(hashlib.sha256(b).hexdigest(), info["raw_sha256"])
        actual_git_blob = hashlib.sha1(b"blob " + str(len(b)).encode() + b"\\0" + b).hexdigest()
        self.assertEqual(actual_git_blob, info["git_blob_sha1"])
        self.assertEqual(info["git_blob_sha1"], "055e169a8ca632022aa85598f175945cedd31ddb")
        self.assertEqual(info["record_count_example_prerequisites"], 9)
        self.assertTrue(info["persisted_in_git"])
        self.assertFalse(info["contains_original_html_or_game_assets"])
        for s in r["web_sources"]:
            self.assertIsNone(s["original_http_sha256"])
            self.assertFalse(s["original_source_replay"])
        self.assertTrue(r["source_scope_not_advanced_by_ci"])
        self.assertTrue(r["old_history_prefix_preserved"])
        self.assertEqual(r["candidate_validation"]["artifact_count"], 0)
        self.assertEqual(r["main_validation"]["artifact_count"], 0)


if __name__ == "__main__":
    unittest.main()
